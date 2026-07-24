"""Domain enumerations.

Centralises every documented allowed-value set (see the entity docs under
``docs/04-database/entities/``). Models use these to build ``CHECK`` constraints;
schemas and services reuse them for validation, so the permitted values live in
exactly one place.

All are :class:`str`-valued so they serialise cleanly to JSON and persist as
plain ``VARCHAR`` columns.
"""

from __future__ import annotations

from enum import StrEnum


class UserRole(StrEnum):
    CANDIDATE = "candidate"
    ADMIN = "admin"
    MODERATOR = "moderator"
    SUPPORT = "support"


class UploadStatus(StrEnum):
    UPLOADED = "uploaded"
    FAILED = "failed"
    DELETED = "deleted"


class ProcessingStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ExtractionStatus(StrEnum):
    COMPLETED = "completed"
    PARTIAL = "partial"
    FAILED = "failed"


class InterviewType(StrEnum):
    TEXT = "text"
    VOICE = "voice"


class ExperienceLevel(StrEnum):
    FRESHER = "fresher"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"


class Difficulty(StrEnum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class InterviewStatus(StrEnum):
    CREATED = "created"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class QuestionCategory(StrEnum):
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    HR = "hr"
    SYSTEM_DESIGN = "system_design"
    CODING = "coding"
    DATABASE = "database"
    OOP = "oop"
    OPERATING_SYSTEM = "operating_system"
    NETWORKING = "networking"
    APTITUDE = "aptitude"
    CUSTOM = "custom"


class AnswerType(StrEnum):
    TEXT = "text"
    VOICE = "voice"


class PreferredInterviewType(StrEnum):
    """Preference on the candidate profile (distinct from InterviewType, which is
    the text/voice interaction mode)."""

    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    MIXED = "mixed"


class InterviewVoice(StrEnum):
    MALE = "male"
    FEMALE = "female"


class PreferredLanguage(StrEnum):
    EN = "en"
    HI = "hi"


class SubmissionStatus(StrEnum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    PROCESSING = "processing"
    EVALUATED = "evaluated"
    FAILED = "failed"


class HiringRecommendation(StrEnum):
    STRONG_HIRE = "strong_hire"
    HIRE = "hire"
    BORDERLINE = "borderline"
    NO_HIRE = "no_hire"


class AuditSeverity(StrEnum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AuditEventType(StrEnum):
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    RESUME_UPLOAD = "resume_upload"
    RESUME_PROCESSING = "resume_processing"
    INTERVIEW = "interview"
    EVALUATION = "evaluation"
    REPORT = "report"
    SECURITY = "security"
    SYSTEM = "system"
    ADMIN = "admin"


def values(enum_cls: type[StrEnum]) -> list[str]:
    """Return the enum's values as a list — convenient for ``IN (...)`` checks."""
    return [member.value for member in enum_cls]
