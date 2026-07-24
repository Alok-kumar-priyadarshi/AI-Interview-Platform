# Authentication Technology Stack

**Document ID:** TS-006

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the authentication and authorization architecture for the
AI Career Interview Platform.

It specifies how users authenticate, how sessions are managed, how APIs are
protected, and how identity information flows throughout the system.

Authentication decisions documented here apply to all frontend, backend, and API
implementations.

---

# Objectives

The authentication system must be:

- Secure
- Stateless
- Easy to use
- Scalable
- Standards compliant
- Extensible
- Production ready

---

# Authentication Stack

| Category | Technology |
|----------|------------|
| Identity Provider | Google OAuth 2.0 |
| Authorization | JWT |
| Session Type | Stateless |
| Transport | HTTPS |
| Token Location | HTTP-only Cookie (Preferred) |
| Backend Framework | FastAPI |
| Frontend | React |
| User Storage | PostgreSQL |

---

# Authentication Philosophy

Version 1 intentionally supports only:

- Google Sign-In

Reasons:

- Better security
- Faster onboarding
- No password management
- Reduced attack surface
- Better user experience

Email/password authentication is intentionally excluded from Version 1.

---

# Authentication Flow

```
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

Identity Verification

↓

User Creation / Lookup

↓

JWT Generation

↓

Authenticated Session
```

---

# User Login Flow

Step 1

User selects:

```
Continue with Google
```

↓

Step 2

Browser redirects to Google.

↓

Step 3

User authenticates.

↓

Step 4

Google returns an authorization code.

↓

Step 5

Backend exchanges the authorization code for user information.

↓

Step 6

Backend validates:

- Token signature
- Audience
- Issuer
- Expiration

↓

Step 7

Backend finds or creates the user.

↓

Step 8

JWT is generated.

↓

Step 9

Session begins.

---

# First Login

If the user does not exist:

- Create user record
- Save Google ID
- Save email
- Save display name
- Save avatar URL (optional)
- Record creation timestamp

No password is stored.

---

# Returning User

If the user already exists:

- Verify identity
- Update profile information if required
- Issue a new JWT
- Continue session

---

# User Identity

Every authenticated user must have:

- UUID
- Google ID
- Email
- Display Name
- Profile Picture (optional)
- Created At
- Updated At

---

# JWT Strategy

JWT contains:

- User ID
- Email
- Issued At
- Expiration
- Token Version

Avoid placing unnecessary personal information inside the token.

---

# Token Lifetime

Recommended:

Access Token

```
15–60 minutes
```

Session renewal:

Handled transparently.

Refresh tokens may be introduced in future versions if required.

---

# Token Storage

Preferred:

HTTP-only Secure Cookies

Reasons:

- Protection against XSS
- Automatic transmission
- Better security

Avoid Local Storage for authentication tokens unless project requirements
change.

---

# Authorization Model

Version 1 roles:

```
User
```

Reserved future roles:

```
Admin
Recruiter
Organization
Premium
```

Authorization checks must be role-based rather than hardcoded.

---

# Protected Resources

Authentication is required for:

- Resume upload
- Interview generation
- Interview history
- Evaluation reports
- User profile
- Dashboard

Public endpoints should remain minimal.

---

# Session Management

The backend is responsible for:

- Session creation
- Token validation
- Session expiration
- Logout
- Revocation (future)

The frontend only consumes authentication state.

---

# Logout Flow

```
User

↓

Logout Request

↓

Backend Invalidates Session (if applicable)

↓

Authentication Cookie Cleared

↓

Frontend Redirect

↓

Login Screen
```

---

# API Authentication

Protected API requests include:

```
Authorization: Bearer <token>
```

or

Secure HTTP-only authentication cookie.

Unauthenticated requests must return:

```
401 Unauthorized
```

Unauthorized requests must return:

```
403 Forbidden
```

---

# User Registration

Registration is automatic.

There is no manual sign-up form.

Account creation occurs during the first successful Google authentication.

---

# Security Principles

Always:

- Validate JWT signature
- Validate expiration
- Validate issuer
- Validate audience
- Enforce HTTPS
- Validate OAuth state parameter

Never trust data received directly from the client.

---

# CSRF Protection

If cookies are used:

Implement CSRF protection using:

- SameSite cookies
- CSRF tokens where appropriate

---

# Rate Limiting

Protect authentication endpoints against abuse.

Examples:

- Login attempts
- OAuth callback endpoint

Future implementations may use middleware or reverse proxy limits.

---

# Error Handling

Authentication failures should return standardized responses.

Example:

```json
{
  "success": false,
  "message": "Authentication failed.",
  "error_code": "AUTH_INVALID_TOKEN"
}
```

Do not expose implementation details.

---

# Audit Logging

Authentication events to log:

- Successful login
- Failed login
- Logout
- Token validation failures
- OAuth callback errors

Never log:

- Tokens
- Authorization codes
- Sensitive credentials

---

# Future Enhancements

Potential future additions:

- Refresh tokens
- Multi-provider OAuth
- Microsoft Login
- GitHub Login
- LinkedIn Login
- Multi-factor authentication (MFA)
- Session management dashboard
- Device management
- Single Sign-On (SSO)

These features are intentionally excluded from Version 1.

---

# Related Documents

- `technology-overview.md`
- `backend-stack.md`
- `database-stack.md`
- `07-security/` (future)
- `05-api-contracts/` (future)

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial authentication technology stack |