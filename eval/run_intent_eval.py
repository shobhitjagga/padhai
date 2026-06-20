"""
Intent classification evaluation across 4 models.
Stratified 70/30 split by intent, evaluated on validation set.

Checkpointing: each model's predictions are saved to eval/checkpoints/
on completion. Re-running skips already-completed models automatically.
"""
import json, os, sys, time, random, csv
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from groq import Groq
import config

groq_client = Groq(api_key=config.GROQ_API_KEY)

# OpenAI client — only initialised if key is present
openai_client = None
if config.OPENAI_API_KEY:
    from openai import OpenAI
    openai_client = OpenAI(api_key=config.OPENAI_API_KEY)

OPENAI_MODELS = {"gpt-4o-mini", "gpt-4.1-mini", "gpt-4.1-nano", "gpt-3.5-turbo", "gpt-4o"}

INTENTS = [
    "content_generation",
    "feedback",
    "query_resolution_academic",
    "query_resolution_sel",
    "out_of_service",
    "language_change",
]

SYSTEM_PROMPT = """You are an intent classifier for Padhai Bot, an educational assistant used by Indian government school teachers.

Classify the teacher's message into exactly one of these intents:

- content_generation : Teacher wants classroom content — a lesson plan, activity, or explanation for a specific NCERT subject/topic.
  Examples: "fractions ke liye lesson do", "Class 7 science activity banao", "photosynthesis pe content chahiye"
  NOTE: Only valid for NCERT school subjects (Science, Math, Social Science, Hindi, English). Reject personal/non-school requests.

- feedback : Teacher is expressing a reaction or opinion about the bot's response or their teaching experience.
  Examples: "bahut acha tha", "yeh helpful nahi tha", "I liked this", "not useful"

- query_resolution_academic : Teacher has a subject/curriculum question wanting a direct factual answer.
  Examples: "what is photosynthesis", "Newton ke niyam kya hain", "fraction aur decimal mein kya fark hai"

- query_resolution_sel : Teacher is asking about student behaviour, emotions, SEL skills, or classroom dynamics.
  Examples: "student engage nahi ho raha", "bachcha bahut shy hai", "how to handle an aggressive student"

- out_of_service : Request is outside the bot's scope — personal advice, cooking, politics, adult content, non-school topics, etc.
  Examples: "mujhe job chahiye", "aaj ka mausam kaisa hai", "cricket score batao"

- language_change : Teacher wants to change the bot's response language.
  Examples: "Hindi mein jawab do", "please respond in Tamil", "switch to Telugu", "thamizh-il sollunga"

The teacher's message may be in English, Hindi, Hinglish, Tamil, or Telugu. Classify based on meaning, not language.

Respond with ONLY the intent label — one of: content_generation, feedback, query_resolution_academic, query_resolution_sel, out_of_service, language_change"""

MODELS = [
    ("llama-3.1-8b-instant",                    "Llama 3.1 8B"),
    ("meta-llama/llama-4-scout-17b-16e-instruct","Llama 4 Scout 17B"),
    ("gpt-4.1-nano",                             "GPT-4.1 Nano"),
    ("gpt-4.1-mini",                             "GPT-4.1 Mini"),
    ("gpt-4o-mini",                              "GPT-4o Mini"),
    ("qwen/qwen3-32b",                           "Qwen3 32B"),
    ("llama-3.3-70b-versatile",                  "Llama 3.3 70B"),
]

LANGUAGES = ["en", "hi", "hinglish", "ta", "te"]

EVAL_DIR      = os.path.dirname(__file__)
CHECKPOINT_DIR = os.path.join(EVAL_DIR, "checkpoints")
SPLIT_FILE    = os.path.join(CHECKPOINT_DIR, "val_test_split.json")

# ── Data loading & splitting ────────────────────────────────────────────────────

def load_and_split(path, seed=42):
    """Load dataset and return (val, test). Saves split so it's reused on re-runs."""
    os.makedirs(CHECKPOINT_DIR, exist_ok=True)

    if os.path.exists(SPLIT_FILE):
        print("Loaded existing val/test split from checkpoint.")
        with open(SPLIT_FILE, encoding="utf-8") as f:
            saved = json.load(f)
        return saved["val"], saved["test"]

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    random.seed(seed)
    by_intent = defaultdict(list)
    for row in data:
        by_intent[row["intent"]].append(row)

    val, test = [], []
    for intent, rows in by_intent.items():
        random.shuffle(rows)
        cut = int(len(rows) * 0.7)
        val.extend(rows[:cut])
        test.extend(rows[cut:])

    random.shuffle(val)
    random.shuffle(test)

    with open(SPLIT_FILE, "w", encoding="utf-8") as f:
        json.dump({"val": val, "test": test}, f, ensure_ascii=False, indent=2)
    print(f"Saved val/test split → {SPLIT_FILE}")
    return val, test

