# Phase 2 Plan — Accuracy Improvement & Human-in-the-Loop Pipeline

**Project:** मोडी ते मराठी — Modi-to-Marathi Transliteration
**Phase 1 exit state:** QLoRA fine-tuned model, CER 0.328. 53% of test images produce a usable first draft.
**Phase 2 goal:** Push CER below 0.20 and build the human correction workflow that turns model output into verified Devanagari.

---

## Where Phase 1 left off

| What we have | What we still need |
|---|---|
| Fine-tuned model (CER 0.328) | More accurate model (target CER < 0.20) |
| 1,635 real training examples | More labelled real documents |
| Gradio demo + CLI inference | Human correction UI that feeds corrections back as training data |
| Error analysis (dominant: anusvāra drops, vowel-length swaps) | Post-processing to fix these systematically |
| MoDeTrans evaluation (no era labels) | Era-aware breakdown to target annotation effort |

---

## Work streams

### Stream A — Quick wins (no new training needed)
*Estimated effort: 2–4 weeks. Payoff: immediate CER improvement on existing model.*

**A1. Post-processing corrector**

The anusvāra drop (~240 per test run) and vowel-length swaps (ी↔ि, ू↔ु, ~207 per run)
are systematic and predictable. A lightweight corrector can recover 10–15% of remaining errors:

1. Build a Marathi word list from a corpus (e.g., Dakshina `mr` dataset — CC BY-SA 4.0, free to use)
2. For each output word, check if adding anusvāra or flipping vowel length produces a known Marathi word
3. Apply the correction if it improves word confidence

This is a rule-based post-processing step, not a new model. It runs in milliseconds.
Script: `scripts/10_postprocess.py` (to be created)

**A2. Era-aware evaluation**

MoDeTrans has no era labels. Manually tag the 204 held-out test images
(Shivakalin / Peshwekalin / Anglakalin) by inspecting document style and date.
Re-run `scripts/06_evaluate.py` with era tags to see which era the model struggles with most.

This costs no GPU time — just labelling effort — and tells us where to focus annotation in Stream B.
Script: add `--era-labels` flag to `scripts/06_evaluate.py` (to be done)

---

### Stream B — Data annotation campaign (main thrust)
*Estimated effort: months, ongoing. Payoff: highest single lever for CER improvement.*

**Why this is the ceiling:**
The model was trained on 1,635 real examples. Labelled data is the constraint,
not model architecture. Adding 500–1,000 expert-labelled pages from MODI-HHDoc
would likely push CER below 0.20 based on the MoDeTrans scaling behaviour.

**B1. Download and inventory MODI-HHDoc**
- 3,350 raw document pages (research-only, no redistribution)
- Request access if not already granted
- Sort by era; prioritise the era Stream A identifies as weakest
- Script: `scripts/11_inventory_hhdoc.py` (to be created)

**B2. Build an annotation interface**
- Export model output for a batch of MODI-HHDoc pages via `scripts/09_infer.py`
- Human expert reviews model draft and corrects it in a simple text editor or label tool
- Corrections saved as `{"image": ..., "text": ...}` pairs in `data/annotations/`
- Script: `scripts/12_export_for_annotation.py` (to be created)

**B3. Incremental fine-tuning**
After each annotation batch (target: 200–300 pages per batch):
- Merge new annotations with existing MoDeTrans training split
- Re-run `scripts/05_train_qlora.py` or `scripts/07_train_with_synth.py`
- Re-evaluate on the fixed 204 MoDeTrans test set (do not add test images to training)
- Track CER per batch to measure annotation ROI

**Annotation recruitment note:**
Target 2–3 Marathi scholars familiar with Modi script. Even 1 expert annotating
200 pages/month would double the training set in 4 months.

---

### Stream C — Pseudo-labelling via ModiTrans-12B (if access granted)
*Estimated effort: 1–2 weeks once access is granted. Payoff: potentially thousands of labelled pages without human annotation.*

**Status:** Gated access to `historyHulk/ModiTrans-12B-Gemma-Teacher` was requested
during Phase 1. This 12B model was fine-tuned by IIT Roorkee specifically on Modi data.

**If access is granted:**
1. Run ModiTrans-12B on all 3,350 MODI-HHDoc pages to generate pseudo-labels
2. Filter by confidence / CER heuristics to keep only high-quality pseudo-labels
3. Add to training set alongside real MoDeTrans data
4. This turns the annotation bottleneck from "1 human × 200 pages/month" to "GPU × 3,350 pages in days"

Script: `scripts/13_pseudolabel_hhdoc.py` (to be created when access granted)

---

### Stream D — Vision encoder pretraining on MODI-HChar (longer term)
*Estimated effort: weeks of GPU time. Payoff: targets the vowel-length confusion directly.*

**Why this helps:**
ी vs ि (long vs short /i/) and ू vs ु (long vs short /u/) differ by a single small stroke.
Post-processing (Stream A) can correct them after the fact, but pretraining on MODI-HChar
would teach the vision encoder to *see* that stroke reliably before fine-tuning begins.

**What MODI-HChar provides:**
~576K isolated character images with class labels (research-only, not redistributable).
Each image is a single Modi character — not a full document.

**Approach:**
1. Fine-tune only the vision encoder (image tower) of Qwen2.5-VL on MODI-HChar
   as a character classification task
2. Save the pretrained encoder weights
3. Initialise the full VLM with the pretrained encoder, then run standard QLoRA fine-tuning
   on MoDeTrans

This adds a pretraining step before the existing pipeline. The code changes are in
`scripts/05_train_qlora.py` to accept a custom encoder checkpoint.

Script: `scripts/14_pretrain_encoder.py` (to be created)

---

## Phase 2 success criteria

| Milestone | Target |
|---|---|
| Post-processing corrector built and measured | CER ≤ 0.295 (10% relative improvement) |
| Era-aware evaluation completed | Know which era is weakest |
| First annotation batch complete (200 pages) | CER ≤ 0.28 after incremental fine-tune |
| 1,000 pages annotated and fine-tuned | CER ≤ 0.20 |
| Human-in-the-loop UI working end-to-end | Corrections saved and used in next training run |

---

## Datasets for Phase 2

| Dataset | Purpose | Status |
|---|---|---|
| MODI-HHDoc | Annotation target (3,350 raw pages) | Not yet downloaded |
| Dakshina `mr` | Marathi word list for post-processing corrector | Not yet downloaded |
| MODI-HChar | Vision encoder pretraining | Not yet downloaded |
| ModiTrans-12B | Pseudo-labelling at scale | Awaiting gated access |

None of these were used in Phase 1.

---

## Sequence recommendation

Start with **A1** (post-processing corrector) while **A2** (era tagging) is in progress —
both are fast and inform where to focus Stream B.
Start **B1** (inventory MODI-HHDoc) in parallel.
Do not start Stream D until Stream B data shows diminishing returns —
pretraining is only worth the effort if the data bottleneck is addressed first.
