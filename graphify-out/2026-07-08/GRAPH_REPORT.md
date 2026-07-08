# Graph Report - .  (2026-07-08)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 216 nodes · 251 edges · 16 communities (12 shown, 4 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 4 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3c92fce0`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- DEVELOPMENT.md — Panduan Pengembangan
- Panduan Pengguna — Papan Instrumen
- CATATAN PENGEMBANGAN — Lessons Learned
- runner.mjs
- Metodologi Scoring
- Saham: Papan Instrumen By. Akhmfz
- package.json
- Cara Berkontribusi
- Changelog
- AI.md — AI Collaboration Context
- test-source-match.mjs
- lint.sh
- gh-sync.sh
- build.sh
- pinets-verify.mjs
- transpile.sh

## God Nodes (most connected - your core abstractions)
1. `Panduan Pengguna — Papan Instrumen` - 14 edges
2. `Saham: Papan Instrumen By. Akhmfz` - 13 edges
3. `Changelog` - 12 edges
4. `runTest()` - 11 edges
5. `7 Dimensi Scoring` - 11 edges
6. `lastVal()` - 10 edges
7. `assert()` - 10 edges
8. `summary()` - 10 edges
9. `Cara Berkontribusi` - 10 edges
10. `CATATAN PENGEMBANGAN — Lessons Learned` - 9 edges

## Surprising Connections (you probably didn't know these)
- `AI Collaboration Guidelines` --references--> `7-Layer Architecture`  [EXTRACTED]
  docs/AI.md → docs/ARCHITECTURE.md
- `Panduan Pengguna — Papan Instrumen` --describes--> `7 Dimensi Scoring`  [EXTRACTED]
  docs/README.id.md → docs/ARCHITECTURE.md
- `Sector Classification` --documented_in--> `Sector Engine (15 classes)`  [INFERRED]
  docs/ARCHITECTURE.md → docs/DEVELOPMENT.md
- `7-Layer Architecture` --includes--> `Sector Engine (15 classes)`  [EXTRACTED]
  docs/ARCHITECTURE.md → docs/DEVELOPMENT.md

## Import Cycles
- None detected.

## Communities (16 total, 4 thin omitted)

### Community 0 - "DEVELOPMENT.md — Panduan Pengembangan"
Cohesion: 0.07
Nodes (29): 6-Level Testing, Anti-Patterns, Backlog, Bug Classification, Build 001, Build 002, Build 003, Build 004 (+21 more)

### Community 1 - "Panduan Pengguna — Papan Instrumen"
Cohesion: 0.07
Nodes (27): Cara Install (TradingView), Bobot Kustom, 1. Deteksi Sektor, 2. Faktor Indonesia, 3. Bobot Kustom, 4. Tema Warna, 5. Tampilan, 7 Dimensi Scoring (+19 more)

### Community 2 - "CATATAN PENGEMBANGAN — Lessons Learned"
Cohesion: 0.09
Nodes (22): 1. Reserved Keywords, 2. NO Local Functions Inside `if` Blocks, 3. Type Annotations pada Parameter, 4. Semicolons di `if` Blocks, 5. `input.float()` tidak bisa default `na`, 6. Error Cascade — fix error PERTAMA dulu, 7. Unicode characters + line breaks in ternary — fatal\n```pine\n// ❌ ERROR (CE10156) — ternary broken across lines + Unicode → in comment\nf_scoreCashFlow(float cf, float mcapVal) =>\n    na(cf) ? na :\n    f_scoreHigher(cf / mcapVal * 100, -2, 5)\n\n// ✅ CORRECT — single line + ASCII only\nf_scoreCashFlow(float cf, float mcapVal) =>\n    na(cf) or na(mcapVal) or mcapVal == 0 ? na : f_scoreHigher(cf / mcapVal * 100, -2, 5)\n```, 🐛 Bug yang Pernah Ada (Fase 0) (+14 more)

### Community 3 - "runner.mjs"
Cohesion: 0.14
Nodes (21): assert(), dummyCandles(), lastVal(), runTest(), summary(), t, t, t (+13 more)

### Community 4 - "Metodologi Scoring"
Cohesion: 0.18
Nodes (10): ARCHITECTURE.md — Arsitektur, Metodologi & Roadmap, Arsitektur Teknis, Executive Summary, Module Dependency (tidak boleh ada dependency terbalik), Problem Statement, Request Budget, Roadmap, Source Code Structure (urutan wajib) (+2 more)

### Community 5 - "Saham: Papan Instrumen By. Akhmfz"
Cohesion: 0.12
Nodes (16): Author, Customization, Development, Disclaimer, Fitur Unggulan, Known Limitations, License, Overview (+8 more)

### Community 6 - "package.json"
Cohesion: 0.13
Nodes (14): description, devDependencies, pinets, license, name, private, scripts, build (+6 more)

### Community 7 - "Cara Berkontribusi"
Cohesion: 0.14
Nodes (11): 1. Laporkan Bug, 2. Usulkan Fitur, 3. Pull Request, Cara Berkontribusi, Coding Standard, Contributing to Papan Instrumen, Development Setup, Keterbatasan (+3 more)

### Community 8 - "Changelog"
Cohesion: 0.14
Nodes (18): AI Collaboration Guidelines, Growth, Financial Health, Income (Dividend), Indonesia Factor, Momentum, Quality (Profitability), Request Budget (35 calls) (+10 more)

### Community 9 - "AI.md — AI Collaboration Context"
Cohesion: 0.20
Nodes (9): AI.md — AI Collaboration Context, AI Roles, Constraints, Context Loading Order (wajib dilakukan setiap AI sebelum bekerja), Delivery Requirements, Golden Rules, Product Philosophy, Project Identity (+1 more)

### Community 10 - "test-source-match.mjs"
Cohesion: 0.25
Nodes (8): Advanced, Automation (future), Benchmark, External Resources, New Discoveries (Build 011), PineTS Testing, Reference, Tools

### Community 11 - "lint.sh"
Cohesion: 0.83
Nodes (3): err(), ok(), lint.sh script

## Knowledge Gaps
- **148 isolated node(s):** `build.sh script`, `name`, `version`, `description`, `private` (+143 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Panduan Pengguna — Papan Instrumen` connect `Panduan Pengguna — Papan Instrumen` to `Changelog`, `Cara Berkontribusi`?**
  _High betweenness centrality (0.210) - this node is a cross-community bridge._
- **Why does `7 Dimensi Scoring` connect `Changelog` to `Panduan Pengguna — Papan Instrumen`?**
  _High betweenness centrality (0.182) - this node is a cross-community bridge._
- **Why does `Metodologi Scoring` connect `Changelog` to `Metodologi Scoring`?**
  _High betweenness centrality (0.180) - this node is a cross-community bridge._
- **What connects `build.sh script`, `name`, `version` to the rest of the system?**
  _148 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `DEVELOPMENT.md — Panduan Pengembangan` be split into smaller, more focused modules?**
  _Cohesion score 0.06666666666666667 - nodes in this community are weakly interconnected._
- **Should `Panduan Pengguna — Papan Instrumen` be split into smaller, more focused modules?**
  _Cohesion score 0.07407407407407407 - nodes in this community are weakly interconnected._
- **Should `CATATAN PENGEMBANGAN — Lessons Learned` be split into smaller, more focused modules?**
  _Cohesion score 0.08695652173913043 - nodes in this community are weakly interconnected._