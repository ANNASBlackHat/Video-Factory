# Caption & TTS Scripts

Reusable Colab scripts for captioning assets and generating TTS voiceovers.

## Quick start (Colab CLI, oauth2)

```bash
# 1. Create CPU session (T4 quota often fails -> use CPU)
colab new -s karhutla-cpu

# 2. Zip & upload assets once
zip -r /tmp/karhutla-assets.zip raws/investigasi-karhutla/assets-collected -x "*.DS_Store"
colab upload -s karhutla-cpu /tmp/karhutla-assets.zip /content/karhutla-assets.zip

# 3. Run any model (reads local script, executes on remote VM)
colab exec -s karhutla-cpu -f /tmp/run_blip_large_fast.py
colab exec -s karhutla-cpu -f /tmp/run_git_base.py
colab exec -s karhutla-cpu -f scripts/caption_assets.py  # default blip-base (needs args workaround, use /tmp wrappers)
```

## Scripts

- `scripts/caption_assets.py` — main modular script: `--model {blip-base,blip-large,git-base,florence2,blip2}` `--input` `--out` `--zip` `--device`
  - Note: `colab exec -f` cannot pass args directly; use wrapper scripts in `/tmp/run_*.py` (see examples below) or edit defaults.
- `scripts/tts_piper.py` — **reusable Piper TTS runner** (trained-model TTS, no reference). Pluggable: upload `tts-lines.json` + optional `tts-knobs.json`, run, done. **Indonesian `id_ID` voice reads Bahasa cleanly; bundled `en_US` voices are English-only.**
- `scripts/tts_omnivoice.py` — **reusable OmniVoice runner (k2-fsa/OmniVoice) — DEFAULT for Indonesian / multi-lingual VO.** Zero-shot clone from `voices/*.m4a`; transcript auto-pairs from the matching `voices/*.srt`. Pluggable: upload `tts-lines.json` + ref `.m4a` + matching `.srt` (+ optional `tts-knobs.json`), run, done. GPU required. See § TTS below.
- `/tmp/run_blip_large_fast.py` — BLIP-large beam=1 (1.88GB, ~10s/img CPU, ~7 min total)
- `/tmp/run_git_base.py` — GIT-base coco (707MB, fastest, ~2s/img)
- `/tmp/run_florence2_colab.py` — Florence-2-base (requires transformers==4.38, currently fails on Colab image 4.55 — needs kernel restart + pip install)
- Original: `/tmp/caption_assets.py` — first BLIP-base run (44 images, captions-blip-base.json)
- `scripts/captions_srt.py` — **post-render caption sidecar (runs locally, no Colab)**: faster-whisper → word-timed `.srt` + word-level `.json` transcript (the input HyperFrames captions consume). Default `--model medium --language id`.
- `scripts/telegram-deliver.sh` — **delivery**: captions + video + title/description message → Telegram in one command (reads `.env`, never prints the token).

## Delivery (post-render: captions → Telegram)

The final two steps of every run (README TL;DR A steps 8–9):

```bash
# one command does it all: make the .srt, send the text package, then video + .srt
scripts/telegram-deliver.sh videos/<project>/renders/<project>.mp4 \
  --srt auto --text raws/<topic>/package.txt

# pieces, if you want them separate
python3 scripts/captions_srt.py <video> --json <video>.transcript.json   # .srt + word transcript
scripts/telegram-deliver.sh <video> --srt <video>.srt --text <package.txt>
scripts/telegram-deliver.sh <video> --dry-run                            # preview, sends nothing
```

- **Captions:** `faster-whisper medium` on CPU ≈ 14 min for a 72 s video; `--json` keeps the
  words, so any later `.srt` re-export is 0.5 s (`--srt auto` reuses it only when it is newer
  than the video). Cue rules: ≤5 words, ≤3.5 s, break on punctuation or a 0.6 s gap.
- **Auth:** `.env` in the repo root → `TELEGRAM_TOKEN` + `TELEGRAM_CHAT_ID` (numeric id, no
  prefix). The bot can only message a chat that has `/start`ed it first.
- **Order:** text message first (so the package sits above the files), then documents.
- **Limit:** Telegram bots cap uploads at 50 MB — renders above that need a YouTube/Drive link
  in the text message instead.

