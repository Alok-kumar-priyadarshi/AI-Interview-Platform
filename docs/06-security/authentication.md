# Authentication Architecture

**Document ID:** SEC-001

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the complete authentication architecture for the AI Career Interview Platform.

Authentication is responsible for:

- Identifying users
- Verifying identity
- Creating authenticated sessions
- Issuing JWT access tokens
- Protecting API endpoints
- Maintaining secure login state

Version 1 exclusively supports Google OAuth 2.0 authentication.

---

# Authentication Overview

Authentication Provider

```
Google OAuth 2.0
```

Backend

```
FastAPI
```

Frontend

```
React + Vite
```

Token Type

```
JWT Access Token
```

---

# Authentication Flow

```text
User

↓

Click "Continue with Google"

↓

Google OAuth Consent

↓

Google Authentication

↓

Authorization Code

↓

Backend Callback

↓

Token Exchange

↓

Google User Verification

↓

Create / Update User

↓

Issue JWT

↓

Return Session

↓

Authenticated User
```

---

# Supported Authentication Methods

| Method | Version 1 | Future |
|----------|-----------|---------|
| Google OAuth | ✅ | ✅ |
| Email/Password | ❌ | Optional |
| GitHub Login | ❌ | Planned |
| Microsoft Login | ❌ | Planned |
| Enterprise SSO | ❌ | Planned |

---

# Login Lifecycle

## Step 1

User selects

```
Continue with Google
```

---

## Step 2

Frontend redirects to Google OAuth authorization endpoint.

---

## Step 3

Google authenticates the user.

---

## Step 4

Google redirects to backend callback endpoint.

---

## Step 5

Backend exchanges authorization code for Google tokens.

---

## Step 6

Backend validates:

- Google ID Token
- Email verification
- Audience
- Issuer
- Expiration

---

## Step 7

Backend:

- Creates new user (first login)
- Updates existing user (returning login)

---

## Step 8

JWT Access Token is generated.

---

## Step 9

Frontend stores authentication state and begins authenticated API requests.

---

# User Creation Rules

First Login

- Create User
- Create Candidate Profile
- Record Login Timestamp

Returning Login

- Update Last Login
- Refresh Session
- Preserve Existing Profile

---

# JWT Structure

Example Payload

```json
{
  "sub": "user_uuid",
  "email": "user@example.com",
  "role": "candidate",
  "iat": 1784780000,
  "exp": 1784783600,
  "iss": "ai-career-platform"
}
```

---

# JWT Claims

| Claim | Description |
|---------|-------------|
| sub | User identifier |
| email | Verified email |
| role | Candidate/Admin |
| iat | Issued at |
| exp | Expiration |
| iss | Token issuer |

---

# Token Lifetime

| Token | Lifetime |
|---------|----------|
| Access Token | 60 minutes |

Future

- Refresh Tokens
- Session Rotation

---

# Session Lifecycle

```text
Login

↓

JWT Issued

↓

Authenticated Requests

↓

Token Expiration

↓

Re-authentication
```

---

# Authentication Middleware

Every protected endpoint validates:

- Authorization header
- JWT signature
- Expiration
- Issuer
- User existence
- Account status

If validation fails

```
401 Unauthorized
```

---

# Logout

Logout Process

1. Frontend removes JWT.
2. Local authentication state is cleared.
3. User is redirected to login page.

Version 1 does not maintain server-side session state.

---

# Failed Authentication

Possible Causes

- Invalid authorization code
- Expired token
- Invalid JWT
- Revoked Google account
- Invalid issuer
- Invalid audience

---

# Authentication Errors

Examples

```
UNAUTHORIZED

INVALID_TOKEN

TOKEN_EXPIRED

LOGIN_REQUIRED

INVALID_GOOGLE_TOKEN
```

---

# Security Controls

Authentication includes:

- HTTPS only
- Google email verification
- Signed JWTs
- Token expiration
- Secure OAuth callback validation
- CSRF protection via OAuth state parameter

---

# Business Rules

- Only verified Google accounts may log in.
- Every authenticated user has exactly one account.
- Email address is immutable once created.
- Authentication must complete before any protected API call.
- Invalid or expired tokens must never be accepted.

---

# Related Documents

- `oauth.md`
- `jwt.md`
- `authorization.md`
- `../05-api-design/authentication.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial authentication architecture specification |