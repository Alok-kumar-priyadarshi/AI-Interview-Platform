# Interview API

**Document ID:** API-005

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines all Interview API endpoints used by the AI Career Interview Platform.

The Interview API manages the complete interview lifecycle including:

- Interview creation
- Resume selection
- AI interview generation
- Voice interview sessions
- Text interview sessions
- Interview progress
- Completion
- Cancellation
- Session recovery

Each interview is generated dynamically based on the selected resume and candidate profile.

---

# Resource

```
/interviews
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

# Interview Modes

Supported

```
Text

Voice
```

Future

```
Video
```

---

# Interview Types

Supported

```
Technical

Behavioral

Mixed
```

---

# Difficulty Levels

```
Easy

Medium

Hard
```

---

# Interview Status

```
Pending

Generating

Ready

In Progress

Completed

Cancelled

Failed
```

---

# Endpoint Summary

| Method | Endpoint | Description |
|----------|----------|-------------|
| GET | /interviews | List interviews |
| POST | /interviews | Create interview |
| GET | /interviews/{id} | Interview details |
| GET | /interviews/{id}/status | Session status |
| POST | /interviews/{id}/start | Start interview |
| POST | /interviews/{id}/pause | Pause interview |
| POST | /interviews/{id}/resume | Resume interview |
| POST | /interviews/{id}/complete | Complete interview |
| POST | /interviews/{id}/cancel | Cancel interview |
| DELETE | /interviews/{id} | Delete interview |

---

# POST /interviews

## Purpose

Creates a new interview.

---

Request

```json
{
  "resume_id": "uuid",
  "interview_type": "technical",
  "difficulty": "medium",
  "mode": "voice",
  "language": "en",
  "interviewer_voice": "female",
  "question_count": 10,
  "time_limit_minutes": 45
}
```

---

Field Definitions

| Field | Required |
|---------|----------|
| resume_id | Yes |
| interview_type | Yes |
| difficulty | Yes |
| mode | Yes |
| language | Yes |
| interviewer_voice | Yes |
| question_count | No |
| time_limit_minutes | No |

---

Response

```json
{
  "success": true,
  "message": "Interview creation started.",
  "data": {
    "interview_id": "uuid",
    "status": "generating"
  }
}
```

Interview generation is asynchronous.

---

# AI Generation Pipeline

```text
Create Interview

↓

Load Resume

↓

Load Candidate Profile

↓

Generate Interview Prompt

↓

LLM Generates Questions

↓

Store Questions

↓

Ready
```

---

# GET /interviews

Returns interview history.

---

Query Parameters

```
page

page_size

status

difficulty

type

mode

sort
```

---

Response

```json
{
  "success": true,
  "data": {
    "items": [],
    "page": 1,
    "page_size": 20,
    "total": 64
  }
}
```

---

# GET /interviews/{id}

Returns interview information.

---

Response

```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "status": "ready",
    "difficulty": "medium",
    "type": "technical",
    "mode": "voice",
    "question_count": 10,
    "created_at": "2026-07-23T12:00:00Z"
  }
}
```

---

# GET /interviews/{id}/status

Returns live interview status.

---

Response

```json
{
  "success": true,
  "data": {
    "status": "in_progress",
    "current_question": 4,
    "completed_questions": 3,
    "remaining_questions": 7,
    "elapsed_seconds": 923
  }
}
```

---

# POST /interviews/{id}/start

Starts an interview.

Requirements

- Interview must be READY.

---

Response

```json
{
  "success": true,
  "message": "Interview started."
}
```

---

# POST /interviews/{id}/pause

Temporarily pauses interview.

Applicable only to:

- Voice interviews
- Text interviews

---

# POST /interviews/{id}/resume

Continues paused interview.

---

# POST /interviews/{id}/complete

Marks interview complete.

Completion triggers:

```text
Finalize Answers

↓

Queue Evaluation

↓

Generate Report

↓

Update Statistics
```

---

Response

```json
{
  "success": true,
  "message": "Interview completed."
}
```

---

# POST /interviews/{id}/cancel

Cancels an unfinished interview.

Allowed States

```
Pending

Ready

In Progress
```

Completed interviews cannot be cancelled.

---

# DELETE /interviews/{id}

Deletes interview metadata.

Associated reports remain subject to retention policy.

Administrative permissions may be required.

---

# Voice Interview Workflow

```text
Start Interview

↓

Play AI Question

↓

Record Audio

↓

Upload Recording

↓

Speech-to-Text

↓

Store Answer

↓

Next Question
```

---

# Text Interview Workflow

```text
Display Question

↓

User Types Answer

↓

Submit Answer

↓

Store Answer

↓

Next Question
```

---

# Session Recovery

Supported after:

- Browser refresh
- Network interruption
- Client restart

Recovery retrieves:

- Current question
- Timer
- Completed answers
- Remaining interview duration

---

# Validation Rules

Question Count

```
5–50
```

Time Limit

```
10–180 minutes
```

Language

```
en

hi
```

Mode

```
voice

text
```

Difficulty

```
easy

medium

hard
```

---

# Authorization

Every request validates:

- JWT
- Resource ownership
- Interview status
- Business rules

---

# Rate Limits

| Endpoint | Limit |
|-----------|--------|
| POST Create | 10/hour |
| GET List | 100/min |
| GET Status | 120/min |
| Start | 20/hour |
| Pause | 60/hour |
| Resume | 60/hour |
| Complete | 20/hour |
| Cancel | 10/day |

---

# Error Responses

Interview Not Found

```json
{
  "success": false,
  "error": {
    "code": "INTERVIEW_NOT_FOUND",
    "message": "Interview does not exist."
  }
}
```

---

Interview Not Ready

```json
{
  "success": false,
  "error": {
    "code": "INTERVIEW_NOT_READY",
    "message": "Interview generation is still in progress."
  }
}
```

---

Invalid State

```json
{
  "success": false,
  "error": {
    "code": "INVALID_INTERVIEW_STATE",
    "message": "Operation is not allowed in the current interview state."
  }
}
```

---

# OpenAPI Tags

```
Interviews
```

---

# Related Documents

- `resume.md`
- `questions.md`
- `answers.md`
- `evaluations.md`
- `reports.md`
- `../04-database/entities/interviews.md`
- `../03-architecture/system-architecture.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial Interview API specification |