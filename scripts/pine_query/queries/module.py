"""query_module — functions, variables, deps, calls in/out."""

from collections import defaultdict


def query_module(db, name):
    mod_info = db.module_index.get(name)
    if not mod_info:
        return {"name": name, "found": False}

    mod_id = f"src_modules_{name.replace('-','')}"
    entry_id = f"module::{name}::entry"

    functions = []
    for fn_id, n in db.node_index.items():
        label = n.get("label", "")
        if fn_id.startswith(f"src_modules_{name.replace('-','')}_") and "(" in label:
            cid = fn_id
            callees = [e for e in db.callee_index.get(cid, []) if e["relation"] == "calls"]
            functions.append({
                "node_id": fn_id,
                "label": label,
                "callee_count": len(callees),
            })

    variables = []
    var_names = set()
    for fn_id, n in db.node_index.items():
        if fn_id.startswith(f"src_modules_{name.replace('-','')}_") and "(" not in n.get("label", ""):
            label = n.get("label", "")
            if not label.startswith(("color:", "theme:", "const:")):
                continue
            variables.append({"node_id": fn_id, "label": label})
            var_names.add(label.split(":")[-1].strip())

    deps = db.dep_index.get(name, [])
    dependents = []
    for mod, info in db.module_index.items():
        if name in db.dep_index.get(mod, []):
            dependents.append(mod)

    entry_callees = []
    for e in db.caller_index.get(entry_id, []):
        if e["relation"] == "calls":
            entry_callees.append({
                "target": e["callee_id"],
                "label": db.node_index.get(e["callee_id"], {}).get("label", ""),
                "count": e["count"],
            })

    total_calls = sum(
        e["count"] for e in db.caller_index.get(entry_id, [])
        if e["relation"] == "calls"
    )

    return {
        "name": name,
        "found": True,
        "file": mod_info["file"],
        "size_lines": mod_info["size_lines"],
        "functions": len(functions),
        "variables": len(variables),
        "depends_on": deps,
        "depended_by": dependents,
        "functions_list": functions[:20],
        "entry_callees": entry_callees[:15],
        "entry_call_count": total_calls,
    }
