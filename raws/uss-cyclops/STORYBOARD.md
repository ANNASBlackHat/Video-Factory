# STORYBOARD — "The Ship That Wasn't Sunk by a U-Boat" (Dead Reckoning Ep1)

**Phase 4 deliverable · Format:** 1080×1920 vertical · **Runtime:** 53.71s (VO-locked) · **Shots:** 25 (avg 2.15s, max 3.24s)
**Concept:** a **forensic evidence board** that re-opens a 1918 case file on camera. The board is the world: pinned photos, paper tags, stamped verdicts. Every shot is a *move on the board* — a tag flips, a stamp slams, a line is drawn. Nothing idles.
**Timing truth:** every cut below is pinned to `voiceover.wordtimes.json` (word timestamps), not prose. Cut = the frame where the cue word *starts* unless noted.
**Facts-lock rule:** on-screen numerals ONLY from `DEAD_RECKONING_FACTS_LOCK.md` → `306 · 1918 · MARCH 1918 · ZERO · 40TH MERIDIAN · 5× · 1 OF 2 · FORCE 8–10 · ~75%`. Nothing else.

---

## 1 · Rhythm plan (name it before you build it)

```
HOOK   : SLAM — push — pop — pop — (U-boat menace) — WRONG        ← peak 1
TURN   : paper — stamp — ZERO — map — FLIP                        ← peak 2
REVEAL : sweep — PUNCH — BUILD(5×) — snap — drop — DROP — drift — CRASH ← peak 3 (gale)
VERDICT: hold — STAMP — cut — SLAM                                ← peak 4 (verdict)
CTA    : settle — hold                                            ← exhale
```
**Peaks (visual + audio coincide):** WRONG @11.6 · ZERO @16.36 · 5× bar fills @27.3 · GALE crash @40.08 · PROBABLE stamp @42.64 · "own physics" @48.4.

## 2 · Design system

### Palette — charcoal forensic board, ember/alarm accents
| Token | Hex | Role |
|---|---|---|
| `board` | `#101218` | board base (near-black charcoal) |
| `panel` | `#1B1E27` | evidence cards / photo mats |
| `line`  | `#2A2E3A` | board grid, pin lines, hairlines |
| `bone`  | `#E9E6DE` | primary text (aged paper white) |
| `dim`   | `#8B8FA0` | mono metadata, secondary |
| `ember` | `#FF5A1F` | accent: active caption word, ore/heat, "306" |
| `alarm` | `#E11D2E` | WRONG · DISPROVEN · PROBABLE stamps, X-out |
| `amber` | `#FFC233` | theory tags under review (U-BOAT?, WAR THEORY) |
| `cold`  | `#3EC6C0` | water/sea only: Plimsoll + gale beats (motif = the sea kills, not war) |

### Typography (all pre-bundled — no fetch risk)
- **Display / numerals / stamps:** `Archivo Black` (**weight 400 only**) — `306`, `ZERO`, `WRONG`, `PROBABLE`, `5×`
- **Tags / captions / eyebrows:** `Oswald 700` — evidence tags, karaoke captions, section slugs (tracking +0.04em, uppercase)
- **Data / metadata:** `JetBrains Mono 400/700` — timestamps, citations, "WEST OF 40TH MERIDIAN", source cards · `font-variant-numeric: tabular-nums` on every counter

### Captions — word-level karaoke, lower third
- Oswald 700, **64px** (≥56px floor), bone; **active word = ember**, past words dim 55%.
- Pill on `panel`/85% with 1px `line` border; centered; **bottom edge no lower than 15% of frame height (≥288px from bottom)** — Shorts UI safe zone.
- Caption text uses **corrected copy** (`DEAD_RECKONING_VO_CORRECTION.md`: `avern`→"Then"); cut sync uses raw word times.

