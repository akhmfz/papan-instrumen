"""query_explain — deterministic structural summary of a function (no LLM)."""


def query_explain(db, name):
    fn_defs = db.function_index.get(name, [])
    if not fn_defs:
        return {"name": name, "found": False}

    fn_def = fn_defs[0]
    mod = fn_def["module"]
    fn_id = f"src_modules_{mod.replace('-','')}_{name}"

    # Outgoing: what this fn calls/reads/writes
    outgoing = db.caller_index.get(fn_id, [])
    # Incoming: who calls this fn
    incoming = db.callee_index.get(fn_id, [])

    direct_calls = [e for e in outgoing if e["relation"] == "calls"]
    reads = [e for e in outgoing if e["relation"] == "reads"]
    writes = [e for e in outgoing if e["relation"] == "writes"]
    callers = [e for e in incoming if e["relation"] == "calls"]

    all_vars = set()
    for ref_list in (reads, writes):
        for e in ref_list:
            all_vars.add(e["callee_id"])

    return {
        "name": name,
        "found": True,
        "module": mod,
        "file": fn_def["file"],
        "line": fn_def["line"],
        "params": fn_def["params"],
        "direct_calls": len(direct_calls),
        "called_by": len(callers),
        "reads_count": len(reads),
        "writes_count": len(writes),
        "variables_total": len(all_vars),
        "total_call_count": sum(e["count"] for e in direct_calls),
        "unique_callers": len(set(e["caller_id"] for e in callers)),
    }
