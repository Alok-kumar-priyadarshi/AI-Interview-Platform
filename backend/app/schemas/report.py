"""Report schemas — see docs/05-api-design/reports.md."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.schemas.evaluation import _roadmap_to_recommendations
from app.utils.grading import grade_for


class ReportSummary(BaseModel):
    report_id: uuid.UUID
    overall_score: float
    grade: str
    hiring_recommendation: str
    created_at: datetime

    @classmethod
    def from_model(cls, report: Any) -> ReportSummary:
        score = float(report.overall_score)
        return cls(
            report_id=report.id,
            overall_score=score,
            grade=grade_for(score),
            hiring_recommendation=report.hiring_recommendation,
            created_at=report.generated_at,
        )


class ReportDetail(BaseModel):
    report_id: uuid.UUID
    overall_score: float
    grade: str
    hiring_recommendation: str
    summary: str
    categories: dict[str, float]
    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]
    generated_at: datetime

    @classmethod
    def from_model(cls, report: Any) -> ReportDetail:
        score = float(report.overall_score)
        categories: dict[str, float] = {}
        if report.technical_score is not None:
            categories["technical_knowledge"] = float(report.technical_score)
        if report.problem_solving_score is not None:
            categories["problem_solving"] = float(report.problem_solving_score)
        if report.communication_score is not None:
            categories["communication"] = float(report.communication_score)
        return cls(
            report_id=report.id,
            overall_score=score,
            grade=grade_for(score),
            hiring_recommendation=report.hiring_recommendation,
            summary=report.executive_summary,
            categories=categories,
            strengths=report.strengths or [],
            weaknesses=report.weaknesses or [],
            recommendations=_roadmap_to_recommendations(report.improvement_roadmap or []),
            generated_at=report.generated_at,
        )


class InterviewReportRef(BaseModel):
    report_id: uuid.UUID
    status: str
