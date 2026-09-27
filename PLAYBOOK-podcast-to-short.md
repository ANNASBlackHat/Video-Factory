# Podcast-to-Viral-Short Workflow

Reusable reference for cutting a viral vertical short from a long Indonesian podcast/interview.
**Last updated:** 2026-09-13 | **Source material:** YouTube podcast with transcript

---

## Quick Start (what to tell the agent)

> Read `PLAYBOOK-podcast-to-short.md`. Here's my folder path:
> `raws/<name>/` — it has an `.mp4` and a transcript `.txt`. Make a 60-90s viral vertical short.

That's it. The agent handles everything below.

---

## Folder Structure Expectation

```
raws/<name>/
├── *.mp4                    # source video (YouTube-dl or similar)
├── *.txt                    # transcript (NoteGPT format, or any timestamped text)
└── video_visual_explainer.md # [OPTIONAL but very valuable] visual log per timestamp
```

**video_visual_explainer.md** is critical. It maps timestamps to what's actually ON SCREEN (documents, IR footage, slides, logos) — not just what's being said. The transcript tells you the words; this tells you the visuals. Without it, you're guessing which timestamps have usable B-roll.

If only a transcript exists, ask the agent to extract the file first and probe key timestamps for visuals. But `video_visual_explainer.md` saves a LOT of time.

---

## Step-by-Step Pipeline

### 1. Reconnaissance (2-3 min)

```bash
# Get video specs
ffprobe -v error -show_entries format=duration,size,bit_rate \
  -show_entries stream=width,height,avg_frame_rate,codec_name \
  -of default=noprint_wrappers=1 "raws/<name>/<file>.mp4"

# Parse transcript for viral keywords
python3 -c "..."  # grep for: nuklir, alien, ufo, space force, area 51, roswe, disclosure

# Read video_visual_explainer.md if it exists
```

**What to look for:**
- Video duration → how much material to cut from
- Transcript language → subtitle language decision
- Visual timestamps → which moments have native B-roll vs talking head only

### 2. Content Selection (decide the angle)

Find the strongest 60-90s segment. Viral hooks for this genre:

| Hook Type | Example | Why it works |
|-----------|---------|--------------|
| Government proof | "162 files released on war.gov" | Authority + conspiracy |
| Military footage | "Missile bounced off UFO" | Visual shock |
| Impossible tech | "90-degree turn without radius" | Defies physics |
| Existential | "Aliens + humans coexisting by 2027" | Future fear |

Pick ONE angle. Don't try to fit everything in.

### 3. B-Roll Strategy (this is the key trick)

**The single biggest improvement over naive podcast clips:** extract B-roll from DIFFERENT timestamps of the same source video.

```bash
# Extract native B-roll clips from key visual moments
SRC="raws/<name>/<file>.mp4"
ffmpeg -y -v error -ss <start_seconds> -i "$SRC" -t <duration> \
  -c:v libx264 -preset fast -crf 20 -c:a aac -b:a 128k \
  assets/native-<topic>.mp4
```

**How to find the right timestamps:**
1. Read `video_visual_explainer.md` → find segments with on-screen evidence (news panels, IR footage, documents, logos)
2. Frame-probe those timestamps to verify:
   ```bash
   ffmpeg -y -v error -ss <t> -i "$SRC" -frames:v 1 check/t<t>.jpg
   ```
3. Look for frames that are: cinematic, proof-bearing, visually distinct from talking head

**B-roll priority:**
1. **Native source footage** (same video, different timestamp) — highest credibility
2. **News/document overlays** from the source — already produced by the podcast
3. **Stock footage** (Pexels/Pixabay) — only as last resort, or for atmospheric filler
4. **Google/Reddit screenshots** — for web-native evidence, requires chrome-devtools-mcp

**Footage Engine MCP** (`footage-engine`) can search Pexels/Pixabay/Coverr semantically:
```
queries: "UFO night sky", "military jet night", "pentagon building night"
```
But for this genre, native source footage > stock every time.

**chrome-devtools-mcp** is the fallback for finding online footage (screenshots, news clips from sites). Not used this run but available.

### 4. Source Cut + Audio Split

```bash
# Extract the dialogue segment (audio + video)
ffmpeg -y -ss <start> -i "$SRC" -t <duration> \
  -c:v libx264 -preset fast -crf 20 -c:a aac -b:a 160k \
  assets/dialogue-<times>.mp4

# Extract audio only (for the final mux)
ffmpeg -y -i assets/dialogue-<times>.mp4 -vn \
  -c:a aac -b:a 160k assets/dialogue-<times>.m4a
```

**Keep the audio clean.** The dialogue audio runs the full duration — you're cutting visuals around it, not the other way around.

### 5. Scaffold Project

```bash
npx hyperframes init "videos/<name>" --non-interactive --example=blank --skill=general-video
```

**GOTCHA:** If the directory already exists and has files, move assets aside first:
```bash
mv videos/<name>/tmp/assets-backup && npx hyperframes init ... && mv tmp/assets-backup videos/<name>/assets
```

### 6. BRIEF.md + Composition

