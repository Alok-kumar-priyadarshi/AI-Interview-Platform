# Project Constitution

**Document ID:** CLAUDE-CON-001
**Version:** 1.0.0
**Status:** Active
**Priority:** Highest
**Last Updated:** 2026-07-23

---

# Purpose

This constitution defines the immutable engineering principles for the AI Career
Interview Platform. Every implementation, refactor, or architectural change
must comply with these rules unless superseded by an approved Architecture
Decision Record (ADR).

---

# Article 1 — Documentation First

1. No feature shall be implemented without a corresponding requirement.
2. Documentation is the source of truth.
3. Code must never intentionally diverge from approved documentation.
4. Any design change must be documented before implementation.

---

# Article 2 — Approved Technology Stack

The Version 1 stack is fixed:

- Frontend: React + Vite + TypeScript + Tailwind CSS
- Backend: FastAPI
- ORM: SQLAlchemy
- Database: PostgreSQL
- AI Provider: Groq
- Authentication: Google OAuth

Technology changes require an ADR.

---

# Article 3 — Architecture Principles

The system shall:

- Follow SOLID principles.
- Use modular, feature-oriented organization.
- Prefer dependency injection.
- Keep business logic independent of UI.
- Keep AI provider implementations behind abstractions.

---

# Article 4 — Development Workflow

Before coding:

1. Read docs/index.md.
2. Read relevant requirements.
3. Read architecture documentation.
4. Read context/current-state.md.
5. Read context/next-task.md.

After coding:

1. Update documentation.
2. Update context.
3. Update changelog.
4. Record the next task.
5. Verify acceptance criteria.

---

# Article 5 — API Governance

- Every endpoint requires an API contract.
- Request and response models must be documented.
- Breaking API changes require review and an ADR.

---

# Article 6 — Database Governance

- Database changes require migrations.
- Schema documentation must remain synchronized.
- ER diagrams must be updated after schema changes.

---

# Article 7 — Security

- Never expose secrets.
- Validate all external input.
- Enforce authentication and authorization.
- Use HTTPS in production.

---

# Article 8 — Quality

A feature is complete only if:

- Requirements satisfied
- Acceptance criteria passed
- Tests written
- Documentation updated
- Context updated
- Changelog updated

---

# Article 9 — Project Consistency

- Reuse existing modules before creating new ones.
- Avoid duplicate logic.
- Prefer composition over inheritance when practical.
- Keep naming conventions consistent across the project.

---

# Article 10 — Architecture Decisions

Significant changes involving technologies, deployment, database design,
authentication, or AI providers require a documented ADR before implementation.

---

# Compliance Checklist

Before merging any feature:

- [ ] Requirement exists
- [ ] User story mapped
- [ ] API documented
- [ ] Architecture updated
- [ ] Tests added
- [ ] Documentation updated
- [ ] Context updated
- [ ] RTM updated

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial project constitution |
