"""Evaluation & report schemas — see docs/05-api-design/{evaluations,reports}.md."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.utils.grading import grade_for


# --------------------------------------------------------------------------- #
# Evaluations                                                                 #
# --------------------------------------------------------------------------- #
class EvaluationResponse(BaseModel):
    evaluation_id: uuid.UUID
    overall_score: float
    grade: str
    status: str
    generated_at: datetime

    @classmethod
    def from_model(cls, evaluation: Any) -> EvaluationResponse:
        score = float(evaluation.overall_score)
        return cls(
            evaluation_id=evaluation.id,
            overall_score=score,
            grade=grade_for(score),
            status="completed",
            generated_at=evaluation.created_at,
        )


class InterviewEvaluation(BaseModel):
    """Aggregate evaluation for a whole interview, derived from the report."""

    overall_score: float
    grade: str
    categories: dict[str, float]
    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]

    @classmethod
    def from_report(cls, report: Any) -> InterviewEvaluation:
        score = float(report.overall_score)
        categories: dict[str, float] = {}
        if report.technical_score is not None:
            categories["technical_knowledge"] = float(report.technical_score)
        if report.problem_solving_score is not None:
            categories["problem_solving"] = float(report.problem_solving_score)
        if report.communication_score is not None:
            categories["communication"] = float(report.communication_score)
        return cls(
            overall_score=score,
            grade=grade_for(score),
            categories=categories,
            strengths=report.strengths or [],
            weaknesses=report.weaknesses or [],
            recommendations=_roadmap_to_recommendations(report.improvement_roadmap or []),
        )


class StatusProgress(BaseModel):
    status: str
    progress: int


def _roadmap_to_recommendations(roadmap: list[dict]) -> list[str]:
    recommendations: list[str] = []
    for item in roadmap:
        if isinstance(item, dict):
            topic = item.get("topic")
            recommendation = item.get("recommendation")
            recommendations.append(
                f"{topic}: {recommendation}" if topic else str(recommendation)
            )
        else:
            recommendations.append(str(item))
    return recommendations
