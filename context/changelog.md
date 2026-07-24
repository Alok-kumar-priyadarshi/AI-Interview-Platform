# Project Changelog

**Version:** 1.0.0  
**Status:** Active

---

# Purpose

This document records all significant project changes in chronological order.

Unlike `session-summary.md`, which captures what happened during a development
session, the changelog records **what changed in the project itself**.

It serves as the project's official historical record.

---

# Changelog Format

Each entry should contain:

- Date
- Version (if applicable)
- Category
- Description
- Impact

Example:

```
## 2026-08-01

### Added

- Authentication module

### Changed

- Updated interview evaluation algorithm

### Fixed

- Resume parser incorrectly handled PDFs

### Removed

- Deprecated API endpoint
```

---

# Categories

Use the following categories whenever applicable.

## Added

New features, documents, modules, or capabilities.

Examples:

- New documentation
- New API
- New database tables
- New frontend pages

---

## Changed

Improvements or modifications to existing functionality.

Examples:

- Updated architecture
- Modified API contract
- Improved AI prompts
- Enhanced UI

---

## Fixed

Bug fixes and corrections.

Examples:

- Fixed authentication bug
- Corrected ER diagram
- Fixed API validation

---

## Removed

Deprecated or deleted functionality.

Examples:

- Removed obsolete documentation
- Deleted deprecated endpoint
- Removed unused components

---

## Security

Security-related improvements.

Examples:

- Added OAuth validation
- Hardened API authentication
- Updated dependency versions

---

## Documentation

Major documentation updates.

Examples:

- Completed Architecture documentation
- Added API specifications
- Updated README

---

# Current Project History

---

## 2026-07-23

### Added

- Project Vision
- Project Scope
- Feature List
- User Personas
- User Journey
- User Stories

---

### Added

Requirements documentation:

- Functional Requirements
- Non-Functional Requirements
- Business Rules
- Constraints
- Acceptance Criteria
- Requirement Traceability Matrix

---

### Added

Claude Operating System

- Project Constitution
- Engineering Principles
- AI Development Principles
- Coding Philosophy
- Claude README

---

### Added

Context Management System

- Context README
- Current State
- Next Task
- Project Progress Dashboard
- Session Summary
- Changelog

---

### Documentation

Established a documentation-first development workflow for the AI Career Interview Platform.

Impact:

Future implementation will be driven entirely from project documentation.

---

## 2026-07-23 (later)

### Added

Backend foundation (`backend/`):

- FastAPI application factory, entrypoint, CORS, lifespan
- Centralised `pydantic-settings` configuration with startup validation
- Structured logging (JSON/console) with request-ID correlation
- Async SQLAlchemy 2.0 engine + per-request session management
- Declarative base, UUID/timestamp mixins, constraint naming convention
- Domain exception hierarchy + centralised handlers (standard error envelope)
- Success/error/pagination response schemas
- Request-context / access-logging middleware
- Health endpoints (`/health`, `/health/live`, `/health/ready`, `/health/version`)
- Test harness (in-memory SQLite) + passing health API tests
- `requirements*.txt`, `pyproject.toml`, `.env.example`, `.gitignore`, README

### Documentation

- Corrected stale `context/` trackers: documentation phase is complete;
  implementation (backend-first) has begun.

Impact:

Backend now boots, serves versioned health endpoints, and enforces the
documented response/error contract. Verified via automated tests.

---

## 2026-07-23 (backend build)

### Added

- **Database layer**: 9 SQLAlchemy 2.0 async models (users, resumes,
  candidate_profiles, interviews, interview_questions, interview_answers,
  evaluations, reports, audit_logs) with documented constraints/indexes;
  portable JSONB/INET types; async Alembic env; migrations 0001 (initial) and
  0002 (resume.is_default). Verified upgrade/downgrade.
- **Authentication**: JWT access+refresh, Google OAuth (provider-abstracted),
  `/auth/{google/login,google/callback,refresh,logout,me}`, current-user +
  admin dependencies, audit logging of auth events.
- **Users API**: `/users/me` (GET/PATCH/DELETE) + `/users/me/statistics`.
- **AI layer**: `LLMProvider` abstraction + Groq adapter, versioned prompt
  registry, orchestrator (validate/parse/retry), typed output schemas, and a
  high-level `AIService` (analyze_resume / generate_questions / evaluate_answer
  / generate_report).
- **Resume domain**: storage abstraction (local + S3/R2), PDF/DOCX/TXT text
  extraction, upload→parse→AI candidate-profile pipeline, resume API (7
  endpoints).
- **Tests**: 36 passing (models, security, AI, auth, users, resume). Ruff clean.

### Security

- Injection-guarded prompts; stateless JWT; ownership checks in services;
  append-only audit log; secrets via validated settings only.

Impact: The backend now supports the full authenticated resume-analysis flow
end to end, verified by automated tests.

---

# Version History

| Version | Date | Description |
|----------|------|-------------|
| 1.11.0 | 2026-07-24 | Conversational interview: AI interviewer speaks questions aloud (browser TTS, voice by preference, replay/mute) and candidates answer by voice OR text, switchable per question. New doc ARC-011. |
| 1.10.2 | 2026-07-24 | Fix: OAuth state via signed JWT (no cookie) — resolves "Sign-in failed" caused by the state cookie not surviving the redirect chain on http/localhost. Removed frontend tsconfig `baseUrl` (TS7-deprecated). |
| 1.10.1 | 2026-07-24 | OAuth callback moved to backend → redirects to SPA with tokens in URL fragment. GOOGLE_REDIRECT_URI now points at the backend callback. |
| 1.10.0 | 2026-07-23 | Voice interviews (Whisper), PDF reports, deployment config (Railway/Vercel/CI), frontend charts + voice recording + code-splitting |
| 1.9.0 | 2026-07-23 | Frontend core: Vite+React+TS+Tailwind SPA, OAuth flow, all core pages (builds clean) |
| 1.8.0 | 2026-07-23 | Backend Version 1 complete: history, dashboard, admin APIs (13 API groups, 75 routes, 62 tests) |
| 1.7.0 | 2026-07-23 | Evaluation + reports domain (AI eval pipeline, report aggregation, grading) |
| 1.6.0 | 2026-07-23 | Interview domain (create, AI question generation, delivery, text answers) |
| 1.5.0 | 2026-07-23 | Candidate preferences table + /candidate-profile API |
| 1.4.0 | 2026-07-23 | Resume domain (storage, parsing, AI profile) |
| 1.3.0 | 2026-07-23 | AI layer (provider abstraction, prompts, orchestrator) |
| 1.2.0 | 2026-07-23 | Auth (Google OAuth + JWT) + database layer |
| 1.1.0 | 2026-07-23 | Backend foundation implemented |
| 1.0.0 | 2026-07-23 | Initial project foundation established |

---

# Changelog Rules

The changelog should record only meaningful project changes.

Do **not** include:

- Temporary experiments
- Incomplete work
- Personal notes
- Planning discussions
- Session details

Those belong in:

- `session-summary.md`
- `todo.md`
- `known-issues.md`

---

# Maintenance Guidelines

Update this document whenever:

- A new milestone is completed.
- A new module is introduced.
- A major document is added.
- Architecture changes.
- Database schema changes.
- API contracts change.
- Production features are released.
- Significant bugs are fixed.

Entries should be:

- Accurate
- Concise
- Chronological
- Permanent

Never delete historical entries.

---

# Definition of Complete

A project change is considered complete only when:

- Documentation is updated.
- Relevant context files are updated.
- The changelog entry is recorded.
- The change has been verified.

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial project changelog |