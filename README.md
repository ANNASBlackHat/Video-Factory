# HyperFrames Experiments

Learning-process repo: turn a topic into a short video, or a short clip from a long-form video. This `README.md` is the **index** — it lists what docs/playbooks exist and how to re-run each process. Playbooks hold the *rules*; `.docs/` holds the *per-topic logs + lessons*.

> Agents: start at [`AGENTS.md`](AGENTS.md) — it routes to this index and names the 3 docs that apply to every run.

## Playbooks (the repeatable processes)

| File | What it does | Use it when |
|---|---|---|
| [`PLAYBOOK-concept-to-video.md`](PLAYBOOK-concept-to-video.md) | **Build-from-nothing:** web-search the facts, freeze images, caption assets on Colab, author a HyperFrames composition from scratch. | You have only a topic; no pre-existing footage. |
| [`PLAYBOOK-longform-to-clip.md`](PLAYBOOK-longform-to-clip.md) | **Cut-a-clip:** produce short vertical clips from a long-form source (word-timed VO, ASS/SRT captions, SFX library, 3-concept scaffold). | You already have a long video / recorded VO + captions to cut down. |
| [`PLAYBOOK-podcast-to-short.md`](PLAYBOOK-podcast-to-short.md) | **Podcast → viral short:** cut a 60-90s vertical short from a long podcast/interview MP4 + transcript. | You have a long Indonesian podcast/interview and want one viral clip. |

*More playbooks will be added here as new use-cases emerge — each is one repeatable process.*

## How to re-run a process (TL;DR)

### A) Concept → short video (from nothing)

```
1. Drop research:      raws/<topic>/<Topic>.md
2. Expand + assets:    websearch + chrome-devtools → raws/<topic>/REPORT-*.md + assets-collected/
   (template: .docs/00-workflow-template.md §2–4)
3. Captions (Colab):   scripts/caption_assets.py   (see PLAYBOOK-concept-to-video.md §3)
4. VO:                 pluggable — put the script in raws/<topic>/tts-lines.json, run a runner:
                       - OmniVoice (DEFAULT, clone of a voice): upload ref .m4a + matching .srt +
                         tts-lines.json → scripts/tts_omnivoice.py
                       - Piper (Bahasa fallback): upload tts-lines.json → scripts/tts_piper.py
                       (see .docs/04-tts-voice-playbook.md)
                       — OR user-supplied WAV(s) in videos/<project>/assets/vo/
5. SFX:               **check existing first** — `ls videos/*/assets/audio/ | wc -l`; if any project
                      has the 19-file library, copy it (`cp -r videos/<existing>/assets/audio .`),
                      don't regenerate. Only run `scripts/gen-sfx-library.sh <dir>` if none exists.
6. Author + render:    npx hyperframes init videos/<project> → index.html → npx hyperframes check → render
   (rules: PLAYBOOK-concept-to-video.md)
7. Freeze recipe:      videos/<project>/.media/recipes/<name>/  (frame.md + recipe.json + skeletons)
```

Full detail: [`PLAYBOOK-concept-to-video.md`](PLAYBOOK-concept-to-video.md).

### B) Long-form → short clip

```
1. Contract:           long video + recorded VO + word-timestamps + captions (ASS/SRT)
2. Scene map:          caption timings → shot blocks (~2.2–2.5s/shot)
3. Scaffold 3 concepts (parallel), each with a FULL self-contained packet + facts lock
4. SFX:               check existing first (`ls videos/*/assets/audio/`); copy the 19-file library
                      from any project that has it, or `scripts/gen-sfx-library.sh <dir>` if none
5. Verify:            rerun lint, grep facts vs source, check asset paths
6. Check → Studio → user approves → render (background nohup)
```

Full detail: [`PLAYBOOK-longform-to-clip.md`](PLAYBOOK-longform-to-clip.md).

## `.docs/` — per-topic logs + lessons

| File | Type |
|---|---|
| [`.docs/00-workflow-template.md`](.docs/00-workflow-template.md) | Fill-in template for any new concept→video topic |
| [`.docs/01-investigasi-karhutla.md`](.docs/01-investigasi-karhutla.md) | Filled example (Karhutla Gambut Kalimantan) |
| [`.docs/02-purbaya-suahasil-menkeu.md`](.docs/02-purbaya-suahasil-menkeu.md) | Workflow log — Purbaya reshuffle (3 concepts rendered) |
| [`.docs/03-purbaya-lessons-learned.md`](.docs/03-purbaya-lessons-learned.md) | **Per-section lessons** from the Purbaya run — read before the next run |
| [`.docs/04-tts-voice-playbook.md`](.docs/04-tts-voice-playbook.md) | **Pluggable TTS VO recipe** — OmniVoice (default, clone of a voice) + Piper `id_ID` (Bahasa fallback); upload lines+knobs, never edit code. Number rules are **engine-specific** (see table inside) |
| [`.docs/05-anthropic-ipo.md`](.docs/05-anthropic-ipo.md) | Workflow log — Anthropic IPO concept 1 (`anthropic-ipo-ticker-shock`, motion-heavy, superseded) |
| [`.docs/06-anthropic-ipo-evidence.md`](.docs/06-anthropic-ipo-evidence.md) | Workflow log — Evidence Desk rebuild (`anthropic-ipo-evidence`, 72.3s, OmniVoice VO, YouTube-clip evidence) + **render rules** (video nesting / screenshot capture / GOP) |
| [`.docs/07-lessons-evidence.md`](.docs/07-lessons-evidence.md) | **Per-section lessons** from the Evidence run — read before the next run (TTS A/B, black-video fix, assertion-script retimes) |

## Other reference

- **Colab CLI:** `~/.local/bin/colab` (v0.6.0, oauth2 as `annas.developer@gmail.com`). Always `colab stop` — sessions burn units. See `scripts/README.md`.
- **Reusable `scripts/`** (shared across projects — do NOT duplicate into `videos/<project>/`):
  - `scripts/caption_assets.py` — image captioning (blip/git/florence2/blip2)
  - `scripts/tts_piper.py` — Piper TTS / voice-clone runner (edit `lines` dict, run on Colab)
  - `scripts/tts_omnivoice.py` — OmniVoice zero-shot clone runner (upload lines + `ref-voice.m4a/.srt`, never edit code)
  - `scripts/gen-sfx-library.sh <dir>` — 19-sound offline SFX generator
  - See `scripts/README.md` for quick-start commands + Piper API notes.
- **VO samples:** `voices/*.m4a` — reference clips for voice cloning (Colab).

## Structure

```
PLAYBOOK-concept-to-video.md      # build-from-nothing process
PLAYBOOK-longform-to-clip.md      # clip-from-longform process
PLAYBOOK-podcast-to-short.md      # podcast/interview → viral vertical short
README.md                         # THIS index
AGENTS.md                         # agent router → starts here
.docs/<n>-<topic>.md             # per-topic logs + lessons
ideas/                            # loose motion/video idea notes (not yet playbooks)
raws/<topic>/                     # research + assets + reports
scripts/caption_assets.py        # image captioning (Colab)
scripts/tts_piper.py            # Piper TTS / voice-clone runner (Colab)
scripts/gen-sfx-library.sh      # SFX generator (reusable)
videos/<project>/                # HyperFrames outputs (+ .media/recipes)
voices/                          # reference VO samples (Colab voice cloning)
```

> **Reusable code lives in `scripts/`, not in each project.** `videos/<project>/` keeps only project-specific assets (images, VO WAVs, SFX copies). Never copy `tts_piper.py` or `caption_assets.py` into a project.
