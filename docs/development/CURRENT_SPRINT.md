# CURRENT_SPRINT.md
---
Document ID   : DOC-009
Document Name : CURRENT_SPRINT
Version       : 1.1.0
Status        : Active
Owner         : Muhammad Akhmal
Architect     : ChatGPT
Last Updated  : 2026-07
Review Cycle  : Every Sprint
---
# Current Project State

---

Release

v0.1.0-alpha

Build

B007

Sprint

S006

Status

🟡 In Development

Current Phase

Alpha Fix & Polish

---

# Active Task

Task ID

ALPHA-001

Objective

Alpha Fix & Polish — hide irrelevant rows, fix scoring thresholds, testing.

Scope

- Hide render rows where weight = 0 (Quality margin + Health leverage/liquidity)
- Fix Interest Cover threshold (5-30)
- Hide non-relevant rows for all sectors (check weight)

Do Not

- Change scoring methodology or weights
- Add new request.financial() calls
- Add new features or dimensions

---

# Target Files

Primary

src/PapanInstrumen.pine

Supporting

docs/development/CURRENT_SPRINT.md
docs/development/CHANGELOG.md
docs/development/BACKLOG.md

---

# Build Progress

Architecture

✅ Completed

Implementation

🟡 In Progress

Testing

⬜ Pending

Documentation

⬜ Pending

Review

⬜ Pending

Merge

⬜ Pending

---

# Known Issues

- Securities auto detection requires further validation.
- TradingView industry classification may be inconsistent.
- Consumer/Industri/Healthcare belum dipisah sebagai kelas sektor.
- Banyak field TradingView tidak terisi untuk emiten IDX tertentu.

---

# Next Milestone

Beta Release
---
# Sprint Information
Sprint Name
Alpha Fix & Polish
Sprint Number
Sprint 006
Status
🟢 Active
Priority
High
Current Build
Build 007
---
# Sprint Goal
Menyelesaikan issue-issue alpha: hide rows tidak relevan, fix threshold scoring, testing dasar.
---
# Sprint Scope
## Included
- Hide render rows by weight (Quality + Health)
- Interest Cover threshold adjustment
- Testing BBCA + ADRO + TLKM
---
## Excluded
- New features or dimensions
- request.financial() additions
- Dashboard layout changes
- Perubahan metodologi scoring
---
# Current Tasks
| ID | Task | Status | Priority |
|----|------|--------|----------|
| ALPHA-001 | Hide rows by weight in Quality render | ✅ Done | High |
| ALPHA-002 | Hide rows by weight in Health render | ✅ Done | High |
| ALPHA-003 | Fix Interest Cover threshold (5-30) | ✅ Done | High |
| ALPHA-004 | Testing (BBCA, ADRO, TLKM) | ⬜ Pending | High |
| ALPHA-005 | Update documentation | 🟡 In Progress | Medium |
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
Hide Rows       ██████████ 100%
Threshold Fix   ██████████ 100%
Testing         ░░░░░░░░░░ 0%
Documentation   ░░░░░░░░░░ 0%
```
---
# Sprint Notes
Catatan penting selama sprint:
- Render rows di-hide berdasarkan weight scoring (bukan hardcode per sektor).
- Quality margin rows hanya muncul jika `wGross/wOp/wNet/wEbitda/wFcfM > 0`.
- Health leverage/liquidity rows hanya muncul jika `wHDe/wHCR/wHAltman > 0`.
- Interest Cover threshold dinaikkan dari 2-20 ke 5-30.
- `f_scorePositive` tetap binary — fungsi cek positif/negatif memang seharusnya binary.
---
# Next Sprint Preview
Sprint berikutnya direncanakan berfokus pada:
- Beta Release
- User documentation final
- Feedback collection
Dokumen ini akan diperbarui setelah Sprint 006 selesai.
---

# AI Context

This document serves as the primary operational context for all AI contributors.

Before starting any development task:

1. Read this document.
2. Read the target source file.
3. Complete only the active task.
4. Ignore completed sprint history unless requested.
