# Scoping Questions for the Team

**Project:** मोडी ते मराठी (modi-to-Marathi) — Modi script → Marathi (Devanagari)
**Repository:** https://github.com/lgtkgtv/ai4-transliteration-modi-to-marathi
**From:** Sachin, Project Maintainer
**To:** Project contributors and faculty advisors
**Date:** [Date]
**Re:** Questions I need answered before we can scope the work and budget effort

---

## Why I'm asking

Team — to plan this properly (and avoid wasting anyone's time or materials), I need to lock down a handful of decisions up front. A few of these will sound basic, but getting them wrong early is expensive to fix later.

Please answer the sections relevant to you. **Contributors** of source material: focus on Part A. **Faculty advisors:** focus on Part B. **Everyone:** please weigh in on Part C. There are no wrong answers — "we don't know yet" is a perfectly useful response that tells me where to dig.

Our source→target is settled: **Modi script (handwritten manuscripts) → Marathi in Devanagari.** Most remaining questions are about *the material, the experts, and our goals.*

---

## Part A — For those contributing source material

The biggest factor in our design is *what form our Modi material physically takes*. (For Modi this is almost certainly scanned/photographed manuscripts rather than digital text — but please confirm.)

**A1. What physical form are the Modi sources in?**
(scanned manuscripts, photographs, printed reproductions, a mix)
> Response:

**A2. Roughly how many items can we expect, and over what timeframe?**
(e.g. ~500 pages now, ~2,000 more over six months)
> Response:

**A3. What condition are they in?**
(faded ink, torn pages, bleed-through, clean modern scans, varying quality)
> Response:

**A4. Which eras, regions, or handwriting styles do they span?**
(e.g. Shivakalin / Peshwekalin / Anglakalin; styles like Chitnisi, Mahadevpanti, Bilavalkari, Ranadi — this strongly affects how much data we'll need)
> Response:

**A5. Are there access, copyright, or sensitivity restrictions on the material?**
(many archives restrict redistribution — we must respect this, especially if we publish the dataset)
> Response:

**A6. In what format and resolution will images be provided?**
(file type, approximate resolution/DPI, naming convention)
> Response:

---

## Part B — For faculty advisors

**B1. What prior research have you (or close colleagues) done on Modi recognition or transliteration?**
(papers, datasets, tools — anything we should build on rather than redo)
> Response:

**B2. Which existing Modi datasets could we license, reuse, or learn from?**
(public or private — see the dataset plan for the ones I've already found)
> Response:

**B3. How was correctness verified in the work you know of?**
(what metrics, what human-checking process, what counts as "good enough")
> Response:

**B4. Beyond the known confusable characters, what are the hard cases for Modi → Marathi?**
(ambiguity, missing word boundaries, diacritics, rare ligatures, era-specific forms)
> Response:

**B5. How many qualified Modi experts can realistically transliterate for us, and how much of their time might we access?**
(this is usually the true bottleneck — I'd rather know the constraint now)
> Response:

**B6. What would make this project genuinely useful to researchers like you?**
(so we build for real use, not just a demo)
> Response:

---

## Part C — Shared decisions for everyone

**C1. Source → target** — *proposed:* **Modi script images → Marathi (Devanagari) text.** Confirm or refine.
> Response:

**C2. What is success for *version 1*?**
(e.g. "a usable first-draft transliteration an expert can quickly correct", "publishable accuracy", "a released open dataset")
> Response:

**C3. Who are the end users, and how will they use the output?**
(historians, archivists, the public, an internal tool)
> Response:

**C4. Where does this eventually need to run?**
(a single offline desktop, a shared server/service, cloud-on-demand, undecided)
> Response:

**C5. What are our constraints?**
(timeline, budget for compute or annotation, must-be-open-source, licensing)
> Response:

**C6. Is the *dataset itself* a deliverable we want to publish openly?**
(this changes our quality bar and our consent/licensing process)
> Response:

---

## What happens after you respond

Once I have these answers I'll come back with a concrete plan: the data we need to create or source, which existing tools we should test first, a realistic effort and timeline estimate, and clear roles. The most important near-term answers are **A1–A4** (what material we actually have) and **B5** (expert availability) — if you can prioritize those, it unblocks the most planning.

Thank you for taking the time.

— Sachin
