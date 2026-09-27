---
workflow: general-video
flow: automation
storyboard: yes
message: "The USS Cyclops wasn't sunk by a U-boat — it was killed by its own physics"
destination: youtube-shorts
aspect: 1080x1920
language: en
length: 53.71s
angle: concept
---

## Intent
Dead Reckoning Ep1 — a forensic evidence-board short re-opening the 1918 USS Cyclops case.
Register: investigator, restrained and precise (never "terrifying mystery" hype). 53.71s
VO-locked vertical Short for YouTube, cross-posted. Verdict is honest: PROBABLE (~75%),
wreck never found.

## Assets (staged → `assets/`)
- `assets/audio/voiceover.wav` — VO truth, 53.71s, 44.1kHz mono; `raws/uss-cyclops/voiceover.wordtimes.json` = word timing truth (124 words).
- `assets/img/uss_cyclops_19N13451.jpg` — hero ship photo (HOOK H1–H2)
- `assets/img/uss_cyclops_plans_NARA.small.jpg` — hull plans (H2 layer)
- `assets/img/stower_sinking_linda_blanche.jpg` — U-boat painting (H5–H6)
- `assets/img/manganese_ore_rock.jpg` — ore punch-in (R2)
- `assets/img/uss_cyclops_crew_righting_arms.small.jpg` — crew (R1)
- `assets/img/courbet_storm_wave.jpg` — wave loom (R7)
- `assets/vid/storm_vertical_1080x1920.mp4` — 16.0s native vertical; R8 hero slice + V1/V2 backdrop slice (DIFFERENT in-points)
- `assets/vid/navy_1920x1080.mp4` — V3 1.8s slice (dimmed)
- Full manifest + provenance: `raws/uss-cyclops/ASSET-INVENTORY.md`

## Customizations
- Full storyboard with cut-locked shot map: `raws/uss-cyclops/STORYBOARD.md` (25 shots, H1–H6/T1–T5/R1–R8/V1–V4/C1–C2, every cut pinned to a word timestamp).
- Signature moves: evidence-tag 3D flip (WAR THEORY→DISPROVEN), coal-vs-ore density bar (ore 5× taller), Plimsoll/waterline rise, PROBABLE stamp slam, source-card row.
- Word-level karaoke captions (Oswald 700 64px, ember active word, bottom ≥288px safe zone).
- SFX at every shot boundary (24 cuts); music bed ducked under VO; master −14 LUFS (Phase 6).

## Notes
- FACTS LOCK: `raws/uss-cyclops/DEAD_RECKONING_FACTS_LOCK.md`. On-screen numerals ONLY: 306, 1918, MARCH 1918, ZERO, 40TH MERIDIAN, 5×, 1 OF 2, FORCE 8–10, ~75%. Nothing else.
- Timing truth ≠ copy truth: captions use corrected copy (`avern`@38.08 → "Then"); cuts use raw word times (`raws/uss-cyclops/DEAD_RECKONING_VO_CORRECTION.md`).
- User rule: NO full-length footage — stills get push/punch motion; footage only ≤2.5s slices.
- Fonts pre-bundled only: Archivo Black (400), Oswald (400/700), JetBrains Mono (400/700).
- Palette: board #101218, panel #1B1E27, line #2A2E3A, bone #E9E6DE, dim #8B8FA0, ember #FF5A1F, alarm #E11D2E, amber #FFC233, cold #3EC6C0 (water only).
- Runtime protection: sister-ship beat (F16) and storm-track map stay CUT.
- Design/motion doctrine: `raws/uss-cyclops/STORYBOARD.md` §1–§3 (rhythm, design system, shot map).
