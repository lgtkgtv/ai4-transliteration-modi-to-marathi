# Datasets for Modi → Marathi Transliteration: A Deep Dive

**Project:** मोडी ते मराठी (modi-to-Marathi)
**Repository:** https://github.com/lgtkgtv/ai4-transliteration-modi-to-marathi
**Author:** Sachin · **Audience:** the data/engineering team
**Purpose:** Catalogue every dataset relevant to training or fine-tuning a Modi→Marathi transliteration model, with honest notes on what each one actually contains, how to get it, and its licence.

---

## 0. The one distinction that organizes everything

Before the list, internalize this — it prevents wasted effort:

> **Recognition data ≠ transliteration data.**
> Most Modi datasets are **character recognition** sets (isolated letters with a class label). Our task needs **paired transliteration** data (an image of Modi text → the correct Marathi/Devanagari text). Recognition sets are still useful — but mainly for *pretraining* and *synthetic data*, not for directly learning end-to-end transliteration.

So we sort everything into three buckets:

| Bucket | What it gives us | Example |
|---|---|---|
| **A. Paired transliteration** | Directly trains/evaluates our exact task | MoDeTrans |
| **B. Modi recognition / raw images** | Pretraining a vision encoder; raw pages to label; synthetic word building | MODI-HChar, MODI-HHDoc |
| **C. Adjacent Indic transliteration text** | The *craft* of transliteration modeling; clean Marathi target text | Aksharantar, Dakshina |

---

## 1. Bucket A — the dataset that matches our exact task

### MoDeTrans  ⭐ (start here)
- **What:** ~**2,043** real handwritten Modi **document images**, each paired with an **expert-verified Devanagari transliteration**. Spans Shivakalin, Peshwekalin, Anglakalin. Split 80:10:10.
- **Why it's special:** the **only** public dataset that gives us *image → Devanagari text* ground truth at the document level — exactly our task.
- **Access:** Hugging Face, `historyHulk/MoDeTrans` (public). Load with the `datasets` library.
- **Companion:** `historyHulk/SynthMoDe` — synthetic Modi images rendered from the same Devanagari text (using Modi fonts). Public. Great for augmentation and for a "train-on-real / test-on-synthetic" generalization check.
- **Caveat:** ~2k examples is small for deep learning. Expect to augment it heavily (Bucket B + C strategies below).

---

## 2. Bucket B — Modi recognition & raw-image datasets

These come mostly from the prolific **Deshmukh & Kolhe** group (Dr. B.A.M. University, Aurangabad) and **Jadhav & Inamdar**. They are excellent, but note the **research-only, no-redistribution** licences — we can train on them, but we generally **cannot republish** them or a thin derivative.

| Dataset | Contents | Size | Access / ID | Licence |
|---|---|---|---|---|
| **MODI-HChar** | Isolated characters: 57 classes (10 numerals, 12 vowels, 35 consonants), 170×170 px grayscale JPG | **~575,920** images | IEEE DataPort DOI **10.21227/v2kt-rr94**; Mendeley `pk2zrt58pp` | Research-only, no redistribution |
| **MODI-HHDoc** | Whole historical Modi **document** page images (Peshwa-era), 24 folders | **3,350** images (~6.83 GB) | IEEE DataPort DOI **10.21227/1z10-w986**; Mendeley `sg337vf6wn` | Research-only, no redistribution |
| **Handwritten MODI Characters** | Isolated character samples | — | IEEE DataPort DOI **10.21227/z3gg-8b29** (Jadhav & Inamdar) | IEEE DataPort subscription |
| **Handwritten Modi Lipi Barakhadi** | *Barakhadi* — consonant×vowel-sign combinations | — | IEEE DataPort | IEEE DataPort |

