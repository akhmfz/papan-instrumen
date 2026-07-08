#!/usr/bin/env python3
"""Stage 2: Inject AST-extracted edges into graph.json

Reads pine_semantic.json (schema >= 1.1) and injects:
- Module entry nodes for top-level code
- calls edges (function→function and entry→function)
- Module → contains → Entry
- Function → belongs_to → Module
- Caller → reads → Variable  (for variables with existing graph nodes)
- Caller → writes → Variable (for variables with existing graph nodes)

All edges deduplicated: one edge per (source, target, relation) with count metadata.
"""

import json
from pathlib import Path
from collections import defaultdict

SCHEMA_VERSION = "1.1"


def module_to_prefix(module_name: str) -> str:
    return module_name.replace("-", "")


def build_node_id(module_name: str, symbol: str) -> str:
    return f"src_modules_{module_to_prefix(module_name)}_{symbol}"


def module_id(module_name: str) -> str:
    return f"src_modules_{module_to_prefix(module_name)}"


def entry_node_id(module_name: str) -> str:
    return f"module::{module_name}::entry"


def build_function_label(fn: dict) -> str:
    params = ", ".join(fn.get("params", []))
    return f"{fn['name']}({params})"


def process_project(sem_file: Path, graph_file: Path) -> dict:
    sem = json.loads(sem_file.read_text())

    # Schema check
    schema = sem.get("schema", "0.0")
    print(f"  Schema: {schema}")
    if schema < SCHEMA_VERSION:
        print(f"  ⚠️  Schema {schema} < {SCHEMA_VERSION}, update extract_ast.py first")
    elif schema > SCHEMA_VERSION:
        print(f"  ⚠️  Schema {schema} > {SCHEMA_VERSION}, update inject_graph.py first")

    graph = json.loads(graph_file.read_text())

    existing_ids = {n["id"] for n in graph["nodes"]}
    existing_links = set()
    for e in graph.get("links", []):
        existing_links.add((e["source"], e["target"], e.get("relation", "")))

    added_nodes = 0
    added_edges = 0

    # ---------------------------------------------------------------
    # 1. Build function index + create missing function nodes
    # ---------------------------------------------------------------
    fn_index = {}  # (module, name) → node_id
    for fi in sem["files"]:
        module = fi["module"]
        src_file = fi["file"]
        for fn in fi["functions"]:
            name = fn["name"]
            node_id = build_node_id(module, name)
            fn_index[(module, name)] = node_id
            if node_id not in existing_ids:
                graph["nodes"].append({
                    "id": node_id,
                    "label": build_function_label(fn),
                    "file_type": "code",
                    "source_file": src_file,
                })
                existing_ids.add(node_id)
                added_nodes += 1

    # Cross-module name lookup
    name_to_ids = {}
    for (mod, name), nid in fn_index.items():
        name_to_ids.setdefault(name, []).append((mod, nid))

    # ---------------------------------------------------------------
    # 2a. Build variable name → [ (module, node_id) ] index
    # ---------------------------------------------------------------
    var_name_to_nodes = defaultdict(list)
    for fi in sem["files"]:
        mod = fi["module"]
        for v in fi.get("variables", []):
            nid = build_node_id(mod, v["name"])
            if nid in existing_ids:
                var_name_to_nodes[v["name"]].append((mod, nid))

    # Also scan all existing graph nodes for ones starting with src_modules_{prefix}_
    for n in graph["nodes"]:
        nid = n["id"]
        if nid.startswith("src_modules_"):
            rest = nid[len("src_modules_"):]
            underscore_pos = rest.find("_")
            if underscore_pos > 0:
                mod_prefix = rest[:underscore_pos]
                name = rest[underscore_pos + 1:]
                for fi in sem["files"]:
                    if module_to_prefix(fi["module"]) == mod_prefix:
                        var_name_to_nodes[name].append((fi["module"], nid))
                        break

    for name in list(var_name_to_nodes.keys()):
        seen = set()
        var_name_to_nodes[name] = [
            x for x in var_name_to_nodes[name] if x[1] not in seen and not seen.add(x[1])
        ]

    # ---------------------------------------------------------------
    # 2b. Detect modules with top-level code → create entry nodes
    # ---------------------------------------------------------------
    modules_with_top_level = set()
    for xref in sem["cross_references"]:
        if xref.get("scope") == "module" and xref.get("resolved"):
            modules_with_top_level.add(xref["caller_module"])
    # Also detect from top-level variable reads/writes
    for fi in sem["files"]:
        mod = fi["module"]
        if mod in modules_with_top_level:
            continue
        for ref_list_name, ref_list in [("reads", fi.get("reads", [])),
                                          ("writes", fi.get("writes", []))]:
            for ref in ref_list:
                if ref.get("parent_function") is None:
                    if var_name_to_nodes.get(ref["name"]):
                        modules_with_top_level.add(mod)
                        break
            if mod in modules_with_top_level:
                break

    for mod in sorted(modules_with_top_level):
        entry_id = entry_node_id(mod)
        if entry_id not in existing_ids:
            graph["nodes"].append({
                "id": entry_id,
                "type": "module_entry",
                "module": mod,
                "label": f"entry::{mod}",
                "file_type": "code",
            })
            existing_ids.add(entry_id)
            added_nodes += 1

        # Edge: Module → contains → Entry
        mid = module_id(mod)
        key = (mid, entry_id, "contains")
        if mid in existing_ids and entry_id in existing_ids and key not in existing_links:
            graph["links"].append({
                "source": mid,
                "target": entry_id,
                "relation": "contains",
                "confidence": "EXTRACTED",
                "confidence_score": 1.0,
            })
            existing_links.add(key)
            added_edges += 1

    # ---------------------------------------------------------------
    # 3. Inject calls edges (function→function + entry→function)
    #    Deduplicate by (caller, callee) with count metadata
    # ---------------------------------------------------------------
    # Collect all candidate edges first
    edge_candidates = defaultdict(lambda: {
        "count": 0, "first_line": None, "first_col": None, "source_file": None,
    })

    for xref in sem["cross_references"]:
        if not xref["resolved"]:
            continue

        callee_name = xref["callee"]
        caller_mod = xref["caller_module"]
        scope = xref.get("scope", "function")
        caller_name = xref.get("caller")
        caller_line = xref["caller_line"]
        caller_col = xref["caller_col"]

        # Determine caller node ID
        if scope == "module":
            caller_id = entry_node_id(caller_mod)
        elif caller_name is not None:
            caller_key = (caller_mod, caller_name)
            caller_id = fn_index.get(caller_key)
            if caller_id is None:
                candidates = name_to_ids.get(caller_name, [])
                if len(candidates) == 1:
                    caller_id = candidates[0][1]
                elif len(candidates) > 1:
                    for cm, cid in candidates:
                        if cm == caller_mod:
                            caller_id = cid
                            break
                    if caller_id is None:
                        caller_id = candidates[0][1]
                else:
                    continue
        else:
            continue  # unknown scope without caller name

        # Resolve callee node ID
        callee_id = None
        for cd in xref.get("callee_definitions", []):
            cmod = cd.get("module", "")
            ckey = (cmod, callee_name)
            cid = fn_index.get(ckey)
            if cid:
                callee_id = cid
                break
            candidates = name_to_ids.get(callee_name, [])
            for cm, cid2 in candidates:
                if cm == cmod:
                    callee_id = cid2
                    break
            if callee_id:
                break

        if callee_id is None:
            candidates = name_to_ids.get(callee_name, [])
            if len(candidates) == 1:
                callee_id = candidates[0][1]
            elif len(candidates) > 1:
                for cm, cid2 in candidates:
                    if cm == caller_mod:
                        callee_id = cid2
                        break
                if callee_id is None:
                    callee_id = candidates[0][1]

        if callee_id is None or caller_id is None:
            continue
        if caller_id == callee_id:
            continue

        edge_key = (caller_id, callee_id)
        ec = edge_candidates[edge_key]
        ec["count"] += 1
        if ec["first_line"] is None:
            ec["first_line"] = caller_line
            ec["first_col"] = caller_col
            ec["source_file"] = xref["caller_file"]

    # Inject deduplicated edges
    for (caller_id, callee_id), meta in sorted(edge_candidates.items()):
        key = (caller_id, callee_id, "calls")
        if key not in existing_links:
            graph["links"].append({
                "source": caller_id,
                "target": callee_id,
                "relation": "calls",
                "confidence": "EXTRACTED",
                "confidence_score": 1.0,
                "count": meta["count"],
                "first_line": meta["first_line"],
                "first_col": meta["first_col"],
                "source_file": meta["source_file"],
            })
            existing_links.add(key)
            added_edges += 1

    # ---------------------------------------------------------------
    # 4. Variable reads/writes edges
    #    Match variable names to existing graph nodes (any module)
    # ---------------------------------------------------------------
    # (var_name_to_nodes already built in section 2a)

    # Collect var edges
    var_edge_candidates = defaultdict(lambda: {
        "count": 0, "first_line": None, "first_col": None,
    })

    for fi in sem["files"]:
        module = fi["module"]
        for ref_list, relation in [(fi.get("reads", []), "reads"),
                                     (fi.get("writes", []), "writes")]:
            for ref in ref_list:
                ref_name = ref["name"]
                # Resolve to existing graph node
                candidates = var_name_to_nodes.get(ref_name, [])
                if not candidates:
                    continue
                # Use first candidate (prefer same module)
                callee_id = None
                for cm, cid in candidates:
                    if cm == module:
                        callee_id = cid
                        break
                if callee_id is None:
                    callee_id = candidates[0][1]

                # Determine caller
                parent_fn = ref.get("parent_function")
                if parent_fn:
                    caller_key = (module, parent_fn)
                    caller_id = fn_index.get(caller_key)
                    if caller_id is None:
                        candidates_call = name_to_ids.get(parent_fn, [])
                        for cm, cid in candidates_call:
                            if cm == module:
                                caller_id = cid
                                break
                        if caller_id is None and candidates_call:
                            caller_id = candidates_call[0][1]
                    if caller_id is None:
                        continue
                else:
                    # Top-level read/write → use entry node
                    caller_id = entry_node_id(module)
                    if caller_id not in existing_ids:
                        continue

                if caller_id == callee_id:
                    continue

                edge_key = (caller_id, callee_id, relation)
                ec = var_edge_candidates[edge_key]
                ec["count"] += 1
                if ec["first_line"] is None:
                    ec["first_line"] = ref.get("line", 0)
                    ec["first_col"] = ref.get("col", 0)

    # Inject var edges
    for (caller_id, callee_id, relation), meta in sorted(var_edge_candidates.items()):
        key = (caller_id, callee_id, relation)
        if key not in existing_links:
            graph["links"].append({
                "source": caller_id,
                "target": callee_id,
                "relation": relation,
                "confidence": "EXTRACTED",
                "confidence_score": 1.0,
                "count": meta["count"],
                "first_line": meta["first_line"],
                "first_col": meta["first_col"],
            })
            existing_links.add(key)
            added_edges += 1

    # ---------------------------------------------------------------
    # 5. belongs_to edges for function→module
    # ---------------------------------------------------------------
    for fi in sem["files"]:
        module = fi["module"]
        mid = module_id(module)
        for fn in fi["functions"]:
            name = fn["name"]
            fn_id = build_node_id(module, name)
            key = (fn_id, mid, "belongs_to")
            if fn_id in existing_ids and mid in existing_ids and key not in existing_links:
                graph["links"].append({
                    "source": fn_id,
                    "target": mid,
                    "relation": "belongs_to",
                    "confidence": "EXTRACTED",
                    "confidence_score": 1.0,
                    "source_file": fi["file"],
                })
                existing_links.add(key)
                added_edges += 1

    # ---------------------------------------------------------------
    # 5. Write
    # ---------------------------------------------------------------
    graph_file.write_text(json.dumps(graph, indent=2))

    # Stats
    calls_in = sum(1 for e in graph["links"] if e.get("relation") == "calls")
    reads_in = sum(1 for e in graph["links"] if e.get("relation") == "reads")
    writes_in = sum(1 for e in graph["links"] if e.get("relation") == "writes")
    callers_with_edges = set()
    for e in graph["links"]:
        if e.get("relation") in ("calls", "reads", "writes"):
            callers_with_edges.add(e["source"])

    all_nodes = {n["id"] for n in graph["nodes"]}
    connected = set()
    for e in graph["links"]:
        connected.add(e["source"])
        connected.add(e["target"])
    isolated = all_nodes - connected

    return {
        "added_nodes": added_nodes,
        "added_edges": added_edges,
        "total_nodes": len(graph["nodes"]),
        "total_links": len(graph["links"]),
        "calls_edges": calls_in,
        "reads_edges": reads_in,
        "writes_edges": writes_in,
        "unique_callers": len(callers_with_edges),
        "modules_with_entry": len(modules_with_top_level),
        "isolated_nodes": len(isolated),
        "isolated_pct": round(100 * len(isolated) / len(all_nodes), 1),
    }


def main():
    project_dirs = [
        "/home/Akhmfz/papan-instrumen",
        "/home/Akhmfz/papan-gerak",
    ]

    for proj in project_dirs:
        sem_file = Path(proj) / "pine_semantic.json"
        graph_file = Path(proj) / "graphify-out" / "graph.json"
        if not sem_file.exists():
            print(f"[SKIP] no {sem_file}")
            continue
        if not graph_file.exists():
            print(f"[SKIP] no {graph_file}")
            continue

        print(f"\n{'='*60}")
        print(f"  {Path(proj).name}")
        print(f"{'='*60}")
        stats = process_project(sem_file, graph_file)
        print(f"  +{stats['added_nodes']} nodes, +{stats['added_edges']} edges")
        print(f"  Total: {stats['total_nodes']} nodes, {stats['total_links']} links")
        print(f"  calls: {stats['calls_edges']} | reads: {stats['reads_edges']} | writes: {stats['writes_edges']}")
        print(f"  Unique callers: {stats['unique_callers']}")
        print(f"  Modules with entry: {stats['modules_with_entry']}")
        print(f"  Isolated: {stats['isolated_nodes']}/{stats['total_nodes']} ({stats['isolated_pct']}%)")


if __name__ == "__main__":
    main()
