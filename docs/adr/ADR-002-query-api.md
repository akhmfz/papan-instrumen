# ADR-002: Python API First, CLI Wrapper Second

**Status:** Accepted  
**Date:** 2026-07-08  
**Tags:** api, cli, architecture

## Context

Sprint 8 membangun Semantic Query Engine. Consumer potensial: manusia (terminal), AI agent (OpenCode, Claude Code), workflow (n8n), MCP server. CLI-only akan memaksa setiap consumer parsing output CLI.

## Decision

**Python API adalah primary interface; CLI hanyalah thin wrapper.** Struktur:

```python
from pine_query import SemanticDB, QUERY_REGISTRY

db = SemanticDB("/project")
result = QUERY_REGISTRY["function"](db, "f_scoreTrend")
```

CLI (`pine_query.py`) hanya argparse yang memanggil API yang sama:

```bash
pine-query function f_scoreTrend --format json
```

Query registry (`QUERY_REGISTRY`) memungkinkan plugin/extensi tanpa mengubah CLI.

## Consequences

- Positif: OpenCode, Claude Code, n8n bisa `import pine_query` langsung.
- Positif: Menambah query baru cukup register di `QUERY_REGISTRY`, CLI otomatis.
- Positif: Satu logika query, banyak consumer.
- Negatif: CLI sedikit lebih tebal (1 layer wrapper).
