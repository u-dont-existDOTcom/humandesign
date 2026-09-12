"""Synthetic contract tests, not evidence of LLM conversational effectiveness."""
from __future__ import annotations

import copy
import hashlib
from typing import Any

import pytest
from pydantic import ValidationError

from hdmatch.api.life_patterns_interview_methods import (
    INTERVIEW_OPENING,
    INTERVIEW_SYSTEM,
    PROCESS_POLICY,
    ClarificationNote,
    clarification_log,
    context_coverage,
    participant_statement_index,
    validate_clarification_sources,
)


def turn(identifier: str, role: str, text: Any, **extras: Any) -> dict[str, Any]:
    return {"turn_id": identifier, "role": role, "text": text, **extras}


def note(status: str = "open", source: str = "U1", gap: str = "GAP-period") -> dict[str, Any]:
    return {"gap_id": gap, "issue": "Period of the reported routine is unclear.",
            "status": status, "source_turn_ids": [source]}


def test_old_answer_retains_its_actual_preceding_question() -> None:
    turns = [turn("A1", "assistant", "Which period are you describing?"),
             turn("U1", "user", "The years in the first apartment.")]
    turns += [turn(f"X{i}", "assistant" if i % 2 == 0 else "user", str(i)) for i in range(30)]
    index = participant_statement_index(turns)
    assert index[0]["preceding_interviewer_turn"]["turn_id"] == "A1"
    assert index[0]["preceding_interviewer_turn"]["text"] == turns[0]["text"]
    assert index[0]["text"] == turns[1]["text"]


def test_unavailable_legacy_opener_is_not_reconstructed() -> None:
    index = participant_statement_index([turn("U1", "user", "Sometimes.")])
    assert index[0]["preceding_interviewer_turn"] is None


def test_consecutive_user_turns_share_preceding_not_invented_question() -> None:
    turns = [turn("A1", "assistant", "What happened next?"),
             turn("U1", "user", "I waited."), turn("U2", "user", "Then I left.")]
    rows = participant_statement_index(turns)
    assert [r["preceding_interviewer_turn"]["turn_id"] for r in rows] == ["A1", "A1"]


@pytest.mark.parametrize("length", [20, 1200, 1250, 1800, 6000])
def test_excerpt_exactness_offsets_and_hash(length: int) -> None:
    text = "  " + "é" * length + " a final qualification\n"
    row = participant_statement_index([turn("U1", "user", text)])[0]
    assert row["text"] == text[:1200]
    assert row["original_text_length"] == len(text)
    assert row["text_sha256"] == hashlib.sha256(text.encode()).hexdigest()
    if len(text) > 1200:
        start = row["tail_start_character"]
        assert start >= 1200
        assert row["text_tail"] == text[start:]
        assert len(row["text_tail"]) <= 400
        assert row["text_truncated"] is True
    else:
        assert row["text_tail"] == ""
        assert row["tail_start_character"] is None
        assert row["text_truncated"] is False


def test_context_bounds_report_omissions_without_altering_source() -> None:
    turns = [turn(f"U{i}", "user", f"answer {i}") for i in range(85)]
    before = copy.deepcopy(turns)
    index = participant_statement_index(turns)
    assert len(index) == 80
    assert index[0]["turn_id"] == "U5"
    assert context_coverage(turns, index)["participant_turns_omitted"] == 5
    assert turns == before


def test_empty_malformed_and_other_roles_do_not_become_participant_statements() -> None:
    turns = [turn("S", "system", "not evidence"), turn("A", "assistant", "Question?"),
             turn("U0", "user", " "), turn("U1", "user", None),
             turn("U2", "user", "yes")]
    assert len(participant_statement_index(turns)) == 1
    assert context_coverage(turns, participant_statement_index(turns))["participant_turns_total"] == 1


@pytest.mark.parametrize("status", ["open", "answered", "unknown", "declined", "not_asked_burden", "not_material"])
def test_dispositions_are_explicit_process_metadata(status: str) -> None:
    turns = [turn("U1", "user", "Source statement."),
             turn("A1", "assistant", "Reply.", clarification_notes=[note(status)])]
    log = clarification_log(turns)
    assert log["policy"] == PROCESS_POLICY
    assert log["items"][0]["status"] == status
    assert log["items"][0]["recorded_at_turn_id"] == "A1"


