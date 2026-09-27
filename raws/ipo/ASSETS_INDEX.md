# 📁 IPO Video Production Asset Index & Media Registry

This registry catalogues all media assets, logos, product photos, and live web browser screenshots captured during the investigative research phase. All files are stored locally in [`raws/ipo/assets/`](assets/).

---

## 🖼️ Media & Screenshot Catalogue

| File Name | Format / Resolution | Source / Origin | Description & Context | Recommended Video Role |
| :--- | :--- | :--- | :--- | :--- |
| **[`swap_logo_eipo.jpg`](assets/swap_logo_eipo.jpg)** | JPEG (1280x709) | `e-ipo.co.id` | Official high-resolution company branding banner for PT Swayasa Prakarsa Tbk | Title card / Intro hero graphic / Ticker reveal |
| **[`swayasa_logo.jpg`](assets/swayasa_logo.jpg)** | JPEG (300x94) | `gamamulti.com` | Official corporate logo of PT Swayasa Prakarsa | Corporate hierarchy overlay & watermarks |
| **[`ugm_logo.png`](assets/ugm_logo.png)** | PNG (192x200) | `ugm.ac.id` | Official Universitas Gadjah Mada (UGM) crest logo | UGM academic affiliation & research origin |
| **[`gamamulti_logo.png`](assets/gamamulti_logo.png)** | PNG (200x27) | `gamamulti.com` | Official PT Gama Multi Usaha Mandiri holding company logo | Parent company holding structure breakdown |
| **[`idx_logo.png`](assets/idx_logo.png)** | WebP (200x195) | `idx.co.id` | Official Indonesia Stock Exchange (Bursa Efek Indonesia / BEI) logo | Listing section / Market overview / Ticker card |
| **[`ojk_logo.png`](assets/ojk_logo.png)** | PNG (114x51) | `ojk.go.id` | Official Otoritas Jasa Keuangan (OJK) regulatory logo | Regulatory approval / Syariah compliance badge |
| **[`swayasa_ojk_event.jpg`](assets/swayasa_ojk_event.jpg)** | JPEG (900x506) | `gamamulti.com` | Corporate photo of SWAP & GMUM directors during bookbuilding preparation | Management & corporate governance b-roll |
| **[`gamacha_product_box.jpg`](assets/gamacha_product_box.jpg)** | JPEG (669x500) | `ugm.ac.id` | Close-up photo of Gama-CHA halal bone graft/filler product packaging | Medical device product highlight (Heprogama) |
| **[`gamacha_ceremony.jpg`](assets/gamacha_ceremony.jpg)** | JPEG (669x500) | `ugm.ac.id` | Launching ceremony and presentation of Gama-CHA by UGM researchers | Innovation / Academic research commercialization |
| **[`e_ipo_index.png`](assets/e_ipo_index.png)** | PNG (1080x552) | `e-ipo.co.id/id/ipo/index` | Live browser capture of the e-IPO pipeline list showing active bookbuilding | Scene 1 market context / e-IPO portal visual |
| **[`e_ipo_swap_detail.png`](assets/e_ipo_swap_detail.png)** | PNG (1080x552) | `e-ipo.co.id/id/ipo/355/swap...` | Viewport screenshot of PT Swayasa Prakarsa Tbk offering parameters | Offering parameters (Price, shares, dates) |
| **[`e_ipo_swap_detail_full.png`](assets/e_ipo_swap_detail_full.png)** | PNG (1080x1723) | `e-ipo.co.id/id/ipo/355/swap...` | Full-page vertical screenshot of the entire e-IPO SWAP filing | Scrolling UI b-roll / In-depth prospectus review |
| **[`gamamulti_home.png`](assets/gamamulti_home.png)** | PNG (1080x552) | `gamamulti.com` | Live browser screenshot of Gama Multi Group corporate portal | Corporate ecosystem & subsidiary network |
| **[`ugm_gamacha_news.png`](assets/ugm_gamacha_news.png)** | PNG (1080x552) | `ugm.ac.id/id/berita/...` | Live browser screenshot of UGM news portal covering medical device innovation | Academic pedigree & R&D credibility |
| **[`idx_homepage.png`](assets/idx_homepage.png)** | PNG (1080x552) | `idx.co.id/id/` | Live browser capture of the Indonesia Stock Exchange homepage | Indonesian capital markets backdrop |
| **[`ojk_homepage.png`](assets/ojk_homepage.png)** | PNG (1080x552) | `ojk.go.id` | Live browser capture of Financial Services Authority portal | Regulatory milestone beat |
| **[`e_ipo_emmi_detail.png`](assets/e_ipo_emmi_detail.png)** | PNG (1080x552) | `e-ipo.co.id/id/ipo/351/emmi...` | Screenshot of peer PT Esa Medika Mandiri Tbk listing page | Healthcare sector comparative analysis |
| **[`e_ipo_prdl_detail.png`](assets/e_ipo_prdl_detail.png)** | PNG (1080x552) | `e-ipo.co.id/id/ipo/350/prdl...` | Screenshot of peer PT Prodia Diagnostic Line Tbk listing page | Healthcare sector comparative analysis |

---

## 🎯 Direct Integration Guide for Remotion

In your Remotion compositions, you can reference these assets using `staticFile()` or relative paths:

```tsx
import { staticFile, Img } from "remotion";

// Example logo usage:
<Img src={staticFile("raws/ipo/assets/swap_logo_eipo.jpg")} className="rounded-xl shadow-2xl" />

// Example UI mockups inside browser frames:
<Img src={staticFile("raws/ipo/assets/e_ipo_swap_detail.png")} className="w-full object-cover" />
```
