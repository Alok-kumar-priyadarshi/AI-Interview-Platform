# Context Management System

**Version:** 1.0.0  
**Status:** Active  
**Priority:** Critical

---

# Purpose

The Context System preserves the current state of the project between Claude Code
sessions.

Unlike documentation, which describes the project, the Context System records
the project's current progress.

Every implementation session must begin by reading the Context folder and end by
updating it.

The Context folder is the project's working memory.

---

# Philosophy

Documentation answers:

> "How is the project designed?"

Context answers:

> "What is happening right now?"

Never confuse these two responsibilities.

---

# Directory Structure

```
context/

README.md

current-state.md
next-task.md
project-progress.md
session-summary.md
changelog.md
known-issues.md
todo.md
```

---

# File Responsibilities

## current-state.md

Contains the current implementation state.

Examples:

- Current feature
- Current branch
- Current milestone
- Current architecture status
- Last completed task

Update:

Every coding session.

---

## next-task.md

Contains exactly one recommended next task.

It should include:

- Objective
- Files to modify
- Dependencies
- Acceptance criteria

Update:

Every coding session.

---

## project-progress.md

Tracks overall completion.

Example:

```
Requirements        ██████████ 100%

Architecture        ██░░░░░░░░ 20%

Database            ░░░░░░░░░░ 0%

Backend             ░░░░░░░░░░ 0%

Frontend            ░░░░░░░░░░ 0%
```

Update whenever major milestones change.

---

## session-summary.md

Summarize the latest Claude session.

Include:

- Work completed
- Decisions made
- Files changed
- Remaining work

Keep summaries concise.

---

## changelog.md

Chronological project history.

Example:

```
2026-07-23

Added Authentication API

Updated ER Diagram

Created Interview Module
```

Never delete history.

---

## known-issues.md

Tracks:

- Bugs
- Technical debt
- Known limitations
- Planned refactors

Each issue should contain:

- Description
- Severity
- Status
- Planned resolution

---

## todo.md

Master implementation backlog.

Tasks should be grouped by module.

Example:

Authentication

- OAuth callback

Resume

- Parser

Interview

- Question generation

Evaluation

- Scoring engine

---

# Claude Startup Workflow

Before implementation read:

1.

```
current-state.md
```

2.

```
next-task.md
```

3.

```
project-progress.md
```

4.

Relevant documentation.

Only then begin implementation.

---

# Claude Shutdown Workflow

Before ending every coding session update:

- current-state.md
- next-task.md
- project-progress.md
- session-summary.md
- changelog.md

Update known-issues.md if applicable.

---

# Context Rules

Context files should:

- Be concise
- Be factual
- Never duplicate documentation
- Reflect only the current state
- Be updated immediately after implementation

---

# Relationship with Documentation

| Documentation | Context |
|--------------|---------|
| Long-term knowledge | Current working state |
| Architecture | Active implementation |
| Requirements | Current progress |
| Stable | Frequently updated |

---

# Definition of Complete

A Claude session is complete only when:

- Code committed (if applicable)
- Documentation updated
- RTM updated
- Context updated
- Next task recorded

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial Context Management System |