**Practical notes on access:**
- **Mendeley Data** mirrors of MODI-HChar and MODI-HHDoc are usually **downloadable without a subscription** (still under the research-only licence) — often the easiest route. IEEE DataPort frequently requires an IEEE/DataPort subscription.
- **MODI-HHDoc gives us raw pages but *not* transliterations.** It's a superb source of *real document images* onto which our experts can add Devanagari labels — effectively a way to grow Bucket A.
- **Character sets (MODI-HChar etc.) are recognition data.** Their best use for us is (a) **pretraining the vision encoder** so it already "knows" Modi letter shapes, and (b) **assembling synthetic words/lines** by stitching characters.

---

## 3. Bucket C — adjacent Indic transliteration corpora (not Modi, still valuable)

These are **Roman ↔ native-script** text datasets. They contain **no Modi**, so they can't teach Modi letter shapes. But they're valuable in two concrete ways: they teach the **modeling craft** of transliteration, and they are a large, clean source of **Marathi Devanagari text** — which we can feed into Modi fonts to mass-produce **synthetic Modi→Devanagari pairs**.

| Dataset | Contents | Marathi? | Size | Access | Licence |
|---|---|---|---|---|---|
| **Aksharantar** (AI4Bharat) | Roman↔Indic **word** pairs, 21 languages | Yes | **~26M** pairs | HF `ai4bharat/Aksharantar` | CC-BY (manual) / CC0 (mined) |
| **Dakshina** (Google Research) | Native-script Wikipedia text + romanization lexicon + **parallel sentences**, 12 South Asian languages | Yes (`mr`) | ~**300K** word pairs, ~**120K** sentence pairs | GitHub `google-research-datasets/dakshina` | CC BY-SA 4.0 |

**Why we care, concretely:**
- **Dakshina's Marathi native-script Wikipedia text and sentence pairs** = a ready supply of correct modern Marathi (Devanagari) sentences. Render those through **MarathiCursive / Noto Sans Modi** → instant synthetic Modi→Devanagari training pairs.
- **Aksharantar** is the proof that *data scale + a small model* wins at transliteration; its Marathi portion and methodology are a useful reference even though the direction (Roman↔Devanagari) differs from ours (Modi→Devanagari).

---

## 4. Tools & libraries worth adopting

| Tool | Use to us |
|---|---|
| **Hugging Face `datasets` / `transformers`** | Load MoDeTrans/SynthMoDe; run/fine-tune models |
| **Modi fonts: MarathiCursive, Noto Sans Modi** | Generate synthetic Modi images from Devanagari text |
| **Indic NLP Library** | Devanagari normalization, script conversion, tokenization for the target side |
| **indic-transliteration (Sanscript)** | Convert Devanagari ↔ romanization schemes (useful for evaluation/normalization) |
| **IndicXlit** (AI4Bharat) | Reference model + library for Indic transliteration; baseline ideas |
| **OpenCV** | Preprocessing real document scans (denoise, threshold, deskew) |

---

## 5. Licensing & ethics summary (read before training)

| Source | Can we train on it? | Can we redistribute it? | Note |
|---|---|---|---|
| MoDeTrans / SynthMoDe | Yes | Check the HF card terms | Public; cite the paper |
| MODI-HChar / MODI-HHDoc | Yes (research) | **No** | Research-only; credit Deshmukh & Kolhe |
| Jadhav & Inamdar (IEEE DataPort) | Yes (per subscription) | **No** | Subscription/licence bound |
| Aksharantar | Yes | Yes (per CC-BY/CC0) | Attribute appropriately |
| Dakshina | Yes | Yes (CC BY-SA 4.0) | **Share-Alike** — derivatives must use the same licence |

Two stakeholder takeaways:
1. If we ever **publish our own dataset**, we must build it from sources whose licences permit redistribution (our own scans + expert labels, synthetic data, and CC-licensed text) — **not** from the no-redistribution Modi sets.
2. Always record **provenance** per item so licence and credit obligations are traceable.

---

## 6. How each dataset maps to our pipeline (the synthesis)

