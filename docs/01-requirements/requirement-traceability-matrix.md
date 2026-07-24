# Requirement Traceability Matrix (RTM)

**Document ID:** DOC-REQ-006  
**Version:** 1.0.0  
**Status:** Active  
**Owner:** Project Architect  
**Last Updated:** 2026-07-23

---

# Purpose

The Requirement Traceability Matrix (RTM) provides complete traceability from
business requirements to implementation artifacts.

Every requirement must map to all affected components including user stories,
architecture, APIs, database entities, frontend screens, backend services,
AI modules, test cases, and documentation.

This document is considered the single source of truth for implementation
tracking.

---

# Traceability Legend

| Prefix | Meaning |
|----------|---------|
| FR | Functional Requirement |
| NFR | Non Functional Requirement |
| BR | Business Rule |
| US | User Story |
| API | API Contract |
| DB | Database Entity |
| BE | Backend Service |
| UI | Frontend Screen |
| AI | AI Component |
| MER | Mermaid Diagram |
| ADR | Architecture Decision |
| TST | Test Case |

---

# Functional Requirement Traceability

| Requirement | User Story | API | DB | Backend | Frontend | AI | Mermaid | Test | Status |
|-------------|------------|-----|----|----------|-----------|----|----------|------|--------|
| FR-001 Authentication | US-001 | API-001 | DB-001 | BE-001 | UI-001 | — | MER-001 | TST-001 | Planned |
| FR-002 Resume Upload | US-002 | API-002 | DB-002 | BE-002 | UI-002 | AI-001 | MER-002 | TST-002 | Planned |
| FR-003 Interview Configuration | US-003 | API-003 | DB-003 | BE-003 | UI-003 | — | MER-003 | TST-003 | Planned |
| FR-004 AI Interview Engine | US-004 | API-004 | DB-004 | BE-004 | UI-004 | AI-002 | MER-004 | TST-004 | Planned |
| FR-005 Evaluation Engine | US-005 | API-005 | DB-005 | BE-005 | UI-005 | AI-003 | MER-005 | TST-005 | Planned |
| FR-006 Dashboard | US-006 | API-006 | DB-006 | BE-006 | UI-006 | — | MER-006 | TST-006 | Planned |
| FR-007 Persistence | — | API-007 | DB-007 | BE-007 | — | — | MER-007 | TST-007 | Planned |
| FR-008 Error Handling | — | API-008 | — | BE-008 | UI-007 | AI-004 | MER-008 | TST-008 | Planned |
| FR-009 Reporting | — | API-009 | DB-008 | BE-009 | UI-008 | AI-005 | MER-009 | TST-009 | Planned |

---

# Non Functional Requirement Traceability

| Requirement | Architecture | Deployment | Testing | ADR | Status |
|-------------|-------------|------------|----------|------|--------|
| NFR-001 Performance | ARC-004 | DEP-001 | TST-101 | ADR-001 | Planned |
| NFR-002 Availability | ARC-005 | DEP-002 | TST-102 | ADR-002 | Planned |
| NFR-003 Scalability | ARC-006 | DEP-003 | TST-103 | ADR-003 | Planned |
| NFR-004 Maintainability | ARC-001 | — | TST-104 | ADR-004 | Planned |
| NFR-005 Security | ARC-007 | DEP-004 | TST-105 | ADR-005 | Planned |
| NFR-006 Reliability | ARC-008 | DEP-005 | TST-106 | ADR-006 | Planned |
| NFR-007 Usability | ARC-009 | — | TST-107 | ADR-007 | Planned |
| NFR-008 Cost | ARC-010 | DEP-006 | — | ADR-008 | Planned |
| NFR-009 Deployability | ARC-011 | DEP-007 | TST-108 | ADR-009 | Planned |
| NFR-010 Documentation | DOC-ALL | — | — | ADR-010 | Active |

---

# Business Rule Traceability

| Business Rule | Related Requirements | Backend | API | Test |
|---------------|----------------------|----------|-----|------|
| BR-001 Authentication | FR-001 | BE-001 | API-001 | TST-201 |
| BR-002 Resume Rules | FR-002 | BE-002 | API-002 | TST-202 |
| BR-003 Interview Configuration | FR-003 | BE-003 | API-003 | TST-203 |
| BR-004 Interview Session | FR-004 | BE-004 | API-004 | TST-204 |
| BR-005 AI Rules | FR-004, FR-005 | BE-005 | API-005 | TST-205 |
| BR-006 Evaluation | FR-005 | BE-005 | API-005 | TST-206 |
| BR-007 History | FR-006 | BE-006 | API-006 | TST-207 |
| BR-008 Security | FR-001, FR-008 | BE-008 | API-008 | TST-208 |
| BR-009 Documentation | All | — | — | Manual Review |
| BR-010 Claude Workflow | All | — | — | Manual Review |

---

# Feature Status

| Feature | Stage | Progress |
|----------|-------|----------|
| Authentication | Planning | 🟡 |
| Resume Upload | Planning | 🟡 |
| Resume Parsing | Planning | 🟡 |
| AI Interview | Planning | 🟡 |
| Evaluation | Planning | 🟡 |
| Dashboard | Planning | 🟡 |
| Reports | Planning | 🟡 |

---

# Traceability Rules

Every Functional Requirement must map to:

- One or more User Stories
- One or more API Contracts
- One Backend Service
- One Frontend Screen (if applicable)
- One Database Entity (if applicable)
- One Mermaid Diagram
- One Test Case

No requirement may exist without traceability.

---

# Update Rules

Whenever any of the following changes:

- Requirement
- API
- Database
- Architecture
- Frontend
- Backend
- AI Prompt
- Mermaid Diagram
- Test Case

The RTM **must** be updated before the feature is marked complete.

---

# Definition of Complete

A requirement is complete only when:

- Requirement approved
- User Story completed
- API implemented
- Backend implemented
- Frontend implemented
- Database updated
- AI component implemented
- Tests passing
- Documentation updated
- Mermaid updated
- RTM updated

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial Requirement Traceability Matrix |