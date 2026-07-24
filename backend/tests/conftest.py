"""Shared pytest fixtures.

Configures a fully isolated test environment:

* Required secrets are injected into the environment *before* any application
  module imports, so configuration validation passes without real credentials.
* The database is an in-memory async SQLite instance (via ``aiosqlite``); the
  ``get_db`` dependency is overridden to use it, so tests never touch Postgres.
* An ``httpx.AsyncClient`` bound to the ASGI app is provided for API tests.
"""

from __future__ import annotations

import os
from collections.abc import AsyncGenerator

# --- Environment must be set before importing app.* ------------------------
os.environ.setdefault("APP_ENV", "ci")
os.environ.setdefault("DATABASE_URL", "postgresql://test:test@localhost:5432/test")
os.environ.setdefault("GOOGLE_CLIENT_ID", "test-client-id")
os.environ.setdefault("GOOGLE_CLIENT_SECRET", "test-client-secret")
os.environ.setdefault("GOOGLE_REDIRECT_URI", "http://localhost/auth/callback")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-that-is-at-least-32-characters-long")
os.environ.setdefault("GROQ_API_KEY", "test-groq-key")
os.environ.setdefault("LOG_FORMAT", "console")
# Tests run over http:// — non-secure cookies so the client stores/sends them.
os.environ.setdefault("COOKIE_SECURE", "false")

import pytest_asyncio  # noqa: E402
from httpx import ASGITransport, AsyncClient  # noqa: E402
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.ai.schemas import (  # noqa: E402
    AnswerEvaluation,
    GeneratedQuestion,
    GeneratedQuestionSet,
    ReportContent,
    ResumeAnalysis,
)
from app.ai.service import AIMetadata, TranscriptionOutput  # noqa: E402
from app.database.session import get_db  # noqa: E402
from app.dependencies.ai import get_ai_service  # noqa: E402
from app.dependencies.auth import get_oauth_provider  # noqa: E402
from app.dependencies.resume import get_storage  # noqa: E402
from app.main import create_app  # noqa: E402
from app.models import Base  # noqa: E402  (imports all models → full metadata)
from app.schemas.auth import GoogleIdentity  # noqa: E402

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

_META = AIMetadata(model="fake-model", prompt_version="v1.0", duration_ms=1)


class FakeAIService:
    """Deterministic stand-in for :class:`app.ai.service.AIService`."""

    async def analyze_resume(self, resume_text: str):
        analysis = ResumeAnalysis(
            professional_summary="Backend engineer with FastAPI experience.",
            total_experience_years=2.0,
            highest_education="B.Tech",
            current_job_title="Backend Developer",
            skills=[{"name": "Python", "level": "Advanced"}],
            languages=["English"],
            ai_confidence_score=90.0,
        )
        return analysis, _META

    async def generate_questions(self, *, profile_summary: str, config: str, count: int):
        questions = [
            GeneratedQuestion(
                category="technical",
                difficulty="medium",
                question_text=f"Question {i + 1}?",
                expected_answer_points=["point"],
                evaluation_rubric={"technical_accuracy": 100},
                estimated_time_seconds=120,
            )
            for i in range(count)
        ]
        return GeneratedQuestionSet(questions=questions), _META

    async def evaluate_answer(self, *, question: str, rubric: dict, answer: str):
        evaluation = AnswerEvaluation(
            overall_score=85.0,
            technical_score=88.0,
            communication_score=82.0,
            problem_solving_score=80.0,
            strengths=["clear explanation"],
            weaknesses=["missed edge cases"],
            improvement_suggestions=["discuss trade-offs"],
            detailed_feedback="A solid answer overall.",
        )
        return evaluation, _META

    async def transcribe_audio(self, *, audio: bytes, filename: str, language: str | None = None):
        return TranscriptionOutput(
            text="This is the transcribed spoken answer.",
            language=language or "en",
            confidence=None,
        )

    async def generate_report(self, *, interview_summary: str, evaluations: str):
        report = ReportContent(
            overall_score=85.0,
            technical_score=88.0,
            communication_score=82.0,
            problem_solving_score=80.0,
            executive_summary="Strong candidate with good fundamentals.",
            strengths=["fundamentals"],
            weaknesses=["scalability"],
            improvement_roadmap=[
                {"priority": 1, "topic": "System Design", "recommendation": "practice"}
            ],
            hiring_recommendation="hire",
        )
        return report, _META


class InMemoryStorage:
    """In-memory storage provider for tests (no filesystem/network)."""

    def __init__(self) -> None:
        self.files: dict[str, bytes] = {}

    async def save(self, *, key: str, data: bytes, content_type: str) -> str:
        self.files[key] = data
        return f"local://{key}"

    async def load(self, *, key: str) -> bytes:
        return self.files[key]

    async def delete(self, *, key: str) -> None:
        self.files.pop(key, None)


class FakeOAuthClient:
    """Deterministic OAuth provider for tests.

    ``exchange_code`` derives a stable identity from the authorization code, so
    passing ``code="jane"`` yields ``jane@example.com``. This lets tests drive
    the real login flow without contacting Google.
    """

    def build_authorization_url(self, *, state: str) -> str:
        return f"https://accounts.google.test/authorize?state={state}"

    async def exchange_code(self, *, code: str) -> GoogleIdentity:
        handle = code or "tester"
        return GoogleIdentity(
            google_id=f"google-{handle}",
            email=f"{handle}@example.com",
            full_name=f"{handle.title()} Tester",
            picture="https://example.com/avatar.png",
            email_verified=True,
        )


@pytest_asyncio.fixture
async def db_engine():
    """Create an in-memory SQLite engine with all tables provisioned."""
    engine = create_async_engine(TEST_DATABASE_URL, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest_asyncio.fixture
async def db_session(db_engine) -> AsyncGenerator[AsyncSession]:
    """Yield a session bound to the test engine."""
    factory = async_sessionmaker(bind=db_engine, class_=AsyncSession, expire_on_commit=False)
    async with factory() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_engine) -> AsyncGenerator[AsyncClient]:
    """Yield an HTTP client with ``get_db`` overridden to the test database."""
    app = create_app()
    factory = async_sessionmaker(bind=db_engine, class_=AsyncSession, expire_on_commit=False)

    async def _override_get_db() -> AsyncGenerator[AsyncSession]:
        async with factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    # One storage instance shared across requests in a test, so a file written
    # in one request (e.g. a report PDF) is readable in a later request.
    storage = InMemoryStorage()
    app.dependency_overrides[get_db] = _override_get_db
    app.dependency_overrides[get_oauth_provider] = lambda: FakeOAuthClient()
    app.dependency_overrides[get_ai_service] = lambda: FakeAIService()
    app.dependency_overrides[get_storage] = lambda: storage

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as http_client:
        yield http_client

    app.dependency_overrides.clear()
