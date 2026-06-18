# CLAUDE.md

Full project context (domain knowledge, phase status, results, dataset details, pipeline notes) is in the companion handbook:

**https://github.com/lgtkgtv/modi-to-marathi-handbook** — see `CLAUDE.md` there.

## Quick orientation

- Task: handwritten Modi-script image → Devanagari text (transliteration, not translation)
- Phase 1 complete: QLoRA fine-tuned Qwen2.5-VL-3B, CER 0.332 (real data) / 0.328 (real+synthetic)
- Scripts: `scripts/` — training (05, 07), evaluation (06), error analysis (08)
- Inference demo: `app.py`
- Dataset catalogue: `docs/data.md`
- Maintainer: Sachin ([@lgtkgtv](https://github.com/lgtkgtv))
