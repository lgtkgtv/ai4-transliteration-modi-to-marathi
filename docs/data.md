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
| **MODI-HChar** | Isolated characters, 57 classes, 170×170 px grayscale JPG | ~575,920 images | IEEE DataPort `10.21227/v2kt-rr94`; Mendeley `pk2zrt58pp` | Research-only, **no redistribution** |
| **MODI-HHDoc** | Whole historical document page images (Peshwa-era) | 3,350 images (~6.83 GB) | IEEE DataPort `10.21227/1z10-w986`; Mendeley `sg337vf6wn` | Research-only, **no redistribution** |
| **Handwritten MODI Characters** | Isolated character samples | — | IEEE DataPort `10.21227/z3gg-8b29` | IEEE DataPort subscription |
| **Handwritten Modi Lipi Barakhadi** | Consonant × vowel-sign combinations | — | IEEE DataPort | IEEE DataPort |

Mendeley mirrors of MODI-HChar and MODI-HHDoc are usually downloadable without a subscription. MODI-HHDoc raw pages can be labelled by our experts to grow Bucket A.

---

## Bucket C — adjacent Indic corpora

| Dataset | Contents | Marathi? | Size | Access | Licence |
|---|---|---|---|---|---|
| **Aksharantar** (AI4Bharat) | Roman ↔ Indic word pairs, 21 languages | Yes | ~26M pairs | HF `ai4bharat/Aksharantar` | CC-BY / CC0 |
| **Dakshina** (Google Research) | Native-script Wikipedia text + romanization + parallel sentences, 12 languages | Yes (`mr`) | ~300K word pairs, ~120K sentence pairs | GitHub `google-research-datasets/dakshina` | CC BY-SA 4.0 |

Dakshina and Aksharantar Marathi text can be rendered through Modi fonts (MarathiCursive, Noto Sans Modi) to produce synthetic Modi → Devanagari training pairs.

---

## Licensing summary

| Source | Train on it? | Redistribute it? | Note |
|---|---|---|---|
| MoDeTrans / SynthMoDe | Yes | Check HF card | Cite arXiv:2503.13060 |
| MODI-HChar / MODI-HHDoc | Yes (research) | **No** | Credit Deshmukh & Kolhe |
| Jadhav & Inamdar (IEEE) | Yes (subscription) | **No** | Licence-bound |
| Aksharantar | Yes | Yes (CC-BY/CC0) | Attribute |
| Dakshina | Yes | Yes (CC BY-SA 4.0) | Share-alike — derivatives must use same licence |

If we publish our own dataset it must be built from our own scans + expert labels, synthetic data from CC-licensed text, and CC-licensed sources — **not** from the no-redistribution Modi sets. Record provenance per item from the start.

---

## Pipeline role of each dataset

```
Pretrain vision encoder  ◄── MODI-HChar (Modi letter shapes)
Bulk synthetic pairs     ◄── Dakshina/Aksharantar Marathi text → render → synthetic Modi images
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
