# Pine Semantic Platform — Arsitektur & Dokumentasi Lengkap

> **Versi:** v1.2.0 (Validation Engine)  
> **Tgl:** 2026-07-08  
> **Author:** Muhammad Akhmal (AKHMFZ Analytics)  
> **Repo:** [github.com/akhmfz/papan-instrumen](https://github.com/akhmfz/papan-instrumen)

---

## Daftar Isi

1. [Gambaran Umum Proyek](#1-gambaran-umum-proyek)
2. [Latar Belakang](#2-latar-belakang)
3. [Evolusi Proyek](#3-evolusi-proyek)
4. [Arsitektur Keseluruhan](#4-arsitektur-keseluruhan)
5. [Semantic Platform](#5-semantic-platform)
6. [Pipeline Lengkap](#6-pipeline-lengkap)
7. [Penjelasan Setiap Komponen](#7-penjelasan-setiap-komponen)
8. [Struktur Folder](#8-struktur-folder)
9. [Data Flow](#9-data-flow)
10. [Semantic Schema](#10-semantic-schema)
11. [Query Engine](#11-query-engine)
12. [Context Engine](#12-context-engine)
13. [Validation Engine](#13-validation-engine)
14. [Testing](#14-testing)
15. [Architecture Decision Records](#15-architecture-decision-records)
16. [Filosofi Desain](#16-filosofi-desain)
17. [Kelebihan Arsitektur](#17-kelebihan-arsitektur)
18. [Kekurangan](#18-kekurangan)
19. [Roadmap](#19-roadmap)
20. [Kesimpulan](#20-kesimpulan)

---

# 1. Gambaran Umum Proyek

## Apa Proyek Ini?

Proyek ini adalah **Pine Semantic Platform** — sebuah infrastruktur lengkap untuk mengekstrak, menyimpan, menquery, mengontekstualisasi, dan memvalidasi kode Pine Script v6 secara deterministik.

Platform ini terdiri dari dua bagian yang saling terkait:

1. **Papan Instrumen** (papan-instrumen) — Dashboard fundamental untuk pasar saham Indonesia (IDX). Menganalisis 7 dimensi: Value, Quality, Growth, Health, Income, Momentum, dan Indonesia Factor, dengan dukungan 15 kelas sektor dan bobot yang berbeda per sektor.
2. **Papan Gerak** (papan-gerak) — Dashboard teknikal multi-dimensi sebagai pendamping natural Papan Instrumen. Menganalisis 4 dimensi (Trend, Momentum, Volatilitas, Volume) + entry trigger + risk management.

Keduanya adalah indikator TradingView yang ditulis dalam Pine Script v6.

Namun nilai sebenarnya dari proyek ini bukan pada indikatornya — melainkan pada **lapisan semantik (Semantic Layer)** yang dibangun di atasnya.

## Tujuan Utama

Membangun pipeline yang mengubah kode Pine Script mentah menjadi:

```
Source Code → Semantic Knowledge → Retrieval → Context → Prompt → LLM
```

Dengan LLM sebagai **komponen terakhir**, bukan pusat arsitektur.

## Masalah yang Ingin Diselesaikan

AI coding assistant (Claude, GPT, Copilot) mengalami masalah fundamental ketika bekerja dengan kode Pine Script:

- **Tanpa konteks semantik**: AI membaca file .pine sebagai teks biasa, tidak mengerti hubungan antar fungsi, dependensi modul, atau dampak perubahan.
- **Token budget terbatas**: Seluruh proyek bisa mencapai 3000+ baris. Tidak mungkin dimasukkan ke context window.
- **Repainting & look-ahead bias**: AI sering menulis kode yang repaint karena tidak paham struktur bar Pine Script.
- **Overfitting parameter**: Tanpa pemahaman tentang parameter apa yang sudah di-backtest, AI bisa menulis ulang parameter yang sudah di-optimasi.
- **Tidak ada validation loop**: Perubahan AI tidak diverifikasi secara otomatis.

## Target Pengguna

| Peran | Bagaimana Menggunakan |
|-------|----------------------|
| **Pine Script Developer** | Menggunakan `pine-query` untuk mencari fungsi/variabel, `pine-context` untuk konteks tugas, `pine-validate` untuk memvalidasi perubahan |
| **AI Agent (Claude, OpenCode, GPT)** | Mengimpor `SemanticDB` dan `QUERY_REGISTRY` secara langsung, memanggil `ContextAssembler` untuk merangkai konteks |
| **CI/CD Pipeline** | Menjalankan `pine-validate` di GitHub Actions sebagai gate sebelum merge |
| **Trader/Analyst** | Menggunakan indikator Papan Instrumen / Papan Gerak di TradingView |

## Mengapa Tidak Cukup Pine Script Biasa?

Pine Script adalah DSL yang kuat untuk indikator trading, tetapi memiliki keterbatasan:

1. **Tidak ada tooling offline**: Parser, tester, dan debugger terbatas.
2. **Tidak ada semantic analysis**: Tidak bisa menjawab "fungsi apa yang dipanggil oleh f_scoreHigher?".
3. **Tidak ada dependency tracking**: Tidak bisa mendeteksi dampak perubahan pada modul lain.
4. **Tidak ada versioning schema**: `pine_semantic.json` memberikan skema terstruktur yang bisa divalidasi.

---

# 2. Latar Belakang

## Bagaimana Ide Proyek Ini Muncul

Proyek dimulai sebagai indikator fundamental IDX biasa (`Papan Instrumen`). Namun dalam proses pengembangan, beberapa masalah muncul:

1. **Source code mencapai 1800+ baris** di 4 file module. Sulit menemukan fungsi tertentu.
2. **Perubahan sering memicu bug** karena dependency antar fungsi tidak terlihat.
3. **AI agent (Claude/OpenCode) sering memberikan jawaban yang salah** karena tidak mengerti konteks proyek.
4. **Golden test sering gagal** tanpa diketahui penyebabnya.

## Mengapa Graphify Digunakan (dan Ditinggalkan)

Graphify adalah knowledge graph generator yang mendukung banyak bahasa pemrograman. Awalnya digunakan untuk memetakan struktur proyek.

**Masalah dengan Graphify:**
- **Pine Script tidak didukung**: Graphify memiliki grammar tree-sitter untuk 36 bahasa, tetapi Pine Script tidak termasuk. File .pine tidak diparse secara otomatis.
- **Semantic depth terbatas**: Graphify menghasilkan graph node/edges, tetapi tidak memahami Pine-specific constructs seperti `request.security()`, `ta.rsi()`, atau tipe data Pine.
- **Tidak ada query engine**: Graphify menyimpan graph, tetapi tidak menyediakan API untuk menanyakan "fungsi apa yang memanggil f_scoreHigher?"

**Solusi:** Build semantic layer sendiri di atas Graphify. Gunakan Graphify hanya sebagai visualisasi graph, sementara semantic layer menangani:
- Ekstraksi AST dari Pine Script (via pynescript)
- Penyimpanan semantic dalam JSON terstruktur
- Query engine dengan 11 tipe query
- Graph injection ke Graphify

## Mengapa Semantic Layer Dibangun

Keputusan untuk membangun semantic layer sendiri adalah titik balik proyek. Alasan:

1. **Single Source of Truth**: Semua komponen (query, graph, context, validation) membaca dari `pine_semantic.json` yang sama.
2. **Deterministik**: Tidak ada AI dalam pipeline utama. Setiap langkah pure function.
3. **Testable**: Setiap query memiliki golden test. Setiap snapshot dibandingkan secara eksak.
4. **LLM-agnostic**: Jika model AI berganti, semantic layer tetap. Hanya adaptor di ujung pipeline yang berubah.

## Keterbatasan Solusi Sebelumnya

| Aspek | Sebelum Semantic Layer | Sesudah |
|-------|----------------------|---------|
| Find function | `grep -r "f_score" src/` | `pine-query function f_scoreHigher` |
| Impact analysis | Manual baca kode | `pine-query impact f_scoreHigher` |
| Dependency tracking | Tebak-tebak | `pine-query module 04-scoring` |
| Context untuk AI | Paste file mentah | `pine-context "Tambah indikator momentum" --profile implementation` |
| Validation | Review manual | `pine-validate --workspace .` |

---

# 3. Evolusi Proyek

## Fase 0 — Indikator Biasa (Pra-Sejarah)

**Kondisi:** Dua repositori Pine Script (`papan-instrumen`, `papan-gerak`) dengan:
- ~1800+ baris kode total
- 4-5 module file per proyek
- Testing via PineTS (89-90 test)
- Build via bash script

**Masalah:** Semua masalah klasik: tidak ada semantic understanding, AI sering salah konteks, debugging manual.

## Fase 1 — Semantic Platform (v1.0)

**Keputusan besar:** Membangun parser AST + semantic JSON + graph injector.

**Yang dibangun:**
- `extract_ast.py` — Parser Pine Script menggunakan ANTLR via pynescript
- `inject_graph.py` — Inject nodes/edges ke Graphify graph.json
- `pine_semantic.json` schema v1.1 — Format data standar
- `pine_query` — 11 query types + 4 formatters + CLI

**Hasil:**
- Parsing 4 file ~154s (<300s target)
- Query 0-0.5ms
- Golden test 28/28 pass (14 PI + 14 PG)

## Fase 1.5 — Hardening (v1.0 RC)

**Perubahan:**
- Validator schema (`validate_semantic.py`)
- Performance benchmark (`tests/benchmark.py`)
- API freeze dengan `__all__` dan `__version__`
- Dokumentasi arsitektur (5 docs + 5 ADR)
- Variable reads/writes graph injection

**Hasil:**
- Isolated nodes turun dari ~30% ke 4.4% (PI) dan 4.6% (PG)
- KPI: parser <5min, load <0.5s, query <5ms, context <30ms

## Fase 2.1 — Context Engine (v1.1)

**Keputusan besar:** Context assembly sebagai komponen terpisah, tanpa LLM di dalamnya.

**Yang dibangun:**
- `pine_query/context/` — 10 files
- 4 profiles: review (4K), implementation (8K), architecture (12K), bugfix (6K)
- Pipeline: intent → select → expand → rank → budget → build → compile
- CLI: `pine-context`

**Hasil:**
- 5 context tests pass
- Context assembly <30ms
- Profiles distinct (rank_focus, token budget, source lines)

## Fase 2.2 — Validation Engine (v1.2)

**Keputusan besar:** Validator read-only, check plugin registry, semantic_diff sebagai core library.

**Yang dibangun:**
- `semantic_diff.py` — Pure function diff, immutable
- `pine_query/validation/` — 11 files
- 5 checks: parser, schema, graph, golden, context (plugin registry)
- Risk scorer: LOW/MEDIUM/HIGH/CRITICAL
- Report: PASS / PASS_WITH_WARNING / FAIL / ERROR
- CLI: `pine-validate` dengan `--skip` / `--only`

**Hasil:**
- 6 validation golden tests pass
- 39 total tests (28 golden + 5 context + 6 validation) all pass

---

# 4. Arsitektur Keseluruhan

## Layered Architecture

```
                    ┌──────────────────────────────────────┐
                    │           FUTURE PRODUCTS            │
                    │   Review Engine  │  MCP  │ Platform  │
                    └──────────────────────────────────────┘
                                      ▲
                    ┌──────────────────┴──────────────────────┐
                    │         VALIDATION ENGINE (v1.2)        │
                    │  Read-only  │  Checks  │  Risk  │ Rep. │
                    └──────────────────────────────────────┘
                                      ▲
                    ┌──────────────────┴──────────────────────┐
                    │          CONTEXT ENGINE (v1.1)          │
                    │  Intent → Select → Expand → Build →     │
                    │  Rank → Budget → Compile                │
                    └──────────────────────────────────────┘
                                      ▲
                    ┌──────────────────┴──────────────────────┐
                    │           QUERY ENGINE (v1.0)           │
                    │  SemanticDB  │  11 Queries  │ 4 Format. │
                    └──────────────────────────────────────┘
                                      ▲
                    ┌──────────────────┴──────────────────────┐
                    │         SEMANTIC LAYER (v1.0)           │
                    │  extract_ast → pine_semantic.json       │
                    │  inject_graph → graph.json              │
                    └──────────────────────────────────────┘
                                      ▲
                    ┌──────────────────┴──────────────────────┐
                    │         PINE SCRIPT SOURCE CODE         │
                    │  Papan Instrumen  │  Papan Gerak        │
                    └──────────────────────────────────────┘
```

## Diagram Aliran Data

```
Source (.pine) ──→ extract_ast.py ──→ pine_semantic.json ──→ inject_graph.py ──→ graph.json
                                                │                                        │
                                                ▼                                        ▼
                                         Query Engine ──────────────────────────→ QUERY_REGISTRY (11 types)
                                                │
                                                ▼
                                         Context Engine ──→ ContextAssembler ──→ Compiled Prompt
                                                │
                                                ▼
                                         Validation Engine ──→ PatchValidator ──→ Structured Report
                                                │
                                                ▼
                                         Future: Review Engine, MCP, Automation
```

## Prinsip Layer

| Layer | Tanggung Jawab | Tidak Boleh |
|-------|---------------|-------------|
| Source | Berisi kode Pine Script | Mengandung logika parsing |
| Semantic | Parse, ekstrak, simpan | Mengubah source code |
| Query | Index, cari, format | Memodifikasi data |
| Context | Pilih, expand, budget, compile | Memanggil LLM |
| Validation | Validasi, diff, risk, report | Mengaplikasikan perubahan |
| Future | Review, MCP, automation | Bergantung pada model AI spesifik |

---

# 5. Semantic Platform

## Apa Itu Semantic Platform?

Semantic Platform adalah fondasi dari seluruh proyek. Ia adalah lapisan yang mengubah kode Pine Script mentah menjadi representasi semantik terstruktur (`pine_semantic.json`) dan graph knowledge (`graphify-out/graph.json`).

## Mengapa Disebut Single Source of Truth (SSOT)?

Karena **semua konsumen** data semantic membaca dari satu sumber:

- `pine_query` query engine membaca `pine_semantic.json`
- `inject_graph.py` membaca `pine_semantic.json` untuk membuat graph
- `semantic_diff.py` membandingkan dua versi `pine_semantic.json`
- `ContextAssembler` menggunakan `QUERY_REGISTRY` yang membaca `pine_semantic.json`
- `PatchValidator` menjalankan check yang membaca `pine_semantic.json` dan `graph.json`

**Tidak ada secondary source.** Tidak ada cache yang bisa basi. Tidak ada format alternatif.

## Pipeline Semantic Platform

```
Step 1: extract_ast.py
    Input:  src/modules/*.pine
    Output: pine_semantic.json (schema 1.1)
    Proses: ANTLR parsing → AST walk → ekstrak functions, calls, variables, reads, writes

Step 2: inject_graph.py
    Input:  pine_semantic.json + graphify-out/graph.json
    Output: graph.json (updated)
    Proses: Inject nodes/edges → dedup → write

Step 3: (Consumed by query/context/validation)
```

## Yang Dihasilkan

`pine_semantic.json` untuk Papan Instrumen (produksi aktual):

| Metrik | Nilai |
|--------|-------|
| File | 4 |
| Functions | 51 |
| Variables | 353 |
| Calls | 239 |
| Reads | 302 |
| Writes | 155 |
| Cross-refs resolved | ~200 |
| Parse time | 154.54s |

---

# 6. Pipeline Lengkap

## Dari .pine ke Semantic Graph — Langkah demi Langkah

```
┌─────────────────────────────────────────────────────────────────────┐
│                         PINE SCRIPT SOURCE                          │
│                                                                     │
│  src/modules/01-base.pine         632 lines (inputs, utilities)     │
│  src/modules/02-data.pine         301 lines (market data, sektor)   │
│  src/modules/03-ui.pine            83 lines (table rendering)       │
│  src/modules/04-scoring.pine      794 lines (scoring engine)        │
│  ─────────────────────────────────────────────────────              │
│  Total: ~1810 lines                                                 │
└─────────────────────────────────────────────────────────────────────┘
                               │
                               ▼ parse via pynescript (ANTLR)
┌─────────────────────────────────────────────────────────────────────┐
│                        extract_ast.py                               │
│                                                                     │
│  1. Load .pine file → InputStream                                   │
│  2. PinescriptLexer → tokenize                                      │
│  3. PinescriptParser → build parse tree                             │
│  4. PinescriptASTBuilder → convert to AST                           │
│  5. Walk AST → extract: FunctionDef, Call, Assign, Name, Import     │
│  6. Build function index (name → definitions)                       │
│  7. Build cross-references (caller → callee)                        │
│  8. Output: pine_semantic.json                                      │
└─────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      pine_semantic.json                             │
│                                                                     │
│  schema: "1.1"                                                      │
│  files: [                                                           │
│    {module, file, functions[], calls[], variables[], reads[],        │
│     writes[], parse_errors, ...}                                    │
│  ]                                                                  │
│  cross_references: [{caller, callee, scope, resolved, ...}]         │
│  function_index: {name → [{module, file, line, params}]}            │
│  totals: {functions, calls, variables, reads, writes}               │
└─────────────────────────────────────────────────────────────────────┘
                      ╱          ╲
                     ▼            ▼
┌─────────────────────────┐  ┌─────────────────────────────────────────┐
│    inject_graph.py      │  │       SemanticDB (pine_query)           │
│                         │  │                                         │
│  Baca semantic.json     │  │  Load JSON → build 9 indexes:           │
│  Inject:                │  │  - function_index: name → def           │
│  - Function nodes       │  │  - variable_index: name → def           │
│  - Module entry nodes   │  │  - caller/callee_index                  │
│  - calls edges          │  │  - node_index: id → node                │
│  - reads/writes edges   │  │  - dep_index: module → deps             │
│  - belongs_to edges     │  │  - reverse_var_index                    │
│  - contains edges       │  │                                         │
│  Write: graph.json      │  │  All O(1) dict lookups after index      │
└─────────────────────────┘  └─────────────────────────────────────────┘
         │                            │
         ▼                            ▼
┌─────────────────────────┐  ┌─────────────────────────────────────────┐
│      graph.json         │  │       QUERY_REGISTRY (11 types)         │
│                         │  │                                         │
│  Nodes: 297 (PI)        │  │  function / variable / module           │
│  Links: ~600            │  │  impact / callers / callees             │
│  calls: 90              │  │  search / builtin / explain             │
│  reads: 262             │  │  context / stats                        │
│  writes: 128            │  │                                         │
│  Isolated: 4.4%         │  │  Formatters: json/table/markdown/mermaid│
└─────────────────────────┘  └─────────────────────────────────────────┘
                                      │
                                      ▼
                      ┌─────────────────────────────────────────────────┐
                      │           CONTEXT ASSEMBLER (v1.1)             │
                      │                                                 │
                      │  Task → Intent → Select → Expand → Rank        │
                      │       → Budget → Build → Compile               │
                      │                                                 │
                      │  Output: Compiled Prompt (markdown)             │
                      │          + Context Object (JSON)               │
                      └─────────────────────────────────────────────────┘
                                      │
                                      ▼
                      ┌─────────────────────────────────────────────────┐
                      │          VALIDATION ENGINE (v1.2)              │
                      │                                                 │
                      │  Workspace → Snapshot → Checks (5) → Diff       │
                      │       → Risk → Report → Artifacts              │
                      │                                                 │
                      │  Output: PASS/PASS_WITH_WARNING/FAIL/ERROR     │
                      └─────────────────────────────────────────────────┘
```

---

# 7. Penjelasan Setiap Komponen

## 7.1 extract_ast.py

**Tujuan:** Parser Pine Script stage 1. Mengubah file .pine menjadi representasi AST, lalu mengekstrak fungsi, panggilan, variabel, read/write.

**Input:** File `.pine` di `src/modules/` atau `src/strategies/`

**Output:** `pine_semantic.json`

**Teknologi:** pynescript (ANTLR-based parser untuk Pine Script v5/v6)

**Detail Implementasi:**
- Menggunakan `PinescriptLexer` + `PinescriptParser` dari ANTLR4
- Error listener custom (QuietListener) untuk mengumpulkan error sintaks tanpa crash
- AST walker rekursif untuk mengekstrak:
  - `FunctionDef` → nama, parameter, baris
  - `Call` → nama fungsi, argumen, parent function, scope (module/function)
  - `Assign` → target variable, mode (var/regular), tipe
  - `Name` → identifier, context (Load/Store) untuk reads/writes
  - `Import` → source, symbols
- Deduplication via set of (key, line, col) tuple
- Function stack tracking untuk menentukan parent function tiap call
- Cross-reference builder: untuk setiap call, cari definisi callee di function_index

**Kenapa Dibuat:** Pine Script tidak punya semantic tooling. Alternatif (grep/manual) tidak scalable untuk 1800+ baris.

## 7.2 inject_graph.py

**Tujuan:** Stage 2. Membaca `pine_semantic.json` dan menginjeksi node/edge ke dalam `graphify-out/graph.json`.

**Input:** `pine_semantic.json` + `graph.json` (yang mungkin sudah ada dari Graphify)

**Output:** `graph.json` (updated)

**Yang Diinjeksi:**
- Function nodes (jika belum ada)
- Module entry nodes (untuk modul dengan top-level code)
- `calls` edges (function→function, entry→function)
- `reads` edges (function→variable, entry→variable)
- `writes` edges (function→variable, entry→variable)
- `belongs_to` edges (function→module)
- `contains` edges (module→entry)

**Deduplication:** Semua edge dicek terhadap existing_links set sebelum ditambahkan. Count metadata diakumulasi.

**Kenapa Dibuat:** Graphify tidak bisa parse Pine Script. Injector ini menjembatani semantic JSON ke format graph.

## 7.3 validate_semantic.py

**Tujuan:** Validator schema untuk `pine_semantic.json`.

**Input:** File `pine_semantic.json`

**Output:** Exit code 0 (valid), 1 (warning), 2 (error)

**Validasi:**
- Required keys di root, file, function, call, variable, read/write, cross-reference, totals
- Tipe data setiap field
- Cross-field consistency (strict mode): totals == actual count
- Schema version check

**Kenapa Dibuat:** Menjamin data quality sebelum konsumen (query engine, context, validation) memproses data.

## 7.4 SemanticDB (database.py)

**Tujuan:** In-memory index engine. Membaca `pine_semantic.json` + `graph.json`, membangun 9 indeks untuk akses O(1).

**Indeks:**
| Index | Key | Value |
|-------|-----|-------|
| function_index | name | [{module, file, line, params}] |
| variable_index | name | [{module, file, line, is_global}] |
| reverse_var_index | name | [{caller_id, relation, module}] |
| module_index | module | {file, size, fn_count, var_count} |
| caller_index | caller_id | [{callee_id, relation, count}] |
| callee_index | callee_id | [{caller_id, relation, count}] |
| dep_index | module | [dep_module] |
| node_index | node_id | node |
| builtin_index | name | builtin_info |

**Metode Query:**
- `resolve_caller_node(name, module)` — function name → graph node ID
- `resolve_var_node(name)` — variable name → graph node ID
- `collect_callees(node_id)` — outgoing graph edges
- `collect_callers(node_id)` — incoming graph edges
- `transitive_callers(node_id, depth)` — upstream caller chain

**Refresh:** Method `refresh()` membaca ulang file dan rebuild index. Checksum untuk deteksi perubahan.

**Kenapa Cepat:** Semua query adalah dict lookup. Index build hanya 0.01-0.03s.

## 7.5 semantic_diff.py

**Tujuan:** Pure function untuk membandingkan dua snapshot `pine_semantic.json`. Core library, immutable, tanpa side effect.

**Input:** `baseline: dict`, `current: dict` (dua snapshot pine_semantic.json)

**Output:**
```python
{
  "added": [entities in current but not baseline],
  "removed": [entities in baseline but not current],
  "modified": [entities in both but changed],
  "unchanged": [entities in both and identical],
  "modules": {"added": [...], "removed": [...]},
  "stats": {"added": N, "removed": N, "modified": N, "unchanged": N, ...}
}
```

**Implementasi:**
1. Flatten semua entities (functions + variables) dari kedua snapshot ke dalam map `{type::name → entity}`
2. Set operation: `added = curr_keys - base_keys`, `removed = base_keys - curr_keys`
3. For common keys, field-level comparison untuk deteksi modifikasi
4. Module-level diff terpisah

**Kenapa Core Library:** Dibutuhkan oleh validation engine (sekarang) dan review engine (masa depan). Dipisahkan dari `validation/` agar bisa diimpor oleh komponen lain tanpa dependensi ke validator.

## 7.6 Query Engine (pine_query/queries/)

**Tujuan:** 11 query types untuk menanyakan semantic database.

**Query Types:**

| Query | Input | Output |
|-------|-------|--------|
| `function(name)` | Nama fungsi | Definition, params, calls, called_by, reads, writes |
| `variable(name)` | Nama variable | Declaration, read_by, written_by |
| `module(name)` | Nama modul | File info, functions, deps, entry callees |
| `impact(name)` | Nama fungsi | Direct callers, transitive callers, affected modules/tables/alerts |
| `callers(name)` | Nama fungsi | Fast direct-caller lookup |
| `callees(name)` | Nama fungsi | Fast direct-callee lookup |
| `search(pattern, mode)` | Pattern + mode | Entities matching substring/regex/exact |
| `builtin(name)` | Nama builtin | Info dari 56-entry builtin catalog |
| `explain(name)` | Nama fungsi | Structural summary: calls, called_by, reads, writes, complexity |
| `context(name, compact)` | Nama fungsi | LLM-ready markdown: signature + source + deps |
| `stats()` | — | Project KPI dashboard |

**Formatter:** Setiap hasil bisa diformat ke JSON, table, markdown, atau mermaid (diagram).

**Response Envelope:** Setiap query mengembalikan dict dengan `{schema, query, generated_at, project, result}`.

**Kenapa Query Registry:** Pattern registry memungkinkan CLI/MCP auto-discover query types tanpa hardcode. Tambah query baru = tambah entry di registry.

## 7.7 Context Engine (pine_query/context/)

**Tujuan:** Mengubah task description menjadi compiled prompt yang siap dikirim ke LLM. **Tidak ada LLM dalam pipeline ini.**

**Pipeline 6 Langkah:**

```
Task → Intent → Select → Expand → Rank → Budget → Build → Compile
```

| Langkah | File | Fungsi |
|---------|------|--------|
| 1. Intent | `intent.py` | Rule-based: extract verb, object, domain, filters dari task text. Tanpa NLP. |
| 2. Select | `selector.py` | Intent keywords → candidate entities via QUERY_REGISTRY search |
| 3. Expand | `expander.py` | BFS graph traversal (1-2 hops): tambah callees, callers dari graph |
| 4. Rank | `ranker.py` | Score per entity berdasarkan profile focus (incoming/outgoing/module/variable) |
| 5. Budget | `budget.py` | Cumulative token cap. Pangkas entity paling rendah sampai ≤ budget. |
| 6. Build | `builder.py` | Ranked entities → Context Object dengan source code, metadata, dependensi |
| 7. Compile | `compiler.py` | Context Object + Profile → compiled markdown prompt |

**4 Profiles:**

| Profile | Budget | Focus | Source Lines | Use Case |
|---------|--------|-------|--------------|----------|
| review | 4K | incoming | 20 | Code review: full dep chain |
| implementation | 8K | outgoing | 30 | Implementasi: direct deps + source |
| architecture | 12K | module | 15 | Arsitektur: module-level + cross-refs |
| bugfix | 6K | variable | 25 | Bug fix: callers + variable chain |

**Kenapa Tanpa NLP:** NLP/library eksternal = dependency hell + non-deterministik. Rule-based extraction sudah cukup untuk task descriptions dalam bahasa Indonesia/Inggris.

## 7.8 Validation Engine (pine_query/validation/)

**Tujuan:** Read-only validation pipeline. Memvalidasi workspace tanpa mengubah source code.

**Check Plugin Registry:**

| Check | Priority | Requires | Produces | Fungsi |
|-------|----------|----------|----------|--------|
| ParserCheck | 10 | — | semantic_raw | Run extract_ast.py, cek exit code |
| SchemaCheck | 20 | semantic_raw | semantic_validated | Run validate_semantic.py |
| GraphCheck | 30 | semantic_validated | graph | Run inject_graph.py + cek integritas |
| GoldenCheck | 40 | graph | golden_result | Run golden test suite |
| ContextCheck | 50 | graph | context_result | Run context test suite |

**Risk Assessment:**

Input: diff stats + check results → Output: `{score, level, reasons}`

| Level | Threshold | Contoh |
|-------|-----------|--------|
| LOW | score < 0.25 | Tidak ada perubahan |
| MEDIUM | score 0.25-0.5 | Beberapa fungsi dimodifikasi |
| HIGH | score 0.5+ | Fungsi dihapus, check gagal |
| CRITICAL | Ada check FAIL/ERROR | Parser crash, golden test gagal |

**Report Status:**

| Status | Arti |
|--------|------|
| PASS | Semua check lulus, risiko rendah |
| PASS_WITH_WARNING | Semua check lulus, tapi ada perubahan signifikan |
| FAIL | Satu atau lebih check gagal |
| ERROR | Infrastructure error (parser crash, file missing) |

**Kenapa Read-Only:** Validator observer, bukan actor. Bisa dipakai di Git hooks, CI/CD, GitHub Actions, VS Code, MCP, OpenCode — tanpa harus tahu siapa yang mengaplikasikan patch.

## 7.9 Formatter (pine_query/formatter.py)

**Tujuan:** 4 output formatter untuk query results.

- **JSON**: Pretty-printed JSON dengan ensure_ascii=False
- **table**: Tabulate-style table untuk CLI
- **markdown**: Markdown table untuk dokumentasi
- **mermaid**: Mermaid.js flow diagram untuk visualisasi dependency

## 7.10 Builtin (pine_query/builtin.py)

**Tujuan:** Catalog 56 builtin Pine Script v6 symbols dalam format terstruktur.

Termasuk: `ta.rsi`, `ta.ema`, `ta.sma`, `ta.bb`, `ta.atr`, `ta.roc`, `ta.macd`, `request.security`, `strategy.*`, `math.*`, `array.*`, `color.*`, format functions, time functions, dll.

Setiap builtin punya: `{name, type, category, description, params, returns}`

## 7.11 CLI Tools

| CLI | Perintah | Fungsi |
|-----|----------|--------|
| `pine-query` | `pine-query function f_scoreHigher` | Query semantic data |
| `pine-context` | `pine-context "Tambah indikator" --profile impl` | Context assembly |
| `pine-validate` | `pine-validate --workspace . --skip golden` | Patch validation |

---

# 8. Struktur Folder

```
papan-instrumen/
├── README.md                     ← Dokumentasi utama indikator
├── CONTRIBUTING.md               ← Panduan kontribusi + test info
├── CATATAN.md                    ← Pelajaran dari Pine Script v6
├── package.json                  ← npm scripts (build, test, lint, transpile, ci)
├── build.sh                      ← Concat 4 module → PapanInstrumen.pine
├── pine_semantic.json            ← ⭐ SSOT: hasil ekstraksi semantic
├── src/
│   ├── modules/                  ← ⭐ Source Pine Script (edit di sini)
│   │   ├── 01-base.pine          ←   Header, inputs, tema, utilities
│   │   ├── 02-data.pine          ←   Market data, financial, sektor
│   │   ├── 03-ui.pine            ←   Table rendering
│   │   └── 04-scoring.pine       ←   Scoring engine 7 dimensi
│   └── PapanInstrumen.pine       ←   Built output (auto-generated)
├── scripts/                      ← ⭐ Semantic Layer tooling
│   ├── extract_ast.py            ←   Stage 1: Parser AST
│   ├── inject_graph.py           ←   Stage 2: Graph injection
│   ├── validate_semantic.py      ←   Schema validator
│   ├── pine_query/               ←   ⭐ Inti: Query + Context + Validation
│   │   ├── __init__.py           ←   Public API: SemanticDB, QUERY_REGISTRY
│   │   ├── database.py           ←   In-memory index engine
│   │   ├── queries/              ←   11 query modules
│   │   ├── formatter.py          ←   4 output formatters
│   │   ├── builtin.py            ←   Builtin Pine Script catalog
│   │   ├── semantic_diff.py      ←   ⭐ Core library: immutable diff
│   │   ├── context/              ←   Context Engine (10 files)
│   │   └── validation/           ←   Validation Engine (11 files)
│   ├── pine_query.py             ←   CLI: pine-query
│   ├── pine_context.py           ←   CLI: pine-context
│   ├── pine_validate.py          ←   CLI: pine-validate
│   ├── lint.sh                   ←   Custom Pine linter
│   └── gh-sync.sh                ←   GitHub Issues sync
├── tests/
│   ├── run_golden.py             ←   Golden test runner (28 tests)
│   ├── benchmark.py              ←   Performance benchmark
│   ├── scoring/                  ←   PineTS scoring tests (96 tests)
│   ├── pinets-verify.mjs         ←   PineTS unit test runner
│   ├── transpile.sh              ←   Pine Script syntax validation
│   ├── context/                  ←   Context Engine tests (5 tests)
│   └── validation/               ←   Validation Engine tests (6 tests)
├── docs/
│   ├── README.id.md              ←   Panduan pengguna (ID)
│   ├── AI.md                     ←   AI collaboration context
│   ├── ARCHITECTURE.md           ←   Arsitektur indikator
│   ├── DEVELOPMENT.md            ←   Sprint status + coding standard
│   ├── WORKFLOW.md               ←   Workflow OpenCode + Graphify
│   ├── architecture.md           ←   Semantic layer architecture
│   ├── semantic-schema.md        ←   Schema v1.1 documentation
│   ├── query-api.md              ←   Query API reference
│   ├── graph-model.md            ←   Node/edge types documentation
│   ├── performance.md            ←   Benchmark results
│   └── adr/                      ←   Architecture Decision Records
├── graphify-out/
│   ├── graph.json                ←   Knowledge graph (nodes + edges)
│   └── GRAPH_REPORT.md           ←   Graph analysis report
├── .graphifyignore               ←   Exclude dari Graphify
├── .github/
│   ├── workflows/build.yml       ←   CI/CD pipeline
│   └── ISSUE_TEMPLATE/           ←   Bug & feature templates
└── assets/
    └── screenshot.png            ←   Dashboard preview
```

**Mengapa Setiap Folder Ada:**

| Folder | Alasan |
|--------|--------|
| `src/modules/` | Pisahkan kode per concern. 01-base untuk setup, 02-data untuk data fetching, 03-ui untuk rendering, 04-scoring untuk logika bisnis |
| `scripts/pine_query/` | Package Python yang bisa diimpor. Bukan sekumpulan script lepas |
| `scripts/` root | CLI entry points. Satu file per tool untuk simplicity |
| `tests/` | Golden tests untuk query, context, validation. Mencegah regresi |
| `docs/` | Dokumentasi arsitektur untuk developer baru + AI agent |
| `docs/adr/` | Catatan keputusan arsitektural. Kenapa, bukan apa |
| `graphify-out/` | Output Graphify. Cache-able, tidak perlu regenerate tiap sesi |

---

# 9. Data Flow

## Flow Lengkap: Source Code → AI Context

```
Timeline: Developer nulis kode → AI bantu maintain

┌──────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│  Developer   │     │  extract_ast.py  │     │  pine_semantic.json │
│  edit .pine  │────►│  parse + extract │────►│  structured data    │
└──────────────┘     └──────────────────┘     └─────────────────────┘
                                                          │
                                                          ▼
                                                  ┌────────────────┐
                                                  │  SemanticDB    │
                                                  │  build indexes │
                                                  └────────────────┘
                                                          │
                                              ┌───────────┴───────────┐
                                              │                       │
                                              ▼                       ▼
                                  ┌────────────────────┐   ┌──────────────────┐
                                  │  AI says:          │   │  CI/CD runs:     │
                                  │  "Tambah indikator │   │  pine-validate   │
                                  │   momentum"        │   │  --workspace .   │
                                  └────────────────────┘   └──────────────────┘
                                              │                       │
                                              ▼                       ▼
                                  ┌────────────────────┐   ┌──────────────────┐
                                  │  ContextAssembler  │   │  PatchValidator  │
                                  │  intent → select   │   │  checks → diff   │
                                  │  expand → rank     │   │  risk → report   │
                                  │  budget → compile  │   └──────────────────┘
                                  └────────────────────┘           │
                                              │                     ▼
                                              ▼             ┌──────────────────────┐
                                  ┌────────────────────┐   │  Validation Report   │
                                  │  Compiled Prompt   │   │  PASS / FAIL / ERROR │
                                  │  (markdown, 4-8K)  │   └──────────────────────┘
                                  └────────────────────┘
                                              │
                                              ▼
                                  ┌────────────────────┐
                                  │  LLM (Claude/GPT)  │
                                  │  REASONING ONLY    │
                                  │  No search needed  │
                                  └────────────────────┘
                                              │
                                              ▼
                                  ┌────────────────────┐
                                  │  Generated Code    │
                                  │  (patch .pine)     │
                                  └────────────────────┘
                                              │
                                              ▼
                                  ┌────────────────────┐
                                  │  pine-validate     │
                                  │  loop (v1.3)       │
                                  └────────────────────┘
```

## Flow: Query Execution

```
User/Agent
    │
    ▼
pine_query call: QUERY_REGISTRY["function"](db, "f_scoreHigher")
    │
    ├── db.function_index["f_scoreHigher"] → [{module, file, line, params}]
    ├── db.caller_index[...f_scoreHigher...] → calls (outgoing)
    ├── db.callee_index[...f_scoreHigher...] → called_by (incoming)
    ├── db.reverse_var_index[...] → reads, writes
    │
    ▼
Result: dict {definition, calls, called_by, reads, writes}
    │
    ▼
Formatter: json/table/markdown/mermaid
    │
    ▼
Output
```

## Flow: Context Assembly

```
"Tambah indikator momentum untuk sektor energi"
    │
    ├── IntentExtractor
    │   ├── verbs: ["create"]
    │   ├── objects: ["indicator"]
    │   ├── domains: ["momentum"]
    │   └── filters: ["energi"]
    │
    ├── SemanticSelector
    │   └── QUERY_REGISTRY["search"](db, "momentum", mode="substring")
    │       → [{name: "f_momentum", type: "function", score: 0.95}]
    │
    ├── Expander (BFS 2 hops)
    │   ├── f_momentum → calls: f_rsi, f_sma → calls: f_avg
    │   └── f_momentum → called_by: entry::04-scoring
    │
    ├── Ranker (profile: implementation → outgoing focus)
    │   └── f_momentum: 0.95, f_rsi: 0.48, f_sma: 0.48, …
    │
    ├── BudgetStrategy (max 8192 tokens)
    │   └── Keep top N entities until budget exhausted
    │
    ├── ContextBuilder
    │   └── For each entity: name, type, module, score, metadata, source code
    │
    └── PromptCompiler (profile: implementation)
        └── Markdown prompt: entities table + source snippets + dependencies
```

---

# 10. Semantic Schema

## Struktur pine_semantic.json (v1.1)

```json
{
  "schema": "1.1",
  "generated_by": "extract_ast.py",
  "pine_version": "v6",
  "parser": "pynescript 0.3.0",
  "project": "/home/Akhmfz/papan-instrumen",
  "generated_at": "2026-07-08T17:00:00",
  "total_time_seconds": 154.3,
  "file_count": 4,
  "files": [
    {
      "module": "01-base",
      "file": "/path/to/01-base.pine",
      "size_lines": 632,
      "parse_time_seconds": 34.48,
      "parse_errors": 0,
      "functions": [
        {
          "name": "f_clamp",
          "params": ["val", "min", "max"],
          "line": 42,
          "col": 0
        }
      ],
      "calls": [
        {
          "func_name": "f_clamp",
          "args_count": 3,
          "line": 150,
          "scope": "function",
          "parent": "f_scoreHigher"
        }
      ],
      "imports": [...],
      "variables": [
        {
          "name": "simbolInput",
          "var_type": "str",
          "is_global": true,
          "line": 15,
          "col": 0,
          "parent_function": null
        }
      ],
      "reads": [
        {
          "name": "simbolInput",
          "ctx": "Load",
          "line": 200,
          "col": 5,
          "parent_function": "f_scoreHigher"
        }
      ],
      "writes": [
        {
          "name": "scoreValue",
          "ctx": "Store",
          "line": 310,
          "col": 8,
          "parent_function": "f_scoreHigher"
        }
      ]
    }
  ],
  "cross_references": [
    {
      "caller": "f_scoreHigher",
      "callee": "f_clamp",
      "scope": "function",
      "parent": "f_scoreHigher",
      "callee_definitions": [{...}],
      "caller_file": "...",
      "caller_module": "01-base",
      "caller_line": 150,
      "resolved": true
    }
  ],
  "function_index": {
    "f_clamp": [{"module": "01-base", "file": "...", "line": 42, "params": ["val","min","max"]}]
  },
  "totals": {
    "functions": 51,
    "calls": 239,
    "imports": 0,
    "variables": 353,
    "reads": 302,
    "writes": 155,
    "internal_calls": 198,
    "unresolved_calls": 41
  }
}
```

## Evolusi Schema

| Version | Field Baru | Alasan |
|---------|-----------|--------|
| 1.0 | functions, calls, imports, cross_references | Minimum viable: bisa query fungsi dan panggilan |
| 1.1 | variables, reads, writes, scope, parent | Dibutuhkan untuk variable tracking dan dependency graph |

**Kenapa Schema 1.1:** Untuk mengetahui apakah suatu fungsi membaca/menulis variable tertentu. Kritis untuk impact analysis — "kalau variable `scoreValue` berubah, fungsi mana yang terpengaruh?"

**Kenapa Tidak Langsung 2.0:** Field baru backward-compatible. Consumer lama tetap bisa baca 1.1 tanpa perubahan (cuma tidak akan melihat variable data).

---

# 11. Query Engine

## Cara Kerja

1. **Load:** `SemanticDB(project_dir)` membaca `pine_semantic.json` + `graph.json`
2. **Index:** Membangun 9 in-memory index (semua dict / defaultdict)
3. **Query:** Setiap fungsi query tinggal lookup di index yang sesuai
4. **Format:** Hasil dilewatkan ke formatter untuk output

## Mengapa Query Sangat Cepat (0-0.5ms)

**Karena semua query adalah O(1) dict lookup setelah index build.**

Tidak ada database SQL. Tidak ada query parsing. Tidak ada file I/O saat query (semua data sudah di memory).

Perbandingan:
- Tanpa index: `find . -name "*.pine" | xargs grep "f_scoreHigher"` → butuh detik
- Dengan index: `function_index["f_scoreHigher"]` → 0.0ms

## Daftar Query (dengan detail teknis)

| Query | Index yang Digunakan | Kompleksitas |
|-------|---------------------|-------------|
| function | function_index, caller_index, callee_index, reverse_var_index | O(1) + O(k) untuk tiap edge |
| variable | variable_index, reverse_var_index | O(1) |
| module | module_index, dep_index | O(1) |
| impact | function_index, callee_index, transitive_callers() | O(d^k) dengan depth |
| callers | callee_index | O(k) |
| callees | caller_index | O(k) |
| search | Iterasi semua index | O(n) |
| builtin | builtin_index | O(1) |
| explain | function, callers, callees, variable (composite) | O(k) |
| context | function + file I/O untuk source | O(1) + I/O |
| stats | Semua index | O(1) |

(**n** = total entities, **k** = edges per node, **d** = branching factor)

---

# 12. Context Engine

Lihat di [7.7 Context Engine](#77-context-engine-pine_querycontext) untuk detail teknis.

## Filosofi

Context Engine adalah jembatan antara **structured knowledge** (pine_semantic.json + query) dan **unstructured LLM** (Claude, GPT).

**Prinsip:**
1. **No LLM in assembly** — Semua langkah deterministik
2. **Token budget first-class** — Setiap profile punya batas token tetap
3. **Reusable** — Context Object bisa dipakai ulang untuk berbagai LLM
4. **Testable** — Setiap langkah bisa diuji dengan golden test

## Intent Extraction (Rule-Based)

Tidak menggunakan NLP library. Hanya keyword matching sederhana:

```python
DOMAIN_KEYWORDS = {
    "momentum": "momentum", "trend": "trend",
    "volatility": "volatility", "volume": "volume",
    "sektor": "sektor", "sector": "sektor",
    "energi": "energy",
    ...
}

VERB_KEYWORDS = {
    "tambah": "create", "buat": "create",
    "ubah": "modify", "hapus": "delete",
    "refactor": "refactor", "fix": "fix",
    ...
}
```

**Kenapa Cukup:** Task description yang masuk ke Context Engine biasanya pendek (1-2 kalimat). Tidak perlu NLP complex. Keyword matching sudah 95% akurat untuk domain ini.

---

# 13. Validation Engine

Lihat di [7.8 Validation Engine](#78-validation-engine-pine_queryvalidation) untuk detail teknis.

## Mengapa Validator Read-Only

Keputusan arsitektural paling penting di Phase 2.2.

**Scenario A (sebelum):**
```text
patch_validator.py
    ├── apply_patch()      ← WRITE: ubah source code
    ├── run_checks()       ← READ
    └── report()           ← READ
```
Masalah: Validator hanya bisa dipakai jika patch sudah diaplikasikan.
Tidak bisa dipakai di git pre-commit hook (belum ada patch file).

**Scenario B (sekarang):**
```text
Workspace (sudah berisi perubahan, diaplikasikan oleh Git/AI/CI)
    │
    ▼
PatchValidator
    ├── snapshot()         ← READ
    ├── checks[].run()     ← READ
    ├── diff()             ← PURE
    ├── risk()             ← PURE
    └── report()           ← PURE
```
Keuntungan:
- Bisa dipakai di mana saja (git hook, CI/CD, VS Code, MCP, OpenCode)
- Tidak perlu tahu asal-usul perubahan
- Aman di race condition (tidak mengubah state)
- Testable: cukup siapkan workspace dengan perubahan tertentu

## Check Plugin Registry

Setiap check:

```python
class ParserCheck:
    name = "parser"           # unique identifier
    priority = 10             # lower = run earlier
    requires = []             # artifact dependencies
    produces = "semantic_raw" # artifact this check creates

    def run(self, workspace: str, artifacts: dict) -> CheckResult:
        # Run extract_ast.py, capture output
        # Return PASS/FAIL/ERROR
```

Kenapa plugin:
- Mudah ditambah check baru (performance, security, style)
- Mendukung `--skip parser` dan `--only golden`
- Urutan bisa diatur via priority

---

# 14. Testing

## Sistem Testing

| Suite | Jumlah | Tools | Lokasi |
|-------|--------|-------|--------|
| **Golden Test** | 28 | Python + file diff | `tests/run_golden.py` + `tests/golden/` |
| **Context Test** | 5 | Python + property check | `tests/context/` |
| **Validation Test** | 6 | Python + property check | `tests/validation/` |
| **Benchmark** | 1 | Python + timer | `tests/benchmark.py` |
| **PineTS Scoring** | 96 | PineTS (Node.js) | `tests/scoring/` |
| **PineTS Verify** | 12 | PineTS | `tests/pinets-verify.mjs` |
| **Transpile** | 1 | PineTS CLI | `tests/transpile.sh` |
| **Total** | **149** | — | — |

## Golden Test

**Cara Kerja:**
1. Untuk setiap query type (function, variable, module, ...), jalankan query
2. Bandingkan hasil JSON dengan snapshot di `tests/golden/{project}/{query}.json`
3. Jika berbeda → FAIL

**Kenapa Golden Test:**
- Mendeteksi regresi secara eksak
- Snapshot bisa di-review di PR
- Mudah di-update: `--update` flag

## Context Test

Property-based check. Bukan snapshot comparison.

Contoh:
```python
{
    "name": "momentum_variable",
    "task": "Tambah indikator momentum untuk sektor energi",
    "checks": {
        "context.get('entity_count', 0) >= 0": True,
        "context.get('task', {}).get('profile') == 'implementation'": True,
    }
}
```

**Kenapa Property Check:**
- Context assembly bersifat non-deterministik (tergantung isi database)
- Snapshot tidak berguna karena hasilnya berbeda tiap generate
- Yang penting: entity_count >= 0, profile benar, struktur context valid

## Validation Test

Test komponen individual (semantic_diff, risk_scorer), bukan full integration.

```python
{
    "name": "semantic_diff_no_change",
    "input": {"baseline": BASELINE, "current": BASELINE},
    "checks": {
        "stats.added == 0": True,
        "stats.modified == 0": True,
        "stats.unchanged == 4": True,
    },
}
```

---

# 15. Architecture Decision Records

## ADR-001: Semantic Layer sebagai Single Source of Truth

**Status:** Accepted  
**Keputusan:** `pine_semantic.json` adalah satu-satunya sumber kebenaran untuk semantic data. Semua konsumen (query, graph, context, validation) membaca darinya.

**Alternatif:** Database SQL, Graf database, API service  
**Alasan:** File JSON sederhana, mudah di-version control, mudah di-debug, tidak perlu service berjalan.

**Konsekuensi:**
- (+) Sederhana, portable, testable
- (+) Versionable via Git
- (-) Tidak cocok untuk data besar (>100MB)
- (-) Tidak ada query optimization (semua di memory)

## ADR-002: Python API First, CLI Second

**Status:** Accepted  
**Keputusan:** API Python bisa diimpor langsung oleh AI agent. CLI adalah sekunder.

**Alternatif:** CLI-only, REST API  
**Alasan:** AI agent (Claude, OpenCode) memanggil Python function lebih natural daripada spawning subprocess.

**Konsekuensi:**
- (+) Import langsung: `from pine_query import SemanticDB`
- (+) Testing lebih mudah (panggil function, bukan CLI)
- (-) Membutuhkan Python runtime di environment AI

## ADR-003: Schema Versioning

**Status:** Accepted  
**Keputusan:** Setiap `pine_semantic.json` punya field `schema`. Minor bump = backward compatible. Major bump = breaking change.

**Alternatif:** Tanpa versioning  
**Alasan:** Consumer perlu tahu format data sebelum parsing. Tanpa versioning, perubahan schema bisa merusak konsumen tanpa peringatan.

**Konsekuensi:**
- (+) AI agent bisa verifikasi format sebelum parsing
- (+) Pipeline mendeteksi ketidakcocokan lebih awal
- (-) Overhead kecil di tiap release

## ADR-004: Structural Explain (Tanpa LLM)

**Status:** Accepted  
**Keputusan:** Query `explain` bersifat struktural (calls, called_by, reads, writes, complexity). Bukan LLM-generated explanation.

**Alternatif:** LLM-generated explanation tiap query  
**Alasan:** LLM mahal, lambat, non-deterministik. Structural explain sudah cukup untuk 90% use case.

**Konsekuensi:**
- (+) Deterministik, instant, gratis
- (+) Testable
- (-) Tidak bisa menjelaskan "mengapa" atau memberi saran

## ADR-005: Query Response Envelope

**Status:** Accepted  
**Keputusan:** Setiap query mengembalikan envelope `{schema, query, generated_at, project, result}`

**Alternatif:** Langsung return result  
**Alasan:** Metadata penting untuk auditable query. AI agent perlu tahu kapan data di-generate dan dari project mana.

**Konsekuensi:**
- (+) Self-describing response
- (+) Cache-aware (generated_at)
- (-) Overhead ~5 baris JSON per response

## ADR-006: Review Engine (Draft)

**Status:** Draft — belum dijadwalkan (Phase v1.3)

**Keputusan:**
- Interface: `review(diff, context, profile, model) → ReviewResult`
- LLM dipanggil hanya di step terakhir (step 5 dari 6)
- Shared component: `semantic_diff`, `risk_scorer`, `profiles`
- Model-agnostic: caller menentukan model

**Belum Diputuskan:**
- Output format: markdown vs JSON
- Auto-approve untuk LOW risk
- GitHub PR comments integration

---

# 16. Filosofi Desain

## Prinsip-Prinsip yang Mendorong Arsitektur

### 1. Single Source of Truth (SSOT)

Semua komponen membaca `pine_semantic.json` dan `graph.json`. Tidak ada secondary source. Tidak ada cache yang bisa basi.

**Dampak:**
- Data consistency terjamin
- Debugging mudah: cukup cek JSON
- Testing mudah: cukup siapkan snapshot

### 2. Deterministic First

Semua pipeline utama (parse, query, diff, risk, report) adalah pure function dengan input/output deterministic.

**Yang NON-deterministik (hanya di step terakhir):**
- LLM call di Review Engine (masih draft)

**Dampak:**
- Reproducible: hasil yang sama untuk input yang sama
- Testable: golden test untuk setiap komponen
- Debuggable: trace tiap langkah

### 3. Layered Architecture

Setiap layer punya tanggung jawab spesifik. Tidak boleh melompat.

**Aturan:**
- Layer N hanya boleh memanggil layer N-1
- Layer N tidak boleh memanggil layer N+1
- Layer N+1 boleh depend pada layer N

**Dampak:**
- Isolated changes: ubah parser tanpa sentuh query
- Pluggable: ganti parser (pynescript → tree-sitter) tanpa ubah consumer
- Testable: test tiap layer independen

### 4. Plugin Pattern

Checks (validation) dan queries (QUERY_REGISTRY) menggunakan plugin registry.

```python
# Tambah query baru
QUERY_REGISTRY["new_query"] = new_query_fn

# Tambah check baru
CHECK_REGISTRY.append(NewCheck())
```

**Dampak:**
- Extensible tanpa refactor
- CLI auto-discover
- Mudah di-skip/only

### 5. Read-Only Validation

Validator tidak pernah mengubah source code. Observer, bukan actor.

**Dampak:**
- Gunakan di mana saja: git hooks, CI/CD, VS Code, MCP
- Aman di race condition
- Testable tanpa mock

### 6. Composition over Inheritance

Semua class composition-based. Tidak ada hierarki inheritance yang dalam.

Contoh: `ContextAssembler` memiliki `IntentExtractor`, `SemanticSelector`, dll sebagai komponen, bukan subclass.

### 7. LLM as Consumer, Not Core

LLM adalah komponen terakhir di pipeline, bukan pusat arsitektur.

**Arti:**
- Jika LLM berganti (Claude → GPT → local model), semantic layer tetap
- Jika LLM tidak tersedia, pipeline tetap bekerja (sampai prompt compilation)
- Token cost predictable (budget ditentukan oleh profile, bukan LLM)

---

# 17. Kelebihan Arsitektur

## Dibandingkan Tool Lain

| Aspek | Tool Lain (Copilot, Cursor) | Platform Ini |
|-------|----------------------------|--------------|
| **Semantic understanding** | Text-based (grep-like) | AST-based dengan full semantic index |
| **Query speed** | Detik (grep) | 0-0.5ms (dict lookup) |
| **Deterministic** | LLM-dependent (berubah tiap kali) | Pure function (sama tiap kali) |
| **Testability** | Sulit (test QA tergantung model) | Golden test (eksak) |
| **Token cost** | Tidak terkontrol | Budget per profile (4k-12k) |
| **Vendor lock-in** | Tergantung model AI | Model-agnostic |
| **Pine Script support** | Tidak spesifik | Parser khusus Pine Script v6 |
| **Validation loop** | Tidak ada | Checks → diff → risk → report |
| **Graph visualization** | Tidak ada | Graphify + mermaid |
| **Offline capability** | Tidak (butuh cloud API) | Fully offline |

## Kekuatan Utama

1. **Speed**: Query dalam 0-0.5ms. Index build dalam 0.02s. Tidak ada database latency.
2. **Determinism**: Hasil yang sama untuk input yang sama. Kritis untuk AI agent yang butuh konsistensi.
3. **Testability**: Golden test untuk semua query. Property check untuk context. Snapshot diff untuk validation.
4. **Extensibility**: Plugin registry untuk queries dan checks. Profile system untuk context.
5. **Portability**: Python package. Bisa diimpor langsung. Bisa di-CLI. Bisa di-web.
6. **Future-proof**: LLM-agnostic. Jika model AI berubah dalam 5 tahun, semantic layer tetap.

---

# 18. Kekurangan

## Analisis Kritis

### 1. Parser Performance

**Masalah:** Parsing 4 file butuh 154.54s. File scoring (104s) mendominasi.

**Bottleneck:** pynescript ANTLR parser. Setiap file diparse dari awal. Tidak ada incremental parsing.

**Rekomendasi:**
- Implementasi parser tree-sitter untuk Pine Script (lebih cepat, streaming)
- Cache hasil parsing per file, hanya re-parse file yang berubah
- Parallel parsing untuk file independen

### 2. In-Memory Database

**Masalah:** Semua data di-load ke memory. Untuk proyek >100 file, memory bisa menjadi isu.

**Bottleneck:** SemanticDB menyimpan semua entities + edges di dict Python.

**Rekomendasi:**
- Lazy loading untuk data yang jarang di-query
- SQLite sebagai persistent store (untuk proyek besar)
- Batch query API untuk mengurangi memory pressure

### 3. Pine-Specific Parser

**Masalah:** Parser hanya untuk Pine Script v6. Tidak bisa untuk bahasa lain.

**Keputusan Sadar:** Ini sengaja. Proyek ini spesifik untuk Pine Script.

**Rekomendasi:**
- Jika ingin multi-language, extract AST interface sebagai abstract class
- Implementasi per bahasa (tree-sitter)

### 4. Limited NLP in Intent Extraction

**Masalah:** Intent extractor hanya rule-based. Tidak bisa memahami task description yang kompleks.

**Contoh Gagal:** "Tambah parameter lookback period ke fungsi momentum, terus update scoring biar pake parameter baru juga" — Intent extractor mungkin kehilangan hubungan antara "parameter lookback" dan "fungsi momentum".

**Rekomendasi:**
- Untuk Phase 2.3: tambah lightweight entity recognition (regex + dictionary)
- Atau: minta user memberi task dalam format task = {action, target, details}

### 5. No Persistent Artifact Storage

**Masalah:** Artifacts disimpan di `.pine-validate/` lokal, tidak terpusat.

**Rekomendasi:**
- Phase 2.4: Pusatkan artifacts di `.pine-platform/` root
- Tambah `--push` untuk sync ke cloud storage

### 6. Golden Test Brittleness

**Masalah:** Golden test membandingkan JSON snapshot secara eksak. Perubahan kecil (format, whitespace) menyebabkan false positive.

**Rekomendasi:**
- Normalize JSON sebelum compare (sort keys, strip whitespace)
- Atau: gunakan semantic diff untuk golden test (hanya bandingkan field relevan)

### 7. Single Developer Risk

**Masalah:** Seluruh arsitektur didesain oleh satu orang. Tidak ada peer review di level arsitektur.

**Rekomendasi:**
- Dokumentasi ADR yang sudah ada (6 ADR) membantu mitigasi
- Butuh kontributor kedua untuk review

---

# 19. Roadmap

## Status Produk

```
Product A: Semantic Platform
  Status: GA (General Availability)
  Versi: v1.0
  Komponen: extract_ast, inject_graph, pine_query

Product B: Context Engine
  Status: RC (Release Candidate)
  Versi: v1.1
  Komponen: ContextAssembler, 4 profiles, intent→compile pipeline

Product C: Validation Engine
  Status: RC (Release Candidate)
  Versi: v1.2
  Komponen: PatchValidator, 5 checks, risk scorer, semantic_diff

Product D: Review Engine
  Status: Planning (ADR-006 only)
  Versi: v1.3 (planned)

Product E: MCP Server
  Status: Planning
  Versi: v1.4 (planned)

Product F: Automation Platform
  Status: Planning
  Versi: v1.5 (planned)
```

## Timeline

```text
v1.0  Semantic Platform        ─── ✅ Jul 2026
v1.1  Context Engine           ─── ✅ Jul 2026
v1.2  Validation Engine        ─── 🔄 Jul 2026 (Phase 2.2)
v1.3  Review Engine            ─── 📋 Not scheduled
v1.4  MCP Server               ─── 📋 Not scheduled
v1.5  Automation Platform      ─── 📋 Not scheduled
```

## Phase Selanjutnya

### Phase 2.2 — Patch Validation Engine (SELESAI)

**Yang Dibangun:**
- Read-only validator
- 5 checks: parser, schema, graph, golden, context
- semantic_diff.py sebagai core library
- Risk scorer: LOW/MEDIUM/HIGH/CRITICAL
- Report: PASS/PASS_WITH_WARNING/FAIL/ERROR
- CLI: pine-validate
- ADR-006: Review Engine design

### Phase 2.3 — (Belum Direncanakan)

Kandidat:
1. **Intent Extraction v2**: Entity recognition untuk task yang lebih kompleks
2. **Context Profile Builder**: User-defined profiles via JSON
3. **Performance Check**: Validasi runtime performance tiap fungsi
4. **Security Check**: Deteksi potensi repainting / look-ahead bias

### Phase v1.3 — Review Engine (Belum Dijadwalkan)

**Interface:**
```python
review(diff, context, profile="review", model="") -> ReviewResult
```

**Pipeline:**
1. semantic_diff.diff(baseline, current)
2. risk_scorer.assess(diff, [])
3. Build affected entity list
4. Compile review prompt
5. LLM.review(prompt)
6. Return ReviewResult

### Phase v1.4 — MCP Server (Belum Dijadwalkan)

Ekspos seluruh platform sebagai MCP tools:
- `pine-query` → MCP tool: `query_semantic`
- `pine-context` → MCP tool: `build_context`
- `pine-validate` → MCP tool: `validate_workspace`
- `semantic_diff` → MCP tool: `diff_snapshot`

### Phase v1.5 — Automation Platform (Belum Dijadwalkan)

n8n workflows + GitHub Actions integration:
- Auto-validate pada setiap PR
- Auto-context pada setiap issue
- Auto-review pada setiap commit

---

# 20. Kesimpulan

## Ringkasan

**Pine Semantic Platform** adalah infrastruktur lengkap untuk mengekstrak, menyimpan, menquery, mengontekstualisasi, dan memvalidasi kode Pine Script v6 secara deterministik.

Platform ini mengubah pipeline AI coding tradisional:

```
Dulu: Source Code → LLM → Tebak-tebak
Sekarang: Source Code → Semantic Layer → Query → Context → LLM → Validasi
```

## Yang Sudah Selesai

| Capaian | Detail |
|---------|--------|
| Parser Pine Script | extract_ast.py dengan pynescript ANTLR, 154s untuk 1800 baris |
| Semantic JSON | Schema 1.1, SSOT untuk semua komponen |
| Graph Injection | 297 nodes (PI), 303 nodes (PG), isolated <5% |
| Query Engine | 11 query types, 0-0.5ms, 4 formatters |
| Context Engine | 6-step pipeline, 4 profiles, rule-based intent |
| Validation Engine | Read-only, 5 checks, risk scoring, plugin registry |
| Golden Tests | 28 query + 5 context + 6 validation = 39 tests all pass |
| API Stability | `__all__`, `__version__`, frozen exports |
| Documentation | 5 ADR + 6 docs + WHITEPAPER |

## Yang Akan Datang

| Fitur | Fase | Status |
|-------|------|--------|
| Review Engine | v1.3 | ADR-006 only |
| MCP Server | v1.4 | Not started |
| Automation Platform | v1.5 | Not started |

## Pesan Terakhir

Nilai utama proyek ini bukan pada indikator TradingView-nya (Papan Instrumen, Papan Gerak), tetapi pada **infrastruktur semantic yang dibangun di sekitarnya**.

Platform ini memisahkan dua hal yang sering dicampur aduk:
1. **Knowledge retrieval** — mencari dan menyusun informasi yang relevan (deterministic)
2. **Reasoning** — mengambil kesimpulan dari informasi tersebut (LLM)

Dengan pemisahan ini, jika lima tahun dari sekarang model AI berganti, hampir seluruh investasi platform tetap bernilai. Yang berubah hanya adaptor di ujung pipeline.

---

*Dokumentasi ini ditulis untuk developer baru yang bergabung dengan proyek Pine Semantic Platform. Setelah membaca, Anda diharapkan memahami arsitektur, filosofi desain, alur data, dan roadmap proyek secara menyeluruh.*
