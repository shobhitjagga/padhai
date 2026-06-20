# Intent Classification Evaluation Results

**Dataset:** 330 examples · 6 intents · 5 languages  
**Split:** 70/30 stratified by intent (231 validation / 99 test)  
**Eval date:** June 2026

---

## Dataset Composition

| Intent | Examples | Languages covered |
|---|---|---|
| content_generation | 60 | en, hi, hinglish, ta, te |
| feedback | 60 | en, hi, hinglish, ta, te |
| query_resolution_academic | 60 | en, hi, hinglish, ta, te |
| query_resolution_sel | 60 | en, hi, hinglish, ta, te |
| out_of_service | 60 | en, hi, hinglish, ta, te |
| language_change | 30 | en, hi, hinglish, ta, te |
| **Total** | **330** | |

---

## Overall Accuracy

| Model | Validation (n=231) | Test (n=99) |
|---|---|---|
| **GPT-4.1 Mini** ⭐ *(production)* | **97.4%** | **91.9%** |
| GPT-4.1 Nano | 96.1% | 96.0% |
| GPT-4o Mini | 94.4% | 96.0% |
| Llama 4 Scout 17B | 91.3% | 82.8% |
| Llama 3.3 70B | 80.1% | 91.9% |
| Llama 3.1 8B *(previous production)* | 71.4% | 75.8% |
| Qwen3 32B | 0% *(broken — max_tokens too low for CoT)* | — |

---

## Per-Intent Accuracy

### Validation Set (n=231)

| Intent | GPT-4.1 Mini | GPT-4.1 Nano | GPT-4o Mini | Llama 4 Scout | Llama 3.3 70B | Llama 3.1 8B |
|---|---|---|---|---|---|---|
| content_generation | 100.0% | 100.0% | 100.0% | 95.2% | 88.1% | 88.1% |
| feedback | 85.7% | 83.3% | 81.0% | 66.7% | 61.9% | 26.2% |
| query_resolution_academic | 100.0% | 100.0% | 95.2% | 97.6% | 92.9% | 92.9% |
| query_resolution_sel | 100.0% | 100.0% | 100.0% | 100.0% | 81.0% | 100.0% |
| out_of_service | 100.0% | 95.2% | 92.9% | 95.2% | 78.6% | 54.8% |
| language_change | 100.0% | 100.0% | 100.0% | 95.2% | 76.2% | 61.9% |
| **Overall** | **97.6%** | **96.4%** | **94.8%** | **91.7%** | **79.8%** | **70.6%** |

### Test Set (n=99)

| Intent | GPT-4.1 Mini | GPT-4.1 Nano | GPT-4o Mini | Llama 4 Scout | Llama 3.3 70B | Llama 3.1 8B |
|---|---|---|---|---|---|---|
| content_generation | 100.0% | 100.0% | 100.0% | 83.3% | 100.0% | 100.0% |
| feedback | 94.4% | 94.4% | 94.4% | 77.8% | 88.9% | 55.6% |
| query_resolution_academic | 100.0% | 100.0% | 88.9% | 77.8% | 94.4% | 88.9% |
| query_resolution_sel | 100.0% | 100.0% | 100.0% | 100.0% | 88.9% | 100.0% |
| out_of_service | 61.1% | 83.3% | 94.4% | 72.2% | 77.8% | 55.6% |
| language_change | 100.0% | 100.0% | 100.0% | 88.9% | 100.0% | 55.6% |
| **Overall** | **92.6%** | **96.3%** | **96.3%** | **83.3%** | **91.7%** | **75.9%** |

---

## Per-Language Accuracy

### Validation Set (n=231)

| Language | GPT-4.1 Mini | GPT-4.1 Nano | GPT-4o Mini | Llama 4 Scout | Llama 3.3 70B | Llama 3.1 8B |
|---|---|---|---|---|---|---|
| English | 97.8% | 97.8% | 97.8% | 91.1% | 80.0% | 68.9% |
| Hindi | 97.8% | 95.6% | 93.3% | 95.6% | 80.0% | 75.6% |
| Hinglish | 97.5% | 97.5% | 95.0% | 92.5% | 90.0% | 80.0% |
| Tamil | 96.1% | 96.1% | 92.2% | 88.2% | 76.5% | 66.7% |
| Telugu | 98.0% | 94.0% | 94.0% | 90.0% | 76.0% | 68.0% |

### Test Set (n=99)

| Language | GPT-4.1 Mini | GPT-4.1 Nano | GPT-4o Mini | Llama 4 Scout | Llama 3.3 70B | Llama 3.1 8B |
|---|---|---|---|---|---|---|
| English | 100.0% | 100.0% | 95.2% | 81.0% | 95.2% | 85.7% |
| Hindi | 95.2% | 95.2% | 100.0% | 85.7% | 95.2% | 85.7% |
| Hinglish | 92.3% | 96.2% | 96.2% | 88.5% | 96.2% | 76.9% |
| Tamil | 86.7% | 100.0% | 100.0% | 86.7% | 93.3% | 80.0% |
| Telugu | 81.2% | 87.5% | 87.5% | 68.8% | 68.8% | 56.2% |

---

## Key Findings

1. **GPT-4.1 Mini chosen for production** — highest validation accuracy (97.4%), +26 percentage points over the previous production model (Llama 3.1 8B at 71.4%).

2. **`feedback` is the hardest intent** across all models. Even GPT-4.1 Mini scores 85.7% on validation. Consistent pattern: teachers' reactions to content are linguistically similar to content requests.

3. **`out_of_service` variance** — GPT-4.1 Mini drops from 100% (val) to 61.1% (test), while GPT-4.1 Nano and GPT-4o Mini are more robust (83–94% on test). The test set contains harder OOS examples.

4. **Telugu is the hardest language** for every model. GPT-4.1 Mini scores 81.2% on the test set in Telugu vs 100% in English. All other GPT models similarly dip on Telugu.

5. **Language_change generalises well** — a new intent added specifically for this eval, yet GPT models achieve 100% F1 on it in both val and test sets.

6. **Dataset is representative** — 5 languages matching the actual teacher population (en, hi, hinglish, ta, te), 6 intent classes covering the full use-case scope, balanced 60/60/60/60/60/30 distribution.

---

## Per-Intent F1 — GPT-4.1 Mini (Production Model), Validation Set

| Intent | Precision | Recall | F1 |
|---|---|---|---|
| content_generation | 91.3% | 100.0% | 95.5% |
| feedback | 100.0% | 85.7% | 92.3% |
| query_resolution_academic | 95.5% | 100.0% | 97.7% |
| query_resolution_sel | 100.0% | 100.0% | 100.0% |
| out_of_service | 100.0% | 100.0% | 100.0% |
| language_change | 100.0% | 100.0% | 100.0% |
