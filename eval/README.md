# Eval

Evaluation experiments for Padhai Bot — intent classification and content generation.

All scripts are run from the **`shikshabot/`** directory (one level up), not from inside `eval/`.

```
cd /Users/shobhit/Documents/padhai/shikshabot
python eval/<script>.py
```

---

## Folder Map

```
eval/
├── Datasets & Annotations
│   ├── intent_classification_dataset.csv / .json / .xlsx   — 330-entry intent dataset
│   ├── teacher_messages_evaluation.csv                      — 51 human-annotated lesson plans (9 metrics)
│   ├── real_messages_content_eval.csv                       — 51 real teacher queries (not yet annotated)
│   ├── content_generation_eval.csv                          — Llama 3.3 70B outputs for 15 queries
│   ├── content_annotated.csv                                — subset with human labels
│   └── content_model_comparison.csv                         — 3-model × 2-judge output comparison
│
├── Intent Classification
│   ├── build_dataset.py        — builds the 300-entry dataset, exports XLSX with dropdowns
│   ├── eval_classifier.py      — quick single-run classifier test on test_cases.json
│   ├── run_intent_eval.py      — full 6-model eval with stratified split + checkpointing
│   └── intent_eval_results.md  — final results doc (accuracy, F1, per-language breakdown)
│
├── Content Generation
│   ├── generate_content_eval_dataset.py  — generates lesson plan outputs for evaluation
│   ├── test_new_format.py                — quick sanity check for prompt format changes
│   ├── compare_content_models.py         — 3-model × 2-judge comparison (Llama vs GPT-4.1)
│   ├── run_content_eval.py               — validates LLM judge against human labels
│   ├── align_judge.py                    — 6-combination LLM-human alignment study
│   └── grounded_judge_test.py            — NCERT context injection experiment (all 51 rows)
│
├── checkpoints/                — cached API results (JSON); delete to re-run from scratch
├── test_cases.json             — small hand-crafted test set for eval_classifier.py
└── intent_eval_val_results.csv — per-row val predictions for all models
```

---

## Experiment 1 — Intent Classification

**Goal:** pick the best model for the production intent classifier.

**Dataset:** 330 labeled examples · 6 intents · 5 languages (en, hi, hinglish, ta, te).

| Intent | Count |
|---|---|
| content_generation | 60 |
| query_resolution_academic | 60 |
| query_resolution_sel | 60 |
| feedback | 60 |
| out_of_service | 60 |
| language_change | 30 |

**Run full eval (6 models, checkpointed):**
```
python eval/run_intent_eval.py
```
Results saved to `checkpoints/` and `intent_eval_val_results.csv`. Re-running skips models that already have a checkpoint.

**Run quick smoke test:**
```
python eval/eval_classifier.py
```
Uses `test_cases.json` — a small hand-picked set. Good for checking that a prompt change hasn't broken obvious cases.

**Key results** (see `intent_eval_results.md` for full tables):

| Model | Val accuracy | Test accuracy |
|---|---|---|
| GPT-4.1 Mini ⭐ production | 97.4% | 91.9% |
| GPT-4.1 Nano | 96.1% | 96.0% |
| GPT-4o Mini | 94.4% | 96.0% |
| Llama 3.1 8B (prev. prod) | 71.4% | 75.8% |

- `feedback` is the hardest intent across all models (~85–94%)
- `out_of_service` has high test variance — harder OOS examples in test set
- Telugu is the weakest language for every model

**Build / update the dataset:**
```
python eval/build_dataset.py
```
Regenerates `intent_classification_dataset.xlsx` with dropdown validation. Edit `NEW_ENTRIES` in the script to add entries.

---

## Experiment 2 — Content Generation: LLM Judge Alignment

**Goal:** measure how well an LLM judge agrees with a human annotator on 9 binary quality metrics.

**Dataset:** `teacher_messages_evaluation.csv` — 51 real teacher queries with lesson plan outputs, human-annotated on 9 metrics (459 labeled data points).

**Metrics:**

