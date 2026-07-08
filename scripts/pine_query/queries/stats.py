"""query_stats — project-level KPI dashboard."""


def query_stats(db):
    all_nodes = db.node_index
    all_links = list(db.caller_index.items())

    total_nodes = len(all_nodes)
    connected = set()
    for nid, edges in db.caller_index.items():
        connected.add(nid)
        for e in edges:
            connected.add(e["callee_id"])
    for nid, edges in db.callee_index.items():
        connected.add(nid)
        for e in edges:
            connected.add(e["caller_id"])

    isolated = total_nodes - len(connected)

    calls_edges = sum(
        1 for edges in db.caller_index.values()
        for e in edges if e["relation"] == "calls"
    )
    reads_edges = sum(
        1 for edges in db.caller_index.values()
        for e in edges if e["relation"] == "reads"
    )
    writes_edges = sum(
        1 for edges in db.caller_index.values()
        for e in edges if e["relation"] == "writes"
    )

    fn_count = len(db.function_index)
    var_count = len(db.variable_index)
    mod_count = len(db.module_index)

    return {
        "project": str(db.project_dir.name),
        "nodes": {
            "total": total_nodes,
            "isolated": isolated,
            "isolated_pct": round(100 * isolated / total_nodes, 1) if total_nodes else 0,
        },
        "edges": {
            "total": calls_edges + reads_edges + writes_edges,
            "calls": calls_edges,
            "reads": reads_edges,
            "writes": writes_edges,
        },
        "symbols": {
            "functions": fn_count,
            "variables": var_count,
            "modules": mod_count,
        },
        "builtins": {
            "total": len(db.builtin_index),
            "unresolved_calls": sum(
                1 for edges in db.caller_index.values()
                for e in edges if e["relation"] == "calls"
                and not e["callee_id"].startswith("src_modules_")
            ),
        },
    }
