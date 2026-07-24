"""Unit tests for the ORM models: persistence, relationships, and constraints."""

from __future__ import annotations

import uuid
from decimal import Decimal

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    AuditLog,
    CandidateProfile,
    Evaluation,
    Interview,
    InterviewAnswer,
    InterviewQuestion,
    Report,
    Resume,
    User,
)
from app.models.enums import (
    AuditEventType,
    HiringRecommendation,
    InterviewStatus,
    QuestionCategory,
    UserRole,
)


async def _make_user(db: AsyncSession, *, email: str = "jane@example.com") -> User:
    user = User(
        google_id=f"google-{uuid.uuid4()}",
        email=email,
        full_name="Jane Candidate",
        role=UserRole.CANDIDATE,
    )
    db.add(user)
    await db.flush()
    return user


async def _make_resume(db: AsyncSession, user: User) -> Resume:
    resume = Resume(
        user_id=user.id,
        original_filename="jane_resume.pdf",
        stored_filename=f"{uuid.uuid4()}.pdf",
        storage_path="resumes/jane_resume.pdf",
        mime_type="application/pdf",
        file_size_bytes=123456,
        checksum_sha256="a" * 64,
    )
    db.add(resume)
    await db.flush()
    return resume


@pytest.mark.asyncio
async def test_user_defaults_and_persistence(db_session: AsyncSession) -> None:
    user = await _make_user(db_session)
    await db_session.commit()

    fetched = (await db_session.execute(select(User).where(User.id == user.id))).scalar_one()
    assert fetched.role == UserRole.CANDIDATE
    assert fetched.is_active is True
    assert fetched.created_at is not None
    assert fetched.updated_at is not None


@pytest.mark.asyncio
async def test_email_uniqueness_enforced(db_session: AsyncSession) -> None:
    await _make_user(db_session, email="dup@example.com")
    await db_session.commit()

    db_session.add(
        User(google_id="another", email="dup@example.com", full_name="Dup", role=UserRole.CANDIDATE)
    )
    with pytest.raises(IntegrityError):
        await db_session.commit()
    await db_session.rollback()


@pytest.mark.asyncio
async def test_full_interview_graph(db_session: AsyncSession) -> None:
    """End-to-end object graph across all nine entities with relationships."""
    user = await _make_user(db_session)
    resume = await _make_resume(db_session, user)

    profile = CandidateProfile(
        resume_id=resume.id,
        professional_summary="Backend engineer",
        skills=[{"name": "Python", "level": "Advanced"}],
        ai_confidence_score=Decimal("92.50"),
    )
    interview = Interview(
        user_id=user.id,
        resume_id=resume.id,
        title="Backend Mock Interview",
        target_role="Backend Developer",
        ai_model="groq-llama",
        total_questions=1,
        answered_questions=1,
        status=InterviewStatus.COMPLETED,
    )
    db_session.add_all([profile, interview])
    await db_session.flush()

    question = InterviewQuestion(
        interview_id=interview.id,
        question_number=1,
        category=QuestionCategory.DATABASE,
        question_text="Explain ACID properties.",
        expected_answer_points=["Atomicity", "Consistency", "Isolation", "Durability"],
        evaluation_rubric={"technical_accuracy": 60, "communication": 40},
        ai_model="groq-llama",
    )
    db_session.add(question)
    await db_session.flush()

    answer = InterviewAnswer(
        question_id=question.id,
        answer_text="ACID stands for Atomicity, Consistency, Isolation, Durability.",
    )
    db_session.add(answer)
    await db_session.flush()

    evaluation = Evaluation(
        answer_id=answer.id,
        overall_score=Decimal("88.00"),
        technical_score=Decimal("90.00"),
        strengths=["clear definition"],
        weaknesses=["no examples"],
        improvement_suggestions=["add real-world examples"],
        evaluation_model="groq-llama",
    )
    report = Report(
        interview_id=interview.id,
        overall_score=Decimal("88.00"),
        executive_summary="Strong fundamentals.",
        hiring_recommendation=HiringRecommendation.HIRE,
        report_model="groq-llama",
    )
    audit = AuditLog(
        user_id=user.id,
        event_type=AuditEventType.INTERVIEW,
        action="GENERATE_REPORT",
        event_metadata={"interview_id": str(interview.id)},
    )
    db_session.add_all([evaluation, report, audit])
    await db_session.commit()

    # Relationship traversal
    loaded = (
        await db_session.execute(select(Interview).where(Interview.id == interview.id))
    ).scalar_one()
    await db_session.refresh(loaded, ["questions", "report"])
    assert len(loaded.questions) == 1
    assert loaded.report is not None
    assert loaded.report.hiring_recommendation == HiringRecommendation.HIRE

    await db_session.refresh(question, ["answer"])
    await db_session.refresh(answer, ["evaluation"])
    assert question.answer is not None
    assert answer.evaluation.overall_score == Decimal("88.00")


@pytest.mark.asyncio
async def test_one_answer_per_question(db_session: AsyncSession) -> None:
    user = await _make_user(db_session)
    resume = await _make_resume(db_session, user)
    interview = Interview(
        user_id=user.id,
        resume_id=resume.id,
        title="T",
        target_role="Dev",
        ai_model="groq-llama",
    )
    db_session.add(interview)
    await db_session.flush()
    question = InterviewQuestion(
        interview_id=interview.id,
        question_number=1,
        category=QuestionCategory.TECHNICAL,
        question_text="Q?",
        ai_model="groq-llama",
    )
    db_session.add(question)
    await db_session.flush()

    db_session.add(InterviewAnswer(question_id=question.id, answer_text="first"))
    await db_session.commit()

    db_session.add(InterviewAnswer(question_id=question.id, answer_text="second"))
    with pytest.raises(IntegrityError):
        await db_session.commit()
    await db_session.rollback()
