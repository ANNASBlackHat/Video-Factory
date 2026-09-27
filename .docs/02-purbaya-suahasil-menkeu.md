# 02 — Reshuffle Menkeu: Purbaya → Suahasil (14 Sep 2026)

**Raw:** `raws/purbaya-suahasil-menkeu/Purbaya-Dicopot-Suahasil-Menkeu.md` | **Report:** `raws/purbaya-suahasil-menkeu/REPORT-BROADENED-menkeu-2026.md`

## Checklist (dari 00-workflow-template)

- [x] `raws/purbaya-suahasil-menkeu/` added (raw + broadened report)
- [x] §1 parse — 19 unique URLs di raw (15 Sep 2026)
- [x] §2 websearch + report — 3 deep queries (ID reshuffle, EN macro, Suahasil profile) + 3 follow-up (BI/rupiah, CELIOS internal, Suahasil fiscal) → REPORT-BROADENED
- [x] §3 chrome 10–15 navigations + provenance table — DONE (20 valid files, 1.2 MB; cdn25.metrotvnews + akcdn.detik DNS retry OK)
- [x] §4 YouTube 20–30 videos table — 16 mapped in SOCIAL-MEDIA-REACTION.md (10 reshuffle + 6 context); gap to 20 noted
- [x] §5 Colab 2–3 models + comparison — captions BLOCKED (upload 500, retry later). **VO** generated via Colab (user-supplied WAV in `videos/purbaya-menkeu-reshuffle/assets/vo/`). Note: this run used Piper TTS (English voice) which does NOT read Indonesian correctly — for the next run, use `scripts/tts_omnivoice.py` (OmniVoice, multilingual + Bahasa, GPU).
- [x] §2b POLICY-IMPACT report — DONE (`REPORT-POLICY-IMPACT-purbaya.md`, facts lock §5)
- [x] PLAYBOOK-concept-to-video.md#workflows row — DONE (row 02 updated to ✅ rendered + recipes frozen)
- [x] Video (PLAYBOOK-longform-to-clip) — DONE, 3 concepts rendered:
  - `videos/purbaya-menkeu-reshuffle/` (92.5s, recipe `purbaya-investigasi`)
  - `videos/purbaya-stat-hit/` (18s, recipe `purbaya-stat-hit`)
  - `videos/purbaya-paper-trail/` (52s, recipe `purbaya-paper-trail`)
  - All check-passed pre-render; VO user-supplied (6 WAV in `assets/vo/`)
  - Facts lock in `REPORT-POLICY-IMPACT-purbaya.md` §5

## Lessons

Detailed per-section lessons (pitfalls, holds, solutions, next-time rules) live in [`03-purbaya-lessons-learned.md`](03-purbaya-lessons-learned.md).

## Temuan kunci (1 baris tiap pertanyaan user)

- **Kenapa dicopot setelah 1 th:** bukan 1 sebab — mutasi eselon II 10 Sep ditolak Dirjen + restitusi ditahan + dividen Danantara Rp120T (internal) + rupiah rekor lemah & outlook dipangkas + friksi BI + beban MBG + gaya overconfidence.
- **Siapa Suahasil:** S1 UI 94, MSc Cornell 97, PhD UIUC 03, Guru Besar 09, Ka BKF 2016-19, Wamenkeu 2019-26, TNP2K/KPPOD/KEN; teknokrat fiskal-kemiskinan.
- **Kenapa dia:** insider 7 th → kontinuitas, sinyal prudence (defisit <3%), penjinak internal, loyal lintas-rezim.
