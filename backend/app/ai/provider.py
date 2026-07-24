"""LLM provider abstraction and Groq adapter.

Business services never touch a provider SDK directly — they go through the
:class:`LLMProvider` protocol (ai-architecture.md — "Provider Independence").
Swapping Groq for another provider means adding one adapter here and changing a
single dependency binding.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from app.core.config import Settings
from app.core.logging import get_logger

logger = get_logger(__name__)


@dataclass(slots=True)
class ChatMessage:
    role: str  # "system" | "user" | "assistant"
    content: str


@dataclass(slots=True)
class TokenUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


@dataclass(slots=True)
class LLMResponse:
    content: str
    model: str
    usage: TokenUsage = field(default_factory=TokenUsage)
    duration_ms: int = 0


@dataclass(slots=True)
class TranscriptionResult:
    text: str
    language: str
    confidence: float | None = None
    duration_ms: int = 0


class LLMProvider(Protocol):
    """A chat-completion provider that can return JSON-only responses."""

    async def complete(
        self,
        messages: list[ChatMessage],
        *,
        json_mode: bool = True,
        temperature: float = 0.2,
        max_tokens: int | None = None,
    ) -> LLMResponse: ...


class TranscriptionProvider(Protocol):
    """A speech-to-text provider (e.g. Groq Whisper)."""

    async def transcribe(
        self, *, audio: bytes, filename: str, language: str | None = None
    ) -> TranscriptionResult: ...


class GroqProvider:
    """Groq chat-completions adapter.

    The ``groq`` SDK is imported lazily so the module (and the wider app) can be
    imported in environments where the SDK is absent — tests inject a fake
    provider instead of constructing this class.
    """

    def __init__(self, settings: Settings) -> None:
        self._model = settings.GROQ_MODEL
        self._transcription_model = settings.GROQ_TRANSCRIPTION_MODEL
        self._timeout = settings.GROQ_TIMEOUT
        self._max_retries = settings.GROQ_MAX_RETRIES
        self._api_key = settings.GROQ_API_KEY
        self._client = None  # lazily constructed

    def _get_client(self):  # type: ignore[no-untyped-def]
        if self._client is None:
            from groq import AsyncGroq

            self._client = AsyncGroq(
                api_key=self._api_key,
                timeout=self._timeout,
                max_retries=0,  # retries are handled by the orchestrator
            )
        return self._client

    async def complete(
        self,
        messages: list[ChatMessage],
        *,
        json_mode: bool = True,
        temperature: float = 0.2,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        import time

        from groq import APIError, APITimeoutError

        from app.exceptions.base import AIServiceError, LLMTimeoutError

        client = self._get_client()
        payload = {
            "model": self._model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": temperature,
        }
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        start = time.perf_counter()
        try:
            completion = await client.chat.completions.create(**payload)
        except APITimeoutError as exc:
            raise LLMTimeoutError() from exc
        except APIError as exc:
            logger.warning("groq_api_error", extra={"error": str(exc)})
            raise AIServiceError("The AI provider returned an error.") from exc

        duration_ms = int((time.perf_counter() - start) * 1000)
        choice = completion.choices[0]
        usage = TokenUsage(
            prompt_tokens=getattr(completion.usage, "prompt_tokens", 0),
            completion_tokens=getattr(completion.usage, "completion_tokens", 0),
            total_tokens=getattr(completion.usage, "total_tokens", 0),
        )
        return LLMResponse(
            content=choice.message.content or "",
            model=self._model,
            usage=usage,
            duration_ms=duration_ms,
        )

    async def transcribe(
        self, *, audio: bytes, filename: str, language: str | None = None
    ) -> TranscriptionResult:
        import time

        from groq import APIError, APITimeoutError

        from app.exceptions.base import TranscriptionFailedError

        client = self._get_client()
        params: dict = {
            "file": (filename, audio),
            "model": self._transcription_model,
            "response_format": "verbose_json",
        }
        if language:
            params["language"] = language

        start = time.perf_counter()
        try:
            result = await client.audio.transcriptions.create(**params)
        except (APIError, APITimeoutError) as exc:
            logger.warning("groq_transcription_error", extra={"error": str(exc)})
            raise TranscriptionFailedError() from exc

        duration_ms = int((time.perf_counter() - start) * 1000)
        text = getattr(result, "text", "") or ""
        detected = getattr(result, "language", None) or language or "en"
        return TranscriptionResult(
            text=text.strip(),
            language=detected,
            confidence=None,  # Whisper verbose_json exposes segment logprobs, not a single score.
            duration_ms=duration_ms,
        )
