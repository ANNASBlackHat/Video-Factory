#!/usr/bin/env python3
"""
Reusable Piper TTS runner for Colab — PLUGGABLE (never edit this file).

Piper = a trained TTS model, NOT a clone. For Indonesian VO, use an `id_` voice
model (e.g. id_ID-medium). It reads Indonesian cleanly — no reference needed.
For English, use en_US voices. This is the recommended engine for Bahasa VO
because, unlike OmniVoice zero-shot cloning, it doesn't depend on a reference
transcript and rarely mangles the audio.

External files (upload per run — the code stays unchanged):

  1. LINES FILE  (upload to /content/tts-lines.json)
        [{"id": "scene_1", "text": "..."}, ...]   OR   {"scene_1": "...", ...}

  2. KNOBS (optional — upload /content/tts-knobs.json, else defaults):
        {
          "model_url":  "https://huggingface.co/rhasspy/piper-voices/resolve/main/id/id_ID/news_tts/medium/id_ID-news_tts-medium.onnx",
          "language":   "id",
          "out_dir":    "/content/piper-out"
        }
     model_url points at the .onnx; the .onnx.json config is derived by appending
     ".json" to the same path. Default model = id_ID-medium (Indonesian).

Usage (Colab):
  colab new -s <topic>-tts
  colab install -s <topic>-tts piper-tts
  colab upload -s <topic>-tts raws/<topic>/tts-lines.json /content/tts-lines.json
  # optional: colab upload -s <topic>-tts raws/<topic>/tts-knobs.json /content/tts-knobs.json
  colab exec -s <topic>-tts -f scripts/tts_piper.py
  for i in 1 2 3; do colab download -s <topic>-tts /content/piper-out/scene_$i.wav /tmp/vo-s$i.wav; done
  colab stop -s <topic>-tts

Piper API notes:
  - PiperVoice.load(onnx) loads model + its .onnx.json config (auto-located if
    the .json sits next to the .onnx with the same basename).
  - voice.synthesize(text) -> generator of AudioChunk
  - chunk.audio_int16_bytes = raw 16-bit PCM; wave.writeframes(bytes) directly.
"""
import os, json, wave, urllib.request

LINES_FILE = "/content/tts-lines.json"
KNOBS_FILE = "/content/tts-knobs.json"

DEFAULTS = {
    "model_url": "https://huggingface.co/rhasspy/piper-voices/resolve/main/id/id_ID/news_tts/medium/id_ID-news_tts-medium.onnx",
    "language": "id",
    "out_dir": "/content/piper-out",
}


def load_lines(path):
    """Load the VO lines. Accepts:
      - a JSON list of {id,text}
      - a JSON dict {id: text}
      - a JSON object with a top-level "lines" list  ({"id":..., "lines":[...]} )
    A stray top-level "id" key is ignored."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        if "lines" in data and isinstance(data["lines"], (list, dict)):
            data = data["lines"]
        if isinstance(data, dict):
            return [{"id": k, "text": v} for k, v in data.items()]
    if not isinstance(data, list):
        raise SystemExit(
            f"{path} must be a list of lines, a dict, or an object with a 'lines' list "
            f"— got {type(data).__name__}"
        )
    return data


def download(url, dest):
    print(f"[dl] {url} -> {dest}")
    urllib.request.urlretrieve(url, dest)


def main():
    if not os.path.exists(LINES_FILE):
        raise SystemExit(f"MISSING {LINES_FILE} — upload your VO lines JSON first (see header)")
    lines = load_lines(LINES_FILE)

    knobs = dict(DEFAULTS)
    if os.path.exists(KNOBS_FILE):
        with open(KNOBS_FILE, encoding="utf-8") as f:
            knobs.update(json.load(f))
        print(f"[knobs] loaded {KNOBS_FILE}: {knobs}")
    out_dir = knobs["out_dir"]
    model_url = knobs["model_url"]
    onnx = model_url.rsplit("/", 1)[-1]
    onnx_json = onnx + ".json"
    model_path, model_json = f"/content/{onnx}", f"/content/{onnx_json}"

    if not os.path.exists(model_path):
        download(model_url, model_path)
    if not os.path.exists(model_json):
        download(model_url + ".json", model_json)

    from piper import PiperVoice
    os.makedirs(out_dir, exist_ok=True)
    voice = PiperVoice.load(model_path, config_path=model_json)
    sr = voice.config.sample_rate
    results = {}
    for i, line in enumerate(lines):
        key, txt = line["id"], line["text"]
        print(f"[{i+1}/{len(lines)}] {key}: {txt[:60]}...")
        out = f"{out_dir}/{key}.wav"
        raw = b""
        for chunk in voice.synthesize(txt):
            raw += chunk.audio_int16_bytes
        with wave.open(out, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(sr)
            w.writeframes(raw)
        print(f"       {len(raw)/2/sr:.1f}s -> {out} ({len(raw)} bytes)")
        results[key] = out
    print(json.dumps(results))
    print("DONE_MARKER")


if __name__ == "__main__":
    main()
