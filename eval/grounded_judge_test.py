"""
Grounded judge test — runs on ALL 51 rows.

For each row, injects NCERT curriculum context (from ncert_curriculum.py +
ncert_data.py) into the judge prompt and compares:
  Human labels  vs  Baseline (no context)  vs  Grounded (with NCERT context)

Run:
  cd /Users/shobhit/Documents/padhai/shikshabot
  python eval/grounded_judge_test.py
"""
import csv, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from openai import OpenAI
import config
from ncert_curriculum import get_ncert_context_for_query

client = OpenAI(api_key=config.OPENAI_API_KEY)

EVAL_DIR       = os.path.dirname(__file__)
CHECKPOINT_DIR = os.path.join(EVAL_DIR, "checkpoints")
CKPT_FILE      = os.path.join(CHECKPOINT_DIR, "judge_grounded_all.json")

METRICS = [
    "sections_complete", "time_allocated", "content_accurate", "ncert_aligned",
    "grade_appropriate", "sel_integrated", "sel_dimension_matched",
    "sel_has_reflection", "culturally_relevant",
]

# ── Prompt ────────────────────────────────────────────────────────────────────────

GROUNDED_PROMPT = """\
You are a quality evaluator for Padhai Bot, an educational chatbot for Indian school teachers.

The teacher sent this request: {query}

{context_block}
Evaluate the generated lesson plan on 9 binary criteria.

{context_instructions}

Criteria:
1. sections_complete — All 4 sections present: Check-in+Mindfulness ~10 min, NCERT Content ~25 min \
with 3 concepts, Group Activity ~10 min, Revision ~5 min
2. time_allocated — Time in minutes explicitly written next to each section/concept heading
3. content_accurate — All NCERT facts, characters, definitions, and literary elements are correct
4. ncert_aligned — Concepts match NCERT curriculum for the grade/subject in the request
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
  "content_accurate":      {{"verdict": true, "reason": "cite specific fact/character/definition confirmed or wrong"}},
  "ncert_aligned":         {{"verdict": true, "reason": "cite chapter match or mismatch"}},
  "grade_appropriate":     {{"verdict": true, "reason": "one sentence with grade-level evidence"}},
  "sel_integrated":        {{"verdict": true, "reason": "one sentence"}},
  "sel_dimension_matched": {{"verdict": true, "reason": "one sentence"}},
  "sel_has_reflection":    {{"verdict": true, "reason": "one sentence"}},
  "culturally_relevant":   {{"verdict": true, "reason": "one sentence"}}
}}"""

CONTEXT_INSTRUCTIONS_WITH_DATA = """\
IMPORTANT — use the NCERT reference above for content_accurate, ncert_aligned, grade_appropriate:
- If the lesson discusses characters, events, definitions, or formulas that contradict the reference, \
mark content_accurate FALSE.
- If the topic/chapter does not exist in the listed curriculum for this grade, mark ncert_aligned FALSE.
- If the lesson is about a topic marked "NOT IN NCERT", mark ncert_aligned FALSE.
- For grade_appropriate: cross-check against the grade level in the reference."""

CONTEXT_INSTRUCTIONS_NO_DATA = """\
No specific NCERT reference data is available for this query — use your general NCERT knowledge \
to evaluate content_accurate, ncert_aligned, and grade_appropriate."""

# ── Judge call ────────────────────────────────────────────────────────────────────

