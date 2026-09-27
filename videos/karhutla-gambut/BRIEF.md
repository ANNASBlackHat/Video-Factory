# BRIEF — "Ini Bukan Musibah Alam" (Karhutla Gambut Kalimantan)

**Format:** 1080×1920 vertical · **Durasi:** 156.2s (mengikuti VO `final_full_voiceover.wav`)
**Kontrak riset:** `raws/investigasi-karhutla/` — VO wav = timing truth, JSON = cue map kata, MD = facts lock, `assets-collected/` = visual.

## Konsep kreatif: "FORENSIC GROUND" (hybrid market-crime-desk × ticker-shock)

Dark broadcast investigation yang bertemu data-overload. Kamera "turun ke bawah tanah"
sebagai motif utama: hook cross-section gambut (0m → −3m) kembali sebagai anchor visual
di 3 titik (hook, mistakes, CTA). Fast pace: **28 shot / 156s ≈ 2.4s rata-rata**, hard cut
+ whip-pan, tanpa shot diam >4s.

| Elemen | Keputusan |
|---|---|
| Palette | Base charcoal `#12100e` + gambut `#2a1f16`; accents ember orange `#ff5a1f`, alarm red `#e11d2e`, wet teal `#2dd4bf` (dipakai HANYA di segmen basah/hope) |
| Type | Archivo Black (display, 400-only) + Oswald 400/700 (caption/tag); JetBrains Mono untuk angka/data |
| Caption | **Word-level karaoke** — active word highlight ember, pill Oswald 700 ≥56px, lower-third, safe-zone bawah 15% kosong |
| Signature moves | (1) cross-section bara 3m, (2) counter odometer hotspot, (3) teks ×4,5 scale-punch, (4) grade dingin→hangat di 128.5s |
| Grain/Vignette | film grain statis seeded + vignette halus full-frame (child fill, bukan root) |

## Facts lock (JANGAN mengarang angka/nama di luar ini)

- 202.010,96 ha terbakar nasional Jan–Jul 2026; +120% vs 2019 (107.465 ha Jan–Jun); Kalbar 38.310,86 ha
- 8.638 hotspot Kalimantan per 21 Agt 2026 (Kalbar 3.705, Kalteng 3.081); 5.735 hotspot live Pantau Gambut 29 Agt
- 74% hotspot dalam konsesi (Walhi); 39% / 5,2 juta ha dari 13,43 juta ha gambut nasional dalam konsesi
- Kanal drainase → risiko kebakaran 4,5× (The Conversation/TitikTerang 24 Agt 2026)
- PLG 1995: Keppres 82/1995, dihentikan Keppres 33/1998, ~15.594 KK transmigran, separuh eksodus
- Food Estate: ~1% dari 243.216 ha eks-PLG layak padi (Pantau Gambut)
- Hukum: 72 tersangka, 89 LP, barang bukti 35 korek api; 4 korporasi diselidiki; denda Rp6,1 T belum cair
- Katingan Mentaya: kredit karbon, potensi US$8,4 M saving / 2,49 juta ha restorasi
- Paludikultur: sagu, jelutung, purun, gelam, belangeran; rewetting 3R, muka air <−40 cm

## Audio plan

1. **VO** = `final_full_voiceover.wav`, clip `data-start=0`, full duration. Track id `vo`.
2. **Music bed**: dark ambient 0–77s (tension build, riser menjelang drop) → beat drop **77.29s** ("Gini cara bacanya") → break minimal 112–128s → hopeful major bed **128.53s** → outro 147–156s. Track id `bed`.
3. **Ducking**: `carve.mjs --bed bed --voice vo --strength 0.25 dynamic` (bed kembali naik di jeda antar-frasa).
4. **SFX**: generate via `scripts/gen-sfx-library.sh .media/sfx` + tweak offline ffmpeg. Cue list per scene di STORYBOARD.md — SFX WAJIB di setiap hard cut boundary (whoosh/impact), angka (ticker tick), stamp (thud).

## Koreksi transkrip (pakai teks benar ini di caption, bukan raw JSON)

`disemperot`→disemprot · `Dela pan ribu 600`→delapan ribu enam ratus · `mengkina`→**menggunung** (perlu konfirmasi user) · `Tawun`→Tahun · `Hector`→hektar · `Escafator tegelam`→Eskavator tenggelam · `Padigagal`→Padi gagal · `ngelup`→nge-loop · `kanal trainer saya`→kanal drainase · `4 stengah`→4,5 · `Bukum`→Hukum · `korak api`→korek api · `M4`→empat · `ketingan mentaya`→Katingan Mentaya · `malam menghasilkan`→malah menghasilkan · `panggan`→pangan · `rocket`→roket · `musib alam`→musibah alam
