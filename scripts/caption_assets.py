#!/usr/bin/env python3
"""
Caption assets in raws/investigasi-karhutla/assets-collected using HuggingFace models.
Supports:
  - blip-base  : Salesforce/blip-image-captioning-base  (light, CPU-friendly, 223M)
  - blip-large : Salesforce/blip-image-captioning-large (better, ~385M)
  - florence2  : microsoft/Florence-2-base  (dense caption, ~0.9B, needs ~2GB RAM)
  - git-base   : microsoft/git-base-coco    (alternative)
  - blip2      : Salesforce/blip2-opt-2.7b  (needs GPU, heavy)

Usage (local):
  python scripts/caption_assets.py --model blip-base --input raws/investigasi-karhutla/assets-collected --out raws/investigasi-karhutla/captions.json

Usage (colab):
  colab exec -s karhutla-cpu -f scripts/caption_assets.py -- --model florence2

Output: JSON + MD table next to --out path.
"""
import argparse
import json
import os
import pathlib
import zipfile
from PIL import Image

def find_images(base: str):
    exts = {".jpg",".jpeg",".png",".gif",".webp",".bmp"}
    files = []
    for root, _, fs in os.walk(base):
        for f in fs:
            if f.startswith("."):
                continue
            if pathlib.Path(f).suffix.lower() in exts:
                files.append(os.path.join(root, f))
    return sorted(files)

def caption_blip(files, base, model_name, out_json, out_md, device="cpu"):
    from transformers import BlipProcessor, BlipForConditionalGeneration
    import torch
    print(f"[blip] loading {model_name} on {device}")
    processor = BlipProcessor.from_pretrained(model_name)
    model = BlipForConditionalGeneration.from_pretrained(model_name)
    model.eval().to(device)
    results = []
    for i, fp in enumerate(files, 1):
        try:
            image = Image.open(fp).convert("RGB")
            inputs = processor(image, return_tensors="pt")
            inputs = {k: v.to(device) for k, v in inputs.items()}
            with torch.no_grad():
                out = model.generate(**inputs, max_length=40, num_beams=5)
            caption = processor.decode(out[0], skip_special_tokens=True)
            rel = os.path.relpath(fp, base)
            print(f"[{i}/{len(files)}] {rel} -> {caption}")
            results.append({"file": rel, "caption": caption})
        except Exception as e:
            rel = os.path.relpath(fp, base)
            print(f"[ERR] {rel}: {e}")
            results.append({"file": rel, "caption": f"ERROR: {e}", "error": str(e)})
    save_results(results, model_name, out_json, out_md)
    return results

def caption_florence2(files, base, out_json, out_md, device="cpu"):
    # Florence-2 uses AutoProcessor + AutoModelForCausalLM
    from transformers import AutoProcessor, AutoModelForCausalLM
    import torch
    model_name = "microsoft/Florence-2-base"
    print(f"[florence2] loading {model_name} on {device}")
    # trust_remote_code required for Florence-2
    processor = AutoProcessor.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)
    model.eval().to(device)
    # Florence-2 prefers bfloat16 on GPU, float32 on CPU
    results = []
    for i, fp in enumerate(files, 1):
        try:
            image = Image.open(fp).convert("RGB")
            # Task prompt: <CAPTION> for short, <DETAILED_CAPTION> or <MORE_DETAILED_CAPTION>
            prompt = "<CAPTION>"
            inputs = processor(text=prompt, images=image, return_tensors="pt")
            inputs = {k: v.to(device) if hasattr(v, 'to') else v for k, v in inputs.items()}
            # move pixel_values etc.
            for k in ["input_ids", "pixel_values"]:
                if k in inputs and hasattr(inputs[k], "to"):
                    inputs[k] = inputs[k].to(device)
            with torch.no_grad():
                generated_ids = model.generate(
                    input_ids=inputs["input_ids"],
                    pixel_values=inputs["pixel_values"],
                    max_new_tokens=64,
                    num_beams=3,
                    do_sample=False,
                )
            generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
            # Florence output includes prompt; strip
            caption = processor.post_process_generation(
                generated_text, task=prompt, image_size=(image.width, image.height)
            )
            # caption is dict like {"<CAPTION>": "..."}
            text = caption.get(prompt, generated_text)
            # fallback if post_process returns string
            if isinstance(text, dict):
                text = list(text.values())[0] if text else generated_text
            rel = os.path.relpath(fp, base)
            print(f"[{i}/{len(files)}] {rel} -> {text}")
            results.append({"file": rel, "caption": text, "raw": generated_text[:500]})
        except Exception as e:
            rel = os.path.relpath(fp, base)
            print(f"[ERR] {rel}: {e}")
            import traceback; traceback.print_exc()
            results.append({"file": rel, "caption": f"ERROR: {e}", "error": str(e)})
    save_results(results, model_name, out_json, out_md)
    return results

