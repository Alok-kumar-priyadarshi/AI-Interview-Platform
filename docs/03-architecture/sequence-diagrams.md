# Sequence Diagrams

**Document ID:** ARC-009

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the runtime interaction sequences for the AI Career
Interview Platform.

Each sequence diagram illustrates how components collaborate to complete
a business workflow.

These diagrams complement the architectural and data flow documentation.

---

# Sequence Diagram Standards

Participants are ordered left-to-right as:

```
User

↓

Frontend

↓

Backend API

↓

Business Service

↓

AI Service (if applicable)

↓

Repository

↓

Database

↓

External Services
```

---

# 1. User Login

```mermaid
sequenceDiagram

participant U as User
participant F as Frontend
participant G as Google OAuth
participant A as Auth API
participant S as Auth Service
participant DB as PostgreSQL

U->>F: Click "Sign in with Google"

F->>G: Start OAuth

G-->>F: Authorization Code

F->>A: Exchange Code

A->>S: Validate Login

S->>G: Verify Authorization Code

G-->>S: User Information

S->>DB: Create / Update User

DB-->>S: User

S-->>A: JWT

A-->>F: Authentication Response

F-->>U: Dashboard
```

---

# 2. Resume Upload

```mermaid
sequenceDiagram

participant U as User
participant F as Frontend
participant API
participant ResumeService
participant AI
participant Repo
participant DB

U->>F: Upload Resume

F->>API: POST /resume

API->>ResumeService: Validate

ResumeService->>Repo: Store File Metadata

Repo->>DB: Save Resume

ResumeService->>AI: Analyze Resume

AI-->>ResumeService: Candidate Profile

ResumeService->>Repo: Save Profile

Repo->>DB: Persist Profile

ResumeService-->>API: Success

API-->>F: Resume Processed
```

---

# 3. Interview Creation

```mermaid
sequenceDiagram

participant U
participant F
participant API
participant InterviewService
participant AI
participant Repo
participant DB

U->>F: Configure Interview

F->>API: Create Interview

API->>InterviewService: Validate Configuration

InterviewService->>AI: Generate Questions

AI-->>InterviewService: Questions

InterviewService->>Repo: Save Interview

Repo->>DB: Persist

InterviewService-->>API: Interview ID

API-->>F: Ready
```

---

# 4. Interview Start

```mermaid
sequenceDiagram

participant U
participant F
participant API
participant InterviewService
participant Repo
participant DB

U->>F: Start Interview

F->>API: Start Session

API->>InterviewService: Load Session

InterviewService->>Repo: Fetch Questions

Repo->>DB: Read

DB-->>Repo: Questions

Repo-->>InterviewService: Questions

InterviewService-->>API: Session

API-->>F: First Question
```

---

# 5. Submit Answer

```mermaid
sequenceDiagram

participant U
participant F
participant API
participant InterviewService
participant EvaluationService
participant AI
participant Repo
participant DB

U->>F: Submit Answer

F->>API: Answer

API->>InterviewService: Save Answer

InterviewService->>Repo: Persist Answer

Repo->>DB: Store

InterviewService->>EvaluationService: Evaluate

EvaluationService->>AI: Score Answer

AI-->>EvaluationService: Evaluation

EvaluationService->>Repo: Save Evaluation

Repo->>DB: Persist

EvaluationService-->>API: Feedback

API-->>F: Display Feedback
```

---

# 6. Voice Interview

```mermaid
sequenceDiagram

participant U
participant Browser
participant API
participant AI
participant DB

U->>Browser: Record Audio

Browser->>API: Upload Audio

API->>AI: Speech-to-Text

AI-->>API: Transcript

API->>DB: Save Transcript

API-->>Browser: Transcript

Browser-->>U: Display Text
```

---

# 7. Interview Completion

```mermaid
sequenceDiagram

participant U
participant F
participant API
participant InterviewService
participant EvaluationService
participant Repo
participant DB

U->>F: Finish Interview

F->>API: Complete

API->>InterviewService: Close Session

InterviewService->>EvaluationService: Generate Final Evaluation

EvaluationService->>Repo: Save Report

Repo->>DB: Persist

EvaluationService-->>API: Report ID

API-->>F: Interview Complete
```

---

# 8. Report Generation

```mermaid
sequenceDiagram

participant U
participant F
participant API
participant ReportService
participant Repo
participant DB

U->>F: Open Report

F->>API: GET Report

API->>ReportService: Fetch Report

ReportService->>Repo: Load

Repo->>DB: Read

DB-->>Repo: Report

Repo-->>ReportService: Report

ReportService-->>API: Response

API-->>F: Render Report
```

---

# 9. Dashboard Loading

```mermaid
sequenceDiagram

participant U
participant F
participant API
participant AnalyticsService
participant Repo
participant DB

U->>F: Open Dashboard

F->>API: Dashboard Data

API->>AnalyticsService: Generate Statistics

AnalyticsService->>Repo: Load History

Repo->>DB: Read

DB-->>Repo: History

Repo-->>AnalyticsService: Data

AnalyticsService-->>API: Metrics

API-->>F: Dashboard
```

---

# 10. Logout

```mermaid
sequenceDiagram

participant U
participant F

U->>F: Logout

F->>F: Remove JWT

F->>F: Clear Context

F-->>U: Login Page
```

---

# Sequence Design Rules

Every workflow should:

- Validate input before processing.
- Enforce authentication where required.
- Keep business logic inside services.
- Persist state changes before responding.
- Return standardized API responses.

---

# Error Handling

Failures follow this interaction pattern:

```mermaid
sequenceDiagram

participant Client
participant API
participant Service
participant ExceptionHandler

Client->>API: Request

API->>Service: Execute

Service-->>ExceptionHandler: Error

ExceptionHandler-->>API: Standard Error

API-->>Client: Error Response
```

---

# Related Documents

- `system-overview.md`
- `data-flow.md`
- `backend-architecture.md`
- `ai-architecture.md`
- `deployment-architecture.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial sequence diagram specification |