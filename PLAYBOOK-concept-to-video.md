# Playbook — Concept to Video (short video built from nothing)

Research → assets → captions → video. Starting from a bare topic, you web-search the facts, freeze images, caption assets, and author a HyperFrames composition from scratch. This is the *build-from-concept* path (no pre-existing long-form footage).

## Quick start

```bash
# 1. Drop research
#    raws/<topic>/Topic.md  (like raws/investigasi-karhutla/Kebakaran Lahan Gambut Kalimantan.md)

# 2. Expand + collect assets + find footage (chrome-devtools + websearch)
#    -> see .docs/01-investigasi-karhutla.md §2.2-2.4

# 3. Caption assets on Colab
colab new -s <topic>-cpu
zip -r /tmp/<topic>-assets.zip raws/<topic>/assets-collected
colab upload -s <topic>-cpu /tmp/<topic>-assets.zip /content/
colab exec -s <topic>-cpu -f scripts/caption_assets.py  # or /tmp/run_*.py wrappers
colab download -s <topic>-cpu /content/captions-*.json raws/<topic>/
colab stop -s <topic>-cpu

# 4a. VO SCRIPT — write it with /yt-script BEFORE any TTS. This is a gate, not a suggestion.
#   Why: every video whose script was raw LLM prose came back as AI-slop — flat hook,
#   no turn, no reason to stay past second 15. The TTS engine reads whatever it is given.
#     /yt-script <idea>  -> 5 hooks scored off 21 formulas -> spoken script + retention beats
#   Skill: ~/.agents/skills/yt-*  (install recipe: README -> "Other reference")
#   Voice profile: ~/.claude/youtube/voice.md  (copy templates/voice.md from that repo once,
#   fill it in — every yt-* skill reads it; without it the skill asks for 3 of your videos)
#   Save the approved script: raws/<topic>/VO-SCRIPT.md  (existing convention: VO-SCRIPT-*.txt,
#   VIDEO-SCRIPT-*.md, *Script*.md)  ->  that file is what tts-lines.json is built from.

# 4b. VO TTS (Bahasa Indonesia) — pluggable runners (no code edits)
#   DEFAULT: OmniVoice (zero-shot clone of a voices/*.m4a):
#     colab new -s <topic>-tts --gpu T4 ; colab install -s <topic>-tts omnivoice
#     colab upload ... voices/female-medium-pace.m4a /content/ref-voice.m4a
#     colab upload ... voices/female-medium-pace.srt  /content/ref-voice.srt   (auto-paired)
#     colab upload ... raws/<topic>/tts-lines.json /content/tts-lines.json
#     colab exec -s <topic>-tts -f scripts/tts_omnivoice.py
#   FALLBACK: Piper (trained id_ID model, reliable, no ref) if the clone sounds off:
#     colab new -s <topic>-tts ; colab install -s <topic>-tts piper-tts
#     colab upload ... raws/<topic>/tts-lines.json /content/tts-lines.json
#     colab exec -s <topic>-tts -f scripts/tts_piper.py  (then resample 24kHz)
#   Full recipe + voice transcripts + model URLs: .docs/04-tts-voice-playbook.md
#   NOTE: write numbers in natural form ("65 miliar"); spelled-out words mangle TTS.

# 4c. SFX: check existing first — if any videos/<project>/assets/audio/ already has
#    the 19-file library, just copy it: cp -r videos/<existing>/assets/audio videos/<new>/
#    Only regenerate if no project has it:
#    scripts/gen-sfx-library.sh videos/<new>/assets/audio
```

See `PLAYBOOK-longform-to-clip.md` for the other production path (short clips cut from a long-form video: word-timed VO + ASS/SRT captions).

## Workflow Template

General pipeline for any investigation: **Research → Broaden → Assets (chrome) → Footage (YouTube) → Captions (Colab) → Video**.

→ **Template:** [`.docs/00-workflow-template.md`](.docs/00-workflow-template.md) (fill for any `<topic>`)

→ **Example filled:** [`.docs/01-investigasi-karhutla.md`](.docs/01-investigasi-karhutla.md) (use as reference)

## Workflows

