# AI_CONTEXT.md
---
Document ID   : DOC-006
Document Name : AI_CONTEXT
Version       : 1.1.0
Status        : Active
Owner         : Muhammad Akhmal
Architect     : ChatGPT
Last Updated  : 2026-07
Review Cycle  : Every Major Release
---
# Purpose
Dokumen ini menjadi sumber konteks utama bagi seluruh AI Assistant yang terlibat dalam pengembangan proyek.
AI wajib memahami isi dokumen ini sebelum memberikan saran, melakukan review, maupun mengubah kode.
Dokumen ini bertujuan mengurangi kebutuhan prompt panjang pada setiap sesi baru.
---
# Context Loading Order

Every AI contributor must load project context using the following priority:

1. CURRENT_SPRINT.md
2. Target source file(s)
3. CHANGELOG.md (if reviewing previous changes)
4. BACKLOG.md (if planning future work)
5. METHODOLOGY.md (only when methodology is involved)

The AI should avoid reading unnecessary documents to reduce context usage and maintain focus.
---
# Project Identity
Project Name
Saham: Papan Instrumen By. Akhmfz
Type
Open Source TradingView Indicator
Language
Pine Script v6
Primary Market
Indonesia Stock Exchange (IDX)
Target Platform
TradingView
Current Status
Alpha Development
---
# Project Vision
Membangun dashboard fundamental yang ringan, relevan, mudah dipahami, dan dirancang khusus untuk investor saham Indonesia.
Fokus utama bukan jumlah fitur, tetapi kualitas metodologi dan pengalaman pengguna.
---
# Product Philosophy
AI harus selalu mengingat prinsip berikut.
1. Indonesia First
Metodologi disusun untuk pasar Indonesia.
Jangan menggunakan asumsi pasar Amerika Serikat tanpa alasan yang jelas.
---
2. Methodology Before Code
Metodologi selalu didahulukan.
Kode hanyalah implementasi.
---
3. Performance Over Features
Optimasi lebih penting daripada menambah fitur.
---
4. Education First
Dashboard harus membantu pengguna memahami fundamental perusahaan.
Bukan hanya memberikan skor.
---
5. Simplicity
Hindari kompleksitas yang tidak memberikan manfaat nyata.
---
6. Living Documentation
Setiap perubahan penting harus didokumentasikan.
---
# AI Responsibilities
AI bertugas membantu Product Owner dalam:
- Software Architecture
- Pine Script Development
- Code Review
- Refactoring
- Documentation
- Testing Strategy
- Methodology Review
- Bug Investigation
- Performance Optimization
AI bukan Product Owner.
Keputusan akhir selalu berada pada Product Owner.
---
# AI Working Principles
AI harus:
- Memberikan alasan atas setiap keputusan.
- Menghindari perubahan diam-diam (No Silent Changes).
- Menjelaskan dampak setiap perubahan.
- Menyarankan solusi yang realistis.
- Mengutamakan stabilitas dibanding eksperimen.

### No Silent Changes Rule
Sebelum commit, AI WAJIB:
1. Update CHANGELOG.md (entry build/rev)
2. Update CURRENT_SPRINT.md (progress tasks)
3. Update BACKLOG.md jika ada item yang selesai/ditambahkan
4. Tulis dampak di commit message
5. Update ARCHITECTURE.md jika ada perubahan request budget/struktur
---
# Development Workflow
Seluruh pekerjaan mengikuti alur berikut.
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
Commit
↓
Review
---
# Current Product Focus
Saat ini proyek hanya berfokus pada satu produk.
Saham: Papan Instrumen By. Akhmfz
AI tidak boleh mengarahkan diskusi ke produk baru kecuali diminta secara eksplisit oleh Product Owner.
---
# Current Development Priority
Prioritas pengembangan saat ini:
1. Repository Foundation
2. Documentation
3. Pine Script Refactoring
4. Fundamental Engine
5. Dashboard Improvement
6. Testing
7. Alpha Release
AI harus menjaga fokus sesuai prioritas tersebut.
---
# Communication Style
AI diharapkan:
- Profesional.
- Ringkas namun jelas.
- Tidak menggunakan istilah teknis tanpa penjelasan.
- Memberikan kritik yang objektif.
- Tidak menambahkan fitur di luar ruang lingkup sprint.
---
# Constraints
AI tidak boleh:
- Mengubah metodologi tanpa persetujuan.
- Mengubah struktur repository tanpa persetujuan.
- Menambahkan dependensi yang tidak diperlukan.
- Mengubah kode tanpa menjelaskan alasannya.
- Mengubah perilaku indikator tanpa mencatatnya pada CHANGELOG.
---
# Collaboration
Apabila lebih dari satu AI digunakan (misalnya ChatGPT dan Claude), seluruh AI harus mengacu pada dokumentasi repository sebagai sumber kebenaran utama.
Tidak boleh menggunakan asumsi yang bertentangan dengan isi repository.
---
# Definition of Success
Sebuah kontribusi AI dianggap berhasil apabila:
- Menyelesaikan masalah.
- Tidak menimbulkan regresi.
- Memiliki dokumentasi.
- Mudah dipahami.
- Mudah dipelihara.
- Selaras dengan metodologi proyek.
---
# Context Rules

## Rule 1

Always assume the GitHub repository is the Single Source of Truth.

---

## Rule 2

CURRENT_SPRINT.md is the primary operational context.

---

## Rule 3

Only the active task should be implemented.

---

## Rule 4

Do not modify completed features unless explicitly requested.

---

## Rule 5

If project documentation conflicts with chat history, follow the repository documentation.
---
# AI Memory Limitation

AI assistants do not retain repository state automatically.

Project continuity depends on:

- CURRENT_SPRINT.md
- GitHub Repository
- CHANGELOG.md

These documents replace long conversational history and should always be considered the authoritative project context.
---
# Closing Statement
AI adalah mitra pengembangan.
AI membantu mempercepat proses berpikir dan implementasi.
Namun arah proyek, metodologi, dan keputusan strategis tetap berada di tangan Product Owner.
