# Resumes Entity

**Document ID:** DB-003-002

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

The `resumes` table stores metadata for every resume uploaded by a user.

It does **not** store the actual resume file. Instead, it stores metadata,
processing status, storage references, and links to AI-generated candidate
profiles.

The original resume remains the source of truth.

---

# Responsibilities

The resumes entity is responsible for:

- Resume ownership
- File metadata
- Storage reference
- Upload tracking
- Parsing status
- AI processing status
- Version tracking

It is **not** responsible for:

- Parsed resume contents
- Candidate skills
- AI analysis
- Interview generation

---

# Table Definition

| Column | Type | Nullable | Default |
|---------|------|----------|----------|
| id | UUID | No | uuid_generate_v4() |
| user_id | UUID | No | — |
| original_filename | VARCHAR(255) | No | — |
| stored_filename | VARCHAR(255) | No | — |
| storage_path | TEXT | No | — |
| mime_type | VARCHAR(100) | No | — |
| file_size_bytes | BIGINT | No | — |
| checksum_sha256 | CHAR(64) | No | — |
| upload_status | VARCHAR(30) | No | 'uploaded' |
| processing_status | VARCHAR(30) | No | 'pending' |
| ai_model_version | VARCHAR(50) | Yes | NULL |
| processing_started_at | TIMESTAMPTZ | Yes | NULL |
| processing_completed_at | TIMESTAMPTZ | Yes | NULL |
| created_at | TIMESTAMPTZ | No | NOW() |
| updated_at | TIMESTAMPTZ | No | NOW() |

---

# Primary Key

```
id UUID
```

Characteristics:

- Immutable
- Globally unique
- Referenced by candidate_profiles

---

# Foreign Keys

```
user_id

↓

users.id
```

Relationship:

```
One User

↓

Many Resumes
```

---

# Column Definitions

## original_filename

The filename uploaded by the user.

Example:

```
John_Doe_Resume.pdf
```

---

## stored_filename

Internal storage filename.

Example:

```
2e1cb8b3-2a93-4d18-bc12.pdf
```

---

## storage_path

Reference to the stored file.

Examples:

```
uploads/resumes/...

s3://bucket/...

gs://bucket/...
```

Never expose internal storage paths directly to clients.

---

## mime_type

Examples:

```
application/pdf

application/vnd.openxmlformats-officedocument.wordprocessingml.document
```

Only supported file types are accepted.

---

## file_size_bytes

Stores file size.

Validation:

- Greater than 0
- Below configured upload limit

---

## checksum_sha256

SHA-256 hash of the uploaded file.

Uses:

- Duplicate detection
- Integrity verification
- File validation

---

## upload_status

Allowed values:

```
uploaded

failed

deleted
```

Tracks upload completion.

---

## processing_status

Allowed values:

```
pending

processing

completed

failed
```

Tracks AI processing lifecycle.

---

## ai_model_version

Stores the AI model version that generated the candidate profile.

Example:

```
groq-llama-4-v1
```

Useful for future reprocessing.

---

## processing_started_at

Timestamp when AI analysis begins.

---

## processing_completed_at

Timestamp when AI analysis completes.

---

## created_at

Upload timestamp.

---

## updated_at

Updated whenever metadata or processing status changes.

---

# Constraints

Primary Key

```
pk_resumes
```

Foreign Key

```
fk_resumes_user
```

Unique

```
uq_resumes_checksum_sha256
```

Check Constraints

```
chk_upload_status

chk_processing_status

chk_file_size
```

---

# Indexes

Primary

```
pk_resumes
```

Secondary

```
idx_resumes_user_id

idx_resumes_processing_status

idx_resumes_created_at

idx_resumes_checksum
```

---

# Relationships

Parent:

```
candidate_profiles
```

Child of:

```
users
```

---

# Business Rules

- Every resume belongs to exactly one user.
- Original resume files remain immutable.
- Processing status changes only through the Resume Service.
- Candidate profiles must reference an existing resume.
- Files failing validation are not persisted.

---

# Resume Lifecycle

```text
Upload

↓

Validate

↓

Store Metadata

↓

Store File

↓

Pending

↓

AI Processing

↓

Completed

↓

Candidate Profile Generated
```

---

# Validation Rules

Filename

- Required
- Maximum 255 characters

File Size

- Greater than 0
- Within configured limit

Checksum

- Required
- SHA-256
- Exactly 64 hexadecimal characters

MIME Type

Allowed values:

- PDF
- DOCX

Unsupported formats are rejected.

---

# Security Considerations

The database must **not** store:

- Resume text
- Parsed content
- AI prompts
- Candidate analysis

Only metadata belongs in this table.

Storage paths should never expose internal infrastructure details.

---

# SQL Example

```sql
CREATE TABLE resumes (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    original_filename VARCHAR(255) NOT NULL,
    stored_filename VARCHAR(255) NOT NULL,
    storage_path TEXT NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    file_size_bytes BIGINT NOT NULL,
    checksum_sha256 CHAR(64) UNIQUE NOT NULL,
    upload_status VARCHAR(30) NOT NULL DEFAULT 'uploaded',
    processing_status VARCHAR(30) NOT NULL DEFAULT 'pending',
    ai_model_version VARCHAR(50),
    processing_started_at TIMESTAMPTZ,
    processing_completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

# SQLAlchemy Example

```python
class Resume(Base):
    __tablename__ = "resumes"

    id = mapped_column(UUID(as_uuid=True), primary_key=True)

    user_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    original_filename = mapped_column(String(255), nullable=False)

    stored_filename = mapped_column(String(255), nullable=False)

    storage_path = mapped_column(Text, nullable=False)

    mime_type = mapped_column(String(100), nullable=False)

    file_size_bytes = mapped_column(BigInteger, nullable=False)

    checksum_sha256 = mapped_column(String(64), unique=True)

    upload_status = mapped_column(String(30), default="uploaded")

    processing_status = mapped_column(String(30), default="pending")

    ai_model_version = mapped_column(String(50))

    processing_started_at = mapped_column(DateTime(timezone=True))

    processing_completed_at = mapped_column(DateTime(timezone=True))

    created_at = mapped_column(DateTime(timezone=True))

    updated_at = mapped_column(DateTime(timezone=True))
```

---

# Future Enhancements

Possible additions:

- Resume language
- OCR status
- Virus scan result
- Storage provider
- Resume versioning
- Parsing confidence
- Upload source
- Encryption metadata

These enhancements should preserve backward compatibility.

---

# Related Documents

- `users.md`
- `candidate_profiles.md`
- `../schema-overview.md`
- `../er-diagram.md`
- `../../03-architecture/ai-architecture.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial resumes entity specification |