# PostgreSQL Deployment Architecture

**Document ID:** DEP-005

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the deployment architecture for the PostgreSQL database used by the AI Career Interview Platform.

The database is the authoritative source of persistent business data and is deployed as a managed PostgreSQL instance on Railway.

---

# Objectives

The database deployment architecture aims to provide:

- Reliable persistence
- High data integrity
- Secure storage
- Automated backups
- Efficient query execution
- Easy schema evolution
- Disaster recovery
- Future scalability

---

# Technology Stack

Database Engine

- PostgreSQL 16+

Hosting Platform

- Railway PostgreSQL

ORM

- SQLAlchemy

Migration Tool

- Alembic

Connection Driver

- psycopg

---

# Database Architecture

```text
FastAPI Backend

↓

SQLAlchemy ORM

↓

Connection Pool

↓

Railway PostgreSQL

↓

Persistent Storage
```

The backend is the only component allowed to communicate with the database.

---

# Responsibilities

The database stores:

- Users
- Authentication records
- Resume metadata
- Interview sessions
- Interview questions
- Candidate answers
- AI evaluations
- Progress analytics
- Chat history
- Audit logs
- Application settings

---

# Database Principles

The production database follows:

- ACID compliance
- Strong consistency
- Referential integrity
- Normalized schema
- Controlled denormalization when justified
- Versioned migrations

---

# Connection Strategy

The backend connects using pooled database connections.

Recommended configuration:

- Connection pooling enabled
- Connection timeout configured
- Idle timeout configured
- Automatic reconnect
- SSL enforced

Connections should never remain idle unnecessarily.

---

# SSL Configuration

Production connections must use:

```text
SSL Mode

require
```

Database credentials are transmitted only over encrypted connections.

---

# Schema Management

Schema changes are managed exclusively using Alembic.

Deployment flow

```text
Deploy

↓

Run Migration

↓

Verify

↓

Start Application
```

Manual schema modifications are prohibited.

---

# Migration Rules

Every migration must:

- Be version controlled
- Be reviewed
- Be repeatable
- Include downgrade logic where practical
- Be tested in staging

Migration files must never be edited after deployment.

---

# Indexing Strategy

Indexes should exist for:

- Primary keys
- Foreign keys
- Frequently searched columns
- Login identifiers
- Resume ownership
- Interview lookup
- Dashboard queries
- History retrieval

Indexes should be reviewed periodically.

---

# Constraints

Database constraints include:

- Primary keys
- Foreign keys
- Unique constraints
- Check constraints
- NOT NULL constraints

Business rules should be enforced in both the application and database where appropriate.

---

# Transaction Management

Use transactions for:

- Interview creation
- Resume upload metadata
- AI evaluation persistence
- User registration
- Profile updates

Transactions should be short-lived.

---

# Backup Strategy

Automated backups should include:

- Daily full backups
- Incremental backups where supported
- Backup verification
- Secure storage
- Defined retention policy

Backups must be encrypted.

---

# Recovery Strategy

Recovery objectives

Recovery Time Objective (RTO)

- Less than 30 minutes

Recovery Point Objective (RPO)

- Less than 15 minutes

Recovery procedures should be tested regularly.

---

# Monitoring

Monitor:

- Connection count
- Active sessions
- Query latency
- Slow queries
- Lock contention
- Disk usage
- CPU utilization
- Memory usage
- Replication status (future)

Alerts should be configured for abnormal thresholds.

---

# Query Optimization

Recommended practices:

- Use indexes appropriately
- Avoid N+1 queries
- Limit returned columns
- Paginate large datasets
- Analyze execution plans
- Optimize joins

---

# Maintenance

Routine maintenance includes:

- VACUUM
- ANALYZE
- Index maintenance
- Statistics updates
- Backup verification
- Migration review

Maintenance should be scheduled during low-traffic periods where possible.

---

# Scaling Strategy

Version 1

- Vertical scaling
- Query optimization
- Connection pooling

Future enhancements

- Read replicas
- Partitioning
- Logical replication
- Multi-region deployment
- Sharding (if justified)

---

# Security

Database security requires:

- Private credentials
- SSL connections
- Least-privilege accounts
- Encrypted backups
- Strong authentication
- Network isolation
- Audit logging

Production credentials must never be shared.

---

# Failure Handling

Recover gracefully from:

- Database restart
- Connection exhaustion
- Temporary network failures
- Query timeout
- Deadlocks
- Disk space warnings

Applications should retry transient failures appropriately.

---

# Deployment Validation

Verify:

- Database connectivity
- Schema version
- Migration completion
- Index creation
- Connection pool
- CRUD operations
- Transaction integrity

---

# Operational Best Practices

- Use migrations exclusively.
- Monitor slow queries.
- Keep transactions short.
- Review indexes regularly.
- Validate backups frequently.

---

# Anti-Patterns

Avoid:

- Manual schema edits
- Long-running transactions
- Missing indexes
- Storing binary files
- Hardcoded credentials
- Excessive table locking

---

# Business Rules

- PostgreSQL is the system of record.
- Every schema change requires an Alembic migration.
- Production databases are backed up automatically.
- SSL is mandatory.
- Database changes require successful staging validation before production deployment.

---

# Related Documents

- `backend-deployment.md`
- `environment-variables.md`
- `rollback-strategy.md`
- `backup-recovery.md`
- `monitoring.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial PostgreSQL deployment architecture specification |