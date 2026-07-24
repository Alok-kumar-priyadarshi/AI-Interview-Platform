# Database Performance Strategy

**Document ID:** DB-010

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the database performance strategy for the AI Career
Interview Platform.

The goals are to:

- Maintain low API latency
- Support concurrent interviews
- Scale efficiently
- Minimize database contention
- Ensure predictable production performance

Performance optimization should always preserve correctness.

---

# Performance Objectives

Target goals:

- Fast query execution
- Minimal lock contention
- Low connection wait time
- Efficient index usage
- Stable performance under increasing load

---

# Expected Scale (Version 1)

Daily Active Users

```
5,000+
```

Registered Users

```
100,000+
```

Resumes

```
500,000+
```

Interviews

```
1,000,000+
```

Interview Questions

```
10,000,000+
```

Audit Logs

```
100,000,000+
```

The schema should support future horizontal scaling.

---

# Query Optimization

General rules:

- Select only required columns.
- Prefer indexed lookups.
- Avoid SELECT *.
- Keep joins simple.
- Limit result sets.
- Use pagination.

---

## Good Example

```sql
SELECT id,
       status,
       created_at

FROM interviews

WHERE user_id = ?

ORDER BY created_at DESC

LIMIT 20;
```

---

## Avoid

```sql
SELECT *

FROM interviews;
```

---

# Pagination Strategy

Always paginate collections.

Preferred:

```
LIMIT

OFFSET
```

Future optimization:

```
Cursor Pagination
```

For:

- Interview history
- Reports
- Audit logs

---

# Connection Pooling

Connection pooling is managed by SQLAlchemy.

Recommended values:

```
pool_size = 20

max_overflow = 10

pool_timeout = 30

pool_recycle = 1800
```

Avoid opening new database connections per request.

---

# Caching Strategy

Database should not repeatedly execute expensive queries.

Candidate caching opportunities:

- Candidate profile
- Dashboard summary
- Resume metadata
- Interview configuration
- Lookup tables

Cache invalidation should occur immediately after updates.

---

# Read Patterns

Most frequent reads:

- Candidate dashboard
- Interview history
- Latest report
- Resume retrieval
- Question retrieval

Indexes should prioritize these workloads.

---

# Write Patterns

Most frequent writes:

- Resume uploads
- Answer submissions
- Audit logs
- Evaluations
- Reports

Write amplification should remain minimal.

---

# Batch Operations

Preferred for:

- Analytics
- Historical imports
- Cleanup jobs
- Backfills

Avoid inserting very large datasets one row at a time.

---

# Partitioning Strategy

Version 1

No partitioning required.

Future candidate tables:

- audit_logs
- interviews
- interview_answers

Potential strategy:

```
Monthly Partitioning
```

or

```
Yearly Partitioning
```

---

# VACUUM Strategy

PostgreSQL should regularly perform:

```
VACUUM

ANALYZE
```

Autovacuum remains enabled.

Monitor:

- Dead tuples
- Table bloat
- Index bloat

---

# ANALYZE

Statistics should remain current.

ANALYZE helps PostgreSQL choose optimal query plans.

Run after:

- Large imports
- Bulk updates
- Bulk deletes

---

# Slow Query Monitoring

Track queries exceeding:

```
100 ms
```

Investigate:

- Missing indexes
- Sequential scans
- Large joins
- Poor execution plans

Use:

```sql
EXPLAIN ANALYZE
```

before optimizing.

---

# PostgreSQL Tuning

Recommended baseline:

```
shared_buffers

work_mem

maintenance_work_mem

effective_cache_size

max_connections
```

Tune based on:

- Available RAM
- CPU cores
- Storage performance

---

# Storage Optimization

Prefer:

- UUID primary keys
- JSONB for flexible metadata
- TEXT only where necessary

Avoid storing:

- Temporary AI outputs
- Duplicate derived values
- Large binary files

Audio and PDFs should be stored externally.

---

# Benchmarking

Benchmark common workflows:

- Login
- Resume upload
- Interview creation
- Question retrieval
- Answer submission
- Report generation
- Dashboard loading

Measure:

- Latency
- Throughput
- Error rate

---

# Performance Targets

| Operation | Target |
|-----------|--------|
| Login | <100 ms |
| Dashboard | <200 ms |
| Resume Metadata Fetch | <100 ms |
| Interview History | <150 ms |
| Question Retrieval | <50 ms |
| Answer Insert | <50 ms |
| Evaluation Insert | <100 ms |
| Report Retrieval | <100 ms |

Targets exclude LLM inference time.

---

# Monitoring

Track:

- Query latency
- Transactions per second
- Active connections
- Lock waits
- Cache hit ratio
- Sequential scans
- Index usage
- CPU utilization
- Memory utilization

---

# Alert Thresholds

Examples:

Query latency

```
>100 ms
```

Connection pool exhaustion

```
>90%
```

Database CPU

```
>80%
```

Replication lag (future)

```
>5 seconds
```

---

# Scalability Roadmap

Version 1

- Single PostgreSQL instance

Version 2

- Read replicas

Version 3

- Partitioned tables

Version 4

- Multi-region deployment

Version 5

- Sharding if required

---

# Performance Review Checklist

Before production:

- Queries indexed
- No unnecessary SELECT *
- Pagination implemented
- Slow queries reviewed
- Execution plans analyzed
- Connection pooling configured
- Autovacuum verified
- Monitoring enabled

---

# Design Principles

- Optimize measured bottlenecks.
- Prefer simpler queries.
- Index for real workloads.
- Keep transactions short.
- Cache where appropriate.
- Avoid premature optimization.

---

# Related Documents

- `indexes.md`
- `transactions.md`
- `constraints.md`
- `backup-recovery.md`
- `governance.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial database performance strategy specification |