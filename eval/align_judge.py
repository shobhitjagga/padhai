"""
Align the LLM judge against human annotations from teacher_messages_evaluation.csv.

Tests 3 judge models × 2 prompt variants (baseline vs strict) = 6 combinations.
Computes per-metric precision / recall / F1 vs human ground truth.

Run:
  cd /Users/shobhit/Documents/padhai/shikshabot
  python eval/align_judge.py
"""
import csv, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from openai import OpenAI
import config

client = OpenAI(api_key=config.OPENAI_API_KEY)

EVAL_DIR       = os.path.dirname(__file__)
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

JUDGE_MODELS = [
    ("gpt-4.1-nano", "GPT-4.1 Nano"),
    ("gpt-4.1-mini", "GPT-4.1 Mini"),
    ("gpt-4o-mini",  "GPT-4o Mini"),
]

# ── Prompts ───────────────────────────────────────────────────────────────────────

BASELINE_PROMPT = """\
You are a quality evaluator for Padhai Bot, an educational chatbot for Indian school teachers.

The teacher sent this request: {query}

Evaluate the generated lesson plan on 9 binary criteria.

Criteria:
1. sections_complete — All 4 sections present: Check-in+Mindfulness ~10 min, NCERT Content ~25 min \
with 3 concepts, Group Activity ~10 min, Revision ~5 min
2. time_allocated — Time in minutes explicitly written next to each section/concept heading
3. content_accurate — All NCERT facts stated are scientifically/academically correct
4. ncert_aligned — Concepts match NCERT curriculum for the grade/subject in the teacher's request
5. grade_appropriate — Language and depth match the grade level requested
6. sel_integrated — SEL woven into academic content, NOT a separate standalone section
7. sel_dimension_matched — An SEL dimension is clearly and consistently present throughout
8. sel_has_reflection — At least one explicit reflection question tied to SEL
9. culturally_relevant — Examples use Indian context, no exclusively Western references

Lesson plan:
{output}

Return ONLY valid JSON:
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


STRICT_PROMPT = """\
You are a strict quality evaluator for Padhai Bot, an educational chatbot for Indian school teachers.
Your job is to find problems, not confirm quality. Default to false when uncertain.

The teacher's request: {query}

Evaluate the generated lesson plan on 9 binary criteria. Be critical and specific.

1. sections_complete [false if any section is missing OR has no real content]
   Required: (1) Check-in+Mindfulness ~10 min, (2) NCERT Content ~25 min with 3 named concept blocks,
   (3) Group Activity + Reflection ~10 min, (4) Revision + Way Forward ~5 min.

2. time_allocated [false if ANY section or concept heading is missing its explicit minute label]
   e.g. "8 मिनट", "10 minutes" — every heading must have one. Missing even one = false.

3. content_accurate [false if ANY fact is incorrect, imprecise, or not standard NCERT]
   Common failures: wrong scientific definitions, imprecise laws, invented examples, grade-wrong facts.
   If you cannot confidently verify a stated fact as correct NCERT, mark false.

