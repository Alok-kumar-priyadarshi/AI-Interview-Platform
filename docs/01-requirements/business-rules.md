# Business Rules

**Document ID:** DOC-REQ-003
**Rule Prefix:** BR
**Version:** 1.0.0
**Status:** Draft
**Owner:** Project Architect
**Last Updated:** 2026-07-23

---

# Purpose

Business Rules define mandatory policies that govern how the platform behaves.
Unlike functional requirements, these rules must always hold true regardless of implementation.

---

# BR-001 Authentication

- Every interview session requires an authenticated user.
- Guest interviews are not allowed in Version 1.
- Google OAuth is the only supported authentication method.

Related Features:
- FR-001
- FR-002

---

# BR-002 Resume Rules

- A resume is required before starting an interview.
- Only PDF resumes are accepted.
- Users may keep multiple resume versions.
- One interview is associated with exactly one resume version.

Related Features:
- FR-010
- FR-011
- FR-012

---

# BR-003 Interview Configuration

Users must configure before starting:
- Difficulty
- Target package
- Question count
- Interview duration
- Interview mode
- Voice preference

System shall validate all configuration values.

---

# BR-004 Interview Session

- A user may have only one active interview at a time.
- An interview may be resumed only if it was interrupted.
- All questions and answers must be stored after completion.

---

# BR-005 AI Rules

- AI must use resume context when generating questions.
- AI must adapt question complexity to selected difficulty.
- AI should ask follow-up questions when appropriate.
- AI must not fabricate resume information.

---

# BR-006 Evaluation

Every completed interview must generate:
- Technical score
- Communication score
- Confidence score
- Strengths
- Weaknesses
- Personalized improvement roadmap
- Overall summary

Reports cannot be manually edited by users.

---

# BR-007 History

- Completed interviews must be retained.
- Users can view only their own interview history.
- Deleted interviews must not appear in analytics.

---

# BR-008 Security

- Users may access only their own data.
- Uploaded files must be validated.
- Sensitive configuration values must never be exposed to clients.

---

# BR-009 Documentation

No feature may be implemented unless:
1. Requirement exists.
2. Feature specification exists.
3. API contract exists.
4. Architecture is documented.

---

# BR-010 Claude Code Workflow

Before coding:
1. Read docs/index.md
2. Read context/current-state.md
3. Read context/next-task.md

After coding:
1. Update documentation
2. Update API contracts
3. Update Mermaid diagrams
4. Update changelog
5. Update all required context files

---

# Traceability

Each Business Rule shall reference:
- Feature IDs (FR)
- User Stories (US)
- API Contracts
- Database entities
- Test cases

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial business rules |
