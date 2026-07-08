# Graph Report - .  (2026-07-08)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 293 nodes · 210 edges · 128 communities (11 shown, 117 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 1 edges (avg confidence: 0.65)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b8f5e180`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- 01-base.pine
- Papan Instrumen — Fundamental Dashboard
- runner.mjs
- f_stat(string id)
- package.json
- 7 Dimensi Scoring
- f_fin(string id)
- test-source-match.mjs
- lint.sh
- gh-sync.sh
- build.sh
- pinets-verify.mjs
- transpile.sh
- Dev Tools Installed
- Engine Comparison: PineTS, PineForge, PyneCore
- Error Cascade — Fix First Error First
- Golden Rule: No Features on Unverified Foundation
- PineTS Limitations
- PR Process & Commit Convention
- AI Golden Rules
- Coding Standard
- Release Checklist (P4-1)
- 5 Color Themes
- Bilingual (ID/EN)
- Compact Mode
- color: altBg
- color: bearTxt
- color: bullTxt
- color: cyanTxt
- f_avg3(float a, float b, float c)
- f_avg4(float a, float b, float c, float d)
- f_avg5(float a, float b, float c, float d, float e)
- f_avg6(float a, float b, float c, float d, float e, float f)
- f_avg7(a,b,c,d,e,f,g)
- f_categoryColor(string name, color fallback)
- f_clamp(float x, float lo, float hi)
- f_countValid4(a,b,c,d)
- f_countValid5(a,b,c,d,e)
- f_countValid6(a,b,c,d,e,f)
- f_countValid7(a,b,c,d,e,f,g)
- f_countValidArr(array<float> vals)
- f_riskBg(float s)
- f_riskColor(float s)
- f_rowBg(int row)
- f_safeDiv(float a, float b)
- f_scoreBg(float s)
- f_scoreCashFlow(float cf, float mcapVal)
- f_scoreColor(float s)
- f_scoreHigher(float v, float bad, float good)
- f_scoreLower(float v, float good, float bad)
- f_scoreLowerSafe(float v, float good, float bad)
- f_scoreMid(float v, float loVal, float ideal, float hiVal)
- f_scorePositive(float v)
- f_sectionBg(string title)
- f_wavg6(a,b,c,d,e,f,wa,wb,wc,wd,we,wf)
- f_wavg7(a,b,c,d,e,f,g,wa,wb,wc,wd,we,wf,wg)
- f_wavgArr(array<float> vals, array<float> wts)
- color: goldTxt
- color: gridCol
- const: grupBank
- const: grupBobot
- const: grupRisiko
- const: grupSektor
- const: grupUtama
- color: headerBg
- theme: isAmber
- theme: isDarkTheme
- theme: isEmerald
- theme: isLightTheme
- theme: isRoyal
- color: mainTxt
- color: mutedTxt
- color: neutralTxt
- pi_arrow(float v)
- pi_formatMoney(float v)
- pi_formatNumber(float v)
- pi_formatPercent(float v)
- pi_grade(float s)
- pi_overallBadge(float s)
- pi_riskGrade(float s)
- pi_scoreText(float score)
- color: purpleTxt
- color: sectionBg
- color: tableBg
- color: titleTxt
- watchlist: bankListIDX
- watchlist: coalListIDX
- watchlist: consumerListIDX
- watchlist: cpoListIDX
- f_ttm(string id)
- f_watchlist(array arr)
- watchlist: healthcareListIDX
- watchlist: industriListIDX
- watchlist: infraListIDX
- sector: isAsuransiSektor
- sector: isBankSektor
- sector: isBatubaraSektor
- sector: isCPOSektor
- sector: isFinancialGenericAuto
- sector: isFinancialLegacyMode
- sector: isFinancialSector
- sector: isIndustriSektor
- sector: isInfrastrukturSektor
- sector: isKesehatanSektor
- sector: isKonsumerSektor
- sector: isPropertySektor
- sector: isSekuritasSektor
- sector: isSiklikalLike
- sector: isSiklikalSektor
- sector: isTechnologySektor
- sector: isTransportasiSektor
- watchlist: propertyListIDX
- sector: sektorLabel
- watchlist: techListIDX
- watchlist: transportListIDX
- type MarketData
- f_boldCell(col, row, txt, bg, tc)
- f_cell(col, row, txt, bg, tc)
- f_headerCell(col, txt, bg, tc)
- f_riskCard(col, row, name, score)
- f_riskRow(col, row, name, value, score)
- f_row(col, row, name, value, score)
- f_scoreCard(col, row, name, score)
- f_scoreCardN(col, row, name, score, nValid, nTotal)
- f_section(col, row, title)
- f_warningCell(col, row, msg)

