"""
मोडी ते मराठी — Modi Script Transliterator
Gradio demo: drag in a Modi image, get Devanagari text out.

Run: .venv/bin/python app.py
Then open: http://localhost:7860
"""

import torch, json
from pathlib import Path
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor, BitsAndBytesConfig
from peft import PeftModel
import gradio as gr

# ── Model paths ──────────────────────────────────────────────────────────────
MODEL_ID        = "Qwen/Qwen2.5-VL-3B-Instruct"
HF_ADAPTER_REPO = "lgtk/qwen25vl-3b-modi-synth-lora"    # HuggingFace Hub fallback
LOCAL_ADAPTER   = "models/qwen25vl-3b-modi-synth-lora/final_adapter"
ADAPTER_DIR     = LOCAL_ADAPTER if Path(LOCAL_ADAPTER).exists() else HF_ADAPTER_REPO

PROMPT = (
    "This image contains handwritten text in Modi script, a historical cursive script "
    "used to write the Marathi language. "
    "Transliterate the text in this image into Devanagari script. "
    "Output only the Devanagari text, with no explanation."
)

# ── Load model once at startup (not per request) ──────────────────────────────
print("Loading model… (this takes ~15 seconds)")
bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                          bnb_4bit_compute_dtype=torch.bfloat16)
base  = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            MODEL_ID, quantization_config=bnb, device_map="auto")
model = PeftModel.from_pretrained(base, ADAPTER_DIR)
model.eval()
processor = AutoProcessor.from_pretrained(MODEL_ID, max_pixels=512 * 28 * 28)
print("Model ready.\n")

# ── Inference function ────────────────────────────────────────────────────────
def transliterate(image):
    if image is None:
        return "Please upload a Modi script image."

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

    return result if result else "(no text detected)"

# ── Load sample gallery ───────────────────────────────────────────────────────
samples_meta = json.loads(Path("samples/index.json").read_text())
example_rows = [[s["file"], s["ground_truth"]] for s in samples_meta]

# ── Build UI ──────────────────────────────────────────────────────────────────
with gr.Blocks(title="मोडी ते मराठी") as demo:

    gr.Markdown("""
# मोडी ते मराठी — Modi Script Transliterator

Upload a **handwritten Modi script** image to get its **Devanagari (Marathi) transliteration**.

**Model:** Qwen2.5-VL-3B fine-tuned with QLoRA on MoDeTrans + SynthMoDe · **Test CER: 0.328**
_(A CER of 0.0 is perfect; 0.328 means ~33% of characters need expert correction)_
""")

    with gr.Row():
        with gr.Column():
            img_input = gr.Image(type="pil", label="Modi Script Image")
            run_btn   = gr.Button("Transliterate →", variant="primary")

        with gr.Column():
            text_output = gr.Textbox(
                label="Devanagari Output",
                lines=6,
                placeholder="Devanagari text will appear here…",
            )
            gt_display = gr.Textbox(
                label="Ground Truth (sample images only)",
                lines=3,
                interactive=False,
            )

    run_btn.click(fn=transliterate, inputs=img_input, outputs=text_output)

    gr.Markdown("### Sample images — click any to load")
    gr.Examples(
        examples=example_rows,
        inputs=[img_input, gt_display],
        label=None,
        examples_per_page=10,
    )

    gr.Markdown("""
---
**Known limitations:**
- Performs best on Peshwekalin/Shivakalin formal letters (the majority of training data)
- Struggles with Modi abbreviations (`वाा`, `खुा`), scribal shorthand, and mixed Modi/English text
- A version trained on real + synthetic data is training — will improve further

**Project:** [modi-to-Marathi](https://github.com/lgtkgtv/ai4-transliteration-modi-to-marathi)
""")

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False,
                theme=gr.themes.Soft())
