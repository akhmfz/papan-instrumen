"""Check registry — plugin protocol for validation checks.

Each check implements:
    name: str
    priority: int (lower = earlier)
    requires: list[str] (names of artifacts this check needs)
    produces: str (artifact key this check creates)
    run(workspace: str, artifacts: dict) -> CheckResult
"""

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass
class CheckResult:
    name: str = ""
    passed: bool = False
    status: str = "ERROR"  # PASS | FAIL | ERROR | SKIPPED
    details: dict = field(default_factory=dict)
    error: str = ""


class Check(Protocol):
    name: str
    priority: int
    requires: list[str]
    produces: str

    def run(self, workspace: str, artifacts: dict) -> CheckResult:
        ...


def skip_checks(checks: list, skip_names: set[str]) -> list:
    return [c for c in checks if c.name not in skip_names]


def only_checks(checks: list, only_names: set[str]) -> list:
    return [c for c in checks if c.name in only_names]


CHECK_REGISTRY: list = []


def _build_registry() -> list:
    from .parser import ParserCheck
    from .schema import SchemaCheck
    from .graph import GraphCheck
    from .golden import GoldenCheck
    from .context import ContextCheck
    return [
        ParserCheck(),
        SchemaCheck(),
        GraphCheck(),
        GoldenCheck(),
        ContextCheck(),
    ]


# Auto-populate on first access
def get_registry() -> list:
    if not CHECK_REGISTRY:
        CHECK_REGISTRY.extend(_build_registry())
    return CHECK_REGISTRY
