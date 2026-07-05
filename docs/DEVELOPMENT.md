# DEVELOPMENT.md — Panduan Pengembangan

Proyek: **Saham: Papan Instrumen By. Akhmfz**
Platform: TradingView Pine Script v6 | Market: IDX | Status: Alpha

---

## Current Sprint (S006 — Build 007)

| Item | Status |
|------|--------|
| **Task**: Alpha Fix & Polish — hide irrelevant rows, fix thresholds, testing | 🟡 In Progress |
| **Target files**: `src/PapanInstrumen.pine` |
| **Sprint scope**: Hide rows by weight, Interest Cover fix, BBCA+ADRO+TLKM testing |
| **Do NOT**: Change methodology, add request.financial(), add new features |

### Active Tasks
| ID | Task | Status |
|----|------|--------|
| ALPHA-001 | Hide rows by weight in Quality render | ✅ Done |
| ALPHA-002 | Hide rows by weight in Health render | ✅ Done |
| ALPHA-003 | Fix Interest Cover threshold (5-30) | ✅ Done |
| ALPHA-004 | Testing (BBCA, ADRO, TLKM) | ⬜ Pending |
| ALPHA-005 | Update documentation | ✅ Done |
| OPT-001 | Merge request.security(sym) market+sector calls | ✅ Done |
| OPT-002 | Hapus enterpriseValue (display only) | ✅ Done |

### Known Issues
- Securities auto detection perlu validasi lanjutan
- TradingView industry classification tidak konsisten
- Consumer/Industri/Healthcare belum dipisah sebagai kelas sektor
- Banyak field TV tidak terisi utk emiten IDX tertentu

---

## Coding Standard

### Naming Conventions
| Elemen | Gaya | Contoh |
|--------|------|--------|
| Variables | camelCase | `currentRatio` |
| Constants | UPPER_SNAKE_CASE | `MAX_SCORE` |
| Functions | camelCase (diawali kata kerja) | `calculateScore()` |
| Boolean | is/has/can/should prefix | `isBankSector` |

### File Structure (urutan wajib)
1. Header → 2. Indicator Declaration → 3. Inputs → 4. Constants → 5. Colors → 6. Utility Functions → 7. Financial Functions → 8. Sector Functions → 9. Score Calculation → 10. Dashboard Rendering

### Function Rules
- Satu tanggung jawab per function
- Output konsisten
- Max 30-50 baris
- Hindari nested if berlebihan

### Anti-Patterns
- Magic numbers, hardcoded text, duplicate logic
- Silent changes
- Variabel mati / tidak terpakai
- request.financial() tidak perlu

### Commit Convention
```
feat(sector): add insurance classification
fix(valuation): restore financial fallback
docs(methodology): update valuation framework
```

---

## Testing

### 6-Level Testing

| Level | Objective | Status |
|-------|-----------|--------|
| 1 — Compile | No error, no warning | Mandatory |
| 2 — Functional | Dashboard muncul, skor benar | Mandatory |
| 3 — Data Validation | request.financial() valid, handle NA | Mandatory |
| 4 — Sector Validation | Klasifikasi benar semua sektor | Mandatory |
| 5 — Regression | Perubahan baru tidak rusak fitur lama | Mandatory |
| 6 — Performance | Tidak ada request/render berlebihan | Mandatory |

### Manual Test Matrix (12 emiten lintas sektor)
BBCA (Bank), AMAG (Asuransi), TRIM (Sekuritas), ICBP (Consumer), ADRO (Mining), MEDC (Energy), CTRA (Property), JSMR (Infrastructure), GOTO (Technology), KLBF (Healthcare), ASSA (Transportation), ASII (Industrial)

### Bug Classification
- **Critical** (harus fix sebelum release): compile gagal, dashboard tidak muncul, error perhitungan
- **Major** (harus fix sebelum merge): skor/sektor salah, layout rusak
- **Minor** (bisa ditunda): tooltip, warna, alignment, typo

---

## Backlog

### Active
| ID | Task | Priority |
|----|------|----------|
| BL-001 | Refactor Dashboard Layout | P2 |
| BL-002 | Finalisasi cutoff sektor IDX | P2 |
| BL-003 | Validasi klasifikasi seluruh sektor IDX | P2 |
| BL-004 | Optimasi request.financial() | P2 |
| BL-005 | Review metodologi setiap build | P3 |
| BL-007 | Consumer/Industri/Healthcare sebagai kelas sektor terpisah | P2 |
| BL-011 | Batubara vs CPO sebagai kelas terpisah | P3 |

### Future Ideas (Parking Lot)
Compact mode, quality score, capital allocation, earnings quality, economic moat, dynamic sector weight, user guide, macro/technical/portfolio dashboard

---

## Changelog

### Build 008 (Current)
**API Budget Optimization**
- Merge `request.security(sym, ...)` market+sector calls → hemat 1 request
- Hapus `enterpriseValue` (display only) → hemat 1 f_stat
- Budget: 37→35 terpakai, sisa 5 slot

### Build 007 (Previous)
**Alpha Fix & Polish**
- Fix K1: multi-var float declarations split (7→16 baris)
- Fix K2: Valuasi + debtEbitdaScore → f_scoreLowerSafe (negatif=0)
- Fix K3: debtAssetScore threshold 80→0.8 desimal
- Fix K4: n/x denominators sinkron dengan ukuran array aktual
- Fix M1: valueN/qualityN → weight-aware counting
- Fix M2: Income f_avg5 → f_avg4 eksplisit
- S1-S4: Komentar diperbaiki, bankListIDX + source URL, disclaimer Growth Modifier
- Breaking: Interest Cover 5-30→5-50, Dividend Yield 0-5→3-8, f_scoreLowerSafe (negatif=0)

### Build 006
**Indonesia Layer (7th factor)**
- Toggle tampilIndonesia (default OFF backward compatible)
- bobotIndonesia custom (default 1.0)
- FX_IDC:USDIDR fetch + ta.beta() vs IDX Composite
- 3 komponen: indoLiqScore, indoBetaScore, indoMacroScore
- overallScore mendukung 7th factor

### Build 005
**Financial Health — sector thresholds + sub-kategori**
- Sector-aware thresholds + weight matrix
- Sub-kategori Bank/Asuransi/Sekuritas
- Altman Z threshold 1.8-3.5 (US) → 1.1-2.6 (Z"-Score EM)

### Build 004
**Growth Engine — hybrid 2-layer**
- Growth Quality Modifier (±0-20%)
- Bobot per sektor (Finansial, Properti, Infrastruktur, Siklikal, Teknologi, Transportasi)

### Build 004 Rev 1
**Koreksi Growth Engine**
- SGR Teknologi di-skip, Rev ×1.7
- Growth Quality Modifier spread max -40%
- Earnings Quality check via OCF

### Build 003
**Profitability — sector-aware weights**
- Bobot per rasio: wRoe, wRoa, wRoic, wGross, wOp, wNet, wEbitda, wFcfM, wPiotroski

### Build 002
**Valuation + Sektor**
- Pemisahan finansial: Bank, Asuransi, Sekuritas
- Override manual sektor

### Build 001
**Dashboard pertama**
- Dashboard awal, modul valuasi, integrasi data fundamental
