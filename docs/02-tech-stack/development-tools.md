# Development Tools

**Document ID:** TS-008

**Version:** 1.0.0

**Status:** Approved

**Priority:** High

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the approved development tools, local development
environment, productivity utilities, debugging tools, testing utilities,
and developer workflows for the AI Career Interview Platform.

Every contributor should use these tools unless an approved Architecture
Decision Record (ADR) specifies an alternative.

---

# Objectives

The development environment should be:

- Consistent
- Reproducible
- Easy to onboard
- Easy to maintain
- Productivity-focused
- Platform independent

---

# Supported Operating Systems

Development is officially supported on:

- Windows 11
- Ubuntu 24.04 LTS
- macOS (latest stable)

All project scripts should work across supported operating systems.

---

# Core Development Tools

| Category | Tool |
|----------|------|
| IDE | Visual Studio Code |
| Version Control | Git |
| Repository Hosting | GitHub |
| API Client | Swagger UI |
| Optional API Client | Postman |
| Database Client | pgAdmin |
| Terminal | PowerShell / Bash |
| Package Manager (Frontend) | npm |
| Package Manager (Backend) | pip |
| Python Environment | venv |

---

# IDE

Recommended IDE:

Visual Studio Code

Recommended extensions:

- Python
- Pylance
- Black Formatter
- Ruff
- ESLint
- Prettier
- Tailwind CSS IntelliSense
- GitLens
- Docker (future)
- Markdown All in One
- Mermaid Preview

---

# Version Control

Git is mandatory.

Repository Hosting:

GitHub

Every change must be committed through Git.

Direct production edits are prohibited.

---

# Branch Strategy

```
main

develop

feature/<feature-name>

bugfix/<bug-name>

hotfix/<issue-name>
```

Rules:

- Never commit directly to `main`
- Feature branches should remain focused
- Merge through Pull Requests
- Resolve conflicts before merging

---

# Python Environment

Use:

```
python -m venv .venv
```

Activate before installing dependencies.

Never install project dependencies globally.

---

# Backend Dependency Installation

```
pip install -r requirements.txt
```

Future:

Dependency locking may be introduced.

---

# Frontend Dependency Installation

```
npm install
```

Use the lock file committed to the repository to ensure reproducible installs.

---

# Code Formatting

Backend

- Black

Frontend

- Prettier

Formatting should be automatic before commits whenever possible.

---

# Linting

Backend

- Ruff

Frontend

- ESLint

Lint errors should be resolved before merging code.

---

# Type Checking

Frontend

TypeScript compiler

Backend

Static typing through Python type hints.

Future consideration:

- mypy

---

# API Testing

Primary tool:

Swagger UI

Optional:

- Postman

API endpoints should remain synchronized with OpenAPI documentation.

---

# Database Tools

Primary:

pgAdmin

Alternative:

psql

Database schema changes must use Alembic migrations.

---

# Logging

Backend logging should use Python's standard logging module.

Log levels:

- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL

Production logging level should default to INFO.

---

# Debugging

Frontend

- Browser Developer Tools
- React Developer Tools

Backend

- VS Code Debugger
- FastAPI Logs

Database

- SQL query inspection
- pgAdmin query tools

---

# Documentation Tools

Primary format:

Markdown

Diagramming:

Mermaid

Documentation should be updated before implementation when introducing
new architecture or behavior.

---

# Testing Tools

Backend

- Pytest

Frontend (Future)

- Vitest
- React Testing Library

Future

- Playwright (End-to-End)

---

# Local Development Workflow

```
Clone Repository

↓

Create Virtual Environment

↓

Install Backend Dependencies

↓

Install Frontend Dependencies

↓

Configure Environment Variables

↓

Run Database Migrations

↓

Start Backend

↓

Start Frontend

↓

Begin Development
```

---

# Pull Request Checklist

Before creating a Pull Request:

- Code compiles successfully
- Tests pass
- Lint checks pass
- Formatting applied
- Documentation updated
- No secrets committed
- Migrations reviewed
- Related issues referenced

---

# Secret Management

Never commit:

- API Keys
- OAuth Secrets
- JWT Secrets
- Database Passwords
- Environment Files

Secrets belong only in environment configuration.

---

# Productivity Recommendations

Developers should:

- Commit frequently
- Write meaningful commit messages
- Keep Pull Requests small
- Update documentation alongside code
- Review generated OpenAPI documentation after API changes

---

# Future Tooling

Potential additions:

- GitHub Actions
- Dependabot
- Renovate
- SonarQube
- Sentry
- Prometheus
- Grafana
- Docker Desktop
- Dev Containers

These tools are intentionally excluded from Version 1 unless project
requirements change.

---

# Related Documents

- `technology-overview.md`
- `deployment-stack.md`
- `coding-standards.md`
- `project-structure.md`
- `environment-management.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial development tools specification |