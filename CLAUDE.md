# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

**मोडी ते मराठी (modi-to-Marathi)** is building an open, human-in-the-loop pipeline to transliterate handwritten Modi-script Marathi manuscripts into Devanagari text. The task is **image input (Modi handwriting) → Devanagari text output**, not translation — the language (Marathi) stays the same, only the script changes.

The project is currently in **Phase 0 — Scoping & Dataset Preparation**. There is no runnable code yet. All files in this repo are planning and stakeholder documents in `docs/`.

## Repository structure

```
docs/                        # All project documents (drafts for stakeholder input)
  00_Transliteration-Primer.md   # Non-technical intro: what transliteration is, AI concepts glossary
  01_Prior-Work-Assessment.md    # What the IIT Roorkee MoDeTrans project built and how good it is
  02_Scoping-Questionnaire.md    # Open questions for contributors and faculty advisors
  03_Dataset-Preparation-Plan.md # Phase 0 strategy: dataset-first approach
  04_Modi-Script-Tutorial.md     # History, eras, and writing-system structure of Modi script
  05_Datasets-for-Transliteration.md  # Catalogue of every relevant dataset with access/licence notes
docs_pdfs/                   # PDF exports of the docs/ files (kept in sync)
```

## Domain knowledge essential for this project

**The three eras we focus on** (following MoDeTrans): Shivakalin (17th c.), Peshwekalin (18th–early 19th c.), Anglakalin (1818–1952). Earlier eras (Adyakalin, Yadavakalin) are excluded because well-preserved documents are scarce.

**This project prioritizes Modi-script Marathi manuscripts from the Anglakalin (1818–1952) era.**

**Key confusable Modi characters** that both humans and models struggle with: भ/म, क/फ, ट/ठ/ढ, न/ण, vowel-sign slips (के/कि), dropped anusvāra. Modi also has **no word spaces** (continuous *shirorekha* top line) and is cursive, making segmentation hard.

**Dataset distinction that organizes all technical work:**
- **Paired transliteration data** (image → Devanagari text): rare, what we need to train on
- **Character recognition data** (isolated character images + class label): abundant, useful for pretraining a vision encoder only
- **Adjacent Indic transliteration text** (Roman ↔ Devanagari word pairs): no Modi, but the Marathi text can be rendered through Modi fonts to produce synthetic training pairs

## Reference project and key datasets

The closest prior work is IIT Roorkee's **MoDeTrans** (arXiv:2503.13060, ICDAR 2025):
- `historyHulk/MoDeTrans` on Hugging Face — ~2,043 real Modi document images + expert-verified Devanagari, public
- `historyHulk/SynthMoDe` on Hugging Face — synthetic Modi images from the same Devanagari text, public
- `historyHulk/ModiTrans-12B-Gemma-Teacher` — the published model (12B, gated); the smaller 429M student model emphasized in the paper is **not yet publicly released**

Other datasets catalogued in `docs/05_Datasets-for-Transliteration.md`:
- **MODI-HChar** (~576K isolated character images, research-only, no redistribution) — best for vision encoder pretraining
- **MODI-HHDoc** (3,350 raw document pages, research-only) — raw pages to add our own expert labels to
- **Dakshina** (`mr`, CC BY-SA 4.0) — clean Marathi Devanagari text to render as synthetic Modi via fonts
- **Aksharantar** (AI4Bharat, CC-BY/CC0) — 26M Indian-language word pairs

**Modi fonts for synthetic data:** MarathiCursive, Noto Sans Modi (both open).

## Phase 0 priorities (what work in this repo is about)

1. **Build the gold test set first** — a few hundred expert-verified, cross-checked examples, locked for measurement only, never used for training. Without this, no accuracy number is trustworthy.
2. Agree on the unit of labeling (reference project used 3–4 lines per segment).
3. Draft transliteration guidelines covering the known confusable characters, vowel signs, anusvāra, and how to mark uncertain readings.
4. Evaluate which existing datasets (section 5 doc) can be legally reused given our intended publishing goals.

## Planned pipeline (for when code work begins)

```
Modi image → preprocessing (grayscale → denoise → threshold → deskew) →
VLM inference (draft Devanagari) → post-processing →
expert correction → corrections saved as new training data
```

**Metrics to use:** CER (Character Error Rate) is primary for transliteration; BLEU as secondary. Always measure on *real* held-out documents, not only synthetic.

## Licensing constraint

If we publish a dataset, it must be built from: our own scans + expert labels, synthetic data from CC-licensed text, and CC-licensed sources. **MODI-HChar and MODI-HHDoc are research-only and cannot be redistributed or included in a published dataset.** Track provenance per item from the start.

## Document conventions

- All `docs/` files are **stakeholder drafts** — they are circulated for expert correction, not final authoritative statements.
- Maintainer: Sachin ([@lgtkgtv](https://github.com/lgtkgtv))
- Dates in document headers are placeholders (`[Date]`) pending stakeholder sign-off.
