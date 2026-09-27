---
workflow: general-video
flow: automation
storyboard: yes
message: "The biggest IPO in history is late: EDGAR still has no public S-1 on 26 Sep 2026"
destination: tiktok-reels
aspect: 1080x1920
language: id
length: 74s
angle: evidence-newsroom
---

## Intent

Vertical 9:16 **evidence-desk / newsroom** video (Bahasa VO) that replaces the motion-heavy
`anthropic-ipo-ticker-shock` with real evidence: live screenshots of news articles and SEC EDGAR,
real photos, and three muted news clips. The story is the **delay** — the IPO slipped October →
mid-October → November and the prospectus is overdue.

Look: dark slate newsroom chrome, browser-window "clippings" with a URL pill and a
source/date bar under every card, one dominant item per beat, slow Ken Burns on screenshots,
hard news cuts between beats. No odometers, no terminal typing, no ticker.

## Assets

- `assets/vo/final_full_voiceover.wav` — 72.9s Piper `id_ID-news_tts` VO, 24 kHz mono (8 lines, `raws/anthropic-ipo/tts-lines.json`).
- `assets/img/*` — 14 news screenshots + 6 Wikimedia photos + Anthropic logo (`raws/anthropic-ipo/ASSET-INVENTORY.md`).
- `assets/footage/*` — 3 muted yt-dlp clips (CNBC filing, Yahoo $2T, Bloomberg "no price range").
- `assets/audio/sfx/*` — 19-file library copied from `anthropic-ipo-ticker-shock` (page flips, stamp, deep hit, bass riser).

## Customizations

- Captions burned in per VO line; static source footer strip; amber progress line at top.
- SFX only at beat changes and evidence reveals (page_flip / stamp_thud / deep_hit / bass_riser).

## Notes

- Facts lock: `raws/anthropic-ipo/REPORT-REFRESH-2026-09-26.md` (supersedes the timing section of the 20 Sep research).
