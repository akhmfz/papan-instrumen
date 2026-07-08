#!/usr/bin/env python3
"""extract_ast.py — Parse .pine files with pynescript, produce pine_semantic.json

Stage 1 of the Inject2 pipeline:
1. Parse all .pine files using pynescript's ANTLR-based parser
2. Extract: FunctionDef, Call, Import, Assign nodes
3. Map calls to their parent function (or "top-level" if outside any function)
4. Output: pine_semantic.json

Usage:
    python3 scripts/extract_ast.py [--project-dir /path/to/project]

Dependencies:
    pip install pynescript antlr4-python3-runtime
"""

import json
import sys
import os
import time
from pathlib import Path
from collections import defaultdict

# ── AST node type names from pynescript ──
# These are the node types we care about:
#   FunctionDef: function definition
#   Call:        function/method call
#   Import:      import statement
#   Assign:      variable assignment (including := in Pine)
#   Name:        identifier reference
#   Param:       function parameter

def load_ast(src: str):
    """Parse Pine Script source and return AST tree."""
    from pynescript.ast.builder import PinescriptASTBuilder
    from pynescript.ast.grammar.antlr4.parser import PinescriptParser
    from pynescript.ast.grammar.antlr4.lexer import PinescriptLexer
    from antlr4 import InputStream, CommonTokenStream
    from antlr4.error.ErrorListener import ErrorListener

    class QuietListener(ErrorListener):
        def __init__(self):
            self.errors = []
        def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
            self.errors.append({"line": line, "col": column, "msg": msg})

    errs = QuietListener()
    lexer = PinescriptLexer(InputStream(src))
    parser = PinescriptParser(CommonTokenStream(lexer))
    parser.removeErrorListeners()
    parser.addErrorListener(errs)
    tree = parser.start_script()
    builder = PinescriptASTBuilder()
    ast = builder.visit(tree)
    return ast, errs.errors


