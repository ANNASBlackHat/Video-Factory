#!/usr/bin/env python3
"""
Reusable OmniVoice TTS runner for Colab (Bahasa + zero-shot voice cloning).

PLUGGABLE — the script never needs editing. All topic-specific config lives in
EXTERNAL files, so you re-run the same code over and over:

  1. LINES FILE  (upload to /content/tts-lines.json)
        [{"id": "scene_1", "text": "..."}, {"id": "scene_2", "text": "..."}, ...]
     Keys "id" (output file name, no .wav) and "text" (the VO line).
     Numbers: write them in NATURAL form ("2026", "65 miliar") — fully-spelled-out
     Indonesian number words ("dua ribu dua enam") mangle the audio.

  2. VOICE REFERENCE (upload the .m4a to /content/ref-voice.m4a)
     Any of voices/*.m4a. The transcript is auto-paired by file name:
       voices/female-medium-pace.m4a  <->  voices/female-medium-pace.srt
     Upload the matching .srt to /content/ref-voice.srt. If the .srt is missing,
     OmniVoice auto-ASR's the reference (slower, less reliable).

  3. KNOBS (optional — upload /content/tts-knobs.json, else defaults):
        {"speed": 0.9, "num_step": 32, "silence_s": 0.4, "out_dir": "/content/tts-out"}
     speed: 0.7 slow/documentary, 1.0 neutral, 1.3 fast.  num_step: 32 quality / 16 fast.

Usage (Colab):
  colab new -s <topic>-tts --gpu T4
  colab install -s <topic>-tts omnivoice
  colab upload -s <topic>-tts voices/female-medium-pace.m4a /content/ref-voice.m4a
  colab upload -s <topic>-tts voices/female-medium-pace.srt /content/ref-voice.srt
  colab upload -s <topic>-tts raws/<topic>/tts-lines.json /content/tts-lines.json
  # optional: colab upload -s <topic>-tts raws/<topic>/tts-knobs.json /content/tts-knobs.json
  colab exec -s <topic>-tts -f scripts/tts_omnivoice.py
  for i in 1 2 3 ...; do colab download -s <topic>-tts /content/tts-out/scene_$i.wav /tmp/vo-s$i.wav; done
  colab stop -s <topic>-tts

Output (out_dir, default /content/tts-out):
  - <id>.wav per line (24 kHz mono float32)
  - final_full_voiceover.wav — all lines concatenated with silence_s gaps
"""
import os, json
import numpy as np
import soundfile as sf

LINES_FILE = "/content/tts-lines.json"      # required
REF_AUDIO  = "/content/ref-voice.m4a"        # required
REF_SRT    = "/content/ref-voice.srt"        # optional (auto-paired transcript)
KNOBS_FILE = "/content/tts-knobs.json"       # optional

DEFAULTS = {"speed": 0.9, "num_step": 32, "silence_s": 0.4, "out_dir": "/content/tts-out"}
SAMPLE_RATE = 24000


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


def load_ref_text(srt_path):
    """Flatten an SRT (or plain-text) transcript into one string.
    Falls back to None (= OmniVoice auto-ASR) if the file is absent."""
    if not os.path.exists(srt_path):
        print(f"[ref-text] {srt_path} not found -> OmniVoice will auto-ASR the reference")
        return None
    with open(srt_path, encoding="utf-8") as f:
        raw = f.read().strip()
    if raw.lower().endswith(".srt") or "-->" in raw:
        # strip SRT index numbers + timestamps, keep subtitle text lines
        parts = []
        for block in raw.split("\n\n"):
            for ln in block.splitlines():
                ln = ln.strip()
                if not ln or ln.isdigit() or "-->" in ln:
                    continue
                parts.append(ln)
        raw = " ".join(parts)
    return raw or None


def main():
    if not os.path.exists(LINES_FILE):
        raise SystemExit(f"MISSING {LINES_FILE} — upload your VO lines JSON first (see header)")
    lines = load_lines(LINES_FILE)

    knobs = dict(DEFAULTS)
    if os.path.exists(KNOBS_FILE):
        with open(KNOBS_FILE, encoding="utf-8") as f:
            knobs.update(json.load(f))
        print(f"[knobs] loaded {KNOBS_FILE}: {knobs}")
    speed, num_step, silence_s, out_dir = knobs["speed"], knobs["num_step"], knobs["silence_s"], knobs["out_dir"]

    ref_text = load_ref_text(REF_SRT)

    from omnivoice import OmniVoice
    import torch
    print(f"[omnivoice] loading k2-fsa/OmniVoice -> cuda:0 fp16 | speed={speed} num_step={num_step} lines={len(lines)}")
    model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="cuda:0", dtype=torch.float16)

    os.makedirs(out_dir, exist_ok=True)
    gap = np.zeros(int(SAMPLE_RATE * silence_s), dtype=np.float32)
    segs, results = [], {}
    for i, line in enumerate(lines):
        key, txt = line["id"], line["text"]
        print(f"[{i+1}/{len(lines)}] {key}: {txt[:60]}...")
        out = model.generate(
            text=txt, ref_audio=REF_AUDIO, ref_text=ref_text,
            num_step=num_step, speed=speed,
        )
        wav = np.array(out[0], dtype=np.float32).squeeze()
        p = f"{out_dir}/{key}.wav"
        sf.write(p, wav, SAMPLE_RATE)
        print(f"       {len(wav)/SAMPLE_RATE:.1f}s -> {p}")
        results[key] = p
        segs.append(wav)
        if i < len(lines) - 1:
            segs.append(gap)

    final = np.concatenate(segs)
    fp = f"{out_dir}/final_full_voiceover.wav"
    sf.write(fp, final, SAMPLE_RATE)
    print(f"[done] {len(lines)} lines, total {len(final)/SAMPLE_RATE:.1f}s -> {fp}")
    print(json.dumps(results))
    print("DONE_MARKER")


if __name__ == "__main__":
    main()
