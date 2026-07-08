"""Context Assembly Engine — task → deterministic context → compiled prompt.

Usage:
    from pine_query.context import ContextAssembler
    from pine_query import SemanticDB

    db = SemanticDB("/project")
    engine = ContextAssembler(db)
    result = engine.assemble("Tambah indikator momentum", "implementation")
    print(result["compiled_prompt"])
    print(result["trace"])  # for --debug
"""

from .assembler import ContextAssembler
from .intent import extract_intent
from .profiles import PROFILES
from .compiler import compile_prompt

__all__ = ["ContextAssembler", "extract_intent", "PROFILES", "compile_prompt"]
