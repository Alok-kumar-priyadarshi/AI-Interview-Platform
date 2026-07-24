# Global Error Handling API

**Document ID:** API-014

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the standardized error handling strategy used across every API in the AI Career Interview Platform.

Goals:

- Consistent error responses
- Predictable HTTP status codes
- Machine-readable error codes
- Human-readable error messages
- Traceability using correlation IDs
- Secure error reporting
- Simplified frontend integration

Every API must follow this specification.

---

# Standard Error Response

Every failed request returns:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "One or more validation errors occurred.",
    "details": [
      {
        "field": "email",
        "message": "Email is invalid."
      }
    ]
  },
  "request_id": "req_7bfb95b0d6f649d9"
}
```

---

# Response Fields

| Field | Description |
|---------|-------------|
| success | Always false |
| error.code | Machine-readable error identifier |
| error.message | Human-readable summary |
| error.details | Optional validation details |
| request_id | Correlation ID for debugging |

---

# HTTP Status Mapping

| Status | Meaning |
|---------|----------|
| 200 | Success |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 413 | Payload Too Large |
| 415 | Unsupported Media Type |
| 422 | Validation Error |
| 429 | Too Many Requests |
| 500 | Internal Server Error |
| 502 | Bad Gateway |
| 503 | Service Unavailable |
| 504 | Gateway Timeout |

---

# Error Categories

Application errors belong to one of the following groups:

- Authentication
- Authorization
- Validation
- Resource
- Business Rules
- Database
- AI Services
- Storage
- Rate Limiting
- Infrastructure

---

# Authentication Errors

Example

```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required."
  },
  "request_id": "req_123"
}
```

Possible Codes

```
UNAUTHORIZED

INVALID_TOKEN

TOKEN_EXPIRED

TOKEN_REVOKED

LOGIN_REQUIRED
```

---

# Authorization Errors

```json
{
  "success": false,
  "error": {
    "code": "FORBIDDEN",
    "message": "Access denied."
  },
  "request_id": "req_456"
}
```

Possible Codes

```
FORBIDDEN

INSUFFICIENT_PERMISSION

ADMIN_REQUIRED
```

---

# Validation Errors

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed.",
    "details": [
      {
        "field": "resume",
        "message": "Unsupported file type."
      }
    ]
  },
  "request_id": "req_789"
}
```

---

# Resource Errors

Common Codes

```
USER_NOT_FOUND

RESUME_NOT_FOUND

INTERVIEW_NOT_FOUND

QUESTION_NOT_FOUND

ANSWER_NOT_FOUND

EVALUATION_NOT_FOUND

REPORT_NOT_FOUND

HISTORY_NOT_FOUND
```

---

# Business Rule Errors

Examples

```
PROFILE_EXISTS

ANSWER_ALREADY_EXISTS

INTERVIEW_NOT_READY

INVALID_INTERVIEW_STATE

QUESTION_LOCKED

PDF_NOT_READY
```

---

# AI Service Errors

Possible Codes

```
LLM_TIMEOUT

LLM_UNAVAILABLE

PROMPT_GENERATION_FAILED

EVALUATION_FAILED

TRANSCRIPTION_FAILED
```

Example

```json
{
  "success": false,
  "error": {
    "code": "LLM_TIMEOUT",
    "message": "The AI service did not respond within the timeout."
  },
  "request_id": "req_ai_001"
}
```

---

# Database Errors

Possible Codes

```
DATABASE_ERROR

DATABASE_TIMEOUT

TRANSACTION_FAILED

CONSTRAINT_VIOLATION
```

---

# Storage Errors

Possible Codes

```
FILE_TOO_LARGE

UNSUPPORTED_FILE

FILE_UPLOAD_FAILED

FILE_NOT_FOUND

STORAGE_UNAVAILABLE
```

---

# Rate Limiting

HTTP Status

```
429 Too Many Requests
```

Response

```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please try again later."
  },
  "request_id": "req_rate_001"
}
```

---

# Internal Server Errors

```json
{
  "success": false,
  "error": {
    "code": "INTERNAL_SERVER_ERROR",
    "message": "An unexpected error occurred."
  },
  "request_id": "req_internal"
}
```

Internal implementation details must never be exposed.

---

# Correlation IDs

Every request receives a unique identifier.

Example

```
req_7bfb95b0d6f649d9
```

Purpose

- Log correlation
- Debugging
- Support requests
- Distributed tracing

---

# Logging Strategy

Errors should log:

- Timestamp
- Request ID
- User ID (if authenticated)
- Endpoint
- HTTP Method
- Status Code
- Error Code
- Stack Trace (server only)

Sensitive information must never appear in client responses.

---

# Retryable Errors

Clients may retry

| Error | Retry |
|---------|--------|
| LLM_TIMEOUT | Yes |
| DATABASE_TIMEOUT | Yes |
| SERVICE_UNAVAILABLE | Yes |
| RATE_LIMIT_EXCEEDED | After delay |
| INTERNAL_SERVER_ERROR | Optional |

Clients should not retry

- Validation errors
- Authorization failures
- Authentication failures
- Not found errors

---

# Business Rules

- Every error must include an error code.
- Every error must include a request ID.
- Error codes are immutable once released.
- Messages should be user-friendly.
- Stack traces must never be returned to clients.

---

# OpenAPI Tags

```
Errors
```

---

# Related Documents

- `authentication.md`
- `health.md`
- `pagination.md`
- `../03-architecture/system-architecture.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial Global Error Handling specification |