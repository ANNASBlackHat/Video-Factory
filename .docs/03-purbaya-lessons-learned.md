# 03 — Lessons Learned: Purbaya Menkeu Reshuffle Run (15–16 Sep 2026)

**What this is:** per-section post-mortem of the Purbaya run. Next time we come back to a topic, skim this before starting — it records where we lost time and what worked.

**Companion docs:**
- Workflow log: [`02-purbaya-suahasil-menkeu.md`](02-purbaya-suahasil-menkeu.md)
- Facts lock: `raws/purbaya-suahasil-menkeu/REPORT-POLICY-IMPACT-purbaya.md` §5
- Rendered concepts: `videos/purbaya-menkeu-reshuffle/`, `videos/purbaya-stat-hit/`, `videos/purbaya-paper-trail/`
- Recipes: `videos/<project>/.media/recipes/<name>/` (purbaya-investigasi, purbaya-stat-hit, purbaya-paper-trail)

---

## §1. Research (websearch + raw)

### What worked
- **20+ sources from 3 deep queries** was enough to lock facts without going deeper. The 7-claim structure (internal coordination, Danantara dividen, BI friction, macro pressure, program burden, communication style, unverified rumor) covers the whole story.
- **Facts lock early** in `REPORT-BROADENED` (before assets) meant every later stage — VO script, captions, recipe — could point to one source of truth.

### What held us back
- **No websearch tool this session** (the `websearch` tool was unavailable in several turns); I fell back on `webfetch` + chrome MCP navigation, which is slower. If `websearch` is available, prefer it for the first pass.
- **Wikipedia EN returned a generic "In the news" page** instead of the Suahasil article — I had to use the ID Wikipedia instead. Don't assume EN will have a fresh article on a <2-day-old reshuffle.

### Next time
- Start with `websearch` if available; fall back to `webfetch` (markdown) or chrome MCP only when a page has JS-rendered content.
- Verify the ID + EN Wikipedia both before relying on a profile.

---

## §2. Social media scan

### What worked
- **YouTube search page via chrome MCP** was the cheapest footage table — I parsed 16 videos in one navigation without needing the YouTube API.
- The **"Udah siap belum?" TikTok post** (4.8M views) was the viral close; I had to actively search for it, it wasn't in the news coverage of the reshuffle itself.

### What held us back
- **X/Twitter API not available** — I could only infer sentiment from media coverage that quoted X. Next time, if the user has X access, capture 3–5 top tweets directly before building.
- **YouTube table stayed at 16** (target was 20–30). The gap is cosmetic but noted.

### Next time
- Search for the subject's own social post (TikTok, X) as a separate query — that's where the viral hook lives, not in the news.
- If X capture is requested, ask the user to share a screen recording rather than trying to scrape.

---

## §3. Chrome asset capture

### Pitfalls hit
1. **Every `navigate_page` returned "timeout of 10000ms exceeded"** yet the page had loaded. I initially assumed the navigation failed and re-navigated, wasting time. The snapshot confirmed the page was fine each time.
2. **CDN DNS failures** — `cdn25.metrotvnews.com`, `akcdn.detik.net.id`, and `img2.beritasatu.com` failed on first curl, succeeded on retry. I burned 20+ seconds on each retry.
3. **beritasatu CDN (img2.beritasatu.com) returned an HTML error page (919 bytes) instead of the image** — I almost froze it. `file` command caught it.

### Solutions made
- Treated "timeout" as "loaded, check snapshot" not "retry navigation."
- **Froze via curl, not via chrome** — chrome MCP gives me the image URLs; I `curl -L -o` locally, then `file` to validate it's actually an image (not HTML/redirect).
- **Retried failed CDNs once** before marking them as broken; most transient DNS failures succeed on the 2nd attempt.
- **Removed empty/0-byte files** before zipping; validated with `find . -type f -size +5k`.

### Next time
- Standard recipe: navigate → snapshot → evaluate `document.images` filtered `w>400` → curl each URL → `file` to confirm JPEG/PNG/WebP → remove HTML/error pages → count.
- If a CDN fails DNS twice, mark it "skip" in ASSET-INVENTORY rather than keep retrying.

