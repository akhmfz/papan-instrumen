# ADR-003: Schema Versioning untuk pine_semantic.json

**Status:** Accepted  
**Date:** 2026-07-08  
**Tags:** schema, versioning, backward-compat

## Context

`pine_semantic.json` adalah artefak kritis yang dikonsumsi oleh injector, query engine, dan nanti MCP/AI. Tanpa versioning, perubahan format dapat merusak consumer secara diam-diam.

## Decision

Setiap file `pine_semantic.json` memiliki field `schema` di root:

```json
{
  "schema": "1.1",
  "generated_by": "extract_ast.py",
  "pine_version": "v6",
  "parser": "pynescript 0.3.0"
}
```

Kebijakan versi:
- **Minor bump** (1.0 → 1.1): field baru ditambahkan, field lama tetap kompatibel.
- **Major bump** (1.x → 2.0): breaking change — injector/query engine harus update.
- Consumer membaca `schema` saat startup dan memberi peringatan jika versi tidak dikenal.

## Consequences

- Positif: AI agent dapat memverifikasi format sebelum parsing.
- Positif: Pipeline mendeteksi ketidakcocokan lebih awal ("Schema 1.1 > 1.0").
- Negatif: Overhead kecil pada setiap release extractor.