## Results (29 Aug 2026, karhutla-cpu CPU)

| Model | File | Images | Size | Avg quality | Note |
|-------|------|--------|------|-------------|------|
| BLIP-base | `captions-blip-base.json` | 44 | 223M | generic | amazon rainforest bias, map -> earthquake |
| GIT-base | `captions-git-base.json` | 44 | 347M (707MB safetensors) | better for photos | portrait politician OK, map still weak |
| BLIP-large FAST (beam=1) | `captions-blip-large.json` | 44 | 385M (1.88GB) | best of 3 on CPU | smoke billowing from forest fire -> correct |

All outputs in `raws/investigasi-karhutla/captions-*.json` + `.md` (table).

## Recommendation

- For **fast + decent**: GIT-base (2s/img CPU)
- For **best CPU**: BLIP-large beam=1 (slightly better detail, 10s/img)
- For **production (GPU)**: `blip2-opt-2.7b` or `Florence-2-large` with detailed caption (`<DETAILED_CAPTION>`) or `Qwen2-VL-2B` — provides actual peatland terminology (kanal, sekat, gambut) vs generic "forest". Use `colab run --gpu T4 scripts/caption_assets.py --model blip2` (ephemeral) or provision GPU when quota available.

## To add Indonesian captions

Post-process with LLM or use `caption_assets.py` with Florence-2 prompt `<CAPTION>` -> translate via `googletrans` or Qwen2-VL with Indonesian prompt.

## Cleanup

```bash
colab download -s karhutla-cpu /content/captions-blip-large.json raws/investigasi-karhutla/
colab stop -s karhutla-cpu
```

## TTS — OmniVoice (default for Bahasa) vs Piper (fallback)

**Default engine = OmniVoice** (zero-shot clone of a `voices/*.m4a`). **Fallback =
Piper `id_ID`** (trained Indonesian model, no reference) — use it when a clone still
sounds off, or when you want a clean, reference-free read. Both are **pluggable**
(upload JSON, never edit code). Full recipe + voice transcripts + model URLs +
gotchas → [`.docs/04-tts-voice-playbook.md`](../.docs/04-tts-voice-playbook.md).

### TTS (OmniVoice — DEFAULT for Bahasa, pluggable)

`scripts/tts_omnivoice.py` — Colab OmniVoice runner (k2-fsa/OmniVoice). Use for
Indonesian / multi-lingual VO when you want a **specific** voice cloned from
`voices/*.m4a`. **No code edits:** upload `/content/tts-lines.json`, the reference
`.m4a` **and its matching `.srt`** (auto-paired), + optional `/content/tts-knobs.json`,
then run.

```bash
# 1. new GPU session (T4 or better — OmniVoice is slow on CPU)
colab new -s <topic>-tts --gpu T4
colab install -s <topic>-tts omnivoice

# 2. upload reference voice + its matching transcript (.srt auto-pairs by filename)
colab upload -s <topic>-tts voices/female-medium-pace.m4a /content/ref-voice.m4a
colab upload -s <topic>-tts voices/female-medium-pace.srt /content/ref-voice.srt

# 3. upload the VO lines (+ optional knobs), then run (code never changes)
colab upload -s <topic>-tts raws/<topic>/tts-lines.json /content/tts-lines.json
# colab upload -s <topic>-tts raws/<topic>/tts-knobs.json /content/tts-knobs.json
colab exec -s <topic>-tts -f scripts/tts_omnivoice.py

# 4. download each scene WAV (single-arg only — loop)
for i in 1 2 3; do colab download -s <topic>-tts /content/tts-out/scene_$i.wav /tmp/vo-s$i.wav; done
colab download -s <topic>-tts /content/tts-out/final_full_voiceover.wav /tmp/vo-full.wav

# 5. stop (burns units)
colab stop -s <topic>-tts
```

**`tts-lines.json`** — `[{"id": "scene_1", "text": "..."}, ...]` or a dict. **Write numbers
in natural form** ("65 miliar", not "enam puluh lima miliar") or the audio mangles.

**`tts-knobs.json`** (optional): `{"speed": 0.9, "num_step": 32, "silence_s": 0.4, "out_dir": "/content/tts-out"}`
(`speed` 0.7 slow / 1.0 neutral / 1.3 fast; `num_step` 32 quality / 16 fast).

