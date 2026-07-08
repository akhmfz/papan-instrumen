"""PromptCompiler — Context Object + Profile → compiled prompt string.

Pure formatting. No logic, no search, no ranking, no budget.
"""




def _section(title: str, body: str) -> str:
    return f"## {title}\n\n{body}\n"


def _bullet_list(items: list) -> str:
    return "\n".join(f"- {i}" for i in items)


def compile_prompt(context: dict, profile_name: str = "implementation") -> str:
    task = context.get("task", {})
    entities = context.get("entities", [])
    modules = context.get("modules", {})
    profile = task.get("profile", profile_name)
    budget = task.get("budget", 4096)

    lines = []
    lines.append(f"# Context: {context.get('context_title', 'Code Task')}\n")
    lines.append(f"**Profile:** {profile}  |  **Budget:** {budget} tokens  "
                 f"|  **Entities:** {context.get('entity_count', 0)}  "
                 f"|  **Modules:** {context.get('module_count', 0)}\n")

    # Entity list
    if entities:
        body = "| Entity | Type | Module | Score | Reason |\n"
        body += "|---|---|---|---|---|\n"
        for e in entities[:20]:
            body += f"| {e['name']} | {e['type']} | {e.get('module','')} | {e.get('score','')} | {e.get('reason','')} |\n"
        lines.append(_section("Selected Entities", body))

    # Source snippets (profile-dependent, only for top entities)
    if profile != "architecture":
        src_sections = []
        for e in entities[:10]:
            if e.get("type") == "function" and "source" in e.get("metadata", {}):
                src = e["metadata"]["source"]
                if src:
                    src_sections.append(f"### {e['name']} ({e.get('module','')})\n```pine\n{src}\n```")
        if src_sections:
            lines.append(_section("Source Code", "\n\n".join(src_sections)))

    # Dependencies
    deps = []
    for e in entities:
        m = e.get("metadata", {})
        if m.get("calls_count", 0) > 0:
            deps.append(f"{e['name']} → {m['calls_count']} callees")
        if m.get("called_by_count", 0) > 0:
            deps.append(f"{e['name']} ← {m['called_by_count']} callers")
        if m.get("reads_count", 0) > 0:
            deps.append(f"{e['name']} reads {m['reads_count']} variables")
        if m.get("writes_count", 0) > 0:
            deps.append(f"{e['name']} writes {m['writes_count']} variables")
    if deps:
        lines.append(_section("Dependencies", _bullet_list(deps)))

    # Module overview
    if modules:
        body = "| Module | Functions | Lines | Depends On | Entry Calls |\n"
        body += "|---|---|---|---|---|\n"
        for mod_name, mi in sorted(modules.items()):
            body += f"| {mod_name} | {mi.get('functions',0)} | {mi.get('size_lines',0)} | {', '.join(mi.get('depends_on',[]))} | {mi.get('entry_call_count',0)} |\n"
        lines.append(_section("Module Overview", body))

    return "\n".join(lines)


def compile_markdown(context: dict, profile_name: str = "implementation") -> str:
    """Alias for compile_prompt."""
    return compile_prompt(context, profile_name)
