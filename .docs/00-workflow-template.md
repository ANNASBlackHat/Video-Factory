# Workflow Template — Research → Assets → Captions → Video

**Use this for any topic:** `raws/<topic>/` → broadened research → 20–50 images → captioned library → HyperFrames storyboard.

> Instances: [`01-investigasi-karhutla.md`](01-investigasi-karhutla.md) (Karhutla Gambut, 29 Aug 2026). Next time just say *"expand raws/<new-topic> like karhutla"* and I follow this template.

---

## 0. Inputs & outputs (contract)

| Folder | You provide | I produce |
|--------|-------------|-----------|
| `raws/<topic>/` | `Topic.md` (research markdown, works cited URLs, optional base64 images) | `assets-collected/` (20–50 imgs, 10–30 MB), `ASSET-INVENTORY.md`, `REPORT-BROADENED-*.md`, `captions-*.json/.md` |
| `scripts/` | (reusable) | `caption_assets.py` + runners |
| `.docs/` | — | `<topic>.md` (this template filled) |
| `videos/` | — | HyperFrames concepts (after captions) |

Naming: `<topic>` is lowercase kebab, e.g. `investigasi-karhutla`, `kebakaran`, `food-estate-papua`. Raw file: `raws/<topic>/<Title>.md`. Colab session: `<topic>-cpu` (CPU) or `<topic>-gpu`.

---

## 1. Parse raw

```bash
# Count unique URLs to scope work
python3 -c "
import re
text=open('raws/<topic>/<File>.md').read()
urls=re.findall(r'https?://[^\s\)\]]+', text)
print(len(set(urls)), 'unique URLs')
# also note inline base64 image* count
print(text.count('[image'))
"
mkdir -p raws/<topic>/assets-collected
```

## 2. Broaden research (websearch)

Run 3–5 queries covering: (a) latest data, (b) failure/controversy, (c) solution.

```
<topic> + data terbaru 2024 2025
<topic> + investigasi gagal
<topic> + solusi <keyword> restorasi
site:youtube.com <topic> dokumenter investigasi
```

Save synthesis to `raws/<topic>/REPORT-BROADENED-*.md` with sections: Executive summary, latest crisis numbers, history, controversy, solution, YouTube list, bibliography.

## 3. Collect assets — chrome-devtools-mcp (required, no guessing)

Every image must be proven via:

```
chrome-devtools-mcp_list_pages -> about:blank
chrome-devtools-mcp_navigate_page -> <URL from Works Cited>
  -> take_snapshot
  -> evaluate_script(() => [...document.querySelectorAll('img')].map(i=>({src:i.src,alt:i.alt})).filter(x=>x.src.startsWith('http')))
  -> bash curl -L -o raws/<topic>/assets-collected/<subfolder>/<name>.jpg <src>
```

Checklist:

- [ ] Visit **all** unique URLs from Works Cited (or log skip reason: PDF/paywall/dup)
- [ ] Extract 3–6 heroes per key domain (slider, peta, foto lapangan)
- [ ] Freeze locally with `curl -L` and keep provenance (URL → file)
- [ ] Record provenance table in `raws/<topic>/ASSET-INVENTORY.md` (URL, status, file, size)
- [ ] Zip for Colab: `zip -r /tmp/<topic>-assets.zip raws/<topic>/assets-collected -x "*.DS_Store"`
- [ ] Target 20–50 files, 10–30 MB (maps + heroes + infographics + 3–4 GIFs if present)

**Provenance table template:**

| # | URL (from Works Cited) | chrome status | Images found | Frozen file |
|---|------------------------|---------------|--------------|-------------|
| 01 | https://... | visited ✓ / timeout / PDF | 5 heroes | `assets-collected/...jpg` |

## 4. Find footage — YouTube (websearch + chrome)

```
websearch: site:youtube.com <topic> dokumenter
chrome: navigate https://www.youtube.com/results?search_query=<topic>+dokumenter
  -> take_snapshot (400 nodes) -> parse 20–30 videos -> split: longform (5–7), breaking (3–4), shorts viral (6–8)
```

Save table with Channel | Link | Duration | Views | Use (hero/explainer/hook) in report.

## 5. Caption assets — Colab (reusable scripts)

**Auth:** `colab 0.6.0` at `~/.local/bin/colab`, default `oauth2` as `annas.developer@gmail.com` (`colab whoami` shows scopes: `cloud-platform`, `colaboratory`, `userinfo.email`). `ADC` not needed. Sessions burn units — always `stop`.

