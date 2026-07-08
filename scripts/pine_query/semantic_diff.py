"""Semantic Diff — pure function, immutable, no side effects.

Compares two pine_semantic.json snapshots at entity level.

Usage:
    diff = semantic_diff(baseline, current)
    print(diff["added"])       # entities in current but not baseline
    print(diff["removed"])     # entities in baseline but not current
    print(diff["modified"])    # entities in both but changed
"""

from copy import deepcopy
from typing import Any


def _entity_key(name: str, typ: str) -> str:
    return f"{typ}::{name}"


def _normalize(ent: dict) -> dict:
    """Stable, comparable entity snapshot (sorted keys)."""
    return {k: ent.get(k) for k in sorted(ent.keys())}


def _entities_map(snapshot: dict) -> dict[str, dict]:
    """Flatten all entities (functions + variables) into key → entity dict."""
    entities = {}
    for mod in snapshot.get("modules", []):
        for fn in mod.get("functions", []):
            key = _entity_key(fn.get("name", ""), "function")
            entities[key] = _normalize(fn)
            entities[key]["module"] = mod.get("name", "")
        for var in mod.get("variables", []):
            key = _entity_key(var.get("name", ""), "variable")
            entities[key] = _normalize(var)
            entities[key]["module"] = mod.get("name", "")
    return entities


def diff(baseline: dict, current: dict) -> dict:
    """Pure function. Returns immutable Diff object.
    
    Returns:
        {"added": [...], "removed": [...], "modified": [...],
         "unchanged": [...], "modules": {"added": [...], "removed": [...]},
         "stats": {"added": N, "removed": N, "modified": N}}
    """
    base_map = _entities_map(baseline)
    curr_map = _entities_map(current)

    base_keys = set(base_map.keys())
    curr_keys = set(curr_map.keys())

    added_keys = curr_keys - base_keys
    removed_keys = base_keys - curr_keys
    common_keys = base_keys & curr_keys

    added = [curr_map[k] for k in sorted(added_keys)]
    removed = [base_map[k] for k in sorted(removed_keys)]
    modified = []
    unchanged = []

    for key in sorted(common_keys):
        if base_map[key] != curr_map[key]:
            diff_detail = _compute_field_diff(base_map[key], curr_map[key])
            modified.append({"name": key, "baseline": base_map[key],
                             "current": curr_map[key], "diff": diff_detail})
        else:
            unchanged.append({"name": key, "entity": base_map[key]})

    # Top-level module diff
    base_mods = {m.get("name", ""): m for m in baseline.get("modules", [])}
    curr_mods = {m.get("name", ""): m for m in current.get("modules", [])}
    mods_added = [curr_mods[n] for n in sorted(set(curr_mods) - set(base_mods))]
    mods_removed = [base_mods[n] for n in sorted(set(base_mods) - set(curr_mods))]

    result = {
        "added": added,
        "removed": removed,
        "modified": modified,
        "unchanged": unchanged,
        "modules": {"added": mods_added, "removed": mods_removed},
        "stats": {
            "added": len(added),
            "removed": len(removed),
            "modified": len(modified),
            "unchanged": len(unchanged),
            "modules_added": len(mods_added),
            "modules_removed": len(mods_removed),
        },
    }

    return result


def _compute_field_diff(a: dict, b: dict) -> list[dict]:
    """List of {'field': str, 'before': Any, 'after': Any} for changed fields."""
    changes = []
    all_keys = set(a.keys()) | set(b.keys())
    for key in sorted(all_keys):
        va = a.get(key)
        vb = b.get(key)
        if va != vb:
            changes.append({"field": key, "before": va, "after": vb})
    return changes
