# Workflow — USS Cyclops Short ("The Ship That Wasn't Sunk by a U-Boat")

**Date:** 13–14 Sep 2026 · **Raw:** `raws/uss-cyclops/Dead_Reckoning_Ep1_USS_Cyclops_short_script.md`
**Target:** ~45–55s vertical (1080×1920), fast-paced. **VO delivered:** 53.71s. **Status:** Phases 0–6 ✅ — SHIPPED (master: `videos/cyclops-short/renders/cyclops-short_MASTER_1080x1920.mp4`).

> Instance of `00-workflow-template.md` (adapted: this is a **vertical Short**, cross-posting the 18:00–End
> "killed by her own physics" verdict — per channel brief §8 "clip verdict/reveal moments for Shorts").

## Phase status

| Phase | State | Notes |
|-------|-------|-------|
| 0 — Preflight & contract | ✅ | toolchain verified; footage-engine verified; contract files created |
| 1 — Script & facts lock | ✅ | 123 words timed; `DEAD_RECKONING_FACTS_LOCK.md` (16 facts, sourced to PDFs + episode) + timed TELEPROMPTER |
| 2 — VO + transcription (Colab) | ✅ | `voiceover.wav` 53.71s (OuteTTS 1B en-female-1-neutral) + `voiceover.wordtimes.json` (124 words); correction table: 1 fix (`avern@38.08`→Then) |
| 3 — Footage & assets | ✅ | 5 footage clips (incl. native vertical 1080×1920) + 11 public-domain stills; `ASSET-INVENTORY.md` full provenance |
| 4 — Storyboard & motion design | ✅ | `raws/uss-cyclops/STORYBOARD.md`: 25 shots cut-locked to word timestamps, forensic-board design system, 5 signature moves, SVG build spec, audio plan |
| 5 — HyperFrames build | ✅ | single `index.html` composition (1080×1920@30, 53.71s): 25-shot evidence-board, word-karaoke captions (corrected copy), 4 video slices, 35 audio elements, local GSAP vendored; `hyperframes check` passed |
| 6 — Validate & render (ffmpeg) | ✅ | 1612/1612 frames captured+validated (3m 9s); **master −14.26 LUFS / TP −1.00 dBTP** (two-pass loudnorm + 0.45dB trim); `renders/cyclops-short_MASTER_1080x1920.mp4` 17MB H.264/AAC 48kHz |

## Step-by-step log

### Phase 0 (13 Sep 2026) — Preflight
- **Toolchain:** Colab `whoami` OK (oauth2, annas.developer@gmail.com, scopes cloud-platform/colaboratory/email, 59m fresh). Node v22.23.2 (nvm) available; prior working runs pin **hyperframes@0.8.16**. ffmpeg-skill `doctor` OK (62 caps, 0 required missing).
- **Footage-engine MCP:** config `~/.cline/data/settings/cline_mcp_settings.json` (`footage-engine` stdio local = available/running; `footage-engine-qwen` remote SSE = **down HTTP 400**). Engine verified working: semantic query returned real Pexels storm/ocean clips + fine-localized cut. Local DB sparse (2 samples) → target ingestion in Phase 3.
- **Contract skeleton:** created `assets-collected/{footage,images}/` + `ASSET-INVENTORY.md`.

### Phase 1 (13 Sep 2026) — Script & facts lock
- Extracted both research PDFs with `pypdf` (16-pg forensic + 9-pg blueprint) → sourced every fact.
- **Facts-lock** `raws/uss-cyclops/DEAD_RECKONING_FACTS_LOCK.md`: 16 facts (306 ppl, March 1918, USN collier AC-4, 10,800 LT manganese ore, ~5× denser than coal [derived], one broken engine 14.6→8–10 kt, Plimsoll submerged at Bridgetown, zero subs west of 40th meridian, U-151 May 15, no claimed kill, Force 8–10 gale Mar 9–10, PROBABLE ~75%, sister ships Proteus/Nereus). Route/timeline + build-time audit rule included.
- **Teleprompter** `Dead_Reckoning_Short_TELEPROMPTER.md`: 123 spoken words; HOOK/TURN/REVEAL/VERDICT/CTA + per-beat on-screen direction, fact-keyed.
- ⚠️ **Risk:** F8 "5× denser" is derived (~4.5 vs ~0.9 t/m³) — phrase as script wording, don't sharpen. F13 "no claimed kill" is E1-stated (R1 confirms no debris signature).

