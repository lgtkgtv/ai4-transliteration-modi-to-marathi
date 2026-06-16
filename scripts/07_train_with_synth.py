"""
Phase 2b: QLoRA fine-tuning on MoDeTrans (real) + SynthMoDe (synthetic).

Training set: 1,635 real + 4,086 synthetic = 5,721 examples
Epochs: 2  (more data → fewer passes needed)
Expected time: ~17 hours

Run: .venv/bin/python scripts/07_train_with_synth.py
"""

import torch
from pathlib import Path
from torch.utils.data import Dataset as TorchDataset, ConcatDataset
from datasets import load_from_disk, load_dataset
from transformers import (
    Qwen2_5_VLForConditionalGeneration,
    AutoProcessor,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# ── Settings ──────────────────────────────────────────────────────────────────
MODEL_ID   = "Qwen/Qwen2.5-VL-3B-Instruct"
OUTPUT_DIR = "models/qwen25vl-3b-modi-synth-lora"
N_EPOCHS   = 2

PROMPT = (
    "This image contains handwritten text in Modi script, a historical cursive script "
    "used to write the Marathi language. "
    "Transliterate the text in this image into Devanagari script. "
    "Output only the Devanagari text, with no explanation."
)

# ── Load model in 4-bit ───────────────────────────────────────────────────────
print("Loading model in 4-bit quantization...")
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)
model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    MODEL_ID, quantization_config=bnb_config, device_map="auto"
)
model = prepare_model_for_kbit_training(model)

# ── LoRA (same config as before) ──────────────────────────────────────────────
lora_config = LoraConfig(
    r=32, lora_alpha=64,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05, bias="none", task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

processor = AutoProcessor.from_pretrained(MODEL_ID, max_pixels=512 * 28 * 28)

# ── Shared preprocessing logic ────────────────────────────────────────────────
def make_item(image, answer):
    """Tokenize one (image, Devanagari text) pair with label masking."""
    messages = [
        {"role": "user", "content": [
            {"type": "image", "image": image},
            {"type": "text",  "text": PROMPT},
        ]},
        {"role": "assistant", "content": [
            {"type": "text",  "text": answer},
        ]},
    ]
    full_text   = processor.apply_chat_template(messages,       tokenize=False, add_generation_prompt=False)
    prompt_text = processor.apply_chat_template(messages[:1],   tokenize=False, add_generation_prompt=True)

    inputs        = processor(text=[full_text],   images=[image], return_tensors="pt")
    prompt_inputs = processor(text=[prompt_text], images=[image], return_tensors="pt")

    input_ids = inputs["input_ids"][0]
    labels    = input_ids.clone()
    labels[:prompt_inputs["input_ids"].shape[1]] = -100

    return {
        "input_ids":      input_ids,
        "attention_mask": inputs["attention_mask"][0],
        "pixel_values":   inputs["pixel_values"],
        "image_grid_thw": inputs["image_grid_thw"],
        "labels":         labels,
    }

# ── Dataset: real MoDeTrans ───────────────────────────────────────────────────
class RealModiDataset(TorchDataset):
    def __init__(self, hf_dataset):
        self.data = hf_dataset

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        ex = self.data[idx]
        return make_item(ex["image"], ex["text"])

# ── Dataset: synthetic SynthMoDe (image1 + image2 both used) ─────────────────
class SynthMoDeDataset(TorchDataset):
    def __init__(self, hf_dataset):
        # Flatten: each row becomes 2 training examples
        self.items = []
        for row in hf_dataset:
            self.items.append((row["image1"], row["text"]))
            self.items.append((row["image2"], row["text"]))
        print(f"  SynthMoDe: {len(hf_dataset)} rows × 2 images = {len(self.items)} examples")

    def __len__(self):
        return len(self.items)

    def __getitem__(self, idx):
        image, answer = self.items[idx]
        return make_item(image, answer)

# ── Collator (batch_size=1) ───────────────────────────────────────────────────
def collate_fn(batch):
    b = batch[0]
    return {
        "input_ids":      b["input_ids"].unsqueeze(0),
        "attention_mask": b["attention_mask"].unsqueeze(0),
        "pixel_values":   b["pixel_values"],
        "image_grid_thw": b["image_grid_thw"],
        "labels":         b["labels"].unsqueeze(0),
    }

# ── Build combined dataset ────────────────────────────────────────────────────
print("\nLoading datasets...")
real_hf  = load_from_disk("data/modetrans_splits/train")
synth_hf = load_dataset("historyHulk/SynthMoDe")["train"]

real_ds  = RealModiDataset(real_hf)
synth_ds = SynthMoDeDataset(synth_hf)
combined = ConcatDataset([real_ds, synth_ds])

print(f"\n  Real (MoDeTrans train): {len(real_ds):,}")
print(f"  Synthetic (SynthMoDe):  {len(synth_ds):,}")
print(f"  Combined total:         {len(combined):,}")

# ── Training ──────────────────────────────────────────────────────────────────
args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    num_train_epochs=N_EPOCHS,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,
    learning_rate=2e-4,
    warmup_ratio=0.03,
    lr_scheduler_type="cosine",
    bf16=True,
    gradient_checkpointing=True,
    logging_steps=20,
    save_steps=200,
    save_total_limit=2,
    dataloader_num_workers=0,
    remove_unused_columns=False,
    report_to="none",
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=combined,
    data_collator=collate_fn,
)

print(f"\nStarting FULL TRAINING — real + synthetic, {N_EPOCHS} epochs...\n")
trainer.train()

# Save adapter
out = Path(OUTPUT_DIR) / "final_adapter"
out.mkdir(parents=True, exist_ok=True)
model.save_pretrained(str(out))
processor.save_pretrained(str(out))
print(f"\nAdapter saved to {out}")