Write `BRIEF.md` at project root. Then write `index.html` with:
- 9:16 canvas (1080×1920)
- Muted video elements with `data-start`, `data-duration`, `class="clip"`
- Separate `<audio>` element for the dialogue track
- GSAP timeline registered on `window.__timelines["main"]`
- Caption rail (bottom, ~5% height, overlay — NOT a reserved band)
- Embed peaks (max 2, behind the action, scarce)

**Layout for talking head + B-roll:**
- **Talking head:** blur-background + fit-width center (don't crop face!)
- **B-roll:** full-bleed cover with `object-fit: cover`
- **Captions:** overlay on top of everything, bottom ~190px from bottom

**Key CSS pattern:**
```css
.fitwrap { position: absolute; left: 0; width: 1080px; top: 656px; }
.fitwrap video { width: 1080px; height: 608px; object-fit: fill; }
.covervid { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.blurbg { filter: blur(48px) brightness(0.55); }
```

### 7. Verify + Render

```bash
npm run check          # lint + runtime + layout + motion + contrast
npm run render         # render to MP4 (takes ~8-10 min for 78s)
```

**GOTCHA — node version:** HyperFrames requires node ≥ 22. If default is v20:
```bash
export NVM_DIR=~/.nvm; source ~/.nvm/nvm.sh >/dev/null 2>&1; nvm use 22.23.2
```

**GOTCHA — render timeout:** Default tool timeout is 120s. Renders take 8+ min. Use background-safe approach:
```bash
nohup npm run render > /tmp/render.log 2>&1 < /dev/null &
# poll for completion
sleep 300; tail -n 5 /tmp/render.log
```

**GOTCHA — video nested in timed element:** Don't put `data-start` on both a wrapper `<div>` and the inner `<video>`. The frame extractor uses the video's own `data-start` without the wrapper offset. Fix: put `class="clip" data-start="..."` directly on the `<video>`, not the wrapper.

**GOTCHA — GSAP on clip wrappers:** Don't animate visibility (`autoAlpha`) on wrapper divs that have `data-start`. Animate the content inside them, or use separate non-clip wrapper for transforms.

---

## Difficulties Encountered & Solutions

| Difficulty | Solution |
|-----------|----------|
| `video_visual_explainer.md` timestamps drift 12-40s vs actual mp4 | Always frame-probe key moments; never trust timestamps blindly |
| footage-engine MCP not in available tools | It's configured in `opencode.json` but not as a callable tool in this session. Fall back to direct Pixabay/Pexels API via Python scripts in the footage-engine repo |
| `npx hyperframes init` fails on non-empty directory | Move existing files aside, init, move them back |
| Render hangs at tool timeout (120s) | Background the process with `nohup` + poll |
| Node v20 vs required v22 | Use `nvm use 22.23.2` before any npx hyperframes command |
| `check` fails: `video_nested_in_timed_element` | Put `data-start` on the `<video>` directly, not on wrapper divs |
| `check` fails: `media_missing_data_start` | Every `<video>` with `src` needs `data-start` and `data-duration` |
| IR footage shows slide instead of raw footage | Adjust `data-media-start` offset on the video element to skip past slides |
| Stock footage feels generic for conspiracy content | Native source footage (from different timestamps) >> stock for credibility |

---

## What to Improve Next Time

1. **More native B-roll.** Extract 5-8 clips from the source at different timestamps — hook, proof, NASA docs, IR cases, ending. This makes the short visually rich.
2. **Sound effects.** Tension bed music + whoosh/impact on transitions. Use `resolve --type sfx` or `resolve --type bgm` from media-use.
3. **Hyperframes animation blueprints.** Use cut-the-curve transitions, not just hard cuts. Load motion-doctrine + cut-the-curve skills.
4. **SRT generation.** Instead of manual rail timing, generate an SRT from the transcript timestamps and use it for caption sync.
5. **Stock for atmosphere.** For non-proof moments (intro tension, abstract space shots), stock UFO/night-sky footage can fill gaps.
6. **Chrome-devtools for web evidence.** Screenshot war.gov/UFO page, news articles, Reddit threads. Use chrome-devtools-mcp.
7. **Color grade / LUT.** Match the talking-head and B-roll color. Use media-treatments from media-use.
8. **Word-level transcript.** NoteGPT gives overlapping lines — a proper whisper transcript with word timestamps would make caption timing precise.

---

## File Locations (this project)

```
videos/alien-short/
├── BRIEF.md                          # intent doc
├── index.html                        # composition
├── hyperframes.json                  # project config
├── package.json                      # pins hyperframes@0.8.36
├── alien-short-9x16.mp4             # final rendered output
├── assets/
│   ├── dialogue-0845-1003.mp4        # source cut (video)
│   ├── dialogue-0845-1003.m4a        # source cut (audio only)
│   ├── native-cbs-missile.mp4        # B-roll: CBS missile-bounce UFO
│   ├── native-ir-football.mp4        # B-roll: IR football UAP
│   ├── native-greece-90deg.mp4       # B-roll: 90-degree turn
│   ├── nightsky-pexels.mp4           # stock: night sky (backup)
│   ├── ufo-alien-138116.mp4          # stock: alien UFO (backup)
│   └── ufo-fleet-pexels.mp4          # stock: UFO fleet (backup)
├── renders/                          # hyperframes render outputs
└── snapshots/                        # preview contact sheets
```
