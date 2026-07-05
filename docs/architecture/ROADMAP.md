# ROADMAP.md
---
Document ID   : DOC-005
Document Name : ROADMAP
Version       : 1.0.0
Status        : Active
Owner         : Muhammad Akhmal
Architect     : ChatGPT
Last Updated  : 2026
Review Cycle  : Every Minor Release
---
# Purpose
Dokumen ini mendefinisikan arah pengembangan proyek **Saham: Papan Instrumen By. Akhmfz**.
Roadmap disusun berdasarkan target build, bukan berdasarkan tanggal.
Setiap build memiliki ruang lingkup (scope), tujuan (objective), dan kriteria penyelesaian (definition of done) yang jelas.
---
# Development Philosophy
Pengembangan mengikuti prinsip berikut:
- Small Increment
- Stable Before Feature
- Documentation First
- No Silent Changes
- Build Before Release
Seluruh fitur baru harus melewati proses:
Idea
↓
Backlog
↓
Sprint
↓
Implementation
↓
Testing
↓
Documentation
↓
Release
---
# Current Status
Repository Version
v0.1.0-alpha

Current Build
Build 006

Current Sprint
Sprint 005 — Indonesia Layer

Project Status
Alpha Release
---
# Development Stages
## Phase 1
Repository Foundation
Status
Completed
Objective
Membangun fondasi repository, dokumentasi, workflow, dan standar pengembangan.
Deliverables
- README
- Architecture Documents
- AI Documentation
- Development Standards
---
## Phase 2
Fundamental Engine
Status
Completed
Objective
Membangun engine fundamental inti.
Modules
- Valuation (Build 002 — sector-aware weighting)
- Profitability (Build 003 — sector-aware weights)
- Growth (Build 004 — hybrid 2-layer + quality modifier)
- Financial Health (Build 005 — sector thresholds + sub-kategori)
- Dividend (Build 001 — standard scoring)
---
## Phase 3
Sector Intelligence
Status
Planned
Objective
Mengembangkan sistem interpretasi berdasarkan karakteristik sektor di Bursa Efek Indonesia.
Modules
- Sector Mapping
- Sector Weight
- Sector Override
- Sector Recommendation
---
## Phase 4
Dashboard Experience
Status
Planned
Objective
Menyempurnakan tampilan dashboard.
Modules
- Layout
- Color
- Compact Mode
- Mobile Friendly
---
## Phase 5
Optimization
Status
Planned
Objective
Optimasi performa Pine Script.
Focus
- Performance
- Memory
- Financial Request
- Rendering
---
## Phase 6
Alpha Release
Status
Completed (v0.1.0-alpha)
Objective
Merilis versi Alpha — 7 dimensi scoring, sector-aware, Indonesia Factor.
Target
- [x] 7 dimensi scoring (Value, Quality, Growth, Health, Income, Momentum, Indonesia)
- [x] Sector-aware methodology (10 klasifikasi)
- [x] Indonesia Factor (7th factor, opt-in)
- [x] 5 color themes
- [ ] User testing & feedback
---
## Phase 7
Beta Release
Status
Planned
Objective
Membuka pengujian publik.
Target
- Bug Report
- Performance Testing
- Documentation Review
---
## Phase 8
Stable Release
Status
Planned
Objective
Merilis versi stabil.
Target
- Documentation Complete
- Stable Performance
- Public Repository
---
# Release Strategy
Versioning mengikuti Semantic Versioning.
Major
Perubahan besar pada metodologi.
Minor
Penambahan fitur.
Patch
Perbaikan bug dan optimasi
---
# Success Criteria
Setiap build dianggap selesai apabila:
- Kode berhasil dikompilasi.
- Tidak ada error Pine Script.
- Dokumentasi diperbarui.
- CHANGELOG diperbarui.
- Telah diuji pada beberapa emiten lintas sektor.
- Mendapat persetujuan Product Owner.
---
# Future Expansion
Setelah versi stabil, proyek dapat dikembangkan menjadi ekosistem indikator Indonesia.
Contoh:
- Quality Dashboard
- Technical Dashboard
- Smart Screener
- Portfolio Dashboard
- Economic Dashboard
Seluruh produk tetap mengikuti filosofi yang sama.
---
# Closing Statement
Roadmap bukan daftar keinginan.
Roadmap adalah komitmen pengembangan.
Seluruh perubahan roadmap harus didokumentasikan dan disetujui sebelum diimplementasikan.
