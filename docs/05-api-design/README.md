# API Design

**Document ID:** API-000

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This directory defines the complete REST API specification for the AI Career
Interview Platform.

The API layer is responsible for exposing secure, predictable, versioned,
well-documented interfaces between the frontend, backend services, AI
components, and external integrations.

This documentation acts as the single source of truth for API development.

---

# Objectives

The API architecture should provide:

- Consistent endpoint design
- Secure authentication
- Predictable request/response formats
- Clear error handling
- High performance
- Version compatibility
- Easy frontend integration
- Extensibility

---

# API Style

The platform follows:

- REST Architecture
- Resource-oriented URLs
- Stateless requests
- JSON payloads
- HTTPS only

Future versions may expose GraphQL for analytics without replacing REST.

---

# Base URL

Development

```
http://localhost:8000/api/v1
```

Production

```
https://api.interviewai.com/api/v1
```

Every endpoint belongs to a versioned namespace.

---

# Versioning Strategy

Current version

```
v1
```

Example

```
GET /api/v1/users/me
```

Future versions

```
v2

v3
```

Breaking changes require a new API version.

Non-breaking additions remain within the current version.

---

# Authentication

Authentication uses:

```
Google OAuth

↓

JWT Access Token

↓

Bearer Authentication
```

Example

```
Authorization:

Bearer <access_token>
```

Every protected endpoint validates the JWT.

---

# API Categories

The API is organized into the following groups:

```
Authentication

Users

Candidate Profile

Resume

Interview

Questions

Answers

Evaluation

Reports

History

Dashboard

Admin

System

Health
```

Each category has its own documentation.

---

# HTTP Methods

Supported methods

| Method | Purpose |
|---------|----------|
| GET | Retrieve resource |
| POST | Create resource |
| PUT | Replace resource |
| PATCH | Partial update |
| DELETE | Remove resource |

---

# Request Format

Example

```json
{
  "difficulty": "medium",
  "interview_type": "technical"
}
```

Request bodies use:

```
application/json
```

File uploads use:

```
multipart/form-data
```

---

# Response Format

Successful responses follow:

```json
{
  "success": true,
  "message": "Interview created successfully.",
  "data": {}
}
```

---

# Error Format

Every error follows one structure.

Example

```json
{
  "success": false,
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Interview does not exist."
  }
}
```

This format must remain consistent across all endpoints.

---

# HTTP Status Codes

| Code | Meaning |
|------|----------|
| 200 | Success |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 422 | Validation Error |
| 429 | Rate Limited |
| 500 | Internal Server Error |

---

# Pagination

Collection endpoints support pagination.

Example

```
GET /interviews?page=1&page_size=20
```

Response

```json
{
  "page": 1,
  "page_size": 20,
  "total": 84,
  "items": []
}
```

Future versions may support cursor pagination.

---

# Filtering

Example

```
GET /reports?difficulty=hard
```

Multiple filters may be combined.

---

# Sorting

Example

```
GET /interviews?sort=created_at
```

Descending

```
GET /interviews?sort=-created_at
```

---

# Idempotency

The following operations should be idempotent:

- Resume upload retry
- Report generation retry
- Evaluation retry

Creation endpoints that may be retried should support an idempotency key.

Header

```
Idempotency-Key
```

---

# Rate Limiting

Example defaults

Authenticated

```
100 requests/minute
```

Unauthenticated

```
20 requests/minute
```

Future versions may implement adaptive rate limiting.

---

# Validation

Validation occurs at three levels.

1. Client

↓

2. FastAPI/Pydantic

↓

3. Database Constraints

Validation errors always return HTTP 422.

---

# Security

Every endpoint must enforce:

- HTTPS
- JWT validation
- Input validation
- Output encoding
- SQL injection protection
- XSS protection
- CSRF protection where applicable

---

# API Documentation

All endpoints are automatically documented using:

```
OpenAPI 3.1
```

FastAPI generates:

- Swagger UI
- OpenAPI JSON
- ReDoc

Documentation must remain synchronized with implementation.

---

# API Lifecycle

```
Requirement

↓

Design

↓

Implementation

↓

Testing

↓

Documentation

↓

Deployment

↓

Monitoring
```

---

# Naming Conventions

Resources

```
Plural

/users

/interviews

/reports
```

Path parameters

```
/users/{user_id}
```

Query parameters

```
snake_case
```

JSON fields

```
snake_case
```

---

# Design Principles

- REST-first
- Stateless
- Versioned
- Predictable
- Secure
- Documentation-first
- Backward compatible where possible

---

# Directory Structure

```
05-api-design/

README.md

authentication.md

users.md

candidate-profile.md

resume.md

interviews.md

questions.md

answers.md

evaluations.md

reports.md

history.md

dashboard.md

admin.md

health.md

errors.md

pagination.md

webhooks.md (future)
```

---

# Related Documents

- `../03-architecture/system-architecture.md`
- `../04-database/schema-overview.md`
- `../04-database/transactions.md`
- `../04-database/governance.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial API architecture overview |