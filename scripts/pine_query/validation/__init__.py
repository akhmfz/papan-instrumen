"""Patch Validation Engine — read-only validation pipeline for Pine Semantic Layer.

Checks: parser, schema, graph, golden, context (plugin registry).
Output: PASS / PASS_WITH_WARNING / FAIL / ERROR.
"""

from .patch_validator import PatchValidator
from .risk_scorer import assess as assess_risk
from .report_writer import write as write_report
from .artifacts import snapshot, file_hash, VALIDATOR_VERSION
from .checks import CheckResult, get_registry

__all__ = [
    "PatchValidator",
    "assess_risk",
    "write_report",
    "snapshot",
    "file_hash",
    "VALIDATOR_VERSION",
    "CheckResult",
    "get_registry",
]
