# Environment Variables Architecture

**Document ID:** DEP-007

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the environment variable architecture for the AI Career Interview Platform.

Environment variables provide configuration and secrets without embedding sensitive information in source code.

---

# Objectives

The configuration system must provide:

- Secure secret management
- Environment isolation
- Easy deployment
- Startup validation
- Secret rotation
- CI/CD integration
- Production safety
- Configuration consistency

---

# Design Principles

The platform follows these principles:

- Configuration outside source code
- Secrets never committed to Git
- Environment-specific configuration
- Fail fast on missing configuration
- Least-privilege access
- Immutable runtime configuration
- Explicit validation

---

# Configuration Categories

Environment variables are grouped into:

- Application
- Authentication
- Database
- AI Services
- Storage
- Security
- Logging
- Monitoring
- Deployment
- Feature Flags

---

# Environment Hierarchy

```text
Local

↓

CI

↓

Staging

↓

Production
```

Each environment maintains an independent configuration.

---

# Frontend Variables

Frontend variables are public and **must** begin with the `VITE_` prefix.

Examples

```text
VITE_API_BASE_URL

VITE_GOOGLE_CLIENT_ID

VITE_APP_NAME

VITE_APP_ENV

VITE_ENABLE_ANALYTICS

VITE_ENABLE_DEBUG
```

Frontend variables must never contain secrets.

---

# Backend Variables

Examples

```text
APP_ENV

APP_NAME

APP_VERSION

HOST

PORT
```

---

# Database Variables

```text
DATABASE_URL

DATABASE_POOL_SIZE

DATABASE_MAX_OVERFLOW

DATABASE_TIMEOUT
```

Only the backend accesses these variables.

---

# Authentication Variables

Google OAuth

```text
GOOGLE_CLIENT_ID

GOOGLE_CLIENT_SECRET

GOOGLE_REDIRECT_URI
```

JWT

```text
JWT_SECRET_KEY

JWT_ALGORITHM

JWT_ACCESS_TOKEN_EXPIRE_MINUTES

JWT_REFRESH_TOKEN_EXPIRE_DAYS
```

---

# AI Variables

```text
GROQ_API_KEY

GROQ_MODEL

GROQ_TIMEOUT

GROQ_MAX_RETRIES
```

---

# Object Storage Variables

```text
STORAGE_PROVIDER

STORAGE_BUCKET

STORAGE_ENDPOINT

STORAGE_REGION

STORAGE_ACCESS_KEY

STORAGE_SECRET_KEY
```

---

# Logging Variables

```text
LOG_LEVEL

LOG_FORMAT

ENABLE_REQUEST_LOGGING
```

---

# Monitoring Variables

```text
ENABLE_METRICS

ENABLE_HEALTH_CHECKS

ENABLE_TRACING

ERROR_REPORTING_DSN
```

---

# Security Variables

```text
CORS_ALLOWED_ORIGINS

RATE_LIMIT_PER_MINUTE

ALLOWED_HOSTS

COOKIE_SECURE

COOKIE_SAMESITE
```

---

# Feature Flags

Examples

```text
ENABLE_AI_FEEDBACK

ENABLE_EXPORTS

ENABLE_EXPERIMENTAL_UI

ENABLE_DEBUG_ENDPOINTS
```

Feature flags should default to safe values.

---

# Variable Naming Conventions

Rules

- Use uppercase letters.
- Separate words with underscores.
- Use descriptive names.
- Avoid abbreviations where possible.
- Keep names stable.

Example

```text
DATABASE_CONNECTION_TIMEOUT
```

Avoid

```text
DBT
```

---

# Startup Validation

At application startup verify:

- Required variables exist
- Data types are valid
- URLs are valid
- Numeric values are within limits
- Secrets are not empty

Application startup must fail if validation fails.

---

# Default Values

Allowed for:

- Logging level
- Debug flags
- Feature flags
- Timeouts

Not allowed for:

- API keys
- OAuth secrets
- JWT secrets
- Database credentials

---

# Secret Management

Secrets include:

- API keys
- OAuth credentials
- JWT keys
- Database passwords
- Storage credentials

Secrets must never:

- Be committed to Git
- Be logged
- Be exposed to the frontend
- Be hardcoded

---

# Secret Rotation

Production secrets should support:

- Scheduled rotation
- Emergency rotation
- Immediate revocation
- Audit logging

Rotation should not require source code changes.

---

# Environment Isolation

Every environment has unique:

- Database credentials
- OAuth credentials
- Storage credentials
- JWT secrets
- API keys

Sharing production secrets with other environments is prohibited.

---

# CI/CD Integration

Secrets are injected during deployment.

```text
GitHub

↓

CI Pipeline

↓

Secret Store

↓

Deployment Platform

↓

Application
```

No secret values are stored in repository files.

---

# Local Development

Developers use:

```text
.env.local
```

Example

```text
backend/

.env.local
```

This file must appear in `.gitignore`.

---

# Environment Files

Recommended structure

```text
.env.example

.env.local

.env.ci

.env.staging

.env.production
```

Only `.env.example` should be committed to source control.

---

# .env.example

The example file contains:

- Variable names
- Sample values
- Comments
- Required flags

No real secrets.

Example

```text
DATABASE_URL=postgresql://...

GROQ_API_KEY=your_api_key_here
```

---

# Validation Library

Recommended tools

Backend

- pydantic-settings

Frontend

- Vite environment validation

Centralize validation logic.

---

# Auditing

Audit:

- Missing variables
- Secret rotation
- Configuration changes
- Unauthorized access

Configuration changes should be traceable.

---

# Operational Best Practices

- Validate configuration at startup.
- Separate public and private variables.
- Rotate secrets regularly.
- Maintain `.env.example`.
- Document every configuration item.

---

# Anti-Patterns

Avoid

- Hardcoded credentials
- Committing `.env` files
- Logging secrets
- Sharing production credentials
- Reusing JWT secrets across environments

---

# Business Rules

- Secrets never enter source control.
- Every deployment validates required configuration.
- Frontend variables always use the `VITE_` prefix.
- Production secrets are unique.
- Environment configuration changes require review.

---

# Related Documents

- `backend-deployment.md`
- `frontend-deployment.md`
- `ci-cd-pipeline.md`
- `rollback-strategy.md`
- `monitoring.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial environment variables architecture specification |