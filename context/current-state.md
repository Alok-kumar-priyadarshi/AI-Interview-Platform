# Current Project State

**Version:** 1.0.0  
**Status:** Active  
**Last Updated:** 2026-07-23

---

# Purpose

This document represents the current snapshot of the project.

It should always answer one question:

> **"If a new Claude session starts right now, what is the exact state of the project?"**

This file should remain concise, factual, and up-to-date.

---

# Current Phase

## Active Phase

Implementation Phase — Backend

---

## Current Milestone

Milestone 5 — Backend Development

Status:

🟡 In Progress

> Note: The `context/` trackers were previously stale — they described the
> project as still being in the Documentation Phase. In reality the entire
> `docs/` tree (project, requirements, tech-stack, architecture, database,
> API design, security, testing, deployment) is complete, and backend
> implementation has begun. Trackers corrected on 2026-07-23.

---

# Current Objective

Build the complete FastAPI backend from the documentation (backend-first),
following the layered architecture: API → Service → Repository → Database.

Current focus:

- Backend foundation (done)
- Database layer (next)
- Authentication, services, AI, API routers, tests

---

# Recently Completed

✅ All documentation (`docs/` — 9 categories, complete)

✅ Claude Operating System + Context System

✅ Backend foundation:

- Project structure (`backend/app/…`) per project-structure.md
- Centralised config (`pydantic-settings`, startup validation)
- Structured JSON/console logging with request-ID correlation
- Async SQLAlchemy 2.0 engine + session management (asyncpg)
- Declarative base + UUID/timestamp mixins + constraint naming
- Domain exception hierarchy + centralised handlers (standard error envelope)
- Standard success/error/pagination response schemas
- Request-context + access-logging middleware
- Application factory (`app.main`) with CORS, lifespan, OpenAPI
- Health endpoints (`/health`, `/live`, `/ready`, `/version`)
- Test harness (in-memory SQLite) + passing health API tests

---

# Currently Working On

Backend implementation — Database layer (SQLAlchemy models + Alembic).

---

# Next Immediate Task

See `context/next-task.md` — implement the database layer (all 9 entity models,
Alembic environment, initial migration).

---

# Current Architecture Status

| Area | Status |
|--------|--------|
| Requirements | ✅ Complete |
| Constitution | ✅ Complete |
| Context System | ✅ Complete |
| Architecture (docs) | ✅ Complete |
| Database Design (docs) | ✅ Complete |
| API Contracts (docs) | ✅ Complete |
| Security (docs) | ✅ Complete |
| Testing (docs) | ✅ Complete |
| Deployment (docs) | ✅ Complete |
| Backend — Foundation | ✅ Complete |
| Backend — Database Layer | ✅ Complete (10 models, Alembic, 3 migrations) |
| Backend — Auth | ✅ Complete (Google OAuth + JWT, users API, audit) |
| Backend — AI Layer | ✅ Complete (provider abstraction, Groq, prompts, orchestrator) |
| Backend — Resume Domain | ✅ Complete |
| Backend — Candidate Preferences | ✅ Complete (/candidate-profile) |
| Backend — Interview Domain | ✅ Complete (create, AI questions, delivery, text answers) |
| Backend — Evaluation + Reports | ✅ Complete (AI eval pipeline, report aggregation, grading) |
| Backend — History / Dashboard / Admin | ✅ Complete |
| **Backend — VERSION 1 COMPLETE** | ✅ 13 API groups · 77 routes · voice + PDF |
| **Frontend — COMPLETE** | ✅ React 19 + Vite + TS + Tailwind; charts + voice; code-split |
| **Deployment config** | ✅ Railway (backend) · Vercel (frontend) · GitHub Actions CI |

**Backend tests:** 64 passing (unit + api) on in-memory SQLite. Ruff clean.
**Backend build:** `create_app()` loads all routers; OpenAPI schema generates.
**Frontend build:** `npm run build` passes (tsc strict + Vite; route-split bundles).

## Completed since backend V1

- **Voice interviews**: Groq Whisper transcription in the AI layer, audio
  storage, `POST /interviews/{id}/answers/voice` + `/transcript`.
- **PDF reports**: reportlab generation on report creation; `/download` streams
  the PDF (`application/pdf`).
- **Deployment**: `backend/railway.toml` + `Procfile` (+ Alembic on deploy),
  `frontend/vercel.json`, `.github/workflows/ci.yml`, root `README.md`.
- **Frontend polish**: Recharts performance-trend chart on the dashboard,
  in-browser voice recording (MediaRecorder) for voice interviews, and
  lazy-loaded routes.
- **Conversational interview** (ARC-011): the AI interviewer **speaks** each
  question aloud (browser SpeechSynthesis), greets the candidate, honours the
  preferred voice, and offers replay/mute; candidates answer by **voice or
  text, switchable per question**. `useSpeech` hook + `InterviewerPanel`.
- **OAuth**: signed-JWT state (cookieless); backend callback → SPA fragment.

## Frontend implemented

Auth (Google OAuth flow + token refresh interceptor), protected routes, nav
layout, reusable UI + state components, typed Axios API layer, and pages:
Login, OAuth callback, Dashboard, Resume (upload/list/default/delete),
Interviews (list), New interview, Interview run (start→answer→complete),
Report, History, Profile (name + preferences), 404.

## Flagged documentation conflicts (awaiting product decision)

1. **Refresh tokens** — ARC-007 says v1 has none; API-001 + env-vars define them.
   Implemented the superset (refresh tokens) per the API contract.
2. **`/candidate-profile` API vs DB `candidate_profiles`** — RESOLVED (user
   decision): added a dedicated `candidate_preferences` table (migration 0003)
   for the user-owned preferences profile, exposed at `/candidate-profile`
   (GET/POST/PATCH/DELETE). The resume-derived AI profile remains at
   `GET /resumes/{id}/metadata`. Two distinct entities, cleanly separated.
3. **Resume `is_default`** — required by the API, absent from the schema. Added
   via migration 0002 (documented).
4. **Resume global-unique checksum vs "users may upload duplicates"** — kept the
   documented unique constraint; duplicate uploads return 409.

---

# Current Approved Technology Stack

## Frontend

- React
- Vite
- TypeScript
- Tailwind CSS

---

## Backend

- FastAPI

---

## ORM

- SQLAlchemy

---

## Database

- PostgreSQL

---

## AI

- Groq API

---

## Authentication

- Google OAuth

---

# Current Folder Status

## Completed

```
docs/
```

```
claude/
```

```
context/
```

Structure established.

---

# Architecture Decision Status

Architecture Decision Records:

Not started.

---

# Blockers

Current blockers:

None.

---

# Known Risks

- Documentation must remain synchronized.
- Architecture should not begin before Context System is completed.
- Avoid introducing undocumented features.

---

# Notes for Next Claude Session

Before continuing:

1.

Read

```
claude/README.md
```

2.

Read

```
context/README.md
```

3.

Read

```
current-state.md
```

4.

Continue with

```
next-task.md
```

---

# Definition of "Current"

This file should always represent the latest project state.

It must never contain historical information.

Historical information belongs in:

```
changelog.md
```

or

```
session-summary.md
```

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial current project state |