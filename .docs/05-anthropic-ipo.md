# 05 — Anthropic IPO: $2 Trillion? (concept → video, 20 Sep 2026)

**Deliverable:** single vertical video, "Money: valuation shock" aesthetic, neutral both-sides, Bahasa VO.
**Project:** `videos/anthropic-ipo-ticker-shock/` (72s, 1080×1920, h264+aac, 13.2 MB).

## What was built

| Scene | Window | Visual |
|---|---|---|
| S1 Hook | 0–9.5s | terminal boots, valuation counter → **$2,000B** |
| S2 Filing | 9.5–20.9s | **1 JUNI 2026** S-1 card + October debut target |
| S3 Media | 20.9–30.9s | FT/WSJ/Bloomberg/Forbes headline feed + "RUMOR, BUKAN FAKTA" chip |
| S4 Revenue | 30.9–41.8s | $4.5B→$47B→**$65B** run-rate, 14× chip |
| S5 Compute bill | 41.8–50.9s | **$517B** counter + 14.8GW / SpaceX $15B/yr |
| S6 Bull vs Bear | 50.9–59.8s | dual terminal: green bull case vs red bear case |
| S7 Duel+Verdict | 59.8–72s | Anthropic vs SpaceX record check ($1.77T → $2T+) + "PASAR YANG AKAN MEMUTUSKAN" |

Burned-in captions every scene, bottom ticker strip, 21 SFX (calibrated to real durations), Bahasa VO.

## Research → facts (locked in `raws/anthropic-ipo/Anthropic-IPO.md`)

- **$2T = investor *expectation*, not a company-set number** (FT, 13 Aug 2026).
- Confidential S-1 filed **1 June 2026** (NYT); target debut **October 2026**.
- Last private valuation **$965B** (May 2026 Series H, $65B raise).
- Revenue: **$4.5B (2025) → $47B (May'26) → $65B (Jul'26)** run-rate; investors project $100–120B by end-2026.
- **$517B compute commitments / 14.8GW** (11 months); pays SpaceX $15B/yr.
- Reference: **SpaceX IPO 12 Jun 2026, $1.77T, largest ever at the time; fell ~50% by late Jul**.
- DoD "supply chain risk" label + litigation (the bear case).

## VO — the pluggable-TTS lesson

- **First attempt: OmniVoice zero-shot** clone of `female-medium-pace.m4a` → **word-salad audio**.
  Root cause: the old script hardcoded a `REF_TEXT` that belonged to a *different* voice; the
  mismatched transcript garbled the clone. Whisper confirmed: "kebunyi temin", "ngai naman banun".
- **Fix: Piper `id_ID-medium`** (trained Indonesian TTS, no reference needed) → clean audio.
- **Then made both runners pluggable** so this can't recur and nothing gets re-coded:
  - `scripts/tts_piper.py` + `scripts/tts_omnivoice.py` now read `tts-lines.json` /
    `tts-knobs.json` / `ref-voice.m4a` + auto-paired `ref-voice.srt` — **never edited**.
  - New doc: [`.docs/04-tts-voice-playbook.md`](04-tts-voice-playbook.md).
  - `voices/` now ships a matching `.srt` per `.m4a` (user-provided).

## Render + verify

- `hyperframes check` → **0 errors** (11 structural warnings: `nested_structure_needs_subcomposition`,
  `composition_file_too_large` — same class the Purbaya run accepted for a single-file comp).
- Rendered via backgrounded `npm run render` (survived shell exit), 72.0s, ffprobe-verified.
- **Open `renders/contact_sheet.png` to verify frames by eye.**

## Numbers-safe rules (for next run)

- TTS numbers: natural form ("65 miliar"), never spelled-out words.
- Piper outputs 22050 Hz int16 → resample to 24 kHz before HyperFrames audio slots.
- Facts: keep the "$2T is a rumor" framing front-and-center — it's the honest anchor.
