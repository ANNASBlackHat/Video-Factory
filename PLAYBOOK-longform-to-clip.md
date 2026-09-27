# 🎬 Video Production Playbook — Learned from the SWAP IPO Run

**Built:** Aug 27, 2026 · Three 63s vertical videos (ipo-crime-desk, ipo-ticker-shock, ipo-paper-trail) · All lint-clean, all facts sourced.
**Updated:** Aug 29, 2026 · Run #2 (karhutla-gambut, 2:36 with word-timed VO) validated the pipeline; new lessons added to §2a and §4.

This document makes run #2 faster and better than run #1. It captures what worked,
what broke, exact SFX recipes, this machine's quirks, and a prioritized backlog.

---

## 1. Where things live

| Path | What |
|---|---|
| `videos/ipo-crime-desk/` | Concept A: dark broadcast investigation (frame.md + STORYBOARD.md + frozen recipe `market-crime-desk`) |
| `videos/ipo-ticker-shock/` | Concept B: trading-terminal data overload (frozen recipe `ticker-shock`) |
| `videos/ipo-paper-trail/` | Concept C: bright editorial paper trail (frozen recipe `paper-trail`) |
| `scripts/gen-sfx-library.sh` | 19-sound offline SFX generator (`./gen-sfx-library.sh <dir>`) — **verified working** |
| `<project>/.media/recipes/<name>/` | Frozen recipes (design spec + storyboard skeleton + brief skeleton) |
| `<project>/assets/{img,audio}/` | Per-project copies of source assets |

**Recall:** next time say *"make another market-crime-desk"* / *"like last time"* — the intent layer finds the matching recipe and starts pre-filled (structure kept, content blanked).

## 2. The proven pipeline (do this order)

1. **Research folder is the contract.** Voiceover = timing truth; ASS/SRT captions = cue map
   (fix transcription errors first: "UJM"→UGM etc.); research MD = fact source;
   `ASSETS_INDEX.md` table = asset→scene role mapping.
2. **Scene map before HTML.** Convert caption timings into scene blocks with per-shot
   windows `[start–end]`, one line each. ~2.2–2.5s average shot for fast pace.
3. **Scaffold 3 concepts in parallel**: `npx hyperframes init videos/<name>
   --non-interactive --example=blank --skill=general-video` → write `BRIEF.md` immediately.
4. **Dispatch one builder agent per concept simultaneously**, each with the FULL
   self-contained packet: technical contract (root attrs, paused timeline on
   `window.__timelines["main"]`, clip conventions, bundled-fonts-only list, overflow attr),
   complete scene map, asset manifest with usage rules, SFX recipes, validation command.
5. **Verify independently after agents finish** — never trust agent self-reports alone:
   rerun lint yourself, grep for fabricated facts vs source docs, check every asset path.
6. **Check → Studio preview → user approval → render.**

### 2a. Word-level VO timestamp workflow (when using recorded voiceover)

When the research contract includes a voiceover WAV plus a word-timestamp JSON
(e.g. from Whisper), the transcript is the timing truth — but it is NOT the copy
truth. It always mishears some words, especially numbers and foreign terms
(run #2: "empat setengah"→"M4", "disemprot"→"disemperot").

1. **Verify the transcript against the final script BEFORE storyboarding.** Build a
   correction table (heard → correct → timestamp) and put it in the project BRIEF.
   Storyboard captions and on-screen text must use the *corrected* words, while cuts
   and animation sync use the *original timestamps*.
2. **Numbers get double-checked in both directions**: transcript→script (what was
   actually said) and script→facts (what was actually meant). A misheard number in
   VO is a fact-lock violation you can't grep for.
3. **Cut per word, not per line.** Word timestamps let every shot boundary land
   exactly on a spoken word — far tighter than estimating from caption lines.
4. If the VO was recorded from a script, include that script with the WAV so the
   correction table is small; if VO was improvised, budget extra review time.

## 3. Hard-won rules (violated once each — don't again)

- ⚠️ **Builder agents invent plausible-looking company names.** One wrote "PT GAMACHA
  MULTITECHNO FYSTA TBK". Every dispatch MUST include a **facts lock block** (real issuer,
  ticker, dates, numbers) plus the rule "never invent names/numbers not in this packet".
  Post-build factual audit against the source MDs is mandatory.
- ⚠️ Agents can die mid-task (auth blips, context limits). Verify artifacts exist ON DISK,
  not just their completion message. Re-dispatch a *continuation* agent describing exactly
  what exists and what's missing (that flow worked perfectly for the half-built paper-trail).
