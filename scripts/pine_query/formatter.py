"""Stateless formatters for 4 output formats: json, table, markdown, mermaid."""

import json


def format_json(data) -> str:
    return json.dumps(data, indent=2, default=str)


def _fmt_val(v):
    if isinstance(v, (list, dict)):
        return json.dumps(v, default=str)
    return str(v)


def _table_row(cols, widths):
    return "  " + "  ".join(c.ljust(w) for c, w in zip(cols, widths))


def format_table(result: dict) -> str:
    lines = []
    query_type = result.get("query", "")
    data = result.get("result", {})

    if not data.get("found", True):
        return f"Not found: {data.get('name', '?')}"

    if query_type == "function":
        lines.append(f"Function: {data['name']}")
        lines.append(f"  Module: {data.get('module','?')}")
        lines.append(f"  File: {data.get('file','?')}:{data.get('line','?')}")
        lines.append(f"  Params: {', '.join(data.get('params',[]))}")
        lines.append(f"  Calls: {len(data.get('calls',[]))}")
        for c in data.get("calls", [])[:10]:
            label = c.get("label", c.get("target", "?"))
            lines.append(f"    → {label}  ({c.get('relation','calls')}×{c.get('count',1)})")
        lines.append(f"  Called by: {len(data.get('called_by',[]))}")
        for c in data.get("called_by", [])[:10]:
            label = c.get("label", c.get("source", "?"))
            lines.append(f"    ← {label}  (×{c.get('count',1)})")
        if data.get("reads"):
            lines.append(f"  Reads: {len(data['reads'])} variables")
            for r in data["reads"][:5]:
                lines.append(f"    reads {r.get('label',r.get('variable','?'))}")
        if data.get("writes"):
            lines.append(f"  Writes: {len(data['writes'])} variables")

    elif query_type == "variable":
        lines.append(f"Variable: {data['name']}")
        if data.get("found"):
            lines.append(f"  Module: {data.get('module','?')}")
            lines.append(f"  File: {data.get('file','?')}:{data.get('line','?')}")
            lines.append(f"  Global: {data.get('is_global',False)}")
            if data.get("read_by"):
                lines.append(f"  Read by ({len(data['read_by'])}):")
                for r in data["read_by"][:10]:
                    lines.append(f"    {r.get('label',r['caller'])}")
            if data.get("written_by"):
                lines.append(f"  Written by ({len(data['written_by'])}):")
                for w in data["written_by"][:5]:
                    lines.append(f"    {w.get('label',w['caller'])}")
        else:
            lines.append("  (node exists in graph, no Pine AST declaration)")

    elif query_type == "module":
        lines.append(f"Module: {data['name']}")
        lines.append(f"  File: {data.get('file','?')} ({data.get('size_lines',0)} lines)")
        lines.append(f"  Functions: {data.get('functions',0)}")
        lines.append(f"  Variables: {data.get('variables',0)}")
        if data.get("depends_on"):
            lines.append(f"  Depends on: {', '.join(data['depends_on'])}")
        if data.get("depended_by"):
            lines.append(f"  Depended by: {', '.join(data['depended_by'])}")
        lines.append(f"  Entry calls: {data.get('entry_call_count',0)} total")
        if data.get("entry_callees"):
            lines.append("  Entry calls to top functions:")
            for ec in data["entry_callees"][:10]:
                lines.append(f"    {ec.get('label','?')} (×{ec['count']})")

    elif query_type in ("impact", "callers", "callees"):
        lines.append(f"{query_type.capitalize()}: {data['name']}")
        if query_type == "impact":
            dc = data.get("direct_callers", [])
            lines.append(f"  Direct callers: {len(dc)}")
            for item in dc[:10]:
                label = item.get("label", str(item))
                count = item.get("count", "")
                count_str = f" (×{count})" if count else ""
                lines.append(f"    {label}{count_str}")
            tc = data.get("transitive_callers", [])
            lines.append(f"  Transitive callers: {data.get('transitive_callers_count', len(tc))}")
            for item in tc[:15]:
                if isinstance(item, str):
                    label = item.split("::")[-1].split("_")[-1]
                else:
                    label = item.get("label", str(item))
                lines.append(f"    {label}")
            if data.get("affected_modules"):
                lines.append(f"  Affected modules: {', '.join(data['affected_modules'])}")
            if data.get("affected_alerts"):
                lines.append(f"  Affected alerts: {', '.join(data['affected_alerts'])}")
        elif query_type == "callers":
            items = data.get("callers", [])
            lines.append(f"  Total: {data.get('total', len(items))}")
            for item in items[:20]:
                label = item.get("label", str(item))
                count = item.get("count", "")
                count_str = f" (×{count})" if count else ""
                lines.append(f"    {label}{count_str}")
        else:
            items = data.get("callees", [])
            lines.append(f"  Total: {data.get('total', len(items))}")
            for item in items[:20]:
                label = item.get("label", str(item))
                count = item.get("count", "")
                count_str = f" (×{count})" if count else ""
                lines.append(f"    {label}{count_str}")

    elif query_type == "search":
        lines.append(f"Search [{data.get('mode','substring')}]: {data['pattern']}")
        lines.append(f"  Found: {data['total']}")
        for r in data.get("results", [])[:25]:
            lines.append(f"  [{r['type']:>8}] {r['name']} ({r['module']})")

    elif query_type == "builtin":
        if data.get("found"):
            lines.append(f"Builtin: {data['name']}")
            lines.append(f"  Category: {data.get('category','?')}")
            lines.append(f"  Returns: {data.get('returns','?')}")
            lines.append(f"  {data.get('description','')}")
            if data.get("used_by_modules"):
                lines.append(f"  Used by: {', '.join(data['used_by_modules'])}")
        else:
            lines.append(f"Unknown builtin: {data['name']}")

    elif query_type == "explain":
        lines.append(f"Explain: {data['name']}")
        lines.append(f"  Module: {data.get('module','?')}  File: {data.get('file','?')}:{data.get('line','?')}")
        lines.append(f"  Params: {', '.join(data.get('params',[]))}")
        lines.append(f"  Direct calls: {data.get('direct_calls',0)}  (total: {data.get('total_call_count',0)})")
        lines.append(f"  Called by: {data.get('called_by',0)} ({data.get('unique_callers',0)} unique)")
        lines.append(f"  Reads: {data.get('reads_count',0)}  Writes: {data.get('writes_count',0)}")
        lines.append(f"  Variables: {data.get('variables_total',0)}")
        lines.append(f"  Complexity: {data.get('direct_calls',0) + data.get('called_by',0) + data.get('reads_count',0) + data.get('writes_count',0)}")

    elif query_type == "context":
        lines.append(f"# Context: {data.get('signature','?')}")
        lines.append(f"")
        lines.append(f"**Module:** {data.get('module','?')}  **File:** {data.get('file','?')}:{data.get('line','?')}")
        lines.append(f"")
        lines.append(f"## Source")
        lines.append(f"```pine")
        lines.append(data.get("source", "(no source)"))
        lines.append(f"```")
        lines.append(f"")
        lines.append(f"Called by: {len(data.get('called_by',[]))}")
        for c in data.get("called_by", [])[:10]:
            lines.append(f"- {c.get('label',c['source'])}")
        lines.append(f"Calls: {len(data.get('calls',[]))}")
        for c in data.get("calls", [])[:10]:
            lines.append(f"- {c.get('label',c['target'])}")
        lines.append(f"Reads: {len(data.get('reads',[]))}")
        for r in data.get("reads", [])[:10]:
            lines.append(f"- {r.get('label',r['variable'])}")
        lines.append(f"Writes: {len(data.get('writes',[]))}")
        for w in data.get("writes", [])[:5]:
            lines.append(f"- {w.get('label',w['variable'])}")
        if data.get("affected_modules"):
            lines.append(f"Affected modules: {', '.join(data['affected_modules'])}")

    elif query_type == "stats":
        lines.append(f"=== Project Stats: {data.get('project','?')} ===")
        lines.append(f"")
        n = data.get("nodes", {})
        lines.append(f"Nodes:   {n.get('total',0)} total, {n.get('isolated',0)} isolated ({n.get('isolated_pct',0)}%)")
        e = data.get("edges", {})
        lines.append(f"Edges:   {e.get('total',0)} total ({e.get('calls',0)} calls, {e.get('reads',0)} reads, {e.get('writes',0)} writes)")
        s = data.get("symbols", {})
        lines.append(f"Symbols: {s.get('functions',0)} functions, {s.get('variables',0)} variables, {s.get('modules',0)} modules")
        b = data.get("builtins", {})
        lines.append(f"Builtin: {b.get('total',0)} catalogued, {b.get('unresolved_calls',0)} calls in code")
    else:
        lines.append(json.dumps(data, indent=2, default=str))

    return "\n".join(lines)


