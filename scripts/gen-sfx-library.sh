#!/usr/bin/env bash
# ============================================================================
# OFFLINE SFX LIBRARY - shared across video projects
# Mono 48kHz WAV, peak-normalized to ~-6 dBFS. Zero downloads, royalty-free
# by construction (everything synthesized from sines + noise with ffmpeg).
#
# Usage:  ./gen-sfx-library.sh <output-dir>     Needs: ffmpeg on PATH
# ============================================================================
set -euo pipefail
OUT="${1:-sfx}"
mkdir -p "$OUT"; cd "$OUT"
R=48000
gen() { echo "  -> $1"; }

# ======================= IMPACTS / HITS =========================
gen deep_hit.wav
ffmpeg -y -loglevel error -f lavfi -i "aevalsrc=0.9*sin(55*2*PI*t)*exp(-8*t):s=$R:d=0.6" \
  -ac 1 -ar $R -c:a pcm_s16le deep_hit.wav

gen stamp_thud.wav
ffmpeg -y -loglevel error -f lavfi -i "aevalsrc=0.8*sin(80*2*PI*t)*exp(-10*t)+0.2*sin(200*2*PI*t)*exp(-18*t):s=$R:d=0.4" \
  -ac 1 -ar $R -c:a pcm_s16le stamp_thud.wav

gen strobe_hit.wav
ffmpeg -y -loglevel error -f lavfi -i "aevalsrc=0.5*sin(220*2*PI*t)*gte(mod(t\,0.12)\,0.06):s=$R:d=0.7" \
  -af "afade=t=out:st=0.5:d=0.2" -ac 1 -ar $R -c:a pcm_s16le strobe_hit.wav

# ======================= WHOOSHES / RISERS ======================
gen whoosh_hard.wav
ffmpeg -y -loglevel error -f lavfi -i "anoisesrc=color=pink:d=0.5:a=0.8:r=$R" \
  -af "afade=t=in:st=0:d=0.05,afade=t=out:st=0.2:d=0.3,lowpass=f=900" \
  -ac 1 -ar $R -c:a pcm_s16le whoosh_hard.wav

gen riser_tension.wav
ffmpeg -y -loglevel error -f lavfi -i "anoisesrc=color=white:d=2.8:a=0.16:r=$R" \
  -af "highpass=f=250,lowpass=f=7500,volume=volume='1+2.2*pow(t/2.8\,2)':eval=frame,afade=t=in:st=0:d=0.03,afade=t=out:st=2.72:d=0.08" \
  -ac 1 -ar $R -c:a pcm_s16le riser_tension.wav

gen bass_riser.wav
ffmpeg -y -loglevel error -f lavfi -i "aevalsrc=0.5*sin((40+50*pow(t/2.5\,2))*2*PI*t):s=$R:d=2.5" \
  -af "volume=volume='0.3+0.7*pow(t/2.5\,2)':eval=frame" -ac 1 -ar $R -c:a pcm_s16le bass_riser.wav

gen soft_riser.wav
ffmpeg -y -loglevel error -f lavfi -i "anoisesrc=color=brown:d=2.4:a=0.35:r=$R" \
  -af "lowpass=f=600,volume=volume='0.15+0.85*pow(t/2.4\,2)':eval=frame,afade=t=out:st=2.25:d=0.15" \
  -ac 1 -ar $R -c:a pcm_s16le soft_riser.wav

# ======================= UI / DATA ==============================
gen ui_blip.wav
ffmpeg -y -loglevel error -f lavfi -i "aevalsrc=0.5*sin(1500*2*PI*t)*exp(-30*t):s=$R:d=0.15" \
  -ac 1 -ar $R -c:a pcm_s16le ui_blip.wav

gen confirm_click.wav
ffmpeg -y -loglevel error -f lavfi -i "aevalsrc=0.45*sin(800*2*PI*t)*lt(t\,0.05)+0.45*sin(1200*2*PI*t)*gte(t\,0.09):s=$R:d=0.2" \
  -ac 1 -ar $R -c:a pcm_s16le confirm_click.wav

gen tick_counter.wav
ffmpeg -y -loglevel error -f lavfi -i "aevalsrc=0.35*sin(1200*2*PI*t)*lt(mod(t\,0.14)\,0.02):s=$R:d=1.1" \
  -ac 1 -ar $R -c:a pcm_s16le tick_counter.wav

gen tick_loop.wav
ffmpeg -y -loglevel error -f lavfi -i "aevalsrc=0.3*sin(1800*2*PI*t)*lt(mod(t\,0.12)\,0.04):s=$R:d=1.0" \
  -ac 1 -ar $R -c:a pcm_s16le tick_loop.wav

gen typewriter_key.wav
ffmpeg -y -loglevel error -f lavfi -i "anoisesrc=color=white:d=0.06:a=0.5:r=$R" \
  -af "highpass=f=2000,lowpass=f=8000" -ac 1 -ar $R -c:a pcm_s16le typewriter_key.wav

gen terminal_boot.wav
ffmpeg -y -loglevel error -f lavfi -i "aevalsrc=0.35*sin((120+700*pow(t/1.2\,2))*2*PI*t):s=$R:d=1.2" \
  -af "volume=volume='0.2+0.8*t/1.2':eval=frame" -ac 1 -ar $R -c:a pcm_s16le terminal_boot.wav

# ======================= ALERTS =================================
gen alarm_buzzer.wav
ffmpeg -y -loglevel error -f lavfi -i "aevalsrc=0.30*sin(880*2*PI*t)*gte(mod(t\,0.4)\,0.2)+0.30*sin(660*2*PI*t)*lt(mod(t\,0.4)\,0.2):s=$R:d=0.82" \
  -ac 1 -ar $R -c:a pcm_s16le alarm_buzzer.wav

gen glitch_stutter.wav
ffmpeg -y -loglevel error -f lavfi -i "anoisesrc=color=white:d=0.48:a=0.6:r=$R" \
  -af "aeval=val(0)*lt(mod(t\,0.08)\,0.045),highpass=f=500,afade=t=out:st=0.38:d=0.1" \
  -ac 1 -ar $R -c:a pcm_s16le glitch_stutter.wav

# ======================= PAPER (editorial) ======================
gen page_flip.wav
ffmpeg -y -loglevel error -f lavfi -i "anoisesrc=color=pink:d=0.22:a=0.7:r=$R" \
  -af "highpass=f=700,tremolo=f=17:d=0.95,afade=t=out:st=0.12:d=0.1" \
  -ac 1 -ar $R -c:a pcm_s16le page_flip.wav

gen paper_rustle.wav
ffmpeg -y -loglevel error -f lavfi -i "anoisesrc=color=pink:d=0.6:a=0.4:r=$R" \
  -af "lowpass=f=3000,tremolo=f=11:d=0.7,afade=t=out:st=0.45:d=0.15" \
  -ac 1 -ar $R -c:a pcm_s16le paper_rustle.wav

gen pen_scratch.wav
ffmpeg -y -loglevel error -f lavfi -i "anoisesrc=color=white:d=0.3:a=0.4:r=$R" \
  -af "lowpass=f=2400,volume=volume='0.4+0.6*abs(sin(22*t))':eval=frame" \
  -ac 1 -ar $R -c:a pcm_s16le pen_scratch.wav

gen seal_pop.wav
ffmpeg -y -loglevel error -f lavfi -i "aevalsrc=0.55*sin((300-1900*t)*2*PI*t):s=$R:d=0.12" \
  -ac 1 -ar $R -c:a pcm_s16le seal_pop.wav

echo "done -> $(cd "$OUT" && pwd)"
