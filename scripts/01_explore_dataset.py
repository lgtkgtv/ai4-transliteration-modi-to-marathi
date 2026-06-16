"""
Phase 1: Explore the MoDeTrans dataset.
Run: .venv/bin/python scripts/01_explore_dataset.py
"""

from datasets import load_dataset
import random

print("=" * 60)
print("Downloading MoDeTrans from HuggingFace...")
print("(First run downloads ~161 MB and caches it)")
print("=" * 60)

ds = load_dataset("historyHulk/MoDeTrans")

print("\n--- Dataset structure ---")
print(ds)

print("\n--- Column names ---")
for split, data in ds.items():
    print(f"  {split}: {data.column_names}")

print("\n--- Split sizes ---")
for split, data in ds.items():
    print(f"  {split}: {len(data)} examples")

print("\n--- 3 random examples ---")
train = ds["train"]
indices = random.sample(range(len(train)), 3)

for i, idx in enumerate(indices):
    example = train[idx]
    img = example["image"]
    text = example["text"]
    filename = example.get("filename", "n/a")
    print(f"\n  Example {i+1} (index {idx})")
    print(f"    filename : {filename}")
    print(f"    image    : {img.size} px, mode={img.mode}")
    print(f"    text     : {text[:120]}")