def extract_symbols(ast):
    """Walk AST tree and collect functions, calls, imports, assignments.

    Returns dict with:
      - functions: list of {name, params, file, line, col}
      - calls: list of {func_name, args_count, file, line, parent_function}
      - imports: list of {source, symbols, file, line}
      - assigns: list of {target, file, line}
      - top_level_calls: calls outside any function
    """
    result = {
        "functions": [],
        "calls": [],
        "imports": [],
        "variables": [],
        "reads": [],
        "writes": [],
    }

    # Stack of parent function names during traversal
    function_stack = []
    # Track calls by file/line for dedup
    seen_calls = set()
    seen_fns = set()
    seen_imports = set()
    seen_names = set()

    def walk(node, parent_fn=None):
        if node is None:
            return

        node_type = type(node).__name__

        if node_type == "FunctionDef":
            name = getattr(node, "name", None)
            if name and name not in seen_fns:
                seen_fns.add(name)
                params = []
                for p in getattr(node, "args", []) or []:
                    pname = getattr(p, "name", str(p)) if hasattr(p, 'name') else str(p)
                    params.append(str(pname))
                result["functions"].append({
                    "name": name,
                    "params": params,
                    "line": getattr(node, "lineno", 0),
                    "col": getattr(node, "col_offset", 0),
                })
            function_stack.append(name)

        elif node_type == "Call":
            func_expr = getattr(node, "func", None)
            func_name = None
            if func_expr is not None:
                ft = type(func_expr).__name__
                if ft == "Name":
                    func_name = getattr(func_expr, "id", None)
                elif ft == "Attribute":
                    # e.g. ta.rsi(...), request.security(...)
                    attr_name = getattr(func_expr, "attr", None)
                    obj_name = ""
                    obj = getattr(func_expr, "value", None)
                    if obj and type(obj).__name__ == "Name":
                        obj_name = getattr(obj, "id", "")
                    func_name = f"{obj_name}.{attr_name}" if obj_name else attr_name
                else:
                    func_name = str(func_expr)[:60]

            if func_name:
                line = getattr(node, "lineno", 0)
                col = getattr(node, "col_offset", 0)
                dedup_key = (func_name, line, col)
                if dedup_key not in seen_calls:
                    seen_calls.add(dedup_key)
                    args_list = getattr(node, "args", []) or []
                    is_top_level = len(function_stack) == 0
                    call_entry = {
                        "func_name": func_name,
                        "args_count": len(args_list),
                        "line": line,
                        "col": col,
                        "parent_function": function_stack[-1] if function_stack else None,
                        "scope": "module" if is_top_level else "function",
                        "parent": "entry" if is_top_level else function_stack[-1],
                    }
                    result["calls"].append(call_entry)

        elif node_type == "Assign":
            target = getattr(node, "target", None)
            mode = getattr(node, "mode", None)
            type_ann = getattr(node, "type", None)
            tname = getattr(target, "id", None) if target else None
            if tname:
                line = getattr(node, "lineno", 0)
                col = getattr(node, "col_offset", 0)
                dedup_key = ("assign", tname, line)
                if dedup_key not in seen_names:
                    seen_names.add(dedup_key)
                    is_global = type(mode).__name__ == "Var" if mode else False
                    result["variables"].append({
                        "name": tname,
                        "var_type": str(type_ann) if type_ann else "",
                        "is_global": is_global,
                        "line": line,
                        "col": col,
                        "parent_function": function_stack[-1] if function_stack else None,
                    })

        elif node_type == "Name":
            name = getattr(node, "id", None)
            ctx_node = getattr(node, "ctx", None)
            ctx = type(ctx_node).__name__ if ctx_node else "Load"
            if name:
                line = getattr(node, "lineno", 0)
                col = getattr(node, "col_offset", 0)
                dedup_key = (name, line, col, ctx)
                if dedup_key not in seen_names:
                    seen_names.add(dedup_key)
                    entry = {
                        "name": name,
                        "ctx": ctx,
                        "line": line,
                        "col": col,
                        "parent_function": function_stack[-1] if function_stack else None,
                    }
                    if ctx == "Store":
                        result["writes"].append(entry)
                    elif ctx == "Load":
                        result["reads"].append(entry)

        elif node_type == "Import":
            src_attr = getattr(node, "source", None) or getattr(node, "module", None)
            if isinstance(src_attr, list):
                src_attr = ",".join(str(s) for s in src_attr)
            symbols = getattr(node, "symbols", []) or getattr(node, "names", [])
            line = getattr(node, "lineno", 0)
            dedup_key = (str(src_attr), line)
            if dedup_key not in seen_imports:
                seen_imports.add(dedup_key)
                result["imports"].append({
                    "source": str(src_attr) if src_attr else "",
                    "symbols": [str(s) for s in (symbols or [])],
                    "line": line,
                })

        # Recurse into child nodes
        if hasattr(node, '__dict__'):
            for attr_name, attr_val in node.__dict__.items():
                if isinstance(attr_val, list):
                    for item in attr_val:
                        walk(item, parent_fn=function_stack[-1] if function_stack else parent_fn)
                elif attr_val is not None:
                    try:
                        if hasattr(attr_val, '__dict__') or hasattr(attr_val, 'getChildCount'):
                            walk(attr_val, parent_fn=function_stack[-1] if function_stack else parent_fn)
                    except (RecursionError, RuntimeError):
                        pass

        if node_type == "FunctionDef":
            function_stack.pop()

    walk(ast)
    return result


def process_file(filepath: str, module_name: str):
    """Parse a single .pine file and extract symbols."""
    filepath = str(filepath)
    with open(filepath) as f:
        src = f.read()

    t0 = time.time()
    ast, errors = load_ast(src)
    parse_time = time.time() - t0

    symbols = extract_symbols(ast)

    return {
        "module": module_name,
        "file": filepath,
        "size_chars": len(src),
        "size_lines": len(src.splitlines()),
        "parse_time_seconds": round(parse_time, 2),
        "parse_errors": len(errors),
        "parse_error_details": errors[:5] if errors else [],
        **symbols,
    }


