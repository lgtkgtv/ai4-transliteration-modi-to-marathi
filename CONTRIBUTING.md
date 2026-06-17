# Contributing

## Adding training data

All data additions go through human expert review before entering the training set. The pipeline is **assistive** — the model produces a first draft, an expert corrects it, and corrections are saved back as training data.

Provenance must be recorded for every example (source, licence, contributor). See [`docs/data.md`](docs/data.md) for the dataset landscape and licensing constraints.

## Human-in-the-loop rule

No model output goes into the gold test set or published dataset without expert verification. This is non-negotiable — historical records are too important to trust to an unchecked model.

## Where the planning docs live

Background reading (Modi script history, AI/ML primers, prior-work assessment, scoping, and the dataset plan) is in the companion handbook — kept separate from this code repo on purpose.

## Code

- Python 3.10+; dependencies in `requirements.txt`
- Scripts in `scripts/`; source code in `src/` (in progress)
- Open an issue before starting significant work
