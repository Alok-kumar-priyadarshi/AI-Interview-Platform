# Project Scope

**Document ID:** DOC-PRJ-002
**Version:** 1.0.0
**Status:** Draft
**Owner:** Project Architect
**Last Updated:** 2026-07-23

---

# Purpose

Define exactly what is included in Version 1 (MVP), what is excluded, project constraints, assumptions, and release boundaries. This document prevents scope creep during development.

---

# Scope Statement

The AI Career Interview Platform will provide an end-to-end mock interview experience where users can upload a resume, configure an interview, complete the interview using voice or text, and receive detailed AI-generated feedback with historical progress tracking.

---

# In Scope (Version 1)

## Authentication
- Google OAuth login
- Secure JWT session handling
- User profile

## Resume
- PDF resume upload
- Resume parsing
- Resume summary generation

## Interview
- AI-generated questions
- Voice and text interview modes
- Difficulty Levels:
  - Easy
  - Medium
  - Hard
  - Complex
  - Killer
- Target salary/package selector
- Question count selector
- Interview duration selector
- Male/Female AI voice

## Evaluation
- Technical score
- Communication score
- Confidence score (LLM-estimated)
- Strengths
- Weaknesses
- Improvement roadmap
- Overall interview report

## Dashboard
- Interview history
- Performance trends
- Previous reports
- Resume history

## Administration
- User settings
- Profile management

---

# Out of Scope (Version 1)

- Live interviewer collaboration
- Video interview analysis
- Multiplayer interviews
- Company recruiter portal
- Mobile application
- Coding IDE with code execution
- Payment system
- Team workspaces
- Multi-language support

---

# Non-Functional Scope

- Responsive web application
- Desktop-first UI
- Secure authentication
- Modular backend
- REST APIs
- Clean architecture
- SOLID principles
- Easy deployment
- Low operating cost

---

# Constraints

- Prefer completely free technologies.
- Use Groq API wherever suitable.
- Backend: FastAPI.
- Frontend: React (Vite) + Tailwind CSS.
- PostgreSQL database.
- Documentation-first development.
- No Docker in initial version.
- Minimize infrastructure complexity.

---

# Assumptions

- Users have internet access.
- Groq API remains available.
- Users upload well-formatted resumes.
- Google account is required for login.

---

# Success Criteria

A release is considered complete when users can:

1. Sign in.
2. Upload a resume.
3. Configure interview settings.
4. Complete a voice/text interview.
5. Receive detailed AI feedback.
6. Review interview history.
7. Continue improving through repeated sessions.

---

# Scope Change Policy

Any new feature must:

1. Be proposed in planning.
2. Be approved.
3. Update documentation.
4. Update API contracts (if required).
5. Update architecture.
6. Update Mermaid diagrams.
7. Update context.

No feature is implemented before documentation approval.

---

# Release Plan

## Version 1.0
Core AI Interview Platform

## Version 1.1
Performance improvements
Better reports
UI polish

## Version 2.0
Coding interviews
Company-specific interviews
Advanced analytics

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial project scope |
