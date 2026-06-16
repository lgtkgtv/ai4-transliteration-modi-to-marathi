"""
Phase 1: Create reproducible train/val/test splits from MoDeTrans.
Run: .venv/bin/python scripts/02_prepare_splits.py

Saves splits to data/modetrans_splits/ so every subsequent script
loads identical train/val/test sets.
"""

from datasets import load_dataset
from pathlib import Path

SEED = 42
VAL_RATIO  = 0.10
TEST_RATIO = 0.10
OUT_DIR = Path("data/modetrans_splits")

print("Loading MoDeTrans from cache...")
ds = load_dataset("historyHulk/MoDeTrans")
full = ds["train"]   # the only split that exists
print(f"Total examples: {len(full)}")

# Step 1: carve out test set first, then split remainder into train/val
# Using train_test_split twice is the standard pattern
test_size  = int(len(full) * TEST_RATIO)
val_size   = int(len(full) * VAL_RATIO)

split1 = full.train_test_split(test_size=test_size, seed=SEED)
train_val = split1["train"]
test      = split1["test"]

split2 = train_val.train_test_split(test_size=val_size, seed=SEED)
train = split2["train"]
val   = split2["test"]

print(f"\nSplit sizes:")
print(f"  train : {len(train)}")
print(f"  val   : {len(val)}")
print(f"  test  : {len(test)}  ← locked, never used for training")
print(f"  total : {len(train) + len(val) + len(test)}")

# Save to disk
OUT_DIR.mkdir(parents=True, exist_ok=True)
train.save_to_disk(str(OUT_DIR / "train"))
val.save_to_disk(str(OUT_DIR / "val"))
test.save_to_disk(str(OUT_DIR / "test"))

print(f"\nSaved to {OUT_DIR}/")
print("  train/  val/  test/")
