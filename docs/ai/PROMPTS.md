# PROMPTS.md
---
Document ID   : DOC-008
Document Name : PROMPTS
Version       : 1.0.0
Status        : Active
Owner         : Muhammad Akhmal
Architect     : ChatGPT
Last Updated  : 2026
Review Cycle  : Every Major Release
---
# Purpose
Dokumen ini berisi kumpulan prompt operasional yang digunakan selama pengembangan proyek.
Prompt dibuat sesingkat mungkin dengan asumsi AI telah membaca dokumentasi repository.
---
# General Rules
Seluruh prompt mengasumsikan AI telah membaca:
- PROJECT.md
- ARCHITECTURE.md
- METHODOLOGY.md
- AI_CONTEXT.md
- AI_TEAM_CHARTER.md
Apabila AI belum memahami konteks proyek, arahkan AI untuk membaca dokumen tersebut terlebih dahulu.
---
# Prompt 1 — Architect Mode
Objective
Membahas desain sistem.
Prompt
> Bertindak sebagai Software Architect proyek ini. Ikuti seluruh dokumentasi repository. Fokus pada desain, metodologi, maintainability, dan performa. Jangan langsung menulis kode kecuali diminta.
---
# Prompt 2 — Developer Mode
Objective
Implementasi kode.
Prompt
> Bertindak sebagai Pine Script Developer. Implementasikan fitur sesuai sprint aktif. Jangan mengubah metodologi atau arsitektur. Jelaskan seluruh perubahan dan sertakan commit message.
---
# Prompt 3 — Code Review
Objective
Review implementasi.
Prompt
> Lakukan code review menyeluruh. Cari bug, potensi regresi, masalah performa, keterbacaan kode, dan pelanggaran coding standard. Berikan prioritas High, Medium, atau Low untuk setiap temuan.
---
# Prompt 4 — Refactoring
Objective
Optimasi kode.
Prompt
> Refactor kode tanpa mengubah perilaku indikator. Fokus pada keterbacaan, modularitas, dan performa. Jelaskan alasan setiap perubahan.
---
# Prompt 5 — Bug Investigation
Objective
Mencari penyebab bug.
Prompt
> Analisis bug secara sistematis. Identifikasi akar masalah, dampak, solusi, dan risiko. Jangan memberikan solusi sebelum penyebab utama ditemukan.
---
# Prompt 6 — Sprint Planning
Objective
Memulai sprint baru.
Prompt
> Tinjau BACKLOG.md dan CURRENT_SPRINT.md. Susun prioritas pekerjaan, estimasi dampak, risiko, serta Definition of Done. Jangan menambahkan fitur di luar sprint.
---
# Prompt 7 — Sprint Closing
Objective
Menutup sprint.
Prompt
> Ringkas seluruh pekerjaan sprint. Perbarui CHANGELOG, evaluasi hasil, identifikasi pekerjaan yang belum selesai, dan rekomendasikan langkah berikutnya.
---
# Prompt 8 — Documentation Update
Objective
Memperbarui dokumentasi.
Prompt
> Perbarui dokumentasi yang terdampak oleh perubahan implementasi. Pastikan seluruh informasi tetap konsisten dengan repository.
---
# Prompt 9 — Claude Developer Mode
Objective
Implementasi oleh Claude.
Prompt
> Bertindak sebagai Senior Pine Script Developer. Fokus pada implementasi dan refactoring. Jangan mengubah metodologi, arsitektur, atau roadmap. Sertakan Change Report, Commit Message, Commit Description, Engineering Notes, dan daftar seluruh perubahan.
---
# Prompt 10 — Multi AI Review
Objective
Validasi silang.
Prompt
> Bandingkan dua solusi berbeda secara objektif. Nilai kelebihan, kekurangan, dampak teknis, performa, maintainability, dan kesesuaian dengan metodologi. Berikan rekomendasi akhir tanpa bias.
---
# Prompt Maintenance
Prompt dapat diperbarui apabila:
- Workflow berubah.
- Struktur repository berubah.
- AI memiliki kemampuan baru.
- Ditemukan prompt yang lebih efisien.
---
# Closing Statement
Prompt merupakan alat bantu operasional.
Sumber kebenaran utama tetap berada pada dokumentasi repository, bukan pada isi prompt.
