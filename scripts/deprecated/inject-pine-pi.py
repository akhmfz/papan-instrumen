#!/usr/bin/env python3
"""Inject Pine Script symbols into Papan Instrumen graph.json"""

import json
from pathlib import Path

PROJECT = "/home/Akhmfz/papan-instrumen"
GRAPH_FILE = f"{PROJECT}/graphify-out/graph.json"
BASE = f"{PROJECT}/src/modules"

modules = {
    "01-base": f"{BASE}/01-base.pine",
    "02-data": f"{BASE}/02-data.pine",
    "03-ui": f"{BASE}/03-ui.pine",
    "04-scoring": f"{BASE}/04-scoring.pine",
}

# ============================================================
# NODES
# ============================================================
pine_nodes = []

# --- Module nodes ---
for mod, path in modules.items():
    pine_nodes.append({
        "id": f"src_modules_{mod.replace('-','')}",
        "label": f"{mod}.pine",
        "file_type": "code",
        "source_file": path,
    })

# --- Utility functions (01-base) ---
utils = [
    ("f_clamp", "f_clamp(float x, float lo, float hi)"),
    ("f_safeDiv", "f_safeDiv(float a, float b)"),
    ("f_scoreHigher", "f_scoreHigher(float v, float bad, float good)"),
    ("f_scoreLower", "f_scoreLower(float v, float good, float bad)"),
    ("f_scoreLowerSafe", "f_scoreLowerSafe(float v, float good, float bad)"),
    ("f_scoreMid", "f_scoreMid(float v, float loVal, float ideal, float hiVal)"),
    ("f_scorePositive", "f_scorePositive(float v)"),
    ("f_scoreCashFlow", "f_scoreCashFlow(float cf, float mcapVal)"),
    ("f_avg5", "f_avg5(float a, float b, float c, float d, float e)"),
    ("f_avg3", "f_avg3(float a, float b, float c)"),
    ("f_avg4", "f_avg4(float a, float b, float c, float d)"),
    ("f_avg6", "f_avg6(float a, float b, float c, float d, float e, float f)"),
    ("f_wavg6", "f_wavg6(a,b,c,d,e,f,wa,wb,wc,wd,we,wf)"),
    ("f_countValid5", "f_countValid5(a,b,c,d,e)"),
    ("f_countValid4", "f_countValid4(a,b,c,d)"),
    ("f_countValid6", "f_countValid6(a,b,c,d,e,f)"),
    ("f_avg7", "f_avg7(a,b,c,d,e,f,g)"),
    ("f_wavg7", "f_wavg7(a,b,c,d,e,f,g,wa,wb,wc,wd,we,wf,wg)"),
    ("f_countValid7", "f_countValid7(a,b,c,d,e,f,g)"),
    ("f_wavgArr", "f_wavgArr(array<float> vals, array<float> wts)"),
    ("f_countValidArr", "f_countValidArr(array<float> vals)"),
    ("pi_formatNumber", "pi_formatNumber(float v)"),
    ("pi_formatPercent", "pi_formatPercent(float v)"),
    ("pi_formatMoney", "pi_formatMoney(float v)"),
    ("pi_grade", "pi_grade(float s)"),
    ("pi_overallBadge", "pi_overallBadge(float s)"),
    ("pi_riskGrade", "pi_riskGrade(float s)"),
    ("pi_arrow", "pi_arrow(float v)"),
    ("pi_scoreText", "pi_scoreText(float score)"),
    ("f_rowBg", "f_rowBg(int row)"),
    ("f_scoreColor", "f_scoreColor(float s)"),
    ("f_riskColor", "f_riskColor(float s)"),
    ("f_scoreBg", "f_scoreBg(float s)"),
    ("f_riskBg", "f_riskBg(float s)"),
    ("f_sectionBg", "f_sectionBg(string title)"),
    ("f_categoryColor", "f_categoryColor(string name, color fallback)"),
]
for name, label in utils:
    pine_nodes.append({
        "id": f"src_modules_01base_{name}",
        "label": label,
        "file_type": "code",
        "source_file": modules["01-base"],
    })

