# Project Constraints

**Document ID:** DOC-REQ-004
**Constraint Prefix:** CON
**Version:** 1.0.0
**Status:** Draft
**Owner:** Project Architect
**Last Updated:** 2026-07-23

---

# Purpose

This document defines the technical, architectural, operational, and business
constraints that every implementation must respect.

Unlike requirements, constraints limit the design space and prevent
architecture drift.

---

# CON-001 Technology Stack

The approved Version 1 stack is fixed unless an Architecture Decision Record (ADR) approves a change.

## Frontend
- React (Vite)
- TypeScript
- Tailwind CSS

## Backend
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic

## Database
- PostgreSQL

## AI
- Groq API

---

# CON-002 Authentication

- Google OAuth only.
- Email/password authentication is not supported in Version 1.

---

# CON-003 Cost

- Prefer free or open-source software.
- Prefer Groq API wherever applicable.
- Avoid paid infrastructure for Version 1.
- Avoid vendor lock-in.

---

# CON-004 Deployment

- Docker is intentionally excluded from Version 1.
- Frontend and backend must be deployable independently.
- Configuration must use environment variables.
- No hard-coded secrets.

---

# CON-005 Architecture

The project must follow:

- SOLID principles
- Feature-first organization
- Layered architecture
- Dependency Injection
- Repository Pattern
- Strategy Pattern for AI providers

No tightly coupled modules.

---

# CON-006 AI

- All prompts must live in the prompts/ directory.
- Prompt strings must not be hardcoded inside business logic.
- AI providers must be replaceable through an abstraction layer.

---

# CON-007 Documentation

Implementation is forbidden unless:

- Requirement exists
- Feature exists
- API contract exists
- Architecture exists

Documentation is the source of truth.

---

# CON-008 Claude Code

Claude must:

1. Read docs/index.md
2. Read context/current-state.md
3. Read context/next-task.md
4. Continue from recorded state

Before ending every coding session Claude must update:

- current-state.md
- next-task.md
- project-progress.md
- session-summary.md
- changelog.md

---

# CON-009 Security

- JWT authentication
- HTTPS in production
- Validate uploaded files
- Validate API inputs
- Never expose secrets to the frontend

---

# CON-010 Database

- PostgreSQL is the only supported database for Version 1.
- Schema changes require migration scripts.
- Every schema change must update documentation and ER diagrams.

---

# CON-011 Version Control

- Every feature is implemented on a dedicated branch.
- Commit messages should follow Conventional Commits.
- Breaking changes require an ADR.

---

# Constraint Change Process

A constraint may only be modified when:

1. A new ADR is approved.
2. Related documentation is updated.
3. Context files are updated.
4. Migration impact is documented.

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial constraints document |
