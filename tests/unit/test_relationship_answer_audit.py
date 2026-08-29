from __future__ import annotations

import json
from pathlib import Path

from hdmatch.api.relationship_adaptive_app import create_relationship_adaptive_app_from_env
from hdmatch.relationship.answer_audit import (
    FieldEvidence,
    assess_field_answer,
    build_clarification_queue,
    legacy_clarification_queue,
)


def test_explicit_unknown_is_complete() -> None:
    quality = assess_field_answer("b_eros_in_love", "unknown", "")
    assert quality.score == 100
    assert quality.band == "explicit_unknown"
    assert not quality.needs_clarification


def test_love_does_not_satisfy_eros_without_romantic_evidence() -> None:
    quality = assess_field_answer(
        "b_eros_in_love",
        "clear",
        "She loved me deeply and cared about me for years.",
    )
    assert "love_eros_conflation" in quality.ambiguity_codes
    assert quality.needs_clarification


def test_clear_answer_with_context_words_is_rechecked() -> None:
    quality = assess_field_answer(
        "internal_emotional_ease",
        "clear",
        "It was easy when we lived apart but changed after we moved in together.",
    )
    assert "hidden_context_dependence" in quality.ambiguity_codes


def test_partner_internal_state_requires_evidence_when_weak() -> None:
    quality = assess_field_answer(
        "b_physical_attraction",
        "clear",
        "I think probably high.",
    )
    assert "partner_evidence_weak" in quality.ambiguity_codes


def test_clarification_queue_is_bounded() -> None:
    evidence = tuple(
        FieldEvidence(
            question_id="RRQ_LOVE_EROS_DIRECTION",
            field_id=field_id,
            status="clear",
            answer="good",
        )
        for field_id in (
            "a_eros_in_love",
            "b_eros_in_love",
            "b_physical_attraction",
            "a_baseline_libido",
            "b_baseline_libido",
            "intellectual_stimulation",
            "communication_quality",
            "visible_drama",
        )
    )
    queue = build_clarification_queue(evidence, max_items=3)
    assert len(queue) == 3
    assert len({item.id for item in queue}) == 3


def test_legacy_queue_asks_direct_v2_field_question() -> None:
    queue = legacy_clarification_queue(
        {"RRQ_LOVE_EROS_DIRECTION": "We loved each other."},
        field_questions={
            "b_eros_in_love": (
                "RRQ_LOVE_EROS_DIRECTION",
                "As best you could tell, how romantically in love were they with you?",
            )
        },
        max_items=8,
    )
    assert len(queue) == 1
    assert "romantically in love" in queue[0].prompt


def test_v2_registry_has_single_construct_fields() -> None:
    payload = json.loads(
        Path("reference/relationship/relationship_guided_response_fields_v2.json").read_text(
            encoding="utf-8"
        )
    )
    fields = [
        field
        for question in payload["questions"].values()
        for field in question["fields"]
    ]
    ids = [field["id"] for field in fields]
    assert len(ids) == 42
    assert len(ids) == len(set(ids))
    assert "a_to_b_attraction_eros" not in ids
    assert "a_sexual_desire_libido" not in ids
    assert "communication_commonality" not in ids
    assert "drama_conflict" not in ids


def test_adaptive_app_factory_exposes_quality_and_audit_routes(
    tmp_path: Path, monkeypatch: object
) -> None:
    monkeypatch.setenv("HDMATCH_RELATIONSHIP_STORE", str(tmp_path))  # type: ignore[attr-defined]
    monkeypatch.setenv(  # type: ignore[attr-defined]
        "HDMATCH_RELATIONSHIP_GUIDED_FIELDS",
        "reference/relationship/relationship_guided_response_fields_v2.json",
    )
    app = create_relationship_adaptive_app_from_env()
    paths = {getattr(route, "path", "") for route in app.routes}
    assert "/api/quality" in paths
    assert "/api/adaptive/sessions" in paths
    assert "/api/sessions/{session_id}/semantic-audit" in paths
