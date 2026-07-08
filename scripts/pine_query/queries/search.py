"""query_search — fuzzy, regex, or exact search across all symbols."""

import re


def _search_candidates(db):
    """Yield (name, type, module, label) for all indexed symbols."""
    seen = set()
    for name, defs in db.function_index.items():
        mod = defs[0]["module"]
        key = ("function", name)
        if key not in seen:
            seen.add(key)
            yield (name, "function", mod, f"{name}()")
    for name, defs in db.variable_index.items():
        mod = defs[0]["module"]
        key = ("variable", name)
        if key not in seen:
            seen.add(key)
            yield (name, "variable", mod, name)
    for name in db.builtin_index:
        key = ("builtin", name)
        if key not in seen:
            seen.add(key)
            yield (name, "builtin", "pine-v6", name)


def query_search(db, pattern, mode="substring"):
    results = []
    for name, typ, mod, label in _search_candidates(db):
        if mode == "exact":
            if name == pattern:
                results.append({"name": name, "type": typ, "module": mod, "label": label})
        elif mode == "regex":
            try:
                if re.search(pattern, name):
                    results.append({"name": name, "type": typ, "module": mod, "label": label})
            except re.error:
                pass
        else:
            if pattern.lower() in name.lower():
                results.append({"name": name, "type": typ, "module": mod, "label": label})
    return {
        "pattern": pattern,
        "mode": mode,
        "total": len(results),
        "results": sorted(results, key=lambda x: (x["type"], x["name"]))[:50],
    }
