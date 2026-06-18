"""
Upload README.md model cards to both HuggingFace adapter repos.

Usage:
  .venv/bin/python scripts/push_model_cards.py
"""

from huggingface_hub import upload_file

# ── Shared content blocks ─────────────────────────────────────────────────────

USAGE_SNIPPET = '''\
```python
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor, BitsAndBytesConfig
from peft import PeftModel
from PIL import Image
import torch

MODEL_ID    = "Qwen/Qwen2.5-VL-3B-Instruct"
ADAPTER_ID  = "{adapter_id}"   # ← this repo

bnb = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)
base  = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            MODEL_ID, quantization_config=bnb, device_map="auto")
model = PeftModel.from_pretrained(base, ADAPTER_ID)
model.eval()
processor = AutoProcessor.from_pretrained(MODEL_ID, max_pixels=512 * 28 * 28)

PROMPT = (
    "This image contains handwritten text in Modi script, a historical cursive "
    "script used to write the Marathi language. "
    "Transliterate the text in this image into Devanagari script. "
    "Output only the Devanagari text, with no explanation."
)

image = Image.open("your_modi_image.jpg").convert("RGB")
messages = [{
    "role": "user",
    "content": [
        {{"type": "image", "image": image}},
        {{"type": "text",  "text": PROMPT}},
    ],
}]
text_in = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs  = processor(text=[text_in], images=[image], return_tensors="pt").to(model.device)

with torch.no_grad():
    out = model.generate(**inputs, max_new_tokens=256, do_sample=False)

result = processor.batch_decode(
    out[:, inputs["input_ids"].shape[1]:], skip_special_tokens=True
)[0].strip()
print(result)
```'''

LIMITATIONS = """\
## Known limitations

- **Deletions dominate errors (46%)** — the model tends to skip characters,
  especially the anusvāra diacritic (ं, ~240 drops per 204-example test run)
- **Vowel length confusion** — ी ↔ ि (long/short /i/) and ू ↔ ु (long/short /u/)
  are the most common substitution pairs
- **No word boundaries** — Modi script is continuous (no spaces), so errors
  sometimes span phrase boundaries
- **Best on formal letters** — trained on Peshwekalin / Shivakalin administrative
  documents; performance on informal or personal correspondence may be lower
- **Image preprocessing not yet implemented** — the model receives raw images.
  Denoising, deskewing, and binarisation would likely improve accuracy.
"""

HARDWARE_NOTE = """\
## Hardware

Developed and tested on a desktop with an **NVIDIA RTX 5060 GPU (8.5 GB VRAM)**
running WSL2 on Windows.
At 4-bit NF4 quantization, the adapter uses approximately 3–4 GB of VRAM during inference.
A 5060 or better is recommended; the pipeline should also fit on any GPU with ≥6 GB VRAM.
"""

# ── Real-data-only model card ─────────────────────────────────────────────────

