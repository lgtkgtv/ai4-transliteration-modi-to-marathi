"""
Error analysis on evaluation_report.json.

Outputs:
  - printed summary to stdout
  - results/error_analysis_report.json

Analysis sections:
  1. CER distribution histogram
  2. Error type breakdown (substitutions vs insertions vs deletions)
  3. Top confused character pairs
  4. Known confusables from CLAUDE.md (भ/म, क/फ, ट/ठ/ढ, न/ण, vowel signs, anusvāra)
  5. Prediction length ratio (truncation vs expansion)
  6. Representative examples per quality tier
"""

import argparse, json, difflib, collections
from pathlib import Path

parser = argparse.ArgumentParser(description="Error analysis on an evaluation_report.json")
parser.add_argument("--input",  "-i", default="results/evaluation_report.json",
                    help="Path to evaluation_report.json  (default: results/evaluation_report.json)")
parser.add_argument("--output", "-o", default="results/error_analysis_report.json",
                    help="Path to write analysis JSON  (default: results/error_analysis_report.json)")
args = parser.parse_args()

REPORT_IN  = Path(args.input)
REPORT_OUT = Path(args.output)

# Known confusable character groups from domain knowledge
KNOWN_CONFUSABLES = [
    ("भ", "म"),
    ("क", "फ"),
    ("ट", "ठ"),
    ("ट", "ढ"),
    ("ठ", "ढ"),
    ("न", "ण"),
    ("े", "ि"),   # ke / ki vowel sign
    ("ं", ""),    # dropped anusvāra
]

# ── Load data ─────────────────────────────────────────────────────────────────
data     = json.loads(REPORT_IN.read_text())
examples = data["examples"]
print(f"Loaded {len(examples)} examples  (mean CER: {data['mean_cer']:.3f})\n")

# ── Per-example character alignment ──────────────────────────────────────────
total_sub = total_ins = total_del = total_ref_chars = 0
sub_pairs   = collections.Counter()   # (gt_char, pred_char) → count
ins_chars   = collections.Counter()   # pred_char inserted
del_chars   = collections.Counter()   # gt_char deleted
length_ratios = []                     # pred_len / gt_len

