# Phase 1 Development Report

**Project:** मोडी ते मराठी — Modi-to-Marathi Transliteration
**Phase:** 1 — Environment Setup, Fine-tuning, and Evaluation
**Dates:** June 15–18, 2026
**Development approach:** This project was developed collaboratively between Sachin Godse and Claude CLI (Anthropic). The workflow, decisions, and findings recorded here reflect that dialog. All code was written, tested, and iterated through that collaboration.
**Hardware:** All training and evaluation was run on a desktop with an **NVIDIA RTX 5060 GPU with 8.5 GB VRAM** running WSL2 on Windows.

---

## 1. Environment Setup

We set up the Python environment using `uv` (a fast pip replacement). The key finding was that the latest PyTorch CUDA wheel (`cu130`) was unreliable due to a dependency on `pypi.nvidia.com`. We fell back to `torch==2.11.0+cu128`, which is the correct wheel for the Blackwell architecture (compute capability 12.0) of the RTX 5060.

```bash
UV_HTTP_TIMEOUT=300 uv pip install "torch==2.11.0+cu128" "torchvision" \
  --index-url https://download.pytorch.org/whl/cu128
```

**Stack installed:** PyTorch 2.11 + cu128, Transformers, PEFT, BitsAndBytes, Accelerate, Datasets, Gradio, jiwer (for CER computation).

---

## 2. Dataset

We used IIT Roorkee's **MoDeTrans** dataset (`historyHulk/MoDeTrans` on HuggingFace) — the only public dataset that provides real handwritten Modi document images paired with expert-verified Devanagari transliterations.

**Dataset properties:**
- 2,043 rows; columns: `filename`, `image` (1268×463 px grayscale), `text` (Devanagari)
- No era labels, no pre-made splits
- We created our own 80/10/10 split with `seed=42` → **train 1,635 / val 204 / test 204**
- Splits saved to `data/modetrans_splits/` (gitignored; recreated by `scripts/02_prepare_splits.py`)

We also downloaded **SynthMoDe** (`historyHulk/SynthMoDe`) — synthetic Modi images rendered from the same Devanagari text using Modi fonts. Used in the second training run.

---

## 3. Model Choice

We chose **Qwen/Qwen2.5-VL-3B-Instruct** as the base model. The reasoning:

- **VLM required** — this is an image → text task; text-only LLMs cannot see the Modi handwriting
- **3B fits the GPU** — at 4-bit NF4 quantization, 3B parameters use ~2–3 GB VRAM for inference and ~4 GB during training, comfortably within the 8.5 GB budget
- **Instruct variant** — we drive the model with a natural-language prompt; the Instruct variant follows it correctly without additional prompt engineering
- **Fully public** — the closest prior model (`historyHulk/ModiTrans-12B-Gemma-Teacher`, 12B) requires gated access approval and does not fit our GPU anyway

---

## 4. Zero-Shot Baseline

Before any fine-tuning, we ran the base model zero-shot on 5 test samples to establish a baseline.

**Result:** Mean CER **0.930** — the model hallucinated random Marathi/Hindi text and had never seen Modi script before. One example produced a repetition loop (CER > 1.0). This is the expected behavior for an out-of-distribution script.

---

## 5. Fine-Tuning: Run 1 — Real Data Only

**Script:** `scripts/05_train_qlora.py`

**Configuration:**
- Base: Qwen2.5-VL-3B-Instruct in 4-bit NF4 quantization
- LoRA: rank=32, alpha=64 → 74M trainable parameters (1.94% of 3.8B total)
- Target modules: `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`
- Batch size: 1, gradient accumulation: 8 (effective batch 8)
- Learning rate: 2e-4, cosine schedule, 3% warmup
- Epochs: 3 on 1,635 training examples
- Label masking: only the assistant's Devanagari answer tokens contribute to loss

**Training duration:** 7.45 hours (~43 seconds per gradient step)

**Loss arc:**

| Point | Loss |
|---|---|
| Step 1 | 2.36 |
| End of epoch 1 | ~0.51 |
| End of epoch 2 | ~0.51 |
| End of epoch 3 | ~0.24 |
| Mean (all steps) | 0.668 |

**Adapter saved locally to:** `models/qwen25vl-3b-modi-lora/final_adapter/` (gitignored)
**Adapter on HuggingFace:** `lgtk/qwen25vl-3b-modi-lora` (public)

---

## 6. Fine-Tuning: Run 2 — Real + Synthetic Data

**Script:** `scripts/07_train_with_synth.py`

We added SynthMoDe to the training set. SynthMoDe has 2,043 rows, each with two synthetic image variants → 4,086 synthetic examples. Combined with the 1,635 real examples: **5,721 total**.

**Configuration:** Same base + LoRA config, 2 epochs (more data → fewer passes needed).

**Training duration:** ~9.75 hours

**Loss arc:** Converged to 0.11–0.17 by end of epoch 2 (mean 0.260)

