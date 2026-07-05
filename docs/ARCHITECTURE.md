# ARCHITECTURE.md — Arsitektur, Metodologi & Roadmap

Proyek: **Saham: Papan Instrumen By. Akhmfz**
Platform: TradingView Pine Script v6 | Market: IDX | Status: Alpha

---

## Executive Summary

Dashboard fundamental khusus **Pasar Modal Indonesia (IDX)** — 7 dimensi scoring yang dinormalisasi per sektor. Bukan sekadar adaptasi dashboard luar negeri.

### Problem Statement
- Data fundamental tersebar
- Dashboard luar negeri pakai asumsi pasar AS
- Rasio fundamental beda relevansinya per sektor IDX
- Investor pemula sulit menentukan metrik penting

### Target Users
- Investor saham Indonesia, swing/position trader, value/growth investor
- Mahasiswa pasar modal, komunitas KSPM, edukator

---

## Arsitektur Teknis

### 7-Layer Architecture

```
Layer 1: Configuration (input pengguna, tidak ada perhitungan)
Layer 2: Data Layer (request.financial() & request.security())
Layer 3: Sector Engine (klasifikasi sektor)
Layer 4: Calculation Engine (hitung rasio, hanya angka)
Layer 5: Scoring Engine (ubah angka jadi skor 0-100)
Layer 6: Interpretation Engine (konteks: "normal utk sektor Bank")
Layer 7: Dashboard Renderer (tampilkan hasil, tidak boleh hitung data)
```

### Source Code Structure (urutan wajib)

```
Header → Input → Constant → Financial Request → Sector Engine → Calculation Engine → Scoring Engine → Interpretation Engine → Dashboard → Alert
```

### Module Dependency (tidak boleh ada dependency terbalik)

```
Configuration → Data Layer → Sector Engine → Calculation Engine → Scoring Engine → Interpretation Engine → Dashboard
```

### Request Budget

| Tipe | Jumlah | Keterangan |
|------|--------|-----------|
| `request.security()` | 3 | market+sector (merged), benchmark, FX |
| `request.financial()` via f_fin | 11 | margin, growth, cash flow |
| `request.financial()` via f_stat | 19 | valuation, profitability, health |
| `request.financial()` via f_ttm | 2 | EPS, revenue TTM |
| **Total** | **35** | **Sisa: 5** |

Aturan: Setiap field baru HARUS menggantikan field existing. Update tabel setiap ada perubahan.

---

## Metodologi Scoring

Dashboard ini **bukan** stock screener, signal generator, atau sistem rekomendasi jual/beli.

### 5 Pilar Analisis

| Pilar | Contoh Rasio |
|-------|-------------|
| Valuation | PER, PBV, EV/EBITDA, PEG |
| Profitability | ROE, ROA, Net Margin, Operating Margin |
| Growth | Revenue Growth, EPS Growth, Net Income Growth |
| Financial Health | Current Ratio, DER, Interest Coverage |
| Shareholder Return | Dividend Yield, Payout Ratio |

### 7 Dimensi Scoring

| # | Dimensi | Build | Method |
|---|---------|-------|--------|
| 1 | Value (Valuasi) | B002 | Sector-aware weighting, 10 rasio |
| 2 | Quality (Profitability) | B003 | Sector-aware weighting, 9 rasio |
| 3 | Growth | B004 | Hybrid 2-layer (weights + quality modifier) |
| 4 | Health | B005 | Sector thresholds + sub-kategori Finansial |
| 5 | Income (Dividend) | B001 | Standard scoring |
| 6 | Momentum | B001 | RSI, 52W position, RS vs Index |
| 7 | Indonesia Factor | B006 | Likuiditas IDX + Beta + Makro (opt-in) |

### Sector Classification

10 sektor dengan perlakuan scoring berbeda: Bank, Asuransi, Sekuritas, Properti, Infrastruktur, Teknologi, Transportasi, Siklikal (Komoditas/Energi), Non-Finansial Umum.

### Scoring Principles

1. **Sector Aware** — Rasio tidak berlaku sama di semua sektor (DER penting utk Consumer, kurang relevan utk Bank)
2. **Context Before Score** — Skor tanpa konteks menyesatkan
3. **Transparency** — Tidak ada black box scoring, semua metodologi terdokumentasi

### Limitations

- Bergantung data TradingView (tidak semua metrik tersedia utk IDX)
- Tidak menggantikan analisis laporan keuangan
- Tidak memperhitungkan makroekonomi secara langsung

---

## Roadmap

| Phase | Status | Deskripsi |
|-------|--------|-----------|
| 1. Repository Foundation | ✅ | README, arsitektur, standar |
| 2. Fundamental Engine | ✅ | Valuation, Profitability, Growth, Health, Dividend |
| 3. Sector Intelligence | 📅 | Sector mapping, weight, override |
| 4. Dashboard Experience | 📅 | Layout, color, compact, mobile |
| 5. Optimization | 📅 | Performa, memory, rendering |
| 6. Alpha Release | ✅ | v0.1.0-alpha |
| 7. Beta Release | ✅ | v0.3.0-beta — Phase A+B complete (15 sektor, compact, i18n, presets, 89 tests) |
| 8. Stable Release | 📅 | v1.0.0 |

### Versioning
- **Major**: perubahan metodologi
- **Minor**: fitur baru
- **Patch**: bug fix & optimasi
