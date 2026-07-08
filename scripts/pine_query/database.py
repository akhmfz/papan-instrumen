"""SemanticDB — load, index, and cache pine_semantic.json + graph.json."""

import json
import os
import hashlib
from pathlib import Path
from collections import defaultdict

from .builtin import BUILTINS

CACHE_DIR = ".cache"


class SemanticDB:
    """In-memory index over pine_semantic.json and graph.json.
    
    Indexes (all O(1) dict lookups):
      function_index    : name → [{module, file, line, params}]
      variable_index    : name → [{module, file, line, is_global}]
      reverse_var_index : name → [{caller_id, relation, count, module}]
      module_index      : module → {file, size, fn_count, var_count}
      caller_index      : caller_id → [{callee_id, relation, count}]
      callee_index      : callee_id → [{caller_id, relation, count}]
      dep_index         : module → [dep_module]
      node_index        : node_id → node
      builtin_index     : name → builtin_info
    """

    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir).resolve()
        self.sem_file = self.project_dir / "pine_semantic.json"
        self.graph_file = self.project_dir / "graphify-out" / "graph.json"
        self._index_checksum = None
        self.refresh()

    def checksum(self) -> str:
        h = hashlib.sha256()
        for f in [self.sem_file, self.graph_file]:
            if f.exists():
                h.update(f.read_bytes()[:65536])
        return h.hexdigest()[:16]

    def refresh(self):
        self.function_index = {}
        self.variable_index = {}
        self.reverse_var_index = defaultdict(list)
        self.module_index = {}
        self.caller_index = defaultdict(list)
        self.callee_index = defaultdict(list)
        self.dep_index = {}
        self.node_index = {}
        self.builtin_index = dict(BUILTINS)

        if not self.sem_file.exists():
            raise FileNotFoundError(f"{self.sem_file} not found")
        if not self.graph_file.exists():
            raise FileNotFoundError(f"{self.graph_file} not found")

        sem = json.loads(self.sem_file.read_text())
        graph = json.loads(self.graph_file.read_text())

        for n in graph["nodes"]:
            self.node_index[n["id"]] = n

        for fi in sem["files"]:
            mod = fi["module"]
            prefix = mod.replace("-", "")
            self.module_index[mod] = {
                "file": fi["file"],
                "size_lines": fi["size_lines"],
                "fn_count": len(fi["functions"]),
                "var_count": len(fi.get("variables", [])),
            }
            for fn in fi["functions"]:
                name = fn["name"]
                self.function_index.setdefault(name, []).append({
                    "module": mod, "file": fi["file"],
                    "line": fn["line"], "col": fn.get("col", 0),
                    "params": fn["params"],
                })

            for v in fi.get("variables", []):
                vname = v["name"]
                self.variable_index.setdefault(vname, []).append({
                    "module": mod, "file": fi["file"],
                    "line": v["line"], "col": v.get("col", 0),
                    "is_global": v.get("is_global", False),
                })

            if mod in ("01-base", "02-data", "03-ui", "04-scoring"):
                order = {"01-base": 0, "02-data": 1, "03-ui": 2, "04-scoring": 3}
                deps = [m for m in order if order[m] < order.get(mod, 99)]
                self.dep_index[mod] = deps

        for ref_list, relation in [
            (sem.get("cross_references", []), "calls"),
        ] + [(fi.get("reads", []), "reads") for fi in sem["files"]] + \
          [(fi.get("writes", []), "writes") for fi in sem["files"]]:
            pass

        for fi in sem["files"]:
            mod = fi["module"]
            for ref in fi.get("reads", []):
                rname = ref["name"]
                parent = ref.get("parent_function")
                caller_id = f"module::{mod}::entry" if parent is None else f"src_modules_{mod.replace('-','')}_{parent}"
                self.reverse_var_index[rname].append({
                    "caller_id": caller_id,
                    "relation": "reads",
                    "module": mod,
                })
            for ref in fi.get("writes", []):
                rname = ref["name"]
                parent = ref.get("parent_function")
                caller_id = f"module::{mod}::entry" if parent is None else f"src_modules_{mod.replace('-','')}_{parent}"
                self.reverse_var_index[rname].append({
                    "caller_id": caller_id,
                    "relation": "writes",
                    "module": mod,
                })

        for e in graph.get("links", []):
            s, t, r = e["source"], e["target"], e.get("relation", "")
            cnt = e.get("count", 1)
            self.caller_index[s].append({
                "callee_id": t, "relation": r, "count": cnt,
            })
            self.callee_index[t].append({
                "caller_id": s, "relation": r, "count": cnt,
            })

        for e in graph.get("links", []):
            if e.get("relation") == "depends_on":
                self.dep_index.setdefault(e["source"], []).append(e["target"])

        self._index_checksum = self.checksum()

    def resolve_caller_node(self, name: str, module: str) -> str:
        """Resolve a function name (or entry module) to a node ID."""
        if name is None:
            return f"module::{module}::entry"
        nid = f"src_modules_{module.replace('-','')}_{name}"
        if nid in self.node_index:
            return nid
        for fn_list in self.function_index.get(name, []):
            nid2 = f"src_modules_{fn_list['module'].replace('-','')}_{name}"
            if nid2 in self.node_index:
                return nid2
        return f"module::{module}::entry"

    def resolve_var_node(self, name: str) -> str | None:
        """Resolve a variable name to a node ID. Checks all modules."""
        for entry in self.variable_index.get(name, []):
            nid = f"src_modules_{entry['module'].replace('-','')}_{name}"
            if nid in self.node_index:
                return nid
        for nid, n in self.node_index.items():
            if nid.startswith("src_modules_") and nid.endswith(f"_{name}"):
                return nid
        return None

    def collect_callees(self, node_id: str, relation: str | None = None):
        for e in self.caller_index.get(node_id, []):
            if relation is None or e["relation"] == relation:
                yield e

    def collect_callers(self, node_id: str, relation: str | None = None):
        for e in self.callee_index.get(node_id, []):
            if relation is None or e["relation"] == relation:
                yield e

    def transitive_callers(self, node_id: str, depth: int = 5, _seen: set | None = None):
        if _seen is None:
            _seen = set()
        if depth <= 0 or node_id in _seen:
            return
        _seen.add(node_id)
        for e in self.callee_index.get(node_id, []):
            if e["relation"] in ("calls", "reads", "writes"):
                yield e["caller_id"]
                yield from self.transitive_callers(e["caller_id"], depth - 1, _seen)
