"""
Multi-model content generation comparison with two LLM judges.

Steps:
  1. Load 15 existing Llama 3.3 70B outputs from content_generation_eval.csv
  2. Generate 15 outputs with GPT-4.1 Mini (checkpointed)
  3. Generate 15 outputs with GPT-4.1 Nano  (checkpointed)
  4. Score all 45 outputs with Judge A (GPT-4.1 Mini) and Judge B (GPT-4o Mini)
  5. Write eval/content_model_comparison.csv with blank human_* columns
  6. Print summary table

Run:
  cd /Users/shobhit/Documents/padhai/shikshabot
  python eval/compare_content_models.py
"""
import csv, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from openai import OpenAI
import config

client = OpenAI(api_key=config.OPENAI_API_KEY)

EVAL_DIR       = os.path.join(os.path.dirname(__file__))
CHECKPOINT_DIR = os.path.join(EVAL_DIR, "checkpoints")
os.makedirs(CHECKPOINT_DIR, exist_ok=True)

METRICS = [
    "sections_complete",
    "time_allocated",
    "content_accurate",
    "ncert_aligned",
    "grade_appropriate",
    "sel_integrated",
    "sel_dimension_matched",
    "sel_has_reflection",
    "culturally_relevant",
]

SEL_DISPLAY = {
    "growth_mindset":       "Growth Mindset (विकास की सोच)",
    "persistence":          "Persistence (दृढ़ता)",
    "self_awareness":       "Self-awareness (आत्म-जागरूकता)",
    "emotional_regulation": "Emotional Regulation (भावना नियंत्रण)",
    "social_awareness":     "Social Awareness (सामाजिक जागरूकता)",
}

GEN_PROMPT = """You are ShikshaBot, an educational assistant for Indian government school teachers.
Generate a complete 45-minute SEL-integrated lesson plan strictly following NCERT curriculum.

Subject : {subject}
Chapter/Topic: {topic}
Grade   : Class {grade}
SEL Focus: {sel_label}
Language: Hindi

Structure the lesson plan EXACTLY as follows (in Hindi):

विषय: [chapter name] (Subject + SEL Integration)
कक्षा: [grade]
समय: 45 मिनट
SEL Skills: [list the SEL skills to be developed]

---

1. Check-in + Mindfulness (10 मिनट)

(पहले 5 मिनट) भावनात्मक Check-in: [title]
गतिविधि: [activity name]
[2-3 discussion questions]
SEL Skill: [skill name]

---

(अगले 5 मिनट) Mindfulness: [title linked to lesson theme]
[Guided imagination activity with 2-3 questions. No physical props.]
SEL Skill: [skill name]

---

2. NCERT Content Learning (25 मिनट)

Concept 1: [concept name] (8 मिनट)
NCERT: [one-line NCERT fact]
[Teacher discussion and examples]
SEL Integration Question: [one question linking concept to SEL]

---

Concept 2: [concept name] (8 मिनट)
NCERT: [one-line NCERT fact]
Activity: [activity name]
[Activity description]
SEL Skill: [skill name]

---

Concept 3: [concept name] (9 मिनट)
[Discussion with SEL integration]
SEL Skill: [skill name]

---

3. Group Activity + Reflection (10 मिनट)

Activity: [activity name]
[Group activity: groups of 4-5, step-by-step]
Reflection Questions:
1. [question]
2. [question]
3. [question]

---

4. Revision + Way Forward (Last 5 मिनट)

Quick Recap:
Teacher पूछें:
1. [question]
2. [question]
3. [question]

Exit Ticket:
बच्चे एक लाइन लिखें: "आज से मैं __ रहूँगा/रहूँगी।"

---

Keep SEL woven into academic content — do NOT add a separate SEL section.
Use India-relevant examples only (no pizza, no US references).
Mindfulness = guided imagination only, no physical props."""

