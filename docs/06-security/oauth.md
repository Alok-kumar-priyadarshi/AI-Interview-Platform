# Google OAuth 2.0 Architecture

**Document ID:** SEC-004

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines how Google OAuth 2.0 is implemented within the AI Career Interview Platform.

Version 1 exclusively supports Google OAuth authentication.

This document covers:

- Authorization Code Flow
- OAuth endpoints
- Identity verification
- Callback processing
- Token exchange
- Account creation
- Session establishment
- Security protections

---

# OAuth Overview

Provider

```
Google Identity Platform
```

OAuth Version

```
OAuth 2.0
```

Flow

```
Authorization Code Flow
```

Authentication Type

```
Google Sign-In
```

---

# Authentication Flow

```text
User

↓

Click "Continue with Google"

↓

Frontend

↓

Google Authorization Endpoint

↓

User Authentication

↓

User Consent

↓

Authorization Code

↓

Backend Callback Endpoint

↓

Exchange Code for Tokens

↓

Validate Google ID Token

↓

Extract User Identity

↓

Create / Update User

↓

Issue Platform JWT

↓

Return Authenticated Session
```

---

# OAuth Components

| Component | Responsibility |
|-----------|----------------|
| React Frontend | Initiates login |
| Google OAuth | User authentication |
| FastAPI Backend | Code exchange & validation |
| JWT Service | Issues platform token |
| Database | User persistence |

---

# OAuth Endpoints

Frontend Login

```
GET /auth/google/login
```

OAuth Callback

```
GET /auth/google/callback
```

Logout

```
POST /auth/logout
```

Current User

```
GET /auth/me
```

---

# Authorization Request

Frontend redirects user to Google with:

- client_id
- redirect_uri
- response_type=code
- scope
- state

---

Example Scope

```
openid

email

profile
```

---

# State Parameter

Every OAuth request includes a randomly generated state value.

Purpose

- CSRF protection
- Request validation
- Session correlation

Validation

```text
Generated

↓

Stored Temporarily

↓

Returned by Google

↓

Compared

↓

Accepted / Rejected
```

If state validation fails

```
401 Unauthorized
```

---

# Authorization Code

Google returns a short-lived authorization code.

Properties

- Single use
- Short expiration
- Exchanged only by backend

The frontend never exchanges the code directly.

---

# Token Exchange

Backend exchanges the authorization code for:

- Access Token
- ID Token

Google endpoint

```
https://oauth2.googleapis.com/token
```

---

# ID Token Validation

Backend validates:

- Signature
- Issuer
- Audience
- Expiration
- Email verification

Rejected tokens are discarded immediately.

---

# Identity Extraction

Information extracted

- Google User ID
- Email
- Display Name
- Profile Picture (optional)

Only verified email addresses are accepted.

---

# Account Linking

First Login

- Create User
- Create Candidate Profile
- Record Login Timestamp

Returning Login

- Locate existing account by verified email
- Update Last Login
- Preserve user data

Duplicate accounts are never created.

---

# JWT Issuance

After successful validation

```text
Google Identity

↓

Platform JWT

↓

Frontend Session

↓

Authenticated APIs
```

Google tokens are never used directly for application authorization.

---

# OAuth Failure Scenarios

Possible failures

- User cancels login
- Invalid authorization code
- Invalid client credentials
- Expired code
- Invalid redirect URI
- Invalid state
- Email not verified
- Google service unavailable

---

# Error Codes

```
GOOGLE_AUTH_FAILED

INVALID_STATE

INVALID_AUTHORIZATION_CODE

EMAIL_NOT_VERIFIED

GOOGLE_SERVICE_UNAVAILABLE
```

---

# Security Controls

Implemented protections

- Authorization Code Flow
- HTTPS only
- State validation
- Backend-only token exchange
- Verified email requirement
- Short-lived authorization codes
- Platform JWT isolation

---

# Business Rules

- Google is the only authentication provider in Version 1.
- Every login requires a verified Google account.
- Email uniquely identifies a user.
- Authorization codes are exchanged exactly once.
- Google access tokens are never exposed to frontend business logic.

---

# Future Enhancements

Planned support

- GitHub OAuth
- Microsoft OAuth
- Enterprise SSO (SAML/OIDC)
- Multi-provider account linking

---

# Related Documents

- `authentication.md`
- `jwt.md`
- `authorization.md`
- `api-security.md`
- `../05-api-design/authentication.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial Google OAuth 2.0 architecture specification |