# Encryption Architecture

**Document ID:** SEC-006

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the encryption strategy for the AI Career Interview Platform.

The platform protects all sensitive information using industry-standard cryptographic practices.

This document covers:

- Encryption in transit
- Encryption at rest
- TLS configuration
- Key management
- Secret protection
- Database encryption
- Object storage encryption
- Cryptographic algorithms

---

# Security Goals

Encryption protects:

- User privacy
- Resume data
- AI interview data
- Authentication tokens
- API credentials
- Infrastructure secrets

The platform follows a defense-in-depth approach.

---

# Encryption Architecture

```text
User

↓

HTTPS (TLS)

↓

Frontend

↓

FastAPI Backend

↓

Encrypted Database

↓

Encrypted Object Storage

↓

Encrypted Backups
```

Every communication channel and storage layer must be encrypted.

---

# Encryption in Transit

All network communication uses:

```
HTTPS
```

Protocol

```
TLS 1.2+
```

Preferred

```
TLS 1.3
```

HTTP traffic is automatically redirected to HTTPS.

---

# TLS Configuration

Minimum Version

```
TLS 1.2
```

Preferred

```
TLS 1.3
```

Disabled

- SSL 2.0
- SSL 3.0
- TLS 1.0
- TLS 1.1

Weak cipher suites must never be enabled.

---

# Protected Network Traffic

Encryption applies to:

- Browser ↔ Frontend
- Frontend ↔ Backend
- Backend ↔ PostgreSQL
- Backend ↔ Groq API
- Backend ↔ Object Storage
- Internal service communication

---

# Encryption at Rest

The following data must remain encrypted at rest:

- PostgreSQL volumes
- Resume files
- Generated reports
- Audio recordings (if retained)
- Database backups
- Log archives
- Infrastructure snapshots

---

# Database Encryption

Database storage relies on encrypted storage volumes provided by the hosting platform.

Protected data includes:

- User accounts
- Candidate profiles
- Interview history
- Evaluations
- Reports
- Metadata

Application-level encryption may be added for highly sensitive fields in future releases.

---

# Object Storage Encryption

Stored assets include:

- PDF resumes
- DOCX resumes
- Generated reports
- Temporary AI artifacts

Requirements

- Server-side encryption enabled
- Random object identifiers
- Private access only
- Signed URLs when temporary access is required

---

# Cryptographic Algorithms

Approved algorithms

| Purpose | Algorithm |
|----------|-----------|
| HTTPS | TLS 1.2 / TLS 1.3 |
| JWT Signing | HS256 |
| Password Hashing | Not Applicable |
| Random Values | CSPRNG |
| File Integrity | SHA-256 (optional) |

Future

- RS256 JWT signing
- AES-256 application-level encryption

---

# Key Management

Secrets include:

- JWT signing key
- Google OAuth client secret
- Database credentials
- API keys
- Encryption keys

Requirements

- Store only in environment variables
- Never commit to source control
- Restrict production access
- Rotate periodically
- Maintain separate keys per environment

---

# Secret Rotation

Rotation should occur:

- During scheduled maintenance
- After suspected compromise
- During infrastructure migration
- According to organizational policy

After rotation:

- Update environment variables
- Restart affected services
- Verify successful deployment

---

# Random Number Generation

Random values must be generated using a cryptographically secure random number generator.

Used for:

- JWT secrets
- OAuth state values
- Temporary tokens
- File identifiers
- Request identifiers

Predictable random values are prohibited.

---

# Backup Encryption

Encrypted backups must include:

- Database snapshots
- Object storage backups
- Configuration backups

Backup encryption keys must be managed independently of application credentials.

---

# Logging Considerations

Encrypted or sensitive values must never appear in logs.

Never log:

- JWT secrets
- OAuth client secrets
- API keys
- Database passwords
- Session tokens
- Encryption keys

---

# Business Rules

- Every external connection must use HTTPS.
- Sensitive storage must remain encrypted at rest.
- Secrets are never hardcoded.
- Cryptographic algorithms must follow current industry recommendations.
- Keys must be replaceable without changing application logic.

---

# Future Enhancements

Planned improvements

- Customer-managed encryption keys
- Envelope encryption
- Automatic key rotation
- Hardware Security Module (HSM) integration
- Field-level encryption for PII

---

# Related Documents

- `authentication.md`
- `jwt.md`
- `secrets-management.md`
- `api-security.md`
- `../02-tech-stack/backend.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial encryption architecture specification |