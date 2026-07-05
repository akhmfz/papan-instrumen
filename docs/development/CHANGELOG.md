# CHANGELOG.md
---
Document ID   : DOC-011
Document Name : CHANGELOG
Version       : 1.0.0
Status        : Active
Owner         : Muhammad Akhmal
Architect     : ChatGPT
Last Updated  : 2026
Review Cycle  : Every Build
---
# Purpose
Dokumen ini mencatat seluruh perubahan yang terjadi pada proyek.
Seluruh perubahan implementasi, refactoring, bug fixing, maupun perubahan metodologi wajib dicatat di sini.
Tidak boleh ada perubahan penting yang tidak terdokumentasi.
---
# Changelog Policy
Setiap Build wajib mencatat:
- Tujuan perubahan
- File yang diubah
- Ringkasan perubahan
- Dampak
- Breaking Change
- Risiko
- Cara pengujian
---
# Version History
---
# Build 004
Status
Current Development
Sprint
Sprint 003
Date
YYYY-MM-DD
---
## Objective
Menerapkan hybrid 2-layer Growth Engine: sector-aware weighting (Layer 1) + Growth Quality Modifier (Layer 2).
---
## Files Modified
```
PapanInstrumen.pine
CURRENT_SPRINT.md
CHANGELOG.md
BACKLOG.md
```
---
## Added
- Growth Quality Modifier: menyesuaikan skor ±0-20% berdasarkan spread Rev vs EPS
- Bobot per-sektor: wGRev, wGEps, wGSgr untuk Finansial, Properti, Infrastruktur, Siklikal, Teknologi, Transportasi
---
## Changed
- Growth Score dari f_avg3 menjadi f_wavgArr (Layer 1) + Growth Quality Modifier (Layer 2)
---
## Fixed
- Tidak ada bug fix.
---
## Removed
Tidak ada.
---
## Performance Impact
Low
Tidak ada penambahan request.financial().
---
## Breaking Change
Minimal.
Non-Finansial Umum dengan spread Rev-EPS ≥ 0: growthScore identik Build 003.
Untuk spread negatif, skor dikurangi maksimal 20%.
---
## Testing
Manual Testing
Lintas sektor IDX.
Compile Test
Pending
Regression Test
Pending
---
## Engineering Notes
- Siklikal: EPS×0.2, SGR×0.3 — sengaja drastis, EPS/SGR semu karena siklus.
- Teknologi: SGR×0.5 — banyak rugi, SGR negatif tidak informatif.
- Growth Quality Modifier hanya aktif untuk spread negatif (margin compression).
---
# Build 004 Rev 1
Status
Current Development
Sprint
Sprint 003
Date
YYYY-MM-DD
---
## Objective
Koreksi Growth Engine berdasarkan riset metodologi (Piotroski, AQR, Higgins SGR).
---
## Files Modified
```
PapanInstrumen.pine
CURRENT_SPRINT.md
CHANGELOG.md
BACKLOG.md
```
---
## Changed
- Finansial: SGR ×1.7 (↑ dari ×1.5), EPS ×1.0 (↓ dari ×1.3)
- Teknologi: SGR di-skip (w=0), Rev ×1.7 (↑ dari ×1.5)
- Infrastruktur: Rev ×1.1 (↓ dari ×1.2)
- Growth Quality Modifier: spread progresif max -40% (↑ dari -20%) dengan multiplier 0.6
- Earnings Quality check via OCF (Piotroski proxy) ditambahkan ke modifier
- growthN sekarang hanya hitung komponen dengan bobot > 0
---
## Fixed
- SGR untuk Teknologi di-skip karena ROE negatif membuat SGR tidak informatif
- EPS Finansial diturunkan karena provisi kredit bisa dimanipulasi
---
## Breaking Change
Minimal.
Non-Finansial Umum tetap identik Build 003.
---
## Performance Impact
Low
Tidak ada penambahan request.financial().
---
## Engineering Notes
- Rev 1 didasarkan pada riset: Piotroski F-Score (point 4: OCF quality),
  AQR Quality Factor (earnings quality), dan Higgins SGR (1977).
