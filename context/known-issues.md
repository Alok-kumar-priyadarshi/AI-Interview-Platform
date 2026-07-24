# Known Issues & Technical Debt

**Version:** 1.0.0  
**Status:** Active  
**Last Updated:** 2026-07-23

---

# Purpose

This document tracks all known issues, technical debt, architectural concerns,
limitations, and planned refactoring tasks.

Unlike `todo.md`, which lists planned work, this document records things that
are already known to require attention.

Not every issue is a bug.

Some issues may be:

- Architectural limitations
- AI limitations
- Performance concerns
- Security concerns
- Missing features
- Planned refactoring
- External dependencies
- Documentation gaps

---

# Issue Lifecycle

```
Identified
      ↓
Reviewed
      ↓
Prioritized
      ↓
In Progress
      ↓
Resolved
      ↓
Closed
```

Never delete resolved issues.

Move them to the **Resolved Issues** section.

---

# Priority Levels

| Priority | Description |
|-----------|-------------|
| Critical | Prevents project progress or production use |
| High | Significant impact but workaround exists |
| Medium | Noticeable issue with limited impact |
| Low | Minor improvement or cosmetic issue |

---

# Severity Levels

| Severity | Meaning |
|----------|---------|
| Blocker | Development cannot continue |
| Major | Important functionality affected |
| Moderate | Limited functionality affected |
| Minor | Small issue with little impact |

---

# Status Values

Use one of the following:

- Identified
- Investigating
- Planned
- In Progress
- Resolved
- Closed

---

# Active Issues

Currently there are no known issues.

---

# Planned Technical Debt

## TD-001

### Title

Prompt Optimization

### Category

AI

### Priority

Medium

### Status

Planned

### Description

Initial prompt engineering will prioritize correctness over optimization.
Prompt refinement will occur after Version 1 functionality is complete.

### Planned Resolution

Iterative prompt optimization using evaluation metrics.

---

## TD-002

### Title

Scalability Review

### Category

Architecture

### Priority

Medium

### Status

Planned

### Description

The initial architecture is optimized for Version 1.
A scalability review will be performed before introducing high-concurrency
features or enterprise deployments.

### Planned Resolution

Conduct architecture review after Version 1 release.

---

## TD-003

### Title

Performance Benchmarking

### Category

Performance

### Priority

Low

### Status

Planned

### Description

Formal benchmarking has not yet been performed.

Areas to evaluate include:

- API latency
- Resume parsing
- AI response generation
- Database queries

### Planned Resolution

Execute performance testing during Milestone 8.

---

# Architectural Limitations

Current limitations:

- No distributed architecture in Version 1.
- Single backend service.
- Single PostgreSQL database.
- AI provider limited to Groq API.
- No offline interview capability.

These limitations are acceptable for Version 1.

---

# External Dependencies

The project depends on:

- Groq API
- Google OAuth
- PostgreSQL
- SQLAlchemy
- FastAPI
- React
- Tailwind CSS

Changes in these services or libraries may require project updates.

---

# Security Observations

Current status:

No known security issues.

Future reviews should include:

- Authentication
- Authorization
- Prompt injection
- File upload validation
- Rate limiting
- API abuse prevention
- Sensitive data handling

---

# AI Limitations

Current assumptions:

- AI responses may vary.
- Interview scoring may not be perfectly deterministic.
- Prompt engineering will evolve over time.
- Evaluation quality depends on the underlying LLM.

These are expected characteristics rather than defects.

---

# Documentation Gaps

Current status:

None.

All required documentation will be created before implementation begins.

---

# Resolved Issues

No resolved issues yet.

Resolved issues should be moved here instead of being deleted.

Example format:

```
Issue ID: BUG-004

Title:
Resume parser failed for scanned PDFs.

Resolution:
OCR preprocessing added.

Resolved On:
2026-09-15
```

---

# Review Schedule

This document should be reviewed:

- Before each milestone.
- Before every release.
- After major architectural changes.
- After significant bug reports.
- After production incidents.

---

# Maintenance Rules

- Never delete historical issues.
- Update issue status instead of removing entries.
- Assign unique IDs (BUG-001, TD-001, SEC-001, PERF-001).
- Keep descriptions concise and factual.
- Link related documentation when applicable.

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial Known Issues & Technical Debt register |