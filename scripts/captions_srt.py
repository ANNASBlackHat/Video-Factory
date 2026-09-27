#!/usr/bin/env python3
"""captions_srt.py — burn-free caption sidecars for a finished render.

    python3 scripts/captions_srt.py <video|wav> -o out.srt
    python3 scripts/captions_srt.py <video|wav> -o out.srt --json out.json
    python3 scripts/captions_srt.py <transcript.json> -o out.srt   # re-export, no ASR

Runs faster-whisper locally (Bahasa by default) and groups word timestamps
into phrase-level SRT cues (<=5 words, <=3.5s, break on punctuation or a
speech gap). `--json` also emits the flat word array HyperFrames captions
consume: [{ "id": "w0", "text": ..., "start": ..., "end": ... }].
"""
import argparse
import json
import sys
from pathlib import Path

MUSIC = set("♪\u266a\u266b\u266c\u266d\u266e\u266f\uFFFD")


def fmt_ts(t: float) -> str:
    t = max(0.0, t)
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("media", help="video/audio file, or a word-level .json transcript to re-export")
    ap.add_argument("-o", "--out", help="output .srt (default: <media>.srt)")
    ap.add_argument("--json", help="also write a word-level .json transcript")
    ap.add_argument("--model", default="medium", help="faster-whisper model (default: medium)")
    ap.add_argument("--language", default="id", help="language code (default: id)")
    ap.add_argument("--max-words", type=int, default=5, help="words per cue (default: 5)")
    ap.add_argument("--max-secs", type=float, default=3.5, help="max cue length (default: 3.5s)")
    args = ap.parse_args()

    media = Path(args.media)
    if not media.is_file():
        print(f"ERROR: no such file: {media}", file=sys.stderr)
        return 2
    out = Path(args.out) if args.out else media.with_suffix(".srt")

    music_hits = 0
    if media.suffix.lower() == ".json":
        data = json.loads(media.read_text(encoding="utf-8"))
        raw_words = data if isinstance(data, list) else data.get("words", [])
        words = [
            {"text": str(w.get("text", "")).strip(), "start": float(w["start"]), "end": float(w["end"])}
            for w in raw_words
            if str(w.get("text", "")).strip()
        ]
        print(f"import: {media} ({len(words)} words, ASR skipped)", file=sys.stderr)
    else:
        from faster_whisper import WhisperModel  # deferred: slow import

        print(f"transcribe: {media} (model={args.model}, language={args.language})", file=sys.stderr)
        model = WhisperModel(args.model, device="cpu", compute_type="int8")
        segments, _info = model.transcribe(
            str(media), language=args.language, word_timestamps=True, vad_filter=True
        )
        words = []
        for seg in segments:
            for w in seg.words or []:
                text = (w.word or "").strip()
                if not text:
                    continue
                if all(c in MUSIC for c in text):
                    music_hits += 1
                    continue
                words.append({"text": text, "start": round(w.start, 3), "end": round(w.end, 3)})

    if not words:
        print("ERROR: transcript empty (no speech found)", file=sys.stderr)
        return 1

    # ── group words into phrase cues ────────────────────────────────────────
    cues, cur, cur_end = [], [], None
    for w in words:
        if cur:
            gap = w["start"] - cur_end
            too_big = len(cur) >= args.max_words
            too_long = w["end"] - cur[0]["start"] >= args.max_secs
            if too_big or too_long or gap > 0.6 or cur[-1]["text"].endswith((".", ",", "!", "?", ":", "…")):
                cues.append(cur)
                cur = []
        cur.append(w)
        cur_end = w["end"]
    if cur:
        cues.append(cur)

    lines = []
    for i, cue in enumerate(cues, 1):
        start = max(0.0, cue[0]["start"] - 0.05)
        end = cue[-1]["end"] + 0.12
        if i < len(cues):  # never overlap the next cue (same -0.05 pad it renders with)
            next_start = max(0.0, cues[i][0]["start"] - 0.05)
            if end > next_start:
                end = max(start + 0.05, next_start - 0.02)
        lines.append(f"{i}\n{fmt_ts(start)} --> {fmt_ts(end)}\n{' '.join(w['text'] for w in cue)}\n")
    out.write_text("\n".join(lines), encoding="utf-8")

    if args.json:
        jp = Path(args.json)
        jp.write_text(
            json.dumps([dict(id=f"w{i}", **w) for i, w in enumerate(words)], ensure_ascii=False, indent=1),
            encoding="utf-8",
        )
        print(f"words json: {jp} ({len(words)} words)", file=sys.stderr)

    dur = words[-1]["end"]
    note = f", {music_hits} music token(s) dropped" if music_hits else ""
    print(f"srt: {out} ({len(cues)} cues, {len(words)} words, speech to {dur:.1f}s{note})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
