"""SchemaCheck — run validate_semantic.py, verify schema compliance."""

import subprocess
import os
from . import CheckResult


class SchemaCheck:
    name = "schema"
    priority = 20
    requires = ["semantic_raw"]
    produces = "semantic_validated"

    def run(self, workspace: str, artifacts: dict) -> CheckResult:
        script = os.path.join(workspace, "scripts", "validate_semantic.py")
        if not os.path.exists(script):
            return CheckResult(
                name=self.name, passed=False, status="ERROR",
                details={}, error=f"validate_semantic.py not found in {workspace}")

        semantic_path = os.path.join(workspace, "pine_semantic.json")
        if not os.path.exists(semantic_path):
            return CheckResult(
                name=self.name, passed=False, status="SKIPPED",
                details={}, error="pine_semantic.json not found (parser may have failed)")

        try:
            result = subprocess.run(
                ["python", script, "--file", semantic_path],
                capture_output=True, text=True, timeout=60,
                cwd=workspace)
        except subprocess.TimeoutExpired:
            return CheckResult(
                name=self.name, passed=False, status="ERROR",
                details={}, error="Schema validator timed out (60s)")

        if result.returncode != 0:
            return CheckResult(
                name=self.name, passed=False, status="FAIL",
                details={"returncode": result.returncode,
                         "stderr": result.stderr[-2000:]},
                error="Schema validation failed")

        return CheckResult(
            name=self.name, passed=True, status="PASS",
            details={"returncode": 0})
