#!/usr/bin/env python3
"""Golden test runner for Semantic Query Engine.

Usage:
    python3 tests/run_golden.py [--update] [--project pi|pg|all]

Without --update: compare query output against golden snapshots.
With --update: regenerate golden snapshots from current output.
"""

import sys
import os
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from pine_query import SemanticDB
from pine_query.queries import QUERY_REGISTRY

GOLDEN_DIR = Path(__file__).resolve().parent / "golden"

PROJECTS = {
    "pi": "/home/Akhmfz/papan-instrumen",
    "pg": "/home/Akhmfz/papan-gerak",
}

QUERIES = {
    "function": {"pi": "f_scoreHigher", "pg": "f_scoreHigher"},
    "variable": {"pi": "grupUtama", "pg": "trendScore"},
    "module": {"pi": "04-scoring", "pg": "03-scoring"},
    "impact": {"pi": "f_scoreHigher", "pg": "f_scoreHigher"},
    "callers": {"pi": "f_scoreHigher", "pg": "f_scoreHigher"},
    "callees": {"pi": "f_scoreHigher", "pg": "f_scoreHigher"},
    "search-substring": {"pi": "score", "pg": "alert"},
    "search-regex": {"pi": "score|f_.*", "pg": "score|f_.*"},
    "search-exact": {"pi": "f_scoreHigher", "pg": "f_scoreHigher"},
    "builtin": {"pi": "ta.rsi", "pg": "ta.rsi"},
    "explain": {"pi": "f_scoreHigher", "pg": "f_scoreHigher"},
    "context": {"pi": "f_scoreHigher", "pg": "f_scoreHigher"},
    "context-compact": {"pi": "f_scoreHigher", "pg": "f_scoreHigher"},
    "stats": {"pi": None, "pg": None},
}

SEARCH_MODE = {
    "search-substring": "substring",
    "search-regex": "regex",
    "search-exact": "exact",
}

CONTEXT_COMPACT = {
    "context-compact": True,
}

def strip_volatile(data):
    """Remove volatile fields (timestamps, checksums, paths) for comparison."""
    if isinstance(data, dict):
        return {
            k: strip_volatile(v) for k, v in data.items()
            if k not in ("generated_at", "_index_checksum", "generated_by")
            and not k.endswith("_checksum")
        }
    elif isinstance(data, list):
        return [strip_volatile(v) for v in data]
    return data


def run_query(db, qname, arg, proj_key):
    """Dispatch a query with the right arguments."""
    if qname.startswith("search-"):
        pattern = arg
        mode = SEARCH_MODE.get(qname, "substring")
        return QUERY_REGISTRY["search"](db, pattern, mode=mode)

    if qname == "context-compact":
        return QUERY_REGISTRY["context"](db, arg, compact=True)

    if arg is None:
        return QUERY_REGISTRY[qname](db)
    return QUERY_REGISTRY[qname](db, arg)


def main():
    parser = argparse.ArgumentParser(description="Golden test runner")
    parser.add_argument("--update", action="store_true",
                        help="Regenerate golden snapshots")
    parser.add_argument("--project", choices=["pi", "pg", "all"], default="all",
                        help="Project to test (default: all)")
    args = parser.parse_args()

    projects = ["pi", "pg"] if args.project == "all" else [args.project]
    all_passed = True

    for proj_key in projects:
        proj_dir = PROJECTS[proj_key]
        print(f"\n{'='*60}")
        print(f"  {proj_dir}")
        print(f"{'='*60}")
        db = SemanticDB(proj_dir)
        golden_sub = GOLDEN_DIR / proj_key

        for qname, arg_spec in QUERIES.items():
            arg = arg_spec[proj_key] if isinstance(arg_spec, dict) else arg_spec
            result = run_query(db, qname, arg, proj_key)

            result_clean = strip_volatile(result)

            golden_file = golden_sub / f"{qname}.json"

            if args.update:
                golden_file.write_text(json.dumps(result_clean, indent=2, default=str))
                print(f"  ✏️  Updated {golden_file.name}")
            else:
                if golden_file.exists():
                    expected = json.loads(golden_file.read_text())
                    if result_clean == expected:
                        print(f"  ✅ {qname}")
                    else:
                        print(f"  ❌ {qname} — MISMATCH")
                        all_passed = False
                        # Show diff summary
                        for key in set(list(result_clean.keys()) + list(expected.keys())):
                            if result_clean.get(key) != expected.get(key):
                                print(f"      key '{key}' differs")
                else:
                    print(f"  ⚠️  {qname} — no golden file, use --update")
                    all_passed = False

    print(f"\n{'='*60}")
    if args.update:
        print("  Golden snapshots regenerated.")
    elif all_passed:
        print("  ✅ ALL TESTS PASSED")
    else:
        print("  ❌ SOME TESTS FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
