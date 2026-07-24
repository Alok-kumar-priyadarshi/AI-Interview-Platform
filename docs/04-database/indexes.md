# Database Indexing Strategy

**Document ID:** DB-007

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the indexing strategy for the AI Career Interview
Platform database.

Proper indexing improves:

- Query latency
- Dashboard performance
- Report generation
- Search performance
- API responsiveness
- Scalability

Indexes are added only when they provide measurable performance benefits.

---

# Index Categories

The platform uses:

- Primary Indexes
- Secondary Indexes
- Composite Indexes
- Partial Indexes
- GIN Indexes
- Full-Text Search Indexes

---

# Primary Indexes

Every table has a clustered primary key index.

| Table | Primary Index |
|---------|---------------|
| users | pk_users |
| resumes | pk_resumes |
| candidate_profiles | pk_candidate_profiles |
| interviews | pk_interviews |
| interview_questions | pk_interview_questions |
| interview_answers | pk_interview_answers |
| evaluations | pk_evaluations |
| reports | pk_reports |
| audit_logs | pk_audit_logs |

---

# Secondary Indexes

## Users

```
idx_users_email
```

Reason

Fast login.

---

## Resumes

```
idx_resumes_user

idx_resumes_uploaded_at
```

Used for:

- Resume history
- Dashboard

---

## Candidate Profiles

```
idx_candidate_profiles_target_role
```

Useful for analytics.

---

## Interviews

```
idx_interviews_user

idx_interviews_status

idx_interviews_created_at

idx_interviews_type
```

Supports:

- Dashboard
- History
- Filtering

---

## Interview Questions

```
idx_questions_interview

idx_questions_category

idx_questions_difficulty
```

---

## Interview Answers

```
idx_answers_question

idx_answers_status

idx_answers_language

idx_answers_submitted_at
```

---

## Evaluations

```
idx_evaluations_answer

idx_evaluations_created_at

idx_evaluations_model
```

---

## Reports

```
idx_reports_interview

idx_reports_generated_at

idx_reports_recommendation

idx_reports_score
```

---

## Audit Logs

```
idx_audit_user

idx_audit_event_type

idx_audit_resource

idx_audit_request

idx_audit_occurred_at
```

---

# Composite Indexes

Composite indexes support multi-column filtering.

---

## Interviews

```
(user_id, created_at DESC)
```

Used by:

```
Interview History
```

---

## Questions

```
(interview_id, question_number)
```

Supports ordered retrieval.

---

## Reports

```
(hiring_recommendation, overall_score)
```

Supports analytics.

---

## Audit Logs

```
(user_id, occurred_at DESC)

(event_type, occurred_at DESC)

(resource_type, resource_id)
```

Supports investigations.

---

# Partial Indexes

Useful when only a subset of rows is queried.

---

## Active Interviews

```sql
WHERE status='in_progress'
```

---

## Completed Interviews

```sql
WHERE status='completed'
```

---

## Generated Reports

```sql
WHERE pdf_generated=TRUE
```

---

## Failed Audit Events

```sql
WHERE severity='critical'
```

---

# JSONB GIN Indexes

Several JSONB columns require GIN indexes.

---

## Evaluations

```
strengths

weaknesses

improvement_suggestions
```

---

## Reports

```
improvement_roadmap
```

---

## Questions

```
evaluation_rubric

expected_answer_points
```

---

## Audit Logs

```
metadata
```

---

## Example

```sql
CREATE INDEX idx_reports_roadmap_gin

ON reports

USING GIN(improvement_roadmap);
```

---

# Full-Text Search

The platform supports PostgreSQL Full-Text Search.

Indexed fields:

- Resume extracted text
- Question text
- Executive summary
- Detailed feedback

---

Example

```sql
CREATE INDEX idx_questions_fts

ON interview_questions

USING GIN(to_tsvector('english', question_text));
```

---

# Unique Indexes

Automatically created by UNIQUE constraints.

Examples:

```
users.email

reports.interview_id

evaluations.answer_id

candidate_profiles.user_id

(interview_id, question_number)
```

---

# Index Naming Convention

Primary

```
pk_<table>
```

---

Secondary

```
idx_<table>_<column>
```

---

Composite

```
idx_<table>_<column1>_<column2>
```

---

GIN

```
gin_<table>_<column>
```

---

FTS

```
fts_<table>_<column>
```

---

Unique

```
uq_<table>_<column>
```

---

# Query Optimization

Indexes should optimize:

- Login
- Resume retrieval
- Candidate dashboard
- Interview history
- Report retrieval
- AI evaluation lookup
- Audit investigation

Avoid indexes on columns with:

- Low selectivity
- Rare filtering
- Frequent updates
- Temporary values

---

# Maintenance Strategy

Indexes require periodic maintenance.

Recommended tasks:

- Monitor index usage
- Remove unused indexes
- Rebuild fragmented indexes
- Update planner statistics
- Vacuum tables regularly

---

# Monitoring

Track:

- Index scan count
- Sequential scan count
- Index size
- Bloat percentage
- Slow queries
- Missing indexes

Useful PostgreSQL views:

- `pg_stat_user_indexes`
- `pg_stat_all_indexes`
- `pg_stat_statements`

---

# PostgreSQL Examples

## Composite Index

```sql
CREATE INDEX idx_interviews_user_created

ON interviews(user_id, created_at DESC);
```

---

## Partial Index

```sql
CREATE INDEX idx_completed_interviews

ON interviews(created_at)

WHERE status='completed';
```

---

## GIN Index

```sql
CREATE INDEX gin_metadata

ON audit_logs

USING GIN(metadata);
```

---

## Full-Text Search Index

```sql
CREATE INDEX fts_feedback

ON evaluations

USING GIN(to_tsvector('english', detailed_feedback));
```

---

# Design Principles

- Prefer indexes that match production query patterns.
- Keep indexes narrow where possible.
- Avoid duplicate indexes.
- Prefer composite indexes over multiple overlapping indexes.
- Monitor index effectiveness continuously.

---

# Related Documents

- `constraints.md`
- `performance.md`
- `schema-overview.md`
- `relationships.md`
- `migrations.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial database indexing strategy specification |