**Provision (CPU fallback — GPU often quota-fails):**

> **TTS (Bahasa VO)** — both runners are now **pluggable** (no code edits): upload
> `tts-lines.json` (+ optional `tts-knobs.json`; OmniVoice also the `.m4a` + matching
> `.srt`) and run `scripts/tts_piper.py` (primary, trained `id_ID` model) or
> `scripts/tts_omnivoice.py` (zero-shot clone). Full recipe + voice transcripts +
> model URLs → [`.docs/04-tts-voice-playbook.md`](04-tts-voice-playbook.md).

```bash
colab new -s <topic>-cpu                # try --gpu T4 first, fallback to CPU on Precondition Failed
colab status -s <topic>-cpu
zip -r /tmp/<topic>-assets.zip raws/<topic>/assets-collected -x "*.DS_Store"
colab upload -s <topic>-cpu /tmp/<topic>-assets.zip /content/<topic>-assets.zip
```

**Scripts (all in `scripts/`):**

- `scripts/caption_assets.py` — modular: `--model {blip-base,blip-large,git-base,florence2,blip2}` `--input` `--out` `--zip` `--device`
  - `blip-base` (223M) — light, generic
  - `blip-large` (385M, 1.88GB) — best CPU (use `beam=1` for FAST, 10s/img)
  - `git-base` (347M) — fastest CPU, good humans
  - `florence2` — dense, needs `transformers==4.38` + kernel restart (fails on 4.55)
  - `blip2` — GPU only

> `colab exec -f` cannot pass args — use `/tmp/run_*.py` wrappers with hardcoded model/zip (see `scripts/README.md`).

**Run:**

```bash
colab exec -s <topic>-cpu -f /tmp/run_blip_large_fast.py   # 44 imgs ~7min CPU
colab exec -s <topic>-cpu -f /tmp/run_git_base.py           # ~1.5min CPU
# Florence-2 needs downgrade: pip install transformers==4.38 inside wrapper + restart-kernel
```

**Download:**

```bash
colab download -s <topic>-cpu /content/captions-blip-large.json /tmp/
cp /tmp/captions-*.json raws/<topic>/
python3 scripts/build_comparison.py  # builds captions-comparison.md
colab stop -s <topic>-cpu
colab log -s <topic>-cpu -o /tmp/<topic>.ipynb  # optional notebook export
```

**Outputs per run:** `raws/<topic>/captions-<model>.json` + `.md` (table), `captions-comparison.md`.

**Model choice:**

- Fast CPU: `git-base` (2s/img)
- Best CPU: `blip-large beam=1`
- Production GPU: `blip2` / `florence-2-large` / `Qwen2-VL` with `<DETAILED_CAPTION>` for domain terms

## 6. Hand off to video

After captions:

1. Pick 6-chapter storyboard (hook → mechanism → history → controversy → law → solution)
2. Map `captions-*.json` → scene roles (`ASSET-INVENTORY` already has hero/kanal/peta tags)
3. Build HyperFrames: `npx hyperframes init videos/<concept> --skill general-video` → dispatch agents with facts lock.

See `PLAYBOOK-longform-to-clip.md` for lint, facts audit, SFX.

---

## 7. Gotchas (from karhutla run)

- T4 `Precondition Failed` → use CPU or `colab run` ephemeral; stop orphan `[?] gpu-t4-...` first.
- `colab exec -f` no args → wrappers.
- Florence-2 pin `4.38` not `4.55/4.44`.
- BLIP-large beam=5 too slow on CPU → beam=1.
- Paywalls/PDFs → log skip reason, don't hallucinate.

---

## 8. Template checklist for next topic

- [ ] `raws/<new-topic>/<File>.md` added
- [ ] Ran §1 parse (URL count)
- [ ] Ran §2 websearch + report
- [ ] Ran §3 chrome 10–15 navigations + provenance table
- [ ] Ran §4 YouTube 20–30 videos table
- [ ] Ran §5 Colab 2–3 models + comparison
- [ ] Updated `PLAYBOOK-concept-to-video.md#workflows` with new row: `| 0N | <Title> | raw | .docs/<new-topic>.md | assets | captions | ✅ |`
- [ ] Copied this template → `.docs/<new-topic>.md` and filled placeholders
- [ ] Wrote `raws/<topic>/tts-lines.json` (VO script) — numbers in natural form; optional `tts-knobs.json` (see § TTS + `.docs/04-tts-voice-playbook.md`)

Next invocation: *"expand raws/<new-topic> like karhutla using the template"*.
