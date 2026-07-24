# Backend Architecture

**Document ID:** ARC-005

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document defines the architecture of the FastAPI backend for the
AI Career Interview Platform.

It specifies project organization, request lifecycle, dependency injection,
service architecture, persistence, validation, middleware, security,
and operational guidelines.

---

# Objectives

The backend architecture should be:

- Modular
- Testable
- Secure
- Scalable
- Maintainable
- Observable
- Layered
- Provider-independent

---

# Architecture Style

The backend follows a **Layered Modular Monolith** architecture.

```
Client

↓

API Layer

↓

Service Layer

↓

Repository Layer

↓

Database
```

External providers are accessed through dedicated adapters.

---

# Technology Stack

| Technology | Purpose |
|------------|---------|
| FastAPI | REST API |
| SQLAlchemy | ORM |
| Alembic | Database Migrations |
| PostgreSQL | Persistence |
| Pydantic | Validation |
| Groq SDK | AI Provider |
| Google OAuth | Authentication |

---

# Project Structure

```text
backend/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── dependencies/
│   ├── middleware/
│   ├── models/
│   ├── schemas/
│   ├── repositories/
│   ├── services/
│   ├── ai/
│   ├── auth/
│   ├── utils/
│   ├── exceptions/
│   ├── database/
│   └── main.py
│
├── tests/
│
├── alembic/
│
└── requirements.txt
```

---

# Layer Responsibilities

## API Layer

Responsibilities:

- Route definitions
- Request parsing
- Response formatting
- Dependency injection
- Authentication enforcement

Must not contain business logic.

---

## Service Layer

Responsibilities:

- Business rules
- Workflow orchestration
- Transaction coordination
- AI orchestration
- Domain validation

This is the core of the application.

---

## Repository Layer

Responsibilities:

- CRUD operations
- Database queries
- Persistence abstraction

Repositories should not contain business rules.

---

## Database Layer

Responsibilities:

- Persistence
- Constraints
- Transactions
- Relationships
- Indexes

---

# Request Lifecycle

```mermaid
flowchart LR

Client

Router

Validation

Authentication

Service

Repository

Database

Response

Client --> Router
Router --> Validation
Validation --> Authentication
Authentication --> Service
Service --> Repository
Repository --> Database
Database --> Response
```

---

# Dependency Injection

FastAPI's dependency injection system should provide:

- Database sessions
- Current user
- Configuration
- AI service
- Repositories

Dependencies must be explicit and type-safe.

---

# API Organization

Routes should be grouped by feature.

Example:

```text
api/

auth.py

users.py

resume.py

interview.py

evaluation.py

history.py
```

Versioned endpoints:

```
/api/v1/auth

/api/v1/users

/api/v1/resumes

/api/v1/interviews

/api/v1/evaluations
```

---

# Service Organization

Example:

```text
services/

auth_service.py

user_service.py

resume_service.py

interview_service.py

evaluation_service.py

history_service.py

analytics_service.py
```

Each service owns one business capability.

---

# Repository Organization

Example:

```text
repositories/

user_repository.py

resume_repository.py

interview_repository.py

evaluation_repository.py
```

Repositories interact only with the database.

---

# Database Session Management

Each request receives its own database session.

```
Incoming Request

↓

Open Session

↓

Execute Operations

↓

Commit or Rollback

↓

Close Session
```

Sessions must never be shared across requests.

---

# Transaction Boundaries

Transactions should wrap complete business operations.

Example:

```
Create Interview

↓

Persist Interview

↓

Persist Questions

↓

Commit
```

Failures should trigger rollback.

---

# Validation Pipeline

Validation occurs in multiple stages.

```
HTTP Request

↓

Pydantic Schema Validation

↓

Business Validation

↓

Database Constraints
```

Every stage should produce meaningful errors.

---

# Exception Handling

Centralized exception handlers should manage:

- Validation errors
- Authentication failures
- Authorization failures
- Database exceptions
- AI provider errors
- Unexpected exceptions

Internal errors should never expose implementation details.

---

# Middleware

Recommended middleware stack:

```text
Request Logging

↓

CORS

↓

Authentication

↓

Rate Limiting (Future)

↓

Exception Handling

↓

Response Processing
```

Each middleware should perform a single concern.

---

# Authentication Flow

```mermaid
flowchart LR

Request

JWT Validation

Current User

Authorization

Endpoint

Request --> JWT Validation
JWT Validation --> Current User
Current User --> Authorization
Authorization --> Endpoint
```

Unauthorized requests return appropriate HTTP status codes.

---

# Authorization

Authorization should be enforced in the service layer.

Examples:

- User owns resource
- Interview belongs to user
- Report belongs to user

Never trust client-provided identifiers.

---

# AI Integration

The backend communicates with AI exclusively through the AI Service.

```
Service

↓

AI Service

↓

Model Adapter

↓

Groq API
```

Controllers must never invoke the provider SDK directly.

---

# File Upload Architecture

Resume uploads follow:

```text
Upload

↓

Validate Type

↓

Validate Size

↓

Temporary Storage

↓

Text Extraction

↓

AI Analysis

↓

Database

↓

Cleanup
```

Invalid files are rejected before processing.

---

# Logging

Structured logging should record:

- Request ID
- User ID (when authenticated)
- Endpoint
- Status Code
- Processing Time
- AI Latency
- Error Context

Sensitive information must never be logged.

---

# Configuration

Configuration is loaded once during startup.

Examples:

- Database URL
- JWT settings
- AI provider settings
- OAuth credentials
- Logging configuration

No module should read environment variables directly.

---

# Performance Considerations

Use:

- Connection pooling
- Efficient queries
- Pagination
- Lazy loading where appropriate
- Proper indexes

Avoid unnecessary database round trips.

---

# Security

The backend enforces:

- JWT validation
- OAuth authentication
- Input validation
- Output serialization
- HTTPS
- SQL injection protection
- File validation

Security checks occur at multiple layers.

---

# Testing Strategy

Backend testing includes:

- Unit tests
- Repository tests
- Service tests
- API integration tests
- Authentication tests
- AI service mocks

Every business service should be independently testable.

---

# Observability

Expose:

- Health endpoint
- Readiness endpoint
- Liveness endpoint
- Request metrics
- Error metrics
- AI latency metrics

These support production monitoring.

---

# Future Extensions

The architecture supports:

- Redis caching
- Background workers
- Message queues
- Multi-provider AI
- Object storage
- WebSockets
- Microservice extraction

These enhancements should require minimal modification to existing services.

---

# Related Documents

- `component-architecture.md`
- `frontend-architecture.md`
- `ai-architecture.md`
- `authentication-architecture.md`
- `deployment-architecture.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial backend architecture specification |