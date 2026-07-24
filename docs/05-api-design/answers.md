# Interview Answers API

**Document ID:** API-007

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines every API related to candidate answer submission during interviews.

The Answers API manages:

- Text answer submission
- Voice answer upload
- Speech-to-Text transcription
- Answer retrieval
- Answer validation
- Answer timestamps
- Answer persistence
- Answer metadata

Each interview question has exactly one answer.

---

# Resource

```
/interviews/{interview_id}/answers
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
| Candidate | Own interview answers |
| Admin | All answers |

---

# Answer Types

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

# Answer Lifecycle

```text
Question Delivered

↓

Candidate Responds

↓

Validate Answer

↓

Store Answer

↓

Voice?

↓

Speech-to-Text

↓

Store Transcript

↓

Queue Evaluation
```

---

# Endpoint Summary

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /interviews/{id}/answers | Submit text answer |
| POST | /interviews/{id}/answers/voice | Upload voice answer |
| GET | /interviews/{id}/answers/{answer_id} | Retrieve answer |
| GET | /interviews/{id}/answers | List answers |
| GET | /interviews/{id}/answers/{answer_id}/transcript | Transcript |

---

# POST /interviews/{id}/answers

## Purpose

Submits a text answer.

---

Request

```json
{
  "question_id": "uuid",
  "answer": "Dependency Injection allows dependencies to be provided externally..."
}
```

---

Response

```json
{
  "success": true,
  "message": "Answer submitted successfully.",
  "data": {
    "answer_id": "uuid",
    "submitted_at": "2026-07-23T12:45:10Z"
  }
}
```

---

Business Rules

- Only one answer per question
- Existing answer may be updated until next question begins
- Empty answers are rejected
- Maximum length applies

---

# POST /interviews/{id}/answers/voice

## Purpose

Uploads a recorded voice response.

---

Content Type

```
multipart/form-data
```

---

Request

| Field | Type | Required |
|------|------|----------|
| question_id | UUID | Yes |
| audio | File | Yes |

---

Supported Formats

```
WAV

MP3

WEBM

M4A
```

---

Maximum File Size

```
25 MB
```

---

Response

```json
{
  "success": true,
  "message": "Voice answer uploaded.",
  "data": {
    "answer_id": "uuid",
    "transcription_status": "processing"
  }
}
```

---

# Speech-to-Text Pipeline

```text
Voice Upload

↓

Validate Audio

↓

Store File

↓

Queue Whisper Job

↓

Transcribe Audio

↓

Store Transcript

↓

Queue Evaluation
```

---

# GET /interviews/{id}/answers/{answer_id}

## Purpose

Returns answer details.

---

Response

```json
{
  "success": true,
  "data": {
    "answer_id": "uuid",
    "question_id": "uuid",
    "type": "voice",
    "submitted_at": "2026-07-23T12:45:10Z",
    "duration_seconds": 92
  }
}
```

---

# GET /interviews/{id}/answers

## Purpose

Returns all submitted answers.

Available only after interview completion or to administrators.

---

Response

```json
{
  "success": true,
  "data": [
    {
      "question_id": "uuid",
      "type": "text",
      "submitted_at": "2026-07-23T12:30:00Z"
    }
  ]
}
```

---

# GET /interviews/{id}/answers/{answer_id}/transcript

## Purpose

Returns the transcription generated from a voice answer.

---

Response

```json
{
  "success": true,
  "data": {
    "transcript": "Dependency injection allows objects to receive dependencies...",
    "confidence": 0.97,
    "language": "en"
  }
}
```

---

# Validation Rules

Text Answer

- Minimum length: 1 character
- Maximum length: 20,000 characters

---

Voice File

Supported

```
WAV

MP3

WEBM

M4A
```

Maximum Size

```
25 MB
```

Maximum Duration

```
10 minutes
```

---

# Answer Metadata

Each stored answer contains:

| Field | Description |
|------|-------------|
| id | Answer identifier |
| question_id | Linked question |
| interview_id | Parent interview |
| answer_type | Text or Voice |
| transcript | Generated transcript |
| duration | Audio duration |
| created_at | Submission time |
| updated_at | Last modification |

---

# Business Rules

- One answer per question.
- Answers cannot be modified after moving to the next question.
- Transcript generation is asynchronous.
- Failed transcription may be retried.
- Evaluation starts only after transcript generation (voice mode).

---

# Authorization

Every request validates:

- JWT
- User ownership
- Interview state
- Question ownership

---

# Rate Limits

| Endpoint | Limit |
|-----------|--------|
| Submit Text | 120/hour |
| Upload Voice | 60/hour |
| Get Answer | 120/min |
| List Answers | 30/min |
| Transcript | 60/min |

---

# Error Responses

Answer Already Exists

```json
{
  "success": false,
  "error": {
    "code": "ANSWER_ALREADY_EXISTS",
    "message": "An answer has already been submitted for this question."
  }
}
```

---

Transcript Processing

```json
{
  "success": false,
  "error": {
    "code": "TRANSCRIPTION_IN_PROGRESS",
    "message": "Transcript is still being generated."
  }
}
```

---

Unsupported Audio

```json
{
  "success": false,
  "error": {
    "code": "UNSUPPORTED_AUDIO_FORMAT",
    "message": "Unsupported audio format."
  }
}
```

---

Interview Closed

```json
{
  "success": false,
  "error": {
    "code": "INTERVIEW_CLOSED",
    "message": "Interview no longer accepts answers."
  }
}
```

---

# OpenAPI Tags

```
Answers
```

---

# Related Documents

- `questions.md`
- `evaluations.md`
- `reports.md`
- `errors.md`
- `../04-database/entities/answers.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial Interview Answers API specification |