| # | Topic | Raw | Detailed log | Assets | Captions | Status |
|---|-------|-----|--------------|--------|----------|--------|
| 01 | Investigasi Karhutla Gambut Kalimantan | `raws/investigasi-karhutla/Kebakaran Lahan Gambut Kalimantan.md` | [`.docs/01-investigasi-karhutla.md`](.docs/01-investigasi-karhutla.md) | `raws/investigasi-karhutla/assets-collected` (46 files, 20 MB, `ASSET-INVENTORY-FULL.md`) | `captions-blip-base/git-base/blip-large` + `captions-comparison.md` | ✅ broadened, captioned |
| 02 | Reshuffle Menkeu: Purbaya → Suahasil | `raws/purbaya-suahasil-menkeu/Purbaya-Dicopot-Suahasil-Menkeu.md` + `REPORT-BROADENED` + `REPORT-POLICY-IMPACT` + `SOCIAL-MEDIA-REACTION` | [`.docs/02-purbaya-suahasil-menkeu.md`](.docs/02-purbaya-suahasil-menkeu.md) | `raws/purbaya-suahasil-menkeu/assets-collected` (20 files, 1.2 MB, `ASSET-INVENTORY.md`) | ⏳ captions pending (Colab upload 500, 15 Sep) — VO user-supplied | ✅ 3 concepts rendered + recipes frozen; lessons → [`.docs/03-purbaya-lessons-learned.md`](.docs/03-purbaya-lessons-learned.md) |
| 03 | Anthropic IPO: $2 Trillion? | `raws/anthropic-ipo/Anthropic-IPO.md` (facts lock + media quotes) | [`.docs/05-anthropic-ipo.md`](.docs/05-anthropic-ipo.md) | `raws/anthropic-ipo/assets-collected` (9 files, 5 MB, `ASSET-INVENTORY.md`) | ✅ blip-large (git-base backup) | ✅ 1 concept rendered (`anthropic-ipo-ticker-shock`, 72s, Piper fallback VO); pluggable TTS → [`.docs/04-tts-voice-playbook.md`](.docs/04-tts-voice-playbook.md) |
| 04 | Anthropic IPO: Evidence Desk (delay angle) | `raws/anthropic-ipo/REPORT-REFRESH-2026-09-26.md` + `ASSET-INVENTORY.md` | [`.docs/06-anthropic-ipo-evidence.md`](.docs/06-anthropic-ipo-evidence.md) | `raws/anthropic-ipo/assets-collected` (14 news PNGs + 6 photos + 3 yt-dlp clips re-encoded for GOP; 19-file SFX copied) | ✅ burned-in band captions synced to OmniVoice house-voice VO (A/B beat Piper; `.docs/04` number rules) | ✅ rendered (`anthropic-ipo-evidence`, 72.3s, 38.8 MB, screenshot capture); video-nesting/fast-capture rules → doc 06; lessons → [`.docs/07-lessons-evidence.md`](.docs/07-lessons-evidence.md) |

## Adding a new workflow

1. Create `raws/<new-topic>/` and add the research markdown.
2. Copy [`.docs/00-workflow-template.md`](.docs/00-workflow-template.md) → `.docs/<new-topic>.md` and fill `<topic>` placeholders (§1–5).
3. Keep [`.docs/01-investigasi-karhutla.md`](.docs/01-investigasi-karhutla.md) as reference for a filled example.
4. Add a row to the table above linking to the new `.docs/<new-topic>.md`.
5. Run the checklist in the template — everything is script-based and reproducible (`scripts/caption_assets.py`).

Details live in `.docs/` — the playbook stays brief. The repo `README.md` is the index of all playbooks + docs.

## Colab CLI

Installed at `~/.local/bin/colab` (v0.6.0), auth `oauth2` as `annas.developer@gmail.com` (`colab whoami`). Default is `oauth2`; `ADC` not needed. Sessions burn units if not stopped — always `colab stop`. See `scripts/README.md` and `.docs/01-investigasi-karhutla.md §2.5`.

## Structure

```
raws/<topic>/              # research + assets-collected + captions + REPORT-BROADENED
scripts/caption_assets.py  # reusable captioning (blip/git/florence2/blip2)
.docs/<topic>.md           # detailed workflow log (per-topic)
videos/<concept>/          # HyperFrames outputs
```
