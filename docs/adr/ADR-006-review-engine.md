# ADR-006: Review Engine — Design Specification

*Status: Draft | Phase: v1.3 (not yet scheduled)*

---

## Context

After Semantic Platform (v1.0), Context Engine (v1.1), and Validation Engine (v1.2) are
stable, the next capability is a **Review Engine** that uses semantic diff to produce
focused, high-quality code reviews.

Unlike generic LLM-based review that dumps the entire diff into context, Review Engine
will:

1. Compute a **semantic diff** (not just text diff) between two code states.
2. Identify only **affected entities** (functions, variables, modules).
3. Attach **graph context** (callers, callees, dependencies).
4. Compute a **risk score** (reuse from Validation Engine).
5. Compile a **targeted review prompt** with minimal token usage.
6. Invoke LLM for reasoning only — not search.

---

## Public Interface

```python
def review(
    diff: dict,           # output of semantic_diff.diff()
    context: dict,        # optional: pre-built context (from ContextAssembler)
    profile: str = "review",  # token budget + focus
    model: str = "",      # optional: LLM model identifier
) -> ReviewResult:
    ...
```

`ReviewResult`:

```json
{
  "status": "CHANGES_DETECTED" | "NO_CHANGES",
  "risk": {"score": 0.0, "level": "LOW", "reasons": []},
  "summary": "...",
  "affected": [
    {"name": "...", "type": "function", "module": "...",
     "changes": ["params: [src] → [src, period]"],
     "impact": {"callers": 3, "callees": 1}}
  ],
  "review_prompt": "...",
  "llm_response": "..."
}
```

---

## Sequence Diagram

```text
User/CI
  │
  ▼
Review Engine
  │
  ├── 1. semantic_diff.diff(baseline, current)   ── pure function
  │
  ├── 2. risk_scorer.assess(diff, [])             ── reuse from v1.2
  │
  ├── 3. Build affected entity list
  │     ├── entity + changes
  │     ├── graph impact (callers, callees)
  │     └── module dependency
  │
  ├── 4. Compile review prompt
  │     ├── affected summary (50 tokens)
  │     ├── change details (200 tokens)
  │     ├── graph context (100 tokens)
  │     └── risk assessment (30 tokens)
  │
  ├── 5. LLM.review(prompt)                      ── first LLM call
  │
  └── 6. Return ReviewResult
```

Key property: **steps 1-4 are deterministic**. Only step 5 invokes an LLM.
This means 90% of the pipeline is testable without a model.

---

## Design Principles

1. **Deterministic first** — semantic diff, risk score, entity analysis, and prompt
   compilation must be pure functions with zero side effects. No LLM until the final step.

2. **Reuse over rewrite** — `semantic_diff.py` (core library), `risk_scorer.py`
   (validation engine), and `profiles.py` (context engine) are shared. The Review Engine
   is a consumer, not a re-implementer.

3. **Token budget is a first-class concern** — the review prompt must fit within the
   profile's budget. The prompt compiler (step 4) is responsible for staying under budget,
   not the LLM.

4. **Model-agnostic** — the public interface accepts `model: str` but defaults to empty,
   meaning the caller decides which model to use. The engine never hardcodes a model
   identifier.

---

## File Structure (future, v1.3)

```
scripts/
  pine_query/
    review/
      __init__.py            ← Public API: review()
      prompt_compiler.py     ← Deterministic: diff + risk → prompt
      review_engine.py       ← Orchestrator
  pine_review.py             ← CLI
```

Estimated 250-400 lines total.

---

## Open Questions (for implementation phase)

1. Should review prompt be markdown or structured JSON?
   → Recommendation: Markdown (human-readable in CI logs).

2. Should Review Engine support `--auto-approve` for LOW risk?
   → Yes, but only when explicitly enabled. Default: manual review.

3. Should Review Engine produce GitHub PR comments?
   → Out of scope for v1.3. That belongs in Automation Platform (v1.5).

---

## Decisions

| Decision | Value |
|----------|-------|
| LLM invocation | Step 5 only (final step) |
| Shared components | `semantic_diff`, `risk_scorer`, profiles |
| Model hardcoding | None. Caller specifies model |
| v1.3 estimate | 250-400 lines + tests |
