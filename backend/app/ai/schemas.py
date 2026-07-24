"""Structured AI output contracts.

Every LLM response is validated against one of these Pydantic models before it
reaches business logic (see ai-architecture.md — "Structured Output Contract").
A response that fails validation is rejected and never persisted.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import Difficulty, HiringRecommendation, QuestionCategory

# --------------------------------------------------------------------------- #
# Resume analysis                                                             #
# --------------------------------------------------------------------------- #


class ResumeAnalysis(BaseModel):
    """Structured candidate profile extracted from resume text."""

    model_config = ConfigDict(extra="ignore")

    professional_summary: str | None = None
    total_experience_years: float | None = Field(default=None, ge=0, le=60)
    highest_education: str | None = None
    current_job_title: str | None = None
    current_company: str | None = None
    skills: list[dict] = Field(default_factory=list)
    education: list[dict] = Field(default_factory=list)
    experience: list[dict] = Field(default_factory=list)
    projects: list[dict] = Field(default_factory=list)
    certifications: list[dict] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    ai_confidence_score: float | None = Field(default=None, ge=0, le=100)


# --------------------------------------------------------------------------- #
# Interview question generation                                               #
# --------------------------------------------------------------------------- #


class GeneratedQuestion(BaseModel):
    model_config = ConfigDict(extra="ignore")

    category: QuestionCategory
    difficulty: Difficulty
    question_text: str = Field(..., min_length=1, max_length=10_000)
    expected_answer_points: list[str] = Field(default_factory=list)
    evaluation_rubric: dict = Field(default_factory=dict)
    estimated_time_seconds: int | None = Field(default=None, gt=0)


class GeneratedQuestionSet(BaseModel):
    questions: list[GeneratedQuestion] = Field(..., min_length=1)


# --------------------------------------------------------------------------- #
# Answer evaluation                                                           #
# --------------------------------------------------------------------------- #


class AnswerEvaluation(BaseModel):
    model_config = ConfigDict(extra="ignore")

    overall_score: float = Field(..., ge=0, le=100)
    technical_score: float | None = Field(default=None, ge=0, le=100)
    communication_score: float | None = Field(default=None, ge=0, le=100)
    problem_solving_score: float | None = Field(default=None, ge=0, le=100)
    confidence_score: float | None = Field(default=None, ge=0, le=100)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    improvement_suggestions: list[str] = Field(default_factory=list)
    detailed_feedback: str | None = None


# --------------------------------------------------------------------------- #
# Interview report                                                            #
# --------------------------------------------------------------------------- #


class ReportContent(BaseModel):
    model_config = ConfigDict(extra="ignore")

    overall_score: float = Field(..., ge=0, le=100)
    technical_score: float | None = Field(default=None, ge=0, le=100)
    communication_score: float | None = Field(default=None, ge=0, le=100)
    problem_solving_score: float | None = Field(default=None, ge=0, le=100)
    executive_summary: str = Field(..., min_length=1)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    improvement_roadmap: list[dict] = Field(default_factory=list)
    hiring_recommendation: HiringRecommendation
