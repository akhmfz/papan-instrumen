#!/usr/bin/env python3
"""Semantic Schema Validator — validate pine_semantic.json against schema.

Usage:
    python3 scripts/validate_semantic.py [--project <dir>] [--strict]
    
Exits with code 0 if valid, 1 if warnings, 2 if errors.
"""

import json
import sys
from pathlib import Path

SCHEMA_VERSION = "1.1"
REQUIRED_KEYS = ["schema", "generated_by", "parser", "project", "files", "totals"]
FILE_KEYS = ["module", "file", "functions", "calls", "variables", "reads", "writes"]
FUNCTION_KEYS = ["name", "params", "line"]
CALL_KEYS = ["func_name", "line", "scope", "parent"]
VAR_KEYS = ["name", "line", "is_global"]
READWRITE_KEYS = ["name", "ctx", "line", "parent_function"]
XREF_KEYS = ["caller", "callee", "scope", "resolved"]
TOTAL_KEYS = ["functions", "calls", "variables", "reads", "writes",
              "internal_calls", "unresolved_calls"]


def check_keys(obj, required, label, errors):
    for k in required:
        if k not in obj:
            errors.append(f"missing key '{k}' in {label}")


def validate(filepath: str, strict: bool = False) -> list:
    errors = []
    warnings = []

    try:
        data = json.loads(Path(filepath).read_text())
    except json.JSONDecodeError as e:
        return [f"invalid JSON: {e}"]
    except FileNotFoundError:
        return [f"file not found: {filepath}"]

    if not isinstance(data, dict):
        return [f"root must be a dict, got {type(data).__name__}"]

    check_keys(data, REQUIRED_KEYS, "root", errors)

    schema = data.get("schema", "")
    if schema != SCHEMA_VERSION:
        warnings.append(
            f"schema version {schema} != expected {SCHEMA_VERSION}"
        )

    files = data.get("files", [])
    if not isinstance(files, list):
        errors.append("'files' must be a list")
    else:
        for i, fi in enumerate(files):
            if not isinstance(fi, dict):
                errors.append(f"files[{i}] not a dict")
                continue
            check_keys(fi, FILE_KEYS, f"files[{i}]", errors)

            for fn in fi.get("functions", []):
                check_keys(fn, FUNCTION_KEYS, f"files[{i}].functions", errors)

            for c in fi.get("calls", []):
                check_keys(c, CALL_KEYS, f"files[{i}].calls", errors)
                if c.get("scope") not in ("module", "function", None):
                    errors.append(f"files[{i}].calls scope='{c['scope']}' not valid")

            for v in fi.get("variables", []):
                check_keys(v, VAR_KEYS, f"files[{i}].variables", errors)

            for r in fi.get("reads", []):
                check_keys(r, READWRITE_KEYS, f"files[{i}].reads", errors)

            for w in fi.get("writes", []):
                check_keys(w, READWRITE_KEYS, f"files[{i}].writes", errors)

    cross_refs = data.get("cross_references", [])
    if not isinstance(cross_refs, list):
        warnings.append("'cross_references' not a list")
    else:
        for i, xr in enumerate(cross_refs):
            check_keys(xr, XREF_KEYS, f"cross_references[{i}]", errors)

    totals = data.get("totals", {})
    check_keys(totals, TOTAL_KEYS, "totals", errors)

    if strict:
        # Additional strict checks
        if files:
            total_fn = sum(len(fi.get("functions", [])) for fi in files)
            if total_fn != totals.get("functions", -1):
                errors.append(
                    f"totals.functions ({totals['functions']}) != actual ({total_fn})"
                )

            total_calls = sum(len(fi.get("calls", [])) for fi in files)
            if total_calls != totals.get("calls", -1):
                errors.append(
                    f"totals.calls ({totals['calls']}) != actual ({total_calls})"
                )

        resolved = sum(1 for x in cross_refs if x.get("resolved"))
        if resolved != totals.get("internal_calls", -1):
            warnings.append(
                f"totals.internal_calls ({totals['internal_calls']}) != "
                f"actual resolved ({resolved})"
            )

    return errors + [f"WARNING: {w}" for w in warnings]


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Validate pine_semantic.json schema")
    parser.add_argument("--project", "-p", default=".",
                        help="Project directory containing pine_semantic.json")
    parser.add_argument("--file", "-f", default=None,
                        help="Direct path to pine_semantic.json (overrides --project)")
    parser.add_argument("--strict", action="store_true",
                        help="Enable cross-field consistency checks")
    args = parser.parse_args()

    filepath = args.file or str(Path(args.project) / "pine_semantic.json")
    issues = validate(filepath, strict=args.strict)

    if not issues:
        print(f"✅ {Path(filepath).name}: valid (schema {SCHEMA_VERSION})")
        sys.exit(0)

    errors = [i for i in issues if not i.startswith("WARNING")]
    warnings = [i for i in issues if i.startswith("WARNING")]

    for i in errors:
        print(f"  ❌ {i}")
    for w in warnings:
        print(f"  ⚠️  {w[9:]}")

    if errors:
        print(f"\n❌ FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        sys.exit(2)
    else:
        print(f"\n⚠️  PASSED WITH WARNINGS: {len(warnings)} warning(s)")
        sys.exit(1)


if __name__ == "__main__":
    main()
