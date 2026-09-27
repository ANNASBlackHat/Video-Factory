#!/usr/bin/env python3
# OmniVoice runner — anthropic-ipo v2 (natural numeric form, slower)
import os, json
import numpy as np
import soundfile as sf
import torch

# Numbers left in NATURAL form (digits). OmniVoice butchers fully-spelled-out
# Indonesian number words; digits + short phrases read cleanly.
lines = [
    {"id": "scene_1", "text": "Pasar keuangan sedang membicarakan satu nama. Anthropic. Satu angka, dua triliun dolar. Apakah ini IPO terbesar dalam sejarah?"},
    {"id": "scene_2", "text": "Sejak awal Juni, perusahaan di balik Claude ini sudah diam-diam mengirim berkas penawaran awal ke bursa Amerika. Targetnya, masuk pasar di bulan Oktober."},
    {"id": "scene_3", "text": "Media besar sudah ramai. FT, WSJ, sampai Bloomberg. Semua menyebut ini IPO raksasa yang bisa melewati rekor Spacex."},
    {"id": "scene_4", "text": "Seberapa besar Anthropic sekarang? Penghasilannya naik empat belas kali dalam setahun. Dari 4,5 miliar, jadi 65 miliar dolar per tahun."},
    {"id": "scene_5", "text": "Tapi mereka butuh uang pasar. Biaya komputasinya 517 miliar dolar. Itu lebih dari tujuh kali penghasilannya."},
    {"id": "scene_6", "text": "Yang optimis bilang ini kebangkitan AI. Yang waspada bilang ini gelembung. Modelnya dua setengah kali lebih mahal dari pesaingnya."},
    {"id": "scene_7", "text": "Kalau dua triliun dolar benar terjadi, Anthropic jadi perusahaan publik terbesar dalam sejarah. Tapi pasar yang akan memutuskan. Apakah itu wajar? Waktu yang menjawab."},
]

REF_AUDIO   = "/content/ref-voice.m4a"
REF_TEXT    = "Kalian tau nggak guys, kalau ada sebuah sungai di Jogjakarta, ini itu diberi nama karena pernah ada gajah raksasa yang hilang dan tenggelam di sungai ini"
SPEED       = 0.9
NUM_STEP    = 32
SILENCE_S   = 0.4
OUT_DIR     = os.environ.get("TTS_OUT_DIR", "/content/tts-out-anthropic-ipo-v2")
SAMPLE_RATE = 24000

def main():
    from omnivoice import OmniVoice
    print("[omnivoice] anthropic-ipo v2 — loading k2-fsa/OmniVoice to cuda fp16 ...")
    model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="cuda:0", dtype=torch.float16)
    os.makedirs(OUT_DIR, exist_ok=True)
    gap = np.zeros(int(SAMPLE_RATE * SILENCE_S), dtype=np.float32)
    segs, results = [], {}
    for i, line in enumerate(lines):
        key, txt = line["id"], line["text"]
        print(f"[{i+1}/{len(lines)}] {key}: {txt[:50]}...")
        out = model.generate(text=txt, ref_audio=REF_AUDIO, ref_text=REF_TEXT, num_step=NUM_STEP, speed=SPEED)
        wav = np.array(out[0], dtype=np.float32).squeeze()
        p = f"{OUT_DIR}/{key}.wav"
        sf.write(p, wav, SAMPLE_RATE)
        print(f"       {len(wav)/SAMPLE_RATE:.1f}s -> {p}")
        results[key] = p
        segs.append(wav)
        if i < len(lines)-1: segs.append(gap)
    final = np.concatenate(segs)
    fp = f"{OUT_DIR}/final_full_voiceover.wav"
    sf.write(fp, final, SAMPLE_RATE)
    print(f"[done] {len(lines)} scenes, total {len(final)/SAMPLE_RATE:.1f}s -> {fp}")
    print(json.dumps(results))
    print("DONE_MARKER")

if __name__ == "__main__":
    main()
