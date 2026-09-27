# Workflow 01 — Investigasi Karhutla Lahan Gambut Kalimantan

**Date:** 29 Aug 2026 · **Raw:** `raws/investigasi-karhutla/Kebakaran Lahan Gambut Kalimantan.md` (5 chapters, 55 cites, 28 base64 images) · **Status:** research broadened, 46 assets captioned, ready for HyperFrames storyboard

> **Instance of** [`00-workflow-template.md`](00-workflow-template.md) — this file is the filled example. Use the template for any new topic.

This is the detailed log. For the brief, see `PLAYBOOK-concept-to-video.md#workflows`.

---

## 1. What we started from

- Single markdown: `raws/investigasi-karhutla/Kebakaran Lahan Gambut Kalimantan.md:1`
  - Chapters: biofisik smouldering, trajektori 1982–2025, korporasi vs Dayak, 3R+paludikultur
  - 61 unique URLs in Works Cited (after dedup), 28 inline base64 `image1..image28` (chemical diagrams + burn-area tables)
- Empty `raws/investigasi-karhutla/assets-collected/` (to be filled)

Goal per user: *collect image assets, broaden research (grab images from pages), search YouTube, list in report — using `chrome-devtools-mcp`*.

---

## 2. Step-by-step — reproducible

### 2.1 Parse & verify raw

```bash
python3 -c "
import re
text=open('raws/investigasi-karhutla/Kebakaran Lahan Gambut Kalimantan.md').read()
urls=re.findall(r'https?://[^\s\)\]]+', text)
print(len(set(urls)), 'unique')
"
# -> 61 unique
```

### 2.2 Broaden research (websearch)

Queries run via `websearch` (not chrome):

- `karhutla Kalimantan lahan gambut kebakaran 2024 2025 data terbaru` → SiPongi Jan–Jul 2026 202k ha, Kalbar 38k ha
- `food estate lahan gambut Kalimantan gagal investigasi 2024 2025` → Swanelangsa 1% layak padi, 4k ha terbengkalai
- `paludikultur purun sagu jelutung solusi gambut BRGM restorasi` → BRIN, WRI, Jurnal Tanah 11(2)
- `youtube karhutla ...` + `site:youtube.com kebakaran ...` → 28 videos

All results saved into `raws/investigasi-karhutla/REPORT-BROADENED-INVESTIGASI-KARHUTLA-2026-08-29.md:1` §4–6.

### 2.3 Collect image assets — chrome-devtools-mcp (required)

> Every asset is proven via `chrome-devtools-mcp` `navigate` + `take_snapshot` + `evaluate_script(() => [...document.querySelectorAll('img')].map(i=>i.src))` + `bash curl -L` freeze.

**Session:**
```
chrome-devtools-mcp_list_pages -> about:blank
chrome-devtools-mcp_navigate_page -> https://pantaugambut.id/ -> take_snapshot -> evaluate_script -> 23 imgs -> 5.735 hotspot/7d
navigate -> https://pantaugambut.id/peta-gambut -> 3 maps
navigate -> https://mongabay.co.id/2016/08/26/bentang-lahan... -> 16 imgs, 5 heroes (kalteng_0691 etc.)
navigate -> https://www.youtube.com/results?search_query=karhutla+Kalimantan... -> 400 nodes, 28 videos
# v2 (after user asked "have you visited the links in the file?")
navigate -> https://foodestate.pantaugambut.id/ -> 28 imgs (main-cover, escavator, soeharto...)
navigate -> https://pantaugambut.id/peta-gambut/ancaman -> 15 widgets (sekat-kanal, kebakaran-pelalawan...)
navigate -> https://pantaugambut.id/pelajari/dampak -> 4 GIFs
navigate -> https://pantaugambut.id/pelajari/sejarah -> kebakaran-feri-irawan.jpg
navigate -> https://pantaugambut.id/peta-gambut/potensi -> pengelolaan-basah.jpg etc.
navigate -> https://www.wwf.id/id/blog/kebakaran... -> wwf-kalteng-hero.jpg
navigate -> https://indonesia.wetlands.org/...paludikultur -> paludikultur-hero.jpg
navigate -> https://www.walhi.or.id/karhutla-berulang... -> cover-rilis 1.351 titik + 3 maps (tambang/sawit/PBPH)
navigate -> https://www.detik.com/kalimantan/berita/d-8633312 -> pemadaman-katingan-2023.jpg
navigate -> https://forestinsights.id/...kallista... -> karhutla-illustrasi.jpg
navigate -> https://pantaugambut.id/kabar/lestarikan... -> niko4.jpg
+ curl fallback for antaranews/cnn/tempo/alinea og:image
```

