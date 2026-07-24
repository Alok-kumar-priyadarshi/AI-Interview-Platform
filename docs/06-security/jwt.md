# JWT Security Architecture

**Document ID:** SEC-003

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines how JSON Web Tokens (JWTs) are issued, validated, and managed within the AI Career Interview Platform.

JWTs provide stateless authentication for all protected backend APIs.

This document covers:

- Token structure
- Claims
- Signing algorithm
- Issuance
- Validation
- Expiration
- Key management
- Security best practices

---

# JWT Overview

Token Type

```
Access Token
```

Format

```
JWT (JSON Web Token)
```

Authentication Header

```
Authorization: Bearer <JWT>
```

---

# JWT Architecture

```text
User Login

↓

Google OAuth Success

↓

Backend Issues JWT

↓

Frontend Stores Token

↓

API Request

↓

JWT Validation Middleware

↓

Authorized Request
```

---

# JWT Structure

A JWT consists of three Base64URL encoded sections.

```text
Header

.

Payload

.

Signature
```

---

# Header

Example

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

---

# Payload

Example

```json
{
  "sub": "4d77d2b6-1d3f-4c8d-a2c5-fd80c7d2e1a5",
  "email": "user@example.com",
  "role": "candidate",
  "iat": 1784780000,
  "exp": 1784783600,
  "iss": "ai-career-platform"
}
```

---

# Supported Claims

| Claim | Description |
|--------|-------------|
| sub | Unique user identifier |
| email | Verified Google email |
| role | Candidate or Admin |
| iat | Issued-at timestamp |
| exp | Expiration timestamp |
| iss | Token issuer |

Future optional claims

- jti
- aud
- session_id

---

# Signature

Version 1

```
HS256
```

Future

```
RS256
```

The signing key is stored only in secure environment variables.

---

# Token Lifetime

| Token | Duration |
|--------|----------|
| Access Token | 60 minutes |

Version 1 does not use refresh tokens.

---

# Token Issuance

JWTs are issued only after:

- Google OAuth succeeds
- User identity is verified
- Email is verified
- User account exists or is created

---

# Token Validation

Every protected request validates:

- Signature
- Expiration
- Issuer
- User existence
- Account status

Validation order

```text
Authorization Header

↓

JWT Parsing

↓

Signature Validation

↓

Expiration Check

↓

Issuer Check

↓

Load User

↓

Authorization
```

---

# Expired Tokens

Expired tokens are rejected.

Response

```
401 Unauthorized
```

Error Code

```
TOKEN_EXPIRED
```

Users must authenticate again.

---

# Invalid Tokens

Rejected if:

- Signature mismatch
- Modified payload
- Malformed token
- Unknown issuer
- Missing required claims

---

# Token Storage

Frontend

- In-memory storage (preferred)

Alternative

- Secure HTTP-only cookies (future)

The application must never store JWTs in:

- Local Storage
- Session Storage

---

# Key Management

JWT signing keys must:

- Be randomly generated
- Be at least 256 bits
- Never be committed to source control
- Be stored in environment variables
- Be rotated during deployments when necessary

Example

```
JWT_SECRET=<secure-random-secret>
```

---

# Revocation Strategy

Version 1

- Stateless JWTs
- No server-side blacklist

Future

- Token blacklist
- Session invalidation
- Refresh token rotation

---

# Middleware Integration

Every protected endpoint uses JWT middleware.

Responsibilities

- Parse Authorization header
- Validate token
- Load authenticated user
- Attach user context to request
- Reject invalid requests

---

# Security Controls

Implemented protections

- HTTPS only
- Signed JWTs
- Token expiration
- Short token lifetime
- Issuer validation
- Role validation
- Account status validation

---

# Common Error Codes

```
INVALID_TOKEN

TOKEN_EXPIRED

TOKEN_REVOKED

UNAUTHORIZED

LOGIN_REQUIRED
```

---

# Example Error Response

```json
{
  "success": false,
  "error": {
    "code": "TOKEN_EXPIRED",
    "message": "Your session has expired. Please sign in again."
  },
  "request_id": "req_jwt_001"
}
```

---

# Business Rules

- JWTs are issued only after successful authentication.
- Every protected endpoint validates the JWT.
- Expired tokens are never accepted.
- JWT payloads must not contain sensitive information.
- Signing secrets must never be exposed.

---

# Related Documents

- `authentication.md`
- `authorization.md`
- `oauth.md`
- `secrets-management.md`
- `../05-api-design/authentication.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial JWT security architecture specification |