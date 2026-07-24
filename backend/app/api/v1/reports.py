"""Report endpoints — see docs/05-api-design/reports.md.

PDF download is deferred in Version 1 (no PDF generation library is bundled);
``/download`` returns ``PDF_NOT_READY``. Full report content is available as
JSON via ``GET /reports/{report_id}``.
"""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response

from app.dependencies.auth import AdminUser, CurrentUser
from app.dependencies.evaluation import get_evaluation_service
from app.schemas.common import Page, SuccessResponse
from app.schemas.evaluation import StatusProgress
from app.schemas.report import InterviewReportRef, ReportDetail, ReportSummary
from app.services.evaluation_service import EvaluationService

router = APIRouter(tags=["Reports"])

ServiceDep = Annotated[EvaluationService, Depends(get_evaluation_service)]


@router.get("/reports", summary="List reports")
async def list_reports(
    user: CurrentUser,
    service: ServiceDep,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
) -> SuccessResponse[Page[ReportSummary]]:
    items, total = await service.list_reports(user, page=page, page_size=page_size)
    data = Page.create(
        [ReportSummary.from_model(r) for r in items],
        page=page,
        page_size=page_size,
        total=total,
    )
    return SuccessResponse(message="OK", data=data)


@router.get("/reports/{report_id}", summary="Get report details")
async def get_report(
    user: CurrentUser, service: ServiceDep, report_id: uuid.UUID
) -> SuccessResponse[ReportDetail]:
    report = await service.get_report(user, report_id)
    return SuccessResponse(message="OK", data=ReportDetail.from_model(report))


@router.get("/reports/{report_id}/status", summary="Get report status")
async def get_report_status(
    user: CurrentUser, service: ServiceDep, report_id: uuid.UUID
) -> SuccessResponse[StatusProgress]:
    await service.get_report(user, report_id)
    return SuccessResponse(message="OK", data=StatusProgress(status="ready", progress=100))


@router.get(
    "/reports/{report_id}/download",
    summary="Download report PDF",
    responses={200: {"content": {"application/pdf": {}}}},
)
async def download_report(
    user: CurrentUser, service: ServiceDep, report_id: uuid.UUID
) -> Response:
    pdf_bytes, filename = await service.get_report_pdf(user, report_id)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/interviews/{interview_id}/report", summary="Get interview report reference")
async def get_interview_report(
    user: CurrentUser, service: ServiceDep, interview_id: uuid.UUID
) -> SuccessResponse[InterviewReportRef]:
    report = await service.get_interview_report(user, interview_id)
    return SuccessResponse(
        message="OK", data=InterviewReportRef(report_id=report.id, status="ready")
    )


@router.post("/reports/{report_id}/regenerate", summary="Regenerate report (admin)")
async def regenerate_report(
    admin: AdminUser, service: ServiceDep, report_id: uuid.UUID
) -> SuccessResponse[None]:
    report = await service.reports.get(report_id)
    if report is not None:
        interview = await service.interviews.get(report.interview_id)
        if interview is not None:
            await service.reports.delete(report)
            await service.reports.flush()
            await service.run_for_interview(interview)
    return SuccessResponse(message="Report regeneration started.", data=None)
