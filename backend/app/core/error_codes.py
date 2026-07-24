"""Canonical catalogue of machine-readable error codes.

Error codes are part of the public API contract (see
``docs/05-api-design/errors.md``). Per that document they are **immutable once
released**: rename or remove a value only through a new API version. New codes
may be appended.
"""

from __future__ import annotations

from enum import StrEnum


class ErrorCode(StrEnum):
    # --- Authentication -----------------------------------------------------
    UNAUTHORIZED = "UNAUTHORIZED"
    INVALID_TOKEN = "INVALID_TOKEN"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    TOKEN_REVOKED = "TOKEN_REVOKED"
    LOGIN_REQUIRED = "LOGIN_REQUIRED"
    OAUTH_FAILED = "OAUTH_FAILED"

    # --- Authorization ------------------------------------------------------
    FORBIDDEN = "FORBIDDEN"
    INSUFFICIENT_PERMISSION = "INSUFFICIENT_PERMISSION"
    ADMIN_REQUIRED = "ADMIN_REQUIRED"

    # --- Validation ---------------------------------------------------------
    VALIDATION_ERROR = "VALIDATION_ERROR"

    # --- Resources ----------------------------------------------------------
    USER_NOT_FOUND = "USER_NOT_FOUND"
    PROFILE_NOT_FOUND = "PROFILE_NOT_FOUND"
    RESUME_NOT_FOUND = "RESUME_NOT_FOUND"
    INTERVIEW_NOT_FOUND = "INTERVIEW_NOT_FOUND"
    QUESTION_NOT_FOUND = "QUESTION_NOT_FOUND"
    ANSWER_NOT_FOUND = "ANSWER_NOT_FOUND"
    EVALUATION_NOT_FOUND = "EVALUATION_NOT_FOUND"
    REPORT_NOT_FOUND = "REPORT_NOT_FOUND"
    HISTORY_NOT_FOUND = "HISTORY_NOT_FOUND"

    # --- Business rules -----------------------------------------------------
    PROFILE_EXISTS = "PROFILE_EXISTS"
    ANSWER_ALREADY_EXISTS = "ANSWER_ALREADY_EXISTS"
    INTERVIEW_NOT_READY = "INTERVIEW_NOT_READY"
    INVALID_INTERVIEW_STATE = "INVALID_INTERVIEW_STATE"
    QUESTION_LOCKED = "QUESTION_LOCKED"
    PDF_NOT_READY = "PDF_NOT_READY"
    CONFLICT = "CONFLICT"

    # --- AI services --------------------------------------------------------
    LLM_TIMEOUT = "LLM_TIMEOUT"
    LLM_UNAVAILABLE = "LLM_UNAVAILABLE"
    PROMPT_GENERATION_FAILED = "PROMPT_GENERATION_FAILED"
    EVALUATION_FAILED = "EVALUATION_FAILED"
    TRANSCRIPTION_FAILED = "TRANSCRIPTION_FAILED"
    AI_RESPONSE_INVALID = "AI_RESPONSE_INVALID"

    # --- Database -----------------------------------------------------------
    DATABASE_ERROR = "DATABASE_ERROR"
    DATABASE_TIMEOUT = "DATABASE_TIMEOUT"
    TRANSACTION_FAILED = "TRANSACTION_FAILED"
    CONSTRAINT_VIOLATION = "CONSTRAINT_VIOLATION"

    # --- Storage ------------------------------------------------------------
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    UNSUPPORTED_FILE = "UNSUPPORTED_FILE"
    FILE_UPLOAD_FAILED = "FILE_UPLOAD_FAILED"
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    STORAGE_UNAVAILABLE = "STORAGE_UNAVAILABLE"

    # --- Rate limiting ------------------------------------------------------
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"

    # --- Infrastructure -----------------------------------------------------
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    DEPENDENCY_FAILURE = "DEPENDENCY_FAILURE"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
