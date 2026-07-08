"""Artifacts — snapshot hashing + manifest generation.

Stores:
    - semantic snapshot hash (pine_semantic.json)
    - graph snapshot hash (graph.json)
    - schema version
    - validator version
    - timestamp
    - checklist of completed checks
"""

import hashlib
import json
import os
import time
from typing import Any


VALIDATOR_VERSION = "1.2.0"


def file_hash(path: str) -> str:
    """SHA-256 of file content. Returns empty string if file missing."""
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


def snapshot(workspace: str, project_name: str = "",
             checks_completed: list[str] | None = None) -> dict:
    """Take a snapshot of current semantic + graph state.
    
    Pure read. No side effects on workspace.
    Returns manifest dict.
    """
    semantic_path = os.path.join(workspace, "pine_semantic.json")
    graph_path = os.path.join(workspace, "graphify-out", "graph.json")

    semantic_hash = file_hash(semantic_path)
    graph_hash = file_hash(graph_path)

    manifest = {
        "project": project_name or os.path.basename(os.path.abspath(workspace)),
        "schema": "1.1",
        "validator": VALIDATOR_VERSION,
        "semantic_hash": semantic_hash,
        "graph_hash": graph_hash,
        "semantic_exists": bool(semantic_hash),
        "graph_exists": bool(graph_hash),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "checks": checks_completed or [],
    }

    return manifest


def read_manifest(manifest_path: str) -> dict | None:
    if not os.path.exists(manifest_path):
        return None
    with open(manifest_path) as f:
        return json.load(f)


def write_manifest(manifest: dict, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