### Phase 2 (13 Sep 2026) — VO + transcription (Colab)
- **OuteTTS** (`edwko/OuteTTS` v1.0, `Llama-OuteTTS-1.0-1B`) on a **Colab T4 GPU** session `cyclops-tts`. Installed `outetts` + `faster-whisper`; fixed a `google.protobuf.runtime_version` ImportError (upgraded protobuf).
- **Voice:** `en-female-1-neutral` (only bundled English default). ⚠️ The `voices/` references are **Indonesian** (OuteTTS transcribed slow-pace sample as Indonesian) — rejected for English VO; used neutral English default instead.
- Generated `raws/uss-cyclops/voiceover.wav` — **44.1kHz mono, 53.71s** (mean −19.7dB). Numbers clean in transcript (`306`, `1918`).
- Transcribed on-VM with faster-whisper `small` → `voiceover.wordtimes.json` (124 words, word-level).
- **Correction table** `DEAD_RECKONING_VO_CORRECTION.md`: 1 fix (`avern`@38.08 → "Then"); all numbers verified; real beats HOOK 0–11.6 / TURN 11.6–21.84 / REVEAL 21.84–40.08 / VERDICT 40.08–48.4 / CTA 48.4–53.71.
- `colab stop -s cyclops-tts` — session terminated, no active sessions (units safe).

### Phase 3 (14 Sep 2026) — Footage & assets
- **Footage-engine** semantic search (Pexels + fallback) returned real stock clips; downloaded **5 candidates** → `assets-collected/footage/`: `storm_vertical_1080x1920` (native vertical, 16s — hook/gale hero), `storm_1920x1080_A`, `storm_720_A`, `navy_1920x1080`, `ore_crane`. Short cuts only.
- **Stills (public domain)** via Wikimedia Commons + NARA/NHHC → `assets-collected/images/`: actual USS Cyclops photo, AC-4 hull plans, crew, Proteus/Nereus (sister ships), WWI U-boat raid + Stöwer painting (hook), manganese ore + NARA coal pile (ore-vs-coal), Courbet + Ślewiński paintings (gale).
- Downscaled all oversized images (≈300MB → ≈5MB). No raster images in the research PDFs (vector/text).
- Wrote `ASSET-INVENTORY.md` (provenance + license + beat→asset map + source cards).
- **Open:** (1) March-1918 storm-track map not located as clean raster (optional); (2) ore-vs-coal "5× denser" graphic → SVG in Phase 4; (3) user's own footage (option b) not yet provided — can drop into `assets-collected/footage/` later; (4) I cannot view frames — **eyeball footage at Phase 4/6**.


