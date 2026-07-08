"""SemanticSelector — intent → candidate entities via QUERY_REGISTRY search."""

from pine_query.queries import QUERY_REGISTRY


def select(db, intent: dict) -> list[dict]:
    """Select candidate entities from intent keywords.
    
    Returns list of {entity_id, name, type, module, score, reason}.
    """
    candidates = {}
    seen = set()

    def add(name: str, typ: str, score: float, reason: str):
        key = (typ, name)
        if key in seen:
            # Boost existing
            for c in candidates.values():
                if c["type"] == typ and c["name"] == name:
                    c["score"] = max(c["score"], score)
                    c["reason"] = f"{c['reason']} + {reason}"
            return
        seen.add(key)
        entry = {"name": name, "type": typ, "module": "", "score": score, "reason": reason}
        # Try to resolve module
        results = QUERY_REGISTRY["search"](db, name, mode="exact")
        for r in results.get("results", []):
            if r["name"] == name:
                entry["module"] = r["module"]
                break
        candidates[f"{typ}:{name}"] = entry

    # Search each domain keyword
    for domain in intent.get("domains", []):
        results = QUERY_REGISTRY["search"](db, domain, mode="substring")
        for r in results.get("results", [])[:10]:
            score = 0.95 if r["name"].startswith(f"f_{domain}") else 0.85
            add(r["name"], r["type"], score, f"keyword '{domain}' matched")

    # Search each filter
    for flt in intent.get("filters", []):
        if "_" in flt:
            parts = flt.split("_")
            for part in parts:
                results = QUERY_REGISTRY["search"](db, part, mode="substring")
                for r in results.get("results", [])[:5]:
                    add(r["name"], r["type"], 0.8, f"filter '{part}' matched")
        else:
            results = QUERY_REGISTRY["search"](db, flt, mode="substring")
            for r in results.get("results", [])[:5]:
                add(r["name"], r["type"], 0.8, f"filter '{flt}' matched")

    return list(candidates.values())
