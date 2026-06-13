# मोडी ते मराठी (modi-to-Marathi)

**AI-assisted transliteration of the historic Modi script into Marathi (Devanagari).**

> Task: **Modi script (handwritten historical manuscripts) → Marathi text in Devanagari.**

Maintainer: **Sachin** ([@lgtkgtv](https://github.com/lgtkgtv)) · Status: **Phase 0 — Scoping & Dataset Preparation**

---

## What this project is

The Modi script was used to write Marathi for centuries, and an estimated tens of millions of historical documents remain in it — land records, administrative records, and more — that very few people can still read. This project aims to build an **open, human-in-the-loop pipeline** that helps experts transliterate Modi documents into Marathi (Devanagari) faster and more accessibly.

We are starting from scratch, deliberately, with **dataset preparation as the first sub-project** — because in this field the dataset and the expert-review process, not the model, determine success.

## Repository contents

| Path | Purpose |
|---|---|
| `docs/01_Prior-Work-Assessment.md` | What already exists publicly, how good it is, and how its quality was verified |
| `docs/02_Scoping-Questionnaire.md` | Questions for contributors and faculty advisors to scope the project |
| `docs/03_Dataset-Preparation-Plan.md` | Our Phase 0 plan for building the labeled dataset |

These documents are **drafts circulated for stakeholder input** — contributors and faculty advisors are invited to correct and extend them.

## Background & references

- Reference paper: *Historic Scripts to Modern Vision* (Kausadikar, Kale, Susladkar, Mittal), ICDAR 2025 — arXiv:2503.13060
- Open datasets to study/reuse: `historyHulk/MoDeTrans`, `historyHulk/SynthMoDe` (Hugging Face)
- Reference model: `historyHulk/ModiTrans-12B-Gemma-Teacher` (Hugging Face, gated)

## How to contribute

1. Read the three documents in `docs/`.
2. Source contributors: see Part A of the scoping questionnaire.
3. Faculty advisors: see Part B.
4. Everyone: weigh in on the shared decisions in Part C.

## License

To be decided (see scoping questionnaire C6). Recommend an open license for documentation (e.g. CC BY 4.0) and a separate decision for any dataset we release.

---

*This is an early-stage, good-faith effort to preserve and open up access to Marathi heritage written in Modi. Corrections and contributions are welcome.*
