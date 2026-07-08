# Graph Report - /home/Akhmfz/papan-instrumen  (2026-07-08)

## Corpus Check
- Corpus is ~16,337 words - fits in a single context window. You may not need a graph.

## Summary
- 109 nodes · 131 edges · 22 communities (6 shown, 16 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 1 edges (avg confidence: 0.65)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- AST Test Scaffolds
- 7 Dimensi Scoring
- Documentation & Changelog
- GitHub CI & Issues
- Pine Script Constraints
- Sector Classification & Coverage
- Architecture & Methodology
- AI Collaboration Framework
- Community 8
- Community 9
- Community 10
- Community 11
- Community 12
- Community 13
- Community 14
- Community 15
- Community 16
- Community 17
- Community 18
- Community 19
- Community 20
- Community 21

## God Nodes (most connected - your core abstractions)
1. `Papan Instrumen — Fundamental Dashboard` - 20 edges
2. `7 Dimensi Scoring` - 12 edges
3. `runTest()` - 11 edges
4. `lastVal()` - 10 edges
5. `assert()` - 10 edges
6. `summary()` - 10 edges
7. `scripts` - 7 edges
8. `lint.sh script` - 3 edges
9. `89 Automated Tests via PineTS` - 3 edges
10. `gh-sync.sh script` - 2 edges

## Surprising Connections (you probably didn't know these)
- `Papan Instrumen — Fundamental Dashboard` --references--> `Dashboard Screenshot Preview`  [EXTRACTED]
  README.md → assets/screenshot.png
- `No Local Functions Inside if Blocks` --rationale_for--> `Papan Instrumen — Fundamental Dashboard`  [EXTRACTED]
  CATATAN.md → README.md
- `Pine Script v6 Reserved Keywords` --conceptually_related_to--> `Papan Instrumen — Fundamental Dashboard`  [EXTRACTED]
  CATATAN.md → README.md
- `Development Setup Guide` --conceptually_related_to--> `Papan Instrumen — Fundamental Dashboard`  [EXTRACTED]
  CONTRIBUTING.md → README.md
- `AI Roles: PO, Architect, Developer, Reviewer` --conceptually_related_to--> `Papan Instrumen — Fundamental Dashboard`  [EXTRACTED]
  docs/AI.md → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **7 Dimensi Scoring** — docs_readme_id_value, docs_readme_id_quality, docs_readme_id_growth, docs_readme_id_health, docs_readme_id_income, docs_readme_id_momentum, docs_readme_id_indonesiafactor [EXTRACTED 1.00]
- **Documentation Files** — docs_architecture_7layerarchitecture, docs_architecture_scoringprinciples, docs_ai_airoles, docs_development_codingstandard, docs_development_changelog, catatan_reservedkeywords [INFERRED 0.85]
- **GitHub CI Pipeline** — github_workflows_build [EXTRACTED 1.00]

## Communities (22 total, 16 thin omitted)

### Community 0 - "AST Test Scaffolds"
Cohesion: 0.09
Nodes (24): Active Backlog (P1-P4), input.float() Cannot Default to na, No Local Functions Inside if Blocks, Pine Script v6 Reserved Keywords, Development Setup Guide, AI Roles: PO, Architect, Developer, Reviewer, Context Loading Order, 7-Layer Architecture (+16 more)

### Community 1 - "7 Dimensi Scoring"
Cohesion: 0.23
Nodes (13): assert(), dummyCandles(), lastVal(), runTest(), summary(), t, t, t (+5 more)

### Community 2 - "Documentation & Changelog"
Cohesion: 0.13
Nodes (14): description, devDependencies, pinets, license, name, private, scripts, build (+6 more)

### Community 3 - "GitHub CI & Issues"
Cohesion: 0.14
Nodes (14): Product Philosophy (6 Principles), 5 Pilar Analisis Fundamental, Scoring Principles, P0 Historical Bugs, Growth Dimension, Health Dimension (Financial), Income Dimension (Dividend), Indonesia Factor (7th Dimension) (+6 more)

### Community 4 - "Pine Script Constraints"
Cohesion: 0.22
Nodes (8): actualSource, allPassed, checks, hasConsumerWeights, hasFSafeLower, hasFSafeLowerSafe, hasSekuritasQuality, testFiles

### Community 5 - "Sector Classification & Coverage"
Cohesion: 0.83
Nodes (3): err(), ok(), lint.sh script

## Knowledge Gaps
- **53 isolated node(s):** `build.sh script`, `name`, `version`, `description`, `private` (+48 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Papan Instrumen — Fundamental Dashboard` connect `AST Test Scaffolds` to `GitHub CI & Issues`?**
  _High betweenness centrality (0.099) - this node is a cross-community bridge._
- **Why does `7 Dimensi Scoring` connect `GitHub CI & Issues` to `AST Test Scaffolds`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Why does `runTest()` connect `7 Dimensi Scoring` to `Pine Script Constraints`?**
  _High betweenness centrality (0.011) - this node is a cross-community bridge._
- **What connects `build.sh script`, `name`, `version` to the rest of the system?**
  _70 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `AST Test Scaffolds` be split into smaller, more focused modules?**
  _Cohesion score 0.08695652173913043 - nodes in this community are weakly interconnected._
- **Should `Documentation & Changelog` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._
- **Should `GitHub CI & Issues` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._