### Phase 4 (14 Sep 2026) — Storyboard & motion design
- **Deliverable** `raws/uss-cyclops/STORYBOARD.md` — forensic **evidence-board** concept ("the board is the world").
- **25 shots / 53.71s** (avg 2.15s, max 3.24s), every cut pinned to a `voiceover.wordtimes.json` word-start: H1–H6 / T1–T5 / R1–R8 / V1–V4 / C1–C2. Hard cuts + 0.22s whip-pans; every still gets push/punch; footage only as ≤2.5s slices (user rule: no full-length footage).
- **Design system:** charcoal palette (`#101218` board, ember `#FF5A1F`, alarm `#E11D2E`, amber `#FFC233`, cold `#3EC6C0` sea-only); Archivo Black (400) display / Oswald 700 tags+captions / JetBrains Mono data with tabular-nums — all pre-bundled fonts.
- **Captions:** word-level karaoke, Oswald 64px, ember active word, bottom-15% safe zone (≥288px), corrected copy (`avern`→Then).
- **Signature moves:** evidence-tag flip (WAR THEORY→DISPROVEN, 3D Y-rotate) · coal-vs-ore density bar (SVG, ore fills 5×) · Plimsoll/waterline rise · PROBABLE stamp slam (music drop-out 1 beat before) · source-card row.
- **Phase 5 build spec:** 8 in-DOM SVG/DOM graphics (evidence-tag, density-bar, engine-schematic, hull-plimsoll, atlantic-map, stamps, source-card-row, end-card); SFX at all 24 cut boundaries; bed −3–4 dB duck; master −14 LUFS in Phase 6.
- **Handoff notes:** storm vertical (16s) sliced from different in-points (R8 hero, V1/V2 backdrop); numerals grep-locked to facts lock; sister-ship F16 + storm-map stay cut (runtime protection).

### Phase 5 (15 Sep 2026) — HyperFrames build
- Scaffolded `videos/cyclops-short/` (init, general-video contract files); `BRIEF.md` written immediately (concept, facts rules, audio plan, correction table).
- Built single-file composition `index.html`: #root 1080×1920@30, **53.71s**, one paused GSAP timeline (`window.__timelines["main"]`), all 25 shots from STORYBOARD.md with clip `data-start/data-duration/data-track-index` lanes (video 10 / SFX 12 / VO 10 / bed 11 convention: VO+bed track 10/11, SFX 12).
- **Video handling:** no `data-media-start` support in 0.8.36 → pre-sliced sources with ffmpeg (`stormV` takes at 0s/10s + navy at 5s as separate files in `assets/vid/`); all 4 slices ≤2.5s per user rule.
- **SVG graphics built in-DOM:** evidence-tag 3D flip (WAR THEORY→DISPROVEN), coal-vs-ore density bar (ore 5× taller), engine schematic (starboard crack + dead rotation), hull/Plimsoll waterline rise, Atlantic route map (dash-draw + meridian), stamps, source chips, end card. Board texture = radial-gradient + CSS grid (no bitmap).
- **Captions:** word-level karaoke from `voiceover.wordtimes.json` inlined as JS array, 58px Oswald pills, bottom 320px (safe zone), active word ember; corrected copy (`avern`→Then).
- **Audio:** VO + dark bed (0.55) + 33 SFX cues on cut boundaries (deep_hit/stamp/whoosh/tick/sonar/riser/water/thunder/paper/click).
- **Gotchas solved:** GSAP vendored locally (`assets/vendor/`) — CDN fetch unreliable in check; eyebrow contrast fixed with scrim pill (1.32→≥3:1); caption panels clipped to canvas (padding+margin pattern); Ken Burns bleed marked `data-layout-allow-overflow`.
- **Gate:** `npx hyperframes@0.8.36 check` (Node 22) → **passed**: layout 0 err / motion 0 err / contrast 0 err (after fixes).

### Phase 6 (15 Sep 2026) — Validate & render
- `hyperframes render` → **1612/1612 frames** captured (beginframe mode, GPU hw), coverage validated, 4/4 video extracts consumed, in 3m 9s → `renders/cyclops-short_2026-09-15_13-13-08.mp4` (1080×1920, 30fps, AAC 48k stereo, 53.73s).
- **Loudness master:** measured −16.28 LUFS / TP −1.03 → two-pass `loudnorm` linear (video `-c:v copy`) → −14.69 → +0.45 dB trim → **final −14.26 LUFS / TP −1.00 dBTP** (measured, not estimated).
- **Deliverable:** `videos/cyclops-short/renders/cyclops-short_MASTER_1080x1920.mp4` (17 MB, H.264 High + AAC 192k). Spot-frames extracted at 0.8/11.8/27.6/36.2/42.9/52.8 confirmed signature beats render as designed.
- Keyframes extracted to `/tmp/cycq/` for review (transient).
