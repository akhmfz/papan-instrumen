"""RiskScorer — assign risk score and level based on semantic diff + check results."""

import os


def _calc_diff_risk(diff: dict) -> tuple[float, list[str]]:
    """Score 0-1 from diff stats. Higher = riskier."""
    reasons = []
    score = 0.0
    stats = diff.get("stats", {})

    removed = stats.get("removed", 0)
    added = stats.get("added", 0)
    modified = stats.get("modified", 0)
    mods_removed = stats.get("modules_removed", 0)
    mods_added = stats.get("modules_added", 0)

    if removed > 0:
        score += 0.3 * min(removed / 5, 1.0)
        reasons.append(f"removed_{removed}_entities")

    if modified > 0:
        score += 0.25 * min(modified / 5, 1.0)
        reasons.append(f"modified_{modified}_entities")

    if added > 10:
        score += 0.15
        reasons.append(f"bulk_add_{added}_entities")

    if mods_removed > 0:
        score += 0.3
        reasons.append(f"removed_{mods_removed}_modules")

    if mods_added > 0:
        score += 0.1
        reasons.append(f"added_{mods_added}_modules")

    # Check if any modified entity has signature change
    for m in diff.get("modified", []):
        field_diffs = m.get("diff", [])
        for fd in field_diffs:
            if fd.get("field") in ("params", "returns", "name"):
                score += 0.2
                reasons.append(f"signature_change:{m.get('name','')}")
                break

    # Check if any modified entity is called by many others
    for m in diff.get("modified", []):
        curr = m.get("current", {})
        if curr.get("called_by_count", 0) > 5:
            score += 0.1
            reasons.append(f"high_impact:{m.get('name','')}_called_by_{curr['called_by_count']}")

    score = min(score, 1.0)
    return round(score, 3), reasons


def _calc_check_risk(checks: list) -> tuple[float, list[str]]:
    """Score 0-1 from check failures."""
    reasons = []
    score = 0.0
    for check in checks:
        if check.status == "FAIL":
            score += 0.5
            reasons.append(f"check_failed:{check.name}")
        elif check.status == "ERROR":
            score += 0.7
            reasons.append(f"check_error:{check.name}")
    score = min(score, 1.0)
    return round(score, 3), reasons


def assess(diff: dict, check_results: list) -> dict:
    """Assess overall risk from semantic diff + check results.
    
    Returns:
        {"score": float, "level": "LOW"|"MEDIUM"|"HIGH"|"CRITICAL",
         "reasons": [str]}
    """
    diff_score, diff_reasons = _calc_diff_risk(diff)
    check_score, check_reasons = _calc_check_risk(check_results)

    # Weighted: check failures matter more than diff changes
    score = max(diff_score, check_score * 1.2)
    reasons = diff_reasons + check_reasons

    if check_score >= 0.5:
        level = "CRITICAL"
    elif score >= 0.5:
        level = "HIGH"
    elif score >= 0.25:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "score": round(min(score, 1.0), 3),
        "level": level,
        "reasons": reasons,
    }
