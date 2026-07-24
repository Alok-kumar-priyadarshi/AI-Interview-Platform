"""Resume service.

Owns the resume lifecycle: validation, storage, text extraction, AI candidate-
profile generation, and ownership-checked retrieval/deletion.

Version 1 processes resumes **synchronously** within the upload request: the
platform excludes background workers (Celery) in v1, so parsing + AI analysis
run inline and the response reflects the terminal processing status. Moving to
queued async processing is a future enhancement (docs note the worker pipeline).
"""

from __future__ import annotations

import hashlib
import uuid
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.service import AIService
from app.core.config import get_settings
from app.core.logging import get_logger
from app.exceptions.base import (
    AppException,
    ConflictError,
    FileTooLargeError,
    ResumeNotFoundError,
    UnsupportedFileError,
)
from app.models.candidate_profile import CandidateProfile
from app.models.enums import AuditEventType, ExtractionStatus, ProcessingStatus
from app.models.resume import Resume
from app.models.user import User
from app.repositories.resume_repository import CandidateProfileRepository, ResumeRepository
from app.services.audit_service import AuditService
from app.services.storage import StorageProvider
from app.utils.text_extraction import extract_text, resolve_mime_type

logger = get_logger(__name__)

MAX_RESUMES_PER_USER = 10
_PROGRESS = {
    ProcessingStatus.PENDING: 0,
    ProcessingStatus.PROCESSING: 50,
    ProcessingStatus.COMPLETED: 100,
    ProcessingStatus.FAILED: 100,
}
_EXTENSION = {
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "text/plain": ".txt",
}


class ResumeService:
    def __init__(
        self, session: AsyncSession, storage: StorageProvider, ai_service: AIService
    ) -> None:
        self.session = session
        self.storage = storage
        self.ai = ai_service
        self.resumes = ResumeRepository(session)
        self.profiles = CandidateProfileRepository(session)
        self.audit = AuditService(session)

    # ------------------------------------------------------------------ #
    # Upload                                                             #
    # ------------------------------------------------------------------ #
    async def upload(
        self, user: User, *, filename: str, content_type: str | None, data: bytes
    ) -> Resume:
        settings = get_settings()
        if not data:
            raise UnsupportedFileError("The uploaded file is empty.")
        if len(data) > settings.MAX_UPLOAD_SIZE_BYTES:
            raise FileTooLargeError("Maximum file size is 10 MB.")

        mime = resolve_mime_type(filename=filename, declared=content_type)

        if await self.resumes.count_by_user(user.id) >= MAX_RESUMES_PER_USER:
            raise ConflictError(f"A maximum of {MAX_RESUMES_PER_USER} resumes is allowed.")

        checksum = hashlib.sha256(data).hexdigest()
        if await self.resumes.get_by_checksum(user.id, checksum):
            raise ConflictError("This resume has already been uploaded.")

        stored_filename = f"{uuid.uuid4()}{_EXTENSION.get(mime, '')}"
        key = f"resumes/{user.id}/{stored_filename}"
        storage_path = await self.storage.save(key=key, data=data, content_type=mime)

        is_first = await self.resumes.count_by_user(user.id) == 0
        resume = Resume(
            user_id=user.id,
            original_filename=filename[:255],
            stored_filename=stored_filename,
            storage_path=storage_path,
            mime_type=mime,
            file_size_bytes=len(data),
            checksum_sha256=checksum,
            processing_status=ProcessingStatus.PENDING,
            is_default=is_first,
        )
        self.resumes.add(resume)
        await self.resumes.flush()

        await self._process(resume, data=data, mime=mime)

        await self.audit.log(
            event_type=AuditEventType.RESUME_UPLOAD,
            action="UPLOAD_RESUME",
            user_id=user.id,
            resource_type="resume",
            resource_id=resume.id,
            metadata={"status": resume.processing_status},
        )
        return resume

    async def _process(self, resume: Resume, *, data: bytes, mime: str) -> None:
        """Extract text and generate the AI candidate profile (best-effort).

        Failures mark the resume ``failed`` rather than raising, so the resume
        record persists and the user can inspect the status and retry.
        """
        resume.processing_status = ProcessingStatus.PROCESSING
        resume.processing_started_at = datetime.now(UTC)
        await self.resumes.flush()

        try:
            text = extract_text(data=data, mime_type=mime)
            if not text:
                raise AppException("No extractable text found in the resume.")

            analysis, meta = await self.ai.analyze_resume(text)
            profile = CandidateProfile(
                resume_id=resume.id,
                professional_summary=analysis.professional_summary,
                total_experience_years=analysis.total_experience_years,
                highest_education=analysis.highest_education,
                current_job_title=analysis.current_job_title,
                current_company=analysis.current_company,
                skills=analysis.skills,
                education=analysis.education,
                experience=analysis.experience,
                projects=analysis.projects,
                certifications=analysis.certifications,
                languages=analysis.languages,
                ai_confidence_score=analysis.ai_confidence_score,
                ai_model_version=meta.model,
                extraction_status=ExtractionStatus.COMPLETED,
            )
            self.profiles.add(profile)
            resume.processing_status = ProcessingStatus.COMPLETED
            resume.ai_model_version = meta.model
            resume.processing_completed_at = datetime.now(UTC)
            logger.info("resume_processed", extra={"resume_id": str(resume.id)})
        except Exception:
            resume.processing_status = ProcessingStatus.FAILED
            resume.processing_completed_at = datetime.now(UTC)
            logger.exception("resume_processing_failed", extra={"resume_id": str(resume.id)})
        finally:
            await self.resumes.flush()

    # ------------------------------------------------------------------ #
    # Retrieval / mutation                                               #
    # ------------------------------------------------------------------ #
    async def list_for_user(self, user_id: uuid.UUID) -> list[Resume]:
        return await self.resumes.list_by_user(user_id)

    async def get_owned(self, user: User, resume_id: uuid.UUID) -> Resume:
        resume = await self.resumes.get(resume_id)
        if resume is None or resume.user_id != user.id:
            raise ResumeNotFoundError()
        return resume

    async def get_metadata(self, user: User, resume_id: uuid.UUID) -> CandidateProfile:
        await self.get_owned(user, resume_id)
        profile = await self.profiles.get_by_resume_id(resume_id)
        if profile is None:
            raise ResumeNotFoundError("Resume has not been processed yet.")
        return profile

    def progress_for(self, resume: Resume) -> int:
        return _PROGRESS.get(ProcessingStatus(resume.processing_status), 0)

    async def set_default(self, user: User, resume_id: uuid.UUID) -> Resume:
        resume = await self.get_owned(user, resume_id)
        await self.resumes.clear_default(user.id)
        resume.is_default = True
        await self.resumes.flush()
        return resume

    async def delete(self, user: User, resume_id: uuid.UUID) -> None:
        resume = await self.get_owned(user, resume_id)
        key = resume.storage_path.split("://", 1)[-1]
        if resume.storage_path.startswith("s3://"):
            key = key.split("/", 1)[-1]  # strip bucket from s3://bucket/key
        try:
            await self.storage.delete(key=key)
        except Exception:  # pragma: no cover - storage cleanup is best-effort
            logger.warning("resume_file_delete_failed", extra={"resume_id": str(resume.id)})
        await self.resumes.delete(resume)
        await self.resumes.flush()
        await self.audit.log(
            event_type=AuditEventType.RESUME_UPLOAD,
            action="DELETE_RESUME",
            user_id=user.id,
            resource_type="resume",
            resource_id=resume_id,
        )
