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

| Component | File | Function |
|-----------|------|----------|
| Parser | `scripts/extract_ast.py` | Parse `.pine` via pynescript ANTLR → `pine_semantic.json` |
| Injector | `scripts/inject_graph.py` | Inject calls/reads/writes edges into Graphify `graph.json` |
| Query Engine | `scripts/pine_query.py` | Query functions, callers, callees, modules, search |
| Context Engine | `scripts/pine_context.py` | Assemble context for AI agent (review/impl/arch/bugfix profiles) |
| Validation | `scripts/pine_validate.py` | 5-category validation: parser, schema, graph, golden, context |
| Schema Validator | `scripts/validate_semantic.py` | Validate `pine_semantic.json` against schema v1.1 |

## Why This Architecture

- **Pine Script unsupported by tree-sitter** → Graphify cannot extract `calls`/`imports` edges
- **Inject2 Pipeline** bridges the gap: AST → semantic snapshot → enriched graph
- **Semantic Snapshot as SSOT** — `pine_semantic.json` committed as baseline (like `package-lock.json`)
- **Modular checks** — each stage independently verifiable

## Key Numbers (v1.1.0)

See `RELEASE-v1.1.md` in project root.
