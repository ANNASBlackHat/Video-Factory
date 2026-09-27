#!/usr/bin/env bash
# Offline SFX generation for ipo-crime-desk — mono 48kHz WAV, peak-normalized to -6 dBFS
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p sfx
cd sfx

R=48000

# --- whoosh_hard.wav : filtered pink-noise sweep hit -------------------------
ffmpeg -y -loglevel error -f lavfi -i "anoisesrc=color=pink:d=0.5:a=0.8:r=$R" \
  -af "afade=t=in:st=0:d=0.05,afade=t=out:st=0.2:d=0.3,lowpass=f=900" \
  -ac 1 -ar $R -c:a pcm_s16le whoosh_hard.wav

# --- glitch_stutter.wav : gated white-noise bursts ---------------------------
ffmpeg -y -loglevel error -f lavfi -i "anoisesrc=color=white:d=0.48:a=0.6:r=$R" \
  -af "aeval=val(0)*lt(mod(t\,0.08)\,0.045),highpass=f=500,afade=t=out:st=0.38:d=0.1" \
  -ac 1 -ar $R -c:a pcm_s16le glitch_stutter.wav

# --- stamp_thud.wav : 55 Hz body slam ----------------------------------------
ffmpeg -y -loglevel error -f lavfi -i "aevalsrc=0.9*sin(55*2*PI*t)*exp(-8*t):s=$R:d=0.6" \
  -ac 1 -ar $R -c:a pcm_s16le stamp_thud.wav

# --- alarm_buzzer.wav : two-tone square siren --------------------------------
ffmpeg -y -loglevel error -f lavfi -i "aevalsrc=0.30*sin(880*2*PI*t)*gte(mod(t\,0.4)\,0.2)+0.30*sin(660*2*PI*t)*lt(mod(t\,0.4)\,0.2):s=$R:d=0.82" \
  -ac 1 -ar $R -c:a pcm_s16le alarm_buzzer.wav

# --- riser_tension.wav : noise, volume ramp, ends hard (2.8s) -----------------
ffmpeg -y -loglevel error -f lavfi -i "anoisesrc=color=white:d=2.8:a=0.16:r=$R" \
  -af "highpass=f=250,lowpass=f=7500,volume=volume='1+2.2*pow(t/2.8\,2)':eval=frame,afade=t=in:st=0:d=0.03,afade=t=out:st=2.72:d=0.08" \
  -ac 1 -ar $R -c:a pcm_s16le riser_tension.wav

# --- deep_hit.wav : 42 Hz cinematic boom --------------------------------------
ffmpeg -y -loglevel error -f lavfi -i "aevalsrc=0.9*sin(42*2*PI*t)*exp(-5*t):s=$R:d=0.9" \
  -ac 1 -ar $R -c:a pcm_s16le deep_hit.wav

# --- tick_counter.wav : 6 x 1200 Hz blips, 100 ms apart -----------------------
ffmpeg -y -loglevel error -f lavfi -i "aevalsrc=0.5*sin(1200*2*PI*t)*exp(-60*mod(t\,0.1)):s=$R:d=0.62" \
  -ac 1 -ar $R -c:a pcm_s16le tick_counter.wav

# --- ui_click.wav : tiny dual-transient click ----------------------------------
ffmpeg -y -loglevel error -f lavfi -i "aevalsrc=0.5*sin(1500*2*PI*t)*exp(-120*t)+0.15*sin(4500*2*PI*t)*exp(-200*t):s=$R:d=0.15" \
  -ac 1 -ar $R -c:a pcm_s16le ui_click.wav

# --- normalize all peaks to -6 dBFS (skip riser: preserves its ramp) -----------
for f in whoosh_hard.wav glitch_stutter.wav stamp_thud.wav alarm_buzzer.wav deep_hit.wav tick_counter.wav ui_click.wav; do
  max=$(ffmpeg -hide_banner -i "$f" -af volumedetect -f null - 2>&1 | grep max_volume | sed 's/.*max_volume: //;s/ dB//' | tr -d '-')
  gain=$(awk -v m="$max" 'BEGIN{printf "%.2f", -6 - m}')
  ffmpeg -y -loglevel error -i "$f" -af "volume=${gain}dB" -c:a pcm_s16le tmp.wav
  mv tmp.wav "$f"
done

echo "--- generated ---"
for f in *.wav; do
  ffprobe -v error -show_entries format=duration -of csv=p=0 "$f" | xargs printf "%-22s %ss\n" "$f"
done