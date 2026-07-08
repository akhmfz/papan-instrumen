# Architecture Overview — Semantic Platform v1.1

```
Pine Script (.pine)
     │
     ▼
extract_ast.py (pynescript ANTLR parser)
     │
     ▼
pine_semantic.json (Semantic Snapshot — schema v1.1)
     │
     ▼
inject_graph.py (inject calls/reads/writes into graph.json)
     │
     ▼
graph.json (Graphify-out — enriched knowledge graph)
     │
     ┌─────┼──────────┐
     ▼     ▼          ▼
  Query   Context   Validation
  Engine  Engine    Engine
  (pine_query)  (pine_context)  (pine_validate)
     │
     ▼
 OpenCode / AI Agent
```

## Component Overview

| Component | Source | Function |
|-----------|--------|----------|
| Parser | `pine-semantic-platform` (`pine-extract`) | Parse `.pine` via pynescript ANTLR → `pine_semantic.json` |
| Injector | `pine-semantic-platform` (`pine-inject-graph`) | Inject calls/reads/writes edges into Graphify `graph.json` |
| Query Engine | `pine-semantic-platform` (`pine-query`) | Query functions, callers, callees, modules, search |
| Context Engine | `pine-semantic-platform` (`pine-context`) | Assemble context for AI agent (review/impl/arch/bugfix profiles) |
| Validation | `pine-semantic-platform` (`pine-validate`) | 5-category validation: parser, schema, graph, golden, context |
| Schema Validator | `pine-semantic-platform` (`pine-validate-semantic`) | Validate `pine_semantic.json` against schema v1.1 |

> **v2.0+**: All tools live in [`pine-semantic-platform`](https://github.com/akhmfz/pine-semantic-platform).
> Local `scripts/*.py` are thin wrappers. Install via `pip install -e /path/to/pine-semantic-platform` or `pip install pine-semantic-platform>=2.0,<3.0`.
> See `requirements.txt` at project root.

## Why This Architecture

- **Pine Script unsupported by tree-sitter** → Graphify cannot extract `calls`/`imports` edges
- **Inject2 Pipeline** bridges the gap: AST → semantic snapshot → enriched graph
- **Semantic Snapshot as SSOT** — `pine_semantic.json` committed as baseline (like `package-lock.json`)
- **Modular checks** — each stage independently verifiable

## Key Numbers (v1.1.0)

See `RELEASE-v1.1.md` in project root.
