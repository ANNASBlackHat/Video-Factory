# 07 — Lessons Learned: Anthropic IPO Evidence Desk Run (26 Sep 2026)

**What this is:** post-mortem of the evidence/newsroom rebuild (`anthropic-ipo-evidence`) +
the OmniVoice-vs-Piper A/B. Skim this before starting the next topic — it records where time
was lost, what got invented along the way, and which older rules this run overturned.

**Companion docs:**
- Workflow log: [`06-anthropic-ipo-evidence.md`](06-anthropic-ipo-evidence.md)
- TTS engine rules (updated this run): [`04-tts-voice-playbook.md`](04-tts-voice-playbook.md)
- Facts lock: `raws/anthropic-ipo/REPORT-REFRESH-2026-09-26.md`
- A/B takes: `raws/anthropic-ipo/vo-omnivoice*/` · VO assets: `videos/anthropic-ipo-evidence/assets/vo/`
- Renders: `videos/anthropic-ipo-evidence/renders/anthropic-ipo-evidence.mp4` (OmniVoice, final)
  + `-piper-backup.mp4`

---

## §1. The premise (why this project exists)

The previous concept (`anthropic-ipo-ticker-shock`) was rejected: too much motion, no real
footage — screenshots only appeared as ~12% opacity backgrounds. This run inverted the rule:

- **Evidence is the visual** — screenshots/photos/muted clips at full opacity, in a browser-card
  grammar (URL pill + source/date bar + red stamp chips).
- **Motion is seasoning** — Ken Burns 1.00→1.045 only, hard news cuts, no odometer/terminal/ticker.

### Next time
- When a video is rejected for "no real footage," don't restyle the old one — rebuild around an
  *evidence container* (the `.win` card) that makes raw screenshots look designed.

---

## §2. YouTube footage as evidence (new, user-approved)

**The idea that landed:** muted news clips (yt-dlp) playing inside a browser card — a CNBC chyron
actually moving proves "this was broadcast" in a way a still can't. User's verdict: *"Youtube is
new, i like that."*

### What held us back
1. **Sparse-keyframe warning** — yt-dlp output had GOPs up to 8.34s; HyperFrames wants dense keys.
2. **Fast capture renders `<video>` regions black** — check passed, preview fine, final render
   black. This was the single scariest failure of the run.

### Solutions made
- Re-encode every clip: `ffmpeg -c:v libx264 -preset fast -crf 18 -r 30 -g 15 -keyint_min 15
  -pix_fmt yuv420p -movflags +faststart -an`; keep `assets/footage/*.orig.mp4`; clear
  `$TMP/hyperframes-extract-cache-<uid>` after re-encoding or the old frames are reused.
- **Render with `--experimental-fast-capture=false`** (screenshot capture) whenever the
  composition contains `<video>`. Verify with luma: `ffmpeg -ss <t> -i out.mp4 -frames:v 1 -vf
  "signalstats,metadata=print:key=lavfi.signalstats.YAVG"` — ~37–45 is bright for a dark
  newsroom frame; ~10–15 means black video.

### Next time
- Bisection harness first: a 1-scene `/tmp` project with one `<video>`, render both capture
  modes (≈1 min) — don't burn two full renders discovering the mode difference.
- Standard clip recipe: yt-dlp → GOP re-encode → ffprobe duration → wire `data-start`/`data-duration`.

---

## §3. Composition contract (video nesting + the `.pane` escape)

### Pitfalls hit
1. **`video_nested_in_timed_element` (hard error)** — a timed wrapper containing a `<video>` with
   its own `data-start`.
2. **The obvious fix was worse** — `class="clip"` on the `<video>` gave it `inset:0`, pulling it
   out of flow and collapsing `.winbody` to height 0 (invisible card).
3. **`gsap_animates_clip_element`** — GSAP animating autoAlpha on anything whose *class attribute*
   contains `clip`. (`getClipTagClasses` reads the class attr only.)

### Solution
One structural idea solves all three: **untimed `class="pane"` wrappers** (no `data-start`),
video owns its own timing, GSAP gates the wrapper in/out at beat edges:
```js
tl.from("#b2", { y: 42, autoAlpha: 0, ... }, beatStart);
tl.to("#b2", { autoAlpha: 0, ... }, beatEnd - 0.2);
```
`.clip, .pane { position:absolute; inset:0 }` — but the `<video>` itself stays plain
(`muted playsinline preload="auto"` + own `data-start`/`data-duration`/`data-track-index`).

### Next time
- Rule: **timed wrapper XOR video timing, never both; `pane` for GSAP-gated wrappers, `clip` for
  DOM-timed ones.** Never put `clip` on a media element.

---

## §4. TTS — the biggest lesson cluster

### Pitfalls hit
1. **OmniVoice digit mangling** — "100 miliar" → "stat miliar", "30 tahun" → "terat tahun",
   "5,44 persen" → "lamuk warawata", "4 September" → "Setarta". The run reports `DONE` regardless.
2. **"Claude" → "klot"** — foreign/brand words are a *third* failure category beyond digits.
3. **`speed 0.9` produced 55.7s vs Piper's 72.9s** — would have silently desynced every caption,
   beat, and SFX in a composition whose timings were baked to the old VO.
