# Model Card

<!-- TODO: fill in when a trained model is published -->

| Field | Value |
|---|---|
| **Base model** | Qwen2.5-VL-3B-Instruct |
| **Fine-tuning method** | QLoRA (rank 32, 4-bit NF4) |
| **Task** | Image → Devanagari text (Modi script transliteration) |
| **Input** | JPEG/PNG image of handwritten Modi text |
| **Output** | Devanagari text string |
| **Primary metric** | CER (Character Error Rate) |
| **Secondary metric** | BLEU |
| **Limitations** | TODO |
| **Licence** | TODO |

## Training data

See [`docs/data.md`](data.md).

## Evaluation

| Model | CER (test set, 204 examples) |
|---|---|
| Zero-shot baseline | 0.930 |
| Fine-tuned (real data only) | 0.332 |
| Fine-tuned (real + synthetic) | TODO |

Lower is better. CER = edit distance / reference length; can exceed 1.0 on catastrophic failures.

## Known error patterns

- Vowel length confusion: ी ↔ ि, ू ↔ ु (accounts for the largest share of substitutions)
- Anusvāra (ं) frequently dropped (242 instances in test set)
- अ / आ confusion

## How to use

See [`docs/quickstart.md`](quickstart.md).
