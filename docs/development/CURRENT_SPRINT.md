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

B003

Sprint

S002

Status

🟡 In Development

Current Phase

Profitability Engine

---

# Active Task

Task ID

PROF-001

Objective

Implement sector-aware weighting for Profitability/Quality dimension.

Scope

- ROE/ROA/ROIC sector weights
- Margin ratios sector weights
- Piotroski F-Score sector weights
- Financial sector margin skip
- Infrastructure/Teknologi/Properti/Siklikal/Transportasi weights

Do Not

- Change Valuation Methodology
- Change Dashboard Layout
- Add New Financial Ratios
- Modify Growth/Health/Income dimensions

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

Growth Engine (B004)
---
# Sprint Information
Sprint Name
Profitability — Sector-Aware Weighting
Sprint Number
Sprint 002
Status
🟢 Active
Priority
High
Current Build
Build 003
---
# Sprint Goal
Menerapkan sector-aware weighting pada dimensi Profitability (Quality Score) menggunakan pola yang sama seperti Valuation Engine di Build 002.
---
# Sprint Scope
## Included
- Quality Score Sector Weights
- Profitability Methodology
- Documentation Update
---
## Excluded
- Valuation Methodology Changes
- Growth/Health/Income Dimensions
- Dashboard Layout Changes
- New Financial Ratios
---
# Current Tasks
| ID | Task | Status | Priority |
|----|------|--------|----------|
| PROF-001 | Define sector weights for profitability ratios | ✅ Done | High |
| PROF-002 | Implement f_wavgArr for Quality score | ✅ Done | High |
| PROF-003 | Financial sector margin skip logic | ✅ Done | High |
| PROF-004 | Update documentation | 🟡 In Progress | Medium |
| PROF-005 | Code review & testing | ⬜ Pending | High |
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
Quality Scoring  ██████████ 100%
Documentation    ████████░░ 80%
Testing          ░░░░░░░░░░ 0%
```
---
# Sprint Notes
Catatan penting selama sprint:
- Profitability weights mengikuti pola f_wavgArr yang sama dengan Valuasi.
- Non-Finansial Umum hasilnya identik dengan Build 002 (no regression).
- Untuk Teknologi, ROE/ROA TIDAK diturunkan (banyak emiten tech IDX masih rugi).
---
# Next Sprint Preview
Sprint berikutnya direncanakan berfokus pada:
- Growth Engine
- Sector-aware weighting untuk Revenue/EPS Growth
Dokumen ini akan diperbarui setelah Sprint 002 selesai.
---

# AI Context

This document serves as the primary operational context for all AI contributors.

Before starting any development task:

1. Read this document.
2. Read the target source file.
3. Complete only the active task.
4. Ignore completed sprint history unless requested.
