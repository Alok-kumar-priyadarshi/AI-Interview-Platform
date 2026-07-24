# Environment Management

**Document ID:** TS-012

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the configuration management strategy for the
AI Career Interview Platform.

It specifies how environment variables, secrets, application settings,
and deployment-specific configurations are managed throughout the software
development lifecycle.

Every environment must remain isolated while sharing the same application code.

---

# Objectives

Configuration management must be:

- Secure
- Reproducible
- Environment-independent
- Easy to maintain
- Easy to validate
- Production-ready

---

# Core Principles

Configuration must follow the following rules:

- Configuration is external to application code.
- Secrets are never committed to version control.
- Every environment is independently configurable.
- Application behavior is controlled through configuration.
- Defaults should be safe.

---

# Supported Environments

The project supports four environments.

```
Development

↓

Testing

↓

Staging

↓

Production
```

Each environment has independent configuration values.

---

# Environment Responsibilities

## Development

Purpose:

Local feature development.

Characteristics:

- Local database
- Debug logging
- Local frontend
- Local backend
- Local AI testing

---

## Testing

Purpose:

Automated tests.

Characteristics:

- Isolated database
- Mock services where appropriate
- Deterministic configuration
- No production credentials

---

## Staging

Purpose:

Pre-production validation.

Characteristics:

- Production-like infrastructure
- Real integrations where practical
- Limited access
- Release verification

---

## Production

Purpose:

End users.

Characteristics:

- Managed infrastructure
- Secure configuration
- Monitoring enabled
- Optimized logging
- Restricted access

---

# Environment Variables

Configuration should be loaded from environment variables.

Example:

```
APP_ENV

DATABASE_URL

GROQ_API_KEY

GOOGLE_CLIENT_ID

GOOGLE_CLIENT_SECRET

JWT_SECRET

JWT_ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES

BACKEND_URL

FRONTEND_URL

ALLOWED_ORIGINS

LOG_LEVEL
```

---

# Configuration Loading

Backend configuration should be centralized.

Example:

```
backend/

app/

core/

config.py
```

Configuration should be loaded once during application startup.

---

# Configuration Validation

Application startup must validate:

- Required variables exist.
- Data types are correct.
- URLs are valid.
- Secrets are present.
- Numeric values are within acceptable ranges.

Startup should fail immediately if critical configuration is invalid.

---

# Secret Management

Secrets include:

- API keys
- OAuth credentials
- JWT secrets
- Database passwords
- Encryption keys

Rules:

- Never commit secrets.
- Never hardcode secrets.
- Never log secrets.
- Rotate secrets periodically.

---

# .env Files

Development may use:

```
.env
```

Example repository layout:

```
.env.example

.env.local

.env.test

.env.production
```

Only `.env.example` should be committed.

Actual `.env` files must be excluded using `.gitignore`.

---

# .env.example

The repository should provide a template containing variable names only.

Example:

```
APP_ENV=

DATABASE_URL=

GROQ_API_KEY=

GOOGLE_CLIENT_ID=

GOOGLE_CLIENT_SECRET=

JWT_SECRET=

FRONTEND_URL=

BACKEND_URL=
```

No real values should ever appear in this file.

---

# Environment Isolation

Every environment must have:

- Independent database
- Independent secrets
- Independent OAuth credentials
- Independent logging configuration
- Independent deployment

Production resources must never be reused for development.

---

# Frontend Configuration

Frontend configuration should expose only values safe for client-side use.

Examples:

```
VITE_API_BASE_URL

VITE_GOOGLE_CLIENT_ID
```

Sensitive values must never be included in frontend environment variables.

---

# Backend Configuration

Backend configuration includes:

- Database credentials
- OAuth secrets
- JWT configuration
- AI provider credentials
- Logging
- CORS
- Feature flags

These values remain server-side only.

---

# Configuration Access

Application code should never read environment variables directly.

Instead:

```
Environment

↓

Configuration Loader

↓

Validated Settings Object

↓

Application
```

This provides:

- Validation
- Type safety
- Centralized management

---

# Feature Flags

Future versions may introduce feature flags.

Examples:

```
ENABLE_VOICE_INTERVIEW

ENABLE_EXPERIMENTAL_AI

ENABLE_ANALYTICS
```

Feature flags should default to disabled.

---

# Logging Configuration

Configuration controls:

- Log level
- Log destination
- Debug mode

Development:

```
DEBUG
```

Production:

```
INFO
```

Sensitive information must never be written to logs.

---

# CORS Configuration

Allowed origins should be configurable.

Example:

Development

```
http://localhost:5173
```

Production

```
https://interviewer.example.com
```

Avoid wildcard origins in production.

---

# AI Configuration

Configurable values:

- Model name
- Temperature
- Maximum tokens
- Timeout
- Retry count

Changing AI behavior should not require code changes.

---

# Database Configuration

Configuration includes:

- Connection URL
- Pool size
- Timeout
- SSL mode

Production databases should enforce encrypted connections.

---

# Deployment Platform Configuration

Deployment platforms should manage secrets using built-in secret managers.

Examples:

- Railway Variables
- Vercel Environment Variables
- GitHub Repository Secrets (CI/CD)

Avoid storing secrets in deployment scripts.

---

# Backup of Configuration

Maintain secure backups of:

- Production environment variables
- OAuth credentials
- AI credentials
- Deployment settings

Access should be restricted to authorized maintainers.

---

# Operational Checklist

Before deployment:

- Environment variables verified
- Secrets present
- OAuth configuration validated
- Database connectivity confirmed
- AI credentials tested
- Health endpoint verified

---

# Future Enhancements

Potential additions:

- HashiCorp Vault
- AWS Secrets Manager
- Azure Key Vault
- Google Secret Manager
- Dynamic configuration service

These are intentionally excluded from Version 1.

---

# Related Documents

- `deployment-stack.md`
- `authentication.md`
- `development-tools.md`
- `backend-stack.md`
- `07-security/` (future)

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial environment management specification |