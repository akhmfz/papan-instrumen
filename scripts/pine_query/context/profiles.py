"""Context profiles: token budget + rank focus per profile."""

from dataclasses import dataclass, field


@dataclass
class Profile:
    name: str
    budget_tokens: int
    description: str
    rank_focus: str  # "incoming", "outgoing", "module", "variable"
    include_source: bool = True
    source_lines: int = 30
    include_impact: bool = True
    include_callers: bool = True
    include_callees: bool = True
    include_modules: bool = True
    include_trace: bool = False


PROFILES: dict[str, Profile] = {
    "review": Profile(
        name="review",
        budget_tokens=4096,
        description="Code review: full dep chain, affected tables/alerts",
        rank_focus="incoming",
        source_lines=20,
        include_impact=True,
        include_callers=True,
        include_callees=False,
        include_modules=True,
    ),
    "implementation": Profile(
        name="implementation",
        budget_tokens=8192,
        description="Implementation: direct deps + source snippets",
        rank_focus="outgoing",
        source_lines=30,
        include_impact=False,
        include_callers=True,
        include_callees=True,
        include_modules=True,
    ),
    "architecture": Profile(
        name="architecture",
        budget_tokens=12288,
        description="Architecture: module-level + cross-refs + full entity list",
        rank_focus="module",
        source_lines=15,
        include_impact=False,
        include_callers=True,
        include_callees=True,
        include_modules=True,
    ),
    "bugfix": Profile(
        name="bugfix",
        budget_tokens=6144,
        description="Bug fix: callers + variable read/write chain",
        rank_focus="variable",
        source_lines=25,
        include_impact=False,
        include_callers=True,
        include_callees=False,
        include_modules=True,
    ),
}
