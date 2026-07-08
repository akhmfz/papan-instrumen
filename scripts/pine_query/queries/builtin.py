"""query_builtin — lookup builtin symbol + show which modules use it."""


def query_builtin(db, name):
    info = db.builtin_index.get(name)
    if not info:
        return {"name": name, "found": False}

    used_in = set()
    for fn_id, edges in db.caller_index.items():
        for e in edges:
            if e["relation"] == "calls":
                callee_label = db.node_index.get(e["callee_id"], {}).get("label", "")
                if callee_label == name:
                    for fmod, defs in db.function_index.items():
                        for d in defs:
                            nid = f"src_modules_{d['module'].replace('-','')}_{fmod}"
                            if nid == fn_id:
                                used_in.add(d["module"])
                    break

    return {
        "name": name,
        "found": True,
        "category": info["category"],
        "returns": info["returns"],
        "description": info["description"],
        "used_by_modules": sorted(used_in),
        "usage_count": len(used_in),
    }
