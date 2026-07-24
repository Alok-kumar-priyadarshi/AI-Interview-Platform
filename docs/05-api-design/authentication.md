# Authentication API

**Document ID:** API-001

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines every authentication endpoint used by the AI Career Interview Platform.

Authentication provides:

- Google OAuth Login
- JWT Authentication
- Session Management
- Token Refresh
- Logout
- Authorization

Only Google Sign-In is supported in Version 1.

---

# Authentication Architecture

```text
Frontend

↓

Google OAuth

↓

Backend Callback

↓

Validate Google Token

↓

Create / Find User

↓

Generate JWT

↓

Return Tokens
```

---

# Authentication Methods

Supported

- Google OAuth 2.0
- JWT Bearer Token

Not Supported

- Username/Password
- Email Login
- OTP Login
- Facebook Login
- GitHub Login

---

# Token Types

## Access Token

Purpose

```
API Authentication
```

Lifetime

```
15 Minutes
```

---

## Refresh Token

Purpose

```
Generate New Access Token
```

Lifetime

```
30 Days
```

Stored securely using HTTP-only cookies.

---

# JWT Claims

Example

```json
{
  "sub": "user_uuid",
  "email": "candidate@example.com",
  "role": "candidate",
  "iat": 1721700000,
  "exp": 1721700900
}
```

---

# Authorization Header

Example

```
Authorization: Bearer <access_token>
```

Required for every protected endpoint.

---

# Authentication Flow

```text
User Clicks Login

↓

Google OAuth

↓

Google Returns Authorization Code

↓

Backend Exchanges Code

↓

Verify Google Identity

↓

Create User (if needed)

↓

Generate JWT Tokens

↓

Return Tokens

↓

Authenticated Requests
```

---

# Endpoint Summary

| Method | Endpoint | Purpose |
|---------|----------|---------|
| GET | /auth/google/login | Redirect to Google |
| GET | /auth/google/callback | OAuth callback |
| POST | /auth/refresh | Refresh access token |
| POST | /auth/logout | Logout |
| GET | /auth/me | Current user |

---

# GET /auth/google/login

## Purpose

Starts Google OAuth flow.

---

Response

```
302 Redirect
```

Redirects user to Google's authorization page.

---

# GET /auth/google/callback

## Purpose

Handles Google OAuth callback.

---

Query Parameters

| Parameter | Required |
|-----------|----------|
| code | Yes |
| state | Yes |

---

Success Response

```json
{
  "success": true,
  "message": "Login successful.",
  "data": {
    "access_token": "<jwt>",
    "refresh_token": "<jwt>",
    "expires_in": 900
  }
}
```

---

Possible Errors

- Invalid authorization code
- Invalid state
- Google unavailable
- Token exchange failed

---

# POST /auth/refresh

## Purpose

Issues a new access token.

---

Request

```json
{
  "refresh_token": "<jwt>"
}
```

---

Response

```json
{
  "success": true,
  "data": {
    "access_token": "<jwt>",
    "expires_in": 900
  }
}
```

---

Errors

```
401 Unauthorized
```

Reasons

- Refresh token expired
- Invalid signature
- Revoked token

---

# POST /auth/logout

## Purpose

Terminates current session.

---

Request

```http
POST /auth/logout
Authorization: Bearer <token>
```

---

Response

```json
{
  "success": true,
  "message": "Logged out successfully."
}
```

Logout actions

- Revoke refresh token
- Invalidate session
- Clear authentication cookie

---

# GET /auth/me

## Purpose

Returns authenticated user information.

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
    "picture": "https://..."
  }
}
```

---

# Authentication Middleware

Every protected endpoint performs:

```text
Extract JWT

↓

Validate Signature

↓

Check Expiration

↓

Verify User Exists

↓

Load User Context

↓

Continue Request
```

Invalid tokens return HTTP 401.

---

# Authorization Roles

Version 1

| Role | Permissions |
|------|-------------|
| candidate | Standard platform access |
| admin | Administrative access |

Future versions may introduce recruiter and moderator roles.

---

# Token Lifecycle

```text
Login

↓

Access Token (15 min)

↓

Expires

↓

Refresh Token

↓

New Access Token

↓

Continue Session
```

Expired refresh tokens require re-authentication.

---

# Security Requirements

- HTTPS only
- Signed JWTs
- Short-lived access tokens
- Secure refresh token storage
- CSRF protection where applicable
- OAuth state validation
- Replay attack prevention

---

# Rate Limits

| Endpoint | Limit |
|----------|-------|
| /auth/google/login | 20/min/IP |
| /auth/google/callback | 20/min/IP |
| /auth/refresh | 30/min/user |
| /auth/logout | 30/min/user |
| /auth/me | 100/min/user |

---

# Error Responses

## Unauthorized

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

## Invalid Token

```json
{
  "success": false,
  "error": {
    "code": "INVALID_TOKEN",
    "message": "Access token is invalid."
  }
}
```

---

## Expired Token

```json
{
  "success": false,
  "error": {
    "code": "TOKEN_EXPIRED",
    "message": "Access token has expired."
  }
}
```

---

# OpenAPI Tags

```
Authentication
```

---

# Related Documents

- `README.md`
- `users.md`
- `errors.md`
- `../04-database/users.md`
- `../04-database/transactions.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial authentication API specification |