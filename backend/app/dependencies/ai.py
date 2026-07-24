"""AI dependency wiring.

Builds the AI stack (Groq provider → orchestrator → service) for injection into
business services. Overriding :func:`get_ai_service` in tests swaps in a fake
provider so no network calls occur.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from app.ai.orchestrator import AIOrchestrator
from app.ai.provider import GroqProvider
from app.ai.service import AIService
from app.core.config import Settings, get_settings


def get_ai_service(settings: Annotated[Settings, Depends(get_settings)]) -> AIService:
    provider = GroqProvider(settings)
    orchestrator = AIOrchestrator(provider, max_retries=settings.GROQ_MAX_RETRIES)
    # GroqProvider implements both chat and transcription.
    return AIService(orchestrator, transcriber=provider)
