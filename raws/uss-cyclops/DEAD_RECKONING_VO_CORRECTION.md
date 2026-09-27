# VO CORRECTION TABLE — USS Cyclops Short

**Purpose (playbook §2a):** the VM transcript is **timing truth, NOT copy truth**. Captions/on-screen text use the **corrected** copy; cuts/animation sync to the **original** word timestamps. This table maps heard → correct → time.

**VO:** `voiceover.wav` (44.1 kHz mono, **53.71s**, 124 words) · Speaker: OuteTTS Llama‑OuteTTS‑1.0‑1B `en-female-1-neutral` · Reference: not used (Indonesian sample rejected — see log) 
**Transcript source:** faster‑whisper `small`, word timestamps → `voiceover.wordtimes.json`.

## Audio sanity
- mean −19.7 dB / max −1.0 dB → real speech, not silent, not clipped. ✅

## Corrections (heard → correct → time)

| # | Heard | Correct | Time(s) | Note |
|---|-------|---------|---------|------|
| C1 | `avern` | **Then** | 38.08 | Whisper misheard "Then she sailed…" → "avern she". Fix copy to "Then she"; cut still syncs to 38.08. |

## Verified correct (no change) — includes every number

| Item | Heard time window | Matches facts lock |
|------|-------------------|--------------------|
| 306 people | 1.04–2.48 | F2 ✅ |
| in 1918 | 3.34–4.10 | F3 ✅ |
| no distress call / no wreckage | 4.76–6.78 | F6 ✅ |
| German U-boat got her → They were wrong | 9.12–11.60 | hook ✅ |
| German naval records checked after the war | 12.86–15.36 | F11 ✅ |
| zero submarines anywhere near her position | 16.36–18.24 | F11 ✅ |
| no one ever claimed the kill | 19.38–20.46 | F13 ✅ |
| ore **five times denser** than the coal she was built for | 26.14–28.96 | F7/F8 ✅ |
| one of her two engines was broken | 29.80–31.24 | F9 ✅ |
| waterline mark fully underwater when she left port | 34.46–37.04 | F10 ✅ |
| sailed straight into a gale | 38.38–40.08 | F14 ✅ |
| case status probable | 41.38–42.64 | F15 ✅ |
| killed by her own physics | 47.40–48.40 | F15 ✅ |

## Real beat boundaries (derived from word timings — timing truth)
| Beat | Window (s) | Cue word @ time |
|------|-----------|-----------------|
| HOOK | 0.00 – 11.60 | …"They were wrong." @ 11.60 |
| TURN | 11.60 – 21.84 | "German naval records… no one was there" @ 21.84 |
| REVEAL | 21.84 – 40.08 | "So what actually happened?… into a gale" @ 40.08 |
| VERDICT | 40.08 – 48.40 | "Case status… killed by her own physics" @ 48.40 |
| CTA | 48.40 – 53.71 | "Full case file… linked below." (end) |

> Provisional beats in the teleprompter (0:08/0:18/0:35/0:45) are **replaced** by these real timings for storyboarding.