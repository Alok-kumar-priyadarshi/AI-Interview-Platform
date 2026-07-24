# Audit Logs Entity

**Document ID:** DB-003-009

**Version:** 1.0.0

**Status:** Approved

**Priority:** High

**Last Updated:** 2026-07-23

---

# Purpose

The `audit_logs` table stores immutable records of significant security,
authentication, and business events that occur within the AI Career Interview
Platform.

Audit records provide traceability, accountability, debugging support,
operational monitoring, and compliance evidence.

Audit logs are append-only.

---

# Responsibilities

The audit_logs entity is responsible for:

- Authentication events
- User activity tracking
- Administrative actions
- Security events
- Resource access logging
- Error event recording
- Compliance auditing

It is **not** responsible for:

- Application metrics
- Performance monitoring
- Business analytics
- User-generated content

---

# Table Definition

| Column | Type | Nullable | Default |
|---------|------|----------|----------|
| id | UUID | No | uuid_generate_v4() |
| user_id | UUID | Yes | NULL |
| event_type | VARCHAR(50) | No | — |
| severity | VARCHAR(20) | No | 'info' |
| resource_type | VARCHAR(50) | Yes | NULL |
| resource_id | UUID | Yes | NULL |
| action | VARCHAR(100) | No | — |
| description | TEXT | Yes | NULL |
| request_id | UUID | Yes | NULL |
| ip_address | INET | Yes | NULL |
| user_agent | TEXT | Yes | NULL |
| metadata | JSONB | No | '{}' |
| occurred_at | TIMESTAMPTZ | No | NOW() |
| created_at | TIMESTAMPTZ | No | NOW() |

---

# Primary Key

```
id UUID
```

Each audit record has a globally unique identifier.

Audit records are immutable.

---

# Foreign Key

```
user_id

↓

users.id
```

Relationship:

```
One User

↓

Many Audit Logs
```

System-generated events may have:

```
user_id = NULL
```

---

# Column Definitions

## event_type

High-level event classification.

Examples:

```
authentication

authorization

resume_upload

resume_processing

interview

evaluation

report

security

system

admin
```

---

## severity

Allowed values:

```
debug

info

warning

error

critical
```

---

## resource_type

Business object involved.

Examples:

```
user

resume

interview

question

answer

evaluation

report
```

---

## resource_id

UUID of the affected resource.

Example:

```
resume_id

interview_id

report_id
```

---

## action

Specific action performed.

Examples:

```
LOGIN_SUCCESS

LOGIN_FAILED

UPLOAD_RESUME

START_INTERVIEW

SUBMIT_ANSWER

GENERATE_REPORT

DELETE_RESUME
```

---

## description

Human-readable explanation.

Example:

```
Candidate successfully uploaded resume.
```

---

## request_id

Unique request identifier.

Allows correlation across logs.

---

## ip_address

Originating client IP.

Supports:

- IPv4
- IPv6

---

## user_agent

Browser or client identifier.

Used for security investigations.

---

## metadata

Additional structured information.

Example:

```json
{
  "browser": "Chrome",
  "platform": "Windows",
  "processing_time_ms": 1450
}
```

---

## occurred_at

Timestamp when the event actually occurred.

---

## created_at

Timestamp when the audit record was persisted.

Usually identical to `occurred_at`.

---

# Constraints

Primary Key

```
pk_audit_logs
```

Foreign Key

```
fk_audit_logs_user
```

Check Constraints

```
chk_event_type

chk_severity
```

---

# Indexes

Primary

```
pk_audit_logs
```

Secondary

```
idx_audit_user

idx_audit_event_type

idx_audit_resource

idx_audit_occurred_at

idx_audit_request

idx_audit_severity
```

Composite

```
(user_id, occurred_at DESC)

(resource_type, resource_id)

(event_type, occurred_at DESC)
```

---

# Relationships

Child of:

```
users
```

References business entities indirectly through:

```
resource_type

resource_id
```

No foreign keys are created for polymorphic resources.

---

# Business Rules

- Audit records are append-only.
- Updates are prohibited.
- Deletes are prohibited except under retention policy.
- Security events must always be logged.
- Failed authentication attempts must be logged.
- Administrative actions must always be logged.

---

# Audit Lifecycle

```text
Business Event

↓

Audit Record Created

↓

Persisted

↓

Indexed

↓

Available for Search

↓

Archived

↓

Deleted (Retention Policy)
```

---

# Validation Rules

Severity

Allowed values:

- debug
- info
- warning
- error
- critical

Action

- Required
- Maximum 100 characters

Metadata

- Valid JSON

Description

- Optional
- Maximum 5,000 characters

---

# Retention Policy

Default retention:

```
365 Days
```

Security events:

```
730 Days
```

Critical administrative events:

```
7 Years
```

Retention duration should remain configurable.

---

# Compliance Considerations

The audit system should support:

- GDPR
- SOC 2
- ISO 27001
- Internal security investigations

Personally identifiable information should be minimized.

Sensitive values (tokens, passwords, secrets) must never be written to audit logs.

---

# Security Considerations

Never log:

- OAuth tokens
- API keys
- Passwords
- Session secrets
- Full resume contents
- AI prompts

Logs should be write-only for application services.

---

# SQL Example

```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    event_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    resource_type VARCHAR(50),
    resource_id UUID,
    action VARCHAR(100) NOT NULL,
    description TEXT,
    request_id UUID,
    ip_address INET,
    user_agent TEXT,
    metadata JSONB NOT NULL,
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

# SQLAlchemy Example

```python
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = mapped_column(UUID(as_uuid=True), primary_key=True)

    user_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id")
    )

    event_type = mapped_column(String(50), nullable=False)

    severity = mapped_column(String(20), default="info")

    resource_type = mapped_column(String(50))

    resource_id = mapped_column(UUID(as_uuid=True))

    action = mapped_column(String(100), nullable=False)

    description = mapped_column(Text)

    request_id = mapped_column(UUID(as_uuid=True))

    ip_address = mapped_column(postgresql.INET)

    user_agent = mapped_column(Text)

    metadata = mapped_column(JSONB)

    occurred_at = mapped_column(DateTime(timezone=True))

    created_at = mapped_column(DateTime(timezone=True))
```

---

# Future Enhancements

Potential additions:

- Geographic location
- Device fingerprint
- Session identifier
- Correlation IDs
- Distributed tracing
- SIEM integration
- Real-time alert flags
- Risk score

---

# Related Documents

- `users.md`
- `../relationships.md`
- `../constraints.md`
- `../../07-security/`
- `../../09-backend/`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial audit logs entity specification |