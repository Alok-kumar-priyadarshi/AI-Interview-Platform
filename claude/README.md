# Claude Operating System (Claude OS)

**Version:** 1.0.0  
**Status:** Active  
**Priority:** Critical

---

# Purpose

This directory contains the operational framework that governs how Claude Code
should understand, implement, maintain, and evolve the AI Career Interview
Platform.

It is **not** application documentation.

It is the development operating system for the project.

Claude should consult this directory before making any architectural,
implementation, or documentation decisions.

---

# Claude Startup Sequence

Every new Claude Code session should follow this exact order.

```
README.md
        ↓
Project Constitution
        ↓
Engineering Principles
        ↓
AI Development Principles
        ↓
Coding Philosophy
        ↓
Project Context
        ↓
Project Documentation
        ↓
Architecture
        ↓
Implementation
```

Never skip a step.

---

# Directory Structure

```
claude/

README.md

constitution/
    project-constitution.md
    engineering-principles.md
    ai-development-principles.md
    coding-philosophy.md

rules/
    ...

workflows/
    build-feature.md
    create-api.md
    create-component.md
    fix-bug.md
    release.md

templates/

prompts/

commands/

checklists/
```

---

# Development Philosophy

This repository follows:

- Documentation First Development
- Context Driven Development
- Architecture Driven Development
- Test Driven Verification
- AI Assisted Development

Implementation is always driven by documentation.

Documentation is the source of truth.

---

# Before Writing Code

Claude must verify:

- Project Constitution reviewed
- Engineering Principles reviewed
- Relevant requirements reviewed
- Architecture reviewed
- API contracts reviewed
- Current context reviewed
- Next task identified

If any item is missing, implementation should stop.

---

# Required Reading Order

## Step 1

Read:

```
docs/README.md
```

or

```
docs/index.md
```

---

## Step 2

Read

```
context/current-state.md
```

---

## Step 3

Read

```
context/next-task.md
```

---

## Step 4

Read relevant documents inside

```
docs/
```

---

## Step 5

Read architecture documents.

---

## Step 6

Begin implementation.

---

# Before Ending a Session

Claude must update

```
context/current-state.md
```

```
context/project-progress.md
```

```
context/session-summary.md
```

```
context/next-task.md
```

```
context/changelog.md
```

---

# Development Rules

Claude shall never:

- Implement undocumented features.
- Skip updating documentation.
- Skip updating context.
- Modify architecture without documentation.
- Introduce technologies outside the approved stack.
- Duplicate business logic.

---

# Priority Order

When conflicts occur, the following precedence applies:

1. Project Constitution
2. Engineering Principles
3. AI Development Principles
4. Coding Philosophy
5. Architecture Decision Records (ADRs)
6. Requirements
7. Architecture
8. API Contracts
9. Workflows
10. Implementation

Higher-priority documents always override lower-priority ones.

---

# Project Lifecycle

```
Requirements
        ↓
Architecture
        ↓
Database
        ↓
API Contracts
        ↓
Frontend
        ↓
Backend
        ↓
AI Integration
        ↓
Testing
        ↓
Deployment
```

Claude should never skip lifecycle stages.

---

# Directory Responsibilities

| Folder | Responsibility |
|----------|----------------|
| constitution | Immutable engineering rules |
| workflows | Standard operating procedures |
| rules | Technology-specific implementation rules |
| templates | Reusable document templates |
| prompts | AI prompts |
| commands | Frequently used implementation commands |
| checklists | Verification before completion |

---

# Definition of Success

A successful implementation satisfies all of the following:

- Requirement implemented
- Acceptance criteria satisfied
- Tests passing
- Documentation updated
- RTM updated
- Context updated
- Changelog updated

Code alone is never considered complete.

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial Claude Operating System README |
