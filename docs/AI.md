# AI.md — AI Collaboration Context

Proyek: **Saham: Papan Instrumen By. Akhmfz**
Platform: TradingView Pine Script v6 | Market: IDX | Status: Alpha

---

## Project Identity

| Atribut | Nilai |
|---------|-------|
| Nama | Saham: Papan Instrumen By. Akhmfz |
| Tipe | Open Source TradingView Indicator |
| Bahasa | Pine Script v6 |
| Market | Indonesia Stock Exchange (IDX) |
| Target | TradingView |
| Status | Beta Development (v0.3.0-beta) |

## Product Philosophy

1. **Indonesia First** — Metodologi untuk pasar Indonesia, bukan adaptasi dari AS.
2. **Methodology Before Code** — Metodologi didahulukan, kode adalah implementasi.
3. **Performance Over Features** — Optimasi > fitur baru.
4. **Education First** — Dashboard harus edukatif, bukan hanya memberi skor.
5. **Simplicity** — Hindari kompleksitas tanpa manfaat nyata.
6. **Living Documentation** — Setiap perubahan penting harus didokumentasikan.

## AI Roles

| Role | Contoh AI | Tanggung Jawab |
|------|-----------|----------------|
| **Product Owner** | Muhammad Akhmal | Visi, prioritas, approve perubahan besar, keputusan akhir |
| **AI Architect** | ChatGPT | Arsitektur, metodologi, sprint planning, technical review |
| **AI Developer** | Claude | Implementasi kode, refactoring, bug fixing, optimasi |
| **AI Reviewer** | ChatGPT/Claude | Code review, regression review, performance review |
| **AI Documentation** | — | Update CHANGELOG, sprint, backlog, jaga sinkronisasi dokumen |

## Context Loading Order (wajib dilakukan setiap AI sebelum bekerja)

1. `docs/DEVELOPMENT.md` — cari `# Current Sprint`
2. File source target
3. `docs/DEVELOPMENT.md` — cari `# Changelog` (jika review perubahan sebelumnya)
4. `docs/DEVELOPMENT.md` — cari `# Backlog` (jika merencanakan pekerjaan baru)
5. `docs/ARCHITECTURE.md` (hanya jika metodologi terlibat)

## Golden Rules

1. GitHub Repository adalah **Single Source of Truth**.
2. **No Silent Changes** — semua perubahan wajib tercatat.
3. **Satu Sprint, Satu Goal** — fokus.
4. Semua ide harus masuk **Backlog** dulu.
5. Dokumentasi mengikuti implementasi.
6. Setiap build selesai → update CHANGELOG.
7. Product Owner pemegang keputusan akhir.

## Delivery Requirements

Setiap kontribusi AI wajib menyertakan:
- **📄 File** — file yang diubah
- **🎯 Objective** — tujuan perubahan
- **📝 Summary** — ringkasan
- **📋 Changes** — daftar perubahan detail
- **💬 Commit Message** — pesan commit
- **📖 Engineering Notes** — catatan teknis

## Standard Development Flow

```
Request → Analysis → Proposal → Approval → Implementation → Testing → Documentation → Commit → Review
```

## Constraints

AI **tidak boleh**:
- Mengubah metodologi tanpa persetujuan PO
- Mengubah struktur repository tanpa persetujuan
- Menambahkan dependensi tidak perlu
- Silent changes
- Mengubah perilaku indikator tanpa catatan di CHANGELOG
