# WORKFLOW — OpenCode + Graphify + Obsidian

> Dokumentasi lengkap alur kerja pengembangan Pine Script dengan OpenCode AI agent,
> knowledge graph via Graphify, dan catatan persisten via Obsidian vault.
> Berlaku untuk proyek **Papan Instrumen** dan **Papan Gerak**.

---

## Daftar Isi

1. [Arsitektur Sistem](#1-arsitektur-sistem)
2. [OpenCode — AI Agent](#2-opencode--ai-agent)
3. [Graphify — Knowledge Graph](#3-graphify--knowledge-graph)
4. [Obsidian Vault — Catatan Persisten](#4-obsidian-vault--catatan-persisten)
5. [Git & GitHub — Sinkronisasi](#5-git--github--sinkronisasi)
6. [Siklus Kerja Lengkap](#6-siklus-kerja-lengkap)
7. [Pine Script v6 — Konvensi](#7-pine-script-v6--konvensi)
8. [Cara Inject Kode Pine ke Graph (Inject2)](#8-cara-inject-kode-pine-ke-graph-inject2)
9. [Troubleshooting](#9-troubleshooting)
10. [Communication & Reporting Style](#10-communication--reporting-style)
11. [Cheat Sheet](#11-cheat-sheet)

---

## 1. Arsitektur Sistem

```
┌──────────────────────────────────────────────────────────────────────┐
│                        OpenCode (AI Agent)                            │
│  ┌─────────┐  ┌──────────┐  ┌───────────┐  ┌────────────────────┐   │
│  │Plan Mode│  │Build Mode│  │  Explore  │  │  Slash Commands    │   │
│  │(read)   │  │(write)   │  │(subagent) │  │  /undo /graphify   │   │
│  └────┬────┘  └────┬─────┘  └─────┬─────┘  └─────────┬──────────┘   │
│       └────────────┼───────────────┼──────────────────┘              │
│                    ▼               ▼                                  │
│           ┌────────────────┐ ┌──────────┐                            │
│           │ /home/Akhmfz/  │ │open code │                            │
│           │ papan-*        │ │commands  │                            │
│           └───────┬────────┘ └──────────┘                            │
└───────────────────┼──────────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      Graphify (Knowledge Graph)                       │
│                                                                       │
│   graphify-out/                                                       │
│   ├── graph.json         ← Raw data graph (queryable)                │
│   ├── GRAPH_REPORT.md    ← God nodes, communities, surprises         │
│   ├── .graphify_*.json   ← Temp extraction files                     │
│   └── cache/             ← Semantic extraction cache                 │
│                                                                       │
│   2 jalur ekstraksi:                                                  │
│   ┌─────────────────┐  ┌────────────────────────────────┐           │
│   │   AST (gratis)   │  │   Semantic (pakai LLM)         │           │
│   │   Parse file     │  │   Baca docs .md, extract       │           │
│   │   .js/.mjs/.json │  │   konsep & hubungan            │           │
│   │   → nodes fungsi │  │   → nodes topik & edge makna   │           │
│   │   → edge import  │  │   → hyperedge group            │           │
│   └────────┬─────────┘  └──────────────┬─────────────────┘           │
│            └────────────┬──────────────┘                              │
│                         ▼                                             │
│              ┌────────────────────┐                                   │
│              │  Merge + Cluster   │                                   │
│              │  → dedup by node id│                                   │
│              │  → community detec │                                   │
│              │  → god nodes       │                                   │
│              │  → label komunitas │                                   │
│              └────────┬───────────┘                                   │
│                       ▼                                               │
│              ┌────────────────────┐                                   │
│              │  Export            │                                   │
│              │  → Obsidian vault  │                                   │
│              │  → HTML graph      │                                   │
│              │  → GRAPH_REPORT.md │                                   │
│              └────────────────────┘                                   │
└──────────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────────────────────────┐
│                   Obsidian Vault (Catatan)                            │
│                                                                       │
│   C:\Users\Akhmfz\obsidian-vault\                                     │
│   ├── Index.md                    ← Dashboard utama                  │
│   ├── papan-instrumen.canvas      ← Visualisasi graph PI (interaktif)│
│   ├── papan-instrumen/            ← 311 notes dari graph PI          │
│   │   ├── Papan Instrumen ....md  ← 1 note per node                  │
│   │   └── _COMMUNITY_*.md         ← 1 note per community             │
│   ├── papan-gerak.canvas          ← Visualisasi graph PG (interaktif)│
│   ├── papan-gerak/                ← 325 notes dari graph PG          │
│   │   └── ...                     ← Sama struktur                    │
│   ├── trading-journal/            ← Catatan pribadi (backtest,dll)   │
│   └── .obsidian/plugins/obsidian-git/  ← Auto sync config            │
│                                                                       │
│   Obsidian Git Plugin (auto):                                         │
│   ├── pullOnBoot: true           ← Pull dari GitHub tiap buka vault  │
│   ├── autoCommitOnBoot: true     ← Commit tiap buka                  │
│   ├── autoSaveInterval: 10       ← Auto commit tiap 10 menit         │
│   ├── autoBackupAfterFileChange  ← Commit tiap selesai edit          │
│   ├── autoPushInterval: 10       ← Push tiap 10 menit                │
│   └── pullBeforePush: true       ← Pull dulu sebelum push            │
└──────────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      Git & GitHub (Sinkronisasi)                      │
│                                                                       │
│   Remote: git@github.com:akhmfz/obsidian-vault.git  (SSH)            │
│   └── WSL:   ~/.ssh/id_ed25519                     → auto auth       │
│   └── Win:   C:\Users\Akhmfz\.ssh\id_ed25519       → auto auth       │
│                                                                       │
│   Repo: github.com/akhmfz/papan-instrumen  (SSH + gh CLI)            │
│   Repo: github.com/akhmfz/papan-gerak      (SSH + gh CLI)            │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 2. OpenCode — AI Agent

### 2.1 Dua Mode Kerja

| Mode | Ikon | Bisa Apa? | Kapan Dipakai |
|---|---|---|---|
| **Plan** | 📋 | Membaca file, analisa, tanya-jawab, bikin rencana | Mau ubah strategy, entry/exit, atau logika scoring |
| **Build** | 🛠️ | Edit file, nulis kode, refactor, git commit | Perubahan kecil (warna, typo, fix) atau setelah plan disetujui |

Cara pindah: tekan **Tab**.

**When NOT to use Plan mode** — langsung Build:
- Typo/komentar fix sepele
- Rename variabel lokal dengan instruksi jelas
- Tugas research/eksplorasi murni (baca kode, cari bug, tidak perlu nulis)
- Perubahan yang user sudah beri instruksi sangat detail dan spesifik

**Autonomous mode**: untuk tindakan reversibel yang mengikuti dari permintaan awal, agent langsung kerjakan tanpa bertanya "Mau saya lanjutkan?". Berhenti hanya untuk: (1) aksi destruktif (hapus file, force push), (2) perubahan scope yang user harus putuskan, (3) perubahan yang menyentuh uang riil tanpa plan mode dulu.

**Don't end turns with plans**: agent tidak boleh mengakhiri giliran dengan daftar "next steps" atau janji kerja yang belum dilakukan. Kalau paragraf terakhir adalah rencana/analisa/pertanyaan/next steps — kerjakan sekarang juga. Akhiri giliran hanya ketika tugas selesai atau benar-benar terblokir oleh input user.

### 2.2 Custom Agents

Tersimpan di `.opencode/agent/*.md`:

| Agent | Fungsi | Read-only? |
|---|---|---|
| **pine-review** | Review kode Pine Script — cek repaint, off-by-one, overfit | ✅ Ya |
| **market-analyst** | Analisa backtest CSV, rangkum metrik, tulis ke Obsidian | ❌ Bisa nulis |
| **build** (default) | Implementasi kode | ❌ Bisa nulis |
| **plan** (default) | Analisa & rencana | ✅ Ya |

### 2.3 Slash Commands

| Command | Fungsi |
|---|---|
| `/undo` | Batalkan perubahan terakhir (bisa beberapa kali) |
| `/redo` | Kembalikan perubahan yang di-undo |
| `/pine-lint` | Cek konvensi Pine Script v6 di file yang disebut |
| `/graphify` | Jalankan pipeline Graphify penuh |
| `/save-analysis` | Simpan ringkasan analisa ke Obsidian vault |
| `/graphify-update` | Update knowledge graph setelah refactor besar |
| `/init` | Generate/update AGENTS.md (sekali di awal project) |

### 2.4 Cara Kerja Sesuai Risiko

**Aturan wajib:** Setiap perubahan pada `strategy()` (entry, exit, position sizing, stop/target) **harus lewat Plan mode dulu**.

Perubahan pada `indicator()` kosmetik (warna, style plot) boleh langsung Build mode.

**Autonomous execution:** Agent bertindak tanpa bertanya untuk perubahan reversibel. Berhenti otomatis untuk aksi destruktif, perubahan scope, atau perubahan strategi tanpa plan mode.

---

## 3. Graphify — Knowledge Graph

### 3.1 Instalasi & Setup

```bash
# Install Graphify (via uv)
uv tool install graphifyy

# Register untuk OpenCode
graphify install --platform opencode

# Generate graph pertama kali
cd /home/Akhmfz/papan-instrumen
graphify . --no-viz

# Atau dengan visualisasi HTML
graphify . --html
```

### 3.2 Struktur Output

```
graphify-out/
├── graph.json               ← Full graph data (bisa di-query via NetworkX)
├── graph.html               ← Visualisasi interaktif (buka di browser)
├── GRAPH_REPORT.md          ← Laporan: god nodes, komunitas, surprising connections
├── .graphify_ast.json       ← Hasil AST extraction (temp)
├── .graphify_semantic.json  ← Hasil semantic extraction (temp)
├── .graphify_extract.json   ← Gabungan AST + semantic (temp)
├── .graphify_analysis.json  ← Analisa komunitas
├── .graphify_labels.json    ← Label komunitas
├── .graphify_python         ← Path interpreter Python
├── .graphify_detect.json    ← Hasil deteksi file
└── cache/                   ← Cache semantic extraction
```

### 3.3 Perintah Graphify

```bash
# Pipeline penuh (detect → extract → build → cluster → export)
graphify .                              # current dir
graphify /path/to/project               # path spesifik
graphify . --mode deep                  # semantic lebih agresif (INFERRED edges)
graphify . --html                       # dengan visualisasi HTML
graphify . --no-viz                     # tanpa HTML

# Incremental (hanya file baru/berubah)
graphify . --update
graphify . --update --force             # paksa overwrite

# Re-cluster (tanpa re-extract)
graphify . --cluster-only

# Query graph
graphify query "Bagaimana cara scoring Value bekerja?"
graphify query "Apa hubungan antara Quality dan Growth?" --dfs
graphify path "01-base" "04-scoring"    # Shortest path

# Export
graphify export obsidian --dir /path/to/vault
graphify export html
```

### 3.4 Ekstraksi AST vs Semantic

| Aspek | AST | Semantic |
|---|---|---|
| **Input** | File kode (.js, .mjs, .json, .ts, .go, dll) | File docs (.md, .txt), paper (.pdf), images |
| **Metode** | Tree-sitter grammar (deterministic) | LLM (butuh token / Gemini API key) |
| **Biaya** | Gratis | Token LLM |
| **Hasil** | Fungsi, variabel, import, call edges | Konsep, topik, hubungan makna |
| **Cepat?** | Sangat cepat (detik) | Lambat (menit, tergantung jumlah file) |

**Catatan penting:** Pine Script (.pine) **tidak didukung** oleh tree-sitter grammar Graphify. Hanya 36 bahasa yang didukung. Solusi: inject manual (lihat bagian 8).

### 3.5 .graphifyignore

```
# Contoh .graphifyignore
analysis/
*.csv
*.log
node_modules/
.git/
```

### 3.6 Semantic Pass tanpa API Key

Graphify bisa jalan **tanpa API key**. Caranya:

1. **Tidak ada GEMINI_API_KEY** → fallback ke host agent (OpenCode) sebagai LLM
2. Untuk proyek **code-only** (tanpa docs) → skip semantic, AST saja
3. Untuk proyek **dengan docs** → OpenCode dispatch subagents untuk baca docs dan extract konsep

Tips: Set `GEMINI_API_KEY` kalau mau semantic pass lebih cepat (tidak perlu subagents):
```bash
export GEMINI_API_KEY="your-key-here"
pip install 'graphifyy[gemini]'
```

---

## 4. Obsidian Vault — Catatan Persisten

### 4.1 Struktur Vault

```
C:\Users\Akhmfz\obsidian-vault\          (636+ notes)
├── Index.md                              ← Dashboard utama (MOC)
│
├── papan-instrumen.canvas                ← Graph visual PI (bisa dibuka & diedit)
├── papan-instrumen/                      ← 311 notes (auto-generated by Graphify)
│   ├── Papan Instrumen — Fundamental Dashboard.md
│   ├── 7 Dimensi Scoring.md
│   ├── Value Dimension (Valuasi).md
│   ├── ...                               ← 1 note per node di graph
│   └── _COMMUNITY_*.md                   ← 1 note per komunitas
│
├── papan-gerak.canvas                    ← Graph visual PG (bisa dibuka & diedit)
├── papan-gerak/                          ← 325 notes (auto-generated by Graphify)
│   ├── Papan Gerak — Technical Analysis Dashboard.md
│   ├── Trend Score (30%).md
│   └── ...
│
├── trading-journal/                      ← Catatan pribadi (manual)
│   ├── strategies/                       ← 1 note per strategy
│   ├── backtests/                        ← Log tiap backtest
│   ├── market-notes/                     ← Observasi pasar
│   └── decisions/                        ← Kenapa suatu keputusan diambil
│
└── .obsidian/
    └── plugins/obsidian-git/data.json    ← Konfigurasi auto sync
```

### 4.2 Cara Generate Vault dari Graph

```bash
# Hapus folder lama (kalau perlu regenerate)
rm -rf /mnt/c/Users/Akhmfz/obsidian-vault/papan-instrumen

# Generate dari graph terbaru
cd /home/Akhmfz/papan-instrumen
graphify export obsidian --dir /mnt/c/Users/Akhmfz/obsidian-vault/papan-instrumen

# Rapikan (hapus .obsidian dari subfolder)
rm -rf /mnt/c/Users/Akhmfz/obsidian-vault/papan-instrumen/.obsidian
```

### 4.3 Format Catatan Manual

Gunakan format Zettelkasten untuk catatan trading journal:

```markdown
---
date: 2026-07-08
tags: [strategy, backtest]
related: [[Papan Gerak — Entry Trigger Engine]]
---

## Konteks
...

## Keputusan / Temuan
...

## Metrik
Win rate: __ | Profit factor: __ | Max DD: __
```

### 4.4 Obsidian Git Plugin — Konfigurasi

File: `.obsidian/plugins/obsidian-git/data.json`

| Setting | Nilai | Fungsi |
|---|---|---|
| `gitExecutablePath` | `C:\...\Git\cmd\git.exe` | Path Git for Windows |
| `autoSaveInterval` | `10` | Commit otomatis tiap 10 menit |
| `autoPushInterval` | `10` | Push otomatis tiap 10 menit |
| `autoPullInterval` | `10` | Pull otomatis tiap 10 menit |
| `pullOnBoot` | `true` | Pull saat buka vault |
| `autoCommitOnBoot` | `true` | Commit saat buka vault |
| `autoBackupAfterFileChange` | `true` | Commit tiap selesai edit |
| `pullBeforePush` | `true` | Pull dulu sebelum push |
| `commitMessage` | `vault backup: {{date}}` | Format pesan commit |
| `syncMethod` | `merge` | Metode sinkronisasi |

---

## 5. Git & GitHub — Sinkronisasi

### 5.1 Repositori

| Repo | Remote | Auth |
|---|---|---|
| `github.com/akhmfz/obsidian-vault` | `git@github.com:akhmfz/obsidian-vault.git` | SSH key |
| `github.com/akhmfz/papan-instrumen` | `git@github.com:akhmfz/papan-instrumen.git` | `gh` CLI |
| `github.com/akhmfz/papan-gerak` | `git@github.com:akhmfz/papan-gerak.git` | `gh` CLI |

### 5.2 SSH Key Lokasi

| OS | Path |
|---|---|
| WSL (Arch Linux) | `~/.ssh/id_ed25519` |
| Windows | `C:\Users\Akhmfz\.ssh\id_ed25519` |

Key sudah di-copy dari WSL ke Windows saat setup.

### 5.3 Perintah Git Penting

```bash
# Status
git status
git diff
git log --oneline -10

# Commit dan push
git add -A
git commit -m "feat(scope): deskripsi"
git push origin main

# Lihat remote
git remote -v

# Ganti remote
git remote set-url origin git@github.com:akhmfz/obsidian-vault.git
```

### 5.4 Commit Convention

```
feat(scope): deskripsi     — fitur baru
fix(scope): deskripsi      — bug fix
docs(scope): deskripsi     — dokumentasi
refactor(scope): deskripsi — perubahan struktur
test(scope): deskripsi     — test
perf(scope): deskripsi     — optimasi
ci: deskripsi              — CI/CD
release: deskripsi         — rilis/tag
```

---

## 6. Siklus Kerja Lengkap

### 6.1 Flow Diagram

```
Mulai sesi baru
       │
       ▼
┌──────────────────────────────┐
│  READ PERTAMA:               │
│  • GRAPH_REPORT.md           │ ← Paham state graph terkini
│  • Obsidian notes relevan    │ ← Paham konteks & keputusan sebelumnya
│  • Agenda sesi               │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│  Pilih mode:                 │
│                              │
│  Apakah perubahan menyentuh  │
│  strategy() / scoring logic? │
│                              │
│  YA ───→ Plan Mode (Tab)     │
│  TIDAK → Build Mode (Tab)    │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│  KERJAKAN:                   │
│                              │
│  Plan Mode:                  │
│  • Analisa kode & graph      │
│  • Baca docs + catatan       │
│  • Susun proposal            │
│  • Anda review → setuju?     │
│                              │
│  Build Mode:                 │
│  • Implementasi              │
│  • Edit file .pine           │
│  • npm run build             │
│  • npm run test:all          │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│  SELESAI (wajib):            │
│                              │
│  1. /pine-lint               │ ← Cek konvensi Pine Script
│  2. graphify . --update      │ ← Update knowledge graph
│  3. graphify export obsidian │ ← Update vault notes
│  4. git add + commit + push  │ ← Simpan perubahan
│  5. Catat ke Obsidian vault  │ ← Keputusan & temuan
│  6. Jangan akhiri giliran    │ ← Kalau masih ada "next steps",
│     dengan rencana           │    kerjakan sekarang, bukan janji
└──────────────────────────────┘
```

### 6.2 Contoh Skenario: Tambah Filter Volume ke Entry Trigger

**Scenario:** Anda mau nambah kondisi "volume harus di atas SMA 20" sebagai syarat entry trigger di Papan Gerak.

```
Step 1: Plan Mode
  → "Saya mau tambah filter volume ke entry trigger Papan Gerak"
  → Agent baca:
     - docs/ARCHITECTURE.md (metodologi scoring)
     - 03-scoring.pine (kode entry trigger existing)
     - GRAPH_REPORT.md (state graph)
  → Agent usul:
     - Tambah input baru: volumeFilterToggle (bool, default true)
     - Di entry trigger: if enableVolumeFilter and not volumeOk → skip
     - Update docs
  → Anda review & setuju

Step 2: Build Mode
  → "Implement proposal"
  → Agent:
     - Edit 01-base.pine (tambah input)
     - Edit 03-scoring.pine (tambah guard di entry trigger)
     - Jalankan npm run build
     - Jalankan npm run test:all

Step 3: Selesai
  → /pine-lint src/modules/03-scoring.pine
  → graphify . --update --no-viz
  → graphify export obsidian --dir /mnt/c/Users/Akhmfz/obsidian-vault/papan-gerak
  → git add -A && git commit -m "feat(scoring): add volume filter to entry trigger"
  → Catat di Obsidian trading-journal/decisions/
```

### 6.3 Contoh Skenario: Refactor Besar (Rename/Hapus File)

```
1. Plan mode: rencanakan struktur baru
2. Build mode: hapus/rename file
3. Jalankan:
   graphify . --update --force    ← Force rebuild graph
   graphify export obsidian ...   ← Export vault
4. Commit + push
```

---

## 7. Pine Script v6 — Konvensi

### 7.1 Aturan Wajib

```pine
//@version=6
indicator("Nama Indikator", overlay=false)
```

| Aturan | Detail |
|---|---|
| **Version** | Selalu `//@version=6` |
| **Boolean** | Strict true/false. Tidak bisa `na`. Jangan pakai `na()`, `nz()`, atau `fixnan()` pada bool |
| **request.\*()** | Dynamic by default (v6). Boleh dipanggil di loop/kondisional |
| **int/int** | Bisa hasilkan float (5/2 = 2.5, bukan dibulatkan) |
| **enum** | Pakai `enum` + `input.enum()` daripada string mentah |

### 7.2 Anti-Pattern yang sudah di-CATATAN.md

```
⛔ Reserved keywords: base, open, high, low, close, volume, hl2, hlc3, ohlc4
⛔ NO local functions inside if blocks (Pine Script v6)
⛔ input.float() cannot default to na (pakai sentinel value -1.0)
⛔ Semicolons di if blocks
⛔ Error cascade — fix error PERTAMA dulu
⛔ Unicode + line breaks in ternary → fatal
```

### 7.3 Naming Convention

| Elemen | Gaya | Contoh |
|---|---|---|
| Variables | camelCase | `currentRatio` |
| Constants | UPPER_SNAKE_CASE | `MAX_SCORE` |
| Functions | camelCase (diawali kata kerja) | `calculateScore()` |
| Boolean | is/has/can/should prefix | `isBankSektor` |
| Float inputs | minval = -1.0 (sentinel) | `carInput` |

### 7.4 Struktur File (urutan wajib)

```
Header → indicator() → Inputs → Constants → Colors →
Utility Functions → Financial Functions → Sector Functions →
Score Calculation → Dashboard Rendering
```

---

## 8. Cara Inject Kode Pine ke Graph (Inject2)

### 8.1 Kenapa Perlu Inject?

Graphify menggunakan tree-sitter untuk parse AST — tapi **Pine Script (.pine) tidak termasuk** dalam 36 grammar yang didukung. Akibatnya:

- File `.pine` = unclassified, tidak diparse
- Fungsi scoring, input variables, sektor flags TIDAK masuk graph
- Graph hanya berisi: test files `.mjs`, config `.json`, docs `.md`

### 8.2 Solusi: Inject Manual via Python

Script Python membaca setiap file `.pine`, ekstrak simbol, lalu inject langsung ke `graph.json`.

### 8.3 Struktur Node untuk Kode Pine

```python
node = {
    "id": "src_modules_01base_f_scorehigher",   # path_module_namaFungsi
    "label": "f_scoreHigher(float v, float bad, float good)",  # Human readable
    "type": "function",                          # function / input / constant / variable
    "file_type": "code",                         # Selalu "code" untuk kode Pine
    "source_file": "/home/.../src/modules/01-base.pine",  # File asal
    "source_location": "01-base.pine:45",        # Baris
    "properties": {
        "module": "01-base",
        "category": "utility",                   # utility / input / scoring / sektor
        "returns": "float",
        "parameters": "v, bad, good"
    }
}
```

### 8.4 Jenis Node yang Di-inject

**Papan Instrumen (~230 nodes):**

| Kategori | Jumlah | Contoh ID |
|---|---|---|
| Utility functions | 36 | `src_modules_01base_f_scorehigher` |
| UI functions | 10 | `src_modules_03ui_f_cell` |
| Data functions | 5 | `src_modules_02data_f_fin` |
| Input variables | 44 | `src_modules_01base_warnaTema` |
| Financial fields | 32 | `src_modules_02data_roe` |
| Sector flags | 16 | `src_modules_02data_isBankSektor` |
| Ticker watchlists | 10 | `src_modules_02data_bankListIDX` |
| Scoring scores | 50 | `src_modules_04scoring_valueScore` |
| Scoring weights | 30 | `src_modules_04scoring_wPe` |
| Risk scores | 5 | `src_modules_04scoring_mcapScore` |
| Color constants | 15 | `src_modules_01base_tableBg` |
| Theme flags | 5 | `src_modules_01base_isDarkTheme` |
| Module nodes | 4 | `src_modules_01base` |

**Papan Gerak (~145 nodes):**

| Kategori | Jumlah | Contoh ID |
|---|---|---|
| Utility functions | 6 | `src_modules_01base_f_scoreRange` |
| Data functions | 4 | `src_modules_02data_f_choppiness` |
| Scoring functions | 6 | `src_modules_03scoring_f_trendScore` |
| UI functions | 4 | `src_modules_04ui_f_webhookMsg` |
| Input variables | 40 | `src_modules_01base_weightTrend` |
| TA indicators | 40 | `src_modules_02data_emaFast` |
| Scoring outputs | 8 | `src_modules_03scoring_trendScore` |
| Confluence counters | 8 | `src_modules_03scoring_trendBull` |
| Signal engine | 10 | `src_modules_03scoring_signalTriggered` |
| Alert events | 7 | `src_modules_04ui_entryAlert` |
| Module nodes | 4 | `src_modules_01base` |

### 8.5 Struktur Edge

```python
# Module dependency
edge = {
    "source": "src_modules_01base",
    "target": "src_modules_04scoring",
    "relation": "depends_on",
    "confidence": "EXTRACTED",
    "confidence_score": 1.0,
    "source_file": "/home/.../04-scoring.pine"
}

# Fungsi scoring memanggil utility
edge = {
    "source": "src_modules_04scoring_valueScore",
    "target": "src_modules_01base_f_scorehigher",
    "relation": "calls",
    "confidence": "EXTRACTED",
    "confidence_score": 1.0,
    "source_file": "/home/.../04-scoring.pine"
}

# Input menentukan color
edge = {
    "source": "src_modules_01base_warnaTema",
    "target": "src_modules_01base_tableBg",
    "relation": "determines",
    "confidence": "EXTRACTED",
    "confidence_score": 1.0,
    "source_file": "/home/.../01-base.pine"
}

# Financial field dari wrapper
edge = {
    "source": "src_modules_02data_roe",
    "target": "src_modules_02data_f_stat",
    "relation": "sourced_from",
    "confidence": "EXTRACTED",
    "confidence_score": 1.0,
    "source_file": "/home/.../02-data.pine"
}

# Sector flag mempengaruhi scoring
edge = {
    "source": "src_modules_02data_isBankSektor",
    "target": "src_modules_04scoring_healthScore",
    "relation": "influences",
    "confidence": "EXTRACTED",
    "confidence_score": 1.0,
    "source_file": "/home/.../04-scoring.pine"
}
```

### 8.6 Script Inject2 (Template)

```python
#!/usr/bin/env python3
"""Inject Pine Script symbols into Graphify graph.json"""

import json
from pathlib import Path

PROJECT = "/home/Akhmfz/papan-instrumen"
GRAPH_FILE = f"{PROJECT}/graphify-out/graph.json"

# 1. Baca graph existing
graph = json.loads(Path(GRAPH_FILE).read_text())

# 2. Definisikan nodes & edges Pine Script
pine_nodes = [...]
pine_edges = [...]

# 3. Dedup by id
existing_ids = {n["id"] for n in graph["nodes"]}
for n in pine_nodes:
    if n["id"] not in existing_ids:
        graph["nodes"].append(n)
        existing_ids.add(n["id"])

# 4. Tambah edges
existing_edges = set()
for e in graph["edges"]:
    existing_edges.add((e["source"], e["target"], e.get("relation", "")))
for e in pine_edges:
    key = (e["source"], e["target"], e.get("relation", ""))
    if key not in existing_edges:
        graph["edges"].append(e)
        existing_edges.add(key)

# 5. Update metadata
graph["metadata"]["total_nodes"] = len(graph["nodes"])
graph["metadata"]["total_edges"] = len(graph["edges"])

# 6. Tulis
Path(GRAPH_FILE).write_text(json.dumps(graph, indent=2))

print(f"Graph updated: {len(graph['nodes'])} nodes, {len(graph['edges'])} edges")
```

### 8.7 Cara Jalankan

```bash
# 1. Backup dulu
cp graphify-out/graph.json graphify-out/graph.json.bak

# 2. Jalankan inject
python3 scripts/inject-pine-pi.py

# 3. Export ke Obsidian
graphify export obsidian --dir /mnt/c/Users/Akhmfz/obsidian-vault/papan-instrumen

# 4. Push vault
cd /mnt/c/Users/Akhmfz/obsidian-vault
git add -A
git commit -m "feat: inject Pine Script symbols into PI graph"
git push
```

---

## 9. Troubleshooting

### 9.1 Graphify refuses to shrink graph.json

```
ERROR: refused to shrink graphify-out/graph.json (existing graph has more nodes)
```

**Penyebab:** Graph baru lebih kecil dari yang existing. Biasanya karena:
- Rebuild setelah hapus banyak file
- Inject manual dihapus/diganti

**Solusi:** Hapus graph.json dulu:
```bash
rm graphify-out/graph.json
graphify . --update --no-viz
```

### 9.2 AST extraction warning: extensions.json

```
warning: 1 source file(s) produced zero nodes
```

**Penyebab:** File JSON extension config tidak punya nodes yang bisa diekstrak. Aman diabaikan.

### 9.3 Semantic pass butuh waktu lama

**Penyebab:** Banyak file docs yang diproses via subagent.

**Solusi:** Set `GEMINI_API_KEY` untuk semantic pass via Gemini (lebih cepat):
```bash
export GEMINI_API_KEY="your-key"
pip install 'graphifyy[gemini]'
```

### 9.4 Windows Git: Permission denied (publickey)

```
git@github.com: Permission denied (publickey)
```

**Penyebab:** SSH key tidak ditemukan di Windows.

**Solusi:** Copy key dari WSL:
```bash
cp ~/.ssh/id_ed25519 /mnt/c/Users/Akhmfz/.ssh/
cp ~/.ssh/id_ed25519.pub /mnt/c/Users/Akhmfz/.ssh/
```

### 9.5 Git push: could not read Username

```
fatal: could not read Username for 'https://github.com'
```

**Penyebab:** Remote HTTPS tapi credential helper tidak bisa interaktif.

**Solusi:** Ganti remote ke SSH:
```bash
git remote set-url origin git@github.com:akhmfz/obsidian-vault.git
```

### 9.6 Obsidian vault notes tidak muncul

**Penyebab:** Folder vault tidak diregenerate setelah graph update.

**Solusi:**
```bash
graphify export obsidian --dir /path/to/vault --force
```

### 9.7 Pine script compile error di TradingView

**Penyebab:** Sintaks v6 error (local function di if block, reserved keyword, dll).

**Solusi:**
```bash
npm run lint           # Cek reserved keywords
npm run transpile      # Syntax check via PineTS
```

Lihat `CATATAN.md` untuk daftar lengkap anti-pattern.

---

## 10. Communication & Reporting Style

Gaya komunikasi agent selama sesi — diadopsi dari Claude Code Fable 5:

- **Lead with the outcome**: Baris pertama setelah selesai harus menjawab "apa yang terjadi" — TLDR dulu, detail setelahnya. Jangan mulai dengan kronologi.
- **Readable > concise**: Kalau user harus baca ulang, waktu yang dihemat oleh brevitas hilang. Tulis dalam kalimat lengkap dengan istilah teknis yang dieja, bukan fragmen/singkatan/jargon.
- **Calibrate ke pertanyaan**: Sederhana → jawab langsung dalam prosa. Kompleks → baru pakai header/section/tabel.
- **Code comments**: Hanya untuk menyatakan constraint yang tidak bisa ditunjukkan kode. Tidak untuk bilang "apa yang dilakukan baris berikutnya".
- **Report outcomes faithfully**: Kalau test fail, bilang "test fail". Kalau step dilewati, bilang dilewati. Selesai dan terverifikasi → state plainly tanpa "seharusnya" atau "semoga."
- **Evidence before action**: Jangan ubah system state tanpa verifikasi bahwa bukti mendukung aksi spesifik itu. Sinyal yang pattern-match ke failure known mungkin punya penyebab berbeda.

> Prinsip ini juga terdaftar di `AGENTS.md` bagian 11.

---

## 11. Cheat Sheet

### 11.1 Perintah Cepat

```bash
# ===== GRAPHIFY =====
graphify .                    # Full pipeline
graphify . --update           # Incremental
graphify . --cluster-only     # Re-cluster
graphify query "..."          # Query graph
graphify path "A" "B"         # Shortest path
graphify export obsidian -d DIR  # Export vault

# ===== BUILD & TEST =====
npm run build                 # Concatenate modules
npm run lint                  # Cek reserved keywords
npm run test:all              # Jalankan semua test
npm run ci                    # Full pipeline

# ===== GIT =====
git status
git diff
git add -A && git commit -m "msg" && git push

# ===== OBSIDIAN VAULT =====
cd /mnt/c/Users/Akhmfz/obsidian-vault
git pull
git add -A && git commit -m "msg" && git push
```

### 11.2 Flow Sesi Singkat

```
1. Mulai → baca GRAPH_REPORT.md + catatan Obsidian
2. Plan mode → susun rencana (skip untuk perubahan kecil)
3. Build mode → implementasi (autonomous — jangan tanya izin)
4. /pine-lint + npm run test:all
5. graphify . --update --no-viz
6. graphify export obsidian --dir ...
7. git add/commit/push (kode)
8. Catat di Obsidian vault
9. Jangan akhiri dengan rencana — kalau masih ada yang bisa
   dikerjakan, kerjakan sekarang. Baru akhiri giliran.
10. Vault auto push (dalam 10 menit)
```

### 11.3 File Penting

| File | Isi |
|---|---|
| `AGENTS.md` | Konfigurasi global OpenCode (+ file ini) |
| `src/modules/*.pine` | Source code Pine Script (edit di sini) |
| `graphify-out/GRAPH_REPORT.md` | State graph terkini |
| `graphify-out/graph.json` | Raw data graph |
| `CATATAN.md` | Lessons learned, anti-pattern |
| `docs/ARCHITECTURE.md` | Metodologi scoring & arsitektur |
| `docs/DEVELOPMENT.md` | Changelog, sprint, backlog |
| `.opencode/plugins/graphify.js` | Plugin OpenCode untuk Graphify |
| `.obsidian/plugins/obsidian-git/data.json` | Konfigurasi auto sync vault |

### 11.4 Label Prioritas Issue

| Label | Warna | Arti |
|---|---|---|
| `P1-critical` | 🔴 | Bug kritis, compile error |
| `P2-high` | 🟠 | Fitur dampak besar |
| `P3-medium` | 🟢 | UX, docs, improvement |
| `P4-low` | 🟣 | Long-term ideas |

---

> **Dokumentasi ini diperbarui:** 2026-07-08
> **Oleh:** OpenCode — Sesi Pattern Update AGENTS.md
> **Untuk:** Proyek Papan Instrumen & Papan Gerak
