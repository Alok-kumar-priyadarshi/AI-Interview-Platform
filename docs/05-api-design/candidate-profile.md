# Candidate Profile API

**Document ID:** API-003

**Version:** 1.0.0

**Status:** Approved

**Priority:** High

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the Candidate Profile API used by the AI Career Interview Platform.

The candidate profile stores structured information that personalizes:

- Interview generation
- Difficulty selection
- Resume evaluation
- Salary estimation
- AI recommendations

Each authenticated user owns exactly one candidate profile.

---

# Resource

```
/candidate-profile
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
| Candidate | Own profile |
| Admin | Any profile |

---

# Endpoint Summary

| Method | Endpoint | Description |
|----------|----------|-------------|
| GET | /candidate-profile | Retrieve profile |
| POST | /candidate-profile | Create profile |
| PATCH | /candidate-profile | Update profile |
| DELETE | /candidate-profile | Delete profile |

---

# Candidate Profile Schema

| Field | Type |
|------|------|
| id | UUID |
| user_id | UUID |
| target_role | String |
| experience_years | Integer |
| current_company | String |
| education | String |
| degree | String |
| university | String |
| graduation_year | Integer |
| skills | Array<String> |
| preferred_domains | Array<String> |
| expected_salary_min | Integer |
| expected_salary_max | Integer |
| preferred_interview_language | String |
| preferred_interviewer_voice | String |
| preferred_interview_type | String |
| created_at | Timestamp |
| updated_at | Timestamp |

---

# GET /candidate-profile

## Purpose

Returns the authenticated user's candidate profile.

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
    "id": "uuid",
    "target_role": "Backend Developer",
    "experience_years": 1,
    "education": "B.Tech Computer Science",
    "degree": "Bachelor of Technology",
    "university": "AKTU",
    "graduation_year": 2027,
    "skills": [
      "Python",
      "FastAPI",
      "PostgreSQL"
    ],
    "preferred_domains": [
      "Backend",
      "AI"
    ],
    "expected_salary_min": 600000,
    "expected_salary_max": 1200000,
    "preferred_interview_language": "en",
    "preferred_interviewer_voice": "female",
    "preferred_interview_type": "technical"
  }
}
```

---

# POST /candidate-profile

## Purpose

Creates the user's candidate profile.

Only one profile may exist per user.

---

Request

```json
{
  "target_role": "Backend Developer",
  "experience_years": 1,
  "education": "B.Tech Computer Science",
  "degree": "Bachelor of Technology",
  "university": "AKTU",
  "graduation_year": 2027,
  "skills": [
    "Python",
    "FastAPI",
    "SQL"
  ],
  "preferred_domains": [
    "Backend",
    "AI"
  ],
  "expected_salary_min": 600000,
  "expected_salary_max": 1200000,
  "preferred_interview_language": "en",
  "preferred_interviewer_voice": "female",
  "preferred_interview_type": "technical"
}
```

---

Success Response

```json
{
  "success": true,
  "message": "Candidate profile created successfully."
}
```

---

Status Codes

| Code | Meaning |
|------|----------|
| 201 | Created |
| 400 | Invalid request |
| 401 | Unauthorized |
| 409 | Profile already exists |
| 422 | Validation failed |

---

# PATCH /candidate-profile

## Purpose

Updates candidate profile information.

All fields are optional.

---

Example Request

```json
{
  "experience_years": 2,
  "skills": [
    "Python",
    "FastAPI",
    "Docker",
    "Redis"
  ]
}
```

---

Response

```json
{
  "success": true,
  "message": "Candidate profile updated successfully."
}
```

---

# DELETE /candidate-profile

## Purpose

Deletes the candidate profile.

Does not delete:

- User account
- Interviews
- Reports

---

Response

```json
{
  "success": true,
  "message": "Candidate profile deleted."
}
```

---

# Validation Rules

## Target Role

- Required
- 2–100 characters

---

## Experience

```
0–50 years
```

---

## Graduation Year

```
1900–2100
```

---

## Salary Range

Minimum

```
>= 0
```

Maximum

```
>= minimum salary
```

---

## Skills

Requirements

- Unique values
- Maximum 100 skills
- Maximum 50 characters per skill

---

## Preferred Domains

Examples

- Backend
- Frontend
- AI
- ML
- DevOps
- Data Science
- Cybersecurity
- Cloud
- Mobile

---

## Preferred Language

Supported

```
en

hi
```

---

## Preferred Interview Voice

Allowed

```
male

female
```

---

## Preferred Interview Type

Allowed

```
technical

behavioral

mixed
```

---

# Business Rules

- One profile per user.
- Skills are case-insensitive.
- Salary values are annual.
- Updating preferences affects future interviews only.
- Existing interviews remain unchanged.

---

# Authorization

Every request verifies:

- JWT token
- User ownership
- Resource existence

Admins may access any profile.

---

# Rate Limits

| Endpoint | Limit |
|-----------|--------|
| GET | 100/min |
| POST | 5/day |
| PATCH | 20/min |
| DELETE | 2/day |

---

# Error Responses

Profile Exists

```json
{
  "success": false,
  "error": {
    "code": "PROFILE_EXISTS",
    "message": "Candidate profile already exists."
  }
}
```

---

Profile Not Found

```json
{
  "success": false,
  "error": {
    "code": "PROFILE_NOT_FOUND",
    "message": "Candidate profile not found."
  }
}
```

---

Validation Error

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid candidate profile."
  }
}
```

---

# OpenAPI Tags

```
Candidate Profile
```

---

# Related Documents

- `users.md`
- `resume.md`
- `interviews.md`
- `errors.md`
- `../04-database/entities/candidate_profiles.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial Candidate Profile API specification |