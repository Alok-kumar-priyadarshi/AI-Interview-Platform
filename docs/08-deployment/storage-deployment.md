# Object Storage Deployment Architecture

**Document ID:** DEP-006

**Version:** 1.0.0

**Status:** Approved

**Priority:** High

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the deployment architecture for cloud object storage used by the AI Career Interview Platform.

Object storage is responsible for securely storing uploaded resumes, generated reports, temporary exports, and future media assets while ensuring durability, scalability, and secure access.

---

# Objectives

The storage architecture provides:

- Secure file storage
- High durability
- Scalability
- Low operational overhead
- Fast uploads
- Secure downloads
- Lifecycle management
- Disaster recovery support

---

# Technology

Primary Recommendation

- Cloudflare R2

Compatible Alternatives

- AWS S3
- Supabase Storage
- DigitalOcean Spaces
- MinIO (self-hosted)

Storage access is implemented using the S3-compatible API.

---

# Storage Architecture

```text
Browser

↓

FastAPI Backend

↓

Upload Validation

↓

Object Storage

↓

Database Metadata
```

The backend is the only component that communicates directly with storage.

---

# Responsibilities

The storage system stores:

- Resume PDFs
- Resume DOCX files
- Resume TXT files
- Generated reports
- User profile images (future)
- AI-generated exports (future)
- Temporary processing files

---

# Storage Principles

The platform follows:

- Object storage only
- Immutable uploads
- Metadata stored in PostgreSQL
- Private buckets
- Signed URL access
- Server-side encryption

---

# Bucket Organization

Recommended structure

```text
career-interview-platform/

resumes/

exports/

temp/

avatars/

logs/
```

Future buckets may be introduced for analytics and backups.

---

# Folder Organization

Example

```text
resumes/

user-id/

resume-id.pdf
```

Example

```text
exports/

user-id/

evaluation-report.pdf
```

---

# Upload Pipeline

```text
User Upload

↓

Frontend

↓

Backend Validation

↓

Virus Scan (Future)

↓

Storage Upload

↓

Database Metadata

↓

Success Response
```

Only validated files are uploaded.

---

# Supported File Types

Allowed

- PDF
- DOCX
- TXT

Future

- Markdown
- Images

Unsupported types are rejected.

---

# File Size Limits

Recommended limits

| File | Maximum |
|------|---------:|
| Resume | 10 MB |
| Export | 20 MB |
| Image | 5 MB |

Limits should be configurable.

---

# Naming Strategy

Avoid user-provided filenames.

Preferred format

```text
UUID.extension
```

Example

```text
7bc6c2fd-2f91-41d6.pdf
```

Original filenames may be stored as metadata.

---

# Metadata

Database stores

- Object ID
- Owner
- Original filename
- MIME type
- File size
- Upload timestamp
- Storage path
- Checksum

Binary content remains in object storage.

---

# Access Control

Buckets remain private.

Access occurs through:

- Backend authorization
- Signed URLs
- Ownership validation

Anonymous public access is prohibited.

---

# Signed URLs

Downloads use time-limited signed URLs.

Example lifetime

- 5 minutes

Signed URLs should:

- Expire automatically
- Be user-specific
- Be generated server-side

---

# Encryption

Storage should support:

- Encryption at rest
- HTTPS in transit
- Server-side encryption

Sensitive files should never travel over unencrypted connections.

---

# Lifecycle Policy

Temporary files

Retention

- 24 hours

Exports

Retention

- 30 days

Resumes

Retention

- Until user deletion or account removal

Lifecycle rules should be automated where supported.

---

# Deletion Workflow

```text
Delete Request

↓

Authorization Check

↓

Delete Object

↓

Delete Metadata

↓

Audit Log
```

Deletion failures should be retried safely.

---

# Versioning

Versioning is optional for Version 1.

Future support may include:

- Resume history
- Report history
- Soft deletion
- File recovery

---

# CDN Integration

Static downloads may use:

- Cloudflare CDN
- Provider CDN

Sensitive files must still require authorization before access.

---

# Monitoring

Monitor

- Storage utilization
- Upload failures
- Download failures
- Latency
- API errors
- Bucket health
- Transfer volume

Alerts should be configured for abnormal activity.

---

# Disaster Recovery

Recovery includes:

- Object replication (future)
- Backup verification
- Restore procedures
- Integrity validation

Critical user documents should remain recoverable.

---

# Security

Storage security requires:

- Private buckets
- Least-privilege credentials
- Server-side validation
- MIME verification
- File extension validation
- Size validation
- Malware scanning (future)

---

# Deployment Validation

Verify

- Bucket exists
- Credentials valid
- Upload succeeds
- Download succeeds
- Signed URLs function
- Delete operation works
- Metadata consistency

---

# Operational Best Practices

- Store metadata separately.
- Validate uploads before storage.
- Generate signed URLs server-side.
- Monitor storage growth.
- Encrypt all traffic.

---

# Anti-Patterns

Avoid

- Public buckets
- Hardcoded credentials
- Predictable filenames
- Database BLOB storage
- Unlimited uploads
- Client-generated signed URLs

---

# Business Rules

- All uploaded files require server-side validation.
- Buckets remain private by default.
- Metadata resides in PostgreSQL.
- Downloads require authorization.
- Production storage credentials are managed through secure environment variables.

---

# Related Documents

- `backend-deployment.md`
- `database-deployment.md`
- `environment-variables.md`
- `backup-recovery.md`
- `monitoring.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial object storage deployment architecture specification |