README_REAL = """\
---
language:
  - mr
license: apache-2.0
base_model: Qwen/Qwen2.5-VL-3B-Instruct
tags:
  - modi-script
  - marathi
  - transliteration
  - historical-documents
  - qlora
  - peft
  - vision-language-model
datasets:
  - historyHulk/MoDeTrans
metrics:
  - cer
model-index:
  - name: qwen25vl-3b-modi-lora
    results:
      - task:
          type: image-to-text
          name: Modi Script Transliteration
        dataset:
          name: MoDeTrans (held-out test set, 204 examples)
          type: historyHulk/MoDeTrans
        metrics:
          - type: cer
            value: 0.332
            name: Character Error Rate
---

# qwen25vl-3b-modi-lora

A **QLoRA adapter** for Modi script → Devanagari (Marathi) transliteration,
fine-tuned on the [MoDeTrans](https://huggingface.co/datasets/historyHulk/MoDeTrans)
dataset (real handwritten Modi document images with expert-verified Devanagari text).

> **Recommended model:** [`lgtk/qwen25vl-3b-modi-synth-lora`](https://huggingface.co/lgtk/qwen25vl-3b-modi-synth-lora)
> adds synthetic training data and achieves a slightly lower CER (0.328 vs 0.332).
> Use this adapter if you want the real-data-only baseline.

**Project:** [modi-to-Marathi on GitHub](https://github.com/lgtkgtv/ai4-transliteration-modi-to-marathi)

---

## Model details

| | |
|---|---|
| **Base model** | Qwen/Qwen2.5-VL-3B-Instruct |
| **Fine-tuning method** | QLoRA — LoRA rank 32, alpha 64, 4-bit NF4 quantization |
| **LoRA target modules** | q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj |
| **Trainable parameters** | 74M (1.94% of 3.8B total) |
| **Training data** | MoDeTrans — 1,635 real document images (80/10/10 split, seed=42) |
| **Training epochs** | 3 |
| **Training time** | ~7.5 hours on RTX 5060 (8.5 GB VRAM) |
| **Test CER** | **0.332** (on 204 held-out MoDeTrans examples) |
| **Zero-shot baseline CER** | 0.930 |

A CER of 0.332 means approximately 33% of characters require expert correction —
suitable as a first-draft assistant in a human-in-the-loop workflow.

---

## Task

**Input:** photograph or scan of a handwritten Modi-script Marathi document
**Output:** Devanagari transliteration of that text

This is *transliteration*, not translation — the language (Marathi) does not change,
only the script. Modi was the administrative script of Maharashtra from roughly the
13th to the mid-20th century; most surviving documents are from the Shivakalin (17th c.),
Peshwekalin (18th–early 19th c.), and Anglakalin (1818–1952) eras.

---

## How to use

Install dependencies:
```bash
pip install transformers peft bitsandbytes accelerate pillow torch
```

""" + USAGE_SNIPPET.replace("{adapter_id}", "lgtk/qwen25vl-3b-modi-lora") + "\n\n---\n\n" + LIMITATIONS + "\n---\n\n" + HARDWARE_NOTE + """\

---

## Citation / acknowledgements

- **MoDeTrans dataset:** IIT Roorkee — `historyHulk/MoDeTrans` on HuggingFace
- **Base model:** Qwen/Qwen2.5-VL-3B-Instruct (Apache 2.0)
- Developed by Sachin Godse ([@lgtkgtv](https://github.com/lgtkgtv)) using Claude CLI (Anthropic)
"""

# ── Real + synthetic model card ───────────────────────────────────────────────

