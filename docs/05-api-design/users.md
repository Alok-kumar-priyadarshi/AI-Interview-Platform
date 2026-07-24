# User Management API

**Document ID:** API-002

**Version:** 1.0.0

**Status:** Approved

**Priority:** High

**Last Updated:** 2026-07-23

---

# Purpose

This document defines all User Management endpoints for the AI Career Interview Platform.

These endpoints allow authenticated users to:

- Retrieve their profile
- Update profile information
- Manage preferences
- View account metadata
- Delete their account

Users can only access their own resources unless they have administrative privileges.

---

# Resource

```
/users
```

---

# Authorization

Authentication Required

```
Yes
```

Roles

| Role | Access |
|------|---------|
| Candidate | Own account only |
| Admin | Any account |

---

# Endpoint Summary

| Method | Endpoint | Description |
|----------|----------|-------------|
| GET | /users/me | Current user profile |
| PATCH | /users/me | Update profile |
| GET | /users/me/preferences | Retrieve preferences |
| PATCH | /users/me/preferences | Update preferences |
| GET | /users/me/statistics | User statistics |
| DELETE | /users/me | Delete account |

---

# GET /users/me

## Purpose

Returns the authenticated user's profile.

---

Headers

```
Authorization: Bearer <token>
```

---

Response

```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "John Doe",
    "email": "john@example.com",
    "profile_picture": "https://...",
    "created_at": "2026-07-22T10:00:00Z",
    "last_login": "2026-07-23T08:30:00Z"
  }
}
```

---

Status Codes

| Code | Meaning |
|------|----------|
| 200 | Success |
| 401 | Unauthorized |
| 404 | User not found |

---

# PATCH /users/me

## Purpose

Updates editable user information.

Editable fields:

- name
- preferred_language
- timezone
- notification preferences

Email cannot be modified because it is managed by Google OAuth.

---

Request

```json
{
  "name": "John Doe",
  "preferred_language": "en",
  "timezone": "Asia/Kolkata"
}
```

---

Validation

| Field | Rule |
|------|------|
| name | 2–100 characters |
| preferred_language | Supported language |
| timezone | Valid IANA timezone |

---

Response

```json
{
  "success": true,
  "message": "Profile updated successfully."
}
```

---

Status Codes

| Code | Meaning |
|------|----------|
| 200 | Updated |
| 400 | Invalid input |
| 401 | Unauthorized |
| 422 | Validation failed |

---

# GET /users/me/preferences

## Purpose

Returns user-specific application preferences.

---

Response

```json
{
  "success": true,
  "data": {
    "theme": "dark",
    "language": "en",
    "voice_gender": "female",
    "default_interview_type": "technical",
    "notifications": true
  }
}
```

---

# PATCH /users/me/preferences

## Purpose

Updates application preferences.

---

Request

```json
{
  "theme": "dark",
  "voice_gender": "male",
  "notifications": false
}
```

---

Allowed Values

Theme

```
light

dark

system
```

Voice Gender

```
male

female
```

Notifications

```
true

false
```

---

Response

```json
{
  "success": true,
  "message": "Preferences updated successfully."
}
```

---

# GET /users/me/statistics

## Purpose

Returns interview statistics for the current user.

---

Response

```json
{
  "success": true,
  "data": {
    "total_interviews": 32,
    "completed_interviews": 28,
    "average_score": 81.6,
    "highest_score": 95,
    "reports_generated": 28,
    "resume_count": 2
  }
}
```

---

# DELETE /users/me

## Purpose

Deletes the authenticated user's account.

Deletion includes:

- User profile
- Candidate profile
- Resume metadata
- Interview history
- Reports
- Evaluations
- Preferences

Files stored externally should be deleted asynchronously.

---

Headers

```
Authorization: Bearer <token>
```

---

Request

```json
{
  "confirm": true
}
```

---

Response

```json
{
  "success": true,
  "message": "Account scheduled for deletion."
}
```

---

Status Codes

| Code | Meaning |
|------|----------|
| 200 | Deletion scheduled |
| 400 | Confirmation missing |
| 401 | Unauthorized |
| 403 | Forbidden |

---

# Validation Rules

Name

- Required
- 2–100 characters

Preferred Language

- ISO language code

Timezone

- Valid IANA timezone

Voice Gender

- male
- female

Theme

- light
- dark
- system

---

# Security

Every endpoint validates:

- JWT token
- User identity
- Resource ownership

Users cannot access another user's data.

---

# Rate Limits

| Endpoint | Limit |
|-----------|--------|
| GET /users/me | 100/min |
| PATCH /users/me | 20/min |
| GET /users/me/preferences | 50/min |
| PATCH /users/me/preferences | 20/min |
| GET /users/me/statistics | 30/min |
| DELETE /users/me | 5/day |

---

# Error Responses

Unauthorized

```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required."
  }
}
```

---

Validation Error

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid profile data."
  }
}
```

---

Forbidden

```json
{
  "success": false,
  "error": {
    "code": "FORBIDDEN",
    "message": "Access denied."
  }
}
```

---

# OpenAPI Tags

```
Users
```

---

# Related Documents

- `authentication.md`
- `candidate-profile.md`
- `errors.md`
- `pagination.md`
- `../04-database/entities/users.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial User Management API specification |