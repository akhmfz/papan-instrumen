# ADR-004: Explain Deterministik, LLM sebagai Extension

**Status:** Accepted  
**Date:** 2026-07-08  
**Tags:** explain, llm, deterministic

## Context

Query `explain` dan `context` dapat diimplementasikan dengan dua cara: (a) murni dari graph (deterministik), atau (b) dengan LLM (non-deterministik, biaya token, latency). Keduanya memiliki use case berbeda.

## Decision

**Sprint 8: `explain` dan `context` 100% deterministik.** Tidak ada dependency LLM. Semua data berasal dari `pine_semantic.json` + `graph.json`.

```bash
pine-query explain f_scoreTrend   # structural only: calls, called_by, reads, writes, complexity
pine-query context f_scoreTrend  # signature + source snippet + deps
```

LLM-powered explain (`explain --llm`) akan menjadi query terpisah di Sprint 9+ dengan nama berbeda (`explain-llm`).

## Consequences

- Positif: Deterministik = reprodusibel, testable, zero cost.
- Positif: Sprint 8 tidak memiliki dependency API key.
- Positif: CLI tetap responsif (<100ms).
- Negatif: Tidak bisa menjelaskan "business purpose" secara otomatis.
