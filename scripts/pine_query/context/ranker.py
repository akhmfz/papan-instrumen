"""Ranker — assign score + evidence to every candidate entity."""

from .profiles import Profile


def rank_entities(entities: list[dict], profile: Profile) -> list[dict]:
    """Rank entities by profile focus.
    
    Each entity gets {entity_id, name, type, module, score, reason, metadata}.
    Returns sorted list descending by score.
    """
    ranked = []
    for ent in entities:
        e = ent.get("entity", ent)
        score = ent.get("score", 0.5)
        reason = ent.get("reason", "graph expansion")

        # Focus boost
        if profile.rank_focus == "incoming" and reason.startswith("caller"):
            score *= 1.2
        elif profile.rank_focus == "outgoing" and reason.startswith("callee"):
            score *= 1.2
        elif profile.rank_focus == "module" and e.get("type") == "module":
            score *= 1.3
        elif profile.rank_focus == "variable" and e.get("type") == "variable":
            score *= 1.2

        ranked.append({
            "entity_id": ent.get("entity_id", ""),
            "name": e.get("name", ""),
            "type": e.get("type", "unknown"),
            "module": e.get("module", ""),
            "score": round(min(score, 1.0), 3),
            "reason": reason,
        })

    ranked.sort(key=lambda x: -x["score"])
    return ranked
