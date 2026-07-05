# BACKLOG.md
---
Document ID   : DOC-010
Document Name : BACKLOG
Version       : 1.0.0
Status        : Active
Owner         : Muhammad Akhmal
Architect     : ChatGPT
Last Updated  : 2026
Review Cycle  : Every Sprint
---
# Purpose
Dokumen ini menjadi tempat penyimpanan seluruh ide, usulan, perbaikan, dan pengembangan yang belum masuk ke sprint aktif.
Backlog bertujuan menjaga fokus pengembangan dengan memisahkan antara pekerjaan yang harus segera dikerjakan dan ide yang dapat dipertimbangkan di masa depan.
Seluruh ide baru harus masuk ke backlog terlebih dahulu sebelum dipertimbangkan menjadi bagian dari sprint.
---
# Backlog Workflow
Setiap item mengikuti alur berikut.
```
Idea
↓
Backlog
↓
Review
↓
Approved
↓
Sprint
↓
Development
↓
Testing
↓
Release
```
Tidak boleh ada implementasi langsung tanpa melalui backlog.
---
# Priority Matrix
Prioritas menggunakan empat tingkat.
## P1 — Critical
Harus segera dikerjakan.
Biasanya berupa:
- Bug kritis
- Error kompilasi
- Kesalahan metodologi
- Kesalahan perhitungan
---
## P2 — High
Memberikan dampak besar terhadap kualitas produk.
Contoh:
- Optimasi performa
- Penyempurnaan dashboard
- Refactoring besar
---
## P3 — Medium
Peningkatan kualitas.
Contoh:
- UX
- Warna
- Layout
- Tooltip
---
## P4 — Low
Ide jangka panjang.
Tidak menjadi prioritas sprint saat ini.
---
# Active Backlog
| ID | Category | Task | Priority | Status |
|----|----------|------|----------|--------|
| BL-001 | Dashboard | Refactor Dashboard Layout | P2 | Open |
| BL-002 | Valuation | Finalisasi cutoff sektor IDX | P2 | Open |
| BL-003 | Sector | Validasi klasifikasi seluruh sektor IDX | P2 | Open |
| BL-004 | Performance | Optimasi request.financial() | P2 | Open |
| BL-005 | Documentation | Review metodologi setiap build | P3 | Open |
| BL-006 | Profitability | Profitability sector weights (Build 003) | P2 | ✅ Done |
| BL-007 | Sector | Consumer/Industri/Healthcare sebagai kelas sektor terpisah | P2 | Open |
---
# Future Backlog
## Dashboard
- Compact Mode
- Color Theme
- Custom Layout
- Mobile Optimization
---
## Methodology
- Quality Score
- Capital Allocation
- Earnings Quality
- Economic Moat
---
## Sector Intelligence
- Dynamic Sector Weight
- Industry Override
- Sector Benchmark
---
## Performance
- Memory Optimization
- Calculation Cache
- Render Optimization
---
## Documentation
- User Guide
- Installation Guide
- Release Notes
---
# Parking Lot
Ide yang menarik tetapi belum memiliki urgensi.
- Macro Dashboard
- Technical Dashboard
- Smart Screener
- Portfolio Dashboard
- Ownership Dashboard
Seluruh item pada Parking Lot tidak boleh masuk sprint tanpa evaluasi ulang.
---
# Rules
1. Ide baru selalu masuk backlog.
2. Backlog bukan janji implementasi.
3. Prioritas dapat berubah sesuai kebutuhan proyek.
4. Sprint hanya mengambil item dari backlog.
5. Item yang selesai dipindahkan ke CHANGELOG.
---
# Acceptance Criteria
Sebuah item backlog dapat dipindahkan ke sprint apabila:
- Tujuannya jelas.
- Dampaknya dipahami.
- Risiko diketahui.
- Scope terdefinisi.
- Product Owner menyetujui.
---
# Closing Statement
Backlog merupakan alat untuk menjaga fokus proyek.
Semakin banyak ide bukan berarti semakin baik.
Produk yang selesai selalu lebih bernilai daripada daftar ide yang tidak pernah diimplementasikan.
