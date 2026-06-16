"""
Phase 2: QLoRA fine-tuning of Qwen2.5-VL-3B on MoDeTrans.

SMOKE_TEST = True  → 50 steps (~5 min) to verify the setup works
SMOKE_TEST = False → full training (3 epochs, ~3-4 hours)

Run: .venv/bin/python scripts/05_train_qlora.py
"""

import torch
from pathlib import Path
from torch.utils.data import Dataset as TorchDataset
from datasets import load_from_disk
from transformers import (
    Qwen2_5_VLForConditionalGeneration,
    AutoProcessor,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# ── Settings ──────────────────────────────────────────────────────────────────
SMOKE_TEST = False   # flip to True for a 50-step smoke test
MODEL_ID   = "Qwen/Qwen2.5-VL-3B-Instruct"
OUTPUT_DIR = "models/qwen25vl-3b-modi-lora"
N_EPOCHS   = 3
MAX_STEPS  = 50 if SMOKE_TEST else -1   # -1 = run full N_EPOCHS

PROMPT = (
    "This image contains handwritten text in Modi script, a historical cursive script "
    "used to write the Marathi language. "
    "Transliterate the text in this image into Devanagari script. "
    "Output only the Devanagari text, with no explanation."
)

# ── 1. Load base model in 4-bit ───────────────────────────────────────────────
print("Loading model in 4-bit quantization...")
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)
model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    MODEL_ID,
    quantization_config=bnb_config,
    device_map="auto",
)

# Required before LoRA: re-enables gradient flow through the frozen 4-bit weights
model = prepare_model_for_kbit_training(model)

# ── 2. Attach LoRA adapters ───────────────────────────────────────────────────
lora_config = LoraConfig(
    r=32,                    # adapter rank: higher = more capacity, more VRAM
    lora_alpha=64,           # scaling factor, conventionally 2× rank
    target_modules=[         # which weight matrices get adapters
        "q_proj", "k_proj", "v_proj", "o_proj",    # attention
        "gate_proj", "up_proj", "down_proj",         # feedforward
    ],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()   # shows how few params actually train

# ── 3. Processor ──────────────────────────────────────────────────────────────
# max_pixels limits image resolution → fewer visual tokens → less VRAM per step
processor = AutoProcessor.from_pretrained(MODEL_ID, max_pixels=512 * 28 * 28)

# ── 4. Dataset ────────────────────────────────────────────────────────────────
class ModiDataset(TorchDataset):
    def __init__(self, hf_dataset):
        self.data = hf_dataset

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        ex     = self.data[idx]
        image  = ex["image"]
        answer = ex["text"]

        # Format as a two-turn conversation: user (image + prompt) → assistant (Devanagari)
        messages = [
            {"role": "user", "content": [
                {"type": "image", "image": image},
                {"type": "text",  "text": PROMPT},
            ]},
            {"role": "assistant", "content": [
                {"type": "text",  "text": answer},
            ]},
        ]

        # Full conversation (prompt + answer) for tokenization
        full_text = processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=False
        )
        # Prompt-only text — needed to know where to start the label
        prompt_text = processor.apply_chat_template(
            messages[:1], tokenize=False, add_generation_prompt=True
        )

        # Tokenize full conversation (images processed here too)
        inputs = processor(text=[full_text], images=[image], return_tensors="pt")

        # Tokenize prompt only (same image, to get prompt token length)
        prompt_inputs = processor(text=[prompt_text], images=[image], return_tensors="pt")

        input_ids = inputs["input_ids"][0]
        labels    = input_ids.clone()

        # Mask all prompt tokens: -100 tells PyTorch "don't compute loss here"
        prompt_len = prompt_inputs["input_ids"].shape[1]
        labels[:prompt_len] = -100

        return {
            "input_ids":      input_ids,
            "attention_mask": inputs["attention_mask"][0],
            "pixel_values":   inputs["pixel_values"],
            "image_grid_thw": inputs["image_grid_thw"],
            "labels":         labels,
        }


def collate_fn(batch):
    # We always use batch_size=1; this just adds the batch dimension
    b = batch[0]
    return {
        "input_ids":      b["input_ids"].unsqueeze(0),
        "attention_mask": b["attention_mask"].unsqueeze(0),
        "pixel_values":   b["pixel_values"],
        "image_grid_thw": b["image_grid_thw"],
        "labels":         b["labels"].unsqueeze(0),
    }


# ── 5. Training ───────────────────────────────────────────────────────────────
train_hf = load_from_disk("data/modetrans_splits/train")
train_ds  = ModiDataset(train_hf)

args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    num_train_epochs=N_EPOCHS,
    max_steps=MAX_STEPS,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,    # effective batch = 8 examples
    learning_rate=2e-4,
    warmup_ratio=0.03,
    lr_scheduler_type="cosine",
    bf16=True,                         # bfloat16 for activations (faster, less VRAM)
    gradient_checkpointing=True,       # trade speed for VRAM: recompute activations
    logging_steps=10,
    save_steps=100,
    save_total_limit=2,
    dataloader_num_workers=0,
    remove_unused_columns=False,
    report_to="none",
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_ds,
    data_collator=collate_fn,
)

mode = "SMOKE TEST (50 steps)" if SMOKE_TEST else f"FULL TRAINING ({N_EPOCHS} epochs)"
print(f"\nStarting {mode}...\n")
trainer.train()

# Save only the LoRA adapter weights (~50 MB), not the full 3B model
out = Path(OUTPUT_DIR) / ("smoke_adapter" if SMOKE_TEST else "final_adapter")
out.mkdir(parents=True, exist_ok=True)
model.save_pretrained(str(out))
processor.save_pretrained(str(out))
print(f"\nAdapter saved to {out}")
