# TTS VOICE PLAYBOOK — plug-and-play (OmniVoice default, Piper fallback)

**Goal:** generate Bahasa VO from topic text with **no code edits**. Both `scripts/tts_piper.py`
and `scripts/tts_omnivoice.py` are now pluggable — you upload 2–4 small files and run them;
the Python never changes.

> **⚠️ Step 0 — the script itself.** TTS only reads what you hand it, and every video whose
> script was raw LLM prose came back as **AI-slop**: a flat opening, no turn, nobody still
> watching at second 15. So before anything on this page runs, write the script with
> **`/yt-script`** (YouTube skills pack — install recipe in `README.md` → "Other reference").
> It gives 5 hook options scored off 21 formulas, then the spoken script with retention beats,
> in the voice from `~/.claude/youtube/voice.md`. Save the approved cut as
> `raws/<topic>/VO-SCRIPT.md`; **that file**, not a chat transcript, is what `tts-lines.json`
> is built from. Structure first, engine second.

## The two engines

| Engine | `scripts/` file | How it works | When to use |
|---|---|---|---|
| **OmniVoice** (default) | `tts_omnivoice.py` | Zero-shot clone from a reference `.m4a` + its `.srt` transcript | **Default for Indonesian VO** — lets you pick a specific voice from `voices/*.m4a` |
| **Piper** (fallback) | `tts_piper.py` | Trained TTS model (`id_ID-medium`), reads Indonesian cleanly | When the OmniVoice clone sounds off, or you want a clean reference-free read |

> **Engine choice:** OmniVoice is the documented default because it reproduces the
> house voice (a specific `voices/*.m4a`). Piper is the reliable fallback — it's a
> trained model, so it never depends on a reference transcript.
>
> **Why the 2026-09 Anthropic VO was garbled:** the old OmniVoice script hardcoded a
> `REF_TEXT` that didn't match the uploaded voice (`female-medium-pace`). Now the
> transcript **auto-pairs from `voices/*.srt`** (one `.srt` per `.m4a`), so a mismatch
> can't happen silently. If a clone still sounds off, fall back to Piper `id_ID-medium`.

## Files you provide (per topic)

1. **`tts-lines.json`** → the VO script. Either shape works:
   ```json
   [{"id": "scene_1", "text": "..."}, {"id": "scene_2", "text": "..."}]
   ```
   or a dict: `{ "scene_1": "...", "scene_2": "..." }`
   - **Numbers are ENGINE-SPECIFIC** (proven 26 Sep 2026, A/B on the same 8 lines):
     | Engine | Digits (`100 miliar`) | Spelled (`seratus miliar`) |
     |---|---|---|
     | **Piper** | ✅ reads perfectly | ❌ mangles |
     | **OmniVoice** | ❌ mangles ("stat miliar", "terat tahun", "lamuk warawata") | ✅ reads perfectly |
     Keep two number forms per line, or convert per engine before upload
     (`scripts/` has no converter yet — hand-write the variant you need).

2. **Reference voice** (OmniVoice only) → upload `voices/<name>.m4a` and its
   matching `voices/<name>.srt` (already in this repo, one `.srt` per `.m4a`).

3. **`tts-knobs.json`** (optional) → speed / num_step / out_dir / model_url.

## Running (Colab CLI)

### A) OmniVoice (Bahasa, DEFAULT — clone of a voices/*.m4a)
```bash
colab new -s <topic>-tts --gpu T4
colab install -s <topic>-tts omnivoice
colab upload -s <topic>-tts voices/female-medium-pace.m4a /content/ref-voice.m4a
colab upload -s <topic>-tts voices/female-medium-pace.srt /content/ref-voice.srt
colab upload -s <topic>-tts raws/<topic>/tts-lines.json /content/tts-lines.json
# optional knobs: colab upload -s <topic>-tts raws/<topic>/tts-knobs.json /content/tts-knobs.json
colab exec -s <topic>-tts -f scripts/tts_omnivoice.py
colab stop -s <topic>-tts
```
Output: `/content/tts-out/<id>.wav` (24 kHz mono float32) + `final_full_voiceover.wav`
(concatenated with `silence_s` gaps).

