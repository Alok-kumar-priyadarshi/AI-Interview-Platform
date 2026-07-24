# Database Constraints

**Document ID:** DB-006

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines every database constraint used throughout the AI Career
Interview Platform.

Database constraints ensure:

- Data integrity
- Business rule enforcement
- Referential integrity
- Data consistency
- Protection against invalid records

The database—not only the application—is responsible for enforcing critical
validation rules.

---

# Constraint Categories

The platform uses the following constraint types:

- Primary Keys
- Foreign Keys
- Unique Constraints
- NOT NULL Constraints
- CHECK Constraints
- DEFAULT Constraints

---

# Primary Keys

## Purpose

Every table must have one immutable primary key.

The platform uses UUID Version 4 identifiers.

Example:

```sql
id UUID PRIMARY KEY
```

---

## Tables

| Table | Primary Key |
|---------|-------------|
| users | id |
| resumes | id |
| candidate_profiles | id |
| interviews | id |
| interview_questions | id |
| interview_answers | id |
| evaluations | id |
| reports | id |
| audit_logs | id |

---

## Rules

Primary keys:

- Must be unique
- Must never change
- Must not contain business meaning
- Must not be reused

---

# Foreign Keys

## Purpose

Foreign keys preserve referential integrity.

Child records cannot exist without valid parents unless explicitly documented.

---

## Foreign Key Matrix

| Child | Parent |
|---------|---------|
| resumes.user_id | users.id |
| candidate_profiles.user_id | users.id |
| interviews.user_id | users.id |
| interview_questions.interview_id | interviews.id |
| interview_answers.question_id | interview_questions.id |
| evaluations.answer_id | interview_answers.id |
| reports.interview_id | interviews.id |
| audit_logs.user_id | users.id |

---

## Delete Policies

| Relationship | Policy |
|--------------|--------|
| User → Resume | CASCADE |
| User → Candidate Profile | CASCADE |
| User → Interview | CASCADE |
| User → Audit Log | SET NULL |
| Interview → Question | CASCADE |
| Question → Answer | CASCADE |
| Answer → Evaluation | CASCADE |
| Interview → Report | CASCADE |

---

# Unique Constraints

## Purpose

Prevent duplicate business records.

---

## Defined Unique Constraints

### Users

```
email
```

---

### Candidate Profiles

```
user_id
```

One profile per user.

---

### Interview Questions

```
(interview_id, question_number)
```

Each interview has a unique question order.

---

### Interview Answers

```
question_id
```

Version 1 allows one answer per question.

---

### Evaluations

```
answer_id
```

One evaluation per answer.

---

### Reports

```
interview_id
```

One report per interview.

---

# NOT NULL Constraints

## Purpose

Ensure mandatory business data always exists.

---

## Required Columns

### Users

- id
- email
- name
- created_at

---

### Resumes

- id
- user_id
- file_name
- file_type
- storage_path
- uploaded_at

---

### Interviews

- id
- user_id
- interview_type
- difficulty
- status

---

### Questions

- interview_id
- question_text
- category
- difficulty

---

### Answers

- question_id
- answer_type

---

### Evaluations

- answer_id
- overall_score
- evaluation_model

---

### Reports

- interview_id
- overall_score
- executive_summary
- hiring_recommendation

---

# CHECK Constraints

## Purpose

Restrict values to valid domains.

---

## Interview Difficulty

```sql
difficulty IN (
'easy',
'medium',
'hard'
)
```

---

## Interview Status

```sql
status IN (

'pending',

'in_progress',

'completed',

'cancelled'
)
```

---

## Question Difficulty

```sql
difficulty IN (

'easy',

'medium',

'hard'
)
```

---

## Question Category

Allowed categories include:

```
technical

behavioral

coding

system_design

database

oop

operating_system

networking

aptitude

custom
```

---

## Answer Type

```sql
answer_type IN (

'text',

'voice'
)
```

---

## Submission Status

```sql
submission_status IN (

'draft',

'submitted',

'processing',

'evaluated',

'failed'
)
```

---

## Hiring Recommendation

```sql
hiring_recommendation IN (

'strong_hire',

'hire',

'borderline',

'no_hire'
)
```

---

## Severity

```sql
severity IN (

'debug',

'info',

'warning',

'error',

'critical'
)
```

---

## Score Constraints

All score columns satisfy:

```sql
score >= 0

AND

score <= 100
```

Examples:

- overall_score
- technical_score
- communication_score
- problem_solving_score
- confidence_score

---

## Response Time

```sql
response_time_seconds >= 0
```

---

## Evaluation Duration

```sql
evaluation_duration_ms >= 0
```

---

# DEFAULT Constraints

## Purpose

Provide safe default values.

---

## Examples

### created_at

```sql
DEFAULT NOW()
```

---

### updated_at

```sql
DEFAULT NOW()
```

---

### report_version

```sql
DEFAULT 1
```

---

### pdf_generated

```sql
DEFAULT FALSE
```

---

### language

```sql
DEFAULT 'en'
```

---

### answer_type

```sql
DEFAULT 'text'
```

---

### submission_status

```sql
DEFAULT 'submitted'
```

---

### severity

```sql
DEFAULT 'info'
```

---

# Constraint Naming Convention

Primary Keys

```
pk_<table>
```

Example

```
pk_users
```

---

Foreign Keys

```
fk_<child>_<parent>
```

Example

```
fk_interviews_user
```

---

Unique Constraints

```
uq_<table>_<columns>
```

Example

```
uq_reports_interview
```

---

Check Constraints

```
chk_<table>_<column>
```

Example

```
chk_interviews_status
```

---

# Business Validation Rules

The application should validate data before reaching the database.

However, the database remains the final authority.

Critical business rules must always be enforced by constraints.

---

# Referential Integrity

Rules:

- Every foreign key references an existing parent.
- Orphan records are prohibited.
- Invalid ownership relationships are rejected.
- Parent deletion follows documented cascade policy.

---

# Constraint Design Principles

- Prefer database enforcement over application-only validation.
- Use CHECK constraints for finite domains.
- Use UNIQUE constraints to protect business invariants.
- Use NOT NULL for mandatory fields.
- Avoid nullable foreign keys unless justified.
- Keep constraints deterministic and easy to understand.

---

# PostgreSQL Implementation Guidelines

Recommended practices:

- Use UUID primary keys.
- Use named constraints.
- Use explicit CHECK constraints instead of relying solely on application logic.
- Prefer database defaults for timestamps.
- Review constraints during every schema migration.

---

# Related Documents

- `relationships.md`
- `normalization.md`
- `indexes.md`
- `migrations.md`
- `schema-overview.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial database constraints specification |