| Category | Metric | What it checks |
|---|---|---|
| Format | sections_complete | All 4 sections present with correct timing |
| Format | time_allocated | Minute labels on every section/concept |
| Curriculum | content_accurate | NCERT facts are correct |
| Curriculum | ncert_aligned | Topics match the stated grade/subject NCERT |
| Curriculum | grade_appropriate | Depth and vocabulary suit the grade |
| SEL | sel_integrated | SEL woven into content, not standalone |
| SEL | sel_dimension_matched | One SEL dimension present consistently |
| SEL | sel_has_reflection | At least one SEL reflection question |
| SEL | culturally_relevant | Indian examples, no Western-only references |

**Run the alignment study (3 models × 2 prompts, checkpointed):**
```
python eval/align_judge.py
```
Tests GPT-4.1 Mini, GPT-4o Mini, GPT-4.1 Nano with baseline and strict prompt variants.
Results: `judge_alignment_results.csv`.

**What to look at in the output:**
- Overall agreement and Macro-F1 per model/prompt combination
- Per-metric breakdown — metrics flagged with `←` are below 70% agreement
- Best model: GPT-4.1 Mini baseline — 80.8% agreement, 87.8% Macro-F1

**Key finding:** All 3 baseline models agree on the same failing rows. Switching models doesn't help — it's a curriculum knowledge gap (judge lacks NCERT source text), not a model capability problem.

| Metric | Agreement | Automatable? |
|---|---|---|
| sel_integrated, sel_has_reflection, culturally_relevant | 100% | Yes |
| sections_complete | 96% | Yes |
| time_allocated | 86% | Yes |
| sel_dimension_matched | 84% | Yes |
| grade_appropriate | 65% | Borderline |
| content_accurate | 49% | No — human review |
| ncert_aligned | 47% | No — human review |

Note: Recall = 100% and Precision = Agreement for all metrics — this is by design. The judge defaults to TRUE when uncertain, so all errors are false positives (over-approval), never false negatives.

---

## Experiment 3 — NCERT Context Injection

**Goal:** inject chapter-level NCERT reference data into the judge prompt and measure whether alignment improves.

**Run:**
```
python eval/grounded_judge_test.py
```
Checkpoint: `checkpoints/judge_grounded_all.json`. Prints a Baseline vs Grounded delta table and a per-row breakdown for the three failing curriculum metrics.

**What it does:**
- Detects grade + subject from each teacher query
- Looks up an internal NCERT curriculum map (`ncert_curriculum.py` + `ncert_data.py`)
- Injects a structured reference block into the judge prompt for the 31/51 queries where data is available
- Compares label-by-label against the baseline (no context) and human labels

**Results:**
- Net improvement: +0.7% overall agreement (80.8% → 81.5%)
- Fixed 3 false positives: correctly flagged "Chutti Ka Din" (not in NCERT Class 7 Vasant) and "Bhasanjali" (not an NCERT textbook)
- Introduced 2 false negatives on rows where "NOT IN NCERT" notes were too aggressive
- Confirmed diagnosis: remaining FPs require full textbook text injection to fix, not just chapter lists

---

## Experiment 4 — Content Model Comparison

**Goal:** compare lesson plan quality across Llama 3.3 70B, GPT-4.1 Mini, and GPT-4.1 Nano using two LLM judges.

**Run:**
```
python eval/compare_content_models.py
```
Generates outputs (checkpointed in `cmp_gen_*.json`) and scores them with two judges (checkpointed in `cmp_scores_*.json`). Writes `content_model_comparison.csv` with blank `human_*` columns for manual annotation.

**Run the content evaluator against human labels:**
```
python eval/run_content_eval.py             # summary
python eval/run_content_eval.py --verbose   # show reasons for every disagreement
python eval/run_content_eval.py --all-reasons
```

---

## Checkpoints

All expensive API calls are checkpointed to `checkpoints/`. To re-run an experiment from scratch, delete the relevant file:

| File | Experiment |
|---|---|
| `GPT-4.1_Mini.json` etc. | Intent eval — model predictions |
| `val_test_split.json` | Intent eval — train/val/test split (delete to re-split) |
| `judge_align_*.json` | Content alignment — per-model/prompt scores |
| `judge_grounded_all.json` | NCERT injection — grounded judge scores |
| `cmp_gen_*.json` | Model comparison — generated outputs |
| `cmp_scores_*.json` | Model comparison — judge scores |

---

## Adding New Experiments

1. Put the script in `eval/`
2. Use `sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))` to import from `shikshabot/`
3. Save checkpoints to `eval/checkpoints/<experiment_name>.json`
4. Update this README
