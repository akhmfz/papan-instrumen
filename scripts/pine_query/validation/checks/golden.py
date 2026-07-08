"""GoldenCheck — run golden test suite, verify all snapshots match."""

import subprocess
import os
from . import CheckResult


class GoldenCheck:
    name = "golden"
    priority = 40
    requires = ["graph"]
    produces = "golden_result"

    def run(self, workspace: str, artifacts: dict) -> CheckResult:
        runner = os.path.join(workspace, "tests", "run_golden.py")
        if not os.path.exists(runner):
            return CheckResult(
                name=self.name, passed=False, status="ERROR",
                details={}, error=f"run_golden.py not found")

        try:
            result = subprocess.run(
                ["python", runner],
                capture_output=True, text=True, timeout=120,
                cwd=workspace)
        except subprocess.TimeoutExpired:
            return CheckResult(
                name=self.name, passed=False, status="ERROR",
                details={}, error="Golden tests timed out (120s)")

        passed = result.returncode == 0
        status = "PASS" if passed else "FAIL"

        # Count tests from output
        tests_passed = 0
        tests_total = 0
        for line in result.stdout.splitlines():
            if "ALL TESTS PASSED" in line:
                tests_passed = 99  # marker, actual count below
                break
            if "/" in line and "passed" in line.lower():
                parts = line.strip().split("/")
                if len(parts) >= 2:
                    try:
                        tests_passed = int(parts[0].strip())
                        rest = parts[1].split()
                        tests_total = int(rest[0].strip())
                    except (ValueError, IndexError):
                        pass

        # Try to extract actual count from final summary
        for line in result.stdout.splitlines():
            if "TESTS PASSED" in line or "tests passed" in line:
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