- ⚠️ Single-file compositions hit lint warnings (~600+ lines: track density, file size).
  Acceptable trade-off for audio-sync simplicity in v1 — see backlog §7 to fix properly.
- ✅ Retroactive `frame.md` (design system) + `STORYBOARD.md` make projects resumable AND
  freezable as recipes. Write them from the start next time (init creates neither).

## 4. Machine ops - THIS workstation (16GB Intel Iris Mac)

- Node >=22 required for hyperframes CLI. Default shell node is v20. In non-interactive
  shells 'nvm use' breaks in subshells - export absolute PATH instead:
  export PATH=~/.nvm/versions/node/v24.18.0/bin:$PATH
- run_commands kills children at 30s. Long tasks: nohup bash -c '... > log 2>&1; echo EXIT=$? >> log' &
  then poll the log in separate calls.
- hyperframes check gets OOM-killed (SIGKILL/137) on 63s 1080x1920 compositions when
  Chrome/VS Code/MCP servers also run. Rules: ONE check at a time; pkill -9 -f
  chrome-headless-shell before starting; if it dies twice -> fall back to lint + asset-ref
  audit + user Studio preview (honest handoff beats thrashing the machine).
- Useful: check --snapshots --at t1,t2,... saves PNG stills for visual self-QA BEFORE handoff (use next time).
- ⚠️ **NEVER run a render in the foreground.** run_commands/timeout will kill it mid-way
  and you lose everything rendered so far (run #2: a 4,687-frame render died at 30s).
  Launch fully detached so it survives the shell session, then poll the log:
  `nohup bash -c 'cmd > /tmp/render.log 2>&1' &` (double-fork via a wrapper script if the
  direct nohup still gets reaped). Poll with `tail` in separate calls; verify the process
  is alive (`ps aux | grep hyperframes`) before assuming a stall.
- A finished render leaves no fanfare — confirm the output file exists on disk with the
  expected duration (ffprobe) before reporting success.

## 5. Offline SFX synthesis (zero-download sound design)

**Check existing before generating.** `ls videos/*/assets/audio/ 2>/dev/null` — if any project
has the full 19-file library, copy it: `cp -r videos/<existing>/assets/audio/ videos/<new>/assets/audio/`.
Regenerate only when no project has it:

Everything = sines/noise shaped by ffmpeg -f lavfi. Library script:
scripts/gen-sfx-library.sh <outdir> -> 19 sounds, 4 families:
- Impacts: deep_hit (55Hz exp decay), stamp_thud, strobe_hit (gated flicker)
- Whooshes/risers: whoosh_hard (pink-noise sweep), riser_tension (~3s ramp ending ON the slam),
  bass_riser (40-90Hz sub), soft_riser (editorial pivot)
- UI/data: ui_blip, confirm_click, tick_counter/tick_loop (odometers), typewriter_key, terminal_boot
- Alerts/paper: alarm_buzzer (two-tone siren), glitch_stutter, page_flip, paper_rustle,
  pen_scratch, seal_pop

Placement doctrine that worked: SFX at every scene boundary + every text/stamp slam +
counter spin; VO always dominant; bake loudness into generation (~peak -6 dBFS); overlapping
audio clips each get their own data-track-index to avoid lint warnings.
New sound = one ffmpeg filtergraph line, test standalone, add to library script.

## 6. Design-system quick reference (the three looks)

| | crime-desk | ticker-shock | paper-trail |
|---|---|---|---|
| BG | #0a0b0d | #061020 navy | #f6f3ec warm paper |
| Accents | blood red #e11d2e | neon green/red/amber | yellow/blue/forensic red |
| Display type | Archivo Black + Oswald | Inter Black + JetBrains Mono | Playfair Display 900 |
| Signature move | RED FLAG stamp slams | odometer P/E spin to 105x | torn pie-wedge flies to folder |
| Captions | Oswald 700 red-box 58px | Inter Black mono-tagged 56px | EB Garamond italic pills |

Fonts: ONLY pre-bundled set renders safely offline/deterministic (Inter, Roboto,
Montserrat/Poppins/Outfit/Nunito/Lato/Oswald at 400+700+900; League Gothic and Archivo
Black are 400-only; Playfair Display, EB Garamond, Space Mono, IBM Plex Mono,
JetBrains Mono, Source Code Pro, Noto Sans JP). Ref: hyperframes-creative/references/typography.md.

## 7. Backlog - next iteration (prioritized)

1. **Sub-composition split.** One index.html per video hits lint warnings (size, track
   density). Next time: compositions/frames/NN-*.html per scene, mounted via
   data-composition-src -> also enables parallel per-scene builder agents.
2. **Lottie / advanced motion.** User asked for lottiefiles in v1 and we didn't use any.
   Explore: hyperframes-registry blocks + Lottie-web via deterministic offline JSON assets
   (host .json locally, no runtime fetches) for liquid/organic flourishes neither CSS nor
   SVG strokes cover well. Test render-safety early (render-time network fetches banned).
3. **Snapshot contact sheet self-review.** check --snapshots or Studio poster sheet before
   handing off; review midpoints of every scene myself, not just lint green.
4. **Music bed + ducking.** VO-only felt slightly bare in gaps. Use media-use audio-duck.mjs:
   low ambient bed ducked under VO (-14 LUFS integrated for social platforms).
5. **Word-level karaoke captions.** Current caption pills are line-level. Transcribe with
   media-use transcribe.mjs for word timings -> highlight active word per hyperframes style.
6. **Hook A/B variants.** Render 2 alternate first-2s hooks per concept for TikTok testing;
   keep the body identical. Cheap retention experiments.
7. **Platform safe-zones pass.** Reserve bottom ~15% / right edge for platform UI overlap;
   verify no critical text in TikTok's interaction zones at check time (--caption-zone flag).
8. **Scripted asset capture.** Codify the chrome-devtools-mcp research workflow: screenshot
   pages -> auto-write ASSETS_INDEX.md rows (file/resolution/source/role). Research folder
   contract: voiceover.wav + captions + facts MD + assets/ + ASSETS_INDEX.md.
9. **Full check on quiet machine.** When RAM frees up: npx hyperframes check --snapshots
   per project (serial), resolve findings, THEN render.
10. **Render pipeline script.** One command to render all approved projects and verify
    output files exist with correct duration.

## 8. QA gates checklist (every run)

- [ ] **VO script passed `/yt-script`** before TTS: scored hook + retention beats, saved as
      `raws/<topic>/VO-SCRIPT*.md`. Raw LLM prose in `tts-lines.json` = AI-slop on air (README step 4)
- [ ] Factual audit: every number/name/date in composition greps true against source MDs
- [ ] No invented company names, tickers, figures (agent fact-lock prompt + post audit)
- [ ] All asset paths resolve (grep assets/img + assets/audio refs vs disk)
- [ ] VO clip present & 0 <= start; total coverage 0 -> duration, no dead air > 1s
- [ ] npx hyperframes lint exit 0
- [ ] Full-text captions synced, corrected language, >= 54px in lower-third zone
- [ ] Deterministic timeline (no Math.random / Date.now / network fetches)
- [ ] SFX present at boundaries; library script regenerates them byte-identical-ish
- [ ] check passes (when machine allows) -> Studio preview -> USER approves -> only then render

---
*Recipes frozen: market-crime-desk, ticker-shock, paper-trail (general-video, v1) · purbaya-investigasi, purbaya-stat-hit, purbaya-paper-trail (v2, 16 Sep 2026).*
*Next run: say "make another <recipe>" or "like last time".*

## 9. Purbaya Menkeu Reshuffle run (16 Sep 2026) — 3 concepts rendered

Research → assets → VO → 3 HyperFrames concepts, all 1080x1920, all facts-locked to `raws/purbaya-suahasil-menkeu/`.

| Concept | Project | Recipe | Duration | Notes |
|---|---|---|---|---|
| Investigasi (crime-desk, VO) | `videos/purbaya-menkeu-reshuffle/` | `purbaya-investigasi` | 92.5s | 6 scenes, VO-synced to `assets/vo/scene_1..6.wav`, 12 SFX |
| Stat-hit (ticker-shock) | `videos/purbaya-stat-hit/` | `purbaya-stat-hit` | 18s | unnarrated, 6 neon stat hits, tick-loop bed |
| Paper-trail (editorial) | `videos/purbaya-paper-trail/` | `purbaya-paper-trail` | 52s | warm paper, 5 beats, forensic stamps |

**Run specifics:**
- VO generated by user (Colab/omnitts); the 6 `scene_N.wav` durations drove the timeline (not the 65s target).
- Rendered with `npm run render` (background nohup), all 3 verified on disk with ffprobe.
- `npx hyperframes check` passed on all 3 pre-render (Video 1: 0 errors / 6 warnings; Video 2: 0/7; Video 3: 0/5).
- Facts lock lives in each `BRIEF.md` + `raws/purbaya-suahasil-menkeu/REPORT-POLICY-IMPACT-purbaya.md` §5.

**New lesson (§3 addendum):** un-bundled display fonts (Archivo Black, Playfair Display 900, EB Garamond) are on the 18-family embed list and render deterministically — no @font-face needed. Confirmed via `check` contrast pass on all 3.
