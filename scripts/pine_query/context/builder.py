"""ContextBuilder — ranked entities → Context Object with full metadata."""

from pine_query.queries import QUERY_REGISTRY


def _get_source_snippet(db, name: str, module: str, max_lines: int = 30) -> str:
    fn = QUERY_REGISTRY["context"](db, name, compact=(max_lines < 20))
    if fn.get("found"):
        src = fn.get("source", "")
        if src:
            lines = src.split("\n")
            return "\n".join(lines[:max_lines])
    return ""


def build_context(db, ranked: list[dict], profile, trace: list | None = None) -> dict:
    """Build full Context Object from ranked entity list."""
    entities = []
    total_tokens = 0
    module_deps = set()

    for ent in ranked:
        name = ent["name"]
        mod = ent["module"]
        typ = ent["type"]
        score = ent["score"]

        metadata = {}

        if typ == "function" and mod:
            fn = QUERY_REGISTRY["function"](db, name)
            if fn.get("found"):
                metadata["params"] = fn.get("params", [])
                metadata["calls_count"] = len(fn.get("calls", []))
                metadata["called_by_count"] = len(fn.get("called_by", []))
                metadata["reads_count"] = len(fn.get("reads", []))
                metadata["writes_count"] = len(fn.get("writes", []))
                if profile.include_source:
                    metadata["source"] = _get_source_snippet(
                        db, name, mod, profile.source_lines)

        elif typ == "variable" and mod:
            var = QUERY_REGISTRY["variable"](db, name)
            if var.get("found"):
                metadata["read_by_count"] = len(var.get("read_by", []))
                metadata["written_by_count"] = len(var.get("written_by", []))

        if mod:
            module_deps.add(mod)

        ent_tokens = len(name) + len(mod) + len(str(metadata)) // 4 + 50
        total_tokens += ent_tokens

        entities.append({
            "name": name,
            "type": typ,
            "module": mod,
            "score": score,
            "reason": ent.get("reason", ""),
            "metadata": metadata,
        })

    # Collect module info
    modules = {}
    for mod in sorted(module_deps):
        m = QUERY_REGISTRY["module"](db, mod)
        if m.get("found"):
            modules[mod] = {
                "functions": m.get("functions", 0),
                "size_lines": m.get("size_lines", 0),
                "depends_on": m.get("depends_on", []),
                "entry_call_count": m.get("entry_call_count", 0),
            }

    context = {
        "task": {"profile": profile.name, "budget": profile.budget_tokens},
        "entities": entities,
        "modules": modules,
        "total_tokens": total_tokens,
        "entity_count": len(entities),
        "module_count": len(modules),
    }

    if trace is not None:
        trace.append({"phase": "build", "total_tokens": total_tokens, "entities": len(entities)})

    return context
