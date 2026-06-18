# Inference Guide

**Project:** मोडी ते मराठी — Modi-to-Marathi Transliteration
**Hardware:** All development and testing was done on a desktop with an **NVIDIA RTX 5060 (8.5 GB VRAM)** running WSL2 on Windows.

---

## Two ways to run transliteration

There are two entry points for running the model. They use exactly the same inference code under the hood — the difference is only in how they are invoked and how they handle model loading.

```
                 ┌──────────────────────────────────────────┐
  Modi image ──► │   Inference core                         │──► Devanagari text
                 │   (load model → build prompt → generate) │
                 └──────────────────────────────────────────┘
                          ▲                    ▲
                          │                    │
                   scripts/09_infer.py       app.py
                   (CLI — exits after         (Gradio — stays running,
                    one image)                 serves a web UI)
```

---

## CLI — `scripts/09_infer.py`

Loads the model, runs one image, prints the result, and **exits**.

```bash
# Basic usage
.venv/bin/python scripts/09_infer.py samples/1672.jpg

# With ground truth for CER comparison
.venv/bin/python scripts/09_infer.py samples/1444.jpg \
    --ground-truth "सकलगुण अलंकर्ण…"
```

**Output:**
```
Loading model from models/qwen25vl-3b-modi-synth-lora/final_adapter …
Ready.

Image : samples/1672.jpg
Output: अखंडित लक्ष्मी आलंकृत
CER   : 0.000
```

**Model load time:** ~30 seconds on the RTX 5060. Each invocation pays this cost from scratch because the process exits after finishing.

**When to use the CLI:**
- Spot-checking a single image
- Scripting batch transliteration in a shell loop
- Debugging or testing — exit means no cleanup needed, no hung process
- When Gradio is not needed (no browser, headless server)

---

## Gradio web app — `app.py`

Loads the model **once**, then starts an HTTP server. The model stays in GPU memory and each new request goes straight to inference — no reload.

```bash
.venv/bin/python app.py
# Open http://localhost:7860
```

**When to use the Gradio app:**
- Transliterating many images in a session — you pay the 30-second load once
- Sharing a demo with others (Gradio's Share button creates a public tunnel)
- Running experiments where you want a visual side-by-side of image vs. output

---

## Why the CLI is faster per session start, but the Gradio app wins for volume

| | CLI (`09_infer.py`) | Gradio (`app.py`) |
|---|---|---|
| Model load | Every invocation (~30 sec) | Once at startup (~30 sec) |
| Per-image time | ~3–5 sec (after load) | ~3–5 sec (after load) |
| 10 images | ~330–50 sec | ~30 + 30–50 sec |
| State after run | Process exits cleanly | Server keeps running |
| GPU memory held | Released on exit | Held until you Ctrl-C |

The break-even is roughly **2 images** — if you're transliterating more than one image, start `app.py` and keep it running.

---

## WSL2: GPU freshness check (why `app.py` can hang)

On WSL2, after a previous GPU process (another Python script, a game, etc.) releases the GPU device, the next process to call `torch.cuda` can hang indefinitely at CUDA initialisation. The weights load into CPU RAM fine, but the GPU is never acquired. `nvidia-smi` shows no compute processes despite the Python process being alive — a silent hang.

`app.py` includes a pre-flight check that runs before model loading:

1. Runs `nvidia-smi --query-compute-apps` to list any running CUDA processes
2. If any are found, prints the PIDs and exits with a clear message
3. Checks that at least 5 GB of GPU memory is free (the model needs ~3–4 GB in 4-bit mode)

If you see the error:
```
ERROR: GPU is occupied — app.py will hang if you continue.
Running CUDA processes:
  12345, 1234 MiB, python3

Run these kill commands, then retry:
  kill 12345
```

Run the kill command, wait a few seconds for WSL2 to release the device, then re-run `app.py`.

**The CLI script (`09_infer.py`) has no equivalent check** — it exits cleanly after one run, so there is no persistent process to conflict with the next invocation.

---

## Adapter loading order

Both entry points use the same logic:

1. Look for a local adapter at `models/qwen25vl-3b-modi-synth-lora/final_adapter/`
2. If not found locally, download from HuggingFace: `lgtk/qwen25vl-3b-modi-synth-lora`

The local path is faster (no download). The HuggingFace fallback means the scripts work on any machine without pre-downloading.

---

## Reproducing a run

```bash
# One-off image (CLI)
.venv/bin/python scripts/09_infer.py <image_path>

# Evaluate on all 204 held-out test examples
.venv/bin/python scripts/06_evaluate.py

# Run error analysis on evaluation output
.venv/bin/python scripts/08_error_analysis.py \
    --input results/evaluation_report.json \
    --output results/error_analysis_report.json
```
