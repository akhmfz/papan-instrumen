"""query_variable — declaration, read_by, written_by."""


def query_variable(db, name):
    var_defs = db.variable_index.get(name, [])
    if not var_defs:
        nid = next(
            (nid for nid, _ in db.node_index.items()
             if nid.startswith("src_modules_") and nid.endswith(f"_{name}")),
            None,
        )
        if nid:
            return {
                "name": name,
                "found": True,
                "file_type": db.node_index[nid].get("file_type", ""),
                "label": db.node_index[nid].get("label", ""),
                "module": nid.split("_")[2],
            }
        return {"name": name, "found": False, "node_exists": nid is not None}

    var_def = var_defs[0]
    refs = db.reverse_var_index.get(name, [])
    read_by = []
    written_by = []
    seen = set()
    for ref in refs:
        cid = ref["caller_id"]
        key = (cid, ref["relation"])
        if key not in seen:
            seen.add(key)
            entry = {
                "caller": cid,
                "relation": ref["relation"],
                "label": db.node_index.get(cid, {}).get("label", ""),
                "module": ref["module"],
            }
            if ref["relation"] == "reads":
                read_by.append(entry)
            else:
                written_by.append(entry)

    return {
        "name": name,
        "found": True,
        "module": var_def["module"],
        "file": var_def["file"],
        "line": var_def["line"],
        "is_global": var_def.get("is_global", False),
        "read_by": read_by,
        "written_by": written_by,
    }
