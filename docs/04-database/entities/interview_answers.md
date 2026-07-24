# Interview Answers Entity

**Document ID:** DB-003-006

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

The `interview_answers` table stores every answer submitted by a candidate
during an interview.

Answers may originate from:

- Text input
- Voice recording

Voice responses are transcribed before evaluation.

This entity acts as the primary input for the AI Evaluation Engine.

---

# Responsibilities

The interview_answers entity is responsible for:

- Candidate responses
- Voice transcription
- Answer timing
- Submission metadata
- Speech confidence
- Evaluation linkage

It is **not** responsible for:

- Question generation
- AI scoring
- Final interview reports

---

# Table Definition

| Column | Type | Nullable | Default |
|---------|------|----------|----------|
| id | UUID | No | uuid_generate_v4() |
| question_id | UUID | No | — |
| answer_type | VARCHAR(20) | No | 'text' |
| answer_text | TEXT | Yes | NULL |
| audio_storage_path | TEXT | Yes | NULL |
| transcription_text | TEXT | Yes | NULL |
| transcription_confidence | DECIMAL(5,2) | Yes | NULL |
| language | VARCHAR(20) | No | 'en' |
| response_time_seconds | INTEGER | Yes | NULL |
| submission_status | VARCHAR(30) | No | 'submitted' |
| submitted_at | TIMESTAMPTZ | No | NOW() |
| created_at | TIMESTAMPTZ | No | NOW() |
| updated_at | TIMESTAMPTZ | No | NOW() |

---

# Primary Key

```
id UUID
```

Immutable identifier for every submitted answer.

---

# Foreign Key

```
question_id

↓

interview_questions.id
```

Relationship:

```
One Question

↓

One Answer (Version 1)
```

Future versions may support multiple answer attempts.

---

# Column Definitions

## answer_type

Origin of the answer.

Allowed values:

```
text

voice
```

---

## answer_text

Raw text entered by the candidate.

Used only for text interviews.

---

## audio_storage_path

Reference to uploaded audio.

Examples:

```
audio/interviews/...

s3://bucket/audio/...

gs://bucket/audio/...
```

Never expose internal storage paths directly.

---

## transcription_text

Speech-to-text output generated using Whisper.

Used by the evaluation engine.

---

## transcription_confidence

Confidence score reported by the speech recognition model.

Range:

```
0.00

↓

100.00
```

---

## language

Detected or selected language.

Examples:

```
en

hi

fr

es
```

---

## response_time_seconds

Time taken to answer.

Measured from question presentation until submission.

---

## submission_status

Allowed values:

```
draft

submitted

processing

evaluated

failed
```

---

## submitted_at

Timestamp when the answer was finalized.

---

## created_at

Creation timestamp.

---

## updated_at

Updated whenever transcription or processing metadata changes.

---

# Constraints

Primary Key

```
pk_interview_answers
```

Foreign Key

```
fk_answers_question
```

Unique

```
uq_answers_question
```

Version 1 permits one answer per question.

Check Constraints

```
chk_answer_type

chk_submission_status

chk_transcription_confidence

chk_response_time
```

---

# Indexes

Primary

```
pk_interview_answers
```

Secondary

```
idx_answers_question

idx_answers_status

idx_answers_language

idx_answers_submitted_at
```

---

# Relationships

Parent of:

```
evaluations
```

Child of:

```
interview_questions
```

Referenced by:

```
answer_id
```

---

# Business Rules

- Every answer belongs to exactly one question.
- A question accepts one submitted answer in Version 1.
- Voice answers must be transcribed before evaluation.
- Text answers bypass transcription.
- Submitted answers become immutable.

---

# Answer Lifecycle

```text
Question Presented

↓

Candidate Responds

↓

Text Submitted
        OR
Voice Uploaded

↓

Speech Transcription (Voice Only)

↓

Ready for Evaluation

↓

Evaluation Completed
```

---

# Validation Rules

Answer Type

Allowed values:

- text
- voice

Text Answers

- Must contain answer_text
- audio_storage_path must be NULL

Voice Answers

- Must contain audio_storage_path
- transcription generated before evaluation

Response Time

- Greater than or equal to 0

Confidence Score

- Between 0 and 100

---

# Security Considerations

Audio recordings may contain sensitive personal information.

Requirements:

- Encrypt audio storage
- Restrict access
- Avoid logging answer contents
- Exclude transcripts from debug logs
- Delete temporary audio after processing when applicable

---

# SQL Example

```sql
CREATE TABLE interview_answers (
    id UUID PRIMARY KEY,
    question_id UUID UNIQUE NOT NULL REFERENCES interview_questions(id),
    answer_type VARCHAR(20) NOT NULL,
    answer_text TEXT,
    audio_storage_path TEXT,
    transcription_text TEXT,
    transcription_confidence DECIMAL(5,2),
    language VARCHAR(20) NOT NULL DEFAULT 'en',
    response_time_seconds INTEGER,
    submission_status VARCHAR(30) NOT NULL,
    submitted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

# SQLAlchemy Example

```python
class InterviewAnswer(Base):
    __tablename__ = "interview_answers"

    id = mapped_column(UUID(as_uuid=True), primary_key=True)

    question_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("interview_questions.id"),
        unique=True,
        nullable=False
    )

    answer_type = mapped_column(String(20), default="text")

    answer_text = mapped_column(Text)

    audio_storage_path = mapped_column(Text)

    transcription_text = mapped_column(Text)

    transcription_confidence = mapped_column(Numeric(5, 2))

    language = mapped_column(String(20), default="en")

    response_time_seconds = mapped_column(Integer)

    submission_status = mapped_column(String(30), default="submitted")

    submitted_at = mapped_column(DateTime(timezone=True))

    created_at = mapped_column(DateTime(timezone=True))

    updated_at = mapped_column(DateTime(timezone=True))
```

---

# Future Enhancements

Potential additions:

- Multiple answer attempts
- Streaming speech recognition
- Emotion analysis
- Voice quality metrics
- Pause detection
- Speaking speed
- Pronunciation analysis
- Vector embeddings
- Multilingual transcription

---

# Related Documents

- `interview_questions.md`
- `evaluations.md`
- `reports.md`
- `../schema-overview.md`
- `../../06-ai-system/`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial interview answers entity specification |