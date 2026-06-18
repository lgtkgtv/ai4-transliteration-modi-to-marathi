"""
CLI transliteration: given a Modi image, print the Devanagari text.

Usage:
  .venv/bin/python scripts/09_infer.py samples/1672.jpg
  .venv/bin/python scripts/09_infer.py samples/1444.jpg --ground-truth "सकलगुण अलंकर्ण…"
"""

import argparse, torch
from pathlib import Path
from PIL import Image
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor, BitsAndBytesConfig
from peft import PeftModel

LOCAL_ADAPTER = "models/qwen25vl-3b-modi-synth-lora/final_adapter"
HF_ADAPTER    = "lgtk/qwen25vl-3b-modi-synth-lora"
ADAPTER_DIR   = LOCAL_ADAPTER if Path(LOCAL_ADAPTER).exists() else HF_ADAPTER
MODEL_ID      = "Qwen/Qwen2.5-VL-3B-Instruct"

PROMPT = (
    "This image contains handwritten text in Modi script, a historical cursive script "
    "used to write the Marathi language. "
    "Transliterate the text in this image into Devanagari script. "
    "Output only the Devanagari text, with no explanation."
)

parser = argparse.ArgumentParser()
parser.add_argument("image", help="Path to a Modi script image")
parser.add_argument("--ground-truth", "-g", default=None, help="Expected Devanagari text (for comparison)")
args = parser.parse_args()

print(f"Loading model from {ADAPTER_DIR} …")
bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                          bnb_4bit_compute_dtype=torch.bfloat16)
base  = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            MODEL_ID, quantization_config=bnb, device_map="auto")
model = PeftModel.from_pretrained(base, ADAPTER_DIR)
model.eval()
processor = AutoProcessor.from_pretrained(MODEL_ID, max_pixels=512 * 28 * 28)
print("Ready.\n")

image = Image.open(args.image).convert("RGB")
messages = [{"role": "user", "content": [
    {"type": "image", "image": image},
    {"type": "text",  "text": PROMPT},
]}]
text_in = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs  = processor(text=[text_in], images=[image], return_tensors="pt").to(model.device)

with torch.no_grad():
    out = model.generate(**inputs, max_new_tokens=256, do_sample=False)

result = processor.batch_decode(
    out[:, inputs["input_ids"].shape[1]:], skip_special_tokens=True
)[0].strip()

print(f"Image : {args.image}")
print(f"Output: {result}")
if args.ground_truth:
    from jiwer import cer
    c = cer(args.ground_truth, result)
    print(f"GT    : {args.ground_truth}")
    print(f"CER   : {c:.3f}")