```
                          ┌─────────────────────────────────────────────┐
   Pretrain vision    ◄───┤ MODI-HChar  (Modi letter shapes)            │
   encoder on Modi        └─────────────────────────────────────────────┘
                          ┌─────────────────────────────────────────────┐
   Bulk synthetic     ◄───┤ Dakshina/Aksharantar Marathi text           │
   training pairs         │      ↓  render with MarathiCursive/Noto      │
                          │   SynthMoDe-style synthetic Modi images      │
                          └─────────────────────────────────────────────┘
                          ┌─────────────────────────────────────────────┐
   Core supervised    ◄───┤ MoDeTrans  (real image → Devanagari)  ⭐     │
   training + eval        └─────────────────────────────────────────────┘
                          ┌─────────────────────────────────────────────┐
   Grow real data     ◄───┤ MODI-HHDoc raw pages + OUR expert labels     │
                          │  + OUR stakeholders' contributed scans       │
                          └─────────────────────────────────────────────┘
                                          ↓
                        Gold TEST set (our experts, locked)  ← measure CER/BLEU
```

The strategy in one line: **pretrain on character shapes, bulk up with synthetic pairs from licence-clean Marathi text, train and measure on MoDeTrans, and grow real data from MODI-HHDoc pages plus our own contributed scans — all verified by our experts.**

---

## 7. Recommended starting bundle (week 1–2)

1. **Pull `historyHulk/MoDeTrans` + `historyHulk/SynthMoDe`** from Hugging Face — this is our backbone and baseline.
2. **Download MODI-HChar and MODI-HHDoc from the Mendeley mirrors** (research-only) — for vision-encoder pretraining and as raw pages to label.
3. **Grab Dakshina (`mr`)** from GitHub — a licence-clean source of Marathi Devanagari text for synthetic generation.
4. **Install** the Modi fonts + Indic NLP Library + OpenCV.
5. **Build the gold test set first** (see `docs/03_Dataset-Preparation-Plan.md`) before training anything.

---

## 8. Sources & access links

- **MoDeTrans / SynthMoDe** — Hugging Face, org `historyHulk`. Described in arXiv:2503.13060 / ICDAR 2025 (DOI 10.1007/978-3-032-04630-7_3).
- **MODI-HChar** — Deshmukh, M. & Kolhe, S. (2023). IEEE DataPort DOI **10.21227/v2kt-rr94**; Mendeley Data `pk2zrt58pp` (https://data.mendeley.com/datasets/pk2zrt58pp/1).
- **MODI-HHDoc** — Deshmukh, M. & Kolhe, S. (2023). IEEE DataPort DOI **10.21227/1z10-w986**; Mendeley Data `sg337vf6wn` (https://data.mendeley.com/datasets/sg337vf6wn/1).
- **Handwritten MODI Characters** — Jadhav, S. & Inamdar, V. (2021). IEEE DataPort DOI **10.21227/z3gg-8b29**.
- **Handwritten Modi Lipi Barakhadi** — IEEE DataPort (https://ieee-dataport.org/documents/handwritten-modi-lipi-barakhadi-dataset).
- **Aksharantar** — AI4Bharat. Hugging Face `ai4bharat/Aksharantar`; paper "Aksharantar: Towards building open transliteration tools for the next billion users." Licences CC-BY / CC0.
- **Dakshina** — Google Research. GitHub `google-research-datasets/dakshina`; Roark et al., LREC 2020. Licence CC BY-SA 4.0.
- **IndicXlit** — AI4Bharat. GitHub `AI4Bharat/IndicXlit`; `pip install ai4bharat-transliteration`.
- **Underlying Modi character-recognition lineage** — Deshmukh, Patil & Kolhe (2015), "Off-line Handwritten Modi Numerals Recognition using Chain Code"; Chandure & Inamdar (2021), "Offline handwritten MODI character recognition using GoogLeNet and AlexNet," ICCMS.

*Verify dataset sizes, DOIs, and licence terms on the source pages before formal use — repositories update over time.*


