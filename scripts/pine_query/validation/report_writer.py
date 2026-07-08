"""ReportWriter — check results + risk + diff → structured report.

Status types:
    PASS                — all checks pass, no warnings
    PASS_WITH_WARNING   — all checks pass, but diff has notable changes
    FAIL                — one or more checks failed
    ERROR               — infrastructure error (parser crash, etc.)
"""

import json


def _final_status(checks: list, risk: dict) -> str:
    has_error = any(c.status == "ERROR" for c in checks)
    has_fail = any(c.status == "FAIL" for c in checks)
    high_risk = risk.get("level") in ("HIGH", "CRITICAL")

    if has_error:
        return "ERROR"
    if has_fail:
        return "FAIL"
    if high_risk:
        return "PASS_WITH_WARNING"
    return "PASS"


def write(checks: list, risk: dict, diff: dict, metadata: dict | None = None) -> dict:
    """Produce structured validation report.
    
    Returns dict ready for JSON serialization.
    """
    status = _final_status(checks, risk)

    report = {
        "report_version": "1.0",
        "status": status,
        "risk": risk,
        "summary": {
            "checks_passed": sum(1 for c in checks if c.status == "PASS"),
            "checks_failed": sum(1 for c in checks if c.status == "FAIL"),
            "checks_errors": sum(1 for c in checks if c.status == "ERROR"),
            "checks_total": len(checks),
        },
        "checks": [
            {"name": c.name, "status": c.status,
             "details": c.details, "error": c.error}
            for c in checks
        ],
        "diff": {
            "stats": diff.get("stats", {}),
            "modified_with_diff": [
                {"name": m.get("name", ""), "changes": m.get("diff", [])}
                for m in diff.get("modified", [])
            ],
        },
        "metadata": metadata or {},
    }

    return report


def write_json(report: dict, path: str) -> None:
    with open(path, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
