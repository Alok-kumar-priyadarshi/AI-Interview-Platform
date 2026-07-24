# Interview History API

**Document ID:** API-010

**Version:** 1.0.0

**Status:** Approved

**Priority:** High

**Last Updated:** 2026-07-23

---

# Purpose

This document defines every API related to interview history management.

The History API provides:

- Interview history retrieval
- Search functionality
- Filtering
- Pagination
- Sorting
- Historical reports
- Historical evaluations
- Archived interview access

Every completed interview remains accessible unless explicitly deleted.

---

# Resource

```
/history
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
| Candidate | Own history |
| Admin | All history |

---

# History Lifecycle

```text
Interview Created

↓

Interview Completed

↓

Evaluation Generated

↓

Report Generated

↓

History Record Created

↓

Available For Search
```

---

# Endpoint Summary

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /history | Interview history |
| GET | /history/{history_id} | History details |
| GET | /history/search | Search history |
| GET | /history/archive | Archived interviews |
| DELETE | /history/{history_id} | Delete history |

---

# GET /history

## Purpose

Returns paginated interview history.

---

Query Parameters

```
page

page_size

sort

status

difficulty

mode

interview_type

date_from

date_to
```

---

Example

```
GET /history?page=1&page_size=20&difficulty=hard
```

---

Response

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "history_id": "uuid",
        "interview_id": "uuid",
        "completed_at": "2026-07-23T14:00:00Z",
        "overall_score": 88,
        "grade": "A",
        "difficulty": "Hard",
        "mode": "Voice"
      }
    ],
    "page": 1,
    "page_size": 20,
    "total": 84
  }
}
```

---

# GET /history/{history_id}

## Purpose

Returns a complete history record.

---

Response

```json
{
  "success": true,
  "data": {
    "history_id": "uuid",
    "interview_id": "uuid",
    "report_id": "uuid",
    "evaluation_id": "uuid",
    "overall_score": 88,
    "grade": "A",
    "duration_minutes": 42,
    "completed_at": "2026-07-23T14:00:00Z"
  }
}
```

---

# GET /history/search

## Purpose

Searches interview history.

---

Supported Filters

```
Interview Type

Difficulty

Mode

Date Range

Minimum Score

Maximum Score

Grade

Keyword
```

---

Example

```
GET /history/search?keyword=backend
```

---

Response

```json
{
  "success": true,
  "data": {
    "items": []
  }
}
```

---

# GET /history/archive

## Purpose

Returns archived interviews.

Version 1

```
Archive == Completed Interviews
```

Future versions may support manual archiving.

---

# DELETE /history/{history_id}

## Purpose

Deletes a history record.

Deletion also removes:

- Report reference
- Evaluation reference
- Search index

Associated interview data may be retained according to platform retention policy.

---

Response

```json
{
  "success": true,
  "message": "History deleted successfully."
}
```

---

# Searchable Fields

Every history record supports searching by:

- Interview type
- Difficulty
- Mode
- Date
- Grade
- Score
- Resume name
- Target role

---

# Sorting

Supported

```
Newest

Oldest

Highest Score

Lowest Score

Duration
```

---

# Pagination

Default

```
20 items/page
```

Maximum

```
100 items/page
```

---

# Business Rules

- Every completed interview creates one history record.
- Failed interviews are excluded.
- Deleted interviews disappear from history.
- Reports remain linked until deletion.
- History is read-only except deletion.

---

# Authorization

Every request validates:

- JWT
- User ownership
- Record existence

---

# Rate Limits

| Endpoint | Limit |
|-----------|--------|
| History List | 60/min |
| Search | 60/min |
| History Details | 60/min |
| Archive | 30/min |
| Delete | 10/day |

---

# Error Responses

History Not Found

```json
{
  "success": false,
  "error": {
    "code": "HISTORY_NOT_FOUND",
    "message": "History record does not exist."
  }
}
```

---

Invalid Filter

```json
{
  "success": false,
  "error": {
    "code": "INVALID_FILTER",
    "message": "One or more filters are invalid."
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
History
```

---

# Related Documents

- `reports.md`
- `dashboard.md`
- `pagination.md`
- `errors.md`
- `../04-database/entities/history.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial Interview History API specification |