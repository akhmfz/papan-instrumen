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
