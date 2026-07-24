# File Security Architecture

**Document ID:** SEC-007

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the secure file handling architecture for the AI Career Interview Platform.

The platform accepts user-uploaded resumes and generates downloadable reports. Every file must be processed securely throughout its lifecycle.

This document covers:

- Secure uploads
- File validation
- Malware protection
- Storage isolation
- Access control
- Signed URLs
- File retention
- Secure deletion

---

# Supported Files

## User Uploads

- PDF Resume
- DOCX Resume

## Platform Generated

- Evaluation Reports
- Feedback PDFs
- Temporary AI Artifacts

Future

- Audio recordings
- Video recordings
- Portfolio attachments

---

# Secure Upload Workflow

```text
User Upload

↓

HTTPS

↓

API Validation

↓

File Type Validation

↓

MIME Validation

↓

Size Validation

↓

Filename Sanitization

↓

Malware Scan (Future)

↓

Generate Random File ID

↓

Encrypted Storage

↓

Database Metadata

↓

Upload Complete
```

---

# Allowed File Types

| Extension | MIME Type |
|-----------|-----------|
| .pdf | application/pdf |
| .docx | application/vnd.openxmlformats-officedocument.wordprocessingml.document |

All other file types are rejected.

---

# File Size Limits

| File | Maximum Size |
|------|--------------|
| Resume | 10 MB |
| Generated Report | 20 MB |

Requests exceeding limits return

```
413 Payload Too Large
```

---

# MIME Type Validation

Validation consists of:

1. Extension validation
2. MIME type validation
3. File signature ("magic bytes") validation

All three checks must succeed.

---

# Filename Handling

Original filenames are never used for storage.

Example

```
resume.pdf
```

Stored as

```
9d67d1a0-f32b-4d8e-b61e.pdf
```

The original filename is stored only as metadata.

---

# Storage Isolation

Files are stored outside the application codebase.

Logical structure

```text
storage/

├── resumes/
├── reports/
├── temporary/
└── archived/
```

Direct filesystem access is prohibited.

---

# Access Control

Files are private by default.

Access requires:

- Authentication
- Authorization
- Resource ownership validation

Administrators may access files only when required for platform administration.

---

# Download Flow

```text
Download Request

↓

JWT Validation

↓

Ownership Validation

↓

Generate Signed URL

↓

Temporary Download

↓

URL Expiration
```

---

# Signed URLs

Version 1

Signed URLs are generated for private downloads.

Properties

- Short-lived
- Single resource
- HTTPS only

Suggested expiration

```
5 minutes
```

---

# Malware Protection

Version 1

- File validation only

Future

- Antivirus scanning
- Malware quarantine
- Threat intelligence integration

Suspicious files must never be processed.

---

# Temporary Files

Temporary files include:

- OCR artifacts
- AI processing outputs
- Intermediate documents

Requirements

- Automatically deleted
- Never publicly accessible
- Time-limited retention

---

# File Metadata

Stored metadata

- File ID
- Original filename
- Storage filename
- MIME type
- Size
- Upload timestamp
- Owner ID
- SHA-256 checksum (optional)

---

# Retention Policy

| File | Retention |
|------|-----------|
| Resume | Until user deletes |
| Reports | Until user deletes |
| Temporary Files | Automatic cleanup |
| Archived Logs | According to operational policy |

---

# Secure Deletion

Deleting a file removes:

- Database metadata
- Storage object
- Temporary references

Deletion events are logged.

---

# Common Error Codes

```
UNSUPPORTED_FILE

INVALID_MIME_TYPE

FILE_TOO_LARGE

UPLOAD_FAILED

FILE_NOT_FOUND

ACCESS_DENIED

DOWNLOAD_EXPIRED
```

---

# Security Best Practices

- Validate every upload.
- Never trust filenames.
- Never trust MIME headers alone.
- Store files outside the web root.
- Generate random storage identifiers.
- Restrict file downloads through authorization.
- Delete temporary files automatically.
- Log upload and deletion events.

---

# Business Rules

- Only supported file types are accepted.
- Every upload requires authentication.
- Every download requires authorization.
- Files are private by default.
- Storage identifiers must be globally unique.
- Temporary artifacts must be cleaned automatically.

---

# Related Documents

- `api-security.md`
- `encryption.md`
- `prompt-security.md`
- `audit-logging.md`
- `../05-api-design/resume.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial file security architecture specification |