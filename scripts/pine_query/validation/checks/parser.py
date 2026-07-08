"""ParserCheck — run extract_ast.py, verify no crash / parse errors."""

import subprocess
import os
from . import CheckResult


class ParserCheck:
    name = "parser"
    priority = 10
    requires = []
    produces = "semantic_raw"

    def run(self, workspace: str, artifacts: dict) -> CheckResult:
        script = os.path.join(workspace, "scripts", "extract_ast.py")
        if not os.path.exists(script):
            return CheckResult(
                name=self.name, passed=False, status="ERROR",
                details={}, error=f"extract_ast.py not found in {workspace}")

        try:
            result = subprocess.run(
                ["python", script, "--project-dir", workspace],
                capture_output=True, text=True, timeout=300,
                cwd=workspace)
        except subprocess.TimeoutExpired:
            return CheckResult(
                name=self.name, passed=False, status="ERROR",
                details={}, error="Parser timed out (300s)")

        output_path = os.path.join(workspace, "pine_semantic.json")
        json_exists = os.path.exists(output_path)

        if result.returncode != 0:
            return CheckResult(
                name=self.name, passed=False, status="FAIL",
                details={"returncode": result.returncode,
                         "stderr": result.stderr[-2000:]},
                error="extract_ast.py exited with non-zero code")

        if not json_exists:
            return CheckResult(
                name=self.name, passed=False, status="FAIL",
                details={"expected": output_path},
                error="pine_semantic.json not produced")

        return CheckResult(
            name=self.name, passed=True, status="PASS",
            details={"returncode": 0, "output": output_path})
