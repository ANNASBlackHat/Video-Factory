# 06 — Anthropic IPO: Evidence Desk (concept → video, 26 Sep 2026)

**Deliverable:** vertical newsroom/evidence video, real screenshots + photos + muted news clips, Bahasa VO.
**Project:** `videos/anthropic-ipo-evidence/` (72.3s, 1080×1920, 38.8 MB, `renders/anthropic-ipo-evidence.mp4`; Piper backup: `renders/anthropic-ipo-evidence-piper-backup.mp4`).

## Why this exists (vs `.docs/05-anthropic-ipo.md`)

User verdict on `anthropic-ipo-ticker-shock`: too much motion, no real footage — old screenshots
only appeared as ~12% opacity backgrounds. New rules:

- **Evidence is the visual:** news screenshots, real photos, muted YouTube news clips at full opacity.
- **Newsroom look:** browser-window cards (`url pill` + `srcbar` source/date), hard cuts, stamp chips.
- **Motion diet:** Ken Burns only (1.00 → 1.045 over each card), no odometer/terminal-typing/ticker.
- **VO rewritten around the delay angle** (Oct → mid-October → November, EDGAR still empty).

## Research → facts (locked in `raws/anthropic-ipo/REPORT-REFRESH-2026-09-26.md`)

- Confidential S-1 filed **1 Jun 2026**; **EDGAR empty as of 26 Sep 2026**.
- Slip chain: Oct → mid-Oct roadshow (Reuters 4 Sep) → November (WSJ 18 Sep); 15-day rule.
- Up to **$100B at ~$2T**; Nvidia up to $10B; $15B revolver; founders 50.1% voting.
- 30y yield **5.44%**; Q2 prelim $11.5B; run-rate $65B; SpaceX IPO $1.77T; Nasdaq, MS/GS/JPM/Citi.
- Blocked sources (use syndication): WSJ, Reuters (bot wall), Polymarket + Admiral Markets (cert errors).

## Assets (`raws/anthropic-ipo/ASSET-INVENTORY.md`)

14 news PNGs + 6 photos + 3 muted clips (CNBC TV, Yahoo Finance, Bloomberg TV via yt-dlp) +
19-file SFX library copied from `anthropic-ipo-ticker-shock/assets/audio/sfx` (never regenerate).

**VO — final = OmniVoice house voice** (A/B won 26 Sep 2026; user picked OmniVoice):
- `raws/anthropic-ipo/vo-omnivoice-final/` — 8 lines + `final_full_voiceover.wav` (71.16s, 24 kHz).
- Take: clone of `voices/female-medium-pace` (`ref-voice.srt` auto-paired), **spelled-out numbers**,
  phonetic "Kloud" for Claude, `tts-knobs.json` `speed: 0.7`.
- A/B + gotcha table in `.docs/04-tts-voice-playbook.md` (digits break OmniVoice, spelled breaks Piper).
- Wired as `assets/vo/final_full_voiceover.wav`; the Piper take is kept at
  `assets/vo/final_full_voiceover-piper.wav` (72.89s) — scene starts 0.00 / 8.81 / 16.72 /
  24.17 / 32.14 / 40.95 / 52.07 / 64.73.
- **OmniVoice scene starts (drive all timing):** 0 / 8.36 / 15.41 / 22.83 / 31.15 / 39.99 /
  50.95 / 63.70; composition is **72.3s** (VO 71.16 + 1.14s tail).

## Composition structure (12 beats, `index.html`, 530 lines)

`data-duration="72.3"`; persistent chrome `#bg #rail #topbar #progress #footer` (z 5/6); beats
B1–B12 with absolute `data-start`/`data-duration`; 8 caption bands `cap1`–`cap8`
(`data-layout-allow-caption-zone`, `bottom:auto`, top 1502 — clear of footer 1768); VO track 10;
14 SFX tracks 11–24; single paused GSAP timeline `window.__timelines["main"]`.

