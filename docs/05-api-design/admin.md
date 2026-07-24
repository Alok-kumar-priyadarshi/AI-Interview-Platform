# Admin API

**Document ID:** API-012

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines every administrative API used by the AI Career Interview Platform.

The Admin API provides:

- User management
- Interview monitoring
- Resume monitoring
- Evaluation management
- Report management
- Analytics
- Audit logs
- Platform health overview
- Administrative operations

All endpoints require administrator privileges.

---

# Resource

```
/admin
```

---

# Authorization

Authentication Required

```
Yes
```

Role Required

```
Admin
```

Every request validates:

- JWT
- Admin role
- Active account
- Session validity

---

# RBAC

Supported Roles

| Role | Permissions |
|------|-------------|
| Candidate | Standard platform access |
| Admin | Full administrative access |

Future versions

- Moderator
- Support Engineer
- Content Manager

---

# Endpoint Summary

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /admin/dashboard | Platform overview |
| GET | /admin/users | List users |
| GET | /admin/users/{id} | User details |
| PATCH | /admin/users/{id}/status | Update user status |
| GET | /admin/interviews | Monitor interviews |
| GET | /admin/evaluations | Monitor evaluations |
| POST | /admin/evaluations/{id}/retry | Retry evaluation |
| GET | /admin/reports | Monitor reports |
| GET | /admin/audit-logs | Audit logs |

---

# GET /admin/dashboard

## Purpose

Returns overall platform statistics.

---

Response

```json
{
  "success": true,
  "data": {
    "total_users": 2845,
    "active_users": 641,
    "total_interviews": 12672,
    "completed_interviews": 11982,
    "reports_generated": 11880,
    "system_status": "healthy"
  }
}
```

---

# GET /admin/users

## Purpose

Returns paginated user list.

---

Query Parameters

```
page

page_size

status

role

search

sort
```

---

Response

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "uuid",
        "name": "John Doe",
        "email": "john@example.com",
        "role": "candidate",
        "status": "active"
      }
    ],
    "page": 1,
    "total": 2845
  }
}
```

---

# GET /admin/users/{id}

Returns complete user information.

Includes

- Profile
- Candidate Profile
- Resume Count
- Interview Count
- Evaluation Count
- Last Login

---

# PATCH /admin/users/{id}/status

## Purpose

Updates account status.

---

Allowed Status

```
Active

Suspended

Disabled
```

---

Request

```json
{
  "status": "Suspended"
}
```

---

Response

```json
{
  "success": true,
  "message": "User status updated."
}
```

---

# GET /admin/interviews

Returns interview monitoring information.

Supported Filters

- Status
- Mode
- Difficulty
- Candidate
- Date Range

---

# GET /admin/evaluations

Returns evaluation queue information.

Includes

- Processing
- Failed
- Completed
- Retry Count

---

# POST /admin/evaluations/{id}/retry

Retries failed evaluation.

---

Response

```json
{
  "success": true,
  "message": "Evaluation queued."
}
```

---

# GET /admin/reports

Returns report generation status.

Supported Filters

- Ready
- Failed
- Processing

---

# GET /admin/audit-logs

Returns administrative activity logs.

Example

```json
{
  "success": true,
  "data": [
    {
      "action": "Suspend User",
      "performed_by": "admin@example.com",
      "timestamp": "2026-07-23T15:20:00Z"
    }
  ]
}
```

---

# Platform Analytics

Dashboard includes:

- Daily active users
- Interview success rate
- Average score
- Processing latency
- Queue sizes
- API usage
- Storage usage

---

# Audit Logging

Every administrative action generates an immutable audit log.

Logged Events

- Login
- User updates
- User suspension
- Evaluation retry
- Report regeneration
- Configuration changes

---

# Business Rules

- Only administrators may access these endpoints.
- Audit logs cannot be modified.
- Deleted users remain visible in audit logs.
- Retry operations are idempotent.

---

# Authorization

Every request validates:

- JWT
- Role
- Permission
- Resource availability

---

# Rate Limits

| Endpoint | Limit |
|-----------|--------|
| Dashboard | 60/min |
| Users | 60/min |
| User Details | 60/min |
| Status Update | 20/min |
| Interviews | 60/min |
| Evaluations | 60/min |
| Reports | 60/min |
| Audit Logs | 30/min |

---

# Error Responses

Forbidden

```json
{
  "success": false,
  "error": {
    "code": "FORBIDDEN",
    "message": "Administrator access required."
  }
}
```

---

User Not Found

```json
{
  "success": false,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User does not exist."
  }
}
```

---

Insufficient Permission

```json
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_PERMISSION",
    "message": "Permission denied."
  }
}
```

---

# OpenAPI Tags

```
Admin
```

---

# Related Documents

- `authentication.md`
- `dashboard.md`
- `errors.md`
- `health.md`
- `../04-database/entities/users.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial Admin API specification |