#!/usr/bin/env python3
"""Test runner for Patch Validation Engine.

Tests focus on core logic (semantic_diff, risk_scorer) rather than
full integration which requires real Pine projects.

Usage:
    python tests/validation/runner.py               # run all scenarios
    python tests/validation/runner.py --verbose      # detailed output
    python tests/validation/runner.py --update       # update golden snapshots
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
sys.path.insert(0, os.path.dirname(__file__))

from scenarios import SCENARIOS

EXPECTED_DIR = os.path.join(os.path.dirname(__file__), "expected")


def _dump_result(scenario: dict, result) -> str:
    if hasattr(result, "__dataclass_fields__"):
        result = {"score": result.score, "level": result.level,
                  "reasons": result.reasons}
    return json.dumps({"name": scenario["name"], "result": result}, indent=2)


def check_scenario(scenario: dict, result) -> list[str]:
    errors = []

    if hasattr(result, "__dataclass_fields__"):
        result_dict = {"score": result.score, "level": result.level,
                       "reasons": result.reasons}
    else:
        result_dict = result

    for check_expr, expected in scenario["checks"].items():
        try:
            if "stats." in check_expr:
                parts = check_expr.split(".")
                obj = result_dict.get(parts[0], {})
                attr = ".".join(parts[1:])
                actual = eval(attr, {"__builtins__": __builtins__}, obj) if "." not in parts[1] else eval(check_expr, {"__builtins__": __builtins__}, result_dict)
            elif "modified" in check_expr:
                actual = eval(check_expr, {"__builtins__": __builtins__}, result_dict)
            else:
                actual = eval(check_expr, {"__builtins__": __builtins__}, result_dict)
            if actual != expected:
                errors.append(f"  FAIL: {check_expr} expected={expected} got={actual}")
        except Exception as e:
            errors.append(f"  ERROR: {check_expr} raised {e}")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Run validation tests")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--update", action="store_true")
    args = parser.parse_args()

    os.makedirs(EXPECTED_DIR, exist_ok=True)

    passed = 0
    failed = 0
    failures = []

    for scenario in SCENARIOS:
        try:
            result = scenario["run"](scenario["input"])
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
                print(f"✓ {scenario['name']}: {scenario.get('description', '')}")

        if args.update:
            dump = _dump_result(scenario, result)
            path = os.path.join(EXPECTED_DIR, f"{scenario['name']}.json")
            with open(path, "w") as f:
                f.write(dump + "\n")
            if args.verbose:
                print(f"  (golden updated: {path})")

    total = passed + failed
    print(f"\n{'='*40}")
    print(f"Validation tests: {passed}/{total} passed")
    if failed:
        print("FAILURES:")
        for name, errs in failures:
            print(f"  - {name}")
            for e in errs:
                print(e)
        sys.exit(1)
    else:
        print("All scenarios passed.")


if __name__ == "__main__":
    main()
