"""AI orchestrator.

Coordinates a single AI request end-to-end: invoke the provider, parse the JSON
response, validate it against the expected schema, and retry transient failures
(timeouts, malformed JSON, schema violations) up to a configured limit. Business
services depend on this rather than on a provider directly.
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import Generic, TypeVar

from pydantic import BaseModel, ValidationError

from app.ai.provider import ChatMessage, LLMProvider, LLMResponse
from app.core.logging import get_logger
from app.exceptions.base import AIResponseInvalidError, AIServiceError, LLMTimeoutError

logger = get_logger(__name__)

SchemaT = TypeVar("SchemaT", bound=BaseModel)


@dataclass(slots=True)
class AIRun(Generic[SchemaT]):
    """Result of a successful, validated AI request."""

    output: SchemaT
    response: LLMResponse


class AIOrchestrator:
    def __init__(self, provider: LLMProvider, *, max_retries: int = 3) -> None:
        self._provider = provider
        self._max_retries = max(1, max_retries)

    async def run(
        self,
        messages: list[ChatMessage],
        output_model: type[SchemaT],
        *,
        temperature: float = 0.2,
        max_tokens: int | None = None,
    ) -> AIRun[SchemaT]:
        """Invoke the provider and return a validated, typed result."""
        last_error: Exception | None = None

        for attempt in range(1, self._max_retries + 1):
            try:
                response = await self._provider.complete(
                    messages,
                    json_mode=True,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                output = self._parse(response.content, output_model)
            except (LLMTimeoutError, AIServiceError) as exc:
                last_error = exc
                logger.warning(
                    "ai_provider_transient_failure",
                    extra={"attempt": attempt, "error_type": type(exc).__name__},
                )
            except (json.JSONDecodeError, ValidationError) as exc:
                last_error = exc
                logger.warning("ai_response_invalid", extra={"attempt": attempt})
            else:
                return AIRun(output=output, response=response)

            if attempt < self._max_retries:
                await asyncio.sleep(min(2 ** (attempt - 1) * 0.5, 4.0))

        logger.error("ai_request_failed", extra={"attempts": self._max_retries})
        raise AIResponseInvalidError(
            "The AI service failed to produce a valid response."
        ) from last_error

    @staticmethod
    def _parse(content: str, output_model: type[SchemaT]) -> SchemaT:
        data = json.loads(content)
        return output_model.model_validate(data)
