# Review Summary

**Risk**: CRITICAL
**Score**: 1.0

## Reasons
- check_failed:parser
- check_failed:schema
- check_failed:graph

## Files Changed
- `scripts/extract_ast.py`
- `scripts/inject_graph.py`
- `scripts/pine_context.py`
- `scripts/pine_query.py`
- `scripts/pine_validate.py`
- `scripts/validate_semantic.py`
- `scripts/vault-fix.py`

## Transitive Impact
- 0 direct changes
- 0 transitive callers
- 0 total affected functions
- 0 tables
- 0 alerts

## Validation Warnings
- ⚠ parser: extract_ast.py exited with non-zero code
- ⚠ schema: Schema validation failed
- ⚠ graph: inject_graph.py exited with non-zero code

## AI Review Context

# Context: Code Task

**Profile:** implementation  |  **Budget:** 8192 tokens  |  **Entities:** 9  |  **Modules:** 2

## Selected Entities

| Entity | Type | Module | Score | Reason |
|---|---|---|---|---|
| f_riskBg | function | 01-base | 0.8 | direct match |
| f_riskColor | function | 01-base | 0.8 | direct match |
| f_riskRow | function | 03-ui | 0.8 | direct match |
| f_riskCard | function | 03-ui | 0.8 | direct match |
| pi_riskGrade | function | 01-base | 0.8 | direct match |
| rowBg | function | 03-ui | 0.48 | callee of f_riskCard (1 hop) |
| cell | function | 03-ui | 0.48 | callee of f_riskCard (1 hop) |
| scoreText | function | 03-ui | 0.48 | callee of f_riskCard (1 hop) |
| module::04-scoring::entry | function | 03-ui | 0.4 | caller of f_riskCard (1 hop) |


## Source Code

### f_riskBg (01-base)
```pine
f_riskBg(float s) =>
    not tampilLatarSkor ? tableBg :
     na(s) ? tableBg :
     color.new(f_riskColor(s), isLightTheme ? 86 : 84)
```

### f_riskColor (01-base)
```pine
f_riskColor(float s) =>
    na(s) ? neutralTxt :
     s >= 70 ? bullTxt :
     s >= 40 ? goldTxt :
```

### f_riskRow (03-ui)
```pine
f_riskRow(int col, int row, string name, string value, float score) =>
    bg = f_rowBg(row)
    scoreBg = tampilLatarSkor ? f_riskBg(score) : bg
    scoreTxt = pi_scoreText(score)
```

### f_riskCard (03-ui)
```pine
f_riskCard(int col, int row, string name, float score) =>
    bg = tampilLatarSkor ? f_riskBg(score) : f_rowBg(row)
    tc = f_riskColor(score)
    f_cell(col, row, name, bg, mainTxt)
```

### pi_riskGrade (01-base)
```pine
pi_riskGrade(float s) =>
    isEN = bahasa == "English"
    na(s) ? "N/A" :
     s >= 70 ? (isEN ? "LOW RISK" : "RISIKO RENDAH") :
```

## Dependencies

- f_riskBg → 1 callees
- f_riskBg ← 2 callers
- f_riskBg reads 4 variables
- f_riskColor ← 3 callers
- f_riskColor reads 4 variables
- f_riskRow → 5 callees
- f_riskRow ← 1 callers
- f_riskRow reads 8 variables
- f_riskCard → 6 callees
- f_riskCard ← 1 callers
- f_riskCard reads 8 variables
- pi_riskGrade ← 1 callers
- pi_riskGrade reads 1 variables

## Module Overview

| Module | Functions | Lines | Depends On | Entry Calls |
|---|---|---|---|---|
| 01-base | 36 | 632 |  | 0 |
| 03-ui | 10 | 83 | 01-base, 02-data | 0 |