README_SYNTH = """\
---
language:
  - mr
license: apache-2.0
base_model: Qwen/Qwen2.5-VL-3B-Instruct
tags:
  - modi-script
  - marathi
  - transliteration
  - historical-documents
  - qlora
  - peft
  - vision-language-model
datasets:
  - historyHulk/MoDeTrans
  - historyHulk/SynthMoDe
metrics:
  - cer
model-index:
  - name: qwen25vl-3b-modi-synth-lora
    results:
      - task:
          type: image-to-text
          name: Modi Script Transliteration
        dataset:
          name: MoDeTrans (held-out test set, 204 examples)
          type: historyHulk/MoDeTrans
        metrics:
          - type: cer
            value: 0.328
            name: Character Error Rate
---

# qwen25vl-3b-modi-synth-lora

A **QLoRA adapter** for Modi script → Devanagari (Marathi) transliteration,
fine-tuned on [MoDeTrans](https://huggingface.co/datasets/historyHulk/MoDeTrans)
(real handwritten Modi documents) **plus** [SynthMoDe](https://huggingface.co/datasets/historyHulk/SynthMoDe)
(synthetic Modi images rendered from the same Devanagari text using Modi fonts).

**This is the recommended adapter** — it achieves the best test CER (0.328) and
is the default in the project's Gradio demo and CLI inference script.

**Project:** [modi-to-Marathi on GitHub](https://github.com/lgtkgtv/ai4-transliteration-modi-to-marathi)

---

## Model details

| | |
|---|---|
| **Base model** | Qwen/Qwen2.5-VL-3B-Instruct |
| **Fine-tuning method** | QLoRA — LoRA rank 32, alpha 64, 4-bit NF4 quantization |
| **LoRA target modules** | q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj |
| **Trainable parameters** | 74M (1.94% of 3.8B total) |
| **Training data** | MoDeTrans (1,635 real) + SynthMoDe (4,086 synthetic) = **5,721 total** |
| **Training epochs** | 2 |
| **Training time** | ~9.75 hours on RTX 5060 (8.5 GB VRAM) |
| **Test CER** | **0.328** (on 204 held-out MoDeTrans examples; real images only) |
| **Zero-shot baseline CER** | 0.930 |

A **65% reduction** in character error rate vs zero-shot. CER 0.328 means roughly
33% of characters require expert correction — designed for human-in-the-loop use.

### CER distribution (204 test examples)

| Quality tier | CER range | Count |
|---|---|---|
| Perfect | 0.0 | 3 |
| Excellent | < 0.10 | 5 |
| Good | 0.10–0.20 | 38 |
| Fair | 0.20–0.40 | 109 |
| Poor | 0.40–0.70 | 44 |
| Very poor | 0.70–1.0 | 3 |
| Hallucination loops | > 1.0 | 2 |

The majority of examples fall in the "fair" tier — usable as a first draft for expert review.

### Effect of synthetic data vs real-only adapter

| Model | Test CER | Poor + worse |
|---|---|---|
| Real data only (`lgtk/qwen25vl-3b-modi-lora`) | 0.332 | 59 examples |
| Real + synthetic (this adapter) | 0.328 | 47 examples |

Synthetic data gave a small but consistent improvement, mainly reducing poor-tier examples.
Vowel-length confusion was unchanged (font rendering does not capture that ambiguity).

---

## Task

**Input:** photograph or scan of a handwritten Modi-script Marathi document
**Output:** Devanagari transliteration of that text

This is *transliteration*, not translation — the language (Marathi) does not change,
only the script. Modi was the administrative script of Maharashtra from roughly the
13th to the mid-20th century; most surviving documents are from the Shivakalin (17th c.),
Peshwekalin (18th–early 19th c.), and Anglakalin (1818–1952) eras.

---

## How to use

Install dependencies:
```bash
pip install transformers peft bitsandbytes accelerate pillow torch
```

""" + USAGE_SNIPPET.replace("{adapter_id}", "lgtk/qwen25vl-3b-modi-synth-lora") + "\n\n---\n\n" + LIMITATIONS + "\n---\n\n" + HARDWARE_NOTE + """\

---

## Citation / acknowledgements

- **MoDeTrans dataset:** IIT Roorkee — `historyHulk/MoDeTrans` on HuggingFace
- **SynthMoDe dataset:** IIT Roorkee — `historyHulk/SynthMoDe` on HuggingFace
- **Base model:** Qwen/Qwen2.5-VL-3B-Instruct (Apache 2.0)
- Developed by Sachin Godse ([@lgtkgtv](https://github.com/lgtkgtv)) using Claude CLI (Anthropic)
"""

# ── Upload ────────────────────────────────────────────────────────────────────

def upload_card(repo_id, content):
    import io
    upload_file(
        path_or_fileobj=io.BytesIO(content.encode()),
        path_in_repo="README.md",
        repo_id=repo_id,
        repo_type="model",
        commit_message="Add model card with usage instructions and evaluation results",
    )
    print(f"Uploaded README.md to {repo_id}")

upload_card("lgtk/qwen25vl-3b-modi-lora",       README_REAL)
upload_card("lgtk/qwen25vl-3b-modi-synth-lora", README_SYNTH)
print("Done.")
