# Documentation Manifest (docs/index.md)

> **Purpose:** This document is the entry point for every development session. Claude Code and contributors must read this file before modifying the project.

---

# 1. Project Overview

**Project:** AI Career Interview Platform

**Goal**
Build a full-stack AI-powered mock interview platform that helps students and job seekers prepare for technical, HR, and behavioral interviews using voice and text.

**Primary Users**
- Students
- Fresh graduates
- Job seekers

**Core Tech Stack**
- Frontend: React (Vite), Tailwind CSS
- Backend: FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy
- AI: Groq API
- Authentication: Google OAuth
- Version Control: Git

---

# 2. Documentation Philosophy

The documentation is the source of truth.

Rules:
1. Documentation is written before implementation.
2. Code must follow documentation.
3. Architecture changes require documentation updates first.
4. No undocumented features may be implemented.
5. Every completed task must update the Context folder.

---

# 3. Documentation Hierarchy

Priority (highest → lowest)

1. Requirements
2. Architecture
3. Feature Specifications
4. API Contracts
5. Database Design
6. Frontend / Backend Design
7. Source Code
8. Tests
9. Context Files

---

# 4. Reading Order (Every New Claude Session)

1. docs/index.md
2. context/current-state.md
3. context/next-task.md
4. Relevant requirement
5. Relevant architecture
6. Relevant feature specification
7. Relevant API contract
8. Relevant database document
9. Relevant Mermaid diagram
10. Begin implementation

---

# 5. Update Order (After Every Coding Session)

1. Source Code
2. Documentation
3. API Contracts
4. Mermaid Diagrams
5. Tests
6. CHANGELOG
7. context/current-state.md
8. context/project-progress.md
9. context/session-summary.md
10. context/next-task.md

---

# 6. Naming Convention

Use lowercase-kebab-case for all documentation.

Examples:
- project-vision.md
- api-contracts.md
- interview-flow.md

---

# 7. Documentation Standards

Every feature must include:

- Requirement
- Architecture
- Feature Specification
- API Contract
- Database Impact (if any)
- Mermaid Diagram(s)
- Testing Notes
- Context Update

---

# 8. Context Standards

Claude must always update:

- current-state.md
- next-task.md
- project-progress.md
- session-summary.md
- changelog.md

No coding session is complete until these files are updated.

---

# 9. Completion Checklist

Before ending a session verify:

- [ ] Feature implemented
- [ ] Documentation updated
- [ ] API updated
- [ ] Mermaid updated
- [ ] Tests updated
- [ ] Context updated
- [ ] Changelog updated
- [ ] Next task defined
- [ ] Session summary written

---

# 10. Traceability

Every feature receives a unique ID.

Example:

FR-001 Resume Upload
FR-002 AI Interview
FR-003 Voice Interview

API-001 Authentication
API-002 Resume Upload

DB-001 Users
DB-002 Interviews

MER-001 High-Level Architecture
MER-002 Interview Sequence

These IDs are referenced throughout the project.

---

# 11. Document Lifecycle

Draft → Reviewed → Approved → Implemented → Deprecated

---

# 12. Important Rule for Claude

Claude Code must never assume project status.

Before implementing anything it must:
1. Read this file.
2. Read the Context folder.
3. Continue from the recorded project state.
4. Update all required Context files before ending the session.
