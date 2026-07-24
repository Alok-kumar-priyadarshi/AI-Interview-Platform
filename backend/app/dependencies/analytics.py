"""Dependency wiring for dashboard, history, and admin services."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.services.admin_service import AdminService
from app.services.dashboard_service import DashboardService
from app.services.history_service import HistoryService

DbSession = Annotated[AsyncSession, Depends(get_db)]


def get_dashboard_service(db: DbSession) -> DashboardService:
    return DashboardService(db)


def get_history_service(db: DbSession) -> HistoryService:
    return HistoryService(db)


def get_admin_service(db: DbSession) -> AdminService:
    return AdminService(db)
