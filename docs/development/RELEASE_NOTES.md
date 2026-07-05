# RELEASE NOTES - v0.1.0-alpha
---
Document ID   : DOC-012
Document Name : RELEASE_NOTES
Version       : 1.0.0
Status        : Active
Owner         : Muhammad Akhmal
Release Date  : 2026-07
---

## Overview

**Saham: Papan Instrumen By. Akhmfz** — Fundamental Dashboard for Indonesian Stock Investors on TradingView.

This is the first alpha release of the project. The dashboard provides a comprehensive fundamental analysis of IDX stocks directly on TradingView charts using Pine Script v6.

---

## Features

### 7 Scoring Dimensions
| # | Dimension | Status | Build |
|---|-----------|--------|-------|
| 1 | **Value** (Valuasi) — Sector-aware weighting | ✅ Complete | B002 |
| 2 | **Quality** (Profitability) — Sector-aware weighting | ✅ Complete | B003 |
| 3 | **Growth** — Hybrid 2-layer (weights + quality modifier) | ✅ Complete | B004 |
| 4 | **Health** — Sector-aware thresholds + sub-kategori Finansial | ✅ Complete | B005 |
| 5 | **Income** (Dividend) | ✅ Complete | B001 |
| 6 | **Momentum** | ✅ Complete | B001 |
| 7 | **Indonesia Factor** — Likuiditas IDX + Stabilitas + Makro (opt-in) | ✅ Complete | B006 |

### Sector Classification
- Otomatis (via syminfo.sector/industry + ticker list)
- Override manual: Bank, Asuransi, Sekuritas, Properti, Infrastruktur, Teknologi, Transportasi, Siklikal, Non-Finansial
- Sub-kategori: Bank, Asuransi, Sekuritas mendapat perlakuan scoring berbeda

### Scoring Features
- Individual ratio scores (0-100) with color-coded bars
- Composite scores per dimension
- Overall composite score (6 or 7 factors)
- Data completeness indicator (n/x)
- Growth Quality Modifier (margin expansion/compression check)
- Earnings Quality check (OCF positivity)

### Risk Module
- Likuiditas & Gorengan detection (separate, not in overall score)
- ARA/ARB proximity proxy
- Market cap tier, volume tier, price tier
- Turnover ratio

### Customization
- 5 color themes (Profesional Gelap, Profesional Terang, Bursa Hijau, Biru Nusantara, Emas Premium)
- Toggle sections on/off
- Custom factor weights
- Table position (4 corners)
- Font size (3 levels)

---

## Technical Specifications

| Aspect | Detail |
|--------|--------|
| Language | Pine Script v6 |
| Platform | TradingView |
| Market | Indonesia Stock Exchange (IDX) |
| Data sources | request.financial() + request.security() |
| External tickers | FX_IDC:USDIDR (exchange rate) |
| Bar requirement | 300 bars minimum |
| Timeframe | Daily (D1) — IDX is EOD-only |
| Table rows | 90 (max), dual column layout |

---

## Known Limitations

1. **Bank-specific data** — CAR, NPL, LDR tidak tersedia di TradingView fields. Bank health scoring bersifat parsial.
2. **Multi-year EPS normalization** — Belum ada normalisasi EPS multi-tahun (keterbatasan request.financial di Pine Script).
3. **Broker summary / kepemilikan** — Tidak tersedia. Modul risiko murni proxy statistik, bukan "bandarmology".
4. **Momentum/RSI thresholds** — Masih menggunakan kalibrasi gaya pasar AS (belum disesuaikan untuk IDX volalitas).
5. **Zero-weight display** — Untuk sektor Finansial di Quality score, f_countValidArr masih menghitung komponen dengan bobot 0 sebagai valid.
6. **IDX EOD-only** — Indikator hanya bekerja pada timeframe Daily.

---

## Install

1. Buka TradingView Pine Editor
2. Copy seluruh isi `src/PapanInstrumen.pine`
3. Paste ke editor
4. Klik "Add to Chart"

Atau import langsung dari GitHub:
```
https://github.com/akhmfz/papan-instrumen/blob/main/src/PapanInstrumen.pine
```

---

## Quick Start

1. Apply indicator to any IDX stock chart (daily timeframe)
2. Default settings work for most users
3. To enable Indonesia Factor: Settings → Pengaturan Utama → Aktifkan Faktor Indonesia
4. To adjust sector: Settings → Sektor & Adaptasi → Deteksi Sektor
5. To customize weights: Settings → Bobot Skor Keseluruhan → Gunakan Bobot Kustom

---

## Disclaimer

Dashboard ini adalah alat bantu analisis, BUKAN nasihat keuangan/investasi.
Seluruh keputusan investasi tetap menjadi tanggung jawab masing-masing pengguna.
Proyek ini tidak memberikan rekomendasi beli maupun jual atas suatu efek.

---

## License

MIT License

---

## Author

**Muhammad Akhmal** — Founder of AKHMFZ Analytics, Indonesia
