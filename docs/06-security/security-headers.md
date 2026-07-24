# HTTP Security Headers Architecture

**Document ID:** SEC-012

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the HTTP security headers used by the AI Career Interview Platform.

Security headers instruct modern browsers to enforce additional protections against common web attacks such as:

- Cross-Site Scripting (XSS)
- Clickjacking
- MIME sniffing
- Downgrade attacks
- Information leakage
- Untrusted resource loading

---

# Security Objectives

The browser security policy must provide:

- Browser hardening
- Secure transport enforcement
- Script execution restrictions
- Frame protection
- Content isolation
- Reduced information disclosure

---

# Response Header Flow

```text
Browser Request

↓

Reverse Proxy

↓

FastAPI Application

↓

Security Header Middleware

↓

Response

↓

Browser Security Enforcement
```

Every HTTP response includes the required security headers.

---

# Standard Security Headers

| Header | Purpose |
|----------|---------|
| Content-Security-Policy | Restrict resource loading |
| Strict-Transport-Security | Enforce HTTPS |
| X-Frame-Options | Prevent clickjacking |
| X-Content-Type-Options | Disable MIME sniffing |
| Referrer-Policy | Control referrer leakage |
| Permissions-Policy | Restrict browser capabilities |

---

# Content Security Policy (CSP)

Purpose

Restricts which resources the browser may load.

Recommended Policy

```
default-src 'self';

script-src 'self';

style-src 'self' 'unsafe-inline';

img-src 'self' data: https:;

font-src 'self';

connect-src 'self' https://api.groq.com;

object-src 'none';

frame-ancestors 'none';

base-uri 'self';

form-action 'self';
```

Future deployments should replace `'unsafe-inline'` with nonces or hashes where feasible.

---

# Strict-Transport-Security (HSTS)

Purpose

Force browsers to communicate only over HTTPS.

Recommended Header

```
Strict-Transport-Security:

max-age=31536000;

includeSubDomains;

preload
```

Requirements

- HTTPS only
- One-year minimum
- Enabled only after HTTPS deployment is verified

---

# X-Frame-Options

Purpose

Prevent clickjacking attacks.

Value

```
DENY
```

The platform must never be embedded inside an iframe.

---

# X-Content-Type-Options

Purpose

Prevent MIME type sniffing.

Value

```
nosniff
```

Browsers must respect declared MIME types.

---

# Referrer-Policy

Purpose

Limit information leakage through the Referer header.

Recommended Value

```
strict-origin-when-cross-origin
```

This balances analytics needs with privacy.

---

# Permissions-Policy

Purpose

Restrict browser features that are unnecessary for the application.

Example

```
camera=(),

microphone=(self),

geolocation=(),

payment=(),

usb=(),

accelerometer=(),

gyroscope=()
```

Only explicitly required capabilities should be enabled.

---

# Cross-Origin Resource Sharing (CORS)

Security headers complement—but do not replace—CORS.

Allowed Origins

Development

```
http://localhost:5173
```

Production

```
https://app.example.com
```

Wildcard origins are prohibited in production.

---

# Cache-Control

Sensitive authenticated responses should include:

```
Cache-Control:

no-store
```

Authentication endpoints should never be cached.

---

# Browser Compatibility

Supported browsers

- Chrome
- Edge
- Firefox
- Safari

Security headers should follow current browser standards.

---

# Middleware Implementation

Headers are injected through centralized middleware.

```text
Incoming Request

↓

Application

↓

Response

↓

Security Middleware

↓

Headers Added

↓

Client
```

Individual endpoints must not manually add security headers unless specifically required.

---

# Verification

Headers should be verified using:

- Browser Developer Tools
- Automated integration tests
- Security scanners
- CI/CD validation

Missing headers should fail deployment quality checks.

---

# Business Rules

- Every HTTP response includes mandatory security headers.
- HTTPS is required in production.
- Clickjacking protection is always enabled.
- MIME sniffing is disabled.
- CSP must restrict external resource loading.
- Browser capabilities follow least privilege.

---

# Future Enhancements

Planned improvements

- CSP nonces
- CSP hashes
- Trusted Types
- Cross-Origin Embedder Policy (COEP)
- Cross-Origin Opener Policy (COOP)
- Cross-Origin Resource Policy (CORP)

---

# Related Documents

- `api-security.md`
- `authentication.md`
- `oauth.md`
- `rate-limiting.md`
- `incident-response.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial HTTP security headers architecture specification |