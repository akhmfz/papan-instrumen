"""query_callees — direct callees of a function (outgoing)."""


def query_callees(db, name):
    fn_defs = db.function_index.get(name, [])
    if not fn_defs:
        return {"name": name, "found": False}

    fn_def = fn_defs[0]
    mod = fn_def["module"]
    fn_id = f"src_modules_{mod.replace('-','')}_{name}"

    callees = []
    seen = set()
    for e in db.caller_index.get(fn_id, []):
        if e["relation"] == "calls" and e["callee_id"] not in seen:
            seen.add(e["callee_id"])
            callees.append({
                "callee": e["callee_id"],
                "count": e["count"],
                "label": db.node_index.get(e["callee_id"], {}).get("label", ""),
            })
    for e in db.caller_index.get(fn_id, []):
        if e["relation"] in ("reads", "writes") and e["callee_id"] not in seen:
            seen.add(e["callee_id"])
            callees.append({
                "callee": e["callee_id"],
                "relation": e["relation"],
                "count": e["count"],
                "label": db.node_index.get(e["callee_id"], {}).get("label", ""),
            })

    return {
        "name": name,
        "found": True,
        "module": mod,
        "callees": callees,
        "total": len(callees),
    }
