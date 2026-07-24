"""ORM models.

Importing this package registers every model on ``Base.metadata`` — required for
``create_all`` (tests) and Alembic autogenerate. Import models from here rather
than from individual modules to avoid partial metadata registration.
"""

from app.database.base import Base
from app.models.audit_log import AuditLog
from app.models.candidate_preferences import CandidatePreferences
from app.models.candidate_profile import CandidateProfile
from app.models.evaluation import Evaluation
from app.models.interview import Interview
from app.models.interview_answer import InterviewAnswer
from app.models.interview_question import InterviewQuestion
from app.models.report import Report
from app.models.resume import Resume
from app.models.user import User

__all__ = [
    "Base",
    "User",
    "Resume",
    "CandidateProfile",
    "CandidatePreferences",
    "Interview",
    "InterviewQuestion",
    "InterviewAnswer",
    "Evaluation",
    "Report",
    "AuditLog",
]
