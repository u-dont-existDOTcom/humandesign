# ruff: noqa: E501
"""Participant-facing framing for the direct-OpenAI relationship research pilot."""

from __future__ import annotations

from hdmatch.api.relationship_adaptive_ui import HTML as BASE_HTML


def _replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        raise RuntimeError(f"expected UI fragment not found: {old[:80]!r}")
    return text.replace(old, new, 1)


HTML = BASE_HTML
HTML = _replace_once(
    HTML, "<title>Relationship X-Ray</title>", "<title>Relationship Pattern Lab</title>"
)
HTML = _replace_once(
    HTML,
    "<h1>Relationship X-Ray</h1>\n"
    "<p>Six finite sections map one relationship before any astrology or Human Design result is shown. Each distinction has its own field. After the core, the AI auditor may ask at most six targeted clarifications.</p>",
    "<h1>Relationship Pattern Lab</h1>\n"
    "<p><strong>A blind astrology &amp; Human Design relationship study.</strong></p>\n"
    "<p>First, this survey builds a structured map of one real relationship: attraction, love, sex, communication, conflict, autonomy, practical fit, and how those changed over time. That map is useful on its own because it separates relationship dynamics that are easy to blur together when you judge a relationship globally.</p>\n"
    "<p>Then your answers are frozen before any astrology or Human Design prediction is revealed. You will be able to inspect the exact developmental signals frozen before your answers and compare them with the chart-blind relationship description. The current raw AstroRRF signals are not yet calibrated as high/low or formal hits/misses, so the study shows them without inventing those labels after seeing your relationship. Across many participants, the scientific question is whether these systems predict real relationship dynamics with out-of-sample specificity rather than producing generic descriptions after the fact.</p>\n"
    "<p>If the system eventually proves predictive across blinded cases, the longer-term goal is practical: it could become useful for comparing other relationships and, eventually, for prospectively checking likely relationship dynamics before much history exists. This study is testing that possibility, not assuming it.</p>\n"
    "<p>There are six finite sections, followed by at most six targeted AI clarifications.</p>",
)
HTML = _replace_once(
    HTML,
    "I consent to these questionnaire answers being sent to OpenRouter and its selected model provider for answer-quality and clarification analysis. Birth/chart data are not sent to this auditor.",
    "I consent to these questionnaire answers being sent to OpenAI's API for answer-quality and clarification analysis. Birth/chart data and Astro/HD predictions are not sent to this auditor.",
)
HTML = _replace_once(
    HTML,
    "I consent to sending this frozen survey's questionnaire answers to OpenRouter/the selected model provider for a separate LLM audit addendum.",
    "I consent to sending this frozen survey's questionnaire answers to OpenAI's API for a separate LLM audit addendum.",
)
