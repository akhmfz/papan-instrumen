"""Golden scenarios for context assembly engine.

Each scenario: task string + expected properties to check.
Context dict is evaluated in eval() as `context` variable.
"""

SCENARIOS = [
    {
        "name": "momentum_variable",
        "task": "Tambah indikator momentum untuk sektor energi",
        "profile": "implementation",
        "checks": {
            "context.get('entity_count', 0) >= 0": True,
            "len(context.get('entities', [])) >= 0": True,
            "context.get('task', {}).get('profile') == 'implementation'": True,
        },
    },
    {
        "name": "review_alert",
        "task": "Review alert function di modul momentum",
        "profile": "review",
        "checks": {
            "context.get('task', {}).get('profile') == 'review'": True,
            "context.get('entity_count', 0) >= 0": True,
        },
    },
    {
        "name": "bugfix_variable",
        "task": "Fix bug on volume variable read chain",
        "profile": "bugfix",
        "checks": {
            "context.get('task', {}).get('profile') == 'bugfix'": True,
            "context.get('entity_count', 0) >= 0": True,
        },
    },
    {
        "name": "architecture",
        "task": "Show architecture of momentum module",
        "profile": "architecture",
        "checks": {
            "context.get('task', {}).get('profile') == 'architecture'": True,
            "context.get('module_count', 0) >= 0": True,
        },
    },
    {
        "name": "unknown_task_graceful",
        "task": "zzz unknown gibberish xyzzy",
        "profile": "implementation",
        "checks": {
            "context.get('entity_count', 0) >= 0": True,
            "context.get('task', {}).get('profile') == 'implementation'": True,
        },
    },
]
