"""Aggregate router for API version 1.

Feature routers are included here and mounted under ``/api/v1`` by the
application factory. As new domains (auth, users, resumes, interviews, …) are
implemented, their routers are registered in this single place.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.api.v1 import (
    admin,
    answers,
    auth,
    candidate_profile,
    dashboard,
    evaluations,
    health,
    history,
    interviews,
    questions,
    reports,
    resume,
    users,
)

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(candidate_profile.router)
api_router.include_router(resume.router)
api_router.include_router(interviews.router)
api_router.include_router(questions.router)
api_router.include_router(answers.router)
api_router.include_router(evaluations.router)
api_router.include_router(reports.router)
api_router.include_router(history.router)
api_router.include_router(dashboard.router)
api_router.include_router(admin.router)
