# Database Technology Stack

**Document ID:** TS-004

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the database technologies, design philosophy,
data modeling standards, migration strategy, and operational guidelines
for the AI Career Interview Platform.

The database serves as the authoritative source of persistent data
and must prioritize correctness, consistency, security, and maintainability.

---

# Database Goals

The database must be:

- Reliable
- Consistent
- Secure
- Scalable
- Performant
- Maintainable
- Extensible
- Well documented

---

# Core Technology Stack

| Category | Technology |
|----------|------------|
| Database Engine | PostgreSQL 17 |
| ORM | SQLAlchemy 2.x |
| Migration Tool | Alembic |
| Driver | psycopg |
| Connection Pool | SQLAlchemy Pool |
| Query Language | SQL |
| Database Administration | pgAdmin (optional) |

---

# Why PostgreSQL?

PostgreSQL was selected because it provides:

- ACID compliance
- Excellent relational modeling
- Mature ecosystem
- Strong indexing capabilities
- JSON/JSONB support
- Transaction safety
- High reliability
- Excellent documentation
- Production-proven scalability

---

# Database Philosophy

The database is the system of record.

Business logic belongs in the application layer,
not inside stored procedures or triggers unless there is a compelling reason.

The schema should be:

- Explicit
- Predictable
- Normalized
- Easy to evolve

---

# Data Modeling Principles

The project follows these principles:

- Normalize data to at least Third Normal Form (3NF)
- Use foreign keys to enforce relationships
- Avoid duplicated data
- Use lookup/reference tables where appropriate
- Prefer explicit relationships over implicit conventions

---

# Entity Design Principles

Every entity should represent one business concept.

Examples:

- User
- Resume
- Interview
- InterviewQuestion
- InterviewAnswer
- Evaluation
- Feedback
- Session

Avoid "God tables" that mix unrelated concepts.

---

# Primary Key Strategy

All tables should use UUIDs as primary keys.

Example:

```
id UUID PRIMARY KEY
```

Benefits:

- Globally unique identifiers
- Safer for distributed systems
- Prevents predictable ID enumeration
- Easier future scaling

---

# Foreign Keys

Foreign keys must be explicitly declared.

Example:

```
resume.user_id
    →
users.id
```

Never rely solely on application logic to enforce relationships.

---

# Naming Conventions

Tables

Plural nouns.

Examples:

```
users
resumes
interviews
evaluations
```

Columns

snake_case

Examples:

```
created_at
updated_at
resume_score
interview_type
```

Constraints

```
pk_users
fk_resume_user
uq_user_email
```

Indexes

```
idx_user_email
idx_interview_created_at
```

---

# Standard Audit Columns

Every table should include:

```
id

created_at

updated_at
```

Where applicable:

```
created_by

updated_by
```

Soft-delete capable tables should also include:

```
deleted_at
```

---

# Soft Delete Strategy

Version 1 adopts soft deletes for user-owned business data.

Instead of deleting records:

```
deleted_at = CURRENT_TIMESTAMP
```

Benefits:

- Data recovery
- Auditability
- Reduced accidental data loss

System reference tables may use hard deletes when appropriate.

---

# Transactions

Transactions must be used whenever multiple related operations occur.

Examples:

- Creating an interview
- Saving interview answers
- Completing an evaluation

Either all operations succeed, or all are rolled back.

---

# Migration Strategy

Schema changes must be performed using Alembic.

Rules:

- Never modify production schemas manually.
- Every schema change requires a migration.
- Migrations must be version controlled.
- Migrations should be reversible whenever possible.

---

# Indexing Strategy

Create indexes for:

- Primary keys
- Foreign keys
- Frequently searched columns
- Authentication fields
- Sorting columns
- Reporting queries

Avoid excessive indexing because it slows writes.

---

# Constraints

Use database constraints whenever possible.

Examples:

- NOT NULL
- UNIQUE
- FOREIGN KEY
- CHECK
- DEFAULT

Prefer database-level enforcement over application-only validation.

---

# Connection Management

Connections should be managed by SQLAlchemy.

Guidelines:

- Use connection pooling.
- Close sessions properly.
- Avoid long-running transactions.
- Do not keep idle connections open unnecessarily.

---

# Query Guidelines

Queries should be:

- Parameterized
- Optimized
- Readable
- Indexed where appropriate

Avoid:

- SELECT *
- N+1 query problems
- Unbounded queries
- Unnecessary joins

---

# Data Integrity

Maintain integrity using:

- Primary keys
- Foreign keys
- Transactions
- Constraints
- Validation in the application layer

Integrity should never depend solely on frontend validation.

---

# Backup Strategy

Version 1 recommendations:

- Daily automated backups
- Retention policy (minimum 7 days)
- Test restore procedures periodically

Backups should be encrypted and stored securely.

---

# Security Guidelines

- Use least-privilege database users.
- Encrypt credentials.
- Store secrets in environment variables.
- Enforce SSL connections in production.
- Never expose the database directly to the internet.

---

# Performance Guidelines

Optimize:

- Query execution plans
- Index usage
- Pagination
- Batch operations
- Connection pooling

Measure before optimizing.

---

# Future Enhancements

Potential future additions:

- Read replicas
- Partitioning
- Sharding
- Materialized views
- Advanced indexing strategies
- Database monitoring
- Automated performance analysis

These are intentionally out of scope for Version 1.

---

# Related Documents

- `technology-overview.md`
- `backend-stack.md`
- `deployment-stack.md`
- `04-database/` (future detailed schema)
- `03-architecture/` (future)

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial database technology stack |