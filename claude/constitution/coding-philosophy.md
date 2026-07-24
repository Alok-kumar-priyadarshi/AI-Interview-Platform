# Coding Philosophy

**Document ID:** CLAUDE-CON-004  
**Version:** 1.0.0  
**Status:** Active  
**Priority:** High  
**Last Updated:** 2026-07-23

---

# Purpose

This document defines the coding philosophy for the AI Career Interview Platform.

It is intended to guide every implementation decision throughout the project's
lifecycle. While the Project Constitution defines *what* must be done, this
document defines *how code should be written*.

---

# Core Philosophy

The project prioritizes:

- Readability over cleverness.
- Maintainability over shortcuts.
- Simplicity over unnecessary complexity.
- Consistency over personal preference.
- Explicitness over implicit behavior.

Code should be written for the next developer who will maintain it.

---

# Guiding Principles

## 1. Simplicity First

Prefer the simplest implementation that satisfies the documented requirements.

Avoid introducing additional abstraction until it provides measurable value.

---

## 2. Readability

Code should explain itself.

Prefer:

- descriptive names
- small functions
- small classes
- meaningful interfaces

Avoid:

- deeply nested logic
- unnecessary one-line expressions
- hidden side effects

---

## 3. Modular Design

Every module should have a single responsibility.

Examples:

Authentication

↓

Resume Processing

↓

Interview Engine

↓

Evaluation Engine

↓

Reporting

Each module should evolve independently.

---

## 4. Feature First

Organize code by feature instead of technology whenever practical.

Example:

backend/

authentication/

resume/

interview/

evaluation/

analytics/

instead of

controllers/

services/

repositories/

---

## 5. Composition Over Inheritance

Prefer composing small reusable objects.

Avoid deep inheritance hierarchies.

---

## 6. Explicit Dependencies

Dependencies should always be visible.

Avoid hidden global state.

Prefer constructor injection or dependency injection.

---

## 7. Fail Fast

Invalid input should fail immediately.

Do not continue execution using invalid assumptions.

Provide useful error messages.

---

## 8. Defensive Programming

Validate:

- API requests
- Uploaded files
- AI responses
- Database inputs
- Configuration values

Never trust external input.

---

## 9. Documentation Driven Development

Implementation begins only after:

- Requirement exists
- User Story exists
- Architecture exists
- API exists

Documentation drives implementation.

---

## 10. Consistency

Naming conventions should remain identical across:

- APIs
- Database
- Backend
- Frontend
- AI
- Tests

Consistency is more important than personal preference.

---

# Code Review Checklist

Before merging code verify:

- Single Responsibility maintained
- No duplicated logic
- No dead code
- No unnecessary abstraction
- Proper validation
- Logging added where appropriate
- Error handling implemented
- Tests updated
- Documentation synchronized

---

# Things We Avoid

Avoid:

- God classes
- Massive functions
- Circular dependencies
- Hardcoded secrets
- Hardcoded prompts
- Duplicate business logic
- Business logic inside UI components
- Direct database access from UI
- Vendor-specific AI logic throughout the codebase

---

# Engineering Values

The engineering team values:

1. Correctness
2. Simplicity
3. Maintainability
4. Testability
5. Security
6. Scalability
7. Documentation
8. Developer Experience

Every implementation should improve at least one of these values without reducing another.

---

# Completion Checklist

Before completing any implementation:

- [ ] Code follows SOLID principles
- [ ] Code follows this philosophy
- [ ] Documentation updated
- [ ] Tests updated
- [ ] RTM updated
- [ ] Context updated
- [ ] Changelog updated

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial coding philosophy |