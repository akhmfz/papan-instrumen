# ADR-001: Pine Semantic Layer sebagai Single Source of Truth

**Status:** Accepted  
**Date:** 2026-07-08  
**Tags:** architecture, semantic-layer, data-flow

## Context

Graphify menggunakan tree-sitter untuk parsing kode, tetapi Pine Script tidak memiliki grammar tree-sitter. Akibatnya, Graphify hanya mengekstrak struktur file/direktori dan dokumentasi Markdown — tidak ada fungsi, panggilan, atau variabel Pine. 78% node graph menjadi terisolasi.

Dua pendekatan mungkin:
1. Menulis grammar tree-sitter untuk Pine → permanen, tetapi lambat dan kompleks.
2. Membangun parser Pine terpisah, output disuntikkan ke Graphify.

## Decision

**`pine_semantic.json` adalah satu-satunya canonical representation dari struktur kode Pine.** Semua artefak lain (`graph.json`, laporan, visualisasi, context AI, query CLI, integrasi otomatis) harus diturunkan dari semantic layer ini dan tidak boleh menjadi sumber kebenaran tersendiri.

Pipeline: `extract_ast.py` (ANTLR/pynescript) → `pine_semantic.json` (schema 1.x) → `inject_graph.py` (Graphify consumer) + `pine_query.py` (query consumer).

## Consequences

- Positif: Parser tidak tahu Graphify; Graphify tidak tahu parser. Dependency satu arah.
- Positif: Jika Graphify berubah/berhenti, semantic layer tetap hidup.
- Positif: AI, n8n, MCP, Obsidian semuanya mengonsumsi `pine_semantic.json` — tidak perlu parsing ulang.
- Negatif: File ast-extract harus di-maintain terpisah dari Graphify.
