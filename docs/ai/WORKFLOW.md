# WORKFLOW.md

---

Document ID   : AI-004
Document Name : AI WORKFLOW
Version       : 1.1.0
Status        : Active
Owner         : Muhammad Akhmal
Architect     : ChatGPT
Last Updated  : 2026
Review Cycle  : When Workflow Changes

---

# Purpose

Dokumen ini mendefinisikan workflow kolaborasi antara Product Owner dan AI Team dalam proses pengembangan proyek.

Workflow ini bertujuan menjaga konsistensi proses, menghindari tumpang tindih pekerjaan, dan memastikan setiap perubahan memiliki alur yang jelas.

GitHub Repository menjadi satu-satunya sumber kebenaran (Single Source of Truth).

---

# Team Structure

                    Product Owner
                  Muhammad Akhmal
                         │
      ┌──────────────────┼──────────────────┐
      │                  │                  │
      ▼                  ▼                  ▼
Chief Architect    Lead Developer    QA & Research
(ChatGPT)            (Claude)          (Gemini)
      │                  │                  │
      └──────────────────┼──────────────────┘
                         ▼
                 GitHub Repository
              (Single Source of Truth)

---

# Team Responsibilities

## Product Owner

Responsible for:

- Product Vision
- Roadmap
- Sprint Approval
- Merge Decision
- Release Management

---

## Chief Architect (ChatGPT)

Responsible for:

- Software Architecture
- Methodology
- Sprint Planning
- Repository Governance
- Technical Review
- Engineering Decision

Should Avoid:

- Large code implementation unless explicitly requested.

---

## Lead Developer (Claude)

Responsible for:

- Pine Script Development
- Feature Implementation
- Refactoring
- Performance Optimization
- Bug Fixing

Must Provide:

- Change Report
- Commit Message
- Commit Description
- Engineering Notes

Should Avoid:

- Changing project methodology.
- Changing repository architecture.

---

## QA & Research Engineer (Gemini)

Responsible for:

- Research
- Validation
- Regression Testing
- Benchmark Analysis
- Cross Documentation Review

Should Avoid:

- Direct modification of production code.

---

# Development Workflow

Idea

↓

BACKLOG

↓

CURRENT_SPRINT

↓

Architecture Planning

↓

Implementation

↓

Testing

↓

Architecture Review

↓

Documentation Update

↓

Commit

↓

Merge

↓

Release

---

# AI Context Workflow

Before starting any task, every AI contributor must:

1. Read CURRENT_SPRINT.md
2. Read the target source file(s)
3. Focus only on the active task
4. Ignore completed sprint history unless requested
5. Follow repository documentation over chat history

CURRENT_SPRINT.md is the operational context for all AI contributors.

--- 

# Repository Workflow

Planning

↓

Code

↓

Testing

↓

Documentation

↓

Commit

↓

Review

↓

Merge

---

# GitHub Workflow

Issue

↓

Development

↓

Commit

↓

Push

↓

Review

↓

Merge

---

# Golden Rules

1. GitHub Repository is the Single Source of Truth.
2. No Silent Changes.
3. One Sprint, One Goal.
4. All ideas must enter BACKLOG first.
5. Documentation follows implementation.
6. Every completed build updates CHANGELOG.
7. Product Owner has the final decision.

---

# Standard Development Cycle

Every development task should follow this sequence:

Planning

↓

Implementation

↓

Testing

↓

Documentation

↓

Review

↓

Commit

↓

Merge

↓

Release

No stage should be skipped without Product Owner approval.

---

# Deliverables by Role

## ChatGPT

- Sprint Planning
- Architecture Review
- Methodology Review
- Technical Decision
- Repository Governance

---

## Claude

- Pine Script Implementation
- Refactoring
- Bug Fix
- Performance Optimization

Must Deliver:

- Updated Source Code
- Change Report
- Commit Message
- Commit Description
- Engineering Notes

---

## Gemini

- QA Review
- Research
- Regression Validation
- Benchmark Comparison

Must Deliver:

- QA Report
- Findings
- Improvement Suggestions

---

## Product Owner

- Review
- Git Commit
- Merge
- Release
- Sprint Approval

---

# Closing Statement

A well-defined workflow enables consistent collaboration between human and AI contributors.

The objective is not only to write code, but to build maintainable software with a predictable development process.