# --- UI functions (03-ui) ---
ui_funcs = [
    ("f_cell", "f_cell(col, row, txt, bg, tc)"),
    ("f_boldCell", "f_boldCell(col, row, txt, bg, tc)"),
    ("f_headerCell", "f_headerCell(col, txt, bg, tc)"),
    ("f_section", "f_section(col, row, title)"),
    ("f_row", "f_row(col, row, name, value, score)"),
    ("f_riskRow", "f_riskRow(col, row, name, value, score)"),
    ("f_scoreCard", "f_scoreCard(col, row, name, score)"),
    ("f_scoreCardN", "f_scoreCardN(col, row, name, score, nValid, nTotal)"),
    ("f_warningCell", "f_warningCell(col, row, msg)"),
    ("f_riskCard", "f_riskCard(col, row, name, score)"),
]
for name, label in ui_funcs:
    pine_nodes.append({
        "id": f"src_modules_03ui_{name}",
        "label": label,
        "file_type": "code",
        "source_file": modules["03-ui"],
    })

# --- Data functions (02-data) ---
data_funcs = [
    ("type_MarketData", "type MarketData"),
    ("getMarketData", "getMarketData()"),
    ("f_fin", "f_fin(string id)"),
    ("f_stat", "f_stat(string id)"),
    ("f_ttm", "f_ttm(string id)"),
    ("f_watchlist", "f_watchlist(array arr)"),
]
for name, label in data_funcs:
    pine_nodes.append({
        "id": f"src_modules_02data_{name}",
        "label": label,
        "file_type": "code",
        "source_file": modules["02-data"],
    })

# --- Input variables (44) ---
inputs = [
    "simbolInput", "indeksAcuan", "periodeLaporan", "posisiInput",
    "ukuranTeksInput", "warnaTema", "tampilLatarSkor", "tampilBarSkor",
    "barisSelangSeling", "headerBerwarna", "tampilSimbolStatus",
    "tampilKelengkapan", "tampilCompact", "bahasa",
    "tampilRingkasan", "tampilValuasi", "tampilKualitas",
    "tampilPertumbuhan", "tampilKesehatan", "tampilDividen",
    "tampilMomentum", "tampilIndonesia",
    "modeSektor", "toleransiSiklikal",
    "gunakanBobotKustom", "presetBobot",
    "bobotValue", "bobotQuality", "bobotGrowth", "bobotHealth",
    "bobotMomentum", "bobotIncome", "bobotIndonesia",
    "tampilRisikoGorengan", "ambangARA", "lookbackARA",
    "kapKecilMiliar", "kapBesarMiliar", "likuiditasRendahJt",
    "likuiditasTinggiJt", "hargaRecehan",
    "carInput", "nplInput", "ldrInput",
]
for inp in inputs:
    pine_nodes.append({
        "id": f"src_modules_01base_{inp}",
        "label": f"input: {inp}",
        "file_type": "code",
        "source_file": modules["01-base"],
    })

# --- Financial fields (32) ---
fin_fields = [
    "sharesOut", "epsTtm", "bvps", "revenueTtm",
    "evEbitda", "evSales",
    "roe", "roa", "roic", "grossM", "opM", "netM", "ebitdaM",
    "fcfMargin", "piotroski",
    "revGrowth", "epsGrowth", "sgr",
    "debtEq", "debtAsset", "debtEbitda", "netDebtEbitda",
    "cashDebt", "currRatio", "quickRatio", "interestCover",
    "altmanZ", "ocf", "fcf",
    "divYield", "payout", "dps",
]
for fld in fin_fields:
    pine_nodes.append({
        "id": f"src_modules_02data_{fld}",
        "label": f"fin: {fld}",
        "file_type": "code",
        "source_file": modules["02-data"],
    })

# --- Sector flags ---
sector_flags = [
    "isFinancialLegacyMode", "isBankSektor", "isAsuransiSektor",
    "isSekuritasSektor", "isFinancialGenericAuto", "isFinancialSector",
    "isSiklikalSektor", "isPropertySektor", "isInfrastrukturSektor",
    "isTechnologySektor", "isTransportasiSektor", "isKonsumerSektor",
    "isIndustriSektor", "isKesehatanSektor", "isBatubaraSektor",
    "isCPOSektor", "sektorLabel", "isSiklikalLike",
]
for fl in sector_flags:
    pine_nodes.append({
        "id": f"src_modules_02data_{fl}",
        "label": f"sector: {fl}",
        "file_type": "code",
        "source_file": modules["02-data"],
    })

