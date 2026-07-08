"""query_impact — transitive callers, affected modules/tables/alerts."""


def _resolve_node_id(db, name):
    fn_defs = db.function_index.get(name, [])
    if fn_defs:
        mod = fn_defs[0]["module"]
        return f"src_modules_{mod.replace('-','')}_{name}"
    return db.resolve_var_node(name)


def query_impact(db, name):
    node_id = _resolve_node_id(db, name)
    if not node_id:
        return {"name": name, "found": False, "note": "could not resolve to any node"}

    direct_callers = []
    seen = set()
    for e in db.callee_index.get(node_id, []):
        if e["relation"] == "calls" and e["caller_id"] not in seen:
            seen.add(e["caller_id"])
            direct_callers.append({
                "caller": e["caller_id"],
                "count": e["count"],
                "label": db.node_index.get(e["caller_id"], {}).get("label", ""),
            })

    transitive = list(db.transitive_callers(node_id, depth=4))
    transitive = list(dict.fromkeys(transitive))

    affected_modules = set()
    affected_tables = set()
    affected_alerts = set()
    for tid in transitive:
        if tid.startswith("module::"):
            affected_modules.add(tid.split("::")[1])
        n = db.node_index.get(tid, {})
        label = n.get("label", "")
        if "table" in label.lower() or tid.endswith("table"):
            affected_tables.add(tid)
        if "alert" in label.lower() or "alert" in tid:
            affected_alerts.add(tid)

    return {
        "name": name,
        "node_id": node_id,
        "found": True,
        "direct_callers": direct_callers,
        "transitive_callers_count": len(transitive),
        "transitive_callers": transitive[:30],
        "affected_modules": sorted(affected_modules),
        "affected_tables": sorted(affected_tables),
        "affected_alerts": sorted(affected_alerts),
    }
