"""GraphCheck — run inject_graph.py, verify graph integrity."""

import subprocess
import os
import json
from . import CheckResult


class GraphCheck:
    name = "graph"
    priority = 30
    requires = ["semantic_validated"]
    produces = "graph"

    def run(self, workspace: str, artifacts: dict) -> CheckResult:
        script = os.path.join(workspace, "scripts", "inject_graph.py")
        if not os.path.exists(script):
            return CheckResult(
                name=self.name, passed=False, status="ERROR",
                details={}, error=f"inject_graph.py not found in {workspace}")

        graph_path = os.path.join(workspace, "graphify-out", "graph.json")

        try:
            result = subprocess.run(
                ["python", script, workspace],
                capture_output=True, text=True, timeout=120,
                cwd=workspace)
        except subprocess.TimeoutExpired:
            return CheckResult(
                name=self.name, passed=False, status="ERROR",
                details={}, error="Graph injector timed out (120s)")

        if result.returncode != 0:
            return CheckResult(
                name=self.name, passed=False, status="FAIL",
                details={"returncode": result.returncode,
                         "stderr": result.stderr[-2000:]},
                error="inject_graph.py exited with non-zero code")

        if not os.path.exists(graph_path):
            return CheckResult(
                name=self.name, passed=False, status="FAIL",
                details={"expected": graph_path},
                error="graph.json not produced")

        # Basic graph integrity check
        try:
            with open(graph_path) as f:
                graph = json.load(f)
            nodes = graph.get("nodes", graph.get("elements", []))
            if not isinstance(nodes, list) or len(nodes) == 0:
                return CheckResult(
                    name=self.name, passed=False, status="FAIL",
                    details={"node_count": len(nodes) if isinstance(nodes, list) else -1},
                    error="Graph has zero nodes")
        except (json.JSONDecodeError, IOError) as e:
            return CheckResult(
                name=self.name, passed=False, status="ERROR",
                details={}, error=f"Graph file unreadable: {e}")

        return CheckResult(
            name=self.name, passed=True, status="PASS",
            details={"node_count": len(nodes), "path": graph_path})
