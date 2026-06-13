# Prior Work Assessment & What We Can Reuse

**Project:** मोडी ते मराठी (modi-to-Marathi) — Modi script → Marathi (Devanagari)
**Repository:** https://github.com/lgtkgtv/ai4-transliteration-modi-to-marathi
**From:** Sachin, Project Maintainer
**To:** Project contributors and faculty advisors
**Date:** [Date]
**Re:** What already exists publicly, how good it is, and how its quality was verified

---

## A note before you read

Team — before we ask anyone to contribute images or spend expert hours, I wanted us to start from a shared understanding of what's *already* been done and published for exactly our task: transliterating Modi script into Marathi (Devanagari). Below is my current reading of the most relevant prior project. **Several of you have researched this topic directly, so please treat this as a draft for you to correct** — where I've got something wrong or oversimplified, I'd rather hear it now than after we've built on a bad assumption.

This document answers three questions together:
1. What can we reuse instead of rebuilding?
2. How good is it, really?
3. How did they *prove* it was good — and how would we check that ourselves?

---

## 1. The reference project

The closest published work to ours is from **IIT Roorkee**: *"Historic Scripts to Modern Vision: A Novel Dataset and a VLM Framework for Transliteration of Modi Script to Devanagari."* It targets the same source→target we do.

| Detail | Value |
|---|---|
| Authors | H. Kausadikar, T. Kale (co-first), O. Susladkar, S. Mittal |
| Preprint | arXiv:2503.13060 |
| Peer-reviewed | ICDAR 2025, Springer LNCS, DOI 10.1007/978-3-032-04630-7_3 |
| Public org | `historyHulk` on Hugging Face |

It's the first published attempt to transliterate **whole handwritten Modi documents** (not just isolated characters) directly into Devanagari — which is precisely our goal.

---

## 2. What they open-sourced, and how we'd access it

