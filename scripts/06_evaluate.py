"""
Phase 2: Evaluate the fine-tuned LoRA adapter on the held-out test set.
Run: .venv/bin/python scripts/06_evaluate.py

Outputs CER per example + summary to results/evaluation_report.json
"""

import torch, json
from pathlib import Path
from datasets import load_from_disk
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor, BitsAndBytesConfig
from peft import PeftModel
from jiwer import cer

MODEL_ID    = "Qwen/Qwen2.5-VL-3B-Instruct"
ADAPTER_DIR = "models/qwen25vl-3b-modi-lora/final_adapter"
TEST_DIR    = "data/modetrans_splits/test"
OUT_FILE    = Path("results/evaluation_report.json")

PROMPT = (
    "This image contains handwritten text in Modi script, a historical cursive script "
    "used to write the Marathi language. "
    "Transliterate the text in this image into Devanagari script. "
    "Output only the Devanagari text, with no explanation."
)

# ── Load model + adapter ──────────────────────────────────────────────────────
print("Loading base model + LoRA adapter...")
bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                          bnb_4bit_compute_dtype=torch.bfloat16)
base  = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            MODEL_ID, quantization_config=bnb, device_map="auto")
model = PeftModel.from_pretrained(base, ADAPTER_DIR)
model.eval()

processor = AutoProcessor.from_pretrained(MODEL_ID, max_pixels=512*28*28)
print("Ready.\n")

# ── Run inference on full test split ──────────────────────────────────────────
test    = load_from_disk(TEST_DIR)
results = []

for i, ex in enumerate(test):
    image    = ex["image"]
    gt       = ex["text"]
    filename = ex["filename"]

    messages = [{"role": "user", "content": [
        {"type": "image", "image": image},
        {"type": "text",  "text": PROMPT},
    ]}]
    text_in = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs  = processor(text=[text_in], images=[image], return_tensors="pt").to(model.device)

    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=256, do_sample=False)

    pred = processor.batch_decode(
        out[:, inputs["input_ids"].shape[1]:], skip_special_tokens=True
    )[0].strip()

    example_cer = cer(gt, pred)
    results.append({"filename": filename, "ground_truth": gt,
                    "predicted": pred, "cer": round(example_cer, 4)})

    if (i + 1) % 20 == 0:
        so_far = sum(r["cer"] for r in results) / len(results)
        print(f"  [{i+1}/204]  running mean CER: {so_far:.3f}")

# ── Summary ───────────────────────────────────────────────────────────────────
mean_cer = sum(r["cer"] for r in results) / len(results)
results_sorted = sorted(results, key=lambda r: r["cer"])

print(f"\n{'='*55}")
print(f"  Mean CER on test set: {mean_cer:.3f}  (zero-shot baseline: 0.930)")
print(f"  Improvement: {(0.930 - mean_cer):.3f} absolute CER reduction")
print(f"{'='*55}")

print("\n--- 5 BEST examples ---")
for r in results_sorted[:5]:
    print(f"  {r['filename']}  CER={r['cer']:.3f}")
    print(f"    GT  : {r['ground_truth'][:70]}")
    print(f"    PRED: {r['predicted'][:70]}")

print("\n--- 5 WORST examples ---")
for r in results_sorted[-5:]:
    print(f"  {r['filename']}  CER={r['cer']:.3f}")
    print(f"    GT  : {r['ground_truth'][:70]}")
    print(f"    PRED: {r['predicted'][:70]}")

# ── Save ──────────────────────────────────────────────────────────────────────
OUT_FILE.parent.mkdir(exist_ok=True)
OUT_FILE.write_text(json.dumps({
    "mean_cer": round(mean_cer, 4),
    "zero_shot_baseline": 0.930,
    "n_examples": len(results),
    "adapter": ADAPTER_DIR,
    "examples": results,
}, ensure_ascii=False, indent=2))
print(f"\nFull results saved to {OUT_FILE}")
