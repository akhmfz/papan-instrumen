"""Expander — entity → neighbor entities via graph traversal (BFS 1-2 hops).

Internal API (not exposed in QUERY_REGISTRY).
"""


def _neighbor_weight(depth: int) -> float:
    return {0: 1.0, 1: 0.5, 2: 0.25}.get(depth, 0.1)


def _entity_type_from_id(node_id: str) -> str:
    if node_id.startswith("module::"):
        return "module_entry"
    if "::" in node_id:
        return "entry"
    if node_id.startswith("src_modules_01base_") and "(" in str(
        __import__("pine_query").SemanticDB.__name__):
        pass
    if node_id.startswith("src_modules_"):
        rest = node_id[len("src_modules_"):]
        if "_" in rest:
            return "function" if "(" in node_id else "variable"
    return "node"


def expand_neighbors(db, entities: list[dict], depth: int = 2) -> list[dict]:
    """Expand entities by walking graph edges (calls, reads, writes).
    
    Returns flat list with dedup + decayed scores.
    """
    from collections import defaultdict
    from pine_query.queries import QUERY_REGISTRY

    expanded = {}
    seen_ids = set()

    def resolve_entity_id(e: dict) -> str | None:
        name = e["name"]
        typ = e["type"]
        mod = e.get("module", "")
        if typ == "function" and mod:
            return f"src_modules_{mod.replace('-','')}_{name}"
        if typ == "module":
            return f"src_modules_{mod.replace('-','')}" if mod else None
        return None

    for e in entities:
        eid = resolve_entity_id(e)
        if eid:
            expanded[eid] = {"entity": e, "depth": 0, "score": e["score"]}
            seen_ids.add(eid)

        name = e["name"]
        fn_result = QUERY_REGISTRY["function"](db, name) if e["type"] == "function" else None
        if fn_result and fn_result.get("found"):
            fn_id = resolve_entity_id(e)
            if fn_id:
                for callee in fn_result.get("calls", []):
                    tid = callee.get("target", "")
                    if tid and tid not in seen_ids:
                        expanded[tid] = {
                            "entity": {"name": tid.split("_")[-1], "type": "function",
                                       "module": e["module"], "score": e["score"] * 0.5},
                            "depth": 1, "score": e["score"] * 0.5,
                            "reason": f"callee of {name} (1 hop)",
                        }
                        seen_ids.add(tid)
                for caller in fn_result.get("called_by", []):
                    sid = caller.get("source", "")
                    if sid and sid not in seen_ids:
                        expanded[sid] = {
                            "entity": {"name": sid.split("_")[-1], "type": "function",
                                       "module": e["module"], "score": e["score"] * 0.5},
                            "depth": 1, "score": e["score"] * 0.5,
                            "reason": f"caller of {name} (1 hop)",
                        }
                        seen_ids.add(sid)

    result = []
    for eid, info in expanded.items():
        result.append({
            "entity_id": eid,
            "entity": info["entity"],
            "depth": info["depth"],
            "score": info["score"],
            "reason": info.get("reason", "direct match"),
        })

    return result
