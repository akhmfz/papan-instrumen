# Query API — pine_query v1.0

## Import

```python
from pine_query import SemanticDB, QUERY_REGISTRY, __version__
```

## SemanticDB

```python
db = SemanticDB("/path/to/project")
```

Loads `pine_semantic.json` + `graphify-out/graph.json`. Builds 9 in-memory indexes. Takes ~0.02s.

### Methods

| Method | Description |
|---|---|
| `refresh()` | Reload files if modified (checks mtime) |
| `resolve_caller_node(name, module)` | Resolve function name → Graphify node ID |
| `resolve_var_node(name)` | Resolve variable name → Graphify node ID |
| `collect_callees(node_id, relation)` | Outgoing edges from a node |
| `collect_callers(node_id, relation)` | Incoming edges to a node |
| `transitive_callers(node_id, depth)` | All upstream callers (up to depth) |

## QUERY_REGISTRY

`QUERY_REGISTRY` is a dict mapping query name → callable. Each callable has signature:

```python
fn(db: SemanticDB, name: str = None, **kwargs) -> dict
```

### Query Types

#### `function(name)`

Returns: definition, params, calls, called_by, reads, writes.

```python
QUERY_REGISTRY["function"](db, "f_scoreHigher")
```

#### `variable(name)`

Returns: declaration, read_by, written_by.

```python
QUERY_REGISTRY["variable"](db, "grupUtama")
```

#### `module(name)`

Returns: file info, functions, deps, entry callees.

```python
QUERY_REGISTRY["module"](db, "04-scoring")
```

#### `impact(name)`

Returns: direct callers, transitive callers, affected modules/tables/alerts.

```python
QUERY_REGISTRY["impact"](db, "f_scoreHigher")
```

#### `callers(name)`

Fast direct-caller lookup (no transitive).

```python
QUERY_REGISTRY["callers"](db, "f_scoreHigher")
```

#### `callees(name)`

Fast direct-callee lookup (no transitive).

```python
QUERY_REGISTRY["callees"](db, "f_scoreHigher")
```

#### `search(pattern, mode="substring")`

Three modes: `"substring"`, `"regex"`, `"exact"`.

```python
QUERY_REGISTRY["search"](db, "score", mode="regex")
```

#### `builtin(name)`

Lookup in 56-entry builtin catalog.

```python
QUERY_REGISTRY["builtin"](db, "ta.rsi")
```

#### `explain(name)`

Structural summary (no LLM). Calls, called_by, reads, writes, complexity score.

```python
QUERY_REGISTRY["explain"](db, "f_scoreHigher")
```

#### `context(name, compact=False)`

LLM-ready markdown: signature + source snippet (~12/30 lines) + deps.

```python
QUERY_REGISTRY["context"](db, "f_scoreHigher", compact=True)
```

#### `stats()`

Project-level KPI dashboard: nodes, edges, symbols, isolated %, builtins.

```python
QUERY_REGISTRY["stats"](db)
```

## Response Envelope

Every query returns a dict with `schema`, `query`, `generated_at`, `project`, `result` keys.

```json
{
  "schema": "query/1.0",
  "query": "function",
  "generated_at": "2026-07-08T17:00:00",
  "project": "papan-instrumen",
  "result": { ... }
}
```

## CLI

```bash
pine-query function f_scoreHigher --project /path --format json
pine-query search "score" --mode regex
pine-query context f_scoreHigher --compact --format markdown
pine-query stats
pine-query help
```
