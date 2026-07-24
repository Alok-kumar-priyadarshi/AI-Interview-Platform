# Unit Testing Architecture

**Document ID:** TEST-001

**Version:** 1.0.0

**Status:** Approved

**Priority:** High

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the unit testing architecture for the AI Career Interview Platform.

Unit tests verify that individual functions, classes, and modules behave correctly in complete isolation from external dependencies.

The goals are:

- Verify business logic
- Detect regressions early
- Enable safe refactoring
- Maintain high code quality
- Provide fast developer feedback

---

# Scope

Unit testing covers:

- Utility functions
- Validation logic
- Business services
- Domain models
- AI prompt builders
- Resume parsing utilities
- Scoring algorithms
- Custom hooks
- React components (isolated)
- Helper libraries

Unit tests must not depend on:

- Databases
- Network APIs
- External AI services
- OAuth providers
- File storage

These belong to integration tests.

---

# Testing Frameworks

## Backend

Framework

```
pytest
```

Supporting Libraries

- pytest
- pytest-mock
- pytest-cov
- faker
- freezegun (time mocking)

---

## Frontend

Framework

```
Vitest
```

Supporting Libraries

- Vitest
- React Testing Library
- @testing-library/user-event
- jsdom

---

# Directory Structure

Backend

```text
backend/

app/

tests/

unit/

test_services.py

test_utils.py

test_validators.py

test_scoring.py
```

Frontend

```text
frontend/

src/

tests/

unit/

Button.test.tsx

InterviewCard.test.tsx

ResumeUploader.test.tsx
```

---

# Test Naming

File names

```
test_resume_parser.py

test_scoring.py

test_prompt_builder.py
```

Frontend

```
Button.test.tsx

Navbar.test.tsx
```

---

# Test Function Naming

Pattern

```
test_<expected_behavior>()
```

Examples

```python
def test_resume_parser_extracts_email():
    ...

def test_invalid_file_type_is_rejected():
    ...
```

---

# Test Structure

Every test follows the Arrange–Act–Assert pattern.

```text
Arrange

↓

Act

↓

Assert
```

Example

```python
def test_total_score():
    # Arrange
    score = ScoreCalculator()

    # Act
    result = score.calculate(...)

    # Assert
    assert result == 85
```

---

# Mocking Strategy

External dependencies must be mocked.

Examples

- Database
- Groq API
- Google OAuth
- File storage
- Email service
- Clock
- UUID generation

Business logic must never depend on live services.

---

# Fixtures

Reusable fixtures should provide:

- Test user
- Test resume
- Interview configuration
- Mock JWT
- AI response
- Candidate profile

Fixtures belong in:

```
conftest.py
```

---

# Assertions

Assertions must verify:

- Return values
- Exceptions
- Validation
- Side effects
- State changes

Avoid multiple unrelated assertions in one test.

---

# Edge Cases

Every module should test:

- Empty input
- Null values
- Invalid types
- Maximum limits
- Minimum limits
- Unicode input
- Large payloads
- Duplicate values

---

# Error Testing

Expected exceptions must be verified.

Example

```python
with pytest.raises(ValueError):
    validate_resume(None)
```

---

# Time-dependent Tests

Use mocked time.

Never depend on:

- Current clock
- Local timezone
- System date

---

# Randomness

Random values must be mocked.

Examples

- UUIDs
- Tokens
- Session IDs

Tests must remain deterministic.

---

# AI Component Testing

Mock:

- Groq API responses
- Prompt outputs
- Token counts

Verify:

- Prompt construction
- Context assembly
- Output parsing
- Error handling

Never invoke real AI services during unit tests.

---

# React Component Testing

Verify:

- Rendering
- Props
- User interaction
- Accessibility roles
- State changes
- Conditional rendering

Do not test implementation details.

---

# Code Coverage Goals

| Module | Target |
|----------|--------:|
| Utilities | ≥95% |
| Validation | ≥95% |
| Services | ≥90% |
| Prompt Builder | ≥95% |
| Business Logic | ≥95% |

Overall backend target

```
90%+
```

---

# Best Practices

- One behavior per test.
- Keep tests independent.
- Avoid shared mutable state.
- Prefer fixtures over duplication.
- Mock external dependencies.
- Keep tests fast.
- Write descriptive test names.

---

# Anti-Patterns

Avoid:

- Network calls
- Database access
- Sleeping
- Random values
- Shared global state
- Order-dependent tests
- Testing private implementation details

---

# CI Requirements

Every pull request must execute:

- Unit tests
- Coverage report
- Linting
- Static analysis

Pull requests failing unit tests must not be merged.

---

# Business Rules

- Every business rule requires unit tests.
- Every bug fix requires a regression test.
- External services are mocked.
- Tests are deterministic.
- Unit tests complete in minutes, not hours.

---

# Related Documents

- `README.md`
- `integration-testing.md`
- `api-testing.md`
- `quality-gates.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial unit testing architecture specification |