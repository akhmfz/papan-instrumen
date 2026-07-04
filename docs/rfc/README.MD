# Request for Comments (RFC)

## Purpose

RFC (Request for Comments) is the official proposal process for introducing significant changes to the **Saham: Papan Instrumen By. Akhmfz** project.

RFCs ensure that architectural decisions, major features, and workflow changes are discussed, documented, reviewed, and approved before implementation.

---

# When is an RFC Required?

An RFC MUST be created for:

- New architecture
- New scoring methodology
- New dashboard layout
- New data source
- Major refactoring
- Breaking changes
- Performance optimization affecting core logic
- Multi-module changes

RFC is NOT required for:

- Bug fixes
- Documentation updates
- Minor UI adjustments
- Typo corrections
- Internal code cleanup without behavior changes

---

# RFC Lifecycle

```text
Draft
    ↓
Review
    ↓
Accepted
    ↓
Implementing
    ↓
Completed
```

Additional states:

```
Rejected
Deferred
Superseded
```

---

# RFC Naming

```
RFC-001-Sector-Aware-Scoring.md
RFC-002-Performance-Optimization.md
RFC-003-Dashboard-Layout-v2.md
```

---

# Directory

```
docs/
└── rfc/
```

All RFC documents MUST be stored here.

---

# Responsibilities

## Architect

- Create RFC
- Design solution
- Define scope
- Review implementation
- Approve or reject

## Developer

- Read RFC
- Ask questions if needed
- Implement exactly as specified
- Report issues during implementation

---

# Workflow

Idea

↓

Backlog

↓

RFC

↓

Architecture Review

↓

Accepted

↓

Implementation

↓

Code Review

↓

Merge

↓

Release

---

# Principles

- Documentation First
- Architecture Before Code
- No Silent Changes
- Backward Compatibility First
- One RFC = One Major Change

---

# Version

Applies starting from:

v0.1.1
