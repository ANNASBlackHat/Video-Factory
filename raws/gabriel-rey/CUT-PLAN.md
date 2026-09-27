# CUT PLAN — gabriel-rey-short (9:16, ~74s)

Source: raws/gabriel-rey/source.mp4 (2345.8s, 1920x1080)
Transcript: raws/gabriel-rey/whisper.json (faster-whisper small, id, word-level)
All boundaries snapped to word gaps (no mid-word cuts).

## Beats (final timeline)

| Beat | content | src range (s) | dur | cut-out visual | audio out |
|------|---------|---------------|-----|----------------|-----------|
| B0 | TRACK-RECORD intro card: "2014 — Gabriel Rey masuk industri crypto. CEO Trif Group." | Agnes-generated image, full 7.0s | 7.0 | hold image | BGM only, duck -8dB |
| B1 | "altcoin itu tidak untuk di hold dalam jangka panjang. Jadi you trade altcoin, to get more bitcoin." | 1124.80 – 1131.60 | 6.8 | Gabriel speaking at 19:24 | cut at end of "bitcoin" |
| B2 | "kesalahan pada umumnya… kenapa orang yang banyak rugi, karena mereka terlalu nafsu dengan altcoin-nya. Berpikir altcoin ini bakal jadi the next bitcoin." | 1147.50 – 1154.60 | 7.1 | Gabriel speaking at 19:07 | cut after "next bitcoin" |
| B3 | "influencer yang gak bertanggung jawab, bro. Ngomong coin ini bakal jadi the next bitcoin." | 1156.60 – 1161.99 | 5.4 | 2-shot w/ host | cut after "the next bitcoin" |
| B4 | "bagi kita yang bilang sebuah altcoin jadi the next bitcoin, gap-nya udah terlalu jauh. Impossible sekali." | 1164.60 – 1170.14 | 5.5 | two-shot, hand gesture | cut after "sekali" |
| B5 | "kalau sampai sebuah negara melakukan blacklist terhadap bitcoin" | 413.72 – 418.35 | 4.6 | Gabriel mid-close gesturing | cut at "ke bitcoin" |
| B6 | "bahkan transisi dari desentralisasi… jadi sentralisasi… kita tidak bisa bilang anti pemerintah." | 548.53 – 554.13 | 5.6 | Gabriel mid-close, fire TV glow | cut after "anti government" |
| B7 | "begitu di pemerintahan, dibikin white-list, dibuat seputih mungkin — bahkan Eric Trump beli bitcoin." | 429.76 – 437.70 | 7.9 | wide two-shot, timer overlay | cut after "Eric Trump beli bitcoin" |
| B8 | "dengar, ya, bahwa ini bukan barang scam. Sudah ter-regulasi, pajaknya sudah final. Let's explore crypto untuk 10 tahun ke depan." | 2308.21 – 2314.50 | 6.3 | Gema + banner + headshots | cut after "untuk 10 tahun ke depan" |
| B9 | "terima kasih so much, bro. Saksikan guys… Astronix x Trif." | 2327.00 – 2340.10 | 13.1 | wide two-shot + end-card | cut at "Astronix x Trif" |

Total speech ≈ 58.9s + B0 card 7.0s = **65.9s** final video. (target 60–90s ✓)

## Visuals per beat (all from source.mp4, verified w/ Agnes 3.0 frame reads)
- B1 1124.8: Gabriel mid-single, light blue shirt, orange watch, fire TV glow left
- B2 1147.5: Gabriel mid, gesturing both hands
- B3 1156.6: 2-shot w/ host (host gesturing)
- B4 1164.6: Gabriel mid, open hands
- B5 411.6: Gabriel mid-close gesturing, timer overlay on screen
- B6 549.0: Gabriel mid-close, fire TV glow
- B7 430.0: wide 2-shot, timer + banner
- B8 2308: Gema (mustard jacket) + banner + headshots
- B9 2327: wide 2-shot, handshake, end-card

## Transitions
- B0 → B1: cut-the-curve (quick zoom into card + 150ms black)
- B1..B8: hard cuts w/ 40ms dip-to-black on audio, 200ms crossfade on video
- B8 → B9: rack-focus blur cut (blur 6px → sharp)

## BGM
- Tension/finance bed from stock or generate w/ media-use resolve
- B0 -8dB (ducked under card text)
- B1-B8 -14dB under speech
- B9 fade out on last second

## Captions
- Word-level from whisper.json, bottom rail, max ~25% frame width
- Highlight "altcoin", "the next bitcoin", "regulasi", "blacklist" in yellow

## Assets to build
- raws/gabriel-rey/assets/b0-card.jpg (Agnes 2.5 img2img from Gema's headshot? NO — pure text2img: "2014 Gabriel Rey crypto pioneer CEO Trif Group")
- raws/gabriel-rey/assets/B1.mp4 .. B9.mp4 (ffmpeg cuts)
- raws/gabriel-rey/assets/BGM.mp4 (finance tension bed)
- raws/gabriel-rey/assets/captions.srt (generated from whisper.json)
