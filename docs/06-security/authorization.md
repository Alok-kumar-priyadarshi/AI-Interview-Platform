# Authorization Architecture

**Document ID:** SEC-002

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the authorization architecture for the AI Career Interview Platform.

Authorization determines what an authenticated user is permitted to access or modify after successful authentication.

This document covers:

- Role-Based Access Control (RBAC)
- Resource ownership validation
- Permission evaluation
- Authorization middleware
- Administrative privileges
- Policy enforcement
- Access control best practices

---

# Authorization Overview

Authentication answers:

> Who are you?

Authorization answers:

> What are you allowed to do?

Every protected API endpoint must perform authorization after authentication succeeds.

---

# Authorization Flow

```text
Incoming Request

↓

Authentication Middleware

↓

JWT Validation

↓

Extract User Identity

↓

Determine User Role

↓

Check Resource Ownership

↓

Evaluate Permissions

↓

Access Granted / Denied

↓

API Handler
```

---

# Supported Roles

Version 1 supports two roles.

| Role | Description |
|------|-------------|
| Candidate | Standard platform user |
| Admin | Platform administrator |

Future roles:

- Moderator
- Support Engineer
- Recruiter
- Organization Admin

---

# RBAC Model

```text
User

↓

Role

↓

Permissions

↓

Resources

↓

Allowed Actions
```

Permissions are assigned to roles rather than individual users.

---

# Permission Matrix

| Resource | Candidate | Admin |
|-----------|-----------|--------|
| Own Profile | Read / Update | Read |
| Other Profiles | ❌ | Read |
| Resume | CRUD (Own) | Read |
| Interviews | CRUD (Own) | Read |
| Evaluations | Read (Own) | Read |
| Reports | Read (Own) | Read |
| Dashboard | Own | Global |
| Users | ❌ | CRUD |
| Audit Logs | ❌ | Read |
| Health Metrics | ❌ | Read |

---

# Resource Ownership

Most resources belong to a specific user.

Ownership is verified using:

```
resource.user_id == authenticated_user.id
```

If ownership validation fails:

```
403 Forbidden
```

---

# Authorization Middleware

Every protected endpoint performs:

1. Verify JWT
2. Load authenticated user
3. Verify account status
4. Evaluate required role
5. Validate resource ownership
6. Continue request

---

# Endpoint Protection

Example

```
GET /resume/{id}
```

Authorization steps

- Resume exists
- Resume belongs to authenticated user
- User account is active

If all checks pass

```
200 OK
```

Otherwise

```
403 Forbidden
```

---

# Admin Authorization

Administrators may:

- View all users
- Monitor interviews
- Retry evaluations
- View reports
- Access analytics
- Read audit logs
- View health metrics

Administrators cannot impersonate users in Version 1.

---

# Policy Enforcement

Policies are enforced at the API layer.

Examples

```
Candidate → Own resources only

Admin → Global access

Inactive user → No access
```

---

# Account Status Validation

Allowed account states

```
Active

Suspended

Disabled
```

Authorization behavior

| Status | Access |
|---------|--------|
| Active | Allowed |
| Suspended | Denied |
| Disabled | Denied |

---

# Permission Evaluation

Authorization evaluates:

- User role
- Account status
- Resource ownership
- Endpoint requirements

All conditions must succeed.

---

# Common Authorization Errors

```
FORBIDDEN

INSUFFICIENT_PERMISSION

RESOURCE_ACCESS_DENIED

ADMIN_REQUIRED

ACCOUNT_DISABLED

ACCOUNT_SUSPENDED
```

---

# Error Response

```json
{
  "success": false,
  "error": {
    "code": "FORBIDDEN",
    "message": "You do not have permission to access this resource."
  },
  "request_id": "req_authz_001"
}
```

---

# Security Best Practices

- Never trust client-supplied user IDs.
- Always derive user identity from the validated JWT.
- Perform authorization on every protected request.
- Validate ownership before returning resource data.
- Deny access by default.
- Avoid exposing resource existence through authorization failures.

---

# Business Rules

- Every protected endpoint requires authorization.
- Resource ownership takes precedence over request parameters.
- Role changes take effect immediately after re-authentication.
- Suspended users cannot access protected resources.
- Authorization decisions must be deterministic and auditable.

---

# Related Documents

- `authentication.md`
- `jwt.md`
- `oauth.md`
- `audit-logging.md`
- `../05-api-design/admin.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial authorization architecture specification |