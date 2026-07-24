# Build Feature Workflow

**Document ID:** CLAUDE-WF-001
**Version:** 1.0.0
**Status:** Active
**Priority:** Highest
**Last Updated:** 2026-07-23

---

# Purpose

This workflow defines the mandatory process for implementing any new feature in
the AI Career Interview Platform. Every development session should follow these
steps to ensure consistency, traceability, and maintainability.

---

# Phase 1 — Understand

## Step 1: Read Project Context

Read, in order:

1. docs/index.md
2. context/current-state.md
3. context/next-task.md
4. Relevant requirements (FR/NFR/BR)
5. Relevant ADRs (if any)

**Output**
- Clear understanding of the feature scope.

---

## Step 2: Validate Readiness

Confirm:

- Requirement exists.
- User Story exists.
- Acceptance criteria exist.
- RTM entry exists.
- Architecture supports the feature.

If any item is missing, stop implementation and document the blocker.

---

# Phase 2 — Design

## Step 3: Review Design

Review:

- Backend architecture
- Frontend architecture
- Database schema
- API contracts
- AI prompts (if applicable)

Avoid introducing duplicate logic.

---

# Phase 3 — Implement

## Step 4: Backend

- Create/update services.
- Add validation.
- Implement business logic.
- Add database migrations if required.

## Step 5: Frontend

- Build reusable components.
- Connect APIs.
- Handle loading and error states.
- Ensure accessibility.

## Step 6: AI (if applicable)

- Add or update prompts.
- Validate structured outputs.
- Keep provider-specific code behind abstractions.

---

# Phase 4 — Verify

## Step 7: Testing

Complete:

- Unit tests
- Integration tests
- End-to-end tests (if applicable)
- Manual verification

---

# Phase 5 — Documentation

## Step 8: Update Documentation

Update all affected files:

- Requirements
- API contracts
- Architecture
- Mermaid diagrams
- Changelog
- RTM

---

## Step 9: Update Context

Before ending the session, update:

- current-state.md
- next-task.md
- session-summary.md
- project-progress.md

---

# Phase 6 — Completion

A feature is complete only if:

- [ ] Requirements satisfied
- [ ] Acceptance criteria passed
- [ ] Backend complete
- [ ] Frontend complete
- [ ] Tests passing
- [ ] Documentation updated
- [ ] RTM updated
- [ ] Context updated
- [ ] Changelog updated

---

# Deliverables

Each completed feature should leave behind:

- Updated source code
- Updated documentation
- Updated tests
- Updated RTM
- Updated context
- Clear next task

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial build feature workflow |