Beat map (OmniVoice): b1 0–4.35, b2 clip 4.35–8.36, b3 8.36–11.74, b4 clip 11.74–15.41,
b5 15.41–22.83, b6 22.83–31.15, b7 31.15–39.99, b8 39.99–45.46, b9 clip 45.46–50.95,
b10 50.95–54.71, b11 54.71–63.70, b12 63.70–72.30.

## Hard-won render rules (do not rediscover)

1. **`video_nested_in_timed_element` is a hard error.** A timed wrapper containing a `<video>`
   with `data-start` fails check. Fix: sections holding videos are **untimed** —
   `class="pane"` (no `data-start`), gated in/out by GSAP `from/to` autoAlpha at beat edges.
   `.clip, .pane { position:absolute; inset:0 }`.
2. **Never add `class="clip"` to a `<video>` itself.** `inset:0` pulls it out of flow and
   collapses `.winbody` (card body height 0). Videos stay plain: `muted playsinline
   preload="auto"` + own `data-start`/`data-duration`/`data-track-index`.
3. **`gsap_animates_clip_element`** fires if GSAP animates autoAlpha on any element whose class
   attr contains `clip` (`getClipTagClasses` checks the class attribute only) — hence the `pane`
   alias above.
4. **Default fast capture (`drawelement`) renders `<video>` areas black** for this composition.
   Render with `--experimental-fast-capture=false` (screenshot capture). Verified: YAVG 58/88/88
   bright vs ~26 black; final render spot-checks 37–45 mean on the dark newsroom frame.
5. **Sparse-keyframe warning (GOP up to 8.3s)** from yt-dlp output → re-encode all clips
   `ffmpeg -c:v libx264 -preset fast -crf 18 -r 30 -g 15 -keyint_min 15 -pix_fmt yuv420p
   -movflags +faststart -an`; keep `assets/footage/*.orig.mp4`; clear
   `$TMP/hyperframes-extract-cache-<uid>` afterwards.
6. **Node: `nvm use 24.18.0`** before any `npx hyperframes` (default v20.19.5 is too old).
7. Layout knobs that fixed check warnings: `data-layout-allow-overflow` on every `.winbody`
   (Ken Burns), `data-layout-allow-occlusion` on closing plate/scrim; `.qpill{white-space:nowrap}`;
   `.close-sub` clamped to `left/right:70px`.

## Final render + QA

```bash
export NVM_DIR="$HOME/.nvm"; . "$NVM_DIR/nvm.sh"; nvm use 24.18.0
npx hyperframes check                    # 0 errors, 14 warnings (advisory only)
npx hyperframes render --no-best-effort --experimental-fast-capture=false \
  --skill hyperframes -o renders/anthropic-ipo-evidence.mp4
```

- **Render 1 (Piper):** 11m54s, 38.5 MB, 74.0s, AAC (mean −16.5 dB, max −1.7 dB) → kept as
  `anthropic-ipo-evidence-piper-backup.mp4`.
- **Render 2 (OmniVoice, final):** 4m14s, 38.8 MB, **72.3s**, AAC (mean −16.8 dB, max −1.5 dB) →
  `anthropic-ipo-evidence.mp4`. Retimed via scripted patch (93 replacement groups: section
  starts/durations, video data-starts, 8 caption bands, 14 SFX, all GSAP cue times, chrome
  duration 74→72.3).
- QA: 16-frame contact sheet `audit/omni/sheet.jpg` + b7→b8 seam strip `audit/omni/seam_row.jpg`
  (hard cut, no black frame); scene-start luma 37–45 (dark newsroom frame — clips bright);
  rendered audio transcribed with faster-whisper — OmniVoice take present, scene starts aligned.
- Diagnostic clutter (diag*.mp4, snapshots/, intermediate audit frames) deleted; keep only the
  final renders + `audit/final_sheet.jpg` + `audit/final/` + `audit/omni/`.
