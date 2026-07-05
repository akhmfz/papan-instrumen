# Saham: Papan Instrumen By. Akhmfz

> All-in-One Fundamental Dashboard for Indonesian Stock Market — built with Pine Script v6.

[![Version](https://img.shields.io/badge/version-v0.1.0--alpha-blue)](https://github.com/akhmfz/papan-instrumen/releases)
[![Pine Script](https://img.shields.io/badge/Pine%20Script-v6-green)](https://www.tradingview.com/pine-script-docs/en/v6/)
[![Build](https://img.shields.io/badge/build-B006-orange)]()
[![Market](https://img.shields.io/badge/Market-IDX-red)]()
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

---

## Quick Start

```
1. Buka TradingView → Pine Editor
2. Copy src/PapanInstrumen.pine → Paste → Add to Chart
3. Sesuaikan sektor via Settings jika auto-detect salah
```

---

## Screenshot

![Dashboard Preview](assets/screenshot.svg)
*Tampilan dashboard di chart TradingView — detail tampilan bisa disesuaikan via Settings (tema, posisi, ukuran teks, toggle section).*

---

## Overview

**Papan Instrumen** adalah dashboard analisis fundamental khusus **Pasar Modal Indonesia (IDX)** — 7 dimensi scoring yang dinormalisasi per sektor, bukan angka mentah tanpa konteks.

Dirancang untuk menjawab masalah utama investor Indonesia:
- Data fundamental tersebar di banyak platform
- Dashboard luar negeri menggunakan asumsi pasar AS
- Rasio fundamental berbeda relevansinya per sektor IDX

---

## 7 Scoring Dimensions

| # | Dimensi | Metodologi |
|---|---------|-----------|
| 1 | **Value** (Valuasi) | Sector-aware weighting, 10 rasio |
| 2 | **Quality** (Profitability) | Sector-aware weighting, 9 rasio |
| 3 | **Growth** | Hybrid 2-layer (weights + quality modifier) |
| 4 | **Health** | Sector-aware thresholds + sub-kategori Finansial |
| 5 | **Income** (Dividend) | Standard scoring |
| 6 | **Momentum** | RSI, 52W position, RS vs Index |
| 7 | **Indonesia Factor** *(opt-in)* | Likuiditas IDX + Beta + Makro (IDR) |

**Indonesia Factor** adalah dimensi ke-7 yang menangkap karakteristik unik IDX — tersedia via toggle (default OFF untuk backward compatibility).

---

## Sector Classification

| Sektor | Deteksi | Override Manual |
|--------|---------|----------------|
| Bank | Auto via ticker list + industry field | ✅ |
| Asuransi | Auto via industry field | ✅ |
| Sekuritas | Auto (best-effort) | ✅ |
| Properti | Auto via sector/industry | ✅ |
| Infrastruktur | Auto via sector/industry | ✅ |
| Teknologi | Auto via sector/industry | ✅ |
| Transportasi | Auto via sector/industry | ✅ |
| Siklikal (Komoditas/Energi) | Auto via sector/industry | ✅ |
| Non-Finansial Umum | Fallback default | ✅ |

Masing-masing sektor mendapat perlakuan scoring berbeda: bobot rasio disesuaikan, threshold dilonggarkan/dipersempit, dan rasio tertentu di-skip jika tidak relevan.

---

## Scoring Features

- **Individual ratio scores** (0-100) dengan color-coded visual bar
- **Composite scores** per dimensi + **overall composite**
- **Data completeness indicator** (n/x) — transparansi data availability
- **Growth Quality Modifier** — deteksi margin expansion/compression
- **Earnings Quality check** — OCF positivity (Piotroski proxy)
- **Risk Module** (separate) — Likuiditas & Gorengan detection

---

## Customization

| Fitur | Opsi |
|-------|------|
| Color Themes | 5 tema (Gelap, Terang, Hijau, Biru, Emas) |
| Table Position | 4 pojok |
| Font Size | 3 level |
| Toggle Sections | Per dimensi (ON/OFF) |
| Custom Weights | Bobot kustom per dimensi |
| Indonesia Factor | Opt-in (default OFF) |

---

## Current Status

```
Version  : v0.1.0-alpha
Build    : Build 006
Status   : Active Development
Phase    : Alpha Release — Code Complete
Next     : Beta Release
```

---

## Roadmap

### ✅ Completed (Phase 1)
- [x] Repository Initialization
- [x] Project Architecture
- [x] Fundamental Research
- [x] **Valuation Engine** (Build 002 — sector-aware weighting)
- [x] **Profitability Engine** (Build 003 — sector-aware weights)
- [x] **Growth Engine** (Build 004 — hybrid 2-layer + quality modifier)
- [x] **Financial Health Engine** (Build 005 — sector thresholds + sub-kategori)
- [x] **Indonesia Layer** (Build 006 — 7th factor, opt-in)
- [x] **Alpha Release** (v0.1.0-alpha)

### 🚧 Upcoming
- [ ] Beta Release (feedback, bug fixes, optimization)
- [ ] Stable Release (v1.0.0)

---

## Tech Stack

| Teknologi | Penggunaan |
|-----------|-----------|
| Pine Script v6 | Core indicator |
| TradingView | Platform |
| Git + GitHub | Version control |
| RTK | Token optimization (dev) |
| Markdown | Documentation |

---

## Development Principles

- **Methodology Before Code** — setiap skor punya dasar riset
- **Performance Over Features** — ringan & cepat adalah prioritas
- **IDX First** — parameter pasar AS tidak relevan untuk IDX
- **No Silent Changes** — semua perubahan tercatat di CHANGELOG
- **Living Documentation** — dokumen hidup, bukan artefak

---

## Repository Structure

```
docs/
├── AI.md              — AI collaboration context & workflow
├── ARCHITECTURE.md    — Arsitektur, metodologi, roadmap
└── DEVELOPMENT.md     — Coding standard, testing, changelog, backlog
src/
└── PapanInstrumen.pine  — Main indicator (~1680 lines)
assets/
└── screenshot.svg       — Dashboard preview
```

---

## Manual Testing Coverage

| Sektor | Emiten | Status |
|--------|--------|--------|
| Bank | BBCA | ✅ |
| Coal/Energy | ADRO | ✅ |
| CPO/Plantation | AALI | ✅ |
| Infrastructure | TLKM | ✅ |
| Consumer | UNVR | ✅ |
| Property | PWON | ✅ |

---

## Contributing

Saat ini masih tahap alpha internal. Kontribusi publik akan dibuka setelah Beta Release.

---

## Disclaimer

**Papan Instrumen** adalah alat bantu analisis — **BUKAN** nasihat keuangan atau investasi. Skor "Risiko Likuiditas" adalah proxy statistik berbasis harga & volume historis, bukan deteksi manipulasi pasar terverifikasi. Seluruh keputusan investasi tetap tanggung jawab masing-masing pengguna.

---

## License

MIT License — lihat [LICENSE](LICENSE).

---

## Author

**Muhammad Akhmal** — Founder of AKHMFZ Analytics, Indonesia

[TradingView](https://www.tradingview.com/u/akhmfz/) · [LinkedIn](https://linkedin.com/in/Akhmfz) · akhmfz.analytics@gmail.com