# ── Checkpointing ───────────────────────────────────────────────────────────────

def checkpoint_path(model_label):
    safe = model_label.replace(" ", "_").replace("/", "-")
    return os.path.join(CHECKPOINT_DIR, f"{safe}.json")

def save_checkpoint(model_label, val_data, preds):
    path = checkpoint_path(model_label)
    payload = [
        {"id": row["id"], "query": row["query"],
         "true_intent": row["intent"], "pred_intent": pred,
         "language": row["language"]}
        for row, pred in zip(val_data, preds)
    ]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"  [checkpoint] saved → {path}")

def load_checkpoint(model_label):
    path = checkpoint_path(model_label)
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        rows = json.load(f)
    preds = [r["pred_intent"] for r in rows]
    print(f"  [checkpoint] loaded {len(preds)} predictions from {path}")
    return preds

# ── Classification ──────────────────────────────────────────────────────────────

def _call_api(model: str, messages: list) -> str:
    if model in OPENAI_MODELS:
        if openai_client is None:
            raise RuntimeError("OPENAI_API_KEY not set — add it to .env")
        resp = openai_client.chat.completions.create(
            model=model, messages=messages, temperature=0.0, max_tokens=20,
        )
    else:
        resp = groq_client.chat.completions.create(
            model=model, messages=messages, temperature=0.0, max_tokens=20,
        )
    return resp.choices[0].message.content.strip().lower()


def classify(query: str, model: str, retries=5) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": query},
    ]
    for attempt in range(retries):
        try:
            label = _call_api(model, messages)
            # strip <think>...</think> blocks (Qwen3 and some models use chain-of-thought)
            if "<think>" in label:
                label = label.split("</think>")[-1].strip()
            for intent in INTENTS:
                if intent in label:
                    return intent
            return label
        except Exception as e:
            err = str(e).lower()
            if "rate limit" in err or "429" in err or "too many" in err:
                wait = 60
                print(f"  [rate limit] sleeping {wait}s...")
                time.sleep(wait)
            elif "decommissioned" in err or "invalid_request" in err:
                print(f"  [FATAL] {e}")
                return "error"
            elif attempt < retries - 1:
                time.sleep(2)
            else:
                print(f"  [ERROR] {e}")
                return "error"

# ── Metrics ────────────────────────────────────────────────────────────────────

def compute_metrics(results):
    total = len(results)
    correct = sum(1 for t, p, _ in results if t == p)
    overall_acc = correct / total if total else 0

    intent_stats = {i: {"tp": 0, "fp": 0, "fn": 0, "total": 0} for i in INTENTS}
    for true, pred, _ in results:
        intent_stats[true]["total"] += 1
        if true == pred:
            intent_stats[true]["tp"] += 1
        else:
            intent_stats[true]["fn"] += 1
            if pred in intent_stats:
                intent_stats[pred]["fp"] += 1

    per_intent = {}
    for intent, s in intent_stats.items():
        prec = s["tp"] / (s["tp"] + s["fp"]) if (s["tp"] + s["fp"]) else 0
        rec  = s["tp"] / (s["tp"] + s["fn"]) if (s["tp"] + s["fn"]) else 0
        f1   = 2 * prec * rec / (prec + rec) if (prec + rec) else 0
        per_intent[intent] = {"precision": prec, "recall": rec, "f1": f1,
                               "acc": s["tp"] / s["total"] if s["total"] else 0}

    lang_stats = {l: {"correct": 0, "total": 0} for l in LANGUAGES}
    for true, pred, lang in results:
        if lang in lang_stats:
            lang_stats[lang]["total"] += 1
            if true == pred:
                lang_stats[lang]["correct"] += 1
    per_lang = {l: s["correct"] / s["total"] if s["total"] else 0
                for l, s in lang_stats.items()}

    return overall_acc, per_intent, per_lang

# ── Output ──────────────────────────────────────────────────────────────────────

