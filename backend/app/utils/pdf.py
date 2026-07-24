"""Interview report PDF generation (reportlab).

Renders a :class:`~app.models.report.Report` into a self-contained PDF matching
the structure in docs/05-api-design/reports.md (summary → scores → strengths →
weaknesses → recommendations). ``reportlab`` is imported lazily so the module
loads without it in minimal environments.
"""

from __future__ import annotations

from io import BytesIO
from typing import Any

from app.utils.grading import grade_for


def build_report_pdf(report: Any, interview: Any) -> bytes:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        title="Interview Report",
    )

    styles = getSampleStyleSheet()
    brand = colors.HexColor("#1f47f5")
    h1 = ParagraphStyle("H1", parent=styles["Heading1"], textColor=brand, fontSize=20)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=13, spaceBefore=12)
    body = ParagraphStyle(
        "Body", parent=styles["Normal"], fontSize=10.5, leading=15, alignment=TA_LEFT
    )
    score = float(report.overall_score)

    flow: list[Any] = []
    flow.append(Paragraph("AI Career Interview — Report", h1))
    flow.append(Spacer(1, 4))
    flow.append(
        Paragraph(
            f"<b>{interview.target_role}</b> &nbsp;·&nbsp; {interview.difficulty} "
            f"&nbsp;·&nbsp; {interview.interview_type}",
            body,
        )
    )
    flow.append(
        HRFlowable(width="100%", color=colors.HexColor("#e2e8f0"), spaceBefore=8, spaceAfter=10)
    )

    flow.append(
        Paragraph(
            f"<b>Overall score:</b> {round(score)} / 100 &nbsp; "
            f"(<b>Grade {grade_for(score)}</b>) &nbsp; "
            f"<b>Recommendation:</b> {report.hiring_recommendation.replace('_', ' ')}",
            body,
        )
    )
    flow.append(Spacer(1, 8))

    flow.append(Paragraph("Executive summary", h2))
    flow.append(Paragraph(report.executive_summary, body))

    categories = {
        "Technical knowledge": report.technical_score,
        "Communication": report.communication_score,
        "Problem solving": report.problem_solving_score,
    }
    present = {k: v for k, v in categories.items() if v is not None}
    if present:
        flow.append(Paragraph("Category scores", h2))
        flow.append(
            _bullets([f"{name}: {round(float(v))} / 100" for name, v in present.items()], body)
        )

    if report.strengths:
        flow.append(Paragraph("Strengths", h2))
        flow.append(_bullets([str(s) for s in report.strengths], body))
    if report.weaknesses:
        flow.append(Paragraph("Areas to improve", h2))
        flow.append(_bullets([str(w) for w in report.weaknesses], body))

    recommendations = _roadmap_lines(report.improvement_roadmap or [])
    if recommendations:
        flow.append(Paragraph("Recommendations", h2))
        flow.append(_bullets(recommendations, body))

    def _footer(canvas: Any, _doc: Any) -> None:
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#94a3b8"))
        canvas.drawString(18 * mm, 12 * mm, "AI Career Interview Platform")
        canvas.restoreState()

    doc.build(flow, onFirstPage=_footer, onLaterPages=_footer)
    return buffer.getvalue()


def _bullets(items: list[str], style: Any) -> Any:
    from reportlab.platypus import ListFlowable, ListItem, Paragraph

    return ListFlowable(
        [ListItem(Paragraph(item, style), leftIndent=10) for item in items],
        bulletType="bullet",
        start="•",
    )


def _roadmap_lines(roadmap: list[dict]) -> list[str]:
    lines: list[str] = []
    for item in roadmap:
        if isinstance(item, dict):
            topic = item.get("topic")
            rec = item.get("recommendation", "")
            lines.append(f"<b>{topic}:</b> {rec}" if topic else str(rec))
        else:
            lines.append(str(item))
    return lines
