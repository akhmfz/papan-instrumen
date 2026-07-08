# Performance Baseline v1.0

Measured 2026-07-08 on:
- CPU: (Linux workstation)
- Python: 3.x via `/tmp/ps-test` venv
- pynescript: 0.3.0
- Graphify: (installed via pip)

## Project: Papan Instrumen (4 modules, 51 functions, 353 variables)

| Operation | Measured | Target | Status |
|---|---|---|---|
| Parse (total) | 154.54s | <300s | ✅ |
|  01-base | 34.48s | — | — |
|  02-data | 14.06s | — | — |
|  03-ui | 1.21s | — | — |
|  04-scoring | 104.79s | — | — |
| DB load + index | 0.027s | <0.5s | ✅ |
| Query: function | 0.0ms | <5ms | ✅ |
| Query: variable | 0.0ms | <5ms | ✅ |
| Query: module | 0.3ms | <5ms | ✅ |
| Query: impact | 0.0ms | <5ms | ✅ |
| Query: callers | 0.0ms | <5ms | ✅ |
| Query: callees | 0.0ms | <5ms | ✅ |
| Query: search | 0.2ms | <5ms | ✅ |
| Query: builtin | 0.1ms | <5ms | ✅ |
| Query: explain | 0.0ms | <5ms | ✅ |
| Query: context | 0.1ms | <30ms | ✅ |
| Query: stats | 0.5ms | <5ms | ✅ |

## Project: Papan Gerak (5 modules, 20 functions, 305 variables)

| Operation | Measured | Target | Status |
|---|---|---|---|
| Parse (total) | 136.59s | <300s | ✅ |
| DB load + index | 0.014s | <0.5s | ✅ |
| All queries | 0.0-0.4ms | <5ms | ✅ |

## Notes

- Parse time dominated by `04-scoring.pine` / `03-scoring.pine` (~100s each) due to large number of expressions.
- DB load is purely I/O + dict construction; scales linearly with file size.
- All queries are O(1) dict lookups after index build — essentially instant.
- Context query includes file I/O for source snippet; dominated by read, not assembly.
- These benchmarks should be re-run after any parser, schema, or query engine changes.
