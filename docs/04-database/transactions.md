# Database Transaction Strategy

**Document ID:** DB-009

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines transaction management for the AI Career Interview Platform.

Transactions guarantee:

- Atomicity
- Consistency
- Isolation
- Durability

Every critical business workflow must execute inside well-defined transaction boundaries.

---

# Objectives

The transaction strategy aims to:

- Prevent partial writes
- Preserve referential integrity
- Avoid inconsistent states
- Support concurrent users
- Minimize lock contention
- Enable safe retries

---

# ACID Guarantees

## Atomicity

Every transaction succeeds completely or fails completely.

Example:

```
Create Interview

↓

Generate Questions

↓

Store Questions

↓

Commit
```

If any step fails:

```
Rollback Entire Transaction
```

---

## Consistency

Database constraints must always remain valid.

Examples:

- No orphan records
- Foreign keys always valid
- Unique constraints preserved

---

## Isolation

Concurrent users must not interfere with each other.

Each interview should behave independently.

---

## Durability

Committed transactions survive:

- Server restart
- Process crash
- Application failure

Durability is provided by PostgreSQL WAL.

---

# Transaction Boundaries

---

## Resume Upload

Single transaction.

Workflow:

```text
Upload Resume

↓

Store Metadata

↓

Parse Resume

↓

Update Candidate Profile

↓

Commit
```

Rollback if:

- File metadata fails
- Parsing fails
- Profile update fails

---

## Interview Creation

Single transaction.

Workflow:

```text
Create Interview

↓

Generate Questions

↓

Insert Questions

↓

Commit
```

Rollback if:

- AI generation fails
- Database insert fails

No partially created interviews should exist.

---

## Answer Submission

Single transaction.

Workflow:

```text
Receive Answer

↓

Store Answer

↓

Update Interview Progress

↓

Commit
```

Voice interviews:

```text
Upload Audio

↓

Store Audio Metadata

↓

Commit

↓

Asynchronous Transcription
```

Large audio processing should not keep database transactions open.

---

## Evaluation

Single transaction.

Workflow:

```text
Load Answer

↓

Generate Evaluation

↓

Store Evaluation

↓

Commit
```

Rollback if evaluation storage fails.

---

## Report Generation

Single transaction.

Workflow:

```text
Aggregate Scores

↓

Generate Report

↓

Store Report

↓

Commit
```

PDF generation should execute after commit.

---

## User Registration

Single transaction.

Workflow:

```text
Google Login

↓

Create User

↓

Create Default Profile

↓

Commit
```

---

# Isolation Levels

Default isolation level:

```
READ COMMITTED
```

Reason:

- Good concurrency
- Suitable for OLTP workloads
- PostgreSQL default

---

## Higher Isolation

Use

```
REPEATABLE READ
```

when:

- Multiple reads must remain consistent.

Example:

- Analytics
- Reporting

---

## SERIALIZABLE

Use only when absolutely required.

Reasons:

- Higher overhead
- Greater lock contention
- Reduced throughput

Not recommended for standard interview workflows.

---

# Locking Strategy

Prefer optimistic concurrency.

Avoid long-lived locks.

Use row-level locking only when necessary.

---

## Row Lock Example

```sql
SELECT *

FROM interviews

WHERE id = ?

FOR UPDATE;
```

Use when updating interview status.

---

# Deadlock Prevention

Rules:

- Access tables in consistent order.
- Keep transactions short.
- Avoid unnecessary locks.
- Commit immediately after work completes.

---

# Retry Strategy

Retry automatically for:

- Deadlocks
- Serialization failures
- Temporary connection issues

Do not retry:

- Validation failures
- Constraint violations
- Business rule violations

---

# Idempotency

Operations that may be retried must be idempotent.

Examples:

Safe:

- Report generation
- Resume parsing
- Evaluation creation (using unique keys)

Unsafe:

- Duplicate interview creation
- Duplicate answer submission

---

# Asynchronous Operations

The following tasks execute outside database transactions:

- Speech transcription
- Resume embedding generation
- Vector indexing
- PDF rendering
- Email notifications
- Analytics updates

Database transaction should commit before background work starts.

---

# SQLAlchemy Implementation

Preferred pattern:

```python
with Session.begin() as session:
    session.add(interview)
    session.add_all(questions)
```

Automatic behavior:

- Commit on success
- Rollback on exception

---

# FastAPI Integration

Example:

```python
def create_interview(
    db: Session,
):
    with db.begin():
        ...
```

Never manually commit multiple times inside one business transaction.

---

# Error Handling

On exception:

```text
Exception

↓

Rollback

↓

Log Error

↓

Return Error Response
```

Never leave transactions open.

---

# Long-Running Operations

Avoid placing these inside transactions:

- LLM calls
- Audio transcription
- PDF generation
- Email sending
- Background analytics

Instead:

```text
Commit

↓

Publish Background Job

↓

Process Asynchronously
```

---

# Monitoring

Track:

- Transaction duration
- Rollback rate
- Deadlock count
- Lock wait time
- Long-running transactions

Alert thresholds should be defined in production monitoring.

---

# Design Principles

- Keep transactions short.
- Avoid nested transactions.
- Commit only after all writes succeed.
- Roll back on any unrecoverable error.
- Separate database work from long-running AI tasks.
- Prefer background workers for expensive processing.

---

# Related Documents

- `constraints.md`
- `relationships.md`
- `migrations.md`
- `performance.md`
- `backup-recovery.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial database transaction strategy specification |