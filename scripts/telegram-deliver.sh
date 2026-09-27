#!/usr/bin/env bash
# telegram-deliver.sh — send a finished render (plus captions + package text) to Telegram.
#
# Usage:
#   scripts/telegram-deliver.sh <video.mp4> --srt auto           # captions + video
#   scripts/telegram-deliver.sh <video.mp4> --srt auto --text <package.txt>
#   scripts/telegram-deliver.sh <video.mp4>                      # video only
#   scripts/telegram-deliver.sh <video.mp4> --dry-run            # show what would be sent
#
#   --srt auto      make a caption sidecar via scripts/captions_srt.py (Bahasa) and send it
#                   (reuses <video>.transcript.json when it is newer than the video)
#   --srt <file>    send an existing .srt/.vtt instead
#   --text <file>   send that file's contents as a message FIRST (the title/description package)
#   --caption <s>   caption on the first document (default: filename + size)
#
# Reads TELEGRAM_TOKEN + TELEGRAM_CHAT_ID from the repo-root .env (never printed).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$ROOT/.env"
[[ -f "$ENV_FILE" ]] || { echo "ERROR: $ENV_FILE not found" >&2; exit 1; }
set -a; . "$ENV_FILE"; set +a

# Tolerate the historical key typo and the "#id123" note format.
CHAT_ID="${TELEGRAM_CHAT_ID:-${TELEGRAN_CHAT_ID:-}}"
CHAT_ID="${CHAT_ID#\#id}"
TOKEN="${TELEGRAM_TOKEN:-}"
[[ -n "$CHAT_ID" && -n "$TOKEN" ]] || { echo "ERROR: TELEGRAM_CHAT_ID / TELEGRAM_TOKEN missing in .env" >&2; exit 1; }

DRY=0; TEXT=""; SRT=""; CAPTION=""; FILES=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY=1; shift ;;
    --text)    TEXT="${2:?--text needs a file}"; shift 2 ;;
    --srt)     SRT="${2:?--srt needs auto|<file>}"; shift 2 ;;
    --caption) CAPTION="${2:?--caption needs a string}"; shift 2 ;;
    -h|--help) sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*) echo "ERROR: unknown flag $1" >&2; exit 2 ;;
    *)   FILES+=("$1"); shift ;;
  esac
done
[[ ${#FILES[@]} -gt 0 || -n "$TEXT" || -n "$SRT" ]] || { echo "ERROR: nothing to send (see --help)" >&2; exit 2; }

# ── captions ────────────────────────────────────────────────────────────────
if [[ "$SRT" == "auto" ]]; then
  [[ ${#FILES[@]} -ge 1 ]] || { echo "ERROR: --srt auto needs a video as the first argument" >&2; exit 2; }
  vid="${FILES[0]}"; srt="${vid%.*}.srt"; tr="${vid%.*}.transcript.json"
  echo "captions: $vid -> $srt"
  if [[ "$DRY" == 1 ]]; then
    echo "  (dry-run: skip captions)"
  else
    src="$vid"
    if [[ -f "$tr" && "$tr" -nt "$vid" ]]; then
      src="$tr"; echo "  reusing transcript: $tr (newer than the video)"
    fi
    python3 "$ROOT/scripts/captions_srt.py" "$src" -o "$srt"
    [[ -s "$srt" ]] || { echo "ERROR: captions not produced" >&2; exit 1; }
  fi
  SRT="$srt"
fi
if [[ -n "$SRT" && "$SRT" != "auto" && ! -f "$SRT" && "$DRY" == 0 ]]; then
  echo "ERROR: no such caption file: $SRT" >&2; exit 2
fi
if [[ -n "$SRT" && -f "$SRT" ]]; then
  FILES+=("$SRT")
elif [[ -n "$SRT" ]]; then
  echo "  (dry-run: would also send $SRT)"
fi

# ── helpers ─────────────────────────────────────────────────────────────────
post() { # post <method> <outfile> [curl args...]
  local method="$1" out="$2"; shift 2
  if [[ "$DRY" == 1 ]]; then
    echo "DRY  $method -> $out"; return 0
  fi
  curl -s --max-time "${TG_TIMEOUT:-900}" -X POST \
    "https://api.telegram.org/bot${TOKEN}/${method}" "$@" -o "$out"
  python3 - "$method" "$out" <<'PY'
import json, sys
method, path = sys.argv[1], sys.argv[2]
r = json.loads(open(path, 'rb').read().decode('utf-8', 'replace'))
if not r.get('ok'):
    print(f"FAIL {method}: {r.get('description', '?')}", file=sys.stderr)
    sys.exit(1)
res = r.get('result') or {}
doc = res.get('document') or res.get('video') or {}
print(f"ok   {method}: message_id={res.get('message_id')}"
      + (f" size={doc.get('file_size')}" if doc.get('file_size') else ''))
PY
}

# ── 1. package text (so it sits above the files) ────────────────────────────
if [[ -n "$TEXT" ]]; then
  [[ -f "$TEXT" ]] || { echo "ERROR: no such text file: $TEXT" >&2; exit 2; }
  post sendMessage /tmp/tg-deliver-text.json \
    --data-urlencode "chat_id=${CHAT_ID}" \
    --data-urlencode "text@${TEXT}"
fi

# ── 2. files ────────────────────────────────────────────────────────────────
for f in "${FILES[@]}"; do
  [[ -f "$f" ]] || { echo "ERROR: no such file: $f" >&2; exit 2; }
  bytes=$(stat -f%z "$f" 2>/dev/null || stat -c%s "$f")
  cap="${CAPTION:-$(basename "$f") · $((bytes / 1024 / 1024)) MB}"
  echo "upload: $f ($bytes bytes)"
  post sendDocument /tmp/tg-deliver-doc.json \
    -F "chat_id=${CHAT_ID}" \
    -F "document=@${f}" \
    -F "caption=${cap}"
  CAPTION=""
done

echo "done — ${#FILES[@]} file(s) delivered."
