from pathlib import Path

import pytest
from fastapi import HTTPException

from hdmatch.api.relationship_public_app import (
    GuidedFieldAnswerRequest,
    _clean_field_answers,
    _legacy_session,
    _load_guided_registry,
)
from hdmatch.relationship.questionnaire import load_relationship_questionnaire


QUESTIONNAIRE_PATH = Path("reference/relationship/relationship_dynamic_questionnaire_v1.json")
GUIDED_PATH = Path("reference/relationship/relationship_guided_response_fields_v1.json")


def _registry():
    spec = load_relationship_questionnaire(QUESTIONNAIRE_PATH)
    return _load_guided_registry(GUIDED_PATH, spec), spec


def test_guided_registry_covers_all_core_domains_with_multiple_fields() -> None:
    registry, spec = _registry()
    assert set(registry.questions) == set(spec.core_question_ids)
    assert sum(len(question.fields) for question in registry.questions.values()) == 24
    assert all(len(question.fields) >= 3 for question in registry.questions.values())


def test_mixed_field_requires_explicit_clarification() -> None:
    registry, _ = _registry()
    question = registry.questions["RRQ_TRAJECTORY_CONTEXT"]
    supplied = tuple(
        GuidedFieldAnswerRequest(
            field_id=field.id,
            status="mixed" if index == 0 else "unknown",
            answer="Two different phases" if index == 0 else "",
            clarification="" if index == 0 else "",
        )
        for index, field in enumerate(question.fields)
    )
    with pytest.raises(HTTPException) as exc:
        _clean_field_answers(question, supplied)
    assert exc.value.status_code == 422
    assert "clarify" in str(exc.value.detail).lower()


def test_unknown_and_not_applicable_can_remain_without_narrative() -> None:
    registry, _ = _registry()
    question = registry.questions["RRQ_TRAJECTORY_CONTEXT"]
    statuses = ("unknown", "not_applicable", "clear")
    supplied = tuple(
        GuidedFieldAnswerRequest(
            field_id=field.id,
            status=statuses[index],
            answer="Known transition" if statuses[index] == "clear" else "",
        )
        for index, field in enumerate(question.fields)
    )
    cleaned = _clean_field_answers(question, supplied)
    assert cleaned[0]["status"] == "unknown"
    assert cleaned[0]["answer"] == ""
    assert cleaned[1]["status"] == "not_applicable"
    assert cleaned[2]["answer"] == "Known transition"


def test_exactly_one_response_is_required_for_every_field() -> None:
    registry, _ = _registry()
    question = registry.questions["RRQ_LOVE_EROS_DIRECTION"]
    supplied = (
        GuidedFieldAnswerRequest(
            field_id=question.fields[0].id,
            status="clear",
            answer="High attraction",
        ),
    )
    with pytest.raises(HTTPException) as exc:
        _clean_field_answers(question, supplied)
    assert exc.value.status_code == 422


def test_old_single_textarea_session_is_detected_as_legacy() -> None:
    assert _legacy_session(
        {
            "answers": [
                {"question_id": "RRQ_TRAJECTORY_CONTEXT", "answer": "old narrative"}
            ]
        }
    )
    assert not _legacy_session(
        {
            "answers": [
                {
                    "question_id": "RRQ_TRAJECTORY_CONTEXT",
                    "fields": [
                        {
                            "field_id": "timeline_exposure",
                            "status": "clear",
                            "answer": "known",
                            "clarification": "",
                        }
                    ],
                }
            ]
        }
    )
