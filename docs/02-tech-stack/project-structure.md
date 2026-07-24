# Project Structure

**Document ID:** TS-009

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the official repository structure, directory ownership,
module boundaries, naming conventions, and organizational principles for the
AI Career Interview Platform.

The repository structure is designed to support:

- Documentation-first development
- Modular architecture
- Scalability
- Maintainability
- Clear ownership
- Easy onboarding

Every file added to the repository must follow the structure defined here.

---

# Repository Principles

The repository should be:

- Predictable
- Modular
- Feature-oriented
- Easy to navigate
- Easy to extend
- Documentation-driven

No directory should exist without a clear responsibility.

---

# Top-Level Repository Structure

```
project-root/

docs/
claude/
context/
planning/
prompts/
assets/
scripts/

frontend/
backend/

database/

tests/

.github/

README.md
LICENSE
.gitignore
```

---

# Directory Responsibilities

## docs/

Contains all project documentation.

Examples:

- Requirements
- Architecture
- Database
- API Contracts
- AI System
- Deployment
- Security
- ADRs

Documentation is the source of truth.

---

## claude/

Contains AI development rules.

Examples:

- Constitution
- Workflows
- Templates
- Prompts
- Commands
- Checklists

This directory is intended for AI-assisted development.

---

## context/

Contains the current development context.

Examples:

- Current State
- Progress
- Next Task
- TODO
- Session Summary
- Changelog

Only active project context belongs here.

---

## planning/

Contains planning artifacts.

Examples:

- Milestones
- Roadmaps
- Release Plans
- Sprint Planning
- Feature Planning

Planning documents should not duplicate requirements.

---

## prompts/

Contains reusable AI prompt templates.

Examples:

- Resume Analysis
- Interview Generation
- Evaluation
- Feedback
- Testing

Prompts should be version-controlled.

---

## assets/

Contains non-code resources.

Examples:

- Images
- Logos
- Icons
- Diagrams
- Mockups

Avoid storing generated build artifacts.

---

## scripts/

Contains utility scripts.

Examples:

- Setup scripts
- Development scripts
- Database scripts
- Maintenance scripts

Scripts should be idempotent whenever possible.

---

## frontend/

Contains the React application.

Responsibilities:

- UI
- Routing
- State Management
- API Integration
- Authentication UI

The frontend must not contain backend business logic.

---

## backend/

Contains the FastAPI application.

Responsibilities:

- APIs
- Business Logic
- Authentication
- AI Integration
- Database Access

The backend owns all application logic.

---

## database/

Contains database-specific resources.

Examples:

- ER diagrams
- Seed data
- SQL utilities
- Migration references

Application code belongs in the backend, not here.

---

## tests/

Contains automated tests.

Structure:

```
tests/

unit/

integration/

api/

ai/

e2e/
```

Tests should mirror the application structure where practical.

---

## .github/

Contains GitHub configuration.

Examples:

- Workflows
- Issue Templates
- Pull Request Templates
- CODEOWNERS

---

# Frontend Structure

```
frontend/

src/

assets/

components/

ui/

shared/

features/

pages/

layouts/

hooks/

contexts/

services/

api/

types/

utils/

constants/

routes/

styles/
```

---

# Feature Organization

Each feature follows the same structure.

Example:

```
features/

interview/

components/

hooks/

services/

types/

utils/
```

Feature modules should remain self-contained.

---

# Backend Structure

```
backend/

app/

api/

core/

config/

models/

schemas/

services/

repositories/

middleware/

dependencies/

auth/

ai/

resume/

interview/

evaluation/

history/

database/

utils/

exceptions/
```

Each module should have a clearly defined responsibility.

---

# Naming Conventions

Directories

```
snake_case
```

Python Files

```
snake_case.py
```

React Components

```
PascalCase.tsx
```

Hooks

```
useSomething.ts
```

Types

```
Something.ts
```

Constants

```
something.ts
```

---

# Module Boundaries

Modules communicate only through well-defined interfaces.

Allowed flow:

```
API

↓

Service

↓

Repository

↓

Database
```

Avoid circular dependencies.

---

# Dependency Rules

Frontend:

```
Page

↓

Feature

↓

Shared

↓

UI
```

Backend:

```
API

↓

Service

↓

Repository

↓

Database
```

Dependencies should always point downward.

---

# Documentation Placement

Architecture documentation:

```
docs/03-architecture/
```

Database documentation:

```
docs/04-database/
```

API documentation:

```
docs/05-api-contracts/
```

AI documentation:

```
docs/06-ai-system/
```

Avoid mixing implementation code with documentation.

---

# Generated Files

Generated artifacts should never be committed unless explicitly required.

Examples:

- Cache
- Temporary files
- Build output
- Virtual environments

---

# File Size Guidelines

Recommendations:

- Source files: keep focused
- Components: one responsibility
- Services: one domain
- Documentation: split by topic

Avoid excessively large files without justification.

---

# Ownership Principles

Each directory should have a clear owner.

Examples:

- Frontend → UI Team
- Backend → API Team
- Database → Backend Team
- Documentation → Entire Team

Ownership improves accountability.

---

# Scalability Guidelines

When introducing a new feature:

1. Create a feature module.
2. Add documentation.
3. Define APIs.
4. Add tests.
5. Update architecture if required.

Never bypass the established structure.

---

# Anti-Patterns

Avoid:

- Circular imports
- Utility dumping grounds
- Mixed responsibilities
- Duplicate documentation
- Business logic in UI
- Database logic in controllers

---

# Future Expansion

The structure is designed to support future additions such as:

- Mobile application
- Admin dashboard
- Background workers
- AI microservices
- Analytics platform
- Plugin system

New modules should integrate without disrupting the existing layout.

---

# Related Documents

- `technology-overview.md`
- `frontend-stack.md`
- `backend-stack.md`
- `coding-standards.md`
- `03-architecture/` (future)

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial project structure specification |