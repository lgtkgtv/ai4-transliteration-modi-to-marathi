# मोडी ते मराठी (modi-to-Marathi)

**AI-assisted transliteration of the historic Modi script into Marathi (Devanagari).**

> Task: **Modi script (handwritten historical manuscripts) → Marathi text in Devanagari.**

Maintainer: **Sachin** ([@lgtkgtv](https://github.com/lgtkgtv)) · Status: **Phase 1 MVP — working fine-tuned model + Gradio demo**

---

## What this project is

The Modi script was used to write Marathi for centuries, and tens of millions of historical documents remain in it — land records, administrative records, and more — that very few people can still read. This project builds an **open, human-in-the-loop pipeline** to transliterate Modi manuscripts into Marathi (Devanagari) faster and more accessibly.

This is **transliteration, not translation** — the language (Marathi) stays the same; only the script changes from Modi to Devanagari.

---

## Results

| Model | CER | Notes |
|---|---|---|
| Qwen2.5-VL-3B (zero-shot) | 0.930 | No fine-tuning |
| Qwen2.5-VL-3B + QLoRA on MoDeTrans | **0.332** | 64% improvement |
| Qwen2.5-VL-3B + QLoRA on MoDeTrans + SynthMoDe | TBD | Training in progress |

CER = Character Error Rate (0.0 is perfect; 0.332 means ~1 in 3 characters needs expert correction).

Fine-tuned adapter: [lgtk/qwen25vl-3b-modi-lora](https://huggingface.co/lgtk/qwen25vl-3b-modi-lora) on Hugging Face.

---

## Quick start — run the demo

### Requirements

- **GPU:** NVIDIA RTX 5060 (16 GB VRAM) or equivalent with CUDA 12.8+ support
- **RAM:** 16 GB+
- **Python:** 3.12
- **OS:** Linux (tested on Ubuntu 24.04 / WSL2)

### 1. Clone and set up environment

```bash
git clone https://github.com/lgtkgtv/ai4-transliteration-modi-to-marathi.git
cd ai4-transliteration-modi-to-marathi

# Install uv (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv --python 3.12

# Install PyTorch with CUDA 12.8 (required for Blackwell/Ada/Ampere GPUs)
uv pip install torch==2.11.0+cu128 torchvision==0.26.0+cu128 \
  --extra-index-url https://download.pytorch.org/whl/cu128

# Install all other dependencies
uv pip install -r requirements.txt
```

### 2. Set your Hugging Face token

```bash
export HF_TOKEN=<your_hf_read_token>   # from https://huggingface.co/settings/tokens
```

### 3. Run the demo

```bash
.venv/bin/python app.py
```

Open [http://localhost:7860](http://localhost:7860) in your browser. The app loads the fine-tuned adapter automatically — from local `models/` if present, otherwise from Hugging Face Hub.

---

## Repository structure

```
app.py                       # Gradio demo (load image → get Devanagari)
requirements.txt             # Python dependencies (PyTorch excluded — see above)
scripts/
  01_explore_dataset.py      # Download MoDeTrans and print sample rows
  02_prepare_splits.py       # Create 80/10/10 train/val/test splits → data/
  03_zero_shot.py            # Run zero-shot baseline on 5 examples
  05_train_qlora.py          # QLoRA fine-tuning on MoDeTrans (real data only)
  06_evaluate.py             # Run evaluation on all 204 test examples → results/
  07_train_with_synth.py     # QLoRA fine-tuning on MoDeTrans + SynthMoDe combined
results/
  zero_shot_sample.json      # 5 zero-shot examples with CER
  evaluation_report.json     # 204 test results with per-example CER
samples/
  index.json                 # 30 sample images with ground truth and CER
  *.jpg                      # Sample images (10 best / 10 middle / 10 worst CER)
docs/                        # Phase 0 planning and stakeholder documents
```

`data/` and `models/` are not in git (large files). Re-create them:

```bash
.venv/bin/python scripts/02_prepare_splits.py   # downloads MoDeTrans, creates data/
.venv/bin/python scripts/05_train_qlora.py      # trains and saves models/
```

Or just use the published adapter from Hugging Face — `app.py` does this automatically.

---

## Training details

**Base model:** [Qwen/Qwen2.5-VL-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct)

**Training data:** [historyHulk/MoDeTrans](https://huggingface.co/datasets/historyHulk/MoDeTrans) — 2,043 real Modi document images with expert-verified Devanagari. Split 80/10/10.

**Method:** QLoRA — 4-bit NF4 quantization + LoRA adapters (rank=32, alpha=64) on all attention and MLP projection layers. 1.94% of weights trainable (74M/3.8B).

**Hardware:** NVIDIA RTX 5060 (16 GB) · Training time: ~7.5 hours for 3 epochs.

**Hyperparameters:** lr=2e-4, cosine decay, warmup 3%, grad accumulation=8, batch=1.

---

## Pipeline (planned)

```
Modi image → preprocessing (grayscale → denoise → threshold → deskew)
           → VLM inference (draft Devanagari)
           → post-processing
           → expert correction
           → corrections saved as new training data
```

---

## Background & references

- Reference paper: *Historic Scripts to Modern Vision* (Kausadikar, Kale, Susladkar, Mittal), ICDAR 2025 — [arXiv:2503.13060](https://arxiv.org/abs/2503.13060)
- MoDeTrans dataset: [`historyHulk/MoDeTrans`](https://huggingface.co/datasets/historyHulk/MoDeTrans) on Hugging Face
- Synthetic dataset: [`historyHulk/SynthMoDe`](https://huggingface.co/datasets/historyHulk/SynthMoDe) on Hugging Face
- Reference model (12B, gated): [`historyHulk/ModiTrans-12B-Gemma-Teacher`](https://huggingface.co/historyHulk/ModiTrans-12B-Gemma-Teacher)
- Our fine-tuned adapter (3B): [`lgtk/qwen25vl-3b-modi-lora`](https://huggingface.co/lgtk/qwen25vl-3b-modi-lora)

---

## Known limitations

- Performs best on formal Peshwekalin/Shivakalin letters (majority of MoDeTrans training data)
- Struggles with Modi abbreviations, scribal shorthand, and mixed Modi/English text
- No era metadata in MoDeTrans — cannot yet filter by Anglakalin era (project priority)
- Output may contain repetition loops on difficult images (CER > 1.0 in those cases)

---

## License

Code: MIT. Dataset provenance and licensing details: `docs/05_Datasets-for-Transliteration.md`.

---

*Open effort to preserve and improve access to Marathi heritage in Modi script. Corrections and contributions welcome.*