### Camera & motion doctrine (user note: *no full-length footage — cut short + move everything*)
- Every still gets a **push/pull (Ken Burns) or punch-in** — no still sits static; every footage use is a **0.6–2.5s cut**, never a full clip.
- Transitions: **hard cuts** at evidence rhythm; **whip-pan (0.22s, blur ramp)** when the board re-aims (R1 sweep, R8 crash, V3 cut); velocity-matched exits (power3.in) → decel entries (power3.out).
- Nothing static >3.5s (verified: longest shot R3 = 3.24s and it's a continuous bar build).


## 3 · Shot map — every cut pinned to a word timestamp

> **Cue column** = the spoken word that *triggers* the cut (time = word **start** in `voiceover.wordtimes.json`).
> **Visual** = primary asset from `ASSET-INVENTORY.md`. **Motion** = verbs (beat-direction doctrine). **SFX** = one-shot library.

### BEAT 1 · HOOK — "the case opens" (0.00–11.60)
| # | window | cue @ | visual | motion | SFX |
|---|--------|-------|--------|--------|-----|
| H1 | 0.00–2.14 | **306** @1.04 | `uss_cyclops_19N13451.jpg` full-bleed, slow push 1.05→1.12; eyebrow `USS CYCLOPS · MARCH 1918` | BLACK→board fade 0.2s; **"306" Archivo Black 340px ember SLAMS** @1.04 (scale 1.5→1.0 overshoot, board shake 6px) | sub-boom + stamp thud @1.04 |
| H2 | 2.14–4.76 | *vanished* @2.14 | same photo drifts; `uss_cyclops_plans_NARA.small.jpg` slides up **under** it (parallax layer); mono `LAST SIGHTING: BARBADOS · MAR 4 1918` types on | blueprint rises behind photo (depth push), photo keeps 1.12 drift | paper slide + low drone |
| H3 | 4.76–6.42 | *no* @4.76 | evidence tag pops center: `NO DISTRESS CALL` (alarm border) | tag pops (scale 0→1 spring 0.18s) → **X strike-through swipes** (alarm, 0.18s) | rejection bwap |
| H4 | 6.42–7.92 | *no* @6.42 | second tag pops below: `NO WRECKAGE` (amber pin) | pin drop + 1px settle jitter; both tags stack on board | stamp thud |
| H5 | 7.92–10.18 | *everyone* @7.92 | board re-aims: `stower_sinking_linda_blanche.jpg` slides over photo; amber tag `U-BOAT?` pins top-right, "?" blinks ×3 | **whip-pan 0.22s** (blur ramp) → U-boat silhouette blooms (scale 1.06 drift) | sonar ping + klaxon swell |
| H6 | 10.18–11.60 | *wrong* @11.60 | hold U-boat image 1.4s → **"WRONG" Archivo Black 300px alarm SLAMS** over tag; tag snaps 2° | scale 1.6→1.0 slam, board shake 8px, 0.3s glitch RGB-split on exit | record-scratch + boom |

### BEAT 2 · TURN — "the records" (11.60–21.84)
| # | window | cue @ | visual | motion | SFX |
|---|--------|-------|--------|--------|-----|
| T1 | 11.60–14.36 | *German* @11.60 | paper card rotates in from −8°: `KTB · BDU WAR DIARIES` (JetBrains Mono 700) + ledger rows | card swings to 0° (spring), rows highlight sequentially | paper slide |
| T2 | 14.36–16.36 | *checked* @14.36 | card push-in (scale 1.0→1.14); stamp `POST-WAR REVIEW` ink-appears @14.36; `CHECKED ✓` @15.64 (*war*) | push + rubber-stamp press (rotate −4°→−2°) | stamp ding |
| T3 | 16.36–18.24 | *zero* @16.36 | **"ZERO" Archivo Black 360px bone SLAMS** @16.36; mono line `WEST OF 40TH MERIDIAN · MARCH 1918` types on beneath | slam + digits-flick-then-lock gag on the 0 | ticker + impact |
| T4 | 18.24–20.46 | *anywhere* @18.24 | Atlantic map card: route line Barbados→Baltimore **draws**, 40th-meridian line crosses frame, position dot pulses at Virginia Capes | line draw (dash-offset 1.2s), dot ping ripples ×2 | map ping ×2 |
| T5 | 20.46–21.84 | *kill* @20.46 | **SIGNATURE — evidence-tag FLIP:** amber tag `WAR THEORY` → Y-rotate 180° (0.45s) → alarm tag `DISPROVEN — NO CLAIM · NO SIGNATURE` | flip with backface reveal, 1px settle | whoosh + flip flap |

> **Carried fact-check:** all on-screen strings above grep to facts lock (F2/F3/F5–F11/F13). No invented numerals.


### BEAT 3 · REVEAL — "the physics" (21.84–40.08) — *the emotional core, most shots, fastest cuts*
| # | window | cue @ | visual | motion | SFX |
|---|--------|-------|--------|--------|-----|
| R1 | 21.84–25.14 | *so* @22.82 | board sweeps clear → `uss_cyclops_crew_righting_arms.small.jpg` rises with amber tag `SO WHAT ACTUALLY HAPPENED?` | **whip-pan 0.22s** into crew photo push-in 1.08; question tag pins | whip + riser |
| R2 | 25.14–26.56 | *carrying* @25.14 | `manganese_ore_rock.jpg` **PUNCH-in** on *ore* @26.14 (scale 1.25→1.0, 0.2s) — texture fills frame, ember grade | punch + brief chromatic pop | heavy rock thud |
| R3 | 26.56–29.80 | *five* @26.56 | **SIGNATURE — DENSITY BAR (SVG, built in-DOM):** hull cross-section, two cargo columns. COAL column fills bone 0.9-height → **ORE column fills ember 5× taller** (fills during *five…denser* 26.56–27.92); tick marks + mono `COAL · BUILT FOR` / `MANGANESE ORE · CARRYING`; on *denser*@27.34 a bracket snaps both, `5×` Archivo stamps right of bar | columns fill bottom-up (transform scaleY, staggered), bracket draws, stamp | tick ×5 + slam |
| R4 | 29.80–31.62 | *one* @29.80 | engine schematic SVG: `2` cylinders bone → starboard cylinder **cracks** (alarm crack line draws) @31.0 (*engines*); mono `1 OF 2 ENGINES · DISABLED` | crack draws, cylinder rotates 3° dead, red flicker ×2 | metal snap |
| R5 | 31.62–34.34 | *and* @32.36 | hull profile SVG: ore bricks **stack** into hold, hull visibly sinks against fixed waterline (water disc `cold`) | bricks drop-stack (0.1s stagger), hull sinks 8px, waterline static | creak + thuds |
| R6 | 34.34–37.48 | *waterline* @34.46 | **SIGNATURE — WATERLINE GRAPHIC:** close on hull side; Plimsoll disc + load line; `cold` water mask **rises past the mark** during *underwater* @35.84–36.42; disc submerges, `FULLY UNDERWATER` mono stamps | water rises (clip-path/transform), disc dips under with ripple ring | water swell |
| R7 | 37.48–39.52 | *Then* @38.08 (corrected copy) | ship silhouette drifts off-frame right; `courbet_storm_wave.jpg` looms from below (dark grade), wave curl rising | silhouette drift 1.0→1.15 exit, wave rises from bottom (parallax) | wind howl riser |
| R8 | 39.52–40.08 | *gale* @40.08 | **storm_vertical_1080x1920.mp4** native-vertical CUT (2.5s max slice) — wave crash frame timed so **impact lands ON *gale*@40.08**; mono `FORCE 8–10 · MAR 9–10 1918` slams bottom-left | hard cut, scale punch 1.1, white flash 2 frames on impact | thunder crack |

### BEAT 4 · VERDICT — "the ruling" (40.08–48.40)
| # | window | cue @ | visual | motion | SFX |
|---|--------|-------|--------|--------|-----|
| V1 | 40.08–41.70 | *probable* @42.64 | storm continues under rain (vertical clip, dimmed); mono line `CASE STATUS: ______` blinks like a terminal cursor @41.38 (*case*) | cursor blink ×3, text types on | UI tick |
| V2 | 41.70–43.94 | *probable* @42.64 | **SIGNATURE — PROBABLE STAMP SLAM:** `PROBABLE ~75%` Archivo alarm SLAMS (scale 2.2→1.0, 2-frame overshoot, 10px board shake) @42.64; music bed DROPS OUT 1 beat before; hold on stamp | slam + settle, rain continues behind (dim 40%) | heavy stamp + reverb tail |
| V3 | 43.94–46.42 | *She* @43.94 | navy footage `navy_1920x1080.mp4` 1.8s cut (dimmed, wartime mood); alarm `✕ NOT WAR` swipes across @45.16 (*war*) | **whip-pan 0.22s** in; X-swipe + slug | whoosh + slice |
| V4 | 46.42–48.40 | *killed* @47.02 | BLACK; signature line builds word-by-word: **"KILLED BY HER OWN PHYSICS"** — `HER OWN` ember @48.0, `PHYSICS` full-alarm @48.40 (*physics*) | kinetic word build (each word pops 0.9→1.0, 0.12s stagger) | deep boom per word |

### BEAT 5 · CTA — "the case file" (48.40–53.71)
| # | window | cue @ | visual | motion | SFX |
|---|--------|-------|--------|--------|-----|
| C1 | 48.40–50.96 | *full* @49.40 | end card on board texture: `DEAD RECKONING` Archivo + `EP 1 · USS CYCLOPS` Oswald; case-file tab graphic slides in from left | card assembles (tab slides, title rises 20px, 0.3s) | drawer slide |
| C2 | 50.96–53.71 | *linked* @52.64 | source-card row pins bottom (JetBrains Mono chips): `NHHC · USN POSTWAR REVIEW · US WEATHER BUREAU MAR 1918`; ember pill `FULL CASE FILE ↓ LINKED BELOW` snaps on @52.64; **hold to 53.71** (longest safe hold, end card is allowed to breathe) | chips cascade in 0.06s stagger, pill scale-pops, subtle board breathing (1.0→1.02 loop, 4s) | soft thud + music resolve |

## 4 · SVG/DOM graphics to author in Phase 5 (no external image needed)
| Asset | Build spec |
|---|---|
| `evidence-tag` | paper tag (panel bg, line border, pin dot), 3D flip (rotateY) amber→alarm states |
| `density-bar` | two-column hull cross-section SVG; scaleY fill, tick marks, `5×` bracket |
| `engine-schematic` | 2-cylinder SVG, crack line draw path, dead-cylinder rotation |
| `hull-plimsoll` | hull profile + load-line disc; water mask rise via transform, ripple ring |
| `atlantic-map` | simplified coastline SVG, dash-offset route draw, meridian line, ping dot |
| `stamps` | reusable Archivo stamp (−8° rotate, 2-frame overshoot, optional shake) |
| `source-card-row` | mono chip strip; staggered pin-in |
| `end-card` | episode slug + case-file tab + CTA pill |

## 5 · Audio plan (Phase 6)
- VO full-length, single track. Music bed: dark investigative pulse, duck −3–4 dB under VO, risers into R1 & V2, **hard drop 1 beat before PROBABLE @42.64**, resolve at CTA.
- SFX at **every shot boundary** (24 cuts) from the one-shot library (stamps, paper, whoosh, ticks, thuds, water, thunder).
- Master: −14 LUFS integrated (ffmpeg loudnorm in Phase 6).

## 6 · Phase 4 → 5 handoff notes
- Longest static hold = 3.24s (T1→T2 continuous card move — counts as one move, compliant). All footage uses are ≤2.5s slices. ✅ user's "no full-length footage" rule.
- storm vertical clip is 16s → use only slices: R8 (≈2.5s), V1/V2 backdrop (dimmed, 2.7s), sourced from *different* in-point each time.
- Karaoke captions: word-level from `voiceover.wordtimes.json`, corrected copy (`avern`→Then), Oswald 64px, ember active word, bottom-15% safe zone (≥288px).
- Every numeral greps to `DEAD_RECKONING_FACTS_LOCK.md` — Phase 5 lint re-audits.

