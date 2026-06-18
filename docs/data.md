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

## Licensing summary

| Source | Train on it? | Publish model trained on it? | Note |
|---|---|---|---|
| MoDeTrans / SynthMoDe | Yes | Yes | Cite arXiv:2503.13060 |
| MODI-HChar / MODI-HHDoc | Yes | Yes (if CC BY 4.0 confirmed) | **Verify licence on Mendeley page first**; credit Deshmukh & Kolhe |
| Jadhav & Inamdar (IEEE) | Only with subscription | Check licence | Subscription-gated |
| Aksharantar (mined) | Yes | Yes | CC0 — no restrictions |
| Aksharantar (manual) | Yes | Yes | CC BY — attribution only |
| Dakshina | **Word list only** (see below) | N/A | CC BY-SA 4.0 ShareAlike — avoid for model training |

**Dakshina CC BY-SA 4.0 — use only for post-processing word list (Stream A1), not for training.**
The ShareAlike clause means any derivative work must carry the same licence.
Whether trained model weights count as a derivative work is legally unsettled.
Safe path: extract a Marathi word list from Dakshina and use it at inference time;
use Aksharantar (CC0/CC-BY) for any synthetic training image generation instead.

If we publish our own dataset it must be built from: our own scans + expert labels,
synthetic data from CC-licensed text, and CC-licensed sources.
Record provenance per item from the start.

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