## God Nodes (most connected - your core abstractions)
1. `Papan Instrumen — Fundamental Dashboard` - 20 edges
2. `f_stat(string id)` - 20 edges
3. `7 Dimensi Scoring` - 12 edges
4. `f_fin(string id)` - 12 edges
5. `runTest()` - 11 edges
6. `lastVal()` - 10 edges
7. `assert()` - 10 edges
8. `summary()` - 10 edges
9. `scripts` - 7 edges
10. `lint.sh script` - 3 edges

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

## Communities (128 total, 117 thin omitted)

### Community 0 - "01-base.pine"
Cohesion: 0.04
Nodes (44): input: ambangARA, input: bahasa, input: barisSelangSeling, input: bobotGrowth, input: bobotHealth, input: bobotIncome, input: bobotIndonesia, input: bobotMomentum (+36 more)

### Community 1 - "Papan Instrumen — Fundamental Dashboard"
Cohesion: 0.09
Nodes (24): Active Backlog (P1-P4), input.float() Cannot Default to na, No Local Functions Inside if Blocks, Pine Script v6 Reserved Keywords, Development Setup Guide, AI Roles: PO, Architect, Developer, Reviewer, Context Loading Order, 7-Layer Architecture (+16 more)

### Community 2 - "runner.mjs"
Cohesion: 0.23
Nodes (13): assert(), dummyCandles(), lastVal(), runTest(), summary(), t, t, t (+5 more)

### Community 3 - "f_stat(string id)"
Cohesion: 0.10
Nodes (21): fin: bvps, fin: debtAsset, fin: debtEq, fin: ebitdaM, fin: epsGrowth, fin: epsTtm, fin: evEbitda, fin: evSales (+13 more)

### Community 4 - "package.json"
Cohesion: 0.13
Nodes (14): description, devDependencies, pinets, license, name, private, scripts, build (+6 more)

### Community 5 - "7 Dimensi Scoring"
Cohesion: 0.14
Nodes (14): Product Philosophy (6 Principles), 5 Pilar Analisis Fundamental, Scoring Principles, P0 Historical Bugs, Growth Dimension, Health Dimension (Financial), Income Dimension (Dividend), Indonesia Factor (7th Dimension) (+6 more)

### Community 6 - "f_fin(string id)"
Cohesion: 0.15
Nodes (13): fin: altmanZ, fin: cashDebt, fin: currRatio, fin: debtEbitda, fin: divYield, fin: dps, f_fin(string id), fin: fcf (+5 more)

### Community 7 - "test-source-match.mjs"
Cohesion: 0.22
Nodes (8): actualSource, allPassed, checks, hasConsumerWeights, hasFSafeLower, hasFSafeLowerSafe, hasSekuritasQuality, testFiles

### Community 8 - "lint.sh"
Cohesion: 0.83
Nodes (3): err(), ok(), lint.sh script

## Knowledge Gaps
- **230 isolated node(s):** `build.sh script`, `name`, `version`, `description`, `private` (+225 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **117 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Papan Instrumen — Fundamental Dashboard` connect `Papan Instrumen — Fundamental Dashboard` to `7 Dimensi Scoring`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Why does `7 Dimensi Scoring` connect `7 Dimensi Scoring` to `Papan Instrumen — Fundamental Dashboard`?**
  _High betweenness centrality (0.008) - this node is a cross-community bridge._
- **What connects `build.sh script`, `name`, `version` to the rest of the system?**
  _247 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `01-base.pine` be split into smaller, more focused modules?**
  _Cohesion score 0.044444444444444446 - nodes in this community are weakly interconnected._
- **Should `Papan Instrumen — Fundamental Dashboard` be split into smaller, more focused modules?**
  _Cohesion score 0.08695652173913043 - nodes in this community are weakly interconnected._
- **Should `f_stat(string id)` be split into smaller, more focused modules?**
  _Cohesion score 0.09523809523809523 - nodes in this community are weakly interconnected._
- **Should `package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._