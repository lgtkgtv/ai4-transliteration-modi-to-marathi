# Phase 0: Building the Dataset

**Project:** मोडी ते मराठी (modi-to-Marathi) — Modi script → Marathi (Devanagari)
**Repository:** https://github.com/lgtkgtv/ai4-transliteration-modi-to-marathi
**From:** Sachin, Project Maintainer
**To:** Project contributors and faculty advisors
**Date:** [Date]
**Re:** Our first real piece of work — and why it isn't the model

---

## The core message

Team — it's tempting to think of this as an "AI model" project, but I want to set expectations clearly: **our first and most important sub-project is building a high-quality, labeled dataset of Modi documents paired with verified Marathi (Devanagari) transliterations.** Every successful project I've studied in this area succeeded or failed on the strength of its dataset and its expert-review process, not its choice of model. The model is the comparatively easy part.

So Phase 0 is about data. Below is how I propose we approach it. Please challenge anything that doesn't fit our reality.

---

## 1. What a "labeled example" means for us

For Modi → Marathi, a labeled example is:

> **an image of Modi text → its correct, expert-verified Marathi transliteration in Devanagari.**

We can't build anything until we agree on the exact unit (a full page? a few lines? a single line?) and a consistent way to produce these pairs. The reference project segmented each document into parts of **3–4 lines** before transliterating — a reasonable starting convention for us to discuss.

---

## 2. Do this first: a small, gold-standard test set

Before generating any volume of data, we need a **small set of examples verified to be correct beyond doubt** — on the order of a few hundred. This is non-negotiable, for one reason:

> Without a trustworthy test set, we cannot tell whether anything we later build is actually working. Every accuracy number we ever report depends on it.

This test set should be:
- transliterated by our **most qualified Modi experts**,
- **cross-checked** by a second expert,
- **locked and never used for training** — kept aside purely for measurement,
- ideally **spanning the eras and styles** we expect to encounter, so it's representative.

If we do nothing else in month one, we should produce this.

---

## 3. How we get from raw Modi images to labeled data efficiently

We won't have unlimited expert time, so the strategy is to **minimize from-scratch labeling** and convert expert effort into *correcting drafts* wherever possible.

| Strategy | What it is | Viability for Modi → Marathi |
|---|---|---|
| **Expert gold labeling** | Experts produce verified pairs from scratch | Required for the test set and a small training seed |
| **Synthetic generation** | Render Modi images from known Marathi/Devanagari text using Modi fonts | **Strong option for us** — see section 4 |
| **Reuse existing datasets** | Build on already-published Modi datasets | **Available** — see section 5 |
| **Bootstrap-and-correct** | A rough first model drafts labels; experts only fix errors | High value once we have any working model |
| **Active learning** | Prioritize labeling the examples the model is least sure about | To stretch limited expert hours |
| **Correction flywheel** | Model drafts → expert corrects → corrections become new training data | Ongoing, compounds over time |

The principle behind all of these: **correcting a draft is far cheaper than writing a label from scratch.**

---

## 4. Synthetic data is genuinely viable for us

Because open **Modi fonts exist**, we can render Modi-script images from any Marathi (Devanagari) text we have — generating large amounts of training data cheaply. The reference project did exactly this using:

- **MarathiCursive** (an open Modi/Marathi cursive font)
- **Noto Sans Modi** (Google's open Modi font)

Synthetic data won't capture the messiness of real faded manuscripts, so it can't replace real data — but it's an excellent way to **bulk up training cheaply** and pre-train before fine-tuning on our real, expert-verified examples. **Worth piloting early.**

---

## 5. Existing Modi datasets we should investigate for reuse

We don't have to start completely empty. These have been published (mostly via IEEE DataPort / Hugging Face) and are worth evaluating — with the caveat that **most are character-level, not full-document transliteration**, so they help recognition more than end-to-end transliteration:

| Dataset | Type |
|---|---|
| `historyHulk/MoDeTrans` | Full Modi documents → Devanagari (closest to our task) |
| `historyHulk/SynthMoDe` | Synthetic Modi → Devanagari |
| Modi-HHDoc | ~3,350 Modi documents |
| MODI-HChar | Individual Modi characters |
| Handwritten Modi Lipi Barakhadi | Character/syllable set |
| Handwritten Modi Characters | Individual characters |

**Advisors — please tell me which of these you trust, and whether their licenses allow our intended use.**

---

## 6. Quality standards we should agree on now

To keep the dataset trustworthy and publishable later, I propose we adopt these from day one:

- **Written transliteration guidelines** so every contributor is consistent — explicitly covering the known confusable Modi characters (भ/म, क/फ, ट/ठ/ढ, न/ण), vowel signs, and the **anusvāra** dot, plus how to mark *uncertain* readings.
- **A second-reviewer pass** on a defined percentage of examples.
- **Strict separation** of training, validation, and test data — with a manual check that no item appears in more than one (the reference team used 10 annotators for exactly this).
- **Provenance tracking** — for every item, record its source archive and who verified it (also important for licensing if we publish).
- **A consistent, documented preprocessing recipe** for images (grayscale → denoise → adaptive threshold → deskew → consistent sizing), applied identically to every item.

---

## 7. Proposed roles

| Role | Who | Responsibility |
|---|---|---|
| Source contributors | [names] | Provide Modi material in an agreed format, with provenance |
| Expert transliterators | [names] | Produce and verify the gold and seed labels |
| Reviewers | [names] | Second-pass cross-checking |
| Engineering | Sachin + [names] | Preprocessing, tooling, the correction interface, split management |
| Coordination | Sachin | Guidelines, schedule, quality tracking |

Please correct these — I've guessed at the structure.

---

## 8. Minimum viable targets (to refine with your input)

We don't need a massive corpus to begin. A realistic v1 footing:
- a **few hundred** locked, expert-verified test examples (representative across eras),
- a **seed set** of verified real training examples,
- a **larger synthetic set** (rendered with Modi fonts) to bulk up training cheaply,
- optionally, **vetted reuse** of an existing dataset from section 5.

Exact numbers depend on the scoping answers (expert availability, source condition, era variation). I'll propose firm targets once those come back.

---

## 9. Risks I want us to manage from the start

| Risk | Why it hurts | How we mitigate |
|---|---|---|
| Too few Modi experts | Labeling becomes the project bottleneck | Reserve experts for the test set + corrections, not bulk labeling |
| Inconsistent labels | Quietly destroys accuracy and trust | Shared written guidelines + second reviewer |
| Data leakage | Makes our results look better than they are | Manual split verification, provenance tracking |
| Over-reliance on synthetic data | Looks good in tests, fails on real manuscripts | Always measure on *real* held-out documents |
| Skipping the test set | We can't measure progress at all | Build it first, before anything else |
| Over-building the model early | Wasted effort before data is ready | Baseline with existing tools before training our own |

---

## 10. What I need from each of you to start

- **Contributors:** confirm the format and provenance details, and start assembling a first small batch.
- **Experts/advisors:** help me draft the transliteration guidelines and define what "verified" means for Modi, and tell me which existing datasets in section 5 we can trust and legally reuse.
- **Everyone:** agree on the definition of a "labeled example" (section 1) so we're all building the same thing.

If we get the gold test set, the guidelines, and a synthetic-data pilot right in the first stretch, everything afterward gets much easier. Happy to walk any of this through live.

— Sachin
