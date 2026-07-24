# Dashboard API

**Document ID:** API-011

**Version:** 1.0.0

**Status:** Approved

**Priority:** High

**Last Updated:** 2026-07-23

---

# Purpose

This document defines every API used to power the user dashboard.

The Dashboard API provides:

- Dashboard overview
- Interview statistics
- Performance trends
- Recent interviews
- AI recommendations
- Progress tracking
- Score analytics
- Achievement summaries

The dashboard aggregates information from multiple services into a single response.

---

# Resource

```
/dashboard
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
| Candidate | Own dashboard |
| Admin | Administrative dashboard |

---

# Dashboard Architecture

```text
Dashboard Request

↓

Authentication

↓

Interview Service

↓

Evaluation Service

↓

Reports Service

↓

History Service

↓

Analytics Aggregation

↓

Dashboard Response
```

---

# Endpoint Summary

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /dashboard | Dashboard overview |
| GET | /dashboard/statistics | Interview statistics |
| GET | /dashboard/trends | Score trends |
| GET | /dashboard/recent | Recent interviews |
| GET | /dashboard/recommendations | AI recommendations |
| GET | /dashboard/achievements | Achievements |

---

# GET /dashboard

## Purpose

Returns complete dashboard information.

---

Response

```json
{
  "success": true,
  "data": {
    "summary": {
      "total_interviews": 24,
      "completed_interviews": 21,
      "average_score": 84.6,
      "highest_score": 95,
      "current_streak": 6
    },
    "recent_interviews": [],
    "recommendations": [],
    "achievements": []
  }
}
```

---

# GET /dashboard/statistics

## Purpose

Returns interview statistics.

---

Response

```json
{
  "success": true,
  "data": {
    "total_interviews": 24,
    "completed": 21,
    "cancelled": 2,
    "failed": 1,
    "average_score": 84.6,
    "best_score": 95,
    "lowest_score": 68
  }
}
```

---

# GET /dashboard/trends

## Purpose

Returns historical performance data.

---

Query Parameters

```
period

limit
```

Supported Periods

```
7d

30d

90d

1y

all
```

---

Response

```json
{
  "success": true,
  "data": [
    {
      "date": "2026-07-01",
      "score": 72
    },
    {
      "date": "2026-07-10",
      "score": 84
    },
    {
      "date": "2026-07-22",
      "score": 91
    }
  ]
}
```

---

# GET /dashboard/recent

## Purpose

Returns recently completed interviews.

---

Response

```json
{
  "success": true,
  "data": [
    {
      "interview_id": "uuid",
      "type": "Technical",
      "mode": "Voice",
      "score": 91,
      "completed_at": "2026-07-22T17:00:00Z"
    }
  ]
}
```

---

# GET /dashboard/recommendations

## Purpose

Returns AI-generated recommendations.

---

Example Response

```json
{
  "success": true,
  "data": [
    {
      "priority": "high",
      "title": "Improve System Design",
      "description": "Practice scalable backend architecture."
    },
    {
      "priority": "medium",
      "title": "Communication",
      "description": "Provide more structured answers."
    }
  ]
}
```

---

# GET /dashboard/achievements

## Purpose

Returns earned achievements and milestones.

---

Example Response

```json
{
  "success": true,
  "data": [
    {
      "id": "first_interview",
      "title": "First Interview Completed",
      "earned_at": "2026-07-01T12:00:00Z"
    },
    {
      "id": "score_90",
      "title": "Scored Above 90",
      "earned_at": "2026-07-20T16:30:00Z"
    }
  ]
}
```

---

# Dashboard Widgets

Supported widgets

- Interview Summary
- Average Score
- Best Score
- Current Streak
- Recent Interviews
- Performance Trend
- Recommendations
- Achievements

Future widgets

- Weekly Goal
- Skill Heatmap
- Company Readiness
- Role Readiness

---

# Business Rules

- Dashboard data is read-only.
- Statistics are updated after interview completion.
- Recommendations are regenerated after every completed evaluation.
- Deleted interviews are excluded from analytics.

---

# Caching Strategy

| Endpoint | Cache Duration |
|-----------|----------------|
| Dashboard | 60 seconds |
| Statistics | 60 seconds |
| Trends | 5 minutes |
| Recent | 30 seconds |
| Recommendations | 5 minutes |
| Achievements | 10 minutes |

---

# Authorization

Every request validates:

- JWT
- User ownership
- Dashboard availability

---

# Rate Limits

| Endpoint | Limit |
|-----------|--------|
| Dashboard | 60/min |
| Statistics | 60/min |
| Trends | 30/min |
| Recent | 60/min |
| Recommendations | 30/min |
| Achievements | 30/min |

---

# Error Responses

Dashboard Not Available

```json
{
  "success": false,
  "error": {
    "code": "DASHBOARD_UNAVAILABLE",
    "message": "Dashboard data is temporarily unavailable."
  }
}
```

---

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

# OpenAPI Tags

```
Dashboard
```

---

# Related Documents

- `history.md`
- `reports.md`
- `evaluations.md`
- `pagination.md`
- `../04-database/entities/dashboard_views.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial Dashboard API specification |