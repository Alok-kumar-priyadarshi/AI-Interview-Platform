# Health & Monitoring API

**Document ID:** API-013

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines every operational endpoint used to monitor the health of the AI Career Interview Platform.

The Health API provides:

- Service health checks
- Readiness probes
- Liveness probes
- Dependency monitoring
- Infrastructure status
- Database connectivity
- AI provider connectivity
- Object storage status
- Metrics endpoint

These endpoints are primarily consumed by deployment platforms, monitoring systems, and administrators.

---

# Resource

```
/health
```

---

# Authentication

| Endpoint | Authentication |
|----------|----------------|
| Liveness | No |
| Readiness | No |
| Metrics | Admin |
| Detailed Status | Admin |

---

# Endpoint Summary

| Method | Endpoint | Purpose |
|---------|----------|----------|
| GET | /health | Overall health |
| GET | /health/live | Liveness probe |
| GET | /health/ready | Readiness probe |
| GET | /health/dependencies | Dependency status |
| GET | /health/metrics | Platform metrics |
| GET | /health/version | Application version |

---

# Health Architecture

```text
Health Request

↓

API Gateway

↓

Application

↓

Database

↓

Groq API

↓

Storage

↓

Return Status
```

---

# GET /health

## Purpose

Returns overall application health.

---

Response

```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": "2026-07-23T16:00:00Z",
    "version": "1.0.0",
    "uptime_seconds": 128340
  }
}
```

---

Status Values

```
Healthy

Degraded

Unhealthy
```

---

# GET /health/live

## Purpose

Liveness probe used by deployment platforms.

Returns only whether the application process is alive.

---

Response

```json
{
  "status": "alive"
}
```

---

HTTP Status

```
200 OK
```

---

# GET /health/ready

## Purpose

Readiness probe.

Determines whether the application is capable of serving traffic.

Checks

- Database connection
- AI provider connectivity
- Storage availability
- Configuration loaded

---

Response

```json
{
  "status": "ready"
}
```

---

Possible Responses

```
Ready

Not Ready
```

---

# GET /health/dependencies

## Purpose

Returns dependency status.

---

Authorization

```
Admin Only
```

---

Response

```json
{
  "success": true,
  "data": {
    "database": {
      "status": "healthy",
      "latency_ms": 8
    },
    "groq_api": {
      "status": "healthy",
      "latency_ms": 121
    },
    "storage": {
      "status": "healthy"
    }
  }
}
```

---

# GET /health/metrics

## Purpose

Returns operational metrics.

---

Authorization

```
Admin Only
```

---

Response

```json
{
  "success": true,
  "data": {
    "cpu_percent": 32.4,
    "memory_percent": 61.8,
    "active_requests": 17,
    "requests_per_minute": 145,
    "database_connections": 11,
    "queue_size": 4
  }
}
```

---

# GET /health/version

## Purpose

Returns deployed application version.

---

Response

```json
{
  "success": true,
  "data": {
    "application": "AI Career Interview Platform",
    "version": "1.0.0",
    "build": "20260723",
    "environment": "production"
  }
}
```

---

# Dependency Checks

Monitored Services

| Dependency | Purpose |
|------------|---------|
| PostgreSQL | Primary database |
| Groq API | LLM inference |
| Whisper API | Speech transcription |
| Object Storage | Resume & audio files |
| Background Worker | Async processing |

---

# Monitoring Metrics

Collected Metrics

- CPU utilization
- Memory utilization
- Disk utilization
- Active sessions
- API latency
- Queue length
- Failed requests
- Database latency
- AI latency
- Storage latency

---

# Business Rules

- Liveness must never depend on external services.
- Readiness must fail if critical dependencies are unavailable.
- Metrics are read-only.
- Dependency endpoints are restricted to administrators.
- Health endpoints should respond within 100 ms under normal conditions.

---

# Monitoring Integration

Supported Platforms

- Railway Health Checks
- Render Health Checks
- UptimeRobot
- Prometheus (future)
- Grafana (future)

---

# Rate Limits

| Endpoint | Limit |
|-----------|--------|
| /health | 300/min |
| /health/live | Unlimited |
| /health/ready | 300/min |
| /health/dependencies | 60/min |
| /health/metrics | 30/min |
| /health/version | 300/min |

---

# Error Responses

Service Unavailable

```json
{
  "success": false,
  "error": {
    "code": "SERVICE_UNAVAILABLE",
    "message": "One or more critical services are unavailable."
  }
}
```

---

Dependency Failure

```json
{
  "success": false,
  "error": {
    "code": "DEPENDENCY_FAILURE",
    "message": "Database connectivity check failed."
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
    "message": "Administrator access required."
  }
}
```

---

# OpenAPI Tags

```
Health
```

---

# Related Documents

- `admin.md`
- `errors.md`
- `../03-architecture/system-architecture.md`
- `../02-tech-stack/backend.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial Health & Monitoring API specification |