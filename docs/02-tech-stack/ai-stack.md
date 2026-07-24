# AI Technology Stack

**Document ID:** TS-005

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the Artificial Intelligence technology stack,
architecture principles, prompt engineering strategy, model integration,
evaluation pipeline, and operational guidelines for the AI Career Interview
Platform.

The AI subsystem is the core differentiator of the platform and is responsible
for generating realistic interviews, evaluating responses, and producing
personalized feedback.

---

# AI Objectives

The AI system must be:

- Accurate
- Reliable
- Consistent
- Context-aware
- Explainable
- Extensible
- Observable
- Secure

---

# Core AI Stack

| Category | Technology |
|----------|------------|
| LLM Provider | Groq API |
| Speech-to-Text | Groq Whisper |
| Text-to-Speech | Browser SpeechSynthesis API |
| Prompt Format | Structured Prompt Templates |
| Output Format | JSON |
| Validation | Pydantic |
| AI Gateway | Internal Service Layer |

---

# Why Groq?

Groq was selected because it provides:

- Extremely low latency
- Competitive model performance
- Simple API
- Affordable pricing
- Good developer experience
- Production-ready infrastructure

The application should never depend directly on Groq-specific APIs outside the
AI service layer.

---

# AI Responsibilities

The AI system is responsible for:

- Resume analysis
- Interview generation
- Follow-up question generation
- Candidate evaluation
- Communication assessment
- Technical assessment
- HR assessment
- Personalized feedback
- Learning recommendations (future)

---

# AI System Architecture

The application should communicate with AI through an abstraction layer.

```
Frontend

↓

Backend API

↓

AI Service Layer

↓

Prompt Builder

↓

LLM Provider

↓

Response Validator

↓

Business Logic
```

The frontend must never communicate directly with an LLM.

---

# AI Service Layer

Responsibilities:

- Prompt construction
- Context assembly
- Model invocation
- Retry handling
- Output validation
- Error recovery
- Usage logging
- Token monitoring

This layer isolates the rest of the application from provider-specific APIs.

---

# Prompt Engineering Strategy

Prompt construction should follow a layered approach.

```
System Prompt

↓

Business Rules

↓

Interview Context

↓

Resume Context

↓

Conversation History

↓

Current User Input
```

Each layer has a clearly defined responsibility.

---

# Prompt Categories

Version 1 defines the following prompt categories:

- Resume Analysis
- Interview Generation
- Follow-up Questions
- Technical Evaluation
- HR Evaluation
- Behavioral Evaluation
- Feedback Report
- Final Summary

Each category should have its own version-controlled prompt template.

---

# Prompt Versioning

Prompts must be versioned independently from application code.

Example:

```
InterviewPrompt_v1

InterviewPrompt_v2

EvaluationPrompt_v1
```

Prompt changes should be tracked similarly to API or schema changes.

---

# Context Management

The AI receives structured context from multiple sources.

Examples:

- User profile
- Resume
- Selected role
- Experience level
- Difficulty level
- Interview history
- Previous questions
- Previous answers

Only relevant context should be included.

Avoid unnecessarily large prompts.

---

# Resume Analysis Pipeline

```
Resume Upload

↓

Resume Extraction

↓

Structured Resume Data

↓

AI Resume Analysis

↓

Candidate Profile

↓

Interview Generator
```

The AI should never analyze raw PDFs directly.

Resume data must first be structured.

---

# Interview Generation Pipeline

```
Candidate Profile

↓

Interview Configuration

↓

Prompt Builder

↓

LLM

↓

Question Validation

↓

Interview Session
```

The generated interview should align with:

- Role
- Experience
- Difficulty
- Skills
- Resume

---

# Evaluation Pipeline

```
Candidate Answer

↓

Interview Context

↓

Evaluation Prompt

↓

LLM

↓

Structured JSON Output

↓

Validation

↓

Evaluation Report
```

Every evaluation response must be validated before storage.

---

# Structured Output

The LLM should always return structured JSON.

Example:

```json
{
  "score": 82,
  "communication": 80,
  "technical": 85,
  "confidence": 78,
  "feedback": "...",
  "strengths": [],
  "improvements": []
}
```

Never rely on free-form text parsing when a structured schema can be enforced.

---

# Response Validation

Every AI response should be validated using Pydantic models.

Validation includes:

- Required fields
- Data types
- Value ranges
- Enum validation
- JSON schema compliance

Invalid responses should never be stored directly.

---

# Token Management

The AI service should monitor:

- Prompt tokens
- Completion tokens
- Total tokens
- Average tokens per interview
- Estimated cost

Future dashboards may visualize this information.

---

# Retry Strategy

Retry only for transient failures.

Examples:

- Network timeout
- Temporary provider error
- Rate limiting

Do not retry:

- Invalid prompts
- Validation failures
- Authentication failures

Use exponential backoff.

---

# Rate Limiting

The AI layer should respect provider limits.

Strategies:

- Queue requests
- Retry after delay
- Graceful degradation

Avoid overwhelming external providers.

---

# Safety Principles

Protect against:

- Prompt injection
- Malicious input
- Prompt leakage
- Data leakage
- Unsafe responses

User input should never override system instructions.

---

# Hallucination Mitigation

Strategies include:

- Structured prompts
- Explicit instructions
- Response validation
- Resume grounding
- Context grounding

The AI should only evaluate information available within the interview context.

---

# AI Observability

Track:

- Request latency
- Success rate
- Failure rate
- Retry count
- Validation failures
- Average response time
- Token usage

These metrics support monitoring and optimization.

---

# Error Handling

Possible failures:

- Network timeout
- Provider unavailable
- Invalid JSON
- Token limit exceeded
- Authentication failure

The application should return user-friendly error messages and log technical
details internally.

---

# Future Enhancements

Potential future capabilities:

- Multi-LLM routing
- Automatic model selection
- AI caching
- Fine-tuned prompts
- Prompt A/B testing
- Voice emotion analysis
- Personalized interviewer personas
- Adaptive interview difficulty
- AI quality scoring

These are intentionally out of scope for Version 1.

---

# Related Documents

- `technology-overview.md`
- `backend-stack.md`
- `authentication.md`
- `06-ai-system/` (future)
- `03-architecture/06-ai-architecture.md` (future)

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial AI technology stack |