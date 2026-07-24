# Database Normalization Strategy

**Document ID:** DB-005

**Version:** 1.0.0

**Status:** Approved

**Priority:** High

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the normalization strategy used throughout the AI Career
Interview Platform database.

The objectives are:

- Eliminate unnecessary redundancy
- Preserve data integrity
- Simplify maintenance
- Improve consistency
- Balance normalization with application performance

Unless explicitly documented, every relational table is designed to satisfy
Third Normal Form (3NF).

---

# Normalization Goals

The database is designed to:

- Prevent duplicate data
- Avoid update anomalies
- Avoid insertion anomalies
- Avoid deletion anomalies
- Maintain referential integrity
- Support future schema evolution

---

# First Normal Form (1NF)

## Definition

A table satisfies First Normal Form when:

- Every row is unique.
- Every column stores a single atomic value.
- No repeating groups exist.
- Each column has one data type.

---

## Compliance

All relational tables satisfy 1NF.

Examples:

### Users

Correct

| id | name | email |
|----|------|-------|

Incorrect

| emails |
|---------|
| email1,email2,email3 |

---

### Interviews

Correct

| id | difficulty | status |

Incorrect

| difficulties |
|--------------|
| easy,medium |

---

### Candidate Profiles

Individual fields are stored separately.

Correct

```
experience_years

current_role

target_role
```

Not

```
profile_details
```

stored as a comma-separated string.

---

# Second Normal Form (2NF)

## Definition

A table satisfies Second Normal Form when:

- It is already in 1NF.
- Every non-key attribute depends on the whole primary key.

---

## Compliance

The platform uses UUID primary keys.

Since every table has a single-column primary key, partial dependency cannot
exist.

Examples:

### Resumes

```
resume_id

↓

file_name

uploaded_at

file_size
```

All attributes depend only on:

```
resume_id
```

---

### Interviews

All interview attributes depend on:

```
interview_id
```

---

### Reports

Every report attribute depends on:

```
report_id
```

---

# Third Normal Form (3NF)

## Definition

A table satisfies Third Normal Form when:

- It is already in 2NF.
- No non-key attribute depends on another non-key attribute.

---

## Compliance

Every relational table satisfies 3NF.

Examples:

### Users

Correct

```
user_id

↓

email

name

created_at
```

Incorrect

```
user_id

↓

email

email_domain
```

because:

```
email

↓

email_domain
```

creates a transitive dependency.

---

### Candidate Profiles

Current role and experience are stored directly.

Derived information such as:

```
Seniority

Career Level

Expected Salary
```

is computed by application services instead of being stored.

---

### Reports

Overall score is intentionally stored because it is:

- Frequently queried
- Computationally expensive to recalculate
- Immutable after report generation

This is an intentional denormalization decision.

---

# Denormalization Decisions

Some values are intentionally duplicated for performance.

---

## Report Scores

Instead of recalculating:

```
Interview

↓

Questions

↓

Answers

↓

Evaluations

↓

Average Score
```

the final score is stored directly.

Reason:

- Faster dashboard loading
- Simpler reporting
- Lower query complexity

---

## Executive Summary

Generated once and stored.

Reason:

- Expensive AI generation
- Immutable result
- Improved performance

---

## Improvement Roadmap

Stored inside the report.

Reason:

- AI-generated
- Candidate-facing
- Read frequently

---

# JSONB Usage

Several entities use PostgreSQL JSONB.

Examples:

```
strengths

weaknesses

evaluation_rubric

metadata

improvement_roadmap

expected_answer_points
```

---

## Why JSONB?

Reasons:

- Flexible schema
- AI-generated structures
- Easier future evolution
- Efficient PostgreSQL indexing
- Reduced migration frequency

---

## JSONB Design Rules

JSONB should only store:

- Variable-length collections
- AI-generated metadata
- Flexible configuration
- Nested recommendation objects

JSONB should NOT store:

- Foreign keys
- Core relational entities
- Frequently joined data
- Ownership relationships

---

# Redundancy Analysis

| Data | Stored Once | Duplicated |
|------|-------------|------------|
| Users | ✅ | ❌ |
| Resumes | ✅ | ❌ |
| Candidate Profiles | ✅ | ❌ |
| Interviews | ✅ | ❌ |
| Questions | ✅ | ❌ |
| Answers | ✅ | ❌ |
| Evaluations | ✅ | ❌ |
| Reports | Intentional | ✅ |

---

# Normalization Exceptions

The following are intentional:

## Overall Score

Stored in Reports.

Reason:

Avoid repeated aggregation.

---

## Executive Summary

Stored directly.

Reason:

Avoid repeated LLM invocation.

---

## AI Metadata

Stored in JSONB.

Reason:

Future model evolution.

---

# Performance Trade-offs

Normalized design improves:

- Consistency
- Integrity
- Maintainability

Denormalized data improves:

- Dashboard latency
- Report retrieval
- Analytics performance

The platform favors normalization unless:

- Recalculation is expensive
- AI generation is costly
- Read performance is critical

---

# Future Schema Evolution

Future additions should:

- Preserve 3NF where practical
- Avoid duplicate business data
- Prefer foreign keys over copied values
- Document every denormalization decision
- Justify all JSONB additions

---

# Review Checklist

Before adding a new column:

- Can it be derived?
- Does it duplicate existing information?
- Does it introduce transitive dependency?
- Does it belong in another table?
- Should it be modeled as a relationship?
- Is JSONB truly required?

---

# Related Documents

- `schema-overview.md`
- `relationships.md`
- `constraints.md`
- `indexes.md`
- `performance.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial normalization strategy specification |