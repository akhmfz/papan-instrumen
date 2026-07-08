"""Query registry — all query functions register here."""

from .function import query_function
from .variable import query_variable
from .module import query_module
from .impact import query_impact
from .callers import query_callers
from .callees import query_callees
from .search import query_search
from .builtin import query_builtin
from .explain import query_explain
from .context import query_context
from .stats import query_stats

QUERY_REGISTRY = {
    "function": query_function,
    "variable": query_variable,
    "module": query_module,
    "impact": query_impact,
    "callers": query_callers,
    "callees": query_callees,
    "search": query_search,
    "builtin": query_builtin,
    "explain": query_explain,
    "context": query_context,
    "stats": query_stats,
}
