"""
Phase 1: Zero-shot baseline — run Qwen2.5-VL-3B on Modi images with no training.
Run: .venv/bin/python scripts/03_zero_shot.py

Downloads ~7GB on first run (cached afterwards).
Outputs predicted Devanagari text alongside ground truth.
"""

import torch
import json
from pathlib import Path
from datasets import load_from_disk
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
from transformers import BitsAndBytesConfig

# ── Config ────────────────────────────────────────────────────────────────────
MODEL_ID  = "Qwen/Qwen2.5-VL-3B-Instruct"
TEST_DIR  = "data/modetrans_splits/test"
N_SAMPLES = 5   # number of test examples to run (full test = 204, slow without batching)
RESULTS_F = Path("results/zero_shot_sample.json")

PROMPT = (
    "This image contains handwritten text in Modi script, a historical cursive script "
    "used to write the Marathi language. "
    "Transliterate the text in this image into Devanagari script. "
    "Output only the Devanagari text, with no explanation or extra words."
)

# ── Load model in 4-bit quantization ─────────────────────────────────────────
print(f"Loading {MODEL_ID} in 4-bit quantization...")
print("(First run downloads ~7 GB — subsequent runs load from cache)\n")

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",           # NF4: best quality 4-bit format
    bnb_4bit_compute_dtype=torch.bfloat16,  # compute in bfloat16 for speed
)

model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    MODEL_ID,
    quantization_config=bnb_config,
    device_map="auto",
)
processor = AutoProcessor.from_pretrained(MODEL_ID)

print(f"Model loaded. VRAM used: "
      f"{torch.cuda.memory_allocated() / 1e9:.1f} GB / "
      f"{torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB\n")

# ── Load test split ───────────────────────────────────────────────────────────
test = load_from_disk(TEST_DIR)
samples = test.select(range(N_SAMPLES))

# ── Run inference ─────────────────────────────────────────────────────────────
results = []

for i, example in enumerate(samples):
    image    = example["image"]
    gt_text  = example["text"]
    filename = example["filename"]

    # Build the chat message Qwen2.5-VL expects
    messages = [{
        "role": "user",
        "content": [
            {"type": "image", "image": image},
            {"type": "text",  "text": PROMPT},
        ],
    }]

    # Apply the model's chat template to format inputs correctly
    text_input = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = processor(
        text=[text_input],
        images=[image],
        return_tensors="pt",
    ).to(model.device)

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=False,   # greedy decode — deterministic output
        )

    # Decode only the newly generated tokens (not the input prompt)
    generated = processor.batch_decode(
        output_ids[:, inputs["input_ids"].shape[1]:],
        skip_special_tokens=True,
    )[0].strip()

    results.append({
        "filename" : filename,
        "ground_truth": gt_text,
        "predicted"   : generated,
    })

    print(f"[{i+1}/{N_SAMPLES}] {filename}")
    print(f"  GT : {gt_text[:80]}")
    print(f"  OUT: {generated[:80]}")
    print()

# ── Save results ──────────────────────────────────────────────────────────────
RESULTS_F.parent.mkdir(exist_ok=True)
RESULTS_F.write_text(json.dumps(results, ensure_ascii=False, indent=2))
print(f"Results saved to {RESULTS_F}")