**Reference transcripts** — `voices/` ships one `.srt` per `.m4a`; the script flattens the
`.srt` (strips index numbers + timestamps) into the `ref_text` it feeds OmniVoice. If the
`.srt` is missing it falls back to auto-ASR (slower, less reliable). **Always upload the
matching `.srt`** — a mismatched/missing transcript is what garbles the cloned audio.

**Output:** `/content/tts-out/<id>.wav` (one per line) + `final_full_voiceover.wav`
(all lines concatenated with `silence_s` gaps), 24 kHz mono float32.

**Word-level captions (optional):** after download, run
`whisperx final_full_voiceover.wav --model base --language id --highlight_words True`
for karaoke-style caption timing (see PLAYBOOK-longform-to-clip §2a).

### OmniVoice known gotchas (from 2026-09 runs — read before your first run)

1. **`HF_TOKEN` vault error is harmless.** Colab prints `Error while fetching
   'HF_TOKEN' secret value ... only when running from the Colab UI.` It's a Colab-UI-only
   path; k2-fsa/OmniVoice is public and loads fine without a token. Ignore it.
2. **`librosa` deprecation spam.** Every `model.generate()` emits `PySoundFile failed.
   Trying audioread instead.` + a `librosa __audioread_load deprecated` FutureWarning.
   Pure noise; output is correct. Ignore.
3. **Cloned audio can be word-salad** if the reference transcript is missing or mismatched.
   `voices/*.srt` now auto-pairs by filename (the script flattens the SRT into `ref_text`).
   2026-09 Anthropic run: hardcoded `REF_TEXT` belonged to a *different* voice → garbage
   ("kebunyi temin"). Now fixed by auto-pairing; if a clone still sounds off, fall back to
   Piper `id_ID-medium` below — it reads the same `tts-lines.json` cleanly.
4. **T4 quota** worked 2026-09. If your account hits the quota, fall back to CPU —
   just slower, not broken.

### TTS (Piper — fallback for Bahasa, pluggable)

`scripts/tts_piper.py` — Colab Piper TTS runner. A **trained** TTS model (no reference),
so it reads Indonesian reliably and never mangles a clone. **No code edits:** upload
`/content/tts-lines.json` + optional `/content/tts-knobs.json` (`model_url` / `language`
/ `out_dir`) and run. The `.onnx` model auto-downloads on first run (default = `id_ID-medium`,
Indonesian).

```bash
# 1. new session + install piper-tts
colab new -s <topic>-tts
colab install -s <topic>-tts piper-tts

# 2. upload the VO lines (+ optional knobs)
colab upload -s <topic>-tts raws/<topic>/tts-lines.json /content/tts-lines.json
# colab upload -s <topic>-tts raws/<topic>/tts-knobs.json /content/tts-knobs.json

# 3. run (code never changes)
colab exec -s <topic>-tts -f scripts/tts_piper.py

# 4. download each WAV (single-arg only — loop)
for i in 1 2 3; do colab download -s <topic>-tts /content/piper-out/scene_$i.wav /tmp/vo-s$i.wav; done

# 5. stop (burns units)
colab stop -s <topic>-tts
```

**`tts-lines.json`** — either shape works:
```json
[{"id": "scene_1", "text": "..."}, {"id": "scene_2", "text": "..."}]
```
or a dict `{"scene_1": "...", "scene_2": "..."}`. Natural-form numbers only.

**`tts-knobs.json`** (optional): `{"model_url": ".../id_ID-news_tts-medium.onnx", "language": "id", "out_dir": "/content/piper-out"}`.

**Piper API (from 2026-09 Purbaya run):**
- `PiperVoice.load(onnx, config_path=onnx_json)` loads model + `.onnx.json`
- `voice.synthesize(text)` → generator of `AudioChunk`
- `chunk.audio_int16_bytes` = raw 16-bit PCM; `wave.writeframes(bytes)` directly
- Voice: `id_ID-medium` (Indonesian, default) — reads Bahasa cleanly; English → `en_US-lessac-medium`.

**Output sample rate:** Piper emits 22050 Hz int16. For HyperFrames audio slots
(24 kHz), resample: `ffmpeg -i in.wav -ar 24000 -ac 1 out.wav`.