### B) Piper (Bahasa fallback — trained id_ID model, no reference)
```bash
colab new -s <topic>-tts
colab install -s <topic>-tts piper-tts
colab upload -s <topic>-tts raws/<topic>/tts-lines.json /content/tts-lines.json
# optional: colab upload -s <topic>-tts raws/<topic>/tts-knobs.json /content/tts-knobs.json
colab exec -s <topic>-tts -f scripts/tts_piper.py
for i in 1 2 3; do colab download -s <topic>-tts /content/piper-out/scene_$i.wav /tmp/vo-s$i.wav; done
colab stop -s <topic>-tts
```
Output: `/content/piper-out/<id>.wav` (native 22050 Hz int16). For a HyperFrames
composition, resample to 24 kHz mono: `ffmpeg -i in.wav -ar 24000 -ac 1 out.wav`.

## Voice reference transcripts (in `voices/`)

Each `.m4a` has a matching `.srt` (auto-paired by filename; upload both for OmniVoice):

| File | Pace | Content (transcript summary) |
|---|---|---|
| `famale-slow-pace.m4a` | slow | Yogyakarta river / giant elephant (calm storytelling) |
| `female-medium-pace.m4a` | medium | "why haven't we found aliens" (conversational) |
| `female-fast-pace.m4a` | fast | "age of the universe 13.8 billion years" (upbeat) |

> `voices/famale-slow-pace` has a historical typo ("famale") in its filename — keep it as-is
> for backwards compat; the `.srt` still auto-pairs.

## Piper model URLs (for `tts-knobs.json` → `model_url`)

```json
{"model_url": "https://huggingface.co/rhasspy/piper-voices/resolve/main/id/id_ID/news_tts/medium/id_ID-news_tts-medium.onnx", "language": "id"}
```
- Indonesian: `.../id/id_ID/news_tts/medium/id_ID-news_tts-medium.onnx`
- The `.json` config is derived automatically (append `.json` to the same path).
- English: `.../en/en_US/lessac/medium/en_US-lessac-medium.onnx`

## Knobs reference

**Piper `tts-knobs.json`:** `model_url`, `language`, `out_dir` (default `/content/piper-out`).

**OmniVoice `tts-knobs.json`:** `speed` (0.7 slow / 1.0 neutral / 1.3 fast), `num_step`
(32 quality / 16 fast), `silence_s` (gap between lines, default 0.4), `out_dir`
(default `/content/tts-out`).

## Gotchas (2026-09 Anthropic-IPO run)

1. **OmniVoice + wrong `REF_TEXT` = word-salad.** Previously `REF_TEXT` was hardcoded to
   one voice's transcript; cloning from a *different* `.m4a` produced garbage
   ("kebunyi temin", "ngai naman banun"). Now the transcript auto-pairs from the
   matching `.srt` — no hardcoded ref text.
2. **Number form is engine-specific — digits break OmniVoice, spelled-out breaks Piper**
   (26 Sep 2026 A/B, `raws/anthropic-ipo/vo-omnivoice*`). OmniVoice mangled
   "100 miliar" → "stat miliar", "30 tahun" → "terat tahun", "5,44 persen" →
   "lamuk warawata", "4 September" → "Setarta"; spelling them out fixed every line.
   Piper has the opposite rule. See the table in §Files above.
3. **OmniVoice also mangles foreign/brand words:** "Claude" → "klot"/"Cloud" —
   write a phonetic stand-in in the VO line if the caption carries the real spelling
   (used "Kloud" for `tts-lines.json`; on-screen text still says Claude).
4. **Piper output is 22050 Hz int16**; resample to 24 kHz before wiring into HyperFrames
   audio slots (the composition's other media is 24 kHz). OmniVoice already outputs 24 kHz.
5. **OmniVoice default `speed=0.9` runs fast** — same 8 lines gave 55.7s vs Piper's 72.9s
   (would break every beat/caption timing). `speed: 0.7` in `tts-knobs.json` stretched it
   to 71.2s (within ~1.8s of Piper). **Always compare total duration against the Piper
   baseline before wiring a new VO in** — beat starts are baked into `data-start`.
6. **OmniVoice read errors are silent** — the run reports `DONE` regardless of quality.
   Always verify with `faster-whisper` (`medium`, `language="id"`) line-by-line against
   `tts-lines.json` before declaring a take good. ASR confirmed all 8 spelled-form lines
   clean, incl. "100 miliar / 30 tahun / 5,44 persen / 22 tahun".
