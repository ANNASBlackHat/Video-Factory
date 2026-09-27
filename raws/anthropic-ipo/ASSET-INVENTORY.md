# ASSET-INVENTORY — anthropic-ipo

All files frozen with provenance (source URL → local file), validated with `file` (real image/vector bytes, no HTML error pages).

## Provenance table

| # | Source | Page visited (chrome) | Frozen file | Note |
|---|--------|-----------------------|-------------|------|
| 01 | techspot.com | https://www.techspot.com/news/113485-anthropic-heading-toward-largest-ipo-ever-possible-2.html | `hero/techspot-anthropic-ipo.jpg` | 2425x1600 editorial hero |
| 02 | techcrunch.com | https://techcrunch.com/2026/08/17/anthropics-annualized-revenue-surges-to-65b/ | `hero/techcrunch-revenue-65b.jpeg` | 1024x681 revenue-story image |
| 03 | en.wikipedia.org | https://en.wikipedia.org/wiki/Anthropic | `hero/dario-amodei.jpg` | 4000x2667 Dario Amodei (CEO) |
| 04 | en.wikipedia.org | https://en.wikipedia.org/wiki/Anthropic | `hero/dario-amodei-small.jpg` | 800px variant |
| 05 | commons.wikimedia.org | via wiki Anthropic logo | `logos/anthropic-logo.svg` | vector wordmark |
| 06 | commons.wikimedia.org | via wiki Anthropic | `logos/anthropic-corporate-structure.svg` | vector org chart |
| 07 | commons.wikimedia.org | https://en.wikipedia.org/wiki/Initial_public_offering_of_SpaceX | `comparisons/spacex-logo.svg` | vector SpaceX logo |
| 08 | commons.wikimedia.org | https://en.wikipedia.org/wiki/Initial_public_offering_of_SpaceX | `comparisons/spacex-ipo-timeline.gif` | 680x690 timeline |
| 09 | commons.wikimedia.org | https://en.wikipedia.org/wiki/Anthropic | `comparisons/anthropic-hq-slack-office.jpg` | 2865x2952 HQ exterior |

## Notes
- Claude symbol SVG returned 404 (filename moved on Commons) — skipped, not needed.
- SVGs are fine for HyperFrames (inline or `<img src>`).
- Total: 9 files, ~5 MB.

---

# Evidence assets — `assets-evidence/` (refresh 26 Sep 2026)

News screenshots captured live via chrome-devtools MCP (viewport 1440×552, EDGAR 900×552), then audited as an ffmpeg `tile` montage. Photos via Wikimedia Commons API (`imageinfo` extmetadata for artist/license). Footage via `yt-dlp --download-sections --force-keyframes`.

## `news/` — 14 screenshots (PNG)

