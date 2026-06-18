# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

**मोडी ते मराठी (modi-to-Marathi)** is building an open, human-in-the-loop pipeline to transliterate handwritten Modi-script Marathi manuscripts into Devanagari text. The task is **image input (Modi handwriting) → Devanagari text output**, not translation — the language (Marathi) stays the same, only the script changes.

The project has completed **Phase 1 — Fine-tuning & Evaluation**. A QLoRA-fine-tuned Qwen2.5-VL-3B model is trained and evaluated. Active work is on improving accuracy and building the inference interface.

## Repository structure

```
scripts/                     # Training, evaluation, and analysis scripts
  01_explore_dataset.py      # EDA on MoDeTrans dataset
  02_prepare_splits.py       # Create train/val/test splits
  03_zero_shot.py            # Zero-shot baseline (CER 0.930)
  05_train_qlora.py          # QLoRA fine-tuning on real MoDeTrans data
  06_evaluate.py             # CER evaluation on held-out test set
  07_train_with_synth.py     # QLoRA fine-tuning on real + SynthMoDe data
  08_error_analysis.py       # Character-level error breakdown and confusion pairs
  sample_images/             # 5 sample Modi JPGs used by the scripts
samples/                     # 30 committed sample Modi images + index.json
src/                         # Transliteration code (in progress)
assets/
  pipeline.excalidraw.svg    # Pipeline diagram placeholder (replace with real Excalidraw export)
docs/
  data.md                    # Dataset catalogue with access and licence notes
  quickstart.md              # Install and run on one image (placeholder)
  model.md                   # Model card with metrics (fill when model is published)
app.py                       # Gradio inference demo
requirements.txt             # Python dependencies
CONTRIBUTING.md              # How to contribute data, the human-in-the-loop rule
```

**Not committed (gitignored):** `models/`, `data/`, `results/`, `logs/`, `.venv/`, `memory/`

**Background docs** (prior-work assessment, scoping, dataset plan, Modi tutorial, transliteration primer) live in the companion handbook: https://github.com/lgtkgtv/modi-to-marathi-handbook (private)

## Current results

| Model | CER (204 test examples) |
|---|---|
| Zero-shot baseline | 0.930 |
| Fine-tuned — real data only (MoDeTrans, 3 epochs) | 0.332 |
| Fine-tuned — real + synthetic (MoDeTrans + SynthMoDe, 2 epochs) | 0.328 |

**65% CER reduction** from zero-shot to fine-tuned. Quality tier breakdown (synth model, 204 test images):

| Tier | CER range | Images | Meaning |
|---|---|---|---|
| Perfect | 0.0 | 3 | Accept as-is |
| Excellent | < 0.10 | 5 | Tiny touch-up |
| Good | 0.10–0.20 | 38 | Minor edits |
| **Fair** | **0.20–0.40** | **109** | **Usable first draft** ← majority |
| Poor | 0.40–0.70 | 44 | Heavy correction |
| Very poor | 0.70–1.0 | 3 | Nearly all wrong |
| Loops | > 1.0 | 2 | Hallucination; discard |

**Dominant error patterns** (from `scripts/08_error_analysis.py`):
- Deletions 46% of errors — model skips characters, especially anusvāra (ं, ~240 drops per test run)
- Vowel length confusion: ी ↔ ि, ू ↔ ु (top substitution pairs)
- अ / आ confusion

## Domain knowledge essential for this project

**The three eras we focus on** (following MoDeTrans): Shivakalin (17th c.), Peshwekalin (18th–early 19th c.), Anglakalin (1818–1952). Earlier eras excluded — well-preserved documents are scarce.

**This project prioritizes Modi-script Marathi manuscripts from the Anglakalin (1818–1952) era.**

**Key confusable Modi characters**: भ/म, क/फ, ट/ठ/ढ, न/ण, vowel-sign slips (के/कि), dropped anusvāra. Modi has **no word spaces** (continuous *shirorekha* top line) and is cursive, making segmentation hard.

**Dataset distinction that organizes all technical work:**
- **Paired transliteration data** (image → Devanagari text): rare, what we train on
- **Character recognition data** (isolated character images + class label): abundant, useful for pretraining a vision encoder only
- **Adjacent Indic transliteration text** (Roman ↔ Devanagari word pairs): no Modi, but the Marathi text can be rendered through Modi fonts to produce synthetic training pairs

## Key datasets

- `historyHulk/MoDeTrans` on Hugging Face — ~2,043 real Modi document images + expert-verified Devanagari, public
- `historyHulk/SynthMoDe` on Hugging Face — synthetic Modi images from the same Devanagari text, public
- **MODI-HChar** (~576K isolated character images, research-only, no redistribution) — best for vision encoder pretraining
- **MODI-HHDoc** (3,350 raw document pages, research-only) — raw pages to add our own expert labels to
- **Dakshina** (`mr`, CC BY-SA 4.0) — clean Marathi Devanagari text to render as synthetic Modi via fonts
- **Aksharantar** (AI4Bharat, CC-BY/CC0) — 26M Indian-language word pairs

Full dataset catalogue with access links and licences: `docs/data.md`

## Implemented pipeline

```
Modi image → VLM inference (draft Devanagari) →
expert correction → corrections saved as new training data
```

Note: image preprocessing (denoise, deskew, threshold) is planned but not yet implemented — scripts currently pass images directly to the VLM.

Model: Qwen2.5-VL-3B-Instruct base, QLoRA adapter (rank 32, 4-bit NF4), trained on RTX 5060 Laptop (8.5 GB VRAM). Two adapters exist (gitignored, download separately):
- `models/qwen25vl-3b-modi-lora/final_adapter` — trained on real data only
- `models/qwen25vl-3b-modi-synth-lora/final_adapter` — trained on real + synthetic data

**Metrics:** CER (Character Error Rate) is primary; BLEU secondary. Always measure on *real* held-out documents, not only synthetic.

## Licensing constraint

If we publish a dataset, it must be built from: our own scans + expert labels, synthetic data from CC-licensed text, and CC-licensed sources. **MODI-HChar and MODI-HHDoc are research-only and cannot be redistributed.** Track provenance per item from the start.

## Maintainer

Sachin ([@lgtkgtv](https://github.com/lgtkgtv))
