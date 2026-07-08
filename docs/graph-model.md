# Graph Model — Node & Edge Types

## Node Types

| Type | ID Pattern | Example | Description |
|---|---|---|---|
| Module | `src_modules_{prefix}` | `src_modules_01base` | .pine module file |
| Function | `src_modules_{prefix}_{name}` | `src_modules_01base_f_scoreHigher` | Pine function |
| Variable (input) | `src_modules_01base_{name}` | `src_modules_01base_simbolInput` | User input |
| Variable (const) | `src_modules_01base_{name}` | `src_modules_01base_grupUtama` | String constant |
| Variable (color) | `src_modules_01base_{name}` | `src_modules_01base_tableBg` | Theme color |
| Variable (sector) | `src_modules_02data_{name}` | `src_modules_02data_isBankSektor` | Sector flag |
| Variable (watchlist) | `src_modules_02data_{name}` | `src_modules_02data_bankListIDX` | Ticker list |
| Variable (fin field) | `src_modules_02data_{name}` | `src_modules_02data_sharesOut` | Financial field |
| Variable (scoring) | `src_modules_04scoring_{name}` | `src_modules_04scoring_scoreValue` | Scoring variable |
| Module Entry | `module::{name}::entry` | `module::04-scoring::entry` | Synthetic entry for top-level code |
| Doc | `docs_*`, `readme_*`, `catatan_*` | `docs_ai_goldenrules` | Documentation node |

## Edge Types

| Relation | Direction | Description | Count (PI) |
|---|---|---|---|
| `calls` | Caller → Callee | Function call | 90 |
| `reads` | Caller → Variable | Variable read | 262 |
| `writes` | Caller → Variable | Variable write | 128 |
| `belongs_to` | Child → Parent | Ownership | 95 |
| `contains` | Module → Entry | Module contains entry | 4 |
| `depends_on` | Module → Module | Module dependency | 3 |
| `sourced_from` | Field → Function | Financial field source | 32 |

## Hierarchy

```
Module (src_modules_01base)
  └── contains → Entry (module::01-base::entry)
                   ├── calls → Function (src_modules_01base_f_scoreHigher)
                   ├── reads → Variable (src_modules_01base_grupUtama)
                   └── writes → Variable (...)

Function (src_modules_01base_f_scoreHigher)
  ├── belongs_to → Module (src_modules_01base)
  ├── calls → Function (src_modules_01base_f_clamp)
  ├── reads → Variable (...)
  └── writes → Variable (...)

Variable (src_modules_01base_simbolInput)
  ├── belongs_to → Module (src_modules_01base)
  ├── read_by → Function/Entry
  └── written_by → Function/Entry
```

## Isolated Nodes (v1.0 Baseline)

- **PI**: 13/297 (4.4%) — mostly documentation nodes + 1 type definition
- **PG**: 14/303 (4.6%) — mostly documentation nodes + 7 alert declarations
