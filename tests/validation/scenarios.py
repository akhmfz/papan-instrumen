"""Golden scenarios for Patch Validation Engine.

These test each component in isolation (not full integration which
would require real Pine projects with actual changes).
"""

from pine_query.semantic_diff import diff

BASELINE = {
    "modules": [
        {
            "name": "01base",
            "functions": [
                {"name": "f_momentum", "params": ["src"], "returns": "float",
                 "called_by_count": 2, "calls_count": 1, "lines": 15},
                {"name": "f_volume", "params": ["src"], "returns": "int",
                 "called_by_count": 3, "calls_count": 2, "lines": 20},
            ],
            "variables": [
                {"name": "v_momentum", "type": "float", "scope": "module"},
                {"name": "v_volume", "type": "int", "scope": "module"},
            ],
        },
    ],
}


SCENARIOS = [
    {
        "name": "semantic_diff_no_change",
        "description": "Diff between identical snapshots",
        "component": "semantic_diff",
        "input": {"baseline": BASELINE, "current": BASELINE},
        "checks": {
            "stats.added == 0": True,
            "stats.removed == 0": True,
            "stats.modified == 0": True,
            "stats.unchanged == 4": True,
        },
        "run": lambda inp: diff(inp["baseline"], inp["current"]),
    },
    {
        "name": "semantic_diff_added_entity",
        "description": "Diff when a function is added",
        "component": "semantic_diff",
        "input": {
            "baseline": BASELINE,
            "current": {
                "modules": [
                    {**BASELINE["modules"][0],
                     "functions": BASELINE["modules"][0]["functions"] + [
                         {"name": "f_new", "params": [], "returns": "float",
                          "called_by_count": 0, "calls_count": 0, "lines": 5}
                     ]}
                ]
            },
        },
        "checks": {
            "stats.added == 1": True,
            "stats.removed == 0": True,
            "stats.modified == 0": True,
        },
        "run": lambda inp: diff(inp["baseline"], inp["current"]),
    },
    {
        "name": "semantic_diff_removed_entity",
        "description": "Diff when a function is removed",
        "component": "semantic_diff",
        "input": {
            "baseline": BASELINE,
            "current": {
                "modules": [
                    {**BASELINE["modules"][0],
                     "functions": [BASELINE["modules"][0]["functions"][0]],
                     "variables": BASELINE["modules"][0]["variables"]}
                ]
            },
        },
        "checks": {
            "stats.added == 0": True,
            "stats.removed == 1": True,
            "stats.modified == 0": True,
        },
        "run": lambda inp: diff(inp["baseline"], inp["current"]),
    },
    {
        "name": "semantic_diff_modified_params",
        "description": "Diff when function signature changes",
        "component": "semantic_diff",
        "input": {
            "baseline": BASELINE,
            "current": {
                "modules": [
                    {
                        **BASELINE["modules"][0],
                        "functions": [
                            {**BASELINE["modules"][0]["functions"][0],
                             "params": ["src", "period"]},  # added param
                            BASELINE["modules"][0]["functions"][1],
                        ],
                        "variables": BASELINE["modules"][0]["variables"],
                    }
                ]
            },
        },
        "checks": {
            "stats.added == 0": True,
            "stats.removed == 0": True,
            "stats.modified == 1": True,
            "len(modified) > 0": True,
            "modified[0]['diff'][0]['field'] == 'params'": True,
        },
        "run": lambda inp: diff(inp["baseline"], inp["current"]),
    },
    {
        "name": "risk_low_no_changes",
        "description": "Risk assessment with no changes",
        "component": "risk_scorer",
        "input": {
            "diff": {"stats": {"added": 0, "removed": 0, "modified": 0,
                               "unchanged": 2, "modules_added": 0, "modules_removed": 0}},
            "check_results": [],
        },
        "run": lambda inp: __import__("pine_query.validation.risk_scorer",
                                       fromlist=["assess"]).assess(
                                           inp["diff"], inp["check_results"]),
        "checks": {
            "score == 0": True,
            "level == 'LOW'": True,
        },
    },
    {
        "name": "risk_critical_check_failure",
        "description": "Risk assessment with check failures",
        "component": "risk_scorer",
        "input": {
            "diff": {"stats": {"added": 0, "removed": 0, "modified": 0,
                               "unchanged": 2, "modules_added": 0, "modules_removed": 0}},
            "check_results": [
                type("CR", (), {"name": "parser", "status": "FAIL",
                                "passed": False, "details": {}, "error": "crash"})(),
                type("CR", (), {"name": "golden", "status": "FAIL",
                                "passed": False, "details": {}, "error": "snapshot mismatch"})(),
            ],
        },
        "run": lambda inp: __import__("pine_query.validation.risk_scorer",
                                       fromlist=["assess"]).assess(
                                           inp["diff"], inp["check_results"]),
        "checks": {
            "score >= 0.6": True,
            "level == 'CRITICAL'": True,
        },
    },
]
