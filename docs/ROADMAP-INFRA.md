# ROADMAP-INFRA.md — Perbaikan Workflow OpenCode + Graphify + Obsidian

Proyek: Infrastruktur knowledge-management untuk **Papan Instrumen** & **Papan Gerak**
Sumber: Audit `Workflow.md` vs isi sungguhan `obsidian-vault` (831 file diperiksa)
Status: **Diverifikasi & dikoreksi** — klaim salah F1-2 dan F1-4 sudah diperbaiki

---

## Ringkasan Audit

Setiap klaim di `Workflow.md` dicek langsung terhadap file di vault.

| Kategori | Jumlah Temuan | Dampak |
|---|---|---|
| Pipeline Graphify menghasilkan data berantakan | 2 | Vault 3x lebih besar dari dugaan, mayoritas noise |
| Navigasi utama (`Index.md`) putus total | 2 | 13/17 link mati — vault tidak bisa dipakai sebagai dashboard |
| Konfigurasi sync tidak konsisten | 2 | Auto-sync bisa tidak berjalan sesuai ekspektasi |
| Portabilitas/disaster-recovery bolong | 1 | `.obsidian/` di-gitignore penuh → plugin config hilang |

---

## Fase 0 — Kritis: Risiko Kehilangan Data/Konfigurasi

| ID | Temuan | Verifikasi | Solusi |
|----|--------|-----------|--------|
| F0-1 | `.obsidian/` di-gitignore penuh — konfigurasi `obsidian-git` tidak ikut backup | ✅ **TERKONFIRMASI** — `.gitignore` baris 2: `.obsidian/` | Ubah `.gitignore` selektif: ignore `.obsidian/workspace.json` dan `.obsidian/cache/`, commit `plugins/obsidian-git/data.json` dan `manifest.json` |
| F0-2 | `pullOnBoot: true` vs `autoPullOnBoot: false` bersamaan — konflik | ✅ **TERKONFIRMASI** — `data.json` line 9 vs line 67 | `autoPullOnBoot` adalah key legacy (obsidian-git v2.38.6 sudah rename ke `pullOnBoot`). Hapus `autoPullOnBoot`. |
| F0-3 | `syncMethod: merge` + `mergeStrategy: none` | ⚠️ **TERVERIFIKASI** — Ini kombinasi valid. `mergeStrategy: none` berarti fallback ke default Git (recursive). Tidak perlu diubah, cukup didokumentasikan. |

---

## Fase 1 — Pipeline Graphify Menghasilkan Data Berantakan

| ID | Temuan | Verifikasi | Solusi |
|----|--------|-----------|--------|
| F1-1 | Community detection gagal — mayoritas "komunitas" isinya 1 node | ✅ **TERKONFIRMASI** — PG: 82/108 (76%) singleton. PI: 114/128 (**89%**) singleton. Bahkan `_COMMUNITY_Color Legend & Themes.md` cuma 1 node. | Jangan export community `members:1` sebagai file terpisah. Gabungkan semua singleton dalam 1 file `_UNCLUSTERED_Nodes.md`, atau turunkan resolusi clustering. |
| F1-2 | Filename encoding Unicode rusak, tidak konsisten | ❌ **SALAH** — Dicek terhadap 831 file vault. Tidak ada filename mengandung literal `#U2014` atau `#U201`. 18 file dengan EM DASH (`—`, U+2014) adalah UTF-8 valid. `\u2014` di manifest.json adalah JSON escaping standar, bukan kegagalan decode. | **HAPUS dari roadmap** — tidak ada bug encoding. |
| F1-3 | Node ID tabrakan dari variabel lokal tak ber-namespace | ⚠️ **PARsial** — Tabrakan terjadi di **layer export Obsidian** (label→filename), bukan di graph.json (yang pakai path-qualified ID). 8 file `t_1..7.md` + 2 file `weightedAvg()_1..2.md` akib at 8 node label `t` dan 3 node label `weightedAvg()`. | Prefix ID export dengan path file sumber SEBELUM proses dedup (konvensi yg sudah tertulis di §8.3 Workflow.md untuk Pine — terapkan aturan yang sama ke `.mjs`). |
| F1-4 | Test suite duplikasi utility function | ❌ **SALAH** — Semua 9 test file import dari `runner.mjs` sentral. 1 fungsi inline `f_wavg6` di `test-overall.mjs` untuk 1 assertion spesifik — bukan duplikasi. Arsitektur test sudah baik. | **HAPUS dari roadmap** — test suite sudah clean. |

---

## Fase 2 — Navigasi Utama (`Index.md`) Putus Total

| ID | Temuan | Verifikasi | Solusi |
|----|--------|-----------|--------|
| F2-1 | Semua link ke catatan proyek di `Index.md` putus | ✅ **TERKONFIRMASI** — 13/17 link mati. File di vault pakai nama berbeda (contoh: `Changelog (Build 001-010).md` tapi link menunjuk `Changelog`). | Regenerate Index.md dengan nama file yang benar, atau pakai Dataview query dinamis. |
| F2-2 | Link ke `docs-repo/` (symlink) dan `*-graph.html` tidak akan pernah ada | ✅ **TERKONFIRMASI** — `docs-repo/` tidak ada di mana pun; `*.html` masuk `.gitignore`. | Hapus link ini dari Index.md. Ganti dengan link ke `.canvas` yang benar-benar ada. |
| F2-3 | Lokasi file `.canvas` tidak sesuai dokumentasi | ✅ **TERKONFIRMASI** — Workflow.md: `papan-instrumen/graph.canvas`. Sungguhan: `papan-instrumen.canvas` di root vault. | Perbaiki Workflow.md (nama file + path). |
| F2-4 | Duplikasi note untuk entitas yang sama | ✅ **TERKONFIRMASI** — 3 file `_COMMUNITY_Saham Papan Gerak By. Akhmfz.md` + `_1` + `_2` untuk 1 entitas. | Fix otomatis setelah F1-1 diperbaiki (singleton umum), tapi duplikasi spesifik ini tetap perlu dibersihkan manual. |

---

## Fase 3 — Verifikasi & Regression Check

| ID | Item |
|----|------|
| F3-1 | Tambahkan skrip `graphify doctor` yang ngecek: (a) rasio community `members:1` di bawah 20%, (b) semua link Index.md resolve ke file yang ada, (c) tidak ada filename mengandung literal encoding gagal |
| F3-2 | Tambahkan langkah ke-6 di Workflow.md §6.1: "Jalankan `graphify doctor`, kalau merah jangan lanjut commit" |
| F3-3 | Verifikasi angka node/edge di commit message terhadap `graph.json` sungguhan — pola di proyek ini menunjukkan angka yang dilaporkan tidak diverifikasi ulang setelah pipeline berubah |

---

## Urutan Pengerjaan

```
Fase 0 (risiko kehilangan config)
   → Fase 2 (Index.md + Workflow.md fix — effort rendah, dampak besar)
   → Fase 1 (perbaiki pipeline Graphify di sumbernya — effort sedang)
   → Fase 3 (regression check permanen)
```

Fase 2 didahulukan karena:
- F0 (gitignore + data.json) sudah selesai
- F2 (Index.md, Workflow.md) bisa langsung diperbaiki tanpa perlu Graphify
- F1 butuh modifikasi pipeline Graphify yang lebih dalam

---

## Lampiran

Semua temuan diverifikasi terhadap isi vault sungguhan per 2026-07-08 (831 `.md` files, 2 `.canvas` files). Simpan di `trading-journal/decisions/` vault sebagai catatan keputusan.
