from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path

import pytest

from hdmatch.relationship.phenotype_classifier import OpenAIRelationshipPhenotypeClassifier


def _answer_record() -> list[dict[str, object]]:
    return [
        {
            "question_id": "RRQ_LOVE_EROS_DIRECTION",
            "fields": [
                {
                    "field_id": "a_physical_attraction",
                    "status": "clear",
                    "answer": "I was extremely physically attracted to them from the beginning.",
                    "clarification": "",
                }
            ],
        }
    ]


def _semantic_audit() -> dict[str, object]:
    return {"audit_version": "test-audit", "queue": [], "answers": []}


def _provider_response(*, evidence: str) -> bytes:
    content = json.dumps(
        {
            "question_results": [
                {
                    "question_id": "RRQ_LOVE_EROS_DIRECTION",
                    "axis_results": [
                        {
                            "axis_id": "physical_attraction",
                            "direction": "a_to_b",
                            "status": "classified",
                            "ordinal_value": "very_high",
                            "trajectory": "stable",
                            "confidence": 0.94,
                            "evidence_spans": [evidence],
                            "counterevidence_spans": [],
                            "context_conditions": [],
                            "observability_limits": [],
                            "forced_choice": False,
                        }
                    ],
                    "applicability_flags": [],
                    "unresolved_axis_ids": [],
                    "verbatim_preserved": True,
                }
            ]
        }
    )
    return json.dumps(
        {
            "output": [
                {
                    "type": "message",
                    "content": [{"type": "output_text", "text": content}],
                }
            ]
        }
    ).encode()


def test_classifier_is_chart_blind_and_freezes_literal_evidence() -> None:
    captured: dict[str, object] = {}

    def transport(url: str, body: bytes, headers: Mapping[str, str], timeout: float) -> bytes:
        captured["url"] = url
        captured["body"] = json.loads(body.decode())
        captured["headers"] = dict(headers)
        captured["timeout"] = timeout
        return _provider_response(evidence="extremely physically attracted")

    classifier = OpenAIRelationshipPhenotypeClassifier(
        api_key="test-key",
        model="gpt-test",
        transport=transport,
    )
    freeze = classifier.classify_and_freeze(
        session_id="RR-TEST",
        answers=_answer_record(),
        semantic_audit=_semantic_audit(),
        questionnaire_path=Path("reference/relationship/relationship_dynamic_questionnaire_v1.json"),
        rubric_path=Path("reference/relationship/relationship_outcome_rubrics_v1.json"),
        protocol_path=Path("reference/relationship/relationship_blind_classifier_protocol_v1.json"),
    )
    request_body = captured["body"]
    assert isinstance(request_body, dict)
    serialized = json.dumps(request_body)
    assert "I was extremely physically attracted" in serialized
    assert "SECRET_BIRTH_SENTINEL" not in serialized
    assert "SECRET_PREDICTION_SENTINEL" not in serialized
    assert request_body["store"] is False
    assert freeze.output.question_results[0].axis_results[0].ordinal_value == "very_high"
    assert len(freeze.freeze_sha256) == 64


def test_classifier_rejects_hallucinated_evidence_span() -> None:
    def transport(url: str, body: bytes, headers: Mapping[str, str], timeout: float) -> bytes:
        return _provider_response(evidence="They told me I was the hottest person alive")

    classifier = OpenAIRelationshipPhenotypeClassifier(
        api_key="test-key",
        model="gpt-test",
        transport=transport,
    )
    with pytest.raises(ValueError, match="not present verbatim"):
        classifier.classify_and_freeze(
            session_id="RR-TEST",
            answers=_answer_record(),
            semantic_audit=_semantic_audit(),
            questionnaire_path=Path(
                "reference/relationship/relationship_dynamic_questionnaire_v1.json"
            ),
            rubric_path=Path("reference/relationship/relationship_outcome_rubrics_v1.json"),
            protocol_path=Path(
                "reference/relationship/relationship_blind_classifier_protocol_v1.json"
            ),
        )