EVAL_PROMPT = """You are a quality evaluator for ShikshaBot, an educational chatbot for Indian government school teachers.

Evaluate the lesson plan on 9 binary criteria.

Lesson metadata:
- Subject: {subject}
- Topic: {topic}
- Grade: Class {grade}
- Requested SEL Dimension: {sel_dimension}

Criteria:
1. sections_complete — All 4 sections present with roughly correct time: Check-in+Mindfulness ~10min, NCERT Content ~25min with 3 concepts, Group Activity ~10min, Revision ~5min
2. time_allocated — Time in minutes explicitly written next to each section/concept heading
3. content_accurate — All NCERT facts stated are scientifically/academically correct
4. ncert_aligned — Concepts match NCERT curriculum for Class {grade} {subject}
5. grade_appropriate — Language complexity and activities suit Class {grade} students
6. sel_integrated — SEL is woven into academic content throughout, NOT as a separate standalone section
7. sel_dimension_matched — The SEL dimension "{sel_dimension}" is clearly and consistently present (not just a single mention)
8. sel_has_reflection — At least one explicit reflection question tied to the SEL dimension
9. culturally_relevant — Examples use Indian context (local food, cricket, festivals, etc.) — no exclusively Western references

Lesson plan:
{output}

Return ONLY valid JSON (no other text):
{{
  "sections_complete":     {{"verdict": true, "reason": "one sentence"}},
  "time_allocated":        {{"verdict": true, "reason": "one sentence"}},
  "content_accurate":      {{"verdict": true, "reason": "one sentence"}},
  "ncert_aligned":         {{"verdict": true, "reason": "one sentence"}},
  "grade_appropriate":     {{"verdict": true, "reason": "one sentence"}},
  "sel_integrated":        {{"verdict": true, "reason": "one sentence"}},
  "sel_dimension_matched": {{"verdict": true, "reason": "one sentence"}},
  "sel_has_reflection":    {{"verdict": true, "reason": "one sentence"}},
  "culturally_relevant":   {{"verdict": true, "reason": "one sentence"}}
}}"""

# ── Checkpoint helpers ────────────────────────────────────────────────────────────

def ckpt_path(name):
    safe = name.replace(" ", "_").replace("/", "-").replace(".", "_")
    return os.path.join(CHECKPOINT_DIR, f"cmp_{safe}.json")

def load_ckpt(name):
    p = ckpt_path(name)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return None

