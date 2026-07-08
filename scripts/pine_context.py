#!/usr/bin/env python3
"""pine-context — CLI for context assembly engine.

Usage:
    python pine_context.py <task> --profile <profile> [--debug] [--json]
    
Profiles: review | implementation | architecture | bugfix
"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pine_query import SemanticDB
from pine_query.context import ContextAssembler, PROFILES
from pine_query.context.compiler import compile_prompt


def main():
    parser = argparse.ArgumentParser(description="pine-context: Context Assembly Engine")
    parser.add_argument("task", nargs="?", default="",
                        help="Natural-language task description (or read stdin if empty)")
    parser.add_argument("--profile", "-p", default="implementation",
                        choices=list(PROFILES.keys()),
                        help="Context profile (default: implementation)")
    parser.add_argument("--db", default=".",
                        help="Project root (default: current dir)")
    parser.add_argument("--debug", action="store_true",
                        help="Print trace for each phase")
    parser.add_argument("--json", action="store_true",
                        help="Output JSON result instead of compiled prompt")
    args = parser.parse_args()

    task = args.task.strip()
    if not task:
        if not sys.stdin.isatty():
            task = sys.stdin.read().strip()
    if not task:
        parser.print_help()
        sys.exit(1)

    db = SemanticDB(args.db)
    engine = ContextAssembler(db)
    result = engine.assemble(task, args.profile)

    if args.json:
        out = {"task": task, "profile": args.profile,
               "context": result["context"], "trace": result["trace"]}
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    print(result["compiled_prompt"])

    if args.debug:
        print("\n--- TRACE ---")
        for step in result["trace"]:
            print(json.dumps(step, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