| Artifact | What it is | Access |
|---|---|---|
| `historyHulk/MoDeTrans` | ~2,043 real Modi manuscript images + verified Devanagari | Public |
| `historyHulk/SynthMoDe` | Synthetic Modi images rendered from the same Devanagari text | Public |
| `historyHulk/ModiTrans-12B-Gemma-Teacher` | A model adapter (built on Google's Gemma-3-12B) | Gated — free account + accept terms |

Their dataset composition tells us which eras they prioritized — useful as a reference point for our own collection:

| Era | Images | Share |
|---|---|---|
| Shivakalin | 891 | 43.6% |
| Peshwekalin | 944 | 46.2% |
| Anglakalin | 208 | 10.2% |

They split the data 80:10:10 (train/test/validation). Notably, they did **not** include the older Adyakalin and Yadavkalin eras, because well-preserved documents from those periods are scarce — a constraint we'll likely share.

---

## 3. An important practical caveat (please sanity-check me on this)

There's a gap between what the press coverage implies and what's actually downloadable, and we should be clear-eyed about it:

- The paper's headline model is a **small, efficient 429M-parameter model** ("MoScNet-XL") trained by distilling a very large teacher.
- But the model actually **published** is the **large 12B teacher**, not that small student — and it's built on a *different* base model than the paper's headline configuration.
- As far as I can find, **the lightweight model the announcements emphasized is not yet downloadable.**

**Why this matters for us:** if we plan to "just reuse their model," we'd actually be running a heavy 12B model, and we shouldn't assume it reaches the accuracy numbers quoted in the paper. **Advisors — if any of you know whether the smaller model has since been released, please flag it.**

---

## 4. How they verified efficacy and correctness (the part I most want your eyes on)

Their credibility rests on *how* they measured success, and we should hold ourselves to the same or higher standard.

**Dataset integrity measures they used:**
- Transliterations were done by **qualified Modi-script experts**, with written guidelines to keep them objective.
- A **cross-verification** pass by experts to catch and fix transliteration errors.
- **10 annotators manually checked** the train/test/validation splits to ensure **no overlap** (no data leakage), on top of automated splitting.
- They used **only genuine historical documents** from credible archives (e.g. the Bharat Itihas Sanshodhak Mandal in Pune, archives departments) — not invented text — for the real dataset.

**How they measured model quality:**

| Method | What it checks |
|---|---|
| **BLEU score** | Overlap between the model's output text and the expert reference |
| **Character-level accuracy** (on standard OCR benchmarks) | Reading accuracy at the character level |
| **Baselines** | Compared against many prior methods (older neural nets through large language models) |
| **Ablation studies** | Removed parts of their own system to prove each part actually helps |
| **Zero-shot generalization test** | Trained on real data, tested on synthetic data, to show it didn't just memorize |

The takeaway: they didn't report a single number — they **triangulated** with multiple metrics, comparisons, and stress tests. That's the bar for us.

---

## 5. How *we* would independently verify their claims (proposed checklist)

If we build on their work, I propose we confirm it ourselves rather than take it on faith:

1. Re-run their released model on **their own published test split** and compute the scores ourselves.
2. Add a **character-level error rate** (how many characters are wrong), which is arguably more honest for transliteration than BLEU alone.
3. Test it on a **small sample of *our* Modi documents** that it has never seen, to see how it holds up outside their data.
4. Independently check for **data leakage** between splits before trusting any score.
5. Have **one of our experts spot-check** outputs for the error types that matter to us — proper nouns, place names, numbers and dates in land records.

**Advisors:** anything you'd add from your own experience reviewing or doing this kind of work?

---

## 6. The Modi-specific hard cases we already know about

From their published error analysis, the model reliably struggles with visually similar Modi characters and diacritics. We should expect — and specifically test for — these:

- **भ / म** (bha / ma)
- **क / फ** (ka / pha)
- **ट / ठ / ढ** (ṭa / ṭha / ḍha)
- **न / ण** (na / ṇa)
- Vowel-sign slips such as **के / कि** (ke / ki)
- Dropped **anusvāra** (the dot above a character), which changes pronunciation

There are also structural challenges intrinsic to Modi: a continuous *shirorekha* (top line), **no spaces between words**, and a cursive, angular style. These make segmentation genuinely hard and are worth raising with our experts early.

---

## 7. Evidence that this *class* of approach genuinely works

So we're not relying on a single project's claims, here are three independent, peer-reviewed efforts in the same family — useful both as proof-of-concept and as models of rigorous evaluation:

| Project | Task | Published in | Result & lesson |
|---|---|---|---|
| **Ithaca** (DeepMind + Venice/Oxford/Athens) | Restoring ancient Greek inscriptions | *Nature* 2022 | Historians' accuracy rose from 25% → **72%** *with* the AI. Lesson: the AI is most valuable *assisting an expert*, and they measured the combined human+AI score. |
| **Akkadian → English** (Gutherz et al.) | Cuneiform translation | *PNAS Nexus* 2023 | Worked well on short text, openly reported where it fails. Lesson: publish your failure modes, design a correction loop. |
| **IndicXlit / Aksharantar** (AI4Bharat, IIT Madras) | Transliteration across 21 Indic languages | *EMNLP Findings* 2023 | A **tiny (~11M) model** on a **huge open dataset (26M pairs)**, now deployed nationally. Lesson: for transliteration, the **dataset is the moat**, not model size. |

The recurring theme — and the most important point in this document — is that **the dataset and the human-in-the-loop process, not the model, are what make or break these projects.** That's why our first real work is dataset preparation (see `docs/03_Dataset-Preparation-Plan.md`).

---

## 8. What I need from the faculty advisors specifically

When you have time, I'd value your input on:
- Anything factually off in sections 3–6 above.
- Prior datasets, tools, or your own past work we should reuse or learn from.
- Whether the verification checklist in section 5 is sufficient.
- Pitfalls you hit in earlier research that we should design around from day one.

Thank you — I'd rather invest this alignment time now than discover gaps later.

— Sachin
