"""Evaluates the intent classifier on labeled test cases."""
import sys, json
sys.path.insert(0, "..")

import ai
from collections import defaultdict

def run(test_cases: list) -> dict:
    intents = ["content", "query", "feedback", "sel_observation"]
    total, correct = 0, 0
    per_class = defaultdict(lambda: {"correct": 0, "total": 0})
    errors = []

    for tc in test_cases:
        result = ai.classify_intent(tc["input"])
        predicted = result.get("intent", "")
        expected  = tc["expected"]
        total += 1
        per_class[expected]["total"] += 1

        if predicted == expected:
            correct += 1
            per_class[expected]["correct"] += 1
        else:
            errors.append({
                "input":     tc["input"],
                "expected":  expected,
                "predicted": predicted,
            })

    accuracy = correct / total if total else 0

    # Per-class F1 (precision = recall = accuracy per class for single-label)
    per_class_scores = {}
    for intent in intents:
        stats = per_class[intent]
        acc   = stats["correct"] / stats["total"] if stats["total"] else 0
        per_class_scores[intent] = {"accuracy": round(acc, 2), "n": stats["total"]}

    return {
        "overall_accuracy": round(accuracy, 2),
        "correct": correct,
        "total":   total,
        "per_class": per_class_scores,
        "errors":  errors,
    }


if __name__ == "__main__":
    with open("test_cases.json") as f:
        test_cases = json.load(f)["intent_classification"]

    print(f"Running classifier eval on {len(test_cases)} test cases...\n")
    results = run(test_cases)

    print(f"Overall Accuracy: {results['overall_accuracy']} ({results['correct']}/{results['total']})\n")
    print("Per-class:")
    for intent, scores in results["per_class"].items():
        print(f"  {intent:<20} accuracy={scores['accuracy']}  n={scores['n']}")

    if results["errors"]:
        print(f"\nMisclassified ({len(results['errors'])}):")
        for e in results["errors"]:
            print(f"  [{e['expected']} → {e['predicted']}] \"{e['input']}\"")
