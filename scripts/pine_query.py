#!/usr/bin/env python3
"""pine-query — Semantic Query CLI for Pine Script codebases.

Usage:
    pine-query <command> <name> [--format json|table|markdown|mermaid] [--project <dir>]
    pine-query search <pattern> [--mode substring|regex|exact] [--format ...]
    pine-query context <name> [--compact] [--format json|markdown]
    pine-query stats [--format ...]
"""

import sys
import os
import argparse
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _find_project_dir(cwd: str) -> str | None:
    cwd = Path(cwd).resolve()
    for d in [cwd] + list(cwd.parents):
        if (d / "pine_semantic.json").exists():
            return str(d)
    return None


def _build_envelope(query: str, result, project: str) -> dict:
    from datetime import datetime
    return {
        "schema": "query/1.0",
        "query": query,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "project": project,
        "result": result,
    }


def main():
    from pine_query import SemanticDB
    from pine_query.queries import QUERY_REGISTRY
    from pine_query.formatter import FORMATTERS

    parser = argparse.ArgumentParser(
        description="Pine Semantic Query Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("command", nargs="?", default="stats",
                        choices=list(QUERY_REGISTRY.keys()) + ["help"],
                        help="Query type")
    parser.add_argument("name", nargs="?", default=None,
                        help="Symbol name to query")
    parser.add_argument("--project", "-p", default=None,
                        help="Project directory (default: auto-detect via pine_semantic.json)")
    parser.add_argument("--format", "-f", default="table",
                        choices=list(FORMATTERS.keys()),
                        help="Output format (default: table)")
    parser.add_argument("--mode", default="substring",
                        choices=["substring", "regex", "exact"],
                        help="Search mode (default: substring)")
    parser.add_argument("--compact", action="store_true",
                        help="Compact output (context query)")
    parser.add_argument("--raw", action="store_true",
                        help="Output raw result without envelope")

    args = parser.parse_args()

    if args.command == "help":
        print(__doc__)
        return

    project_dir = args.project or _find_project_dir(os.getcwd())
    if not project_dir:
        print("Error: no pine_semantic.json found. Use --project or run from project root.")
        sys.exit(1)

    try:
        db = SemanticDB(project_dir)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    query_fn = QUERY_REGISTRY[args.command]

    if args.command == "search":
        if not args.name:
            print("Error: search requires a pattern argument")
            sys.exit(1)
        result = query_fn(db, args.name, mode=args.mode)
    elif args.command == "context":
        if not args.name:
            print("Error: context requires a function name")
            sys.exit(1)
        result = query_fn(db, args.name, compact=args.compact)
    else:
        result = query_fn(db, args.name) if args.name else query_fn(db)

    envelope = _build_envelope(args.command, result, Path(project_dir).name)
    output = result if args.raw else envelope

    if args.format == "mermaid" and args.command not in ("function", "impact", "module", "callers", "callees"):
        print(f"(mermaid not supported for {args.command}, falling back to table)", file=sys.stderr)
        args.format = "table"

    print(FORMATTERS[args.format](output))


if __name__ == "__main__":
    main()
