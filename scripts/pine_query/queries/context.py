"""query_context — LLM-ready markdown with signature, source snippet, deps."""


def _get_source_snippet(db, name, module, line, max_lines=30):
    fn_defs = db.function_index.get(name, [])
    if not fn_defs:
        return ""
    fn_def = fn_defs[0]
    filepath = fn_def["file"]
    start_line = fn_def["line"]
    try:
        with open(filepath) as f:
            lines = f.readlines()
    except (FileNotFoundError, OSError):
        return ""
    snippet_lines = lines[start_line - 1: start_line - 1 + max_lines]
    result = []
    depth = 0
    for i, line_text in enumerate(snippet_lines):
        stripped = line_text.rstrip("\n")
        open_parens = stripped.count("(") - stripped.count(")")
        depth += open_parens
        result.append(stripped)
        if depth <= 0 and i > 2:
            if not stripped.strip() or stripped.strip().startswith("//"):
                continue
            break
    return "\n".join(result)


def query_context(db, name, compact=False):
    fn_defs = db.function_index.get(name, [])
    if not fn_defs:
        return {"name": name, "found": False}

    fn_def = fn_defs[0]
    mod = fn_def["module"]
    fn_id = f"src_modules_{mod.replace('-','')}_{name}"

    max_lines = 12 if compact else 30
    source = _get_source_snippet(db, name, mod, fn_def["line"], max_lines)

    # Who calls this function (incoming): callee_index
    called_by = []
    seen = set()
    for e in db.callee_index.get(fn_id, []):
        if e["relation"] == "calls" and e["caller_id"] not in seen:
            seen.add(e["caller_id"])
            called_by.append({
                "source": e["caller_id"],
                "label": db.node_index.get(e["caller_id"], {}).get("label", ""),
            })

    # What this function calls (outgoing): caller_index
    callees = []
    seen2 = set()
    for e in db.caller_index.get(fn_id, []):
        if e["relation"] == "calls" and e["callee_id"] not in seen2:
            seen2.add(e["callee_id"])
            callees.append({
                "target": e["callee_id"],
                "label": db.node_index.get(e["callee_id"], {}).get("label", ""),
            })

    reads = []
    writes = []
    for e in db.caller_index.get(fn_id, []):
        if e["relation"] == "reads":
            reads.append({
                "variable": e["callee_id"],
                "label": db.node_index.get(e["callee_id"], {}).get("label", ""),
            })
        elif e["relation"] == "writes":
            writes.append({
                "variable": e["callee_id"],
                "label": db.node_index.get(e["callee_id"], {}).get("label", ""),
            })

    impact_nodes = list(db.transitive_callers(fn_id, depth=3))
    impact_nodes = list(dict.fromkeys(impact_nodes))
    affected_modules = sorted(set(
        tid.split("::")[1] for tid in impact_nodes if tid.startswith("module::")
    ))

    params_str = ", ".join(fn_def["params"])

    return {
        "name": name,
        "found": True,
        "module": mod,
        "file": fn_def["file"],
        "line": fn_def["line"],
        "signature": f"{name}({params_str})",
        "source": source,
        "called_by": called_by,
        "calls": callees,
        "reads": reads,
        "writes": writes,
        "affected_modules": affected_modules,
        "compact": compact,
    }
