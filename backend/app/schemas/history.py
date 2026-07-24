"""History schemas — see docs/05-api-design/history.md."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.utils.grading import grade_for


class HistoryItem(BaseModel):
    history_id: uuid.UUID
    interview_id: uuid.UUID
    completed_at: datetime | None
    overall_score: float | None
    grade: str
    difficulty: str
    mode: str
    target_role: str

    @classmethod
    def from_row(cls, interview: Any, report: Any | None) -> HistoryItem:
        score = (
            float(report.overall_score)
            if report is not None
            else (float(interview.overall_score) if interview.overall_score is not None else None)
        )
        return cls(
            history_id=interview.id,
            interview_id=interview.id,
            completed_at=interview.completed_at,
            overall_score=score,
            grade=grade_for(score),
            difficulty=interview.difficulty,
            mode=interview.interview_type,
            target_role=interview.target_role,
        )


class HistoryDetail(BaseModel):
    history_id: uuid.UUID
    interview_id: uuid.UUID
    report_id: uuid.UUID | None
    overall_score: float | None
    grade: str
    duration_minutes: int | None
    completed_at: datetime | None

    @classmethod
    def from_row(cls, interview: Any, report: Any | None) -> HistoryDetail:
        score = float(report.overall_score) if report is not None else None
        return cls(
            history_id=interview.id,
            interview_id=interview.id,
            report_id=report.id if report is not None else None,
            overall_score=score,
            grade=grade_for(score),
            duration_minutes=(
                round(interview.duration_seconds / 60)
                if interview.duration_seconds is not None
                else None
            ),
            completed_at=interview.completed_at,
        )