---

## §4. Colab (caption step + VO generation)

### Pitfalls hit
1. **`colab upload` 500 Internal Server Error** — 4 consecutive failures across 2 fresh sessions. The endpoint is platform-side; auth + exec both worked. I retried blindly for ~10 minutes before realizing the only fix was stop/re-create/retry.
2. **Piper TTS API misuse** — 6 iterations to get the right call:
   - `synthesize()` returns `AudioChunk` objects, not raw ints
   - The correct property is `chunk.audio_int16_bytes` (not `.samples` or `.audio_float_array`)
   - `wave.writeframes(raw_bytes)` takes bytes directly — no `struct.pack`, no `array.array` conversion
3. **`colab download` is single-path only** — I tried passing 6 paths, got "unexpected extra argument". Had to loop.
4. **Piper with English voice reading Indonesian** produced 86.8s of audio for 6 short lines, and it sounded clearly wrong. I shipped it anyway; the user caught it and said to use their own VO instead.
5. **OmniVoice `OUT_DIR` collision** — when I generated stat-hit then paper-trail in the *same* Colab session, both wrote to the default `/content/tts-out/` and the second run overwrote the first. I re-ran stat-hit to recover. (Fixed: `scripts/tts_omnivoice.py` now reads `TTS_OUT_DIR` env var; default still `/content/tts-out`.)
6. **OmniVoice `HF_TOKEN` vault error** — every run prints `Error while fetching 'HF_TOKEN' secret value from your vault: ... only when running from the Colab UI.` This is a Colab-UI-only path; the model is public and loads fine. It looked alarming but is **harmless** — ignore it.
7. **`librosa` deprecation spam** — every `model.generate()` emits `PySoundFile failed. Trying audioread instead.` + a FutureWarning. Pure noise, output is correct.

### Solutions made
- **Colab upload retry pattern:** on 500, `colab stop`, `colab new`, wait 5s, retry. Worked on the 6th attempt.
- **Piper recipe (documented in `/tmp/run_piper_final2.py`):**
  ```python
  from piper import PiperVoice
  voice = PiperVoice.load(model_path)
  for chunk in voice.synthesize(text):
      raw += chunk.audio_int16_bytes
  wave.writeframes(raw)
  ```
- **`colab download` loop:** one file at a time, `for i in 1 2 3 4 5 6; do colab download ...; done`.
- **OmniVoice reusable runner:** `scripts/tts_omnivoice.py` (with `TTS_OUT_DIR` env var to avoid the collision above). Known-gotchas block in `scripts/README.md` § TTS.

### Next time
> **SUPERSEDED (26 Sep 2026):** the Piper/OmniVoice guidance below has been revised — number
> formatting is now **engine-specific** (digits break OmniVoice, spelled-out breaks Piper), the
> `REF_TEXT` hardcode is gone (transcript auto-pairs from `voices/*.srt`), and OmniVoice beat
> Piper in an A/B. Use [`.docs/04-tts-voice-playbook.md`](04-tts-voice-playbook.md) as the
> source of truth; lessons from the run that proved this: [`.docs/07-lessons-evidence.md`](07-lessons-evidence.md).
- **Don't generate VO with Piper for Indonesian** — the English-voice fallback is not a usable substitute. **Use `scripts/tts_omnivoice.py` (OmniVoice, k2-fsa/OmniVoice) instead** — it's multilingual (including `id`), zero-shot clones from `voices/*.m4a` samples, and outputs 24 kHz WAV per scene. GPU required (`--gpu T4`). Keep the `REF_TEXT` transcript of the reference clip in the script so cloning is faster + more reliable.
- **For OmniVoice:** set `TTS_OUT_DIR=/content/tts-out-<topic>` (or stop/recreate the session per topic) so two topics in one session don't clobber each other. Ignore the `HF_TOKEN` and `librosa` warnings — they're noise.
- For Colab captions (BLIP-large on 20 imgs): keep the wrapper script pattern, but note the upload 500s may recur. Budget 5 minutes for retry.

---

## §5. HyperFrames build (3 concepts)

