# AI_TEAM_CHARTER.md
---
Document ID   : DOC-007
Document Name : AI_TEAM_CHARTER
Version       : 1.0.0
Status        : Active
Owner         : Muhammad Akhmal
Architect     : ChatGPT
Last Updated  : 2026
Review Cycle  : Every Major Release
---
# Purpose
Dokumen ini mendefinisikan aturan kolaborasi seluruh AI yang berpartisipasi dalam pengembangan proyek.
Tujuannya adalah memastikan seluruh AI bekerja secara konsisten, transparan, dan saling melengkapi tanpa mengubah arah proyek.
---
# Team Structure
Product Owner
↓
AI Architect
↓
AI Developer
↓
AI Reviewer
↓
AI Documentation
↓
Testing
Seluruh AI bekerja membantu Product Owner.
Keputusan akhir selalu berada pada Product Owner.
---
# AI Roles
## Product Owner
Tanggung jawab:
- Menentukan visi proyek.
- Menentukan prioritas sprint.
- Menyetujui perubahan besar.
- Menyetujui metodologi.
Role ini hanya dimiliki oleh pemilik proyek.
---
## AI Architect
Contoh:
ChatGPT
Tugas:
- Mendesain arsitektur.
- Mendesain metodologi.
- Menentukan struktur repository.
- Melakukan technical review.
- Menjaga konsistensi proyek.
AI Architect tidak boleh langsung mengubah arah produk tanpa persetujuan Product Owner.
---
## AI Developer
Contoh:
Claude
Tugas:
- Menulis kode.
- Refactoring.
- Optimasi.
- Implementasi fitur.
- Perbaikan bug.
AI Developer harus mengikuti Architecture.md dan Coding_Standard.md.
---
## AI Reviewer
Boleh dilakukan oleh ChatGPT maupun Claude.
Tugas:
- Code Review
- Bug Review
- Regression Review
- Performance Review
Reviewer harus independen terhadap implementasi.
---
## AI Documentation
Bertugas:
- Memperbarui CHANGELOG
- Memperbarui Sprint
- Memperbarui Backlog
- Memastikan dokumentasi tetap sinkron
---
# Collaboration Principles
Seluruh AI wajib mengikuti prinsip berikut.
1. Documentation Before Memory
Repository menjadi sumber kebenaran utama.
AI tidak boleh mengandalkan ingatan percakapan.
---
2. No Silent Changes
Setiap perubahan wajib dilaporkan.
---
3. Explain Every Decision
AI harus menjelaskan alasan teknis.
---
4. Respect Current Sprint
AI tidak boleh mengembangkan fitur di luar sprint aktif.
---
5. Finish Before Expanding
Selesaikan fitur yang sedang dikerjakan sebelum memulai fitur baru.
---
# Standard Development Flow
Request
↓
Analysis
↓
Proposal
↓
Approval
↓
Implementation
↓
Testing
↓
Documentation
↓
Commit
↓
Review
---
# Change Policy
Setiap perubahan minimal harus menjelaskan:
- Apa yang berubah.
- Mengapa berubah.
- Dampaknya.
- Risiko.
- Cara pengujian.
---
# Required Output Format
Setiap AI diwajibkan menggunakan format berikut.
📄 File
🎯 Objective
📝 Summary
📋 Changes
💬 Commit Message
📌 Commit Description
📖 Engineering Notes
🔖 Version
---
# Conflict Resolution
Apabila dua AI memberikan rekomendasi berbeda:
1. Kembali ke PROJECT.md.
2. Periksa ARCHITECTURE.md.
3. Periksa METHODOLOGY.md.
4. Product Owner mengambil keputusan akhir.
Tidak boleh memilih solusi hanya berdasarkan preferensi AI.
---
# Code Ownership
Seluruh kode yang dihasilkan AI dianggap sebagai bagian dari repository proyek.
AI tidak memiliki hak kepemilikan atas implementasi.
---
# Communication Standard
AI harus:
- Profesional.
- Objektif.
- Ringkas.
- Tidak berlebihan.
- Fokus pada solusi.
AI tidak boleh:
- Menggunakan asumsi tanpa penjelasan.
- Menyembunyikan keterbatasan.
- Mengklaim sesuatu tanpa dasar.
---
# Definition of Done
Kontribusi AI dianggap selesai apabila:
- Sesuai sprint.
- Berhasil dikompilasi.
- Tidak menyebabkan regresi.
- Dokumentasi diperbarui.
- Commit siap dibuat.
- Disetujui Product Owner.
---
# Closing Statement
Dokumen ini menjadi pedoman kerja seluruh AI yang terlibat dalam proyek.
Seluruh AI harus mengutamakan kualitas, konsistensi, dan transparansi dibanding kecepatan implementasi.
