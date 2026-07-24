# Interview Questions API

**Document ID:** API-006

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines every API related to interview question delivery.

The Questions API is responsible for:

- Delivering interview questions
- Managing question progression
- Tracking current question
- Supporting adaptive interview flow
- Providing question metadata
- Preventing unauthorized question access

Questions are generated before the interview begins and delivered sequentially.

---

# Resource

```
/interviews/{interview_id}/questions
```

---

# Authorization

Authentication Required

```
Yes
```

Roles

| Role | Access |
|------|---------|
| Candidate | Own interviews |
| Admin | All interviews |

---

# Question Lifecycle

```text
Interview Created

↓

AI Generates Questions

↓

Questions Stored

↓

Interview Starts

↓

Question Delivered

↓

Answer Submitted

↓

Next Question

↓

Interview Completed
```

---

# Endpoint Summary

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /interviews/{id}/questions/current | Current question |
| GET | /interviews/{id}/questions/{question_id} | Question details |
| POST | /interviews/{id}/questions/{question_id}/next | Move to next question |
| GET | /interviews/{id}/questions | List questions (completed interviews only) |

---

# GET /interviews/{id}/questions/current

## Purpose

Returns the active interview question.

---

Headers

```
Authorization: Bearer <token>
```

---

Response

```json
{
  "success": true,
  "data": {
    "question_id": "uuid",
    "sequence": 4,
    "type": "technical",
    "difficulty": "medium",
    "question": "Explain dependency injection in FastAPI.",
    "time_limit_seconds": 180,
    "remaining_seconds": 172
  }
}
```

---

Business Rules

- Only one active question exists.
- Previous unanswered questions block progression.
- Future questions cannot be requested.

---

# GET /interviews/{id}/questions/{question_id}

## Purpose

Returns metadata for a specific question.

During an active interview, access is limited to the current question.

After interview completion, all questions become available.

---

Response

```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "sequence": 4,
    "difficulty": "medium",
    "category": "Backend",
    "estimated_time_seconds": 180
  }
}
```

---

# POST /interviews/{id}/questions/{question_id}/next

## Purpose

Advances the interview to the next question.

---

Requirements

- Current answer submitted
- Current question completed
- Interview status is `In Progress`

---

Response

```json
{
  "success": true,
  "data": {
    "next_question_id": "uuid",
    "sequence": 5
  }
}
```

---

Progression Flow

```text
Answer Saved

↓

Answer Validated

↓

Update Progress

↓

Load Next Question

↓

Deliver Question
```

---

# GET /interviews/{id}/questions

## Purpose

Returns every interview question.

Only available after interview completion or to administrators.

---

Response

```json
{
  "success": true,
  "data": [
    {
      "sequence": 1,
      "difficulty": "easy",
      "category": "Programming"
    },
    {
      "sequence": 2,
      "difficulty": "medium",
      "category": "Database"
    }
  ]
}
```

---

# Question Metadata

Each question contains:

| Field | Description |
|------|-------------|
| id | Question identifier |
| sequence | Display order |
| type | Technical / Behavioral |
| category | Subject area |
| difficulty | Easy / Medium / Hard |
| estimated_time | Suggested duration |
| generated_by | AI model identifier |

---

# Adaptive Question Sequencing

Version 1

```
Disabled
```

Questions are generated before interview start.

---

Future Versions

Adaptive questioning based on:

- Previous answers
- Confidence score
- Candidate performance
- Time remaining

---

# Timing Rules

Each question has:

- Start timestamp
- End timestamp
- Remaining time
- Time spent

The server remains the source of truth.

---

# Business Rules

- Questions are immutable after generation.
- Sequence numbers are continuous.
- Question order cannot change.
- Questions cannot be skipped.
- Revisiting previous questions is not supported during an active interview.

---

# Authorization

Every request validates:

- JWT
- User ownership
- Interview status
- Question availability

---

# Rate Limits

| Endpoint | Limit |
|-----------|--------|
| Current Question | 120/min |
| Question Details | 120/min |
| Next Question | 60/min |
| Question List | 30/min |

---

# Error Responses

Question Not Found

```json
{
  "success": false,
  "error": {
    "code": "QUESTION_NOT_FOUND",
    "message": "Question does not exist."
  }
}
```

---

Question Locked

```json
{
  "success": false,
  "error": {
    "code": "QUESTION_LOCKED",
    "message": "This question is not yet available."
  }
}
```

---

Interview Not Active

```json
{
  "success": false,
  "error": {
    "code": "INTERVIEW_NOT_ACTIVE",
    "message": "Interview is not currently active."
  }
}
```

---

# OpenAPI Tags

```
Questions
```

---

# Related Documents

- `interviews.md`
- `answers.md`
- `evaluations.md`
- `errors.md`
- `../04-database/entities/questions.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial Interview Questions API specification |