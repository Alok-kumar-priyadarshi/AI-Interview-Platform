# Next Task

**Status:** Active

**Priority:** High

**Last Updated:** 2026-07-23

---

# Current Task

## Title

Go live: provision credentials and deploy

---

## Objective

The application is feature-complete for Version 1 and fully verified locally.
The remaining work is operational — provisioning real services and deploying.

Steps:

1. Provision **managed PostgreSQL**, **Google OAuth** credentials (redirect URI
   `https://<frontend>/auth/callback`), a **Groq API key**, and (optional)
   **Cloudflare R2** bucket + keys.
2. Set backend env on Railway (see `backend/.env.example` /
   `docs/08-deployment/environment-variables.md`) and deploy — `railway.toml`
   runs `alembic upgrade head` then Uvicorn.
3. Set `VITE_API_BASE_URL` on Vercel and deploy the frontend.
4. Add the deployed frontend origin to backend `CORS_ALLOWED_ORIGINS`.
5. Smoke-test: OAuth login → resume upload → interview → report + PDF.

---

## Optional follow-ups (post-launch)

- Frontend component tests (Vitest + React Testing Library).
- Monitoring/error reporting (Sentry) — hooks exist via `ERROR_REPORTING_DSN`.
- Background worker (Celery/queue) to make resume/interview/evaluation
  processing asynchronous (currently synchronous per Version 1 scope).
- Rate limiting middleware (documented as future in v1).

---

# Status: FEATURE-COMPLETE (Version 1)

- Backend: 13 API groups, 77 routes, 64 tests, ruff clean, 3 migrations,
  voice (Whisper) + PDF reports.
- Frontend: full SPA, OAuth, charts, voice recording, code-split, builds clean.
- Deployment: Railway + Vercel + GitHub Actions CI configured.

No credentials are committed anywhere; all secrets are env-driven.

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 5.0.0 | 2026-07-23 | Feature-complete; remaining work is go-live/ops |
| 4.0.0 | 2026-07-23 | Frontend build task |
