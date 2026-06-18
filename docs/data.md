# Data

Datasets used for Modi → Marathi transliteration training and evaluation.

---

## The key distinction

| Bucket | What it gives us | Example |
|---|---|---|
| **A. Paired transliteration** | Directly trains/evaluates our exact task | MoDeTrans |
| **B. Modi recognition / raw images** | Vision encoder pretraining; raw pages to label | MODI-HChar, MODI-HHDoc |
| **C. Adjacent Indic text** | Clean Marathi Devanagari text for synthetic pair generation | Aksharantar, Dakshina |

---

## Bucket A — paired transliteration (start here)

**MoDeTrans** (`historyHulk/MoDeTrans` on Hugging Face, public)
~2,043 real handwritten Modi document images with expert-verified Devanagari transliteration. Split 80:10:10. The only public dataset with image → Devanagari ground truth at document level.

**SynthMoDe** (`historyHulk/SynthMoDe` on Hugging Face, public)
Synthetic Modi images rendered from the same Devanagari text using Modi fonts. Good for augmentation.

---

## Bucket B — Modi recognition & raw-image datasets

| Dataset | Contents | Size | Access | Licence |
|---|---|---|---|---|
| **MODI-HChar** | Isolated characters, 57 classes, 170×170 px grayscale JPG | ~575,920 images | **Free** — Mendeley `pk2zrt58pp`; also IEEE DataPort `10.21227/v2kt-rr94` | Likely CC BY 4.0 — **verify on Mendeley page before use** |
| **MODI-HHDoc** | Whole historical document page images (Peshwa-era) | 3,350 images (~6.83 GB) | **Free** — Mendeley `sg337vf6wn`; also IEEE DataPort `10.21227/1z10-w986` | Likely CC BY 4.0 — **verify on Mendeley page before use** |
| **Handwritten MODI Characters** | Isolated character samples | — | IEEE DataPort `10.21227/z3gg-8b29` | IEEE DataPort subscription required |
| **Handwritten Modi Lipi Barakhadi** | Consonant × vowel-sign combinations | — | IEEE DataPort | IEEE DataPort subscription required |

Both MODI-HChar and MODI-HHDoc are freely downloadable from Mendeley Data (no subscription, no approval needed). Our earlier "research-only, no redistribution" characterisation was not confirmed by the actual dataset pages — Mendeley Data defaults to CC BY 4.0. **Verify the exact licence shown on each Mendeley page before training or publishing.**

MODI-HHDoc raw pages can be labelled by domain experts to grow Bucket A.

---

## Bucket C — adjacent Indic corpora

| Dataset | Contents | Marathi? | Size | Access | Licence |
|---|---|---|---|---|---|
| **Aksharantar** (AI4Bharat) | Roman ↔ Indic word pairs, 21 languages | Yes | ~26M pairs | HF `ai4bharat/Aksharantar` | CC-BY / CC0 |
| **Dakshina** (Google Research) | Native-script Wikipedia text + romanization + parallel sentences, 12 languages | Yes (`mr`) | ~300K word pairs, ~120K sentence pairs | GitHub `google-research-datasets/dakshina` | CC BY-SA 4.0 |

Dakshina and Aksharantar Marathi text can be rendered through Modi fonts (MarathiCursive, Noto Sans Modi) to produce synthetic Modi → Devanagari training pairs.

---

## Licensing rules — always follow the safe path

These are hard rules, not guidelines. When in doubt, don't use the dataset.

| Source | Use for training? | Publish model? | Rule |
|---|---|---|---|
| MoDeTrans / SynthMoDe | ✅ Yes | ✅ Yes | Cite arXiv:2503.13060 |
| MODI-HChar / MODI-HHDoc | ✅ Only after confirming CC BY 4.0 on Mendeley | ✅ Yes (CC BY) | **Must verify licence on Mendeley page before any use. Do not assume.** |
| Jadhav & Inamdar (IEEE) | ⛔ No | ⛔ No | Subscription-gated; licence unclear — skip |
| Aksharantar (mined, CC0) | ✅ Yes | ✅ Yes | No restrictions — preferred for synthetic training data |
| Aksharantar (manual, CC BY) | ✅ Yes | ✅ Yes | Attribution required |
| Dakshina (CC BY-SA 4.0) | ⛔ **Never for training** | ⛔ N/A | ShareAlike copyleft — word list use at inference only |

**Dakshina rule:** Extract a Marathi word list and use it at inference time (post-processing corrector). Never add Dakshina text to training data or synthetic image generation. Use Aksharantar instead for anything that touches the training pipeline.

**MODI-HChar / MODI-HHDoc gate:** Before downloading or using either dataset, open the Mendeley page, read the licence field, and record it in `docs/data.md`. If the licence is not CC BY 4.0 or more permissive, stop and do not use.

**Publishing rule:** Any dataset we publish must consist entirely of: our own scans + expert labels, synthetic data from CC0/CC-BY sources, and other CC-licensed sources. Record provenance per image from the start. MODI-HChar and MODI-HHDoc (even if CC BY) must not be included in any redistributed dataset — they are inputs to our training pipeline only.

---

## Pipeline role of each dataset

```
Pretrain vision encoder  ◄── MODI-HChar (Modi letter shapes)
Bulk synthetic pairs     ◄── Aksharantar Marathi text → render → synthetic Modi images (Dakshina: word list only)
Core training + eval     ◄── MoDeTrans (real image → Devanagari)  ⭐
Grow real data           ◄── MODI-HHDoc raw pages + expert labels + contributed scans
Gold test set            ◄── our experts, locked, never used for training
```

---

## Useful tools

| Tool | Purpose |
|---|---|
| HuggingFace `datasets` / `transformers` | Load MoDeTrans/SynthMoDe; fine-tune models |
| Modi fonts: MarathiCursive, Noto Sans Modi | Generate synthetic Modi images from Devanagari text |
| Indic NLP Library | Devanagari normalization, tokenization |
| OpenCV | Preprocessing scans (denoise, threshold, deskew) |
| IndicXlit (AI4Bharat) | Reference transliteration model and library |

---

## Sources

- **MoDeTrans / SynthMoDe** — `historyHulk` org on Hugging Face; arXiv:2503.13060 / ICDAR 2025.
- **MODI-HChar** — Deshmukh & Kolhe (2023). IEEE DataPort `10.21227/v2kt-rr94`; Mendeley `pk2zrt58pp`.
- **MODI-HHDoc** — Deshmukh & Kolhe (2023). IEEE DataPort `10.21227/1z10-w986`; Mendeley `sg337vf6wn`.
- **Handwritten MODI Characters** — Jadhav & Inamdar (2021). IEEE DataPort `10.21227/z3gg-8b29`.
- **Aksharantar** — AI4Bharat. HF `ai4bharat/Aksharantar`. CC-BY / CC0.
- **Dakshina** — Google Research. GitHub `google-research-datasets/dakshina`. CC BY-SA 4.0.

*Verify sizes, DOIs, and licence terms on source pages before formal use.*
