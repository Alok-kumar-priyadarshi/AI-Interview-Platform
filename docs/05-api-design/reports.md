# Interview Reports API

**Document ID:** API-009

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines all APIs responsible for interview report generation and retrieval.

The Reports API provides:

- AI-generated interview reports
- Overall interview summary
- Score breakdown
- Strength analysis
- Weakness analysis
- Improvement recommendations
- Downloadable PDF reports
- Report history
- Export functionality

Reports are generated automatically after a successful evaluation.

---

# Resource

```
/reports
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
| Candidate | Own reports |
| Admin | All reports |

---

# Report Lifecycle

```text
Interview Completed

↓

Evaluation Completed

↓

Generate Report

↓

Store Report

↓

Generate PDF

↓

Ready For Download
```

---

# Report Status

```
Queued

Generating

Ready

Failed
```

---

# Endpoint Summary

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /reports | List reports |
| GET | /reports/{report_id} | Report details |
| GET | /interviews/{interview_id}/report | Interview report |
| GET | /reports/{report_id}/status | Generation status |
| GET | /reports/{report_id}/download | Download PDF |
| POST | /reports/{report_id}/regenerate | Regenerate report (Admin) |

---

# GET /reports

## Purpose

Returns every report owned by the authenticated user.

---

Query Parameters

```
page

page_size

sort

interview_type

date_from

date_to
```

---

Response

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "report_id": "uuid",
        "overall_score": 87,
        "grade": "A",
        "created_at": "2026-07-23T15:20:00Z"
      }
    ],
    "page": 1,
    "page_size": 20,
    "total": 35
  }
}
```

---

# GET /reports/{report_id}

## Purpose

Returns the complete report.

---

Response

```json
{
  "success": true,
  "data": {
    "report_id": "uuid",
    "overall_score": 87,
    "grade": "A",
    "summary": "Strong backend knowledge with good communication skills.",
    "strengths": [
      "Excellent API design",
      "Clear explanations"
    ],
    "weaknesses": [
      "Limited system design depth"
    ],
    "recommendations": [
      "Practice scalability concepts",
      "Improve optimization techniques"
    ]
  }
}
```

---

# GET /interviews/{interview_id}/report

## Purpose

Returns the report associated with an interview.

---

Response

```json
{
  "success": true,
  "data": {
    "report_id": "uuid",
    "status": "ready"
  }
}
```

---

# GET /reports/{report_id}/status

## Purpose

Returns report generation progress.

---

Response

```json
{
  "success": true,
  "data": {
    "status": "generating",
    "progress": 78
  }
}
```

---

Possible Status

```
queued

generating

ready

failed
```

---

# GET /reports/{report_id}/download

## Purpose

Downloads the generated PDF report.

---

Response

```
Content-Type: application/pdf
```

---

Headers

```
Content-Disposition:
attachment;
filename="Interview_Report.pdf"
```

---

# POST /reports/{report_id}/regenerate

## Purpose

Regenerates a failed report.

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
  "message": "Report regeneration started."
}
```

---

# Report Structure

Every report contains:

| Section | Description |
|-----------|-------------|
| Candidate Information | User profile snapshot |
| Interview Metadata | Date, duration, mode |
| Overall Score | Final score |
| Grade | Letter grade |
| Category Scores | Detailed breakdown |
| Strengths | Positive observations |
| Weaknesses | Areas requiring improvement |
| Recommendations | Personalized advice |
| AI Summary | Overall interview assessment |

---

# PDF Structure

```text
Cover Page

↓

Interview Summary

↓

Overall Score

↓

Category Scores

↓

Strengths

↓

Weaknesses

↓

Recommendations

↓

Question-wise Analysis
```

---

# Business Rules

- Reports are generated automatically.
- Reports are immutable after generation.
- PDF generation occurs after report creation.
- Every completed interview has at most one report.
- Regeneration is allowed only for failed reports.

---

# Authorization

Every request validates:

- JWT
- User ownership
- Report availability

---

# Rate Limits

| Endpoint | Limit |
|-----------|--------|
| List Reports | 60/min |
| Get Report | 60/min |
| Status | 120/min |
| Download PDF | 20/min |
| Regenerate | 5/hour (Admin) |

---

# Error Responses

Report Not Found

```json
{
  "success": false,
  "error": {
    "code": "REPORT_NOT_FOUND",
    "message": "Report does not exist."
  }
}
```

---

Report Processing

```json
{
  "success": false,
  "error": {
    "code": "REPORT_GENERATING",
    "message": "Report generation is still in progress."
  }
}
```

---

PDF Not Ready

```json
{
  "success": false,
  "error": {
    "code": "PDF_NOT_READY",
    "message": "PDF report is not yet available."
  }
}
```

---

# OpenAPI Tags

```
Reports
```

---

# Related Documents

- `evaluations.md`
- `history.md`
- `dashboard.md`
- `errors.md`
- `../04-database/entities/reports.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial Interview Reports API specification |