4. ncert_aligned [false if the concepts don't match the NCERT textbook for that grade/subject]
   Check: is this topic actually taught in that class's NCERT book? Are the terms standard NCERT terms?
   If the query is vague (no chapter specified), check whether the content scope fits NCERT for that grade.

5. grade_appropriate [false if vocabulary or conceptual depth doesn't match the grade]
   Class 3-5: very basic. Class 6-8: intermediate. Class 9-10: abstract. Mark false if it feels
   too simple for the grade (primary-level content for Class 9) or too advanced.

6. sel_integrated [false if SEL appears only in headers or only at the end as a separate section]
   SEL must be linked to each NCERT concept block — not just mentioned in passing.

7. sel_dimension_matched [false if the SEL dimension is barely present or only in one place]
   The SEL theme must appear substantively in at least 3 different places.

8. sel_has_reflection [false if there is no direct question asking students to reflect on SEL in their life]
   A reflection must be a concrete question, not just an instruction or generic prompt.

9. culturally_relevant [false if Western/generic examples dominate over Indian ones]
   Acceptable: Indian food, festivals, local places, cricket, Bollywood.
   Not acceptable: pizza, baseball, or Western celebrities as primary examples.

For metrics 3 and 4, name the specific fact or concept you are checking before giving your verdict.

Return ONLY valid JSON:
{{
  "sections_complete":     {{"verdict": true, "reason": "what is present or missing"}},
  "time_allocated":        {{"verdict": true, "reason": "cite a heading and confirm its time label"}},
  "content_accurate":      {{"verdict": true, "reason": "name one key fact and confirm or flag it"}},
  "ncert_aligned":         {{"verdict": true, "reason": "name the NCERT chapter or flag the mismatch"}},
  "grade_appropriate":     {{"verdict": true, "reason": "cite one concept and explain grade fit"}},
  "sel_integrated":        {{"verdict": true, "reason": "cite how SEL links to NCERT content"}},
  "sel_dimension_matched": {{"verdict": true, "reason": "name the dimension and count its appearances"}},
  "sel_has_reflection":    {{"verdict": true, "reason": "quote or describe the reflection question"}},
  "culturally_relevant":   {{"verdict": true, "reason": "cite an Indian example or flag a Western one"}}
}}"""

PROMPTS = [
    ("baseline", BASELINE_PROMPT),
    ("strict",   STRICT_PROMPT),
]

# ── Checkpoint helpers ─────────────────────────────────────────────────────────────

def ckpt_path(name):
    return os.path.join(CHECKPOINT_DIR, f"judge_align_{name}.json")

def load_ckpt(name):
    p = ckpt_path(name)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}

def save_ckpt(name, data):
    with open(ckpt_path(name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ── Scoring ───────────────────────────────────────────────────────────────────────

def judge(model, prompt_template, query, output, retries=3):
    prompt = prompt_template.format(query=query, output=output)
    for attempt in range(retries):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=900,
                response_format={"type": "json_object"},
            )
            return json.loads(resp.choices[0].message.content)
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                return {m: {"verdict": None, "reason": f"error: {e}"} for m in METRICS}

def run_judge(run_name, model_id, prompt_template, rows):
    ckpt = load_ckpt(run_name)
    remaining = [r for r in rows if str(r["id"]) not in ckpt]
    if remaining:
        print(f"  scoring {len(remaining)} rows ({len(ckpt)} cached)...", end="", flush=True)
        for row in remaining:
            result = judge(model_id, prompt_template, row["original_query"], row["generated_output"])
            ckpt[str(row["id"])] = result
            time.sleep(0.3)
        save_ckpt(run_name, ckpt)
        print(f" done")
    else:
        print(f"  all {len(ckpt)} rows cached")
    return ckpt

# ── Agreement metrics ──────────────────────────────────────────────────────────────

def agreement_stats(rows, scores_by_id):
    stats = {m: {"tp": 0, "fp": 0, "tn": 0, "fn": 0} for m in METRICS}
    for row in rows:
        rid = str(row["id"])
        if rid not in scores_by_id:
            continue
        for m in METRICS:
            human = row.get(m, "").strip().upper() == "TRUE"
            ai_v  = scores_by_id[rid].get(m, {}).get("verdict")
            if ai_v is None:
                continue
            if     human and     ai_v: stats[m]["tp"] += 1
            elif   human and not ai_v: stats[m]["fn"] += 1
            elif not human and     ai_v: stats[m]["fp"] += 1
            else:                      stats[m]["tn"] += 1
    return stats

def overall_agree(stats):
    agree = sum(s["tp"] + s["tn"] for s in stats.values())
    total = sum(s["tp"] + s["fp"] + s["tn"] + s["fn"] for s in stats.values())
    return agree / total if total else 0

def macro_f1(stats):
    f1s = []
    for s in stats.values():
        prec = s["tp"] / (s["tp"] + s["fp"]) if (s["tp"] + s["fp"]) else 0
        rec  = s["tp"] / (s["tp"] + s["fn"]) if (s["tp"] + s["fn"]) else 0
        f1s.append(2 * prec * rec / (prec + rec) if (prec + rec) else 0)
    return sum(f1s) / len(f1s)

# ── Reporting ──────────────────────────────────────────────────────────────────────

def print_detail(label, rows, scores_by_id):
    stats = agreement_stats(rows, scores_by_id)
    print(f"\n{'─'*68}")
    print(f"  {label}")
    print(f"  Overall agree: {overall_agree(stats):.1%}   Macro-F1: {macro_f1(stats):.1%}")
    print(f"  {'Metric':<28}  {'Agree':>6}  {'Prec':>6}  {'Rec':>6}  {'F1':>6}  {'FP':>3}  {'FN':>3}")
    print(f"  {'·'*62}")
    for m in METRICS:
        s = stats[m]
        n = s["tp"] + s["fp"] + s["tn"] + s["fn"]
        ag   = (s["tp"] + s["tn"]) / n if n else 0
        prec = s["tp"] / (s["tp"] + s["fp"]) if (s["tp"] + s["fp"]) else 0
        rec  = s["tp"] / (s["tp"] + s["fn"]) if (s["tp"] + s["fn"]) else 0
        f1   = 2 * prec * rec / (prec + rec) if (prec + rec) else 0
        flag = "  ←" if ag < 0.70 else ""
        print(f"  {m:<28}  {ag:>6.1%}  {prec:>6.1%}  {rec:>6.1%}  {f1:>6.1%}  {s['fp']:>3}  {s['fn']:>3}{flag}")
    return stats

# ── Main ──────────────────────────────────────────────────────────────────────────

def main():
    path = os.path.join(EVAL_DIR, "teacher_messages_evaluation.csv")
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    print(f"Loaded {len(rows)} human-annotated rows\n")

    print("Human label distribution:")
    print(f"  {'Metric':<28}  TRUE  FALSE")
    for m in METRICS:
        t  = sum(1 for r in rows if r.get(m,"").strip().upper() == "TRUE")
        fa = sum(1 for r in rows if r.get(m,"").strip().upper() == "FALSE")
        print(f"  {m:<28}  {t:>4}  {fa:>4}")

    # Run all combinations
    all_results = {}  # run_name → scores_by_id
    for model_id, model_label in JUDGE_MODELS:
        for prompt_name, prompt_template in PROMPTS:
            run_name = f"{model_label}_{prompt_name}"
            print(f"\n[{run_name}]")
            scores = run_judge(run_name, model_id, prompt_template, rows)
            all_results[run_name] = scores

    # Summary comparison table
    print(f"\n\n{'='*68}")
    print("  SUMMARY — overall agreement & macro-F1 vs human labels")
    print(f"{'='*68}")
    print(f"  {'Run':<32}  {'Agree':>7}  {'Macro-F1':>9}")
    print(f"  {'─'*52}")
    summary_rows = []
    for model_id, model_label in JUDGE_MODELS:
        for prompt_name, _ in PROMPTS:
            run_name = f"{model_label}_{prompt_name}"
            stats = agreement_stats(rows, all_results[run_name])
            ag = overall_agree(stats)
            mf = macro_f1(stats)
            print(f"  {run_name:<32}  {ag:>7.1%}  {mf:>9.1%}")
            summary_rows.append((run_name, ag, mf, stats))

    # Best model detail
    best = max(summary_rows, key=lambda x: x[2])  # highest macro-F1
    print(f"\n  Best: {best[0]} (Macro-F1 {best[2]:.1%})")
    print_detail(f"BEST: {best[0]}", rows, all_results[best[0]])

    # Also print details for all models
    for model_id, model_label in JUDGE_MODELS:
        for prompt_name, _ in PROMPTS:
            run_name = f"{model_label}_{prompt_name}"
            print_detail(run_name, rows, all_results[run_name])

    # Save comparison CSV
    out_path = os.path.join(EVAL_DIR, "judge_alignment_results.csv")
    cols = ["id", "original_query"] + METRICS
    for run_name, _, _, _ in summary_rows:
        short = run_name.replace(" ", "_")
        cols += [f"{short}_{m}" for m in METRICS]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for row in rows:
            rid = str(row["id"])
            r = {"id": row["id"], "original_query": row["original_query"]}
            for m in METRICS:
                r[m] = row.get(m, "")
            for run_name, _, _, _ in summary_rows:
                short = run_name.replace(" ", "_")
                scores = all_results[run_name]
                for m in METRICS:
                    v = scores.get(rid, {}).get(m, {}).get("verdict")
                    r[f"{short}_{m}"] = "TRUE" if v else ("FALSE" if v is False else "")
            w.writerow(r)
    print(f"\nDetailed comparison → {out_path}")


if __name__ == "__main__":
    main()