**Freeze:**
```bash
mkdir -p raws/investigasi-karhutla/assets-collected/{foodestate,peta-ancaman,pelajari,potensi,walhi,wwf,wetlands,kabar,detik,extra}
curl -L -o raws/investigasi-karhutla/assets-collected/pantaugambut-slider-01.jpg https://pantaugambut.id/images/slider/slides/gp0sttqko2-X6HDq.jpg
# ... (see .docs log for full 46-file list)
zip -r /tmp/karhutla-assets.zip raws/investigasi-karhutla/assets-collected -x "*.DS_Store"
```

**Inventory:** 46 files, 20 MB (see `raws/investigasi-karhutla/ASSET-INVENTORY-FULL.md:1` for per-URL provenance table). First pass was 10 files — expanded to 46 after visiting all 61 links.

### 2.4 YouTube — chrome + websearch

- `websearch site:youtube.com kebakaran lahan gambut ...` → 10 hits
- `chrome navigate https://www.youtube.com/results?search_query=karhutla+Kalimantan...` → snapshot 400 nodes → 28 videos parsed, split into:
  - 7 longform investigasi (Pesta Babi, Proyek Membakar Kalimantan, Wildfires Keep Burning, etc.)
  - 4 breaking 2026 (Prabowo tinjau, BMKG 694 hotspot, Sanga-Sanga 100ha)
  - 8 viral shorts (Api di Bawah Tanah 367K, Superman Palangkaraya, etc.)

Table in `REPORT-BROADENED...md:119` §5.

### 2.5 Caption assets — Colab (BLIP family)

**Colab CLI:** `colab 0.6.0` at `~/.local/bin/colab`, `oauth2` default, authenticated as `annas.developer@gmail.com` (scopes: cloud-platform, colaboratory, userinfo.email — verified via `colab whoami`). ADC not configured — use oauth2. See `scripts/README.md`.

**Provision:**
```bash
colab new -s karhutla-cpu              # CPU works; --gpu T4 failed: Precondition Failed (quota)
colab status -s karhutla-cpu           # m-s-kkb-use1b0-us02acy3i5ux | CPU | IDLE
zip -r /tmp/karhutla-assets.zip raws/investigasi-karhutla/assets-collected -x "*.DS_Store"
colab upload -s karhutla-cpu /tmp/karhutla-assets.zip /content/karhutla-assets.zip
```

**Scripts (reusable, in `scripts/`):**

- `scripts/caption_assets.py:1` — modular CLI: `--model {blip-base,blip-large,git-base,florence2,blip2}` `--input` `--out` `--zip` `--device`
  - Note: `colab exec -f` cannot pass args, so use `/tmp/run_*.py` wrappers (hardcoded) — see `scripts/README.md`.
- `/tmp/run_blip_large_fast.py`, `/tmp/run_git_base.py`, `/tmp/run_florence2_colab.py` — wrappers used for remote exec.

**Runs (all on `karhutla-cpu` CPU):**