def format_markdown(result: dict) -> str:
    data = result.get("result", {})
    name = data.get("name", "?")
    query_type = result.get("query", "")

    if not data.get("found", True):
        return f"# {name}\n\nNot found."

    lines = [f"# {name}\n"]

    if query_type == "function":
        lines.append(f"**Module:** {data.get('module','?')}  ")
        lines.append(f"**File:** `{data.get('file','?')}:{data.get('line','?')}`  ")
        lines.append(f"**Params:** `{', '.join(data.get('params',[]))}`  \n")
        if data.get("calls"):
            lines.append(f"## Calls ({len(data['calls'])})\n")
            for c in data["calls"][:15]:
                lines.append(f"- `{c.get('label',c.get('target','?'))}` (×{c.get('count',1)})")
            lines.append("")
        if data.get("called_by"):
            lines.append(f"## Called By ({len(data['called_by'])})\n")
            for c in data["called_by"][:15]:
                lines.append(f"- `{c.get('label',c.get('source','?'))}` (×{c.get('count',1)})")
            lines.append("")
        if data.get("reads"):
            lines.append(f"## Reads ({len(data['reads'])})\n")
            for r in data["reads"][:10]:
                lines.append(f"- `{r.get('label',r.get('variable','?'))}`")
            lines.append("")
        if data.get("writes"):
            lines.append(f"## Writes ({len(data['writes'])})\n")
            for w in data["writes"][:10]:
                lines.append(f"- `{w.get('label',w.get('variable','?'))}`")

    elif query_type == "explain":
        lines.append(f"**Module:** {data.get('module','?')}  ")
        lines.append(f"**File:** `{data.get('file','?')}:{data.get('line','?')}`  ")
        lines.append(f"**Params:** `{', '.join(data.get('params',[]))}`  \n")
        lines.append(f"| Metric | Value |")
        lines.append(f"|---|---|")
        lines.append(f"| Direct calls | {data.get('direct_calls',0)} ({data.get('total_call_count',0)} total) |")
        lines.append(f"| Called by | {data.get('called_by',0)} ({data.get('unique_callers',0)} unique) |")
        lines.append(f"| Reads | {data.get('reads_count',0)} |")
        lines.append(f"| Writes | {data.get('writes_count',0)} |")
        lines.append(f"| Variables | {data.get('variables_total',0)} |")

    elif query_type == "context":
        lines.append(f"**Module:** {data.get('module','?')}  ")
        lines.append(f"**File:** `{data.get('file','?')}:{data.get('line','?')}`  \n")
        lines.append(f"```pine\n{data.get('source','')}\n```\n")
        if data.get("called_by"):
            lines.append(f"Called by: {', '.join(c.get('label',c['source']) for c in data['called_by'][:10])}")
        if data.get("calls"):
            lines.append(f"  \nCalls: {', '.join(c.get('label',c['target']) for c in data['calls'][:10])}")

    elif query_type == "stats":
        n = data.get("nodes", {})
        e = data.get("edges", {})
        s = data.get("symbols", {})
        lines.append(f"**Project:** {data.get('project','?')}  \n")
        lines.append(f"| Category | Value |")
        lines.append(f"|---|---|")
        lines.append(f"| Nodes | {n.get('total',0)} ({n.get('isolated',0)} isolated, {n.get('isolated_pct',0)}%) |")
        lines.append(f"| Edges | {e.get('total',0)} ({e.get('calls',0)}c/{e.get('reads',0)}r/{e.get('writes',0)}w) |")
        lines.append(f"| Functions | {s.get('functions',0)} |")
        lines.append(f"| Variables | {s.get('variables',0)} |")
        lines.append(f"| Modules | {s.get('modules',0)} |")
        lines.append(f"| Builtins | {data.get('builtins',{}).get('total',0)} catalogued |")

    return "\n".join(lines)