- Sumber rujukan: Piotroski (2000), Asness/Frazzini/Pedersen (2019).
---
# Build 005
Status
Current Development
Sprint
Sprint 004
Date
YYYY-MM-DD
---
## Objective
Menerapkan sector-aware thresholds + weight matrix + sub-kategori Bank/Asuransi/Sekuritas pada Financial Health Engine.
---
## Files Modified
```
PapanInstrumen.pine
CURRENT_SPRINT.md
CHANGELOG.md
BACKLOG.md
```
---
## Added
- Threshold parameters per sektor: debtEqG/B, debtEbitdaG/B, currL/I/H, intBad/Good, altmanBad/Good
- Weight matrix: wHDe, wHDa, wHDeB, wHNetD, wHCash, wHIC, wHCR, wHQR, wHAltman, wHOCF, wHFCF
- Sub-kategori Bank, Asuransi, Sekuritas dengan penanganan berbeda
---
## Changed
- HealthScore dari f_avg5/3 menjadi f_wavgArr (11 rasio, sector-aware)
- Altman Z threshold dari 1.8-3.5 (US) → 1.1-2.6 (Z"-Score EM)
- Rendering: sub-kategori menampilkan rasio yang relevan saja
---
## Fixed
- Bank/Asuransi/Sekuritas tidak lagi digabung sebagai isFinancialSector
---
## Performance Impact
Low
Tidak ada penambahan request.financial().
---
## Breaking Change
Minimal.
Non-Finansial Umum hasil healthScore identik Build 003.
Altman Z threshold berubah → skor Altman untuk IDX lebih akurat.
---
## Testing
Manual Testing
Lintas sektor IDX.
Compile Test
Pending
Regression Test
Pending
---
## Engineering Notes
- Sumber: Altman Z (1968+1993), Piotroski F-Score (2000), Moody's/S&P, AQR (2019).
- Threshold dilarikan dari credit rating agencies + OJK reg + IDX norms.
---
# Build 006
Status
Current Development
Sprint
Sprint 005
Date
YYYY-MM-DD
---
## Objective
Menerapkan Indonesia Layer sebagai 7th factor (opt-in via toggle) — Likuiditas IDX + Stabilitas Pasar + Dukungan Makro.
---
## Files Modified
```
PapanInstrumen.pine
CURRENT_SPRINT.md
CHANGELOG.md
BACKLOG.md
```
---
## Added
- Toggle tampilIndonesia (default OFF — backward compatible)
- bobotIndonesia input kustom (default 1.0 = ~14%, sector-aware 0.8-1.3x)
- f_avg7, f_wavg7, f_countValid7 utility functions
- secIndonesiaBg color + f_sectionBg wiring
- FX_IDC:USDIDR fetch (exchange rate + volatility + trend)
- ta.beta() vs IDX Composite computation
- 3 komponen scoring: indoLiqScore, indoBetaScore, indoMacroScore
- Conditional f_avg6 vs f_avg7 overallScore (based on toggle)
- Rendering: score card + detail section in right column
---
## Changed
- overallScore: supports 7th factor when toggle ON
- overallTxt: dynamic n/6 or n/7 based on toggle
- New build version 2.5.0
---
## Performance Impact
Low.
0 tambahan request.financial(). 1 tambahan request.security("FX_IDC:USDIDR").
ta.beta() menggunakan data existing benchmark (tidak ada request baru).
---
## Breaking Change
NO — toggle default OFF, backward compatible dengan Build 005.
---
## Engineering Notes
- Data sources: FX_IDC:USDIDR (ICE Data Services, confirmed working).
- Commodity proxy: IDX sector indices (IDX:IDXENERGY, IDX:IDXBASIC) fallback.
- Sumber: Altman Z (1968), AQR Quality (2019), IDX market structure.
---
# Build 003
Status
Completed
Sprint
Sprint 002
Date
YYYY-MM-DD
---
## Objective
Menerapkan sector-aware weighting pada dimensi Profitability (Quality Score) menggunakan pola f_wavgArr yang sama seperti Valuation Engine di Build 002.
---
## Files Modified
```
PapanInstrumen.pine
CURRENT_SPRINT.md
CHANGELOG.md
BACKLOG.md
```
---
## Added
- Bobot per-rasio profitability: wRoe, wRoa, wRoic, wGross, wOp, wNet, wEbitda, wFcfM, wPiotroski
- Penyesuaian sektor untuk Finansial, Properti, Infrastruktur, Siklikal, Teknologi, Transportasi
---
## Changed
- QualityScore dari f_avg5 (rata-rata grup setara) menjadi f_wavgArr (bobot per-rasio)
---
## Fixed
- Tidak ada bug fix.
---
## Removed
Tidak ada.
---
## Performance Impact
Low
Tidak ada penambahan request.financial().
---
## Breaking Change
Tidak ada.
Non-Finansial Umum hasil qualityScore IDENTIK dengan Build 002.
---
## Testing
Manual Testing
Lintas sektor IDX.
Compile Test
Pending
Regression Test
Pending
---
## Engineering Notes
- Untuk Teknologi, ROE/ROA tidak diturunkan — banyak emiten tech IDX masih rugi,
  menurunkan bobot akan memberi bias.
- Finansial: margin tradisional di-skip (NIM-based, tidak relevan).
---
# Build 002
Status
Completed
Sprint
Sprint 001
Date
YYYY-MM-DD
---
## Objective
Melanjutkan pembangunan fondasi repository serta penyempurnaan modul Valuation dan klasifikasi sektor.
---
## Files Modified
```
PapanInstrumen.pine
CURRENT_SPRINT.md
BACKLOG.md
```
---
## Added
- Pemisahan sektor finansial menjadi Bank, Asuransi, dan Sekuritas.
- Override manual untuk beberapa sektor.
- Dokumentasi repository.
---
## Changed
- Penyempurnaan klasifikasi sektor.
- Penyempurnaan struktur repository.
- Penyempurnaan metodologi.
---
## Fixed
- Regresi fallback sektor finansial.
- Konsistensi klasifikasi sektor.
---
## Removed
Tidak ada.
---
## Performance Impact
Low
Tidak ada penambahan request.financial().
---
## Breaking Change
Tidak ada.
---
## Testing
Manual Testing
Lintas sektor IDX.
Compile Test
Passed
Regression Test
Passed
---
## Engineering Notes
Build ini merupakan build transisi menuju engine fundamental yang lebih modular.
Belum terdapat perubahan besar pada skor valuasi.
Sebagian perubahan merupakan persiapan untuk Sprint berikutnya.
---
# Build 001
Status
Completed
Sprint
Sprint 001
---
## Objective
Membangun dashboard fundamental pertama.
---
## Files Modified
```
PapanInstrumen.pine
```
---
## Summary
- Dashboard awal.
- Modul valuasi awal.
- Integrasi data fundamental.
- Struktur dasar dashboard.
---
## Performance Impact
Baseline.
---
## Breaking Change
Tidak ada.
---
## Engineering Notes
Build pertama difokuskan pada pembentukan fondasi indikator.
---
# Release Rules
Sebelum Build dinyatakan selesai:
☐ Pine berhasil compile
☐ Manual test selesai
☐ Dokumentasi diperbarui
☐ Commit dibuat
☐ Changelog diperbarui
☐ Product Owner menyetujui
---
# Closing Statement
CHANGELOG merupakan sejarah teknis proyek.
Dokumen ini harus mampu menjelaskan evolusi proyek tanpa perlu membaca seluruh commit Git.
