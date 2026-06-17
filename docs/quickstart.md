# Quickstart

Install, then run transliteration on one Modi image.

```bash
# TODO: fill in once the transliteration code lands in src/
pip install -r requirements.txt
python src/transliterate.py --image path/to/modi_scan.jpg
```

## Requirements

- Python 3.10+
- A CUDA GPU is strongly recommended (the model is ~3B parameters)

## Expected output

The model produces a Devanagari first draft. A human expert should review and correct it — corrections can be saved back as training data to improve the next version.

## Next step

See [`docs/model.md`](model.md) for details on the underlying model.
