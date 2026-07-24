"""Domain exception hierarchy.

Every application-level failure is expressed as an :class:`AppException` (or a
subclass). Each carries an HTTP status code, a machine-readable
:class:`~app.core.error_codes.ErrorCode`, a human-readable message, and
optional structured ``details``. Centralised handlers (see
``app/exceptions/handlers.py``) serialise these into the standard error
envelope defined in ``docs/05-api-design/errors.md``.

Service and repository code should raise these exceptions rather than
FastAPI's ``HTTPException`` so that error semantics stay independent of the
web framework.
"""

from __future__ import annotations

from typing import Any

from app.core.error_codes import ErrorCode


class AppException(Exception):
    """Base class for all expected, handled application errors."""

    status_code: int = 500
    error_code: ErrorCode = ErrorCode.INTERNAL_SERVER_ERROR
    message: str = "An unexpected error occurred."

    def __init__(
        self,
        message: str | None = None,
        *,
        error_code: ErrorCode | None = None,
        status_code: int | None = None,
        details: list[dict[str, Any]] | None = None,
    ) -> None:
        self.message = message or self.message
        self.error_code = error_code or self.error_code
        self.status_code = status_code or self.status_code
        self.details = details
        super().__init__(self.message)


# --------------------------------------------------------------------------- #
# Authentication (401)                                                         #
# --------------------------------------------------------------------------- #
class AuthenticationError(AppException):
    status_code = 401
    error_code = ErrorCode.UNAUTHORIZED
    message = "Authentication required."


class InvalidTokenError(AuthenticationError):
    error_code = ErrorCode.INVALID_TOKEN
    message = "The provided token is invalid."


class TokenExpiredError(AuthenticationError):
    error_code = ErrorCode.TOKEN_EXPIRED
    message = "The provided token has expired."


class OAuthError(AuthenticationError):
    error_code = ErrorCode.OAUTH_FAILED
    message = "Google authentication failed."


# --------------------------------------------------------------------------- #
# Authorization (403)                                                          #
# --------------------------------------------------------------------------- #
class AuthorizationError(AppException):
    status_code = 403
    error_code = ErrorCode.FORBIDDEN
    message = "Access denied."


class AdminRequiredError(AuthorizationError):
    error_code = ErrorCode.ADMIN_REQUIRED
    message = "Administrator access required."


# --------------------------------------------------------------------------- #
# Validation (422)                                                            #
# --------------------------------------------------------------------------- #
class ValidationError(AppException):
    status_code = 422
    error_code = ErrorCode.VALIDATION_ERROR
    message = "One or more validation errors occurred."


# --------------------------------------------------------------------------- #
# Resources (404)                                                            #
# --------------------------------------------------------------------------- #
class NotFoundError(AppException):
    status_code = 404
    error_code = ErrorCode.INTERNAL_SERVER_ERROR  # overridden per resource
    message = "The requested resource was not found."


class UserNotFoundError(NotFoundError):
    error_code = ErrorCode.USER_NOT_FOUND
    message = "User not found."


class ProfileNotFoundError(NotFoundError):
    error_code = ErrorCode.PROFILE_NOT_FOUND
    message = "Candidate profile not found."


class ResumeNotFoundError(NotFoundError):
    error_code = ErrorCode.RESUME_NOT_FOUND
    message = "Resume not found."


class InterviewNotFoundError(NotFoundError):
    error_code = ErrorCode.INTERVIEW_NOT_FOUND
    message = "Interview not found."


class QuestionNotFoundError(NotFoundError):
    error_code = ErrorCode.QUESTION_NOT_FOUND
    message = "Question not found."


class AnswerNotFoundError(NotFoundError):
    error_code = ErrorCode.ANSWER_NOT_FOUND
    message = "Answer not found."


class EvaluationNotFoundError(NotFoundError):
    error_code = ErrorCode.EVALUATION_NOT_FOUND
    message = "Evaluation not found."


class ReportNotFoundError(NotFoundError):
    error_code = ErrorCode.REPORT_NOT_FOUND
    message = "Report not found."


class HistoryNotFoundError(NotFoundError):
    error_code = ErrorCode.HISTORY_NOT_FOUND
    message = "History record not found."


# --------------------------------------------------------------------------- #
# Business rules / conflict (409)                                            #
# --------------------------------------------------------------------------- #
class ConflictError(AppException):
    status_code = 409
    error_code = ErrorCode.CONFLICT
    message = "The request conflicts with the current state of the resource."


class ProfileExistsError(ConflictError):
    error_code = ErrorCode.PROFILE_EXISTS
    message = "A candidate profile already exists for this user."


class AnswerAlreadyExistsError(ConflictError):
    error_code = ErrorCode.ANSWER_ALREADY_EXISTS
    message = "An answer has already been submitted for this question."


class InvalidInterviewStateError(ConflictError):
    error_code = ErrorCode.INVALID_INTERVIEW_STATE
    message = "The interview is not in a valid state for this operation."


class InterviewNotReadyError(ConflictError):
    error_code = ErrorCode.INTERVIEW_NOT_READY
    message = "The interview is not ready yet."


# --------------------------------------------------------------------------- #
# AI services (502 / 503 / 504)                                             #
# --------------------------------------------------------------------------- #
class AIServiceError(AppException):
    status_code = 502
    error_code = ErrorCode.LLM_UNAVAILABLE
    message = "The AI service is currently unavailable."


class LLMTimeoutError(AIServiceError):
    status_code = 504
    error_code = ErrorCode.LLM_TIMEOUT
    message = "The AI service did not respond within the timeout."


class PromptGenerationError(AIServiceError):
    error_code = ErrorCode.PROMPT_GENERATION_FAILED
    message = "Failed to generate interview content."


class EvaluationFailedError(AIServiceError):
    error_code = ErrorCode.EVALUATION_FAILED
    message = "Failed to evaluate the answer."


class TranscriptionFailedError(AIServiceError):
    error_code = ErrorCode.TRANSCRIPTION_FAILED
    message = "Failed to transcribe the audio."


class AIResponseInvalidError(AIServiceError):
    error_code = ErrorCode.AI_RESPONSE_INVALID
    message = "The AI service returned an invalid response."


# --------------------------------------------------------------------------- #
# Storage (400 / 413 / 415 / 503)                                           #
# --------------------------------------------------------------------------- #
class FileTooLargeError(AppException):
    status_code = 413
    error_code = ErrorCode.FILE_TOO_LARGE
    message = "The uploaded file exceeds the maximum allowed size."


class UnsupportedFileError(AppException):
    status_code = 415
    error_code = ErrorCode.UNSUPPORTED_FILE
    message = "The uploaded file type is not supported."


class FileUploadError(AppException):
    status_code = 500
    error_code = ErrorCode.FILE_UPLOAD_FAILED
    message = "The file could not be stored."


class StorageUnavailableError(AppException):
    status_code = 503
    error_code = ErrorCode.STORAGE_UNAVAILABLE
    message = "File storage is currently unavailable."


# --------------------------------------------------------------------------- #
# Database (500)                                                             #
# --------------------------------------------------------------------------- #
class DatabaseError(AppException):
    status_code = 500
    error_code = ErrorCode.DATABASE_ERROR
    message = "A database error occurred."


# --------------------------------------------------------------------------- #
# Infrastructure (503)                                                       #
# --------------------------------------------------------------------------- #
class ServiceUnavailableError(AppException):
    status_code = 503
    error_code = ErrorCode.SERVICE_UNAVAILABLE
    message = "One or more critical services are unavailable."
