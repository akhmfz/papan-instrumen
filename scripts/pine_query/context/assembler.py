"""ContextAssembler — orchestrate: intent → select → expand → rank → budget → build."""

from .intent import extract_intent
from .selector import select
from .expander import expand_neighbors
from .ranker import rank_entities
from .budget import SimpleBudget
from .builder import build_context
from .profiles import PROFILES
from .compiler import compile_prompt
from pine_query import SemanticDB


class ContextAssembler:
    """Orchestrator. Each step is logged in self.trace."""

    def __init__(self, db: SemanticDB):
        self.db = db
        self.trace = []
        self.budget_strategy = SimpleBudget()

    def assemble(self, task: str, profile_name: str = "implementation") -> dict:
        profile = PROFILES.get(profile_name)
        if not profile:
            available = list(PROFILES.keys())
            raise ValueError(f"Unknown profile '{profile_name}'. Available: {available}")

        self.trace = []

        intent = extract_intent(task)
        self.trace.append({"phase": "intent", "intent": intent})

        candidates = select(self.db, intent)
        self.trace.append({"phase": "select", "candidates": len(candidates)})

        expanded = expand_neighbors(self.db, candidates, depth=2)
        self.trace.append({"phase": "expand", "expanded": len(expanded)})

        ranked = rank_entities(expanded, profile)
        self.trace.append({"phase": "rank", "ranked": len(ranked),
                          "top": ranked[:5] if ranked else []})

        budgeted = self.budget_strategy.apply(ranked, profile, trace=self.trace)

        context = build_context(self.db, budgeted, profile, trace=self.trace)

        return {
            "task": task,
            "profile": profile_name,
            "context": context,
            "trace": self.trace,
            "compiled_prompt": compile_prompt(context, profile_name),
        }
