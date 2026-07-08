#!/usr/bin/env python3
"""Performance benchmark for Semantic Layer (Sprint 8 RC v1.0 baseline)."""

import sys, json, time, statistics
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from pine_query import SemanticDB
from pine_query.queries import QUERY_REGISTRY

PROJECTS = [
    ("papan-instrumen", "/home/Akhmfz/papan-instrumen"),
    ("papan-gerak", "/home/Akhmfz/papan-gerak"),
]

QUERY_ARGS = {"function": "f_scoreHigher", "variable": "grupUtama",
    "module": "04-scoring", "impact": "f_scoreHigher", "callers": "f_scoreHigher",
    "callees": "f_scoreHigher", "search": None, "builtin": "ta.rsi",
    "explain": "f_scoreHigher", "context": "f_scoreHigher", "stats": None}


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    out = []

    all_results = {}
    for name, proj_dir in PROJECTS:
        r = {"project": name}
        sem_file = Path(proj_dir) / "pine_semantic.json"
        sem = json.loads(sem_file.read_text()) if sem_file.exists() else {}
        r["parse"] = {"total_seconds": round(sum(
            fi.get("parse_time_seconds", 0) for fi in sem.get("files", [])), 2)}

        times = []
        for _ in range(3):
            t0 = time.perf_counter()
            db = SemanticDB(proj_dir)
            times.append(time.perf_counter() - t0)
        r["db_load"] = {"seconds": round(statistics.median(times), 4),
            "functions": len(db.function_index), "variables": len(db.variable_index),
            "modules": len(db.module_index), "nodes": len(db.node_index)}

        qr = {}
        for qname, arg in QUERY_ARGS.items():
            fn = QUERY_REGISTRY[qname]
            t = []
            for _ in range(5):
                t0 = time.perf_counter()
                if qname == "search": fn(db, "score", mode="substring")
                elif arg is None: fn(db)
                elif qname == "context": fn(db, arg, compact=True)
                else: fn(db, arg)
                t.append(time.perf_counter() - t0)
            qr[qname] = round(statistics.median(t) * 1000, 1)
        r["queries"] = qr
        all_results[name] = r

        if not args.json:
            out.append(f"\n=== {name} ===")
            out.append(f"  Parse: {r['parse']['total_seconds']}s")
            out.append(f"  DB load: {r['db_load']['seconds']}s")
            out.append(f"  Queries (ms):")
            for qn, ms in sorted(qr.items()):
                tag = "✅" if ms < 5 else "⚠️" if ms < 20 else "❌"
                out.append(f"    {tag} {qn}: {ms}ms")

    if not args.json:
        out.append(f"\n{'='*60}")
        out.append("  BASELINE v1.0")
        out.append(f"{'='*60}")
        for n, r in all_results.items():
            q = r["queries"]
            out.append(f"  {n}: parse={r['parse']['total_seconds']}s "
                       f"load={r['db_load']['seconds']}s "
                       f"query_range={min(q.values())}ms-{max(q.values())}ms")
        print("\n".join(out))
    else:
        print(json.dumps(all_results, indent=2))


if __name__ == "__main__":
    main()
