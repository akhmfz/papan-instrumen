"""PatchValidator — read-only orchestrator: snapshot → checks → diff → risk → report → artifacts.

This is the main entry point for validation. It:
    1. Reads the workspace (never writes to it)
    2. Runs each check in CHECK_REGISTRY (ordered by priority)
    3. Computes semantic diff (if baseline available)
    4. Assesses risk
    5. Writes structured report + artifacts
"""

import json
import os
import time

from .checks import CheckResult, get_registry, skip_checks, only_checks
from .risk_scorer import assess
from .report_writer import write as write_report, write_json
from .artifacts import snapshot as snap, write_manifest, VALIDATOR_VERSION
from pine_query.semantic_diff import diff

BASELINE_DIR = ".pine-validate"


class PatchValidator:
    """Read-only validator. Never modifies workspace source code."""

    def __init__(self, workspace: str, project_name: str = ""):
        self.workspace = os.path.abspath(workspace)
        self.project_name = project_name or os.path.basename(self.workspace)
        self.artifacts_dir = os.path.join(self.workspace, BASELINE_DIR)
        self.check_results: list[CheckResult] = []

    def _load_baseline(self) -> dict | None:
        path = os.path.join(self.artifacts_dir, "pine_semantic.json")
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
        return None

    def _load_current(self) -> dict | None:
        path = os.path.join(self.workspace, "pine_semantic.json")
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
        return None

    def validate(self, skip: set[str] | None = None,
                 only: set[str] | None = None,
                 save_artifacts: bool = True) -> dict:
        """Run full validation pipeline.
        
        Args:
            skip: set of check names to skip
            only: if set, only run these checks
            save_artifacts: write report + manifest to .pine-validate/
        
        Returns:
            dict with {status, checks, risk, diff, report, artifacts, trace}
        """
        trace = []
        checks = list(get_registry())

        if only:
            checks = only_checks(checks, only)
        elif skip:
            checks = skip_checks(checks, skip)

        checks.sort(key=lambda c: c.priority)
        trace.append({"phase": "check_order",
                      "checks": [c.name for c in checks]})

        # Run each check
        artifacts: dict[str, object] = {}
        self.check_results = []

        for check in checks:
            result = check.run(self.workspace, artifacts)
            self.check_results.append(result)
            if result.status == "PASS" and check.produces:
                artifacts[check.produces] = True
            trace.append({"phase": f"check:{check.name}",
                          "status": result.status,
                          "duration": result.details.get("duration", 0)})

        # Semantic diff
        baseline = self._load_baseline()
        current = self._load_current()
        diff_result: dict = {}
        if baseline and current:
            try:
                diff_result = diff(baseline, current)
            except Exception as e:
                diff_result = {"stats": {}, "error": str(e)}
        trace.append({"phase": "diff",
                      "baseline": baseline is not None,
                      "current": current is not None,
                      "diff_stats": diff_result.get("stats", {})})

        # Risk assessment
        risk = assess(diff_result, self.check_results)
        trace.append({"phase": "risk",
                      "score": risk["score"],
                      "level": risk["level"]})

        # Report
        metadata = {"workspace": self.workspace,
                    "validator_version": VALIDATOR_VERSION}
        report = write_report(self.check_results, risk, diff_result, metadata)
        trace.append({"phase": "report", "status": report["status"]})

        result_data = {
            "status": report["status"],
            "checks": self.check_results,
            "risk": risk,
            "diff": diff_result,
            "report": report,
            "trace": trace,
        }

        # Save artifacts
        if save_artifacts:
            self._save_artifacts(result_data)

        return result_data

    def _save_artifacts(self, result: dict) -> None:
        os.makedirs(self.artifacts_dir, exist_ok=True)

        # Report JSON
        report_path = os.path.join(self.artifacts_dir, "report.json")
        write_json(result["report"], report_path)

        # Manifest
        checks_done = [c.name for c in self.check_results]
        manifest = snap(self.workspace, self.project_name, checks_done)
        manifest_path = os.path.join(self.artifacts_dir, "manifest.json")
        write_manifest(manifest, manifest_path)