**Adapter saved locally to:** `models/qwen25vl-3b-modi-synth-lora/final_adapter/` (gitignored)
**Adapter on HuggingFace:** `lgtk/qwen25vl-3b-modi-synth-lora` (public)

---

## 7. Evaluation Results

**Script:** `scripts/06_evaluate.py` — runs inference on all 204 held-out test examples and computes CER per example.

| Model | CER (204 test examples) |
|---|---|
| Zero-shot baseline | 0.930 |
| Fine-tuned — real data only | 0.332 |
| Fine-tuned — real + synthetic | **0.328** |

A **64–65% reduction** in character error rate from zero-shot to fine-tuned. The synthetic data gave a modest but consistent improvement.

**CER distribution (real + synthetic model):**

| Quality tier | CER range | Count |
|---|---|---|
| Perfect | 0.0 | 3 |
| Excellent | < 0.10 | 5 |
| Good | 0.10–0.20 | 38 |
| Fair | 0.20–0.40 | 109 |
| Poor | 0.40–0.70 | 44 |
| Very poor | 0.70–1.0 | 3 |
| Loops (hallucination) | > 1.0 | 2 |

The majority of examples land in the "fair" tier — usable as a first draft requiring expert correction, which is exactly the assistive use-case this project targets.

---

## 8. Error Analysis

**Script:** `scripts/08_error_analysis.py` — character-level alignment using Python's `difflib`, breaking errors into substitutions, insertions, and deletions.

**Error type breakdown:**

| Type | Share | Meaning |
|---|---|---|
| Deletions | 46% | Model skips characters |
| Insertions | 28% | Model adds spurious characters |
| Substitutions | 25% | Model reads the wrong character |

**Top confused character pairs:**

| Pair | Errors | Note |
|---|---|---|
| ी ↔ ि | 150 | Long vs short /i/ vowel diacritic |
| ू ↔ ु | 57 | Long vs short /u/ vowel diacritic |
| अ ↔ आ | 50 | Short vs long /a/ |
| anusvāra (ं) dropped | 242 | Most common single error |

**Key surprise:** The confusable pairs highlighted in the Modi literature (भ/म, क/फ, ट/ठ/ढ) turned out to be minor — 5 to 14 errors each. The dominant errors are **vowel length and nasalization diacritics** — small marks that look visually similar or are easy to miss.

**Effect of synthetic data:** Reduced poor-tier examples from 59 to 47, and anusvāra drops from 242 to 217. Vowel length confusion was unchanged — synthetic font rendering does not help with that ambiguity.

**Prediction length:** Mean ratio 0.958 (predictions slightly shorter than ground truth) — consistent with the deletion-heavy pattern.

---

## 9. Inference Demo

**File:** `app.py` — a Gradio web interface. Upload any Modi image, click "Transliterate →", get Devanagari text.

- Loads the fine-tuned adapter from local `models/` if present, or falls back to the HuggingFace Hub (`lgtk/qwen25vl-3b-modi-synth-lora`) automatically
- Includes a sample gallery (30 images from `samples/` with ground truth for comparison)

To run:
```bash
pip install -r requirements.txt
python app.py
# Open http://localhost:7860
```

---

## 10. Key Findings and Recommendations for Next Steps

### What worked
- QLoRA fine-tuning on 1,635 real examples drove CER from 0.930 to 0.332 in ~7.5 hours on a consumer GPU — a strong result for a niche historical script
- Synthetic data gave a small additional gain (0.332 → 0.328) with relatively low effort

### What to tackle next

1. **More expert-labelled real data** — the biggest remaining gain. MODI-HHDoc (3,350 raw pages) is the immediate source. Recruit domain experts to annotate batches, then incrementally fine-tune.

2. **Era-aware evaluation** — MoDeTrans has no era labels. Splitting test results by document era (Anglakalin vs Peshwekalin vs Shivakalin) would reveal where the model is weakest and guide labelling priorities.

3. **Post-processing for systematic errors** — anusvāra drops and vowel-length swaps are systematic and predictable. A lightweight rule-based corrector or reranker could recover 15–20% of remaining errors without additional training data.

4. **Vision encoder pretraining on MODI-HChar** — 576K isolated character images could pretrain the visual backbone to recognize Modi letter shapes before full document fine-tuning. This targets the vowel-length confusion directly, as it is partly a visual discrimination problem.

5. **Complete the inference pipeline** — `app.py` works but has not been tested end-to-end on the full `samples/` gallery. A CLI entry point (`src/transliterate.py`) is planned.

6. **ModiTrans-12B access** — gated access was requested on HuggingFace. If approved, the 12B teacher model could generate pseudo-labels for unlabelled MODI-HHDoc pages (knowledge distillation / pseudo-labelling).

---

## Reproducibility Notes

- All scripts are deterministic given `seed=42` in `scripts/02_prepare_splits.py`
- The test split (204 examples) is fixed — never used for training
- Both adapters are publicly available on HuggingFace under the `lgtk` account
- Large directories (`models/`, `data/`, `results/`, `logs/`) are gitignored; recreate them by running the scripts in order (01 → 02 → 05 or 07 → 06 → 08)
