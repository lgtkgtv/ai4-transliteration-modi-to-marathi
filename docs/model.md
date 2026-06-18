# Model Card

**Task:** Handwritten Modi script image → Devanagari (Marathi) text
**Phase 1 status:** Trained and evaluated. Two public adapters on HuggingFace.

---

## Model details

| Field | Value |
|---|---|
| **Base model** | Qwen/Qwen2.5-VL-3B-Instruct |
| **Fine-tuning method** | QLoRA — LoRA rank 32, alpha 64, 4-bit NF4 quantization |
| **Trainable parameters** | 74M (1.94% of 3.8B total) |
| **Task** | Image → Devanagari text (transliteration, not translation) |
| **Input** | JPEG/PNG scan or photograph of handwritten Modi text |
| **Output** | Devanagari text string |
| **Primary metric** | CER (Character Error Rate) — lower is better; 0.0 = perfect |
| **Hardware** | RTX 5060 GPU, 8.5 GB VRAM, WSL2 |

---

## Evaluation results

Evaluated on **204 held-out real document images** from MoDeTrans (never seen during training).

| Model | CER | Adapter on HuggingFace |
|---|---|---|
| Zero-shot baseline (no fine-tuning) | 0.930 | — |
| Fine-tuned — real data only | 0.332 | `lgtk/qwen25vl-3b-modi-lora` |
| Fine-tuned — real + synthetic | **0.328** | `lgtk/qwen25vl-3b-modi-synth-lora` ← recommended |

**65% reduction** in CER from zero-shot to fine-tuned.

---

## What CER 0.328 means in practice

CER is the fraction of characters that are wrong. 0.328 means roughly 1 in 3
characters needs expert correction — useful as a first draft in a
human-in-the-loop workflow, not as a finished output.

The 204 test images break down by quality tier:

| Quality tier | CER range | Images | Practical meaning |
|---|---|---|---|
| Perfect | 0.0 | 3 | Accept as-is — nothing to fix |
| Excellent | < 0.10 | 5 | Tiny touch-up — 1 char in 10 wrong |
| Good | 0.10–0.20 | 38 | Minor editing — 1–2 chars in 10 wrong |
| **Fair** | **0.20–0.40** | **109** | **Usable first draft — moderate expert editing** |
| Poor | 0.40–0.70 | 44 | Heavy correction needed |
| Very poor | 0.70–1.0 | 3 | Nearly all wrong — marginal as scaffold |
| Hallucination loops | > 1.0 | 2 | Model repeated itself; discard and retype |

**53% of images (109/204) land in the "fair" tier** — the model saves expert time
even when it is not accurate. The 46 poor/worse images still require near-complete rework.

---

## Error patterns

From `scripts/08_error_analysis.py` on the 204 test examples:

| Error type | Share | Detail |
|---|---|---|
| **Deletions** | 46% | Model skips characters |
| Insertions | 28% | Model adds spurious characters |
| Substitutions | 25% | Model reads the wrong character |

**Most frequent specific errors:**

| Error | Count | Note |
|---|---|---|
| Anusvāra (ं) dropped | ~240 | Most common single error |
| ी → ि (long /i/ → short) | 150 | Vowel length confusion |
| ू → ु (long /u/ → short) | 57 | Vowel length confusion |
| अ → आ / आ → अ | 50 | Short/long /a/ confusion |

**Key finding:** The visually obvious confusables from the Modi literature
(भ/म, क/फ, ट/ठ/ढ) turned out to be minor (5–14 errors each). The dominant
errors are *small diacritics* — anusvāra and vowel-length marks — which look
similar and are easy to miss even for human readers.

**Effect of synthetic data:** Reduced poor-tier images from 59 → 47 and
anusvāra drops from 242 → 217. Vowel-length confusion was unchanged —
font-rendered synthetic data does not capture that visual ambiguity.

---

## Training data

| Dataset | Type | Examples |
|---|---|---|
| `historyHulk/MoDeTrans` | Real handwritten documents | 1,635 (training split) |
| `historyHulk/SynthMoDe` | Synthetic — Modi font renders | 4,086 |
| **Total (synth adapter)** | | **5,721** |

Test set: 204 examples from MoDeTrans (real images only, never used for training).
See [`docs/data.md`](data.md) for full dataset catalogue with licences.

---

## Known limitations

- Best on **Peshwekalin / Shivakalin formal administrative letters** — the
  majority of training data. Performance on informal correspondence or
  personal records may be lower.
- **No image preprocessing** — the model receives raw images. Denoising,
  deskewing, and binarisation are planned but not yet implemented.
- **Modi abbreviations and scribal shorthand** (e.g., `वाा`, `खुा`) are
  poorly handled.
- **Mixed Modi/English text** (common in Anglakalin-era documents) is not
  handled.

---

## Licence

Base model: Apache 2.0 (Qwen/Qwen2.5-VL-3B-Instruct).
Adapters: Apache 2.0.
Training data: MoDeTrans and SynthMoDe are public on HuggingFace; see
[`docs/data.md`](data.md) for per-dataset licence details.

---

## How to use

See [`docs/quickstart.md`](quickstart.md) for a quick start.
See [`docs/inference-guide.md`](inference-guide.md) for CLI vs Gradio trade-offs.