| # | Source | Page | File | Note |
|---|--------|------|------|------|
| N01 | Anthropic | https://www.anthropic.com/news/confidential-draft-s1-sec | `anthropic-own-s1-announcement.png` | official 1 Jun filing post |
| N02 | CNBC | CNBC, "What Amodei's AI slowdown could mean…" (URL not captured) | `cnbc-amodei-slowdown-ipo.png` | slowdown ↔ IPO beat |
| N03 | CNBC (Reuters synd.) | https://www.cnbc.com/2026/09/05/anthropic-ipo-launch-shifts-toward-mid-October-reuters.html | `cnbc-mid-october-slip.png` | slip Oct → mid-Oct |
| N04 | CNBC-TV18 | cnbctv18.com (URL not captured) | `cnbc18-nvidia-10b-anchor.png` | Nvidia $10B anchor |
| N05 | Crypto Briefing | https://cryptobriefing.com/anthropic-targets-november-ipo-delay/ | `cryptobriefing-november-slip.png` | **cropped to headline** (ads removed) |
| N06 | Forbes | https://www.forbes.com/sites/jimosman/2026/09/17/anthropic-ipo-could-hit-2-trillion-and-put-public-investors-last/ | `forbes-2t-public-last.png` | $2T, public last |
| N07 | Forkast | https://forkast.news/the-anthropic-s-1-that-was-expected-after-labor-day-still-hasnt-arrived/ | `forkast-edgar-empty-line.png` | "EDGAR remains empty" |
| N08 | Fortune | https://fortune.com/2026/08/13/anthropic-ipo-2-trillion-october-largest-ever-spacex/ | `fortune-october-2t-promise.png` | re-captured, headline unclipped |
| N09 | Pomegra | https://pomegra.io/briefs/2026-09-25-ipo-pipeline-anthropic | `pomegra-yields-window.png` | mid-Oct + 30y 5.44% |
| N10 | SEC EDGAR | https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company=anthropic+pbc&type=S-1 | `sec-edgar-no-s1.png` | "No matching companies." (query added as film overlay) |
| N11 | TechCrunch | https://techcrunch.com/2026/09/25/anthropics-founders-seek-voting-control-ahead-of-ipo/ | `techcrunch-founder-voting-control.png` | 50.1% voting |
| N12 | Value Add Pulse | https://valueaddvc.com/pulse/anthropic-ipo-delayed-november-2-trillion-2026 | `valueadd-pushes-2t-november.png` | slip chips: Nov / mid-Oct / $965B |
| N13 | Yahoo/Investing.com | au.finance.yahoo.com …221211879 (WSJ-sourced) | `yahoo-investing-wsj-november-delay.png` | WSJ Nov delay |
| N14 | Mixed News | https://mixed-news.com/en/anthropic-ipo-november-third-quarter-numbers-report/ | `mixednews-q3-rationale.png` | delay = show Q3 numbers |

Dropped: `reuters-mid-october-slip.png` (bot wall), `forkast-s1-late.png` (duplicate of N07).

## `photos/` — 6 files (Wikimedia Commons, API metadata recorded)

| # | File | Author | License | Commons page |
|---|------|--------|---------|--------------|
| P01 | `nasdaq-tower-2026.jpg` 1920×2880 | Nielsoncaetanosalmeron | CC BY 4.0 | File:Nasdaq Tower May 2026.jpg |
| P02 | `datacenter-racks.jpg` 1920×1280 | Carl Lender | CC BY 2.0 | File:Datacenter Server Racks (22370909788).jpg |
| P03 | `amodei-stage.jpg` 1920×1280 | TechCrunch | CC BY 2.0 | File:Dario Amodei at TechCrunch Disrupt 2023 06.jpg |
| P04 | `nvidia-logo.svg` | Nvidia | Apache-2.0 | File:NVIDIA logo.svg |
| P05 | `nvidia-hq.jpg` 1920×1175 | Coolcaesar | CC BY-SA 4.0 | File:NVIDIA Headquarters.jpg |
| P06 | `wall-street-nyse.jpg` 1920×1440 | Carlos Delgado | CC BY-SA 3.0 | File:Wall Street - New York Stock Exchange.jpg |

## `footage/` — 3 clips (YouTube, yt-dlp, h264+aac)

| # | File | Channel / date | Source | Slice | Spec |
|---|------|----------------|--------|-------|------|
| V01 | `cnbc-jun1-filing.mp4` | CNBC Television, 1 Jun 2026 | watch?v=LF1b0UFb6fE | 0:00–0:13.5 | 608×1080 (vertical card), 13.5s |
| V02 | `yahoo-2t-question.mp4` | Yahoo Finance, 13 Aug 2026 | watch?v=fK48rqSR8UQ | 0:00–0:13.5 | 1920×1080, 13.5s — "HIGH EXPECTATIONS FOR ANTHROPIC IPO / $2 trillion · FT" |
| V03 | `bloomberg-no-price-965b.mp4` | Bloomberg Television, 1 Jun 2026 | watch?v=SlsBIWjIU2s | 0:13–0:27 | 1920×1080, 14s — Ed Ludlow: no share count / no price / $965B |

Cut rationale: V01 = filing beat, V02 = $2T beat, V03 = honest "we don't know the price range" beat.
Rejected: Reuters (bot wall), WSJ direct (paywall), Polymarket (cert error), Admiral Markets (cert error).
