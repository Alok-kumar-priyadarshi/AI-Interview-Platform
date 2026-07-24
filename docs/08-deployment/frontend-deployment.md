# Frontend Deployment Architecture

**Document ID:** DEP-003

**Version:** 1.0.0

**Status:** Approved

**Priority:** High

**Last Updated:** 2026-07-23

---

# Purpose

This document defines how the React frontend is built, deployed, configured, monitored, and maintained in production.

The frontend is deployed as a static application using Vercel with global CDN distribution.

---

# Objectives

Frontend deployment should provide:

- Fast global delivery
- Secure hosting
- Zero-downtime deployments
- Automatic rollbacks
- Efficient caching
- High availability
- Easy maintenance
- Production observability

---

# Technology Stack

Framework

- React
- TypeScript
- Vite

Hosting

- Vercel

Package Manager

- npm

Build Tool

- Vite

Version Control

- GitHub

---

# Deployment Architecture

```text
Developer

↓

GitHub

↓

Pull Request

↓

CI Validation

↓

Merge

↓

Vercel Build

↓

Static Assets

↓

Global CDN

↓

Users
```

---

# Build Process

## Step 1

Install dependencies

```bash
npm install
```

---

## Step 2

Type checking

```bash
npm run type-check
```

---

## Step 3

Linting

```bash
npm run lint
```

---

## Step 4

Run tests

```bash
npm test
```

---

## Step 5

Production build

```bash
npm run build
```

---

## Step 6

Deploy generated assets

```text
dist/
```

---

# Build Output

Generated assets include:

- HTML
- JavaScript bundles
- CSS bundles
- Images
- Fonts
- Icons

---

# Vercel Configuration

Recommended configuration

```text
Framework Preset

Vite
```

Root Directory

```text
frontend/
```

Output Directory

```text
dist/
```

Install Command

```bash
npm install
```

Build Command

```bash
npm run build
```

---

# Branch Strategy

| Branch | Deployment |
|----------|------------|
| main | Production |
| develop | Preview |
| feature/* | Preview |

Every pull request generates a preview deployment.

---

# CDN Strategy

Static assets are distributed using Vercel's global CDN.

Benefits

- Low latency
- Geographic distribution
- Automatic caching
- High availability

---

# Asset Optimization

Production assets should include:

- Code splitting
- Tree shaking
- Lazy loading
- Minification
- Compression
- Cache hashing

---

# Cache Strategy

## HTML

```text
Cache-Control:
no-cache
```

Always validate.

---

## JavaScript

```text
Cache-Control:
public,
max-age=31536000,
immutable
```

---

## CSS

Same policy as JavaScript.

---

## Images

Long-term caching using hashed filenames.

---

# Environment Variables

Frontend uses only public variables.

Examples

```text
VITE_API_BASE_URL

VITE_GOOGLE_CLIENT_ID

VITE_APP_ENV

VITE_ENABLE_ANALYTICS
```

Secrets must never be exposed.

---

# API Communication

All API requests use HTTPS.

```text
Frontend

↓

HTTPS

↓

FastAPI Backend
```

No direct database communication.

---

# Security Headers

Recommended headers

```text
Strict-Transport-Security

Content-Security-Policy

X-Frame-Options

Referrer-Policy

X-Content-Type-Options
```

---

# HTTPS

Requirements

- HTTPS only
- Automatic certificate renewal
- HTTP redirected to HTTPS

---

# Custom Domain

Example

```text
app.example.com
```

Requirements

- SSL enabled
- DNS configured
- Domain ownership verified

---

# Authentication

Google OAuth redirects

```text
Frontend

↓

Google

↓

Backend Callback

↓

Frontend Dashboard
```

Frontend never stores OAuth secrets.

---

# Static Asset Strategy

Organize assets

```text
assets/

images/

icons/

fonts/

animations/
```

Large assets should be optimized before deployment.

---

# Deployment Validation

Verify

- Application loads
- Routing works
- Login works
- API connectivity
- Static assets load
- Resume upload UI
- Dashboard rendering
- Error pages

---

# Health Verification

Confirm

- Home page
- Login page
- Dashboard
- Interview page
- Resume upload page
- History page

---

# Monitoring

Collect

- Build success
- Deployment history
- Page load metrics
- JavaScript errors
- Web Vitals
- Availability

---

# Rollback

Rollback procedure

```text
Previous Deployment

↓

Promote Previous Version

↓

Verify

↓

Restore Service
```

Rollback should complete within minutes.

---

# Performance Targets

| Metric | Target |
|---------|--------:|
| First Contentful Paint | <2 s |
| Largest Contentful Paint | <2.5 s |
| Time to Interactive | <3 s |
| Bundle Size | <500 KB (initial target) |

---

# Accessibility Verification

Confirm

- Keyboard navigation
- Screen reader support
- Color contrast
- Focus indicators
- Semantic HTML

---

# Logging

Frontend logs should include

- Build version
- Client errors
- API failures
- Route errors

Sensitive information must never be logged.

---

# Failure Scenarios

Handle

- API unavailable
- Authentication failure
- Network interruption
- CDN delay
- Asset loading failure

Display user-friendly error messages.

---

# Operational Best Practices

- Keep bundles small.
- Optimize images.
- Use lazy loading.
- Version deployments.
- Validate preview deployments before merge.

---

# Anti-Patterns

Avoid

- Hardcoded URLs
- Client-side secrets
- Large initial bundles
- Unused dependencies
- Blocking rendering with unnecessary scripts

---

# Business Rules

- Frontend deployments are fully automated.
- Every production deployment originates from the main branch.
- Public environment variables use the `VITE_` prefix.
- Static assets are fingerprinted for cache invalidation.
- Production deployments require successful validation.

---

# Related Documents

- `deployment-architecture.md`
- `environments.md`
- `backend-deployment.md`
- `environment-variables.md`
- `ci-cd-pipeline.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-23 | Initial frontend deployment architecture specification |