
# User Journey

**Document ID:** DOC-PRJ-005
**Version:** 1.0.0
**Status:** Draft
**Owner:** Project Architect
**Last Updated:** 2026-07-23

---

# Purpose

Describe the complete end-to-end experience of a user interacting with the AI Career Interview Platform. This document serves as the foundation for UI design, backend workflow, API contracts, database design, and Mermaid sequence diagrams.

---

# Primary User Journey

```
Landing Page
    │
    ▼
Google Sign In
    │
    ▼
Dashboard
    │
    ▼
Upload Resume
    │
    ▼
Resume Analysis
    │
    ▼
Configure Interview
    ├── Difficulty
    ├── Target Package
    ├── Question Count
    ├── Duration
    ├── Voice (Male/Female)
    └── Interview Mode (Voice/Text)
    │
    ▼
Start Interview
    │
    ▼
AI Conducts Interview
    │
    ▼
User Answers
    │
    ▼
AI Evaluates Responses
    │
    ▼
Generate Detailed Report
    │
    ▼
Save Session
    │
    ▼
Dashboard & Progress Tracking
```

---

# Screen Flow

## 1. Landing Page
- Product introduction
- Sign in with Google

Related Features:
- FR-001

---

## 2. Dashboard

User can:

- View interview history
- Upload a resume
- Continue previous sessions
- Start a new interview
- View analytics

Related Features:
- FR-050
- FR-051
- FR-052

---

## 3. Resume Upload

User uploads PDF resume.

System:

- Validates file
- Extracts text
- Parses resume
- Generates structured profile

Related Features:
- FR-010
- FR-011
- FR-012

---

## 4. Interview Configuration

User selects:

- Difficulty
- Package
- Question Count
- Duration
- Voice
- Interview Mode

Related Features:
- FR-020
- FR-021
- FR-022
- FR-023
- FR-024
- FR-025

---

## 5. Interview Session

AI:

- Greets user
- Reads resume context
- Generates questions
- Asks follow-up questions
- Maintains conversation

User:

- Answers using voice or text

Related Features:
- FR-030
- FR-031
- FR-032
- FR-033
- FR-034

---

## 6. Evaluation

System generates:

- Technical score
- Communication score
- Confidence score
- Strengths
- Weaknesses
- Improvement roadmap

Related Features:
- FR-040
- FR-041
- FR-042
- FR-043
- FR-044
- FR-045
- FR-046

---

## 7. History & Analytics

Users can:

- Compare interviews
- Review reports
- Track improvement
- Download reports (future)

Related Features:
- FR-050
- FR-051
- FR-052
- FR-053

---

# Exceptional Flows

- Resume upload failure
- Network interruption
- Groq API timeout
- User leaves interview
- Resume parsing failure
- Authentication failure

Each exceptional flow will have dedicated API handling and Mermaid sequence diagrams.

---

# UX Principles

- Minimal setup before interview
- Maximum focus on interview
- Clear progress indicators
- Immediate feedback
- Resume previous work where possible

---

# Future Journey Extensions

- Coding interview
- Company-specific interview
- Recruiter review
- Peer mock interview

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial user journey |
