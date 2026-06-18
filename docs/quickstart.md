# Quickstart

Install dependencies, then run the Gradio demo on any Modi image.

```bash
pip install -r requirements.txt
python app.py
# Open http://localhost:7860 in your browser
# Drag in a Modi image → click "Transliterate →"
```

## Requirements

- Python 3.10+
- A CUDA GPU is strongly recommended (the model is ~3B parameters; runs in 4-bit on ~8.5 GB VRAM)

## Expected output

The model produces a Devanagari first draft. A human expert should review and correct it — corrections can be saved back as training data to improve the next version.

## CLI / scripting (coming soon)

A command-line entry point (`src/transliterate.py`) is planned but not yet implemented. For now, use `app.py` or call the inference logic directly from `scripts/06_evaluate.py` as a reference.

## Next step

See [`docs/model.md`](model.md) for details on the underlying model.
