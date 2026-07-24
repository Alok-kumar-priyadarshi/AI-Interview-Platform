# Pagination & Filtering Standard

**Document ID:** API-015

**Version:** 1.0.0

**Status:** Approved

**Priority:** High

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the standard pagination, filtering, sorting, and search behavior for all collection endpoints.

Every API returning multiple resources must follow this specification.

Goals:

- Consistent API behavior
- Predictable frontend implementation
- Efficient database queries
- Stable sorting
- Extensible filtering
- Standard metadata

---

# Supported Resources

This standard applies to:

- Users
- Resumes
- Interviews
- Questions
- Answers
- Evaluations
- Reports
- History
- Admin resources

---

# Pagination Strategy

Version 1 uses offset-based pagination.

```
?page=1&page_size=20
```

Future versions may introduce cursor pagination for high-volume datasets.

---

# Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| page | Integer | No | Page number (default: 1) |
| page_size | Integer | No | Items per page |
| search | String | No | Full-text search |
| sort_by | String | No | Sort field |
| order | String | No | asc or desc |
| filters | Object | No | Resource-specific filters |

---

# Defaults

| Parameter | Default |
|-----------|----------|
| page | 1 |
| page_size | 20 |
| order | desc |

---

# Limits

| Parameter | Minimum | Maximum |
|-----------|----------|----------|
| page | 1 | Unlimited |
| page_size | 1 | 100 |

Requests exceeding limits return a validation error.

---

# Example Request

```
GET /history?page=2&page_size=20&sort_by=completed_at&order=desc
```

---

# Standard Response

```json
{
  "success": true,
  "data": {
    "items": [],
    "pagination": {
      "page": 2,
      "page_size": 20,
      "total_items": 184,
      "total_pages": 10,
      "has_next": true,
      "has_previous": true
    }
  }
}
```

---

# Pagination Fields

| Field | Description |
|---------|-------------|
| page | Current page |
| page_size | Requested page size |
| total_items | Total matching records |
| total_pages | Calculated page count |
| has_next | Whether another page exists |
| has_previous | Whether a previous page exists |

---

# Sorting

Supported order values

```
asc

desc
```

Common sortable fields

- created_at
- updated_at
- completed_at
- score
- duration
- difficulty
- name

Each endpoint documents any additional sortable fields.

---

# Filtering

Filtering is resource-specific.

Common filters include:

```
status

difficulty

mode

date_from

date_to

role

grade

score_min

score_max
```

Multiple filters may be combined.

Example

```
GET /history?difficulty=Hard&mode=Voice&score_min=80
```

---

# Search

Search uses the `search` query parameter.

Example

```
GET /users?search=john
```

Search behavior:

- Case-insensitive
- Partial matches
- Whitespace normalized

Each resource defines which fields are searchable.

---

# Validation Rules

- page must be ≥ 1
- page_size must be between 1 and 100
- order must be `asc` or `desc`
- sort_by must reference a supported field
- Invalid filters return HTTP 422

---

# Empty Results

An empty result is not an error.

Example

```json
{
  "success": true,
  "data": {
    "items": [],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total_items": 0,
      "total_pages": 0,
      "has_next": false,
      "has_previous": false
    }
  }
}
```

---

# Performance Guidelines

- Database indexes should support common sort fields.
- Avoid sorting on computed values when possible.
- Apply filters before pagination.
- Apply sorting before pagination.
- Return only requested page data.

---

# Future Cursor Pagination

For very large datasets, cursor pagination may be introduced.

Example

```
GET /history?cursor=eyJpZCI6IjEyMyJ9&limit=20
```

Cursor pagination will coexist with offset pagination during migration.

---

# Error Responses

Invalid Page

```json
{
  "success": false,
  "error": {
    "code": "INVALID_PAGE",
    "message": "Page number must be greater than or equal to 1."
  },
  "request_id": "req_page_001"
}
```

---

Invalid Sort Field

```json
{
  "success": false,
  "error": {
    "code": "INVALID_SORT_FIELD",
    "message": "Unsupported sort field."
  },
  "request_id": "req_sort_001"
}
```

---

Invalid Page Size

```json
{
  "success": false,
  "error": {
    "code": "INVALID_PAGE_SIZE",
    "message": "Page size must be between 1 and 100."
  },
  "request_id": "req_size_001"
}
```

---

# Business Rules

- All collection endpoints must implement pagination.
- Responses must include pagination metadata.
- Sorting must be deterministic.
- Empty collections return HTTP 200.
- Maximum page size is enforced consistently across the platform.

---

# OpenAPI Tags

```
Pagination

Filtering

Search
```

---

# Related Documents

- `errors.md`
- `history.md`
- `dashboard.md`
- `admin.md`
- `README.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial Pagination & Filtering standard |