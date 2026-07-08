"""BudgetStrategy — select entities within token budget."""

from dataclasses import dataclass, field
from typing import Protocol

from .profiles import Profile


class BudgetStrategy(Protocol):
    def apply(self, entities: list[dict], profile: Profile,
              trace: list | None = None) -> list[dict]:
        ...


def _estimate_tokens(ent: dict) -> int:
    name = ent.get("name", "")
    mod = ent.get("module", "")
    base = len(name) + len(mod) + 50  # overhead for metadata
    return max(base, 30)


@dataclass
class SimpleBudget:
    """Simple cumulative budget: keep entities until token cap reached."""

    def apply(self, entities: list[dict], profile: Profile,
              trace: list | None = None) -> list[dict]:
        budget = profile.budget_tokens
        selected = []
        used = 0
        dropped = []

        for ent in entities:
            tokens = _estimate_tokens(ent)
            if used + tokens <= budget:
                selected.append(ent)
                used += tokens
            else:
                dropped.append({"entity": ent, "reason": f"budget exceeded ({used}+{tokens}>{budget})"})

        if trace is not None:
            trace.append({
                "phase": "budget",
                "profile": profile.name,
                "budget_tokens": budget,
                "used_tokens": used,
                "selected": len(selected),
                "dropped": [{"name": d["entity"]["name"], "reason": d["reason"]} for d in dropped],
            })

        return selected
