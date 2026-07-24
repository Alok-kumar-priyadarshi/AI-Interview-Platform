
# User Stories

**Document ID:** DOC-PRJ-006
**Version:** 1.0.0
**Status:** Draft
**Owner:** Project Architect
**Last Updated:** 2026-07-23

---

# Purpose

This document captures the functional behavior of the platform from the user's perspective.
Each story is independently implementable and traceable to features, APIs, UI screens,
backend services, and test cases.

---

# Story Status

- Planned
- In Progress
- Completed
- Blocked

---

# Epic EP-001 — Authentication

## US-001 — Google Login

**Priority:** Critical

**User Story**

As a job seeker,
I want to sign in using my Google account,
so that I can securely access my interview history.

**Acceptance Criteria**

- Google OAuth succeeds.
- User profile is created automatically.
- Existing users are logged in.
- JWT session is established.

**Related Features**

- FR-001
- FR-002
- FR-003

---

# Epic EP-002 — Resume Management

## US-002 — Upload Resume

**Priority:** Critical

As a user,
I want to upload my resume,
so the AI can personalize the interview.

Acceptance Criteria

- PDF validation
- Resume stored
- Resume parsed
- Resume summary generated

Related Features

- FR-010
- FR-011
- FR-012

---

# Epic EP-003 — Interview Configuration

## US-003 — Configure Interview

Priority: Critical

As a user,
I want to configure the interview before it starts,
so that it matches my preparation goals.

Acceptance Criteria

- Difficulty selectable
- Target package selectable
- Question count selectable
- Duration selectable
- Voice selectable
- Interview mode selectable

Related Features

- FR-020
- FR-021
- FR-022
- FR-023
- FR-024
- FR-025

---

# Epic EP-004 — AI Interview

## US-004 — Conduct Interview

Priority: Critical

As a user,
I want the AI interviewer to ask realistic questions,
so I can practice effectively.

Acceptance Criteria

- Resume-aware questions
- Follow-up questions
- Voice conversation
- Text conversation
- Session timer
- Session persistence

Related Features

- FR-030
- FR-031
- FR-032
- FR-033
- FR-034
- FR-035

---

# Epic EP-005 — Evaluation

## US-005 — Receive Feedback

Priority: Critical

As a user,
I want detailed interview feedback,
so I know how to improve.

Acceptance Criteria

- Technical score
- Communication score
- Confidence score
- Strength analysis
- Weakness analysis
- Personalized roadmap

Related Features

- FR-040
- FR-041
- FR-042
- FR-043
- FR-044
- FR-045
- FR-046

---

# Epic EP-006 — Progress Tracking

## US-006 — View Progress

Priority: High

As a returning user,
I want to review previous interviews,
so I can measure improvement.

Acceptance Criteria

- Interview history
- Analytics dashboard
- Previous reports
- Progress timeline

Related Features

- FR-050
- FR-051
- FR-052
- FR-053

---

# Definition of Done

A story is complete only if:

- Requirements implemented
- API implemented
- Backend completed
- Frontend completed
- Tests written
- Documentation updated
- Mermaid updated
- Context updated

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial user stories |