def build_cross_references(results):
    """Build cross-file reference index: which functions call which others."""
    # Index all functions by name → list of (module, file)
    fn_index = defaultdict(list)
    for r in results:
        for fn in r["functions"]:
            fn_index[fn["name"]].append({
                "module": r["module"],
                "file": r["file"],
                "line": fn["line"],
                "params": fn["params"],
            })

    # For each call, try to find the callee's definition
    cross_refs = []
    for r in results:
        for call in r["calls"]:
            callee_defs = fn_index.get(call["func_name"], [])
            caller = call.get("parent_function")
            cross_refs.append({
                "caller": caller,
                "callee": call["func_name"],
                "scope": call.get("scope", "function"),
                "parent": call.get("parent", None),
                "callee_definitions": callee_defs,
                "caller_file": r["file"],
                "caller_module": r["module"],
                "caller_line": call["line"],
                "caller_col": call["col"],
                "args_count": call["args_count"],
                "resolved": len(callee_defs) > 0,
            })

    return cross_refs, dict(fn_index)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Extract Pine Script AST symbols")
    parser.add_argument("--project-dir", default=os.getcwd(),
                        help="Project root directory (default: cwd)")
    parser.add_argument("--out", default=None,
                        help="Output path for pine_semantic.json (default: <project-dir>/pine_semantic.json)")
    args = parser.parse_args()

    project_dir = Path(args.project_dir)
    modules_dir = project_dir / "src" / "modules"

    if not modules_dir.exists():
        print(f"Error: no src/modules/ directory in {project_dir}")
        sys.exit(1)

    # Discover .pine files (module files only, skip built/concatenated output)
    pine_files = []
    for pf in sorted((project_dir / "src").rglob("*.pine")):
        rel = str(pf.relative_to(project_dir))
        # Only include files in src/modules/ or src/strategies/
        if rel.startswith("src/modules/") or rel.startswith("src/strategies/"):
            pine_files.append(pf)
        else:
            # Skip built files directly in src/
            print(f"  (skipping built file: {rel})")

    if not pine_files:
        print(f"Error: no .pine files found in {modules_dir}")
        sys.exit(1)

    print(f"Found {len(pine_files)} .pine files")
    for pf in pine_files:
        rel = pf.relative_to(project_dir)
        print(f"  {rel}")

    results = []
    total_t0 = time.time()

    for pf in pine_files:
        module_name = pf.stem.replace(".pine", "")
        print(f"\nParsing {pf.name}...")
        try:
            result = process_file(str(pf), module_name)
            results.append(result)
            status = "✅" if result["parse_errors"] == 0 else "⚠️"
            print(f"  {status} {result['parse_time_seconds']:.1f}s | "
                  f"{len(result['functions'])} fns, {len(result['calls'])} calls, "
                  f"{len(result['variables'])} vars, {len(result['reads'])} reads, "
                  f"{len(result['writes'])} writes, "
                  f"{result['parse_errors']} errors")
        except Exception as e:
            print(f"  ❌ CRASHED: {e}")
            results.append({
                "module": module_name,
                "file": str(pf),
                "error": str(e),
            })

    total_time = time.time() - total_t0

    # Build cross-references
    cross_refs, fn_index = build_cross_references(results)

    # Count resolved vs unresolved calls
    total_calls = len(cross_refs)
    resolved_calls = sum(1 for c in cross_refs if c["resolved"])
    print(f"\nCross-reference: {resolved_calls}/{total_calls} calls resolved")

    # Prepare output
    output = {
        "schema": "1.1",
        "generated_by": "extract_ast.py",
        "pine_version": "v6",
        "parser": "pynescript 0.3.0",
        "project": str(project_dir),
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_time_seconds": round(total_time, 2),
        "file_count": len(results),
        "files": results,
        "cross_references": cross_refs,
        "function_index": {k: v for k, v in fn_index.items()},
        "totals": {
            "functions": sum(len(r.get("functions", [])) for r in results),
            "calls": sum(len(r.get("calls", [])) for r in results),
            "imports": sum(len(r.get("imports", [])) for r in results),
            "variables": sum(len(r.get("variables", [])) for r in results),
            "reads": sum(len(r.get("reads", [])) for r in results),
            "writes": sum(len(r.get("writes", [])) for r in results),
            "internal_calls": resolved_calls,
            "unresolved_calls": total_calls - resolved_calls,
        }
    }

    out_path = args.out or str(project_dir / "pine_semantic.json")
    Path(out_path).write_text(json.dumps(output, indent=2))
    print(f"\nOutput: {out_path}")
    print(f"Total time: {total_time:.1f}s")
    print(f"Totals: {output['totals']}")


if __name__ == "__main__":
    main()
