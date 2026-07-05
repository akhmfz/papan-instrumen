# CURRENT_SPRINT.md
---
Document ID   : DOC-009
Document Name : CURRENT_SPRINT
Version       : 1.1.0
Status        : Active
Owner         : Muhammad Akhmal
Architect     : ChatGPT
Last Updated  : 2026
Review Cycle  : Every Sprint
---
# Current Project State

---

Release

v0.1.0-alpha

Build

B006

Sprint

S005

Status

🟡 In Development

Current Phase

Indonesia Layer

---

# Active Task

Task ID

IDN-001

Objective

Implement Indonesia Layer sebagai 7th factor dalam overall scoring (opt-in via toggle).

Scope

- Toggle tampilIndonesia (default OFF)
- 3 komponen: Likuiditas IDX, Stabilitas Pasar (beta), Dukungan Makro (IDR)
- bobotIndonesia input kustom
- Sector-aware weight adjustment
- Data baru: FX_IDC:USDIDR, ta.beta() vs IDX Composite
- Rendering FAKTOR INDONESIA di kedua kolom

Do Not

- Change existing 6-factor scoring when toggle is OFF
- Add new request.financial() calls
- Modify existing dashboard layout or color themes

---

# Target Files

Primary

src/PapanInstrumen.pine

Supporting

docs/development/CURRENT_SPRINT.md

---

# Build Progress

Architecture

✅ Completed

Implementation

✅ Completed

Testing

🟡 In Progress

Documentation

🟡 In Progress

Review

⬜ Pending

Merge

⬜ Pending

---

# Known Issues

- Securities auto detection requires further validation.
- TradingView industry classification may be inconsistent.
- Consumer/Industri/Healthcare belum dipisah sebagai kelas sektor.

---

# Next Milestone

Alpha Release (v0.1.0-alpha — Candidate Review)
---
# Sprint Information
Sprint Name
Indonesia Layer — 7th Factor
Sprint Number
Sprint 005
Status
🟢 Active
Priority
High
Current Build
Build 006
---
# Sprint Goal
Menerapkan Indonesia Layer sebagai 7th factor (opt-in) — Likuiditas IDX + Stabilitas Pasar + Dukungan Makro.
---
# Sprint Scope
## Included
- Toggle tampilIndonesia (default OFF — backward compatible)
- 3 komponen Faktor Indonesia
- FX_IDC:USDIDR + ta.beta() data sources
- Sector-aware weight adjustment (0.8-1.3x)
- bobotIndonesia input kustom
- Rendering FAKTOR INDONESIA
---
## Excluded
- Existing 6-factor scoring unchanged when toggle OFF
- request.financial() additions
- Dashboard layout changes
- New color themes
---
# Current Tasks
| ID | Task | Status | Priority |
|----|------|--------|----------|
| IDN-001 | Add toggle + bobotIndonesia input | ✅ Done | High |
| IDN-002 | Add FX_IDC:USDIDR + beta fetch | ✅ Done | High |
| IDN-003 | Implement Indonesia scoring (3 komponen) | ✅ Done | High |
| IDN-004 | Conditional f_avg6 vs f_avg7 overallScore | ✅ Done | High |
| IDN-005 | Add FAKTOR INDONESIA rendering | ✅ Done | High |
| IDN-006 | Update documentation | 🟡 In Progress | Medium |
---
# Definition of Done
Sprint dianggap selesai apabila:
- Seluruh dokumentasi inti selesai.
- Repository memiliki struktur final.
- Pine Script berhasil dikompilasi.
- Tidak ada error kritis.
- CHANGELOG diperbarui.
- Seluruh perubahan telah di-commit.
---
# Sprint Risks
Risiko yang saat ini diketahui:
- Pine Script memiliki keterbatasan resource.
- Data fundamental TradingView tidak selalu lengkap.
- Perbedaan karakteristik sektor IDX memerlukan metodologi khusus.
- Scope creep akibat penambahan ide baru.
---
# Sprint Rules
Selama sprint berlangsung:
- Tidak menambahkan fitur di luar scope.
- Tidak mengubah metodologi tanpa persetujuan.
- Tidak melakukan refactor besar tanpa alasan.
- Seluruh perubahan wajib didokumentasikan.
---
# Deliverables
Target akhir Sprint:
- Repository siap digunakan.
- Dokumentasi selesai.
- Dashboard Build pertama siap diuji.
- Standar pengembangan telah ditetapkan.
---
# Progress
Overall Progress
```
Indonesia Layer  ██████████ 100%
Documentation    ████████░░ 80%
Testing          ░░░░░░░░░░ 0%
```
---
# Sprint Notes
Catatan penting selama sprint:
- Toggle default OFF: backward compatible dengan Build 005.
- Data baru: FX_IDC:USDIDR (ICE Data Services) + ta.beta() vs IDX Composite.
- 3 komponen: Likuiditas (val+turn+mcap), Stabilitas (beta+RS+vol), Makro (IDR vol+trend).
- Sector-aware weight: Siklikal 1.3x, Teknologi 1.2x, Bank/Asuransi/Infra 0.8x.
- IDX sector indices sebagai fallback commodity proxy.
- Skor Likuiditas positif (beda dari modul Risiko yang ukur bahaya).
---
# Next Sprint Preview
Sprint berikutnya direncanakan berfokus pada:
- Alpha Release Candidate
- Code review, testing, bug fixes
- Finalisasi dokumentasi pengguna
Dokumen ini akan diperbarui setelah Sprint 005 selesai.
---

# AI Context

This document serves as the primary operational context for all AI contributors.

Before starting any development task:

1. Read this document.
2. Read the target source file.
3. Complete only the active task.
4. Ignore completed sprint history unless requested.
