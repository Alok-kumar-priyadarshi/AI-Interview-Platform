# Architecture Decision Summary

**Document ID:** ARC-014

**Version:** 1.0.0

**Status:** Approved

**Priority:** Critical

**Last Updated:** 2026-07-23

---

# Purpose

This document summarizes the major architectural decisions made for the
AI Career Interview Platform.

It provides a single reference describing the rationale behind each decision,
the alternatives considered, the associated trade-offs, and future review
considerations.

Detailed decision records should be maintained separately in the ADR
(Architecture Decision Record) directory.

---

# Objectives

This document exists to:

- Capture architectural intent
- Preserve design rationale
- Improve onboarding
- Reduce repeated discussions
- Guide future decisions
- Support long-term maintainability

---

# Decision Classification

| Status | Meaning |
|----------|---------|
| Accepted | Active architectural decision |
| Planned | Approved for future implementation |
| Deferred | Postponed until later versions |
| Rejected | Evaluated but intentionally not adopted |

---

# ADR Index

| Decision ID | Status |
|-------------|--------|
| ADR-001 | Accepted |
| ADR-002 | Accepted |
| ADR-003 | Accepted |
| ADR-004 | Accepted |
| ADR-005 | Accepted |
| ADR-006 | Accepted |
| ADR-007 | Accepted |
| ADR-008 | Accepted |
| ADR-009 | Accepted |
| ADR-010 | Accepted |

Future ADRs should be added to this index.

---

# ADR-001

## Decision

Use a Modular Monolith architecture for Version 1.

## Status

Accepted

## Rationale

The expected scale does not justify microservices.

A modular monolith provides:

- Lower operational complexity
- Easier debugging
- Faster development
- Clear module boundaries

## Alternatives Considered

- Microservices
- Serverless architecture

## Trade-offs

Advantages:

- Simpler deployment
- Lower infrastructure cost

Disadvantages:

- Shared deployment lifecycle
- Future module extraction required

---

# ADR-002

## Decision

Use FastAPI as the backend framework.

## Status

Accepted

## Rationale

FastAPI provides:

- High performance
- Strong typing
- Automatic OpenAPI generation
- Excellent async support
- Pydantic integration

## Alternatives

- Flask
- Django
- Express.js

---

# ADR-003

## Decision

Use PostgreSQL as the primary database.

## Status

Accepted

## Rationale

Requirements include:

- ACID transactions
- Relational integrity
- Mature ecosystem
- JSON support
- Strong indexing

## Alternatives

- MongoDB
- MySQL
- SQLite

---

# ADR-004

## Decision

Use React with Vite for the frontend.

## Status

Accepted

## Rationale

Provides:

- Excellent developer experience
- Fast builds
- Large ecosystem
- TypeScript support

## Alternatives

- Next.js
- Angular
- Vue

---

# ADR-005

## Decision

Use Google OAuth as the only authentication provider in Version 1.

## Status

Accepted

## Rationale

Benefits:

- Reduced implementation complexity
- Verified identities
- Familiar user experience
- No password management

## Deferred

Support for additional identity providers.

---

# ADR-006

## Decision

Abstract AI providers behind a Model Adapter.

## Status

Accepted

## Rationale

Business logic should remain independent of:

- Groq
- OpenAI
- Claude
- Gemini

Provider changes should not affect domain logic.

---

# ADR-007

## Decision

Require structured JSON output from all AI interactions.

## Status

Accepted

## Rationale

Benefits:

- Deterministic parsing
- Schema validation
- Predictable behavior
- Reduced prompt ambiguity

Natural-language-only responses are not accepted for business workflows.

---

# ADR-008

## Decision

Use stateless JWT authentication.

## Status

Accepted

## Rationale

Advantages:

- Horizontal scalability
- Simple deployment
- No server-side session storage

Refresh tokens are deferred to a future version.

---

# ADR-009

## Decision

Adopt a documentation-first workflow.

## Status

Accepted

## Rationale

Every major feature should have:

- Requirements
- Architecture
- API contract
- Database design
- AI specification
- Testing strategy

Implementation follows approved documentation.

---

# ADR-010

## Decision

Design the system for incremental scalability.

## Status

Accepted

## Rationale

Version 1 targets simplicity while preserving a clear path toward:

- Multiple backend instances
- Distributed workers
- Redis
- Object storage
- Multi-provider AI
- Read replicas

Avoid premature optimization while eliminating architectural dead ends.

---

# Deferred Decisions

The following decisions are intentionally postponed:

| Decision | Target Version |
|----------|----------------|
| Redis Cache | V2 |
| Background Workers | V2 |
| Object Storage | V2 |
| Refresh Tokens | V2 |
| AI Provider Failover | V2 |
| Multi-factor Authentication | V2 |
| Read Replicas | V3 |
| Kubernetes | V3 |
| Event-Driven Architecture | V3 |

---

# Rejected Alternatives

## Microservices (V1)

Reason:

Operational complexity outweighs current benefits.

---

## NoSQL as Primary Database

Reason:

Current data model is relational and transactional.

---

## Password-Based Authentication

Reason:

Google OAuth satisfies Version 1 requirements while reducing security overhead.

---

## Direct LLM Calls from Business Logic

Reason:

Violates separation of concerns and creates vendor lock-in.

---

# Decision Review Process

Architectural decisions should be reviewed when:

- Business requirements change
- Significant scalability issues arise
- Security risks emerge
- Infrastructure constraints change
- New technologies offer measurable advantages

Reviews should result in:

- No change
- Updated ADR
- New ADR
- Deprecation

---

# Governance Rules

Major architectural changes require:

- Updated documentation
- Impact analysis
- Trade-off evaluation
- ADR creation
- Team approval

No implementation should contradict accepted architectural decisions without an approved ADR.

---

# Traceability Matrix

| Decision | Related Documents |
|----------|-------------------|
| Modular Monolith | ARC-002, ARC-003 |
| FastAPI | ARC-005, TS-003 |
| PostgreSQL | TS-004, Database Docs |
| React + Vite | ARC-004, TS-002 |
| Google OAuth | ARC-007, TS-006 |
| AI Adapter | ARC-006 |
| JWT | ARC-007 |
| Documentation First | Architecture Principles |
| Scalability | ARC-011 |
| Fault Tolerance | ARC-012 |

---

# Related Documents

- `README.md`
- `high-level-architecture.md`
- `architecture-principles.md`
- `../13-adr/`
- `../02-tech-stack/`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial architecture decision summary |