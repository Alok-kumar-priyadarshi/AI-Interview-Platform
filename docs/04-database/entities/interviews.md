# Interviews Entity

**Document ID:** DB-003-004

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

The `interviews` table stores every interview session created by a user.

It acts as the parent entity for interview questions, candidate answers,
AI evaluations, and the final interview report.

Every interview represents one complete assessment session.

---

# Responsibilities

The interviews entity is responsible for:

- Interview configuration
- Interview type
- Difficulty
- Target role
- Salary target
- AI model selection
- Session status
- Timing
- Overall interview metrics

It is **not** responsible for:

- Individual questions
- Candidate answers
- Detailed evaluation
- Resume parsing

---

# Table Definition

| Column | Type | Nullable | Default |
|---------|------|----------|----------|
| id | UUID | No | uuid_generate_v4() |
| user_id | UUID | No | — |
| resume_id | UUID | No | — |
| title | VARCHAR(255) | No | — |
| interview_type | VARCHAR(20) | No | 'text' |
| interviewer_voice | VARCHAR(50) | Yes | NULL |
| target_role | VARCHAR(150) | No | — |
| target_company | VARCHAR(150) | Yes | NULL |
| expected_salary | INTEGER | Yes | NULL |
| experience_level | VARCHAR(30) | No | 'fresher' |
| difficulty | VARCHAR(20) | No | 'medium' |
| ai_model | VARCHAR(50) | No | — |
| total_questions | INTEGER | No | 0 |
| answered_questions | INTEGER | No | 0 |
| overall_score | DECIMAL(5,2) | Yes | NULL |
| status | VARCHAR(30) | No | 'created' |
| started_at | TIMESTAMPTZ | Yes | NULL |
| completed_at | TIMESTAMPTZ | Yes | NULL |
| duration_seconds | INTEGER | Yes | NULL |
| created_at | TIMESTAMPTZ | No | NOW() |
| updated_at | TIMESTAMPTZ | No | NOW() |

---

# Primary Key

```
id UUID
```

Globally unique identifier for the interview session.

---

# Foreign Keys

```
user_id

↓

users.id
```

```
resume_id

↓

resumes.id
```

Relationships:

```
One User

↓

Many Interviews
```

```
One Resume

↓

Many Interviews
```

A user may reuse the same resume for multiple interview sessions.

---

# Column Definitions

## title

User-friendly interview name.

Example:

```
Backend Developer Mock Interview

Google SDE Practice

ML Engineer Interview
```

---

## interview_type

Determines interaction mode.

Allowed values:

```
text

voice
```

---

## interviewer_voice

Voice selected for voice interviews.

Examples:

```
male

female
```

Reserved for future TTS voice identifiers.

---

## target_role

Job role being simulated.

Examples:

```
Backend Developer

Software Engineer

Machine Learning Engineer

Data Scientist
```

---

## target_company

Optional company-specific interview.

Examples:

```
Google

Amazon

Microsoft
```

---

## expected_salary

Annual expected salary.

Examples:

```
600000

1200000

2500000
```

Stored as whole currency units.

---

## experience_level

Allowed values:

```
fresher

junior

mid

senior
```

---

## difficulty

Interview difficulty.

Allowed values:

```
easy

medium

hard
```

---

## ai_model

Model responsible for question generation.

Example:

```
groq-llama-4

groq-mixtral
```

---

## total_questions

Number of generated questions.

Must be non-negative.

---

## answered_questions

Questions answered by the candidate.

Cannot exceed `total_questions`.

---

## overall_score

Final interview score.

Range:

```
0.00

↓

100.00
```

---

## status

Interview lifecycle.

Allowed values:

```
created

ready

in_progress

completed

cancelled

failed
```

---

## started_at

Timestamp when interview begins.

---

## completed_at

Timestamp when interview finishes.

---

## duration_seconds

Total interview duration.

Calculated automatically.

---

## created_at

Interview creation timestamp.

---

## updated_at

Updated whenever interview metadata changes.

---

# Constraints

Primary Key

```
pk_interviews
```

Foreign Keys

```
fk_interviews_user

fk_interviews_resume
```

