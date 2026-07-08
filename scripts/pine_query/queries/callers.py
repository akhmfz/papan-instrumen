"""query_callers — direct callers of a function (incoming)."""


def query_callers(db, name):
    fn_defs = db.function_index.get(name, [])
    if not fn_defs:
        return {"name": name, "found": False}

    fn_def = fn_defs[0]
    mod = fn_def["module"]
    fn_id = f"src_modules_{mod.replace('-','')}_{name}"

    callers = []
    seen = set()
    for e in db.callee_index.get(fn_id, []):
        if e["relation"] == "calls" and e["caller_id"] not in seen:
            seen.add(e["caller_id"])
            callers.append({
                "caller": e["caller_id"],
                "count": e["count"],
                "label": db.node_index.get(e["caller_id"], {}).get("label", ""),
            })

    return {
        "name": name,
        "found": True,
        "module": mod,
        "callers": callers,
        "total": len(callers),
    }
