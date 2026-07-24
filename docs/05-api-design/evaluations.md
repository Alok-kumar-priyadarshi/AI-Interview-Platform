# AI Evaluation API

**Document ID:** API-008

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines every API related to AI-powered interview evaluation.

The Evaluation API is responsible for:

- AI answer evaluation
- Interview scoring
- Category-wise scoring
- Overall performance analysis
- Strength identification
- Weakness detection
- Personalized recommendations
- Final report generation trigger

Evaluation begins automatically after interview completion.

---

# Resource

```
/evaluations
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
| Candidate | Own evaluations |
| Admin | All evaluations |

---

# Evaluation Lifecycle

```text
Interview Completed

↓

Collect Answers

↓

Prepare Evaluation Prompt

↓

LLM Evaluation

↓

Generate Scores

↓

Generate Feedback

↓

Store Evaluation

↓

Generate Report
```

---

# Evaluation Status

```
Queued

Processing

Completed

Failed
```

---

# Endpoint Summary

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /evaluations/{evaluation_id} | Evaluation details |
| GET | /interviews/{interview_id}/evaluation | Interview evaluation |
| GET | /evaluations/{evaluation_id}/status | Evaluation status |
| POST | /evaluations/{evaluation_id}/retry | Retry failed evaluation (Admin) |

---

# GET /evaluations/{evaluation_id}

## Purpose

Returns a completed evaluation.

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
    "evaluation_id": "uuid",
    "overall_score": 84,
    "grade": "A",
    "status": "completed",
    "generated_at": "2026-07-23T14:35:00Z"
  }
}
```

---

# GET /interviews/{interview_id}/evaluation

## Purpose

Returns the complete evaluation for an interview.

---

Response

```json
{
  "success": true,
  "data": {
    "overall_score": 84,
    "grade": "A",
    "categories": {
      "technical_knowledge": 88,
      "problem_solving": 81,
      "communication": 79,
      "confidence": 86,
      "system_design": 82
    },
    "strengths": [
      "Strong backend concepts",
      "Clear explanations"
    ],
    "weaknesses": [
      "Limited optimization discussion"
    ],
    "recommendations": [
      "Practice distributed systems",
      "Improve complexity analysis"
    ]
  }
}
```

---

# GET /evaluations/{evaluation_id}/status

## Purpose

Returns evaluation progress.

---

Response

```json
{
  "success": true,
  "data": {
    "status": "processing",
    "progress": 72
  }
}
```

---

Possible Status

```
queued

processing

completed

failed
```

---

# POST /evaluations/{evaluation_id}/retry

## Purpose

Retries a failed evaluation.

---

Authorization

```
Admin Only
```

---

Response

```json
{
  "success": true,
  "message": "Evaluation queued for retry."
}
```

---

# Evaluation Rubric

Every interview is scored across multiple dimensions.

| Category | Weight |
|-----------|--------|
| Technical Knowledge | 30% |
| Problem Solving | 20% |
| Communication | 15% |
| Confidence | 10% |
| Accuracy | 15% |
| Completeness | 10% |

---

# Grade Mapping

| Score | Grade |
|--------|-------|
| 90–100 | A+ |
| 80–89 | A |
| 70–79 | B |
| 60–69 | C |
| Below 60 | D |

---

# Evaluation Output

Every evaluation contains:

- Overall score
- Category scores
- Grade
- Strengths
- Weaknesses
- Improvement suggestions
- AI summary
- Evaluation timestamp

---

# AI Evaluation Workflow

```text
Load Interview

↓

Load Questions

↓

Load Answers

↓

Build Evaluation Prompt

↓

LLM Evaluation

↓

Extract Scores

↓

Generate Feedback

↓

Persist Results
```

---

# Business Rules

- Evaluation starts automatically after interview completion.
- A completed evaluation is immutable.
- Failed evaluations may be retried.
- Reports depend on completed evaluations.
- Manual score editing is not supported in Version 1.

---

# Authorization

Every request validates:

- JWT
- User ownership
- Evaluation availability

---

# Rate Limits

| Endpoint | Limit |
|-----------|--------|
| Get Evaluation | 60/min |
| Get Status | 120/min |
| Retry Evaluation | 10/hour (Admin) |

---

# Error Responses

Evaluation Not Found

```json
{
  "success": false,
  "error": {
    "code": "EVALUATION_NOT_FOUND",
    "message": "Evaluation does not exist."
  }
}
```

---

Evaluation Processing

```json
{
  "success": false,
  "error": {
    "code": "EVALUATION_PROCESSING",
    "message": "Evaluation is still being generated."
  }
}
```

---

Evaluation Failed

```json
{
  "success": false,
  "error": {
    "code": "EVALUATION_FAILED",
    "message": "Evaluation could not be completed."
  }
}
```

---

# OpenAPI Tags

```
Evaluations
```

---

# Related Documents

- `answers.md`
- `reports.md`
- `history.md`
- `errors.md`
- `../04-database/entities/evaluations.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial AI Evaluation API specification |