"""Score → letter grade mapping (docs/05-api-design/evaluations.md — Grade Mapping)."""

from __future__ import annotations


def grade_for(score: float | None) -> str:
    """Map a 0–100 score to a letter grade."""
    if score is None:
        return "N/A"
    if score >= 90:
        return "A+"
    if score >= 80:
        return "A"
    if score >= 70:
        return "B"
    if score >= 60:
        return "C"
    return "D"
