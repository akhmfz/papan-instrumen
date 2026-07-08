#!/usr/bin/env python3
"""pine-validate — CLI for Patch Validation Engine.

Read-only validation of a workspace with Pine Semantic Layer changes.

Usage:
    python pine_validate.py --workspace <dir>                   # full validation
    python pine_validate.py --workspace <dir> --json            # JSON output
    python pine_validate.py --workspace <dir> --skip golden     # skip specific checks
    python pine_validate.py --workspace <dir> --only parser     # run only one check
    python pine_validate.py --workspace <dir> --debug           # with execution trace
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pine_query.validation import PatchValidator
from pine_query.validation.checks import get_registry


def main():
    parser = argparse.ArgumentParser(
        description="pine-validate: Patch Validation Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__)
    parser.add_argument("--workspace", "-w", default=".",
                        help="Project root with Pine Semantic Layer (default: .)")
    parser.add_argument("--json", action="store_true",
                        help="Output full JSON report")
    parser.add_argument("--debug", action="store_true",
                        help="Print execution trace")
    parser.add_argument("--skip", nargs="+", default=[],
                        choices=[c.name for c in get_registry()],
                        help="Checks to skip")
    parser.add_argument("--only", nargs="+", default=[],
                        choices=[c.name for c in get_registry()],
                        help="Only run specified checks")
    parser.add_argument("--no-artifacts", action="store_true",
                        help="Skip saving artifacts to .pine-validate/")

    args = parser.parse_args()

    workspace = os.path.abspath(args.workspace)
    if not os.path.isdir(workspace):
        print(f"Error: workspace directory not found: {workspace}", file=sys.stderr)
        sys.exit(1)

    validator = PatchValidator(workspace)

    skip = set(args.skip) if args.skip else None
    only = set(args.only) if args.only else None

    result = validator.validate(
        skip=skip,
        only=only,
        save_artifacts=not args.no_artifacts,
    )

    if args.json:
        output = {
            "status": result["report"]["status"],
            "risk": result["risk"],
            "summary": result["report"]["summary"],
            "checks": [
                {"name": c.name, "status": c.status,
                 "details": c.details, "error": c.error}
                for c in result["checks"]
            ],
            "diff_stats": result["diff"].get("stats", {}),
        }
        if args.debug:
            output["trace"] = result["trace"]
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return

    # Human-readable output
    print(f"\n{'='*50}")
    print(f"  Pine Validate — {workspace}")
    print(f"{'='*50}")
    print(f"  Status:      {result['report']['status']}")
    print(f"  Risk Level:  {result['risk']['level']} (score: {result['risk']['score']})")
    print(f"  Checks:      {result['report']['summary']['checks_passed']}/"
          f"{result['report']['summary']['checks_total']} passed")
    print(f"  Artifacts:   {'.pine-validate/' if not args.no_artifacts else '(disabled)'}")

    for c in result["checks"]:
        icon = {"PASS": "✓", "FAIL": "✗", "ERROR": "⚡", "SKIPPED": "–"}
        print(f"  {icon.get(c.status, '?')} {c.name}: {c.status}")
        if c.status in ("FAIL", "ERROR") and c.error:
            print(f"     {c.error[:200]}")

    if result["risk"].get("reasons"):
        print(f"  Risk Reasons: {', '.join(result['risk']['reasons'][:5])}")

    diff_stats = result["diff"].get("stats", {})
    if any(v for v in diff_stats.values()):
        print(f"\n  Semantic Changes:")
        print(f"    +{diff_stats.get('added', 0)}  -{diff_stats.get('removed', 0)}"
              f"  ~{diff_stats.get('modified', 0)} entities")

    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
