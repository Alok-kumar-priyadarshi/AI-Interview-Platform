# System Overview

**Document ID:** ARC-001

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document provides a high-level overview of the AI Career Interview Platform,
its major subsystems, architectural boundaries, responsibilities, external
integrations, and overall request lifecycle.

It serves as the primary architectural reference before exploring the detailed
component, frontend, backend, AI, and deployment architectures.

---

# System Vision

The AI Career Interview Platform enables candidates to practice realistic
technical and HR interviews that are personalized according to their:

- Resume
- Job role
- Experience level
- Skill set
- Target salary
- Interview difficulty

The platform evaluates responses using AI and produces structured reports,
actionable feedback, and historical progress tracking.

---

# Core Objectives

The system aims to:

- Simulate real interview experiences
- Personalize interviews using resume context
- Evaluate responses consistently
- Provide actionable improvement suggestions
- Track user progress across sessions
- Support voice and text interactions
- Remain modular and extensible

---

# Primary Users

## Candidate

Capabilities:

- Login
- Upload resume
- Configure interview
- Attend interview
- View reports
- Track progress

---

## Administrator (Future)

Capabilities:

- Monitor system
- Manage prompts
- View analytics
- Configure models
- Manage feature flags

---

# Functional Capabilities

The platform supports:

- Google Authentication
- Resume Upload
- Resume Parsing
- Resume Analysis
- AI Interview Generation
- Technical Interviews
- HR Interviews
- Behavioral Interviews
- Voice Interviews
- Text Interviews
- AI Evaluation
- Detailed Feedback
- Historical Analytics

---

# High-Level System Context

```text
                    Candidate
                        │
                        ▼
                React Frontend
                        │
                 HTTPS / REST API
                        │
                        ▼
               FastAPI Backend
                        │
     ┌──────────────┬──────────────┐
     │              │              │
     ▼              ▼              ▼
 Authentication   AI Service   PostgreSQL
     │              │
     ▼              ▼
 Google OAuth     Groq API
                  Whisper
```

---

# Major Subsystems

The application consists of the following major subsystems.

---

## Presentation Layer

Technology:

- React
- TypeScript
- Tailwind CSS

Responsibilities:

- User Interface
- Authentication Flow
- Interview Experience
- Report Visualization
- Progress Dashboard

---

## API Layer

Technology:

FastAPI

Responsibilities:

- Request validation
- Authentication
- Authorization
- Routing
- Response formatting

---

## Business Layer

Responsibilities:

- Resume management
- Interview orchestration
- Evaluation
- User management
- Report generation

This layer contains the application's business rules.

---

## AI Layer

Responsibilities:

- Resume analysis
- Interview generation
- Follow-up questions
- Candidate evaluation
- Feedback generation
- Structured output validation

The AI layer communicates only through the AI abstraction service.

---

## Persistence Layer

Technology:

PostgreSQL

Responsibilities:

- Users
- Resumes
- Interviews
- Questions
- Answers
- Evaluations
- Reports
- History

---

## External Services

The system integrates with:

Google OAuth

Purpose:

Authentication

Groq API

Purpose:

Large Language Model

Groq Whisper

Purpose:

Speech-to-Text

Browser Speech API

Purpose:

Text-to-Speech

---

# Architectural Boundaries

The platform follows strict responsibility boundaries.

```
Frontend

↓

REST API

↓

Business Services

↓

Repositories

↓

Database
```

AI interactions are isolated behind the AI Service.

No component bypasses these layers.

---

# Request Lifecycle

A typical request follows:

```
User Action

↓

Frontend Validation

↓

API Request

↓

Authentication

↓

Business Service

↓

Repository

↓

Database

↓

Business Logic

↓

API Response

↓

Frontend Update
```

If AI processing is required:

```
Business Service

↓

AI Service

↓

Prompt Builder

↓

Groq API

↓

Structured Response

↓

Validation

↓

Business Logic
```

---

# Resume Processing Flow

```
Upload Resume

↓

File Validation

↓

Text Extraction

↓

Structured Resume

↓

AI Resume Analysis

↓

Candidate Profile

↓

Database Storage
```

The parsed profile becomes the foundation for personalized interviews.

---

# Interview Flow

```
Select Interview

↓

Configure Session

↓

Generate Questions

↓

Present Questions

↓

Capture Answers

↓

AI Evaluation

↓

Store Results

↓

Generate Report
```

---

# Evaluation Flow

```
Candidate Answer

↓

Interview Context

↓

Evaluation Prompt

↓

Groq API

↓

Structured JSON

↓

Validation

↓

Score Calculation

↓

Feedback Report
```

---

# Cross-Cutting Concerns

The following concerns apply across all subsystems:

- Authentication
- Authorization
- Validation
- Logging
- Monitoring
- Error Handling
- Configuration
- Documentation

These concerns are implemented consistently across the application.

---

# Security Overview

Security measures include:

- Google OAuth
- JWT Authentication
- HTTPS
- Input Validation
- Secure Cookies
- Environment-Based Secrets
- Database Constraints

Security is addressed at every architectural layer.

---

# Scalability Strategy

Version 1 focuses on vertical scaling.

Future enhancements may include:

- Redis
- Background Workers
- Multi-LLM Support
- Object Storage
- Read Replicas
- Horizontal Scaling

The architecture is intentionally modular to support these additions.

---

# Observability

The system records:

- API requests
- AI latency
- Authentication events
- Errors
- Performance metrics
- Health checks

These metrics support troubleshooting and future optimization.

---

# Failure Handling

The system should degrade gracefully.

Examples:

- AI provider unavailable
- Database timeout
- Invalid uploads
- Authentication failures

Failures should be isolated whenever possible and should not cascade across the system.

---

# Architectural Principles

The platform follows:

- Layered Architecture
- Separation of Concerns
- Dependency Inversion
- Interface-Driven Design
- Documentation-First Development
- Explicit Module Boundaries
- Stateless APIs

---

# Assumptions

Version 1 assumes:

- Single backend service
- Single PostgreSQL database
- Single AI provider
- Single authentication provider
- Managed hosting
- Moderate user traffic

These assumptions may change in future versions.

---

# Out of Scope

Version 1 intentionally excludes:

- Microservices
- Kubernetes
- Distributed caching
- Event streaming
- Offline mode
- Multi-tenant organizations
- Real-time collaborative interviews

---

# Related Documents

- `README.md`
- `high-level-architecture.md`
- `component-architecture.md`
- `frontend-architecture.md`
- `backend-architecture.md`
- `ai-architecture.md`
- `deployment-architecture.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial system overview |