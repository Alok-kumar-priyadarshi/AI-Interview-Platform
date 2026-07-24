# Coding Standards

**Document ID:** TS-011

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the official coding standards, naming conventions,
quality requirements, documentation practices, testing expectations,
and review guidelines for the AI Career Interview Platform.

All implementation must follow these standards unless an approved
Architecture Decision Record (ADR) explicitly documents an exception.

---

# Objectives

The codebase should be:

- Readable
- Consistent
- Maintainable
- Testable
- Modular
- Secure
- Predictable

Code is written for humans first and computers second.

---

# General Principles

Follow these principles:

- Prefer clarity over cleverness.
- Keep functions focused.
- Avoid unnecessary abstraction.
- Eliminate duplicated logic.
- Write deterministic code.
- Fail fast on invalid input.
- Optimize only after measurement.

---

# Single Responsibility Principle

Every module, class, and function should have one primary responsibility.

Avoid:

```
InterviewService

↓

Resume Parsing

↓

Authentication

↓

Email Sending

↓

Database Access
```

Instead:

```
InterviewService

↓

Interview Logic Only
```

---

# File Size Guidelines

Recommended limits:

| Type | Recommended Size |
|------|------------------|
| React Component | < 300 lines |
| Python Module | < 500 lines |
| Function | < 50 lines |
| Class | < 300 lines |

Large files should be split by responsibility.

---

# Naming Conventions

## Directories

```
snake_case
```

Example:

```
resume_processing
```

---

## Python Files

```
snake_case.py
```

Example:

```
resume_service.py
```

---

## React Components

```
PascalCase.tsx
```

Example:

```
InterviewCard.tsx
```

---

## Hooks

```
useInterview.ts
```

---

## Interfaces / Types

```
Interview.ts
```

---

## Constants

```
routes.ts
```

---

## Environment Variables

```
UPPER_SNAKE_CASE
```

Example:

```
DATABASE_URL
JWT_SECRET
```

---

# Function Design

Functions should:

- Perform one task.
- Return predictable results.
- Avoid hidden side effects.
- Validate inputs.
- Use descriptive names.

Prefer:

```
calculateInterviewScore()
```

Avoid:

```
doWork()
```

---

# Variable Naming

Good:

```
candidateScore

resumeSummary

interviewQuestions
```

Avoid:

```
x

tmp

value1

abc
```

---

# Comments

Write comments that explain **why**, not **what**.

Good:

```python
# Retry because the AI provider may return transient failures.
```

Avoid:

```python
# Increment i
i += 1
```

Self-explanatory code reduces the need for comments.

---

# Documentation

Public functions, classes, and modules should include documentation.

Python example:

```python
def generate_interview():
    """
    Generates interview questions using the configured AI provider.
    """
```

Complex business logic should reference the relevant design document or ADR where appropriate.

---

# Error Handling

Errors should:

- Be explicit.
- Include meaningful messages.
- Preserve context.
- Never expose sensitive information.

Use custom exception classes for domain-specific failures.

---

# Logging

Log:

- Startup
- Shutdown
- API requests
- Authentication events
- AI requests
- Validation failures
- Unexpected exceptions

Do not log:

- Passwords
- API keys
- OAuth tokens
- JWTs
- Personally sensitive data

---

# API Standards

Endpoints should:

- Use nouns instead of verbs.
- Be versioned.
- Return consistent response formats.
- Use appropriate HTTP status codes.

Example:

```
GET    /api/v1/interviews
POST   /api/v1/interviews
GET    /api/v1/interviews/{id}
DELETE /api/v1/interviews/{id}
```

---

# Database Standards

- Always use Alembic migrations.
- Avoid raw SQL unless necessary.
- Use transactions for related operations.
- Validate data before persistence.
- Do not bypass repositories.

---

# Frontend Standards

Components should:

- Be reusable.
- Receive typed props.
- Avoid business logic.
- Be responsive.
- Follow accessibility guidelines.

Use composition instead of deeply nested inheritance-like structures.

---

# Backend Standards

The backend should follow:

```
API

↓

Service

↓

Repository

↓

Database
```

Business logic belongs only in the service layer.

---

# AI Integration Standards

All AI interactions must:

- Use the AI service layer.
- Validate responses.
- Handle retries.
- Record usage metrics.
- Return structured data.

Never call an AI provider directly from controllers or UI components.

---

# Testing Expectations

Every feature should include:

- Unit tests
- Integration tests (where applicable)
- API tests for exposed endpoints

Critical business logic should have high test coverage.

---

# Security Standards

Always:

- Validate input.
- Sanitize uploaded files.
- Enforce authorization.
- Use HTTPS in production.
- Store secrets in environment variables.

Never trust client-provided data.

---

# Git Commit Convention

Recommended format:

```
feat: add interview evaluation service

fix: resolve resume parsing bug

docs: update authentication flow

refactor: simplify AI service

test: add interview API tests

chore: upgrade dependencies
```

---

# Pull Request Standards

Every Pull Request should:

- Have a clear purpose.
- Reference related issues.
- Pass automated checks.
- Include documentation updates if behavior changes.
- Remain focused on a single concern.

Large, unrelated changes should be split into multiple Pull Requests.

---

# Code Review Checklist

Reviewers should verify:

- Correctness
- Readability
- Security
- Performance
- Test coverage
- Documentation
- Error handling
- Naming consistency
- Architectural compliance

---

# Anti-Patterns

Avoid:

- God classes
- God functions
- Circular dependencies
- Duplicate code
- Premature optimization
- Hidden side effects
- Hardcoded secrets
- Business logic in UI

---

# Quality Gates

Before merging:

- All tests pass.
- Linting passes.
- Formatting passes.
- Documentation updated.
- No critical review comments remain.
- CI pipeline succeeds.

---

# Exceptions

Any deviation from these standards must be documented through an Architecture Decision Record (ADR) and reviewed before implementation.

---

# Related Documents

- `technology-overview.md`
- `development-tools.md`
- `project-structure.md`
- `13-adr/` (future)

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial coding standards specification |