Check Constraints

```
chk_interview_type

chk_difficulty

chk_status

chk_experience_level

chk_overall_score

chk_answer_count
```

---

# Indexes

Primary

```
pk_interviews
```

Secondary

```
idx_interviews_user

idx_interviews_resume

idx_interviews_status

idx_interviews_created_at

idx_interviews_role

idx_interviews_company
```

Composite

```
idx_interviews_user_created

(user_id, created_at DESC)
```

Optimized for interview history queries.

---

# Relationships

Parent of:

```
interview_questions

reports
```

Child of:

```
users

resumes
```

Referenced indirectly by:

```
evaluations

interview_answers
```

---

# Business Rules

- Every interview belongs to one user.
- Every interview references one resume.
- Questions are generated only after interview creation.
- Interviews cannot be completed without generated questions.
- Completed interviews become immutable except for report regeneration.

---

# Interview Lifecycle

```text
Created

↓

Resume Selected

↓

Configuration Complete

↓

Questions Generated

↓

Ready

↓

In Progress

↓

Completed

↓

Evaluation Generated

↓

Final Report Created
```

---

# Validation Rules

Title

- Required
- Maximum 255 characters

Expected Salary

- Greater than or equal to 0

Question Counts

- Non-negative
- Answered ≤ Total

Overall Score

- Between 0 and 100

Duration

- Greater than or equal to 0

---

# Security Considerations

Interview metadata contains user preferences and assessment results.

Access rules:

- Users may access only their own interviews.
- Administrators may access all interviews.
- Internal AI metadata must not be exposed through public APIs.

---

# SQL Example

```sql
CREATE TABLE interviews (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    resume_id UUID NOT NULL REFERENCES resumes(id),
    title VARCHAR(255) NOT NULL,
    interview_type VARCHAR(20) NOT NULL,
    interviewer_voice VARCHAR(50),
    target_role VARCHAR(150) NOT NULL,
    target_company VARCHAR(150),
    expected_salary INTEGER,
    experience_level VARCHAR(30) NOT NULL,
    difficulty VARCHAR(20) NOT NULL,
    ai_model VARCHAR(50) NOT NULL,
    total_questions INTEGER NOT NULL DEFAULT 0,
    answered_questions INTEGER NOT NULL DEFAULT 0,
    overall_score DECIMAL(5,2),
    status VARCHAR(30) NOT NULL,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    duration_seconds INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

# SQLAlchemy Example

```python
class Interview(Base):
    __tablename__ = "interviews"

    id = mapped_column(UUID(as_uuid=True), primary_key=True)

    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))

    resume_id = mapped_column(UUID(as_uuid=True), ForeignKey("resumes.id"))

    title = mapped_column(String(255), nullable=False)

    interview_type = mapped_column(String(20), default="text")

    interviewer_voice = mapped_column(String(50))

    target_role = mapped_column(String(150), nullable=False)

    target_company = mapped_column(String(150))

    expected_salary = mapped_column(Integer)

    experience_level = mapped_column(String(30), default="fresher")

    difficulty = mapped_column(String(20), default="medium")

    ai_model = mapped_column(String(50), nullable=False)

    total_questions = mapped_column(Integer, default=0)

    answered_questions = mapped_column(Integer, default=0)

    overall_score = mapped_column(Numeric(5, 2))

    status = mapped_column(String(30), default="created")

    started_at = mapped_column(DateTime(timezone=True))

    completed_at = mapped_column(DateTime(timezone=True))

    duration_seconds = mapped_column(Integer)

    created_at = mapped_column(DateTime(timezone=True))

    updated_at = mapped_column(DateTime(timezone=True))
```

---

# Future Enhancements

Potential additions:

- Interview templates
- Adaptive questioning
- Live coding sessions
- Video interviews
- Multi-round interviews
- Collaborative interviews
- AI interviewer personality
- Benchmark comparisons

---

# Related Documents

- `users.md`
- `resumes.md`
- `candidate_profiles.md`
- `interview_questions.md`
- `../schema-overview.md`
- `../../03-architecture/ai-architecture.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial interviews entity specification |