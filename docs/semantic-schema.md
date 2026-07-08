# Semantic Schema — pine_semantic.json v1.1

## File Structure

```json
{
  "schema": "1.1",
  "generated_by": "extract_ast.py",
  "pine_version": "v6",
  "parser": "pynescript 0.3.0",
  "project": "/path/to/project",
  "generated_at": "2026-07-08T17:00:00",
  "total_time_seconds": 154.3,
  "file_count": 4,
  "files": [ ... ],
  "cross_references": [ ... ],
  "function_index": { ... },
  "totals": { ... }
}
```

## Root Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `schema` | string | ✅ | Semantic schema version (currently "1.1") |
| `generated_by` | string | ✅ | Extractor script name |
| `parser` | string | ✅ | Parser name + version |
| `project` | string | ✅ | Absolute project path |
| `files` | array | ✅ | Per-file extraction results |
| `cross_references` | array | ✅ | Resolved/unresolved call references |
| `function_index` | object | ✅ | Function name → definition index |
| `totals` | object | ✅ | Aggregate statistics |

## File Object

| Field | Type | Description |
|---|---|---|
| `module` | string | Module name (e.g. "01-base") |
| `file` | string | Absolute file path |
| `size_lines` | int | File line count |
| `parse_time_seconds` | float | Parse duration |
| `parse_errors` | int | Error count (0 = clean) |
| `functions` | array | Function definitions |
| `calls` | array | Call expressions |
| `variables` | array | Variable assignments |
| `reads` | array | Variable reads (Name + Load) |
| `writes` | array | Variable writes (Name + Store) |

## Call Object Fields

| Field | Type | Description |
|---|---|---|
| `func_name` | string | Callee name |
| `line` | int | Source line |
| `scope` | string | "module" or "function" |
| `parent` | string | null (top-level) or function name |

## Variable Object Fields

| Field | Type | Description |
|---|---|---|
| `name` | string | Variable name |
| `is_global` | bool | True if declared with `var`/`varip` |
| `line` | int | Declaration line |

## Cross-Reference Object

| Field | Type | Description |
|---|---|---|
| `caller` | string | null (top-level) or function name |
| `callee` | string | Called function name |
| `scope` | string | "module" or "function" |
| `resolved` | bool | Whether callee has a definition in the project |

## Version History

| Version | Changes |
|---|---|
| 1.0 | Initial schema: functions, calls, imports, cross-references |
| 1.1 | Added: variables, reads, writes, scope/parent tracking |
