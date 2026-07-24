"""Unit tests for the AI orchestrator and service (with a fake provider)."""

from __future__ import annotations

import json

import pytest

from app.ai.orchestrator import AIOrchestrator
from app.ai.provider import ChatMessage, LLMResponse, TokenUsage
from app.ai.schemas import ResumeAnalysis
from app.ai.service import AIService
from app.exceptions.base import AIResponseInvalidError


class ScriptedProvider:
    """Returns queued responses in order; records the number of calls."""

    def __init__(self, contents: list[str]) -> None:
        self._contents = contents
        self.calls = 0

    async def complete(self, messages, *, json_mode=True, temperature=0.2, max_tokens=None):  # noqa: ANN001
        content = self._contents[min(self.calls, len(self._contents) - 1)]
        self.calls += 1
        return LLMResponse(content=content, model="fake-model", usage=TokenUsage(), duration_ms=5)


@pytest.mark.asyncio
async def test_orchestrator_parses_and_validates() -> None:
    payload = json.dumps({"professional_summary": "Backend dev", "ai_confidence_score": 91})
    orch = AIOrchestrator(ScriptedProvider([payload]), max_retries=3)
    run = await orch.run([ChatMessage("user", "x")], ResumeAnalysis)
    assert isinstance(run.output, ResumeAnalysis)
    assert run.output.ai_confidence_score == 91


@pytest.mark.asyncio
async def test_orchestrator_retries_on_invalid_json_then_succeeds() -> None:
    good = json.dumps({"professional_summary": "ok"})
    provider = ScriptedProvider(["not json at all", good])
    orch = AIOrchestrator(provider, max_retries=3)
    run = await orch.run([ChatMessage("user", "x")], ResumeAnalysis)
    assert run.output.professional_summary == "ok"
    assert provider.calls == 2


@pytest.mark.asyncio
async def test_orchestrator_gives_up_after_max_retries() -> None:
    provider = ScriptedProvider(["garbage"])
    orch = AIOrchestrator(provider, max_retries=2)
    with pytest.raises(AIResponseInvalidError):
        await orch.run([ChatMessage("user", "x")], ResumeAnalysis)
    assert provider.calls == 2


@pytest.mark.asyncio
async def test_orchestrator_rejects_out_of_range_scores() -> None:
    bad = json.dumps({"overall_score": 250})  # invalid for AnswerEvaluation
    from app.ai.schemas import AnswerEvaluation

    orch = AIOrchestrator(ScriptedProvider([bad]), max_retries=1)
    with pytest.raises(AIResponseInvalidError):
        await orch.run([ChatMessage("user", "x")], AnswerEvaluation)


@pytest.mark.asyncio
async def test_ai_service_analyze_resume_returns_metadata() -> None:
    payload = json.dumps({"professional_summary": "s", "skills": [{"name": "Python"}]})
    service = AIService(AIOrchestrator(ScriptedProvider([payload]), max_retries=1))
    analysis, meta = await service.analyze_resume("some resume text")
    assert analysis.skills == [{"name": "Python"}]
    assert meta.prompt_version == "v1.0"
    assert meta.model == "fake-model"
