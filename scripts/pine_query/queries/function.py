"""query_function — definition, calls, called_by, reads, writes."""


def query_function(db, name):
    fn_defs = db.function_index.get(name, [])
    if not fn_defs:
        return {"name": name, "found": False}

    fn_def = fn_defs[0]
    mod = fn_def["module"]
    fn_id = f"src_modules_{mod.replace('-','')}_{name}"

    # What this function CALLS (outgoing): use caller_index[fn_id]
    calls = []
    seen_callees = set()
    for e in db.caller_index.get(fn_id, []):
        if e["relation"] == "calls" and e["callee_id"] not in seen_callees:
            seen_callees.add(e["callee_id"])
            calls.append({
                "target": e["callee_id"],
                "relation": "calls",
                "count": e["count"],
                "label": db.node_index.get(e["callee_id"], {}).get("label", ""),
            })

    # Who CALLS this function (incoming): use callee_index[fn_id]
    called_by = []
    seen_callers = set()
    for e in db.callee_index.get(fn_id, []):
        if e["relation"] == "calls" and e["caller_id"] not in seen_callers:
            seen_callers.add(e["caller_id"])
            called_by.append({
                "source": e["caller_id"],
                "relation": "calls",
                "count": e["count"],
                "label": db.node_index.get(e["caller_id"], {}).get("label", ""),
            })

    # Reads/writes: this function → variables, use caller_index[fn_id]
    reads = []
    writes = []
    for e in db.caller_index.get(fn_id, []):
        if e["relation"] == "reads":
            reads.append({
                "variable": e["callee_id"],
                "count": e["count"],
                "label": db.node_index.get(e["callee_id"], {}).get("label", ""),
            })
        elif e["relation"] == "writes":
            writes.append({
                "variable": e["callee_id"],
                "count": e["count"],
                "label": db.node_index.get(e["callee_id"], {}).get("label", ""),
            })

    return {
        "name": name,
        "found": True,
        "module": mod,
        "file": fn_def["file"],
        "line": fn_def["line"],
        "params": fn_def["params"],
        "calls": calls,
        "called_by": called_by,
        "reads": reads,
        "writes": writes,
    }
