# Database Migration Strategy

**Document ID:** DB-008

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the migration strategy for the AI Career Interview
Platform.

Database migrations ensure that schema changes are:

- Version controlled
- Repeatable
- Reversible
- Tested
- Safe for production deployment

All schema modifications must be performed through Alembic migrations.

---

# Technology

Migration Framework

```
Alembic
```

ORM

```
SQLAlchemy
```

Database

```
PostgreSQL
```

---

# Migration Objectives

Every migration should be:

- Deterministic
- Idempotent where practical
- Reversible
- Atomic
- Peer reviewed
- Tested before production

---

# Directory Structure

```
backend/

└── alembic/

    ├── env.py

    ├── script.py.mako

    ├── versions/

    │     ├── 20260723_create_users.py

    │     ├── 20260724_add_reports.py

    │     └── ...
    │
    └── README.md
```

---

# Migration Lifecycle

```text
Schema Change Required

↓

Modify SQLAlchemy Models

↓

Generate Migration

↓

Review Migration

↓

Test Migration

↓

Apply to Development

↓

Apply to Staging

↓

Apply to Production
```

---

# Creating a Migration

Autogenerate migration:

```bash
alembic revision --autogenerate -m "create_reports_table"
```

Manual migration:

```bash
alembic revision -m "add_candidate_profile_index"
```

---

# Applying Migrations

Upgrade to latest:

```bash
alembic upgrade head
```

Upgrade to a specific revision:

```bash
alembic upgrade <revision_id>
```

---

# Rolling Back

Rollback one revision:

```bash
alembic downgrade -1
```

Rollback to a revision:

```bash
alembic downgrade <revision_id>
```

Rollback to base:

```bash
alembic downgrade base
```

---

# Migration Naming Convention

Migration message format:

```
create_users_table

create_reports_table

add_resume_indexes

add_question_category

remove_unused_column

rename_interview_status
```

Migration filenames should clearly describe the schema change.

---

# Revision Guidelines

Every migration contains:

- Revision ID
- Parent Revision
- Upgrade function
- Downgrade function

Example:

```python
revision = "7c92b2"

down_revision = "4fd182"
```

---

# Upgrade Rules

Upgrade functions may:

- Create tables
- Drop tables
- Add columns
- Remove columns
- Rename columns
- Create indexes
- Remove indexes
- Add constraints
- Remove constraints

Upgrade functions should avoid destructive data loss whenever possible.

---

# Downgrade Rules

Every migration must provide a downgrade path.

Downgrades should:

- Restore removed schema
- Remove added schema
- Preserve data where possible

If a downgrade cannot safely restore data, document the limitation clearly.

---

# Branching Strategy

Only one migration head should exist.

When multiple branches create migration conflicts:

```bash
alembic merge
```

Merge migrations should be reviewed before deployment.

---

# Zero-Downtime Guidelines

Production deployments should avoid breaking running applications.

Preferred strategy:

```text
Add Column

↓

Deploy Application

↓

Backfill Data

↓

Switch Reads

↓

Remove Old Column
```

Avoid:

- Dropping active columns
- Renaming columns without compatibility
- Long-running locks

---

# Seed Data

Schema migrations should not contain business seed data.

Allowed:

- Lookup tables
- Default roles
- Required system configuration

Disallowed:

- Demo users
- Test resumes
- Mock interviews

Seed data should be managed separately.

---

# Environment Promotion

Deployment order:

```text
Local

↓

Development

↓

Testing

↓

Staging

↓

Production
```

Never skip an environment for production schema changes.

---

# Migration Testing

Every migration should be tested for:

- Successful upgrade
- Successful downgrade
- Existing data preservation
- Constraint validation
- Index creation
- Performance impact

---

# Data Migration Strategy

Schema changes and data migrations should be separated whenever practical.

Preferred workflow:

```text
Migration 1

↓

Deploy

↓

Background Data Migration

↓

Migration 2

↓

Cleanup
```

---

# Production Deployment Checklist

Before applying migrations:

- Backup database
- Verify migration ordering
- Review generated SQL
- Test on staging
- Confirm rollback procedure
- Notify stakeholders if required

---

# Failure Recovery

If a migration fails:

1. Stop deployment.
2. Investigate failure.
3. Restore backup if necessary.
4. Roll back migration.
5. Fix migration.
6. Redeploy.

Never manually modify production schema without a tracked migration.

---

# PostgreSQL Guidelines

Recommended practices:

- Prefer transactional DDL where supported.
- Create indexes concurrently for very large tables.
- Avoid locking large tables during peak traffic.
- Keep migrations small and focused.

---

# Migration Review Checklist

Before merging a migration:

- Naming follows convention
- Upgrade works
- Downgrade works
- Constraints validated
- Indexes reviewed
- No unnecessary schema changes
- Documentation updated

---

# Related Documents

- `schema-overview.md`
- `constraints.md`
- `indexes.md`
- `transactions.md`
- `performance.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial database migration strategy specification |