def caption_git(files, base, model_name, out_json, out_md, device="cpu"):
    from transformers import AutoProcessor, AutoModelForCausalLM
    import torch
    print(f"[git] loading {model_name} on {device}")
    processor = AutoProcessor.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval().to(device)
    results = []
    for i, fp in enumerate(files, 1):
        try:
            image = Image.open(fp).convert("RGB")
            inputs = processor(images=image, return_tensors="pt")
            inputs = {k: v.to(device) for k, v in inputs.items()}
            with torch.no_grad():
                out = model.generate(pixel_values=inputs["pixel_values"], max_length=40, num_beams=3)
            caption = processor.batch_decode(out, skip_special_tokens=True)[0].strip()
            rel = os.path.relpath(fp, base)
            print(f"[{i}/{len(files)}] {rel} -> {caption}")
            results.append({"file": rel, "caption": caption})
        except Exception as e:
            rel = os.path.relpath(fp, base)
            print(f"[ERR] {rel}: {e}")
            results.append({"file": rel, "caption": f"ERROR: {e}", "error": str(e)})
    save_results(results, model_name, out_json, out_md)
    return results

def save_results(results, model_name, out_json, out_md):
    os.makedirs(os.path.dirname(out_json) or ".", exist_ok=True)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"[save] {out_json} ({len(results)} entries)")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(f"# Captions — {model_name}\n\n")
        f.write(f"Model: `{model_name}` | Images: {len(results)}\n\n")
        f.write("| # | File | Caption |\n|---|---|---|\n")
        for idx, r in enumerate(results, 1):
            cap = r["caption"].replace("|", "\\|").replace("\n", " ")
            f.write(f"| {idx} | `{r['file']}` | {cap} |\n")
    print(f"[save] {out_md}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="blip-base", choices=["blip-base","blip-large","florence2","git-base","blip2"], help="model key")
    parser.add_argument("--input", default="raws/investigasi-karhutla/assets-collected", help="image folder")
    parser.add_argument("--out", default=None, help="output json path")
    parser.add_argument("--zip", default=None, help="optional zip to extract (colab: /content/karhutla-assets.zip)")
    parser.add_argument("--device", default="cpu", help="cpu or cuda")
    args = parser.parse_args()

    # handle zip extract (colab convenience)
    if args.zip and os.path.exists(args.zip):
        print(f"[zip] extracting {args.zip}")
        with zipfile.ZipFile(args.zip, 'r') as z:
            z.extractall("/content" if os.path.exists("/content") else ".")
        # if input path doesn't exist, try to locate
        if not os.path.exists(args.input):
            import glob
            cands = glob.glob(f"/content/**/assets-collected", recursive=True)
            if cands:
                args.input = cands[0]
                print(f"[zip] resolved input to {args.input}")

    base = args.input
    # also handle colab absolute prefix
    if not os.path.exists(base) and os.path.exists("/content/" + base.lstrip("/")):
        base = "/content/" + base.lstrip("/")

    print(f"[config] model={args.model} input={base} device={args.device}")
    files = find_images(base)
    print(f"[scan] found {len(files)} images")
    if not files:
        print("[scan] no images found — check --input path")
        return

    model_map = {
        "blip-base": "Salesforce/blip-image-captioning-base",
        "blip-large": "Salesforce/blip-image-captioning-large",
        "git-base": "microsoft/git-base-coco",
        "blip2": "Salesforce/blip2-opt-2.7b",
    }

    out_json = args.out or os.path.join(os.path.dirname(base) or ".", f"captions-{args.model}.json")
    out_md = out_json.replace(".json", ".md")

    # ensure out paths work for colab (/content/captions-*.json fallback)
    if base.startswith("/content") and not args.out:
        out_json = f"/content/captions-{args.model}.json"
        out_md = f"/content/captions-{args.model}.md"

    if args.model in ("blip-base", "blip-large", "blip2"):
        caption_blip(files, base, model_map[args.model], out_json, out_md, device=args.device)
    elif args.model == "florence2":
        caption_florence2(files, base, out_json, out_md, device=args.device)
    elif args.model == "git-base":
        caption_git(files, base, model_map[args.model], out_json, out_md, device=args.device)

if __name__ == "__main__":
    main()