4. **Colab session died mid-run** (404/401) — uploads started failing after ~1h.
5. **Ambiguous ASR result** ("5,4" vs "5,44") — whisper collapses repeated digits; word-timestamp
   span analysis couldn't settle it either.

### Solutions made
- **A/B ladder (3 runs):** digits (garbled) → spelled numbers (clean, but "Claude" broken) →
  spelled + phonetic "Kloud" + `speed: 0.7` = 71.16s, all 8 lines ASR-clean.
- **Engine-specific number rule** (overturns doc 03/doc 04's old blanket rule):

  | Engine | Digits (`100 miliar`) | Spelled (`seratus miliar`) |
  |---|---|---|
  | Piper | ✅ | ❌ |
  | OmniVoice | ❌ | ✅ |

- **ASR as a QA gate:** `faster-whisper medium`, `language="id"`, transcribe every take
  line-by-line against `tts-lines.json` *before* declaring it good. Also transcribe the
  **rendered** file to confirm which take actually shipped.
- **Phonetic stand-in pattern:** audio says "Kloud", on-screen text keeps "Claude".
- **Duration gate:** compare total VO duration to the outgoing baseline before wiring in;
  stretch with `speed` (OmniVoice) not by editing beats.
- **Beep-separated A/B listen file** (`ffmpeg` concat with 880 Hz separators) so the *user's*
  ears decide, not mine — I can't listen.
- **Session hygiene:** recreate Colab sessions per work block; re-upload all inputs (ref voice +
  srt + lines + knobs + script) rather than assuming files persist.

### Next time
- Never wire a new VO into an existing timeline without: (1) ASR line check, (2) total-duration
  match, (3) recomputed scene starts → retime.
- For Indonesian: OmniVoice house voice (`voices/*.m4a` + matching `.srt`) is the default if
  numbers are spelled out; Piper `id_ID-*` is the fallback if digits are needed. (Doc 03's
  "never use Piper for Indonesian" was about the *English voice* Piper fallback — `id_ID-*`
  models are fine.)

---

## §5. The retime (90 values, zero typos)

### Pitfalls hit
Swapping the VO meant moving every timing in `index.html`: 12 beat sections, 3 video
`data-start`s, 8 caption bands, 14 SFX, ~40 GSAP cue times, chrome duration 74→72.3.

### Solution made
A **scripted patch with per-replacement count assertions** — each `(old, new, expected_count)`
pair fails the whole run if the old string doesn't appear exactly that many times:
```python
pairs = [('data-start="16.72"', 'data-start="15.41"', 2), ...]  # b5 section + sfx05
for old, new, exp in pairs:
    assert src.count(old) == exp, f"{old!r}: {src.count(old)} != {exp}"
```
93/93 groups exact; one `hyperframes check` after → 0 errors.

### Next time
- For any bulk retiming: derive new scene starts first (OmniVoice: durations + `silence_s` gaps
  summed *exactly* to the file duration — arithmetic beats VAD, which split mid-sentence here),
  then write the assertion script. Hand-editing 90 numbers guarantees a typo.

---

## §6. Render + QA

### What worked
- **Contact sheets + seam audit** — 16-frame sheet (`ffmpeg select+tile`) for overall pass, plus
  an hstack strip *across a hard cut* (b7→b8 at 39.6/40.4/41.0/42.0s) to catch black-frame gaps
  a random sheet would miss. The seam was clean (hard cut, card fades in 0.38s).
- **Luma probes** at scene starts (YAVG 37–45 = bright on this dark design).
- **ffprobe + volumedetect** on every render (duration/size/mean/max dB).
- Renders: Piper 11m54s (74.0s) → backup; OmniVoice 4m14s (72.3s, 38.8 MB) → final.

### What held us back
- **`check` passing says nothing about pixels.** Two full renders were needed to catch
  black-video; the fix (§2) means one render now.

### Next time
- Render pipeline: `check` → 30s luma/snapshot probe on the first minute → full render →
  contact sheet + seam strip + rendered-audio ASR.

---

## §7. Cross-cutting (all sections)

### Top 5 time sinks this run
1. Black-video discovery (2 full renders + a bisection harness) — ~40 min
2. TTS A/B ladder (3 Colab runs incl. one session death) — ~1.5 h
3. The 93-group retime (fast *because* scripted, but still the scariest edit) — ~20 min
4. ASR verification passes (whisper medium on CPU is slow; one 15-min timeout on a 2-file run)
5. Layout-warning iteration (`allow-overflow`/`allow-occlusion`/caption `bottom:auto`)

### Rules for next run
1. **`<video>` in a composition → screenshot capture, GOP-re-encoded clips, `pane` wrappers.**
2. **ASR-gate every TTS take before wiring; match duration to the outgoing baseline.**
3. **Numbers in VO text are engine-specific** — see the doc 04 table.
4. **Bulk timing changes → assertion script, never hand edits.**
5. **Audit seams, not just scenes** — one hstack across each hard cut.
6. **Docs record reversals** — when this run overturned doc 03's Piper rule, update the old doc
   too, or the next run will follow a dead rule.
