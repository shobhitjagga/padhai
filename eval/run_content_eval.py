"""
Validates the AI content evaluator against human-annotated labels.

Usage:
  cd shikshabot
  python eval/run_content_eval.py                # summary report
  python eval/run_content_eval.py --verbose      # show reasons for every disagreement
  python eval/run_content_eval.py --all-reasons  # show reasons for every entry
"""
import sys, csv, json, argparse
sys.path.insert(0, "..")

import ai

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

ANNOTATED_CSV = "eval/content_annotated.csv"


def load_annotated(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def run_eval(rows: list[dict]) -> tuple[dict, list[dict], list[dict]]:
    metric_stats = {m: {"agree": 0, "total": 0} for m in METRICS}
    disagreements = []
    all_results = []

    for row in rows:
        entry_id = row["id"]
        print(f"  [{entry_id:>2}] {row['topic'][:50]}")

        scores = ai.evaluate_content(
            subject=row["subject"],
            topic=row["topic"],
            grade=row["grade"],
            sel_dimension=row["sel_dimension"],
            language=row["language"],
            content=row["generated_output"],
        )

        if scores is None:
            print(f"       ERROR: eval call failed, skipping")
            continue

        entry_result = {"id": entry_id, "topic": row["topic"], "metrics": {}}

        for metric in METRICS:
            human = row.get(metric, "").strip().upper() == "TRUE"
            ai_result = scores.get(metric, {})
            ai_verdict = ai_result.get("verdict")
            reason = ai_result.get("reason", "")

            if ai_verdict is None:
                continue

            metric_stats[metric]["total"] += 1
            agree = ai_verdict == human
            if agree:
                metric_stats[metric]["agree"] += 1

            entry_result["metrics"][metric] = {
                "human": human,
                "ai": ai_verdict,
                "agree": agree,
                "reason": reason,
            }

            if not agree:
                disagreements.append({
                    "id": entry_id,
                    "topic": row["topic"],
                    "metric": metric,
                    "human": human,
                    "ai": ai_verdict,
                    "reason": reason,
                })

        all_results.append(entry_result)

    return metric_stats, disagreements, all_results


def print_report(metric_stats: dict, disagreements: list, all_results: list,
                 verbose: bool, all_reasons: bool):
    total_checks = sum(v["total"] for v in metric_stats.values())
    total_agree  = sum(v["agree"] for v in metric_stats.values())
    overall_pct  = total_agree / total_checks * 100 if total_checks else 0

    print(f"\n{'='*55}")
    print(f"Overall agreement: {overall_pct:.0f}%  ({total_agree}/{total_checks} checks)")
    print(f"{'='*55}")
    print(f"\nPer-metric agreement:")
    for metric in METRICS:
        v = metric_stats[metric]
        pct = v["agree"] / v["total"] * 100 if v["total"] else 0
        flag = "  <-- needs tuning" if pct < 80 else ""
        print(f"  {metric:<25}  {pct:>5.0f}%  ({v['agree']}/{v['total']}){flag}")

    if all_reasons:
        print(f"\n{'='*55}")
        print("All AI reasons:")
        for entry in all_results:
            print(f"\n  ID {entry['id']} — {entry['topic']}")
            for metric, m in entry["metrics"].items():
                mark = "✓" if m["agree"] else "✗"
                h = "T" if m["human"] else "F"
                a = "T" if m["ai"] else "F"
                print(f"    {mark} {metric:<25} human={h} ai={a}  {m['reason']}")

    elif disagreements:
        print(f"\nDisagreements ({len(disagreements)}):")
        for d in disagreements:
            h = "TRUE " if d["human"] else "FALSE"
            a = "TRUE " if d["ai"]    else "FALSE"
            print(f"  ID {d['id']:>2}  {d['metric']:<25}  human={h}  ai={a}", end="")
            if verbose:
                print(f"\n        {d['reason']}")
            else:
                print()

    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose",     action="store_true", help="Show reason for each disagreement")
    parser.add_argument("--all-reasons", action="store_true", help="Show AI reasons for every metric")
    parser.add_argument("--csv",         default=ANNOTATED_CSV, help="Path to annotated CSV")
    args = parser.parse_args()

    print(f"Loading {args.csv} ...")
    rows = load_annotated(args.csv)
    print(f"Running AI eval on {len(rows)} entries ...\n")

    metric_stats, disagreements, all_results = run_eval(rows)
    print_report(metric_stats, disagreements, all_results,
                 verbose=args.verbose, all_reasons=args.all_reasons)
