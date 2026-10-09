"""Researcher-only question-quality feedback; never behavioral evidence or public data.

Only explicitly identified interview criticism is collected. A conservative
phrase detector catches untagged objections in the exact consented source; its
classification is a suggestion for the researcher, not an instrument verdict.
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Iterable
from typing import Any

from .domain import resolved_turn_route_id

# Narrow user-addressed objections, not everyday uncertainty or "it depends".
_DIRECT_COMPLAINT = re.compile(
    r"(?:why (?:are )?you ask(?:ing)? (?:me )?(?:this|that)|"
    r"what(?:'s| is) the point of (?:this|that|the) question|"
    r"(?:i(?:'ve| have) )?already answered (?:this|that)|"
    r"(?:you(?:'ve| have) )?already ask(?:ed)? (?:this|that)|"
    r"(?:this|that) question (?:is|was|seems|doesn't|does not) (?:obvious|silly|dumb|unclear|confusing|redundant|pointless|ill[- ]posed|too vague)|"
    r"(?:i (?:don't|do not|can't|cannot) understand (?:this|that|the) question)|"
    r"(?:fix|rephrase|change) (?:this|that|the) question|"
    r"(?:you(?:'re| are) )?repeating (?:this|that|the) question)",
    re.I,
)


# A respondent asking whether their *own answer* is normal is not thereby
# criticizing question wording, duplication or psychometric usefulness.
_RESPONSE_NORMALITY = re.compile(
    r"^\s*(?:is(?:n['’]t| not)? (?:that|this|it) (?:pretty |quite )?normal|"
    r"is (?:my|that) (?:response|reaction|answer) normal|"
    r"(?:doesn't|does not) (?:everyone|most people) (?:do|feel|think) that)"
    r"\s*[?!.]*\s*$",
    re.I,
)
# Model-derived snippets require literal evidence of a question-design target.
# Non-explicit snippets remain inspectable as context, not improvement tasks.
_DESIGN_REFERENT = re.compile(
    r"\b(?:questions?|ask(?:ing|ed)?|re[ -]?ask(?:ing|ed)?|repeat(?:ed|ing)?|"
    r"already (?:answered|told|explained)|i just told you|you just asked|"
    r"not enough (?:context|detail|information)|ambiguous|under[- ]specified)\b",
    re.I,
)


def feedback_actionability(item: dict[str, Any]) -> str:
    """Conservative distinction between instrument objections and conversational asides."""

    quote = str(item.get("feedback_text") or "").strip()
    if _RESPONSE_NORMALITY.fullmatch(quote):
        return "context_only_normality_question"
    if item.get("source_type") == "review_derived" and not _DESIGN_REFERENT.search(quote):
        return "context_only_unanchored_model_inference"
    return "possible_question_design_issue"


def feedback_issue(text: str) -> str:
    """Triage hint only; do not infer a personality property."""

    value = text.casefold()
    if any(
        x in value
        for x in ("repeat", "already ask", "already answer", "redundant", "same question")
    ):
        return "redundant"
    if any(
        x in value for x in ("unclear", "confus", "understand", "vague", "ill-posed", "mean by")
    ):
        return "unclear"
    if any(
        x in value
        for x in ("obvious", "pointless", "silly", "dumb", "what's the point", "what is the point")
    ):
        return "low_information"
    if any(
        x in value
        for x in ("depends on", "not enough detail", "not enough information", "missing context")
    ):
        return "missing_context"
    return "other"


def _explicit_feedback_parts(value: Any) -> Iterable[str]:
    if isinstance(value, str) and value.strip():
        yield value.strip()
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, str) and item.strip():
                yield item.strip()
            elif isinstance(item, dict):
                for key in ("quote", "text", "feedback", "comment"):
                    if isinstance(item.get(key), str) and item[key].strip():
                        yield item[key].strip()
                        break


def _meaningful_synthetic(record: dict[str, Any]) -> bool:
    return "synthetic" in str(record.get("evidence_authority", "")).casefold() or bool(
        record.get("synthetic_only")
    )


def collect_feedback(
    record: dict[str, Any], *, source_type: str, source_id: str, observed_at: float | None = None
) -> list[dict[str, Any]]:
    """Extract exact tagged feedback and conservative candidate objections from a consented source."""

    if record.get("consent", {}).get("research_use_consented") is not True or _meaningful_synthetic(
        record
    ):
        return []
    entries: list[dict[str, Any]] = []
    seen = set()
    turns = record.get("turns") or []
    if not isinstance(turns, list):
        return []
    for index, turn in enumerate(turns):
        if not isinstance(turn, dict):
            continue
        turn_id = str(turn.get("turn_id") or f"turn-index-{index}")
        route = resolved_turn_route_id(turn) or str(turn.get("canonical_question_id") or "unmapped")
        question = str(turn.get("question_text") or "")
        parts: list[tuple[str, str]] = []
        for field in ("process_feedback", "derived_process_feedback"):
            parts.extend((part, field) for part in _explicit_feedback_parts(turn.get(field)))
        original = turn.get("answer_text")
        if (
            isinstance(original, str)
            and not turn.get("_skip_auto_answer_scan")
            and _DIRECT_COMPLAINT.search(original)
        ):
            parts.append((original.strip(), "explicit_objection_in_answer"))
        for part, evidence_source in parts:
            # De-duplicate a tagged objection also present verbatim in the answer.
            signature = part.casefold().strip()
            unique_key = (turn_id, signature)
            if not signature or unique_key in seen:
                continue
            seen.add(unique_key)
            event_key = f"{source_type}|{source_id}|{turn_id}|{index}|{signature}"
            feedback_id = "F-" + hashlib.sha256(event_key.encode()).hexdigest()[:24]
            entries.append(
                {
                    "feedback_id": feedback_id,
                    "route_id": route,
                    "question_text": question[:2000],
                    "feedback_text": part[:1200],
                    "feedback_truncated": len(part) > 1200,
                    "issue_hint": feedback_issue(part),
                    "capture_method": evidence_source,
                    "source_type": source_type,
                    "source_id": source_id,
                    "turn_id": turn_id,
                    "observed_at_unix": observed_at,
                    "recorded_answer_context": (original or "")[:5000]
                    if isinstance(original, str) else "",
                    "answer_context_truncated": isinstance(original, str) and len(original) > 5000,
                    "provenance_label": (
                        "Reviewer-extracted phrase (not a separately recorded reply)"
                        if source_type == "review_derived"
                        else "Explicit source annotation"
                        if evidence_source in {"process_feedback", "derived_process_feedback"}
                        else "Explicit critique within answer"
                    ),
                }
            )
    return entries


def researcher_feedback_overview(store: Any) -> dict[str, Any]:
    """Read consenting, encrypted source for the researcher; never a public API."""

    from collections import Counter

    with store.connection() as db:
        reviews = db.execute(
            "SELECT id,created,payload FROM gpt_review_jobs ORDER BY created DESC"
        ).fetchall()
        submissions = db.execute(
            "SELECT id,created,payload FROM gpt_submissions ORDER BY created DESC"
        ).fetchall()
        sessions = db.execute(
            "SELECT id,created,payload FROM sessions ORDER BY created DESC"
        ).fetchall()
    found: dict[str, dict[str, Any]] = {}
    for review_id, created, raw in reviews:
        record = store.decode(raw)
        candidate = record.get("candidate_record") or {}
        if (
            record.get("status") == "withdrawn"
            or candidate.get("consent", {}).get("research_use_consented") is not True
            or _meaningful_synthetic(candidate)
        ):
            continue
        for item in collect_feedback(
            candidate,
            source_type="review_record",
            source_id=review_id,
            observed_at=created,
        ):
            found.setdefault(item["feedback_id"], item)
        for index, answer in enumerate(record.get("clarification_history") or []):
            if not isinstance(answer, dict):
                continue
            clarification = {
                "consent": {"research_use_consented": True},
                "turns": [
                    {
                        "turn_id": f"clarification-{index:04d}",
                        "canonical_question_id": answer.get("route_id"),
                        "question_text": answer.get("question_text"),
                        "answer_text": answer.get("answer_text"),
                    }
                ],
            }
            for item in collect_feedback(
                clarification,
                source_type="review_clarification",
                source_id=review_id,
                observed_at=answer.get("answered_at_unix") or created,
            ):
                found.setdefault(item["feedback_id"], item)
        # The independent reviewer may extract an exact process-feedback quote
        # from an otherwise ordinary-looking answer. Admit only its explicitly
        # separate derived feedback, not the answer as inferred personality data.
        worker = record.get("worker_state") or {}
        for turn in worker.get("turns") or []:
            if not isinstance(turn, dict) or not turn.get("derived_process_feedback"):
                continue
            pseudo = {
                "consent": {"research_use_consented": True},
                "turns": [
                    {
                        "turn_id": turn.get("turn_id"),
                        "canonical_question_id": turn.get("canonical_question_id"),
                        "question_text": turn.get("question_text"),
                        "answer_text": turn.get("answer_text"),
                        "_skip_auto_answer_scan": True,
                        "derived_process_feedback": turn["derived_process_feedback"],
                    }
                ],
            }
            for item in collect_feedback(
                pseudo,
                source_type="review_derived",
                source_id=review_id,
                observed_at=created,
            ):
                if not any(
                    other["source_id"] == review_id
                    and other["route_id"] == item["route_id"]
                    and other["feedback_text"].casefold() == item["feedback_text"].casefold()
                    for other in found.values()
                ):
                    found.setdefault(item["feedback_id"], item)
    for submission_id, created, raw in submissions:
        payload = store.decode(raw)
        source_id = payload.get("review_id") or submission_id
        for item in collect_feedback(
            payload.get("primary_record") or {},
            source_type="review_record" if payload.get("review_id") else "submission_record",
            source_id=source_id,
            observed_at=created,
        ):
            found.setdefault(item["feedback_id"], item)
    for session_id, created, raw in sessions:
        state = store.decode(raw)
        if state.get("consent") is not True:
            continue
        pseudo = {
            "consent": {"research_use_consented": True},
            "turns": state.get("turns") or [],
        }
        for item in collect_feedback(
            pseudo,
            source_type="railway_session",
            source_id=session_id,
            observed_at=created,
        ):
            found.setdefault(item["feedback_id"], item)
    contextual_notes = []
    possible_issues = []
    for item in found.values():
        item["feedback_actionability"] = feedback_actionability(item)
        if item["feedback_actionability"].startswith("context_only_"):
            contextual_notes.append(item)
        else:
            possible_issues.append(item)
    dispositions = store.question_feedback_dispositions()
    for feedback in possible_issues:
        feedback.update(dispositions.get(feedback["feedback_id"], {
            "status": "new", "revision_id": "",
        }))
    ordered = sorted(
        possible_issues,
        key=lambda row: float(row.get("observed_at_unix") or 0),
        reverse=True,
    )
    contextual_notes.sort(
        key=lambda row: float(row.get("observed_at_unix") or 0), reverse=True
    )
    return {
        "total": len(ordered),
        "contextual_notes_count": len(contextual_notes),
        "contextual_notes": contextual_notes,
        "by_route": dict(Counter(row["route_id"] for row in ordered).most_common()),
        "by_issue_hint": dict(Counter(row["issue_hint"] for row in ordered)),
        "feedback": ordered,
        "visibility": "researcher_authenticated_only",
        "auto_applies_question_changes": False,
    }
