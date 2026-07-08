"""Pine Semantic Query API — importable Python interface.

Stable API (v1.0):
    from pine_query import SemanticDB, QUERY_REGISTRY, __version__

    db = SemanticDB("/path/to/project")
    result = QUERY_REGISTRY["function"](db, "f_scoreTrend")


Stable API Surface:
    SemanticDB          — load + index pine_semantic.json + graph.json
    QUERY_REGISTRY      — dict[str, callable]: "function", "variable",
                          "module", "impact", "callers", "callees",
                          "search", "builtin", "explain", "context", "stats"

    Each query callable signature:
        fn(db: SemanticDB, name: str, **kwargs) -> dict

Internal (not part of stable API, may change):
    pine_query.queries.*     — individual query modules
    pine_query.formatter     — output formatters
    pine_query.database      — SemanticDB implementation internals
    pine_query.builtin       — builtin catalog
"""

__version__ = "1.0.0"
__all__ = ["SemanticDB", "QUERY_REGISTRY", "__version__"]

from .database import SemanticDB
from .queries import QUERY_REGISTRY
