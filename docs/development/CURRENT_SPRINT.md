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

B005

Sprint

S004

Status

🟡 In Development

Current Phase

Financial Health Engine

---

# Active Task

Task ID

HLT-001

Objective

Implement sector-aware financial health engine with sub-category handling for Bank/Asuransi/Sekuritas.

Scope

- Sector-aware thresholds for D/E, D/EBITDA, CR, QR, IC, Altman Z
- Weight matrix per sektor (Leverage, DebtService, Liquidity, AltmanZ, CashFlow)
- Sub-kategori Bank vs Asuransi vs Sekuritas
- Altman Z threshold Z"-Score EM (1.1-2.6)

Do Not

- Change Valuation/Profitability/Growth Methodology
- Change Dashboard Layout
- Add New Financial Ratios
- Modify Income/Momentum dimensions

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

Indonesia Layer (B006)
---
# Sprint Information
Sprint Name
Financial Health — Sector Thresholds
Sprint Number
Sprint 004
Status
🟢 Active
Priority
High
Current Build
Build 005
---
# Sprint Goal
Menerapkan sector-aware thresholds + weight matrix untuk Financial Health Engine dengan sub-kategori Bank/Asuransi/Sekuritas.
---
# Sprint Scope
## Included
- Sector-aware thresholds for 7 health ratios
- Weight matrix per sektor (f_wavgArr)
- Sub-kategori Bank, Asuransi, Sekuritas
- Altman Z threshold → Z"-Score EM (1.1-2.6)
- Rendering per sub-kategori
---
## Excluded
- Valuation/Profitability/Growth Methodology Changes
- Dashboard Layout Changes
- New Financial Ratios
- Income/Momentum dimensions
---
# Current Tasks
| ID | Task | Status | Priority |
|----|------|--------|----------|
| HLT-001 | Define sector-aware thresholds per sektor | ✅ Done | High |
| HLT-002 | Implement weight matrix (f_wavgArr) for health | ✅ Done | High |
| HLT-003 | Sub-kategori Bank/Asuransi/Sekuritas | ✅ Done | High |
| HLT-004 | Update rendering per sub-kategori | ✅ Done | High |
| HLT-005 | Update documentation | 🟡 In Progress | Medium |
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
Health Scoring   ██████████ 100%
Documentation    ████████░░ 80%
Testing          ░░░░░░░░░░ 0%
```
---
# Sprint Notes
Catatan penting selama sprint:
- Bank: hanya Interest Cover + OCF + FCF (CAR/NPL/LDR tidak tersedia).
- Asuransi: sama seperti bank, Interest Cover bobot 1.0.
- Sekuritas: Cash/Debt prioritas (×1.3), D/E & CR partially relevant.
- Infrastruktur: D/E threshold 0-5 (BUMN normal 3-4x), D/EBITDA 0-8.
- Properti: D/E 0-4, CR/QR threshold longgar (1.5 ideal), Cash Flow prioritas.
- Teknologi: Cash/Debt prioritas (×1.5), D/E & leverage diturunkan (×0.3).
- Siklikal: Interest Cover threshold 3-20 (trough safety).
- Altman Z: threshold diubah ke 1.1-2.6 (Z"-Score untuk EM).
---
# Next Sprint Preview
Sprint berikutnya direncanakan berfokus pada:
- Indonesia Layer
- Kategori "Indonesia Factor" pada Scoring Matrix
Dokumen ini akan diperbarui setelah Sprint 004 selesai.
---

# AI Context

This document serves as the primary operational context for all AI contributors.

Before starting any development task:

1. Read this document.
2. Read the target source file.
3. Complete only the active task.
4. Ignore completed sprint history unless requested.
