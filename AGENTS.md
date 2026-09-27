# Agent Instructions — hyperframes-experiments

**Read [`README.md`](README.md) first.** It is the index: every playbook, every `.docs/` file,
and the TL;DR for both workflows. This file only tells you *what to open when*.

## 1. Rules that apply to every run

| Need | Open |
|---|---|
| Build-from-nothing pipeline (research → assets → captions → VO → SFX → render) | [`PLAYBOOK-concept-to-video.md`](PLAYBOOK-concept-to-video.md) |
| Cut clips from long-form footage | [`PLAYBOOK-longform-to-clip.md`](PLAYBOOK-longform-to-clip.md) |
| Cut a viral vertical short from a podcast/interview MP4 + transcript | [`PLAYBOOK-podcast-to-short.md`](PLAYBOOK-podcast-to-short.md) |
| TTS / voiceover (OmniVoice default, Piper fallback, **engine-specific number rules**) | [`.docs/04-tts-voice-playbook.md`](.docs/04-tts-voice-playbook.md) |
| **VO script / hook / script structure** — mandatory before any TTS run (`/yt-script`) | YouTube skills pack, installed globally; install recipe in [`README.md`](README.md) → "Other reference" |
| Hard-won lessons — read before the next run | [`.docs/07-lessons-evidence.md`](.docs/07-lessons-evidence.md) (newest) and [`.docs/03-purbaya-lessons-learned.md`](.docs/03-purbaya-lessons-learned.md) |
| **Captions + delivery** — .srt sidecar after render, then send video/captions/package to Telegram | `scripts/captions_srt.py`, then `scripts/telegram-deliver.sh <video> --srt auto --text <package.txt>` (one command; creds from `.env`) |

## 2. Per-topic logs — open only when working that topic

`.docs/00` (template) · `01` karhutla · `02` purbaya reshuffle · `05` anthropic-ipo motion ·
`06` anthropic-ipo evidence · `uss-cyclops-*`. These are records, not rules — don't read them
on a fresh topic.

## 3. Composition work

Inside `videos/<project>/`, its own `AGENTS.md`/`CLAUDE.md` carries the composition rules.
Always load the `/hyperframes` skill before writing or editing any composition HTML — it routes
to the owning workflow and domain skills (`/hyperframes-core`, `-animation`, `-cli`, …).

## 4. Environment gotchas (verified, don't relearn)

```bash
# Node: default v20 is too old — use 24 before any npx hyperframes
export NVM_DIR="$HOME/.nvm"; . "$NVM_DIR/nvm.sh"; nvm use 24.18.0

# Render containing <video> → screenshot capture (fast capture renders video black)
npx hyperframes render --no-best-effort --experimental-fast-capture=false \
  --skill hyperframes -o renders/<project>.mp4

# After every composition edit
npx hyperframes check
```

- SFX: copy the existing 19-file library from any `videos/*/assets/audio/` — never regenerate.
- Delivery: `.env` holds `TELEGRAM_TOKEN` + `TELEGRAM_CHAT_ID` — never echo the token; the
  delivery script reads it itself. Final step of every run: render → captions →
  `scripts/telegram-deliver.sh` (details in README TL;DR steps 8–9).
- Colab: `~/.local/bin/colab`; always `colab stop`; re-upload inputs per session.
- Docs have reversals: when a run overturns an older rule, update the old doc in the same
  change (see the SUPERSEDED banner in `.docs/03`).
