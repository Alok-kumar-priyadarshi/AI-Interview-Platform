# Rate Limiting Architecture

**Document ID:** SEC-011

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the rate limiting architecture for the AI Career Interview Platform.

Rate limiting protects platform resources from abuse, accidental overload, automated attacks, excessive AI usage, and denial-of-service attempts while ensuring fair usage for all users.

This document covers:

- API rate limiting
- AI request quotas
- Upload throttling
- Per-user limits
- Per-IP limits
- Adaptive limiting
- Abuse detection
- Distributed rate limiting

---

# Security Objectives

The rate limiting system must provide:

- Fair resource allocation
- Abuse prevention
- Platform stability
- Cost control
- AI usage protection
- Graceful degradation

---

# Rate Limiting Architecture

```text
Incoming Request

↓

Reverse Proxy

↓

Rate Limiter

↓

Authentication

↓

Authorization

↓

Business Logic

↓

Response
```

Every incoming request is evaluated before reaching application logic.

---

# Limiting Dimensions

Requests may be limited by:

- User ID
- IP Address
- API Key (future)
- Endpoint
- Authentication Status
- AI Token Usage
- Upload Activity

Multiple limits may apply simultaneously.

---

# Rate Limiting Algorithm

Primary algorithm:

```
Sliding Window
```

Future enhancements:

- Token Bucket
- Leaky Bucket
- Adaptive Algorithms

---

# Default API Limits

## Anonymous Users

| Window | Limit |
|----------|-------|
| 1 Minute | 30 Requests |
| 1 Hour | 500 Requests |

---

## Authenticated Users

| Window | Limit |
|----------|-------|
| 1 Minute | 120 Requests |
| 1 Hour | 5,000 Requests |

---

## Administrative APIs

| Window | Limit |
|----------|-------|
| 1 Minute | 300 Requests |

Administrative endpoints remain authenticated.

---

# Authentication Limits

Login attempts

```
5 Attempts

per 15 Minutes

per IP
```

After exceeding the limit:

- Reject authentication
- Log security event
- Return retry information

---

# Resume Upload Limits

| Window | Limit |
|----------|-------|
| 1 Hour | 20 Uploads |
| 1 Day | 100 Uploads |

Rejected uploads return:

```
429 Too Many Requests
```

---

# AI Interview Limits

| Operation | Limit |
|------------|-------|
| Interview Creation | 10 / Hour |
| AI Evaluation | 50 / Day |
| Resume Analysis | 30 / Day |

Future subscription tiers may adjust these quotas.

---

# AI Token Budget

Each user receives a configurable AI token budget.

Budget applies to:

- Resume parsing
- Interview generation
- AI evaluation
- Follow-up questions

Requests exceeding quota are rejected until the budget resets.

---

# Burst Handling

Short traffic bursts are permitted within configured thresholds.

```text
Normal Traffic

↓

Temporary Burst

↓

Accepted

↓

Sustained Excess

↓

Rate Limited
```

---

# Distributed Rate Limiting

Production deployments should use centralized storage.

Recommended backend:

```
Redis
```

This ensures consistent limits across multiple application instances.

---

# Response Headers

Successful responses include:

```
X-RateLimit-Limit

X-RateLimit-Remaining

X-RateLimit-Reset
```

Rejected responses include:

```
Retry-After
```

---

# Error Response

Status

```
429 Too Many Requests
```

Example

```json
{
  "error": "RATE_LIMIT_EXCEEDED",
  "message": "Too many requests.",
  "retry_after": 60
}
```

---

# Adaptive Rate Limiting

Additional restrictions may be applied when detecting:

- Credential stuffing
- Prompt injection attempts
- Automated bots
- Upload flooding
- AI abuse
- Repeated authorization failures

Adaptive controls may temporarily reduce request limits.

---

# Monitoring

Track:

- Requests per second
- Rejected requests
- AI quota usage
- Upload frequency
- Authentication failures
- Geographic anomalies

Metrics feed operational dashboards and alerting systems.

---

# Alert Conditions

Generate alerts for:

- Sustained rate limit violations
- Login abuse
- AI token exhaustion spikes
- Distributed attack patterns
- Upload floods
- Excessive API failures

---

# Exemptions

Internal infrastructure may receive higher limits:

- Health checks
- Monitoring systems
- Deployment verification
- Internal service communication

All exemptions must be explicitly documented and audited.

---

# Business Rules

- Every public API is rate limited.
- Authenticated users receive higher quotas than anonymous users.
- AI requests consume user quotas.
- Rate limit violations generate audit events.
- Limits must be configurable without code changes.

---

# Future Enhancements

Planned improvements

- Tier-based quotas
- Organization-wide quotas
- Dynamic pricing limits
- Device fingerprinting
- Reputation-based throttling
- Machine learning anomaly detection

---

# Related Documents

- `api-security.md`
- `authentication.md`
- `audit-logging.md`
- `prompt-security.md`
- `incident-response.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial rate limiting architecture specification |