# --- Ticker watchlists ---
watchlists = [
    "bankListIDX", "coalListIDX", "cpoListIDX",
    "consumerListIDX", "industriListIDX", "healthcareListIDX",
    "propertyListIDX", "infraListIDX", "techListIDX", "transportListIDX",
]
for wl in watchlists:
    pine_nodes.append({
        "id": f"src_modules_02data_{wl}",
        "label": f"watchlist: {wl}",
        "file_type": "code",
        "source_file": modules["02-data"],
    })

# --- Theme color constants ---
theme_colors = [
    "tableBg", "altBg", "headerBg", "sectionBg", "gridCol",
    "mainTxt", "mutedTxt", "titleTxt",
    "bullTxt", "bearTxt", "purpleTxt", "goldTxt", "cyanTxt", "neutralTxt",
]
for tc in theme_colors:
    pine_nodes.append({
        "id": f"src_modules_01base_{tc}",
        "label": f"color: {tc}",
        "file_type": "code",
        "source_file": modules["01-base"],
    })

# --- Theme flags ---
theme_flags = ["isLightTheme", "isDarkTheme", "isEmerald", "isRoyal", "isAmber"]
for tf in theme_flags:
    pine_nodes.append({
        "id": f"src_modules_01base_{tf}",
        "label": f"theme: {tf}",
        "file_type": "code",
        "source_file": modules["01-base"],
    })

# --- String constants ---
str_consts = [
    "grupUtama", "grupSektor", "grupBobot", "grupRisiko", "grupBank",
]
for sc in str_consts:
    pine_nodes.append({
        "id": f"src_modules_01base_{sc}",
        "label": f"const: {sc}",
        "file_type": "code",
        "source_file": modules["01-base"],
    })

# ============================================================
# EDGES
# ============================================================
pine_edges = []

# Module dependency chain
mod_order = ["01base", "02data", "03ui", "04scoring"]
for i in range(len(mod_order) - 1):
    src = f"src_modules_{mod_order[i]}"
    tgt = f"src_modules_{mod_order[i+1]}"
    pine_edges.append({
        "source": src, "target": tgt,
        "relation": "depends_on",
        "confidence": "EXTRACTED", "confidence_score": 1.0,
        "source_file": modules[list(modules.keys())[i+1]],
    })

# Financial fields → f_stat
for fld in fin_fields[:20]:
    pine_edges.append({
        "source": f"src_modules_02data_{fld}",
        "target": "src_modules_02data_f_stat",
        "relation": "sourced_from",
        "confidence": "EXTRACTED", "confidence_score": 1.0,
        "source_file": modules["02-data"],
    })
for fld in fin_fields[20:]:
    pine_edges.append({
        "source": f"src_modules_02data_{fld}",
        "target": "src_modules_02data_f_fin",
        "relation": "sourced_from",
        "confidence": "EXTRACTED", "confidence_score": 1.0,
        "source_file": modules["02-data"],
    })

# Input → module
for inp in inputs:
    pine_edges.append({
        "source": f"src_modules_01base_{inp}",
        "target": "src_modules_01base",
        "relation": "belongs_to",
        "confidence": "EXTRACTED", "confidence_score": 1.0,
        "source_file": modules["01-base"],
    })

# ============================================================
# MERGE
# ============================================================
graph = json.loads(Path(GRAPH_FILE).read_text())

# graph.json uses NetworkX format: 'links' not 'edges'
existing_ids = {n["id"] for n in graph["nodes"]}
added_nodes = 0
for n in pine_nodes:
    if n["id"] not in existing_ids:
        graph["nodes"].append(n)
        existing_ids.add(n["id"])
        added_nodes += 1

existing_links = set()
for e in graph.get("links", []):
    existing_links.add((e["source"], e["target"], e.get("relation", "")))
added_edges = 0
for e in pine_edges:
    key = (e["source"], e["target"], e.get("relation", ""))
    if key not in existing_links:
        graph["links"].append(e)
        existing_links.add(key)
        added_edges += 1

Path(GRAPH_FILE).write_text(json.dumps(graph, indent=2))
print(f"PI inject: +{added_nodes} nodes, +{added_edges} edges")
print(f"Total: {len(graph['nodes'])} nodes, {len(graph['links'])} links")
