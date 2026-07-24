# Backend Technology Stack

**Document ID:** TS-003

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the backend technology stack, architecture principles,
coding standards, and development practices for the AI Career Interview
Platform.

The backend is responsible for:

- Business logic
- Authentication
- AI orchestration
- Resume processing
- Interview management
- Evaluation
- Data persistence
- API communication

Every backend implementation must comply with this document.

---

# Backend Goals

The backend must be:

- Fast
- Secure
- Modular
- Testable
- Scalable
- Maintainable
- Observable
- Documentation-driven

---

# Core Technology Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.13+ |
| Framework | FastAPI |
| ASGI Server | Uvicorn |
| Validation | Pydantic v2 |
| ORM | SQLAlchemy 2.x |
| Database Migration | Alembic |
| Authentication | Google OAuth 2.0 |
| Authorization | JWT |
| Password Hashing | Not Required (Google OAuth Only) |
| AI Provider | Groq API |
| Environment | python-dotenv |
| Logging | Python Logging |
| API Documentation | OpenAPI / Swagger |
| Testing | Pytest |
| Dependency Management | pip |

---

# Why FastAPI?

FastAPI was selected because it provides:

- Excellent performance
- Native async support
- Automatic OpenAPI generation
- Strong typing
- Pydantic integration
- Excellent documentation
- Modern Python ecosystem

---

# High-Level Backend Responsibilities

The backend owns:

- Authentication
- User management
- Resume processing
- Interview generation
- AI orchestration
- Evaluation
- Reports
- History
- Database
- External integrations

The frontend should never contain business logic.

---

# Backend Architecture Style

The project follows a layered architecture.

```
API Layer
      ↓
Service Layer
      ↓
Business Logic
      ↓
Repository Layer
      ↓
Database
```

Each layer has a single responsibility.

---

# Project Structure

```
backend/

app/

api/

core/

config/

models/

schemas/

services/

repositories/

dependencies/

middleware/

auth/

ai/

resume/

interview/

evaluation/

history/

utils/

exceptions/

database/

tests/
```

Each directory should remain focused and cohesive.

---

# API Layer

Responsibilities:

- Receive HTTP requests
- Validate input
- Authenticate user
- Call services
- Return responses

The API layer must not contain business logic.

---

# Service Layer

The service layer contains business workflows.

Examples:

- Create interview
- Analyze resume
- Evaluate responses
- Generate reports

Business rules belong here.

---

# Repository Layer

Responsibilities:

- Database communication
- CRUD operations
- Query optimization

Repositories should not contain business logic.

---

# Database Layer

Managed using:

- SQLAlchemy
- Alembic

Models represent database entities.

Repositories interact with models.

Services never directly manipulate SQL.

---

# Configuration Management

Configuration is loaded from:

```
.env
```

Never hardcode:

- API Keys
- Secrets
- Database URLs
- OAuth credentials

Configuration should be centralized inside:

```
core/config.py
```

---

# Dependency Injection

FastAPI dependency injection should be used for:

- Database sessions
- Authentication
- Current user
- AI clients
- Configuration

Avoid global state.

---

# Authentication

Authentication provider:

Google OAuth

Authorization:

JWT

Protected endpoints must validate:

- Token
- User
- Permissions

---

# Authorization Strategy

Version 1 roles:

- User
- Admin (future)

Future roles:

- Recruiter
- Organization
- Premium User

Authorization should be extensible.

---

# Validation

All request and response models must use Pydantic.

Never trust client input.

Validate:

- Request body
- Query parameters
- Path parameters
- Uploaded files
- AI responses

---

# Error Handling

Use centralized exception handling.

Errors should return:

```
{
  "success": false,
  "message": "...",
  "error_code": "...",
  "details": {}
}
```

Avoid exposing stack traces.

---

# Logging

Log:

- Startup
- Shutdown
- Authentication
- API requests
- AI requests
- Errors
- Warnings

Never log:

- API keys
- JWT tokens
- Sensitive user data

---

# AI Integration

The backend owns all AI communication.

Responsibilities:

- Prompt construction
- Context assembly
- LLM invocation
- Response validation
- Retry logic
- Usage tracking

The frontend never communicates directly with the LLM.

---

# File Processing

Supported uploads:

- PDF
- DOCX
- TXT

Future:

- Images
- Audio
- Video

Validation:

- MIME type
- Extension
- Size
- Malware scanning (future)

---

# API Design Principles

The API should be:

- RESTful
- Predictable
- Versioned
- Stateless
- JSON-based

Base URL:

```
/api/v1/
```

---

# Naming Conventions

Endpoints:

```
/interviews
/interviews/{id}
/resume/upload
```

Services:

```
InterviewService
```

Repositories:

```
InterviewRepository
```

Schemas:

```
InterviewCreate
InterviewResponse
```

Models:

```
Interview
```

---

# Async Programming

Use async for:

- API routes
- AI calls
- Database operations where appropriate
- External services

Avoid unnecessary blocking operations.

---

# Security Principles

Implement:

- HTTPS
- JWT validation
- Input validation
- Rate limiting (future)
- CORS
- Secure headers
- Environment variables

Never expose internal implementation details.

---

# Testing Strategy

Testing levels:

- Unit Tests
- Integration Tests
- API Tests
- AI Evaluation Tests

Target:

High coverage for business logic.

---

# Performance Guidelines

Optimize:

- Database queries
- AI requests
- File parsing
- Response size
- Connection management

Avoid premature optimization.

Measure before optimizing.

---

# Future Enhancements

Potential additions:

- Redis
- Celery
- Background workers
- WebSockets
- Event-driven architecture
- Multi-LLM routing
- Caching
- Queue management

These are intentionally excluded from Version 1.

---

# Related Documents

- `technology-overview.md`
- `database-stack.md`
- `ai-stack.md`
- `authentication.md`
- `backend architecture` (future)
- `API contracts` (future)

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial backend technology stack |