for ex in examples:
    gt   = ex["ground_truth"]
    pred = ex["predicted"]

    if not gt:
        continue

    length_ratios.append(len(pred) / len(gt))
    total_ref_chars += len(gt)

    matcher = difflib.SequenceMatcher(None, gt, pred, autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            pass
        elif tag == "replace":
            # Align character by character within the replace block
            for g, p in zip(gt[i1:i2], pred[j1:j2]):
                sub_pairs[(g, p)] += 1
                total_sub += 1
            # Leftover characters in the longer side become ins/del
            extra = (i2 - i1) - (j2 - j1)
            if extra > 0:   # GT longer → deletions
                for g in gt[i1 + (j2 - j1): i2]:
                    del_chars[g] += 1
                total_del += extra
            elif extra < 0: # pred longer → insertions
                for p in pred[j1 + (i2 - i1): j2]:
                    ins_chars[p] += 1
                total_ins += -extra
        elif tag == "insert":
            for p in pred[j1:j2]:
                ins_chars[p] += 1
            total_ins += (j2 - j1)
        elif tag == "delete":
            for g in gt[i1:i2]:
                del_chars[g] += 1
            total_del += (i2 - i1)

total_errors = total_sub + total_ins + total_del

# ── CER distribution ──────────────────────────────────────────────────────────
tiers = [
    ("perfect",   0.00, 0.00),
    ("excellent", 0.00, 0.10),
    ("good",      0.10, 0.20),
    ("fair",      0.20, 0.40),
    ("poor",      0.40, 0.70),
    ("very_poor", 0.70, 1.00),
    ("loops",     1.00, 9.99),
]

tier_counts = collections.OrderedDict()
for name, lo, hi in tiers:
    tier_counts[name] = [e for e in examples
                         if (lo == hi == 0.0 and e["cer"] == 0.0)
                         or (lo < hi and lo < e["cer"] <= hi)
                         or (name == "loops" and e["cer"] > 1.0)]

print("=" * 60)
print("1. CER DISTRIBUTION")
print("=" * 60)
for name, bucket in tier_counts.items():
    bar = "█" * len(bucket)
    label = f"{name:12s}"
    print(f"  {label}: {len(bucket):3d}  {bar}")

# ── Error type breakdown ───────────────────────────────────────────────────────
print()
print("=" * 60)
print("2. ERROR TYPES  (across all 204 examples)")
print("=" * 60)
print(f"  Total reference characters : {total_ref_chars:,}")
print(f"  Substitutions              : {total_sub:,}  ({100*total_sub/total_errors:.1f}%)")
print(f"  Insertions (extra chars)   : {total_ins:,}  ({100*total_ins/total_errors:.1f}%)")
print(f"  Deletions  (missed chars)  : {total_del:,}  ({100*total_del/total_errors:.1f}%)")

# ── Top confused pairs ─────────────────────────────────────────────────────────
print()
print("=" * 60)
print("3. TOP 20 CONFUSED CHARACTER PAIRS  (GT → Predicted)")
print("=" * 60)
for (gt_c, pr_c), cnt in sub_pairs.most_common(20):
    gt_disp = repr(gt_c) if gt_c.isspace() else gt_c
    pr_disp = repr(pr_c) if pr_c.isspace() else pr_c
    bar = "█" * min(cnt, 40)
    print(f"  {gt_disp} → {pr_disp}  : {cnt:4d}  {bar}")

# ── Known confusables check ────────────────────────────────────────────────────
print()
print("=" * 60)
print("4. KNOWN CONFUSABLE PAIRS  (from domain knowledge)")
print("=" * 60)
for a, b in KNOWN_CONFUSABLES:
    a_disp = a if a else "∅"
    b_disp = b if b else "∅"
    ab = sub_pairs.get((a, b), 0)
    ba = sub_pairs.get((b, a), 0)
    # For anusvāra drop: count deletions
    if b == "":
        drop = del_chars.get(a, 0)
        print(f"  {a_disp} dropped (deleted)          : {drop:4d}")
    else:
        print(f"  {a_disp}→{b_disp}: {ab:4d}   {b_disp}→{a_disp}: {ba:4d}")

# ── Length ratio ───────────────────────────────────────────────────────────────
import statistics
mean_ratio  = statistics.mean(length_ratios)
short_count = sum(1 for r in length_ratios if r < 0.8)
long_count  = sum(1 for r in length_ratios if r > 1.2)

print()
print("=" * 60)
print("5. PREDICTION LENGTH  (predicted / ground-truth characters)")
print("=" * 60)
print(f"  Mean ratio       : {mean_ratio:.3f}  (1.0 = perfect length)")
print(f"  Too short (<0.8) : {short_count} examples")
print(f"  Too long  (>1.2) : {long_count} examples")

# ── Representative examples per tier ──────────────────────────────────────────
print()
print("=" * 60)
print("6. REPRESENTATIVE EXAMPLES PER TIER")
print("=" * 60)

TIER_SAMPLE = 2   # show N examples per tier

for name, bucket in tier_counts.items():
    if not bucket:
        continue
    # Pick examples closest to the median CER of the bucket
    bucket_sorted = sorted(bucket, key=lambda e: e["cer"])
    mid = len(bucket_sorted) // 2
    picks = bucket_sorted[max(0, mid - 1): mid + 1][:TIER_SAMPLE]
    print(f"\n  [{name.upper()}]")
    for ex in picks:
        print(f"    file: {ex['filename']}  CER: {ex['cer']:.3f}")
        print(f"    GT  : {ex['ground_truth'][:80]}")
        print(f"    Pred: {ex['predicted'][:80]}")

# ── Save report ────────────────────────────────────────────────────────────────
report = {
    "source_report": str(REPORT_IN),
    "n_examples": len(examples),
    "mean_cer": data["mean_cer"],
    "cer_distribution": {name: len(b) for name, b in tier_counts.items()},
    "error_types": {
        "total_ref_chars": total_ref_chars,
        "substitutions": total_sub,
        "insertions": total_ins,
        "deletions": total_del,
        "pct_substitutions": round(100 * total_sub / total_errors, 1),
        "pct_insertions":    round(100 * total_ins / total_errors, 1),
        "pct_deletions":     round(100 * total_del / total_errors, 1),
    },
    "top_confused_pairs": [
        {"gt": g, "pred": p, "count": c}
        for (g, p), c in sub_pairs.most_common(50)
    ],
    "known_confusables": {
        f"{a or '∅'}_{b or '∅'}": {"gt_to_pred": sub_pairs.get((a, b), 0),
                                    "pred_to_gt": sub_pairs.get((b, a), 0)}
        for a, b in KNOWN_CONFUSABLES if b
    },
    "anusvara_drops": del_chars.get("ं", 0),
    "length_ratio": {
        "mean": round(mean_ratio, 3),
        "too_short_lt_0_8": short_count,
        "too_long_gt_1_2":  long_count,
    },
}

REPORT_OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2))
print(f"\nReport saved to {REPORT_OUT}")
