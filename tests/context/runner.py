#!/usr/bin/env python3
"""Test runner for context assembly engine.

Usage:
    python tests/context/runner.py               # run all scenarios
    python tests/context/runner.py --verbose      # detailed output
    python tests/context/runner.py --update       # update golden snapshots
"""

import argparse
import json
import os
import sys
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
sys.path.insert(0, os.path.dirname(__file__))

from pine_query import SemanticDB
from pine_query.context import ContextAssembler
from scenarios import SCENARIOS

EXPECTED_DIR = os.path.join(os.path.dirname(__file__), "expected")


def _dump_scenario_result(scenario, result):
    return json.dumps({
        "name": scenario["name"],
        "profile": scenario["profile"],
        "task": scenario["task"],
        "context": result["context"],
        "trace": result["trace"],
    }, indent=2, ensure_ascii=False)


def run_scenario(db, scenario: dict) -> dict:
    engine = ContextAssembler(db)
    result = engine.assemble(scenario["task"], scenario["profile"])
    return result


def check_scenario(scenario: dict, result: dict) -> list[str]:
    errors = []
    ctx = result["context"]

    for check_expr, expected in scenario["checks"].items():
        try:
            actual = eval(check_expr, {"context": ctx, "any": any, "all": all})
            if actual != expected:
                errors.append(f"  FAIL: {check_expr} expected={expected} got={actual}")
        except Exception as e:
            errors.append(f"  ERROR: {check_expr} raised {e}")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Run context assembly tests")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Print detailed results")
    parser.add_argument("--update", action="store_true",
                        help="Update golden snapshots")
    args = parser.parse_args()

    db = SemanticDB(os.path.join(os.path.dirname(__file__), "..", ".."))

    os.makedirs(EXPECTED_DIR, exist_ok=True)

    passed = 0
    failed = 0
    failures = []

    for scenario in SCENARIOS:
        try:
            result = run_scenario(db, scenario)
            errors = check_scenario(scenario, result)
        except Exception as e:
            errors = [f"  RUNTIME ERROR: {e}"]

        if errors:
            failed += 1
            failures.append((scenario["name"], errors))
            if args.verbose:
                print(f"✗ {scenario['name']}")
                for e in errors:
                    print(e)
        else:
            passed += 1
            if args.verbose:
                print(f"✓ {scenario['name']}")

        if args.update:
            dump = _dump_scenario_result(scenario, result)
            path = os.path.join(EXPECTED_DIR, f"{scenario['name']}.json")
            with open(path, "w") as f:
                f.write(dump + "\n")
            if args.verbose:
                print(f"  (golden updated: {path})")

    total = passed + failed
    print(f"\n{'=' * 40}")
    print(f"Context tests: {passed}/{total} passed")
    if failed:
        print(f"FAILURES:")
        for name, errs in failures:
            print(f"  - {name}")
            for e in errs:
                print(e)
        sys.exit(1)
    else:
        print("All scenarios passed.")


if __name__ == "__main__":
    main()
