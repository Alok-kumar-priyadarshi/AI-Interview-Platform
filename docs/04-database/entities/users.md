# Users Entity

**Document ID:** DB-003-001

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

The `users` table stores authenticated users of the AI Career Interview Platform.

Every authenticated feature in the system ultimately references a user record.

The application uses Google OAuth for authentication. Passwords are never stored.

---

# Responsibilities

The users entity is responsible for:

- User identity
- Google account mapping
- Display information
- Account status
- Authentication metadata
- Audit timestamps

It is **not** responsible for:

- Resume data
- Interview data
- AI evaluations
- Reports

---

# Table Definition

| Column | Type | Nullable | Default |
|---------|------|----------|----------|
| id | UUID | No | uuid_generate_v4() |
| google_id | VARCHAR(255) | No | — |
| email | VARCHAR(320) | No | — |
| full_name | VARCHAR(255) | No | — |
| profile_picture_url | TEXT | Yes | NULL |
| role | VARCHAR(32) | No | 'candidate' |
| is_active | BOOLEAN | No | TRUE |
| last_login_at | TIMESTAMP WITH TIME ZONE | Yes | NULL |
| created_at | TIMESTAMP WITH TIME ZONE | No | NOW() |
| updated_at | TIMESTAMP WITH TIME ZONE | No | NOW() |

---

# Primary Key

```
id UUID
```

Characteristics:

- Globally unique
- Immutable
- Never reused
- Referenced by foreign keys

---

# Candidate Key

```
google_id
```

Google guarantees uniqueness.

---

# Alternate Key

```
email
```

Email addresses are unique across users.

---

# Column Definitions

## id

Purpose:

Primary identifier.

Rules:

- UUID
- Immutable
- Generated automatically

---

## google_id

Stores the unique Google account identifier.

Constraints:

- Required
- Unique
- Immutable

---

## email

Stores the verified Google email.

Rules:

- Required
- Unique
- Lowercase
- Verified by Google OAuth

---

## full_name

Display name received from Google.

Rules:

- Required
- Trim whitespace
- Maximum 255 characters

---

## profile_picture_url

Optional Google profile image.

May be refreshed during login.

---

## role

Current values:

```
candidate
```

Reserved values:

```
admin

moderator

support
```

---

## is_active

Determines whether the account may access the platform.

Inactive accounts cannot authenticate.

---

## last_login_at

Updated after every successful authentication.

---

## created_at

Creation timestamp.

Never modified.

---

## updated_at

Updated whenever mutable profile fields change.

---

# Constraints

Primary Key

```
pk_users
```

Unique

```
uq_users_google_id

uq_users_email
```

Check

```
chk_users_role
```

Allowed values:

```
candidate

admin

moderator

support
```

---

# Indexes

Primary

```
pk_users
```

Unique

```
idx_users_google_id

idx_users_email
```

Secondary

```
idx_users_role

idx_users_is_active
```

---

# Relationships

Parent of:

```
resumes

interviews

audit_logs
```

Referenced by:

```
user_id
```

---

# Business Rules

- Every authenticated user has exactly one user record.
- Users authenticate only through Google OAuth.
- Emails are unique.
- Google IDs never change.
- User deletion is restricted if dependent records exist.

---

# Lifecycle

```text
OAuth Login

↓

User Created

↓

Profile Updated

↓

Interviews Created

↓

Resume Uploaded

↓

History Accumulates

↓

Account Deactivated (Optional)
```

---

# Validation Rules

Email

- Required
- RFC-compliant
- Lowercase

Name

- Required
- Non-empty
- Maximum 255 characters

Role

- Must be one of the allowed enum values

Google ID

- Required
- Unique

---

# Security Considerations

Do not store:

- OAuth access tokens
- Refresh tokens
- Passwords
- Session secrets

Only verified identity information should be persisted.

---

# SQL Example

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    google_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(320) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    profile_picture_url TEXT,
    role VARCHAR(32) NOT NULL DEFAULT 'candidate',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_login_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

# SQLAlchemy Example

```python
class User(Base):
    __tablename__ = "users"

    id = mapped_column(UUID(as_uuid=True), primary_key=True)

    google_id = mapped_column(String(255), unique=True, nullable=False)

    email = mapped_column(String(320), unique=True, nullable=False)

    full_name = mapped_column(String(255), nullable=False)

    profile_picture_url = mapped_column(Text)

    role = mapped_column(String(32), default="candidate")

    is_active = mapped_column(Boolean, default=True)

    last_login_at = mapped_column(DateTime(timezone=True))

    created_at = mapped_column(DateTime(timezone=True))

    updated_at = mapped_column(DateTime(timezone=True))
```

---

# Future Enhancements

Potential additions:

- Preferred language
- Time zone
- Notification preferences
- Subscription tier
- Account settings
- MFA configuration
- User preferences

These additions should preserve backward compatibility.

---

# Related Documents

- `schema-overview.md`
- `er-diagram.md`
- `relationships.md`
- `constraints.md`
- `../../03-architecture/authentication-architecture.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial users entity specification |