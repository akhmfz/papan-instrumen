# ADR-005: Query Response Envelope

**Status:** Accepted  
**Date:** 2026-07-08  
**Tags:** api, response, mcp, integration

## Context

Response query API perlu dikonsumsi oleh berbagai sistem (MCP, REST, n8n, cache). Raw result object tanpa metadata menyebabkan ambiguity tentang asal data.

## Decision

Setiap response query dibungkus dalam envelope standar:

```json
{
  "schema": "query/1.0",
  "query": "function",
  "generated_at": "2026-07-08T17:00:00",
  "project": "papan-instrumen",
  "result": { ... }
}
```

- `schema`: versi format response (independen dari semantic schema).
- `query`: nama query yang dijalankan.
- `generated_at`: timestamp ISO8601.
- `project`: nama project (directory name).
- `result`: payload spesifik-query.

CLI flag `--raw` menghilangkan envelope untuk pipeline Unix.

## Consequences

- Positif: MCP, cache, dan n8n bisa identifikasi response tanpa inspeksi isi.
- Positif: Backward compat — field baru bisa ditambahkan ke envelope tanpa mengubah `result`.
- Negatif: Overhead ~100 bytes per response.