def judge(prompt: str, retries: int = 3) -> dict:
    for attempt in range(retries):
        try:
            resp = client.chat.completions.create(
                model="gpt-4.1-mini",
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

def build_prompt(query: str, output: str) -> tuple[str, bool]:
    """Returns (prompt_string, has_ncert_context)."""
    ctx = get_ncert_context_for_query(query)
    if ctx:
        context_block = f"--- NCERT CURRICULUM REFERENCE ---\n{ctx}\n--- END REFERENCE ---\n\n"
        instructions  = CONTEXT_INSTRUCTIONS_WITH_DATA
    else:
        context_block = ""
        instructions  = CONTEXT_INSTRUCTIONS_NO_DATA
    prompt = GROUNDED_PROMPT.format(
        query=query,
        context_block=context_block,
        context_instructions=instructions,
        output=output,
    )
    return prompt, bool(ctx)

# ── Stats helpers ─────────────────────────────────────────────────────────────────

def metric_stats(rows, scores_by_id):
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
            if human and ai_v:          stats[m]["tp"] += 1
            elif human and not ai_v:    stats[m]["fn"] += 1
            elif not human and ai_v:    stats[m]["fp"] += 1
            else:                       stats[m]["tn"] += 1
    return stats

def overall_agree(stats):
    a = sum(s["tp"] + s["tn"] for s in stats.values())
    t = sum(s["tp"] + s["fp"] + s["tn"] + s["fn"] for s in stats.values())
    return a / t if t else 0

def macro_f1(stats):
    f1s = []
    for s in stats.values():
        p = s["tp"] / (s["tp"] + s["fp"]) if (s["tp"] + s["fp"]) else 0
        r = s["tp"] / (s["tp"] + s["fn"]) if (s["tp"] + s["fn"]) else 0
        f1s.append(2 * p * r / (p + r) if (p + r) else 0)
    return sum(f1s) / len(f1s)

def print_metric_table(label, rows, scores_by_id):
    stats = metric_stats(rows, scores_by_id)
    print(f"\n  {label}")
    print(f"  Overall agree: {overall_agree(stats):.1%}   Macro-F1: {macro_f1(stats):.1%}")
    print(f"  {'Metric':<24}  {'Agree':>6}  {'Prec':>6}  {'Rec':>6}  {'F1':>6}  FP  FN")
    print(f"  {'·'*60}")
    for m in METRICS:
        s = stats[m]
        n  = s["tp"] + s["fp"] + s["tn"] + s["fn"]
        ag = (s["tp"] + s["tn"]) / n if n else 0
        pr = s["tp"] / (s["tp"] + s["fp"]) if (s["tp"] + s["fp"]) else 0
        rc = s["tp"] / (s["tp"] + s["fn"]) if (s["tp"] + s["fn"]) else 0
        f1 = 2 * pr * rc / (pr + rc) if (pr + rc) else 0
        flag = "  ←" if ag < 0.70 else ""
        print(f"  {m:<24}  {ag:>6.1%}  {pr:>6.1%}  {rc:>6.1%}  {f1:>6.1%}  {s['fp']:>2}  {s['fn']:>2}{flag}")
    return stats

# ── Main ──────────────────────────────────────────────────────────────────────────

def main():
    with open(os.path.join(EVAL_DIR, "teacher_messages_evaluation.csv"), encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    print(f"Loaded {len(rows)} rows\n")

    # Load baseline checkpoint
    baseline_path = os.path.join(CHECKPOINT_DIR, "judge_align_GPT-4.1 Mini_baseline.json")
    with open(baseline_path, encoding="utf-8") as f:
        baseline_scores = json.load(f)
    print(f"Loaded baseline scores ({len(baseline_scores)} rows cached)\n")

    # Load or score grounded
    if os.path.exists(CKPT_FILE):
        with open(CKPT_FILE, encoding="utf-8") as f:
            grounded_scores = json.load(f)
    else:
        grounded_scores = {}

    to_score = [r for r in rows if str(r["id"]) not in grounded_scores]
    if to_score:
        print(f"Scoring {len(to_score)} rows with grounded judge (model: gpt-4.1-mini)...")
        context_count = 0
        for i, row in enumerate(to_score):
            rid   = str(row["id"])
            query = row["original_query"]
            output = row["generated_output"]
            prompt, has_ctx = build_prompt(query, output)
            if has_ctx:
                context_count += 1
            label = query.replace("\n", " | ").strip()[:55]
            print(f"  [{i+1:>2}/{len(to_score)}] {'[CTX]' if has_ctx else '[   ]'} {label}", flush=True)
            result = judge(prompt)
            grounded_scores[rid] = result
            time.sleep(0.4)
        with open(CKPT_FILE, "w", encoding="utf-8") as f:
            json.dump(grounded_scores, f, ensure_ascii=False, indent=2)
        print(f"\nDone — {context_count}/{len(to_score)} rows had NCERT context injected\n")
    else:
        print(f"All {len(rows)} rows cached — skipping API calls\n")

    # ── Summary comparison ────────────────────────────────────────────────────────
    print("=" * 70)
    print("  RESULTS — Baseline vs Grounded judge (GPT-4.1 Mini, all 51 rows)")
    print("=" * 70)

    b_stats = print_metric_table("BASELINE (no NCERT context)", rows, baseline_scores)
    g_stats = print_metric_table("GROUNDED (with NCERT context)", rows, grounded_scores)

    # Delta table
    print(f"\n  {'DELTA (Grounded − Baseline)'}")
    print(f"  {'Metric':<24}  {'ΔAgree':>8}  {'ΔF1':>6}  {'ΔFP':>5}  {'ΔFN':>5}")
    print(f"  {'·'*54}")
    for m in METRICS:
        bs, gs = b_stats[m], g_stats[m]
        bn = bs["tp"] + bs["fp"] + bs["tn"] + bs["fn"]
        gn = gs["tp"] + gs["fp"] + gs["tn"] + gs["fn"]
        b_ag = (bs["tp"] + bs["tn"]) / bn if bn else 0
        g_ag = (gs["tp"] + gs["tn"]) / gn if gn else 0
        b_p  = bs["tp"] / (bs["tp"] + bs["fp"]) if (bs["tp"] + bs["fp"]) else 0
        b_r  = bs["tp"] / (bs["tp"] + bs["fn"]) if (bs["tp"] + bs["fn"]) else 0
        b_f1 = 2 * b_p * b_r / (b_p + b_r) if (b_p + b_r) else 0
        g_p  = gs["tp"] / (gs["tp"] + gs["fp"]) if (gs["tp"] + gs["fp"]) else 0
        g_r  = gs["tp"] / (gs["tp"] + gs["fn"]) if (gs["tp"] + gs["fn"]) else 0
        g_f1 = 2 * g_p * g_r / (g_p + g_r) if (g_p + g_r) else 0
        d_ag = g_ag - b_ag
        d_f1 = g_f1 - b_f1
        d_fp = gs["fp"] - bs["fp"]
        d_fn = gs["fn"] - bs["fn"]
        flag = ""
        if m in ("content_accurate", "ncert_aligned", "grade_appropriate"):
            flag = "  ←"
        print(f"  {m:<24}  {d_ag:>+8.1%}  {d_f1:>+6.1%}  {d_fp:>+5}  {d_fn:>+5}{flag}")

    b_oa = overall_agree(b_stats)
    g_oa = overall_agree(g_stats)
    b_mf = macro_f1(b_stats)
    g_mf = macro_f1(g_stats)
    print(f"\n  Overall agree: Baseline {b_oa:.1%} → Grounded {g_oa:.1%}  ({g_oa-b_oa:+.1%})")
    print(f"  Macro-F1:     Baseline {b_mf:.1%} → Grounded {g_mf:.1%}  ({g_mf-b_mf:+.1%})")

    # ── Per-row breakdown for failing metrics ─────────────────────────────────────
    print(f"\n{'─'*70}")
    print("  Per-row results for content_accurate / ncert_aligned / grade_appropriate")
    print(f"  (rows where human=FALSE — these are the ones the judge needs to fix)")
    print(f"{'─'*70}")
    print(f"  {'id':>3}  {'Human CA/NA/GA':<16}  {'Baseline':>9}  {'Grounded':>9}  Query")

    KEY = ["content_accurate", "ncert_aligned", "grade_appropriate"]
    for row in rows:
        rid = str(row["id"])
        h   = [row.get(m, "").strip().upper()[0] for m in KEY]   # T or F
        if "F" not in h:
            continue  # skip rows where all 3 are TRUE
        b = [("T" if baseline_scores.get(rid, {}).get(m, {}).get("verdict") else "F") for m in KEY]
        g = [("T" if grounded_scores.get(rid, {}).get(m, {}).get("verdict") else "F") for m in KEY]
        h_str = "/".join(h)
        b_str = "/".join(b)
        g_str = "/".join(g)
        q = row["original_query"].replace("\n", " | ").strip()[:38]
        improved = "*" if g_str != b_str else " "
        print(f"  {rid:>3}  H:{h_str}  B:{b_str}  G:{g_str} {improved}  {q}")

    print()


if __name__ == "__main__":
    main()
