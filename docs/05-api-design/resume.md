# Resume API

**Document ID:** API-004

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines every Resume API endpoint used by the AI Career Interview Platform.

The Resume API is responsible for:

- Resume upload
- Resume storage
- Resume parsing
- Metadata extraction
- Resume retrieval
- Resume deletion
- Resume selection for interviews
- Resume processing status

Users may maintain multiple resumes.

---

# Resource

```
/resumes
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
| Candidate | Own resumes |
| Admin | All resumes |

---

# Supported Formats

| Extension | MIME Type |
|-----------|-----------|
| PDF | application/pdf |
| DOCX | application/vnd.openxmlformats-officedocument.wordprocessingml.document |
| DOC | application/msword |

Maximum file size

```
10 MB
```

---

# Resume Lifecycle

```text
Upload Resume

↓

Store File

↓

Store Metadata

↓

Queue Parsing Job

↓

Extract Text

↓

Extract Structured Data

↓

Generate Embeddings

↓

Save Results

↓

Ready
```

---

# Resume Status

Possible values

```
uploaded

processing

parsed

failed

deleted
```

---

# Endpoint Summary

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /resumes | List resumes |
| POST | /resumes | Upload resume |
| GET | /resumes/{resume_id} | Resume details |
| GET | /resumes/{resume_id}/status | Parsing status |
| GET | /resumes/{resume_id}/metadata | Extracted metadata |
| PATCH | /resumes/{resume_id}/default | Set default resume |
| DELETE | /resumes/{resume_id} | Delete resume |

---

# GET /resumes

## Purpose

Returns every resume owned by the authenticated user.

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
  "data": [
    {
      "id": "uuid",
      "file_name": "Backend_Resume.pdf",
      "status": "parsed",
      "uploaded_at": "2026-07-22T10:30:00Z",
      "is_default": true
    }
  ]
}
```

---

# POST /resumes

## Purpose

Uploads a new resume.

---

Content Type

```
multipart/form-data
```

---

Request

| Field | Type | Required |
|------|------|----------|
| file | File | Yes |

---

Response

```json
{
  "success": true,
  "message": "Resume uploaded successfully.",
  "data": {
    "resume_id": "uuid",
    "status": "processing"
  }
}
```

---

Status Codes

| Code | Meaning |
|------|----------|
| 201 | Uploaded |
| 400 | Invalid file |
| 401 | Unauthorized |
| 413 | File too large |
| 415 | Unsupported format |

---

# GET /resumes/{resume_id}

## Purpose

Returns resume metadata.

---

Response

```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "file_name": "Backend_Resume.pdf",
    "file_size": 734221,
    "status": "parsed",
    "uploaded_at": "2026-07-22T10:30:00Z",
    "is_default": true
  }
}
```

---

# GET /resumes/{resume_id}/status

## Purpose

Returns processing status.

---

Response

```json
{
  "success": true,
  "data": {
    "status": "processing",
    "progress": 65
  }
}
```

---

Possible Status

```
uploaded

processing

parsed

failed
```

---

# GET /resumes/{resume_id}/metadata

## Purpose

Returns extracted structured information.

---

Example Response

```json
{
  "success": true,
  "data": {
    "name": "John Doe",
    "email": "john@example.com",
    "skills": [
      "Python",
      "FastAPI",
      "PostgreSQL"
    ],
    "education": [
      "Bachelor of Technology"
    ],
    "experience": [
      "Backend Developer"
    ],
    "projects": [
      "Interview Platform"
    ]
  }
}
```

---

# PATCH /resumes/{resume_id}/default

## Purpose

Marks a resume as the default resume.

Only one default resume may exist.

---

Response

```json
{
  "success": true,
  "message": "Default resume updated."
}
```

---

# DELETE /resumes/{resume_id}

## Purpose

Deletes a resume.

Deletion includes:

- Resume metadata
- Parsed text
- Embeddings
- Vector index entries

Underlying file storage is cleaned asynchronously.

---

Response

```json
{
  "success": true,
  "message": "Resume deleted successfully."
}
```

---

# Validation Rules

File Type

```
PDF

DOCX

DOC
```

---

Maximum Size

```
10 MB
```

---

Maximum Resumes Per User

```
10
```

---

Duplicate Detection

The platform may detect duplicate resumes using:

- File checksum
- File hash
- Extracted text similarity

Users may still choose to upload duplicates.

---

# Asynchronous Processing

Parsing is performed asynchronously.

Workflow

```text
Upload

↓

Queue Job

↓

OCR (if required)

↓

Text Extraction

↓

Metadata Extraction

↓

Embedding Generation

↓

Database Update
```

Upload endpoints should return immediately after queuing.

---

# Security

Every request validates:

- JWT
- Ownership
- File type
- File size
- Malware scan (future)

Uploaded files are never executed.

---

# Rate Limits

| Endpoint | Limit |
|-----------|--------|
| GET /resumes | 100/min |
| POST /resumes | 10/hour |
| GET /status | 120/min |
| GET /metadata | 60/min |
| PATCH /default | 20/min |
| DELETE | 10/day |

---

# Error Responses

Unsupported File

```json
{
  "success": false,
  "error": {
    "code": "UNSUPPORTED_FILE",
    "message": "Only PDF, DOC and DOCX are supported."
  }
}
```

---

File Too Large

```json
{
  "success": false,
  "error": {
    "code": "FILE_TOO_LARGE",
    "message": "Maximum file size is 10 MB."
  }
}
```

---

Resume Not Found

```json
{
  "success": false,
  "error": {
    "code": "RESUME_NOT_FOUND",
    "message": "Resume does not exist."
  }
}
```

---

# OpenAPI Tags

```
Resume
```

---

# Related Documents

- `candidate-profile.md`
- `interviews.md`
- `errors.md`
- `../04-database/entities/resumes.md`
- `../03-architecture/system-architecture.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial Resume API specification |