def print_results(model_label, overall_acc, per_intent, per_lang, n_val):
    print(f"\n{'─'*60}")
    print(f"  {model_label}   (n={n_val})")
    print(f"{'─'*60}")
    print(f"  Overall accuracy: {overall_acc:.1%}")
    print()
    print(f"  {'Intent':<30} {'Acc':>6}  {'Prec':>6}  {'Rec':>6}  {'F1':>6}")
    print(f"  {'─'*56}")
    for intent in INTENTS:
        m = per_intent[intent]
        print(f"  {intent:<30} {m['acc']:>6.1%}  {m['precision']:>6.1%}  {m['recall']:>6.1%}  {m['f1']:>6.1%}")
    print()
    print(f"  {'Language':<12} {'Acc':>6}")
    print(f"  {'─'*20}")
    for lang in LANGUAGES:
        print(f"  {lang:<12} {per_lang[lang]:>6.1%}")

def save_combined_csv(model_preds_map, val_data):
    """Save one CSV with all model predictions side by side."""
    out_path = os.path.join(EVAL_DIR, "intent_eval_val_results.csv")
    fieldnames = ["id", "query", "true_intent", "language"] + [m[1] for m in MODELS]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in val_data:
            r = {"id": row["id"], "query": row["query"],
                 "true_intent": row["intent"], "language": row["language"]}
            for _, label in MODELS:
                r[label] = model_preds_map.get(label, {}).get(row["id"], "")
            writer.writerow(r)
    print(f"\nCombined predictions saved → {out_path}")

def save_summary_json(summary_rows):
    out_path = os.path.join(CHECKPOINT_DIR, "summary.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary_rows, f, ensure_ascii=False, indent=2)
    print(f"Summary saved → {out_path}")

# ── Main ────────────────────────────────────────────────────────────────────────

def main():
    dataset_path = os.path.join(EVAL_DIR, "intent_classification_dataset.json")
    val, test = load_and_split(dataset_path)
    print(f"Split: {len(val)} validation / {len(test)} test\n")

    model_preds_map = {}  # label → {id: pred}
    summary_rows = []

    for model_id, model_label in MODELS:
        # Skip OpenAI models if no key configured
        if model_id in OPENAI_MODELS and not config.OPENAI_API_KEY:
            print(f"[{model_label}] skipping — OPENAI_API_KEY not set in .env")
            continue

        # Check for existing checkpoint
        preds = load_checkpoint(model_label)
        if preds is not None:
            print(f"[{model_label}] skipping — checkpoint found")
        else:
            print(f"[{model_label}] classifying {len(val)} queries...")
            preds = []
            for i, row in enumerate(val):
                pred = classify(row["query"], model_id)
                preds.append(pred)
                if (i + 1) % 20 == 0:
                    correct_so_far = sum(1 for t, p in zip([r["intent"] for r in val[:i+1]], preds) if t == p)
                    print(f"  {i+1}/{len(val)}  running acc: {correct_so_far/(i+1):.1%}")
                time.sleep(0.3 if model_id in OPENAI_MODELS else 2.1)

            save_checkpoint(model_label, val, preds)

        results = [(row["intent"], pred, row["language"])
                   for row, pred in zip(val, preds)]
        overall_acc, per_intent, per_lang = compute_metrics(results)
        print_results(model_label, overall_acc, per_intent, per_lang, len(val))

        model_preds_map[model_label] = {row["id"]: pred for row, pred in zip(val, preds)}
        summary_rows.append({
            "model": model_label,
            "overall_acc": overall_acc,
            "per_intent": per_intent,
            "per_lang": per_lang,
        })

    # Summary comparison table
    print(f"\n{'='*60}")
    print("  MODEL COMPARISON SUMMARY")
    print(f"{'='*60}")
    print(f"  {'Model':<24} {'Overall':>8}  {'en':>6}  {'hi':>6}  {'hinglish':>8}  {'ta':>6}  {'te':>6}")
    print(f"  {'─'*72}")
    for s in summary_rows:
        pl = s["per_lang"]
        print(f"  {s['model']:<24} {s['overall_acc']:>8.1%}  "
              f"{pl['en']:>6.1%}  {pl['hi']:>6.1%}  {pl['hinglish']:>8.1%}  "
              f"{pl['ta']:>6.1%}  {pl['te']:>6.1%}")

    save_combined_csv(model_preds_map, val)
    save_summary_json(summary_rows)

if __name__ == "__main__":
    main()
