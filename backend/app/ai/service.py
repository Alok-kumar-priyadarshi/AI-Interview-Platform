"""High-level AI service.

The single entry point business services use for AI work. Each method assembles
context, selects the versioned prompt, runs the orchestrator, and returns a
validated typed result together with metadata (model + prompt version + latency)
that callers persist for traceability.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from app.ai import prompts
from app.ai.orchestrator import AIOrchestrator
from app.ai.prompts import PromptTemplate
from app.ai.provider import TranscriptionProvider
from app.ai.schemas import (
    AnswerEvaluation,
    GeneratedQuestionSet,
    ReportContent,
    ResumeAnalysis,
)
from app.core.logging import get_logger
from app.exceptions.base import TranscriptionFailedError

logger = get_logger(__name__)


@dataclass(slots=True)
class AIMetadata:
    model: str
    prompt_version: str
    duration_ms: int


@dataclass(slots=True)
class TranscriptionOutput:
    text: str
    language: str
    confidence: float | None


class AIService:
    def __init__(
        self, orchestrator: AIOrchestrator, transcriber: TranscriptionProvider | None = None
    ) -> None:
        self._orchestrator = orchestrator
        self._transcriber = transcriber

    async def analyze_resume(self, resume_text: str) -> tuple[ResumeAnalysis, AIMetadata]:
        messages = prompts.resume_analysis_prompt(resume_text)
        run = await self._orchestrator.run(messages, ResumeAnalysis, temperature=0.1)
        return run.output, self._meta(run, prompts.RESUME_ANALYSIS)

    async def generate_questions(
        self, *, profile_summary: str, config: str, count: int
    ) -> tuple[GeneratedQuestionSet, AIMetadata]:
        messages = prompts.question_generation_prompt(
            profile_summary=profile_summary, config=config, count=count
        )
        run = await self._orchestrator.run(messages, GeneratedQuestionSet, temperature=0.5)
        return run.output, self._meta(run, prompts.QUESTION_GENERATION)

    async def evaluate_answer(
        self, *, question: str, rubric: dict, answer: str
    ) -> tuple[AnswerEvaluation, AIMetadata]:
        messages = prompts.answer_evaluation_prompt(
            question=question, rubric=json.dumps(rubric), answer=answer
        )
        run = await self._orchestrator.run(messages, AnswerEvaluation, temperature=0.2)
        return run.output, self._meta(run, prompts.ANSWER_EVALUATION)

    async def transcribe_audio(
        self, *, audio: bytes, filename: str, language: str | None = None
    ) -> TranscriptionOutput:
        if self._transcriber is None:
            raise TranscriptionFailedError("Transcription is not configured.")
        result = await self._transcriber.transcribe(
            audio=audio, filename=filename, language=language
        )
        return TranscriptionOutput(
            text=result.text, language=result.language, confidence=result.confidence
        )

    async def generate_report(
        self, *, interview_summary: str, evaluations: str
    ) -> tuple[ReportContent, AIMetadata]:
        messages = prompts.report_generation_prompt(
            interview_summary=interview_summary, evaluations=evaluations
        )
        run = await self._orchestrator.run(messages, ReportContent, temperature=0.3)
        return run.output, self._meta(run, prompts.REPORT_GENERATION)

    @staticmethod
    def _meta(run, template: PromptTemplate) -> AIMetadata:  # type: ignore[no-untyped-def]
        return AIMetadata(
            model=run.response.model,
            prompt_version=template.version,
            duration_ms=run.response.duration_ms,
        )
