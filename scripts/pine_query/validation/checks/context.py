"""ContextCheck — run context test suite, verify no regression."""

import subprocess
import os
from . import CheckResult


class ContextCheck:
    name = "context"
    priority = 50
    requires = ["graph"]
    produces = "context_result"

    def run(self, workspace: str, artifacts: dict) -> CheckResult:
        runner = os.path.join(workspace, "tests", "context", "runner.py")
        if not os.path.exists(runner):
            return CheckResult(
                name=self.name, passed=False, status="ERROR",
                details={}, error=f"context runner not found")

        try:
            result = subprocess.run(
                ["python", runner],
                capture_output=True, text=True, timeout=60,
                cwd=workspace)
        except subprocess.TimeoutExpired:
            return CheckResult(
                name=self.name, passed=False, status="ERROR",
                details={}, error="Context tests timed out (60s)")

        passed = result.returncode == 0
        status = "PASS" if passed else "FAIL"

        # Parse test count
        tests_passed = 0
        tests_total = 0
        for line in result.stdout.splitlines():
            if "context tests:" in line.lower() or "tests passed" in line.lower():
                words = line.split()
                for w in words:
                    if "/" in w:
                        parts = w.split("/")
                        try:
                            tests_passed = int(parts[0])
                            tests_total = int(parts[1])
                        except (ValueError, IndexError):
                            pass

        return CheckResult(
            name=self.name, passed=passed, status=status,
            details={
                "returncode": result.returncode,
                "tests_passed": tests_passed,
                "tests_total": tests_total,
                "stdout": result.stdout[-1000:] if not passed else "",
                "stderr": result.stderr[-1000:] if not passed else "",
            })