def test_latest_disposition_does_not_erase_old_note_or_resolve_other_gaps() -> None:
    turns = [turn("U1", "user", "I used to do this."),
             turn("A1", "assistant", "Around what period?", clarification_notes=[note()]),
             turn("U2", "user", "I do not remember."),
             turn("A2", "assistant", "We can leave that uncertain.",
                  clarification_notes=[note("unknown", "U2"), note(gap="GAP-context")])]
    before = copy.deepcopy(turns)
    log = clarification_log(turns)
    assert [(n["gap_id"], n["status"]) for n in log["items"]] == [
        ("GAP-period", "unknown"), ("GAP-context", "open")]
    assert turns == before
    assert turns[1]["clarification_notes"][0]["status"] == "open"


@pytest.mark.parametrize("source", ["invented", "A1", ""])
def test_unknown_assistant_and_empty_sources_are_rejected(source: str) -> None:
    turns = [turn("U1", "user", "Source"), turn("A1", "assistant", "Question")]
    with pytest.raises(ValueError):
        validate_clarification_sources((ClarificationNote.model_validate(note(source=source)),), turns)


def test_duplicate_gap_and_source_ids_rejected() -> None:
    n = ClarificationNote.model_validate(note())
    turns = [turn("U1", "user", "Source")]
    with pytest.raises(ValueError, match="duplicate clarification ID"):
        validate_clarification_sources((n, n), turns)
    duplicate = n.model_copy(update={"source_turn_ids": ("U1", "U1")})
    with pytest.raises(ValueError, match="duplicate clarification source"):
        validate_clarification_sources((duplicate,), turns)


def test_future_turn_does_not_retroactively_validate_an_old_note() -> None:
    turns = [turn("A1", "assistant", "Reply", clarification_notes=[note(source="U-later")]),
             turn("U-later", "user", "A later source")]
    log = clarification_log(turns)
    assert log["items"] == []
    assert log["invalid_note_count"] == 1


def test_invalid_bundle_is_flagged_not_silently_interpreted() -> None:
    turns = [turn("U1", "user", "Source"),
             turn("A1", "assistant", "Reply", clarification_notes=[note(), note()])]
    log = clarification_log(turns)
    assert log["items"] == []
    assert log["invalid_note_count"] == 2


def test_bounded_log_reports_omitted_items() -> None:
    turns = [turn("U1", "user", "Source"), turn("A1", "assistant", "Reply",
             clarification_notes=[note(gap=f"GAP-{i}") for i in range(3)])]
    log = clarification_log(turns, limit=2)
    assert len(log["items"]) == 2
    assert log["omitted_item_count"] == 1


def test_model_refuses_new_behavioral_or_diagnostic_fields() -> None:
    with pytest.raises(ValidationError):
        ClarificationNote.model_validate({**note(), "personality": "a trait"})
    with pytest.raises(ValidationError):
        ClarificationNote.model_validate(note("validated"))
    assert ClarificationNote.model_json_schema()["additionalProperties"] is False


def test_prompt_contract_is_neutral_and_keeps_methodological_limits() -> None:
    prompt = " ".join(INTERVIEW_SYSTEM.casefold().split())
    for phrase in ("pattern-first does not mean pattern-assuming", "material unresolved ambiguity",
                   "conditional claim", "participant-supplied", "not an enumerated count",
                   "model_reported_interview_process_not_behavioral_evidence"):
        assert phrase in prompt or phrase == PROCESS_POLICY
    for term in ("astrohd", "astrology", "human design", "mbti", "enneagram"):
        assert term not in prompt
        assert term not in INTERVIEW_OPENING.casefold()
    assert INTERVIEW_OPENING.count("?") == 1
    assert "do not force a dated incident" in INTERVIEW_SYSTEM
    assert "These are provisional interview" in INTERVIEW_SYSTEM


@pytest.mark.parametrize("kwargs", [{"max_turns": 0}, {"chars": 0}])
def test_invalid_context_limits_rejected(kwargs: dict[str, int]) -> None:
    with pytest.raises(ValueError):
        participant_statement_index([], **kwargs)