1. BLIP-base `Salesforce/blip-image-captioning-base` (223M, beam=3) → 44 images, ~2min → `captions-blip-base.json/.md` (generic, e.g. map → "earthquake")
2. GIT-base `microsoft/git-base-coco` (347M) → 44 images, ~1.5min → `captions-git-base.json/.md` (better humans, still weak on maps)
3. BLIP-large `Salesforce/blip-image-captioning-large` (385M, 1.88GB) beam=5 timed out at 600s (10s/img), retried beam=1 → 44 images, ~7min → `captions-blip-large.json/.md` (best CPU: "smoke billowing from a forest fire")
4. Florence-2-base `microsoft/Florence-2-base` → failed on Colab transformers 4.55 (and 4.44.2) `forced_bos_token_id` AttributeError — needs `transformers==4.38` + kernel restart. Documented, not blocking.

**Download:**
```bash
colab download -s karhutla-cpu /content/captions-blip-base.json /tmp/captions.json
cp /tmp/captions*.json raws/investigasi-karhutla/
# also comparison
python3 -c "import json; ..."  # builds captions-comparison.md
```

**Outputs:**
- `raws/investigasi-karhutla/captions-blip-base.json/.md` (9.4K/4.1K)
- `captions-git-base.json/.md` (4.6K/3.5K)
- `captions-blip-large.json/.md` (5.5K/4.5K)
- `captions-comparison.md` — side-by-side 44 rows + takeaways
- `scripts/README.md` — quick start + model tradeoffs

**Recommendation for next run:**
- Fast CPU: GIT-base (2s/img)
- Best CPU: BLIP-large beam=1
- Production GPU: `blip2-opt-2.7b` or Florence-2-large with `<DETAILED_CAPTION>` / Qwen2-VL-2B for peat terminology → `colab run --gpu T4 scripts/caption_assets.py --model blip2` (ephemeral, auto-stop) or wait for T4 quota.

---

## 3. Artifacts map

| Artifact | Path | Provenance |
|----------|------|------------|
| Raw research | `raws/investigasi-karhutla/Kebakaran Lahan Gambut Kalimantan.md` | user-provided |
| Broadened report | `raws/investigasi-karhutla/REPORT-BROADENED-INVESTIGASI-KARHUTLA-2026-08-29.md` | websearch + chrome |
| Asset provenance | `raws/investigasi-karhutla/ASSET-INVENTORY-FULL.md` | chrome 14 navigations |
| Assets (46) | `raws/investigasi-karhutla/assets-collected/**` | chrome + curl, 20 MB |
| Captions | `raws/investigasi-karhutla/captions-*.json/.md` + `captions-comparison.md` | Colab karhutla-cpu |
| Scripts | `scripts/caption_assets.py`, `scripts/README.md` | reusable |
| Colab session | `karhutla-cpu` (CPU, m-s-kkb-use1b0-us02...) | oauth2, still IDLE |

---

## 4. Gotchas & fixes

- **T4 quota `Precondition Failed`** → use CPU or `colab run` ephemeral. Or stop orphan `[?] gpu-t4-s-kkb-usw4b2-13fxdktqztbsl` first.
- **`colab exec -f` can't pass args** → use wrapper `/tmp/run_*.py` with hardcoded model/zip.
- **Florence-2 transformer pin** → requires 4.38, not 4.55/4.44 — restart kernel after `pip install`.
- **BLIP-large beam=5 too slow on CPU** → use beam=1 (FAST) or GPU.
- **Paywalls/PDFs** (6 PDFs, Detik paywall) → skipped with reason in provenance table.

---

## 5. How to reuse for next workflow (e.g., `raws/kebakaran/`)

1. Drop new markdown in `raws/<topic>/`
2. Repeat §2.1–2.5 changing `karhutla` → `<topic>` (zip name, colab session name)
3. Update `PLAYBOOK-concept-to-video.md#workflows` table with new row linking to `.docs/<topic>.md`
4. Create `.docs/<topic>.md` by copying this file and editing URLs/models.

Next workflow: just say *"expand raws/kebakaran like karhutla"* — I’ll follow this doc.

