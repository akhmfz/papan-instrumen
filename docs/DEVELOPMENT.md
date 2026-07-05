# DEVELOPMENT.md — Panduan Pengembangan

Proyek: **Saham: Papan Instrumen By. Akhmfz**
Platform: TradingView Pine Script v6 | Market: IDX | Status: Alpha

---

## Current Sprint (S007 — Phase A: Beta Readiness)

| Item | Status |
|------|--------|
| **Milestone**: Phase A → v0.3.0-beta | 🟡 In Progress |
| **Sprint**: A1 — Backlog Migration | 🟡 In Progress |
| **Target files**: `.github/`, `scripts/gh-sync.sh`, `docs/` |
| **Scope**: Migrate backlog → GitHub Issues + labels + templates |
| **Next**: A2 — Sector Classification (Consumer/Industri/Healthcare) |

### Active Tasks
| ID | Task | Status |
|----|------|--------|
| A1-001 | GitHub Issues: backlog → issues + labels | ✅ Done |
| A1-002 | Issue templates (feature, bug) | ✅ Done |
| A1-003 | gh-sync.sh auto-create script | ✅ Done |
| A1-004 | User run `bash scripts/gh-sync.sh` | ⏳ After `gh auth login` |

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

Seluruh backlog telah dimigrasi ke **[GitHub Issues](https://github.com/akhmfz/papan-instrumen/issues)**.

Jalankan `bash scripts/gh-sync.sh` (setelah `gh auth login`) untuk auto-create semua issues + labels.

### Issue Labels
| Label | Warna | Use |
|-------|-------|-----|
| `P1-critical` | #d73a4a | Bug kritis, compile error |
| `P2-high` | #f29513 | Fitur dampak besar |
| `P3-medium` | #0e8a16 | UX, docs, improvement |
| `P4-low` | #5319e7 | Long-term ideas |
| `phase-a` `phase-b` `phase-c` | blue/orange/green | Sprint milestone |
| `scoring` `dashboard` `sector` `performance` `docs` `test` | — | Komponen |

---

## External Resources

### Reference
- **[Pine Script v6 Manual](https://www.tradingview.com/pine-script-docs/welcome/)** — Official docs
- **[Pine Coders FAQ](https://www.pinecoders.com/faq_and_code/)** — Bookmark wajib
- **[Pine Coders Utils](https://github.com/pinecoders/pine-utils)** — Reusable snippets & trik
- **[Writing Good Pine](https://www.pinecoders.com/coding_conventions/)** — Coding conventions
- **[What is Repainting?](https://www.tradingview.com/pine-script-docs/en/v5/concepts/Repainting.html)** — Wajib paham

### Tools
- **[pine-script-linter](https://github.com/pine-language-tools)** — Linter + VSCode syntax highlighting
- **[Pine Script Pro (VSCode)](https://github.com/revanthpobala/pinescript-vscode-extension)** — Static analysis & type checking
- **[Script Stopwatch](https://www.tradingview.com/script/rRmrkRDr-Script-Stopwatch-PineCoders-FAQ/)** — Benchmark performa script
- **[pinets-cli](https://www.npmjs.com/package/pinets-cli)** — Run Pine Script locally via CLI
- **[pinescript-mcp](https://www.npmjs.com/package/pinescript-mcp)** — Linting & validation via MCP

### Advanced
- **[120 ticker Screener](https://www.tradingview.com/script/0h0gKNcy-120x-ticker-screener-composite-tickers/)** — Trik bypass 40 request limit
- **[Fundamentals Graphing](https://www.tradingview.com/script/7qjXp2op-Fundamentals-Graphing-Kioseff-Trading/)** — Visualisasi fundamental alternatif
- **[TradingView-Screener (Python)](https://github.com/shner-elmo/TradingView-Screener)** — Screener via API
- **[DSP Techniques](https://www.pinecoders.com/techniques/dsp/)** — Digital Signal Processing di Pine
- **[awesome-pinescript](https://github.com/pAulseperformance/awesome-pinescript)** — Direktori curated lengkap

### PineTS Testing
**[LuxAlgo/PineTS](https://github.com/LuxAlgo/PineTS)** — Runtime + transpiler Pine Script v5/v6 di Node.js.
- `npm test` → `tests/pinets-verify.mjs` — verifikasi 12 fungsi utilitas PapanInstrumen
- `npm run transpile` → `tests/transpile.sh` — syntax check full file via PineTS
- Semua utility functions (f_clamp, f_safeDiv, f_scoreHigher/Lower/Mid/Positive, f_avg3/5) terverifikasi
- Runtime script penuh gagal di `syminfo.tickerid` & `request.financial()` (TradingView-specific, expected)
- Source: [pine-utils](https://github.com/pinecoders/pine-utils) — snippets reusable Pine Coders

### Benchmark
Gunakan **[Script Stopwatch](https://www.tradingview.com/script/rRmrkRDr-Script-Stopwatch-PineCoders-FAQ/)** untuk mengukur performa:
1. Copy Script Stopwatch ke Pine Editor
2. Bungkus logika utama indikator dengan `start/stop` calls
3. Target: < 2 detik load time untuk 90-row table
4. Jika > 2 detik, optimasi paling efektif:
   - Kurangi `request.financial()` calls (cek ulang redundancy)
   - Pindahkan kalkulasi ke luar `barstate.islast` jika memungkinkan
   - Gunakan `var` untuk menyimpan hasil yang tidak berubah per bar
5. Run benchmark setiap major release

### Automation (future)
- **[TradersPost](https://traderspost.io/)** — Webhook → stocks/options/futures
- **[Pine Connector](https://www.pineconnector.com/)** — TradingView → MT4/MT5
- **[AutoView](https://autoview.with.pink/)** — Chrome extension TV alerts → exchange

---

## Changelog

### Build 008 (Current)
**API Budget Optimization**
- Merge `request.security(sym, ...)` market+sector calls → hemat 1 request
- Hapus `enterpriseValue` (display only) → hemat 1 f_stat
- Budget: 37→35 terpakai, sisa 5 slot

### Build 008 (Current)
**API Budget + Dev Tools + PineTS**
- API budget: 37→35 (merge request.security market+sector, hapus enterpriseValue)
- Sektor: 6 watchlist (115 ticker) + f_watchlist()
- No-data guard: f_warningCell, pesan '⚠ DATA TIDAK TERSEDIA'
- Dev: scripts/lint.sh, tests/transpile.sh, tests/pinets-verify.mjs (12 utils verified)
- CI: GitHub Actions (lint → build → verify → transpile → test)
- VSCode: .vscode/extensions.json (Pine Script Pro rec)
- Docs: 16 reference curated dari awesome-pinescript + PineTS + pine-utils

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