def format_mermaid(result: dict) -> str:
    data = result.get("result", {})
    query_type = result.get("query", "")
    name = data.get("name", "?")

    lines = ["graph TD"]
    added = set()

    def safe_id(text):
        return text.replace("-", "_").replace("::", "_").replace(".", "_")

    def add_edge(src, tgt, label=""):
        sid = safe_id(src)
        tid = safe_id(tgt)
        if src not in added:
            lines.append(f"  {sid}[\"{src.split('::')[-1].split('_')[-1]}\"]")
            added.add(src)
        if tgt not in added:
            lines.append(f"  {tid}[\"{tgt.split('::')[-1].split('_')[-1]}\"]")
            added.add(tgt)
        lbl = f"|{label}|" if label else ""
        lines.append(f"  {sid}{lbl}-->{tid}")

    if query_type in ("function", "callers", "callees"):
        fn_id = None
        if data.get("found"):
            mod = data.get("module", "")
            fn_id = f"src_modules_{mod.replace('-','')}_{name}"
        if fn_id and fn_id not in added:
            lines.append(f"  {safe_id(fn_id)}[\"{name}\"]")
            added.add(fn_id)

        for item in data.get("called_by", data.get("callers", [])):
            src = item.get("source", item.get("caller", ""))
            if src:
                add_edge(src, fn_id) if fn_id else add_edge(src, "unknown")

        for item in data.get("calls", data.get("callees", [])):
            tgt = item.get("target", item.get("callee", ""))
            if tgt:
                add_edge(fn_id, tgt) if fn_id else add_edge("unknown", tgt)

    elif query_type == "impact":
        for item in data.get("direct_callers", []):
            src = item.get("caller", "")
            if src:
                add_edge(src, data.get("node_id", name))
        for tid in data.get("transitive_callers", [])[:15]:
            add_edge(tid, data.get("node_id", name))

    elif query_type == "module":
        mod_id = f"src_modules_{data.get('name','?').replace('-','')}"
        entry_id = f"module::{data.get('name','?')}::entry"
        add_edge(mod_id, entry_id)
        for ec in data.get("entry_callees", [])[:10]:
            add_edge(entry_id, ec.get("target", ""))

    lines.append("")
    return "\n".join(lines)


FORMATTERS = {
    "json": format_json,
    "table": format_table,
    "markdown": format_markdown,
    "mermaid": format_mermaid,
}
