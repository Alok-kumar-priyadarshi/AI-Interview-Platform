"""Resume text extraction.

Extracts plain text from supported resume formats (PDF, DOCX, TXT). Parsing
libraries are imported lazily so importing this module never requires them.
Unsupported formats raise :class:`UnsupportedFileError`.

Supported MIME types follow docs/02-tech-stack/backend-stack.md (PDF, DOCX, TXT).
"""

from __future__ import annotations

import io

from app.core.logging import get_logger
from app.exceptions.base import UnsupportedFileError

logger = get_logger(__name__)

PDF_MIME = "application/pdf"
DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
TXT_MIME = "text/plain"

SUPPORTED_MIME_TYPES: frozenset[str] = frozenset({PDF_MIME, DOCX_MIME, TXT_MIME})

_EXTENSION_MIME = {
    ".pdf": PDF_MIME,
    ".docx": DOCX_MIME,
    ".txt": TXT_MIME,
}


def resolve_mime_type(*, filename: str, declared: str | None) -> str:
    """Resolve the effective MIME type from the declared type or extension."""
    if declared in SUPPORTED_MIME_TYPES:
        return declared
    lower = filename.lower()
    for ext, mime in _EXTENSION_MIME.items():
        if lower.endswith(ext):
            return mime
    raise UnsupportedFileError("Only PDF, DOCX, and TXT resumes are supported.")


def extract_text(*, data: bytes, mime_type: str) -> str:
    """Return normalised plain text extracted from the file bytes."""
    if mime_type == PDF_MIME:
        text = _extract_pdf(data)
    elif mime_type == DOCX_MIME:
        text = _extract_docx(data)
    elif mime_type == TXT_MIME:
        text = data.decode("utf-8", errors="replace")
    else:
        raise UnsupportedFileError("Only PDF, DOCX, and TXT resumes are supported.")

    normalised = "\n".join(line.rstrip() for line in text.splitlines() if line.strip())
    return normalised.strip()


def _extract_pdf(data: bytes) -> str:
    import fitz  # PyMuPDF

    parts: list[str] = []
    with fitz.open(stream=data, filetype="pdf") as doc:
        for page in doc:
            parts.append(page.get_text())
    return "\n".join(parts)


def _extract_docx(data: bytes) -> str:
    import docx

    document = docx.Document(io.BytesIO(data))
    return "\n".join(paragraph.text for paragraph in document.paragraphs)