def save_ckpt(name, data):
    with open(ckpt_path(name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ── API calls ─────────────────────────────────────────────────────────────────────

def generate(model, subject, topic, grade, sel_dim, retries=3):
    prompt = GEN_PROMPT.format(
        subject=subject, topic=topic, grade=grade,
        sel_label=SEL_DISPLAY.get(sel_dim, sel_dim),
    )
    for attempt in range(retries):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1800,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                raise

def score(judge_model, output_text, subject, topic, grade, sel_dim, retries=3):
    prompt = EVAL_PROMPT.format(
        subject=subject, topic=topic, grade=grade,
        sel_dimension=sel_dim, output=output_text,
    )
    for attempt in range(retries):
        try:
            resp = client.chat.completions.create(
                model=judge_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=700,
                response_format={"type": "json_object"},
            )
            return json.loads(resp.choices[0].message.content)
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                print(f"  [score ERROR] {judge_model}: {e}")
                return {m: {"verdict": None, "reason": "error"} for m in METRICS}

# ── Load existing Llama outputs ───────────────────────────────────────────────────

def load_existing():
    path = os.path.join(EVAL_DIR, "content_generation_eval.csv")
    rows = {}
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows[int(row["id"])] = row
    return rows

# ── Config ────────────────────────────────────────────────────────────────────────

GEN_MODELS = [
    ("gpt-4.1-mini", "GPT-4.1 Mini"),
    ("gpt-4.1-nano", "GPT-4.1 Nano"),
]

JUDGES = [
    ("gpt-4.1-mini", "judge_mini"),
    ("gpt-4o-mini",  "judge_4omini"),
]

# ── Main ──────────────────────────────────────────────────────────────────────────

def main():
    existing = load_existing()
    ids = sorted(existing.keys())
    print(f"Loaded {len(ids)} Llama 3.3 70B outputs")

    # ── Step 1: Generate with GPT models ─────────────────────────────────────────
    gen_outputs = {"Llama 3.3 70B": {i: existing[i]["generated_output"] for i in ids}}

    for model_id, model_label in GEN_MODELS:
        ckpt = load_ckpt(f"gen_{model_label}")
        if ckpt:
            print(f"[{model_label}] checkpoint found — skipping generation")
            gen_outputs[model_label] = {int(k): v for k, v in ckpt.items()}
            continue

        print(f"\n[{model_label}] generating {len(ids)} lesson plans...")
        outputs = {}
        for i, row_id in enumerate(ids, 1):
            row = existing[row_id]
            desc = f"Class {row['grade']} {row['subject']} — {row['topic'][:30]}"
            print(f"  {i:02d}/{len(ids)} {desc}...")
            outputs[row_id] = generate(
                model_id, row["subject"], row["topic"],
                row["grade"], row["sel_dimension"],
            )
            time.sleep(0.4)

        save_ckpt(f"gen_{model_label}", {str(k): v for k, v in outputs.items()})
        gen_outputs[model_label] = outputs
        print(f"  [checkpoint saved]")

    all_gen_labels = ["Llama 3.3 70B"] + [lbl for _, lbl in GEN_MODELS]

    # ── Step 2: Score with both judges ────────────────────────────────────────────
    # all_scores[judge_key][gen_label][row_id] = {metric: {verdict, reason}}
    all_scores = {}

    for judge_id, judge_key in JUDGES:
        all_scores[judge_key] = {}
        for gen_label in all_gen_labels:
            ckpt_name = f"scores_{gen_label}_{judge_key}"
            ckpt = load_ckpt(ckpt_name)
            if ckpt:
                print(f"[Judge:{judge_key}] [{gen_label}] checkpoint found")
                all_scores[judge_key][gen_label] = {int(k): v for k, v in ckpt.items()}
                continue

            print(f"\n[Judge:{judge_key}] scoring {gen_label} ({len(ids)} outputs)...")
            scores = {}
            for i, row_id in enumerate(ids, 1):
                row = existing[row_id]
                text = gen_outputs[gen_label][row_id]
                result = score(
                    judge_id, text,
                    row["subject"], row["topic"], row["grade"], row["sel_dimension"],
                )
                passed = sum(1 for m in METRICS if result.get(m, {}).get("verdict") is True)
                print(f"  {i:02d}/{len(ids)} Class {row['grade']} {row['subject'][:15]:<15} → {passed}/9")
                scores[row_id] = result
                time.sleep(0.3)

            save_ckpt(ckpt_name, {str(k): v for k, v in scores.items()})
            all_scores[judge_key][gen_label] = scores
            print(f"  [checkpoint saved]")

    # ── Step 3: Write comparison CSV ──────────────────────────────────────────────
    fieldnames = ["id", "subject", "topic", "grade", "sel_dimension", "language", "generator", "generated_output"]
    for m in METRICS:
        for _, jk in JUDGES:
            fieldnames += [f"{m}_{jk}", f"{m}_{jk}_reason"]
    for m in METRICS:
        fieldnames.append(f"human_{m}")

    out_path = os.path.join(EVAL_DIR, "content_model_comparison.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row_id in ids:
            row = existing[row_id]
            for gen_label in all_gen_labels:
                r = {
                    "id": row_id,
                    "subject": row["subject"],
                    "topic": row["topic"],
                    "grade": row["grade"],
                    "sel_dimension": row["sel_dimension"],
                    "language": row["language"],
                    "generator": gen_label,
                    "generated_output": gen_outputs[gen_label][row_id],
                }
                for m in METRICS:
                    for _, jk in JUDGES:
                        res = all_scores[jk][gen_label][row_id].get(m, {})
                        r[f"{m}_{jk}"] = "yes" if res.get("verdict") is True else "no"
                        r[f"{m}_{jk}_reason"] = res.get("reason", "")
                for m in METRICS:
                    r[f"human_{m}"] = ""
                writer.writerow(r)

    n_rows = len(ids) * len(all_gen_labels)
    print(f"\nSaved → {out_path}  ({n_rows} rows, {len(fieldnames)} columns)")

    # ── Step 4: Summary table ─────────────────────────────────────────────────────
    print(f"\n{'='*70}")
    print("  METRIC PASS RATES  (avg across both judges)")
    print(f"{'='*70}")
    header = f"  {'Metric':<28}"
    for gl in all_gen_labels:
        header += f"  {gl[:12]:>12}"
    print(header)
    print(f"  {'─'*66}")

    def avg_pass_rate(gen_label, metric):
        vals = []
        for _, jk in JUDGES:
            passed = sum(
                1 for rid in ids
                if all_scores[jk][gen_label][rid].get(metric, {}).get("verdict") is True
            )
            vals.append(passed / len(ids))
        return sum(vals) / len(vals)

    for m in METRICS:
        line = f"  {m:<28}"
        for gl in all_gen_labels:
            line += f"  {avg_pass_rate(gl, m):>12.0%}"
        print(line)

    print(f"  {'─'*66}")
    line = f"  {'OVERALL':<28}"
    for gl in all_gen_labels:
        overall = sum(avg_pass_rate(gl, m) for m in METRICS) / len(METRICS)
        line += f"  {overall:>12.0%}"
    print(line)

    # ── Step 5: Judge agreement ───────────────────────────────────────────────────
    print(f"\n  Judge agreement (% where GPT-4.1 Mini and GPT-4o Mini agree):")
    print(f"  {'─'*50}")
    for gl in all_gen_labels:
        agree = sum(
            1 for rid in ids for m in METRICS
            if (all_scores["judge_mini"][gl][rid].get(m, {}).get("verdict") ==
                all_scores["judge_4omini"][gl][rid].get(m, {}).get("verdict"))
        )
        total = len(ids) * len(METRICS)
        print(f"  {gl:<22} {agree/total:.1%}")

    print()

if __name__ == "__main__":
    main()