### Pitfalls hit
1. **Audio `data-duration` mismatch** — my SFX slots (0.4–3.0s) didn't match the actual SFX file lengths (0.12–2.8s), triggering 10 `clip_media_fit` warnings.
2. **`<audio>` elements need `id`** — first lint run caught `media_missing_id` as an error; I had to add ids to all 18 audio elements.
3. **Scene divs needed `id` for Studio** — 6 `studio_missing_editable_id` warnings on the scene divs; fixed by adding `id="scene-N"`.
4. **GSAP + CSS `transform` conflict** — the first pass had a CSS `transform` on `.stamp` that fought the GSAP tween; `gsap_css_transform_conflict` would have caught it. I caught it in the initial write by using `gsap.fromTo` for the initial state instead of CSS.
5. **Contrast check failed on the `.ghost` text (0.05 opacity)** and the `#404040` watermark — both fixed by removing the ghost element and brightening the watermark to `#8a8a8a`.

### Solutions made
- **SFX calibration step:** probe every SFX with `python3 -c "import wave; w=wave.open(f); print(w.getnframes()/w.getframerate())"` and set `data-duration` to the real length. This eliminated all `clip_media_fit` warnings.
- **All 3 projects passed `npx hyperframes check`** before render — 0 errors each. The 5–7 remaining warnings are all `studio_missing_editable_id` / `timeline_track_too_dense`, which are acceptable for a single-file composition.

### Next time
- Standard recipe for SFX: generate library → probe each file → set `data-duration` to measured length → add `id` to every `<audio>`.
- For multi-scene single-file compositions, accept `timeline_track_too_dense` warnings rather than splitting into sub-compositions (the 6-scene investigation is ~300 lines, splitting adds overhead).

---

## §6. Render

### What worked
- **`nohup npm run render &` + poll log** — all 3 renders survived the shell session. Total render time: Video 1 ~7 min (2775 frames), Video 2 ~2 min (540 frames), Video 3 ~4 min (1560 frames).
- **ffprobe verification after each render** — confirmed duration + codec before declaring success.
- **`look.py` contact sheets** — generated `*_sheet.png` for each; I can't view them but the user can.

### What held us back
- **No image vision** — I can't open the contact sheets to verify layout. "Check passed" was my only quality gate. If the user shares a screenshot I can calibrate.

### Next time
- After render, ask the user to open the `*_sheet.png` and confirm before considering the video final.
- For 90s+ videos at 1080x1920, budget ~8 minutes for render; check the process is still alive (`ps aux | grep hyperframes render`) before assuming a stall.

---

## §7. Recipe freeze

### What worked
- The **4-file recipe structure** (`frame.md`, `recipe.json`, `brief-skeleton.md`, `storyboard-skeleton.md`) matches the IPO `market-crime-desk` format exactly, so the intent layer will pick it up without modification.
- **Facts lock in 3 places** (BRIEF.md per project, REPORT-POLICY-IMPACT §5 as source of truth, recipe frame.md "Facts lock" section) reduces the chance of agent-invented numbers on the next run.

### Next time
- When freezing a recipe, copy the `frame.md` "Facts lock" section from the `REPORT-*-IMPACT` doc — don't re-derive it.
- Name the recipe after the topic (`purbaya-investigasi`), not the aesthetic (`crime-desk-v2`), so "make another purbaya-investigasi" is unambiguous.

---

## §8. Cross-cutting (all sections)

### Top 5 time sinks this run
1. Chrome "timeout" confusion — ~10 wasted navigations
2. Colab upload 500s — ~5 minutes blind retries
3. Piper TTS API — 6 iterations
4. CDN DNS failures — 4 retries
5. Audio `data-duration` calibration — 1 lint pass to catch, then ffprobe to fix

### Rules for next run
- Treat chrome MCP "timeout" as "loaded, check snapshot" not "retry navigation."
- CDN DNS: retry once; if it fails twice, mark "skip" and move on.
- Colab upload 500: stop → new → wait 5s → retry; max 3 attempts, then ask the user.
- Don't generate Indonesian VO with Piper; ask the user for WAV files up front.
- Probe SFX lengths with `wave.open()` before writing `data-duration`.
- Add `id` to every `<audio>` element on first write (not after lint catches it).
