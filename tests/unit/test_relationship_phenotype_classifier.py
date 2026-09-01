from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path

import pytest

from hdmatch.relationship.phenotype import (
    VALIDATION_CONTRACT_SHA256,
    VALIDATION_CONTRACT_VERSION,
    QuestionPhenotype,
    RelationshipPhenotypeFreeze,
    RelationshipPhenotypeOutput,
    calibration_phenotype_observations,
    canonical_sha256,
    source_text_corpus,
)
from hdmatch.relationship.phenotype_classifier import OpenAIRelationshipPhenotypeClassifier
from hdmatch.relationship.reveal import relationship_fingerprint


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


def _provider_response(
    *,
    evidence: str,
    axis_id: str = "physical_attraction",
    direction: str = "a_to_b",
    duplicate: bool = False,
) -> bytes:
    axis = {
        "axis_id": axis_id,
        "direction": direction,
        "status": "classified",
        "ordinal_value": "very_high",
        "trajectory": "stable",
        "confidence": 0.94,
        "evidence_spans": [evidence] if evidence else [],
        "counterevidence_spans": [],
        "context_conditions": [],
        "observability_limits": [],
        "forced_choice": False,
    }
    content = json.dumps(
        {
            "question_results": [
                {
                    "question_id": "RRQ_LOVE_EROS_DIRECTION",
                    "axis_results": [axis, dict(axis)] if duplicate else [axis],
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
        questionnaire_path=Path(
            "reference/relationship/relationship_dynamic_questionnaire_v1.json"
        ),
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
    assert freeze.schema_version == "relationship-phenotype-freeze-v2"
    assert freeze.validation_contract_version == VALIDATION_CONTRACT_VERSION
    assert freeze.validation_contract_sha256 == VALIDATION_CONTRACT_SHA256
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


def test_classifier_rejects_evidence_cited_from_a_different_question() -> None:
    other_question_text = "This sentence belongs only to the sexual-system answer."

    def transport(url: str, body: bytes, headers: Mapping[str, str], timeout: float) -> bytes:
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
                                "ordinal_value": "high",
                                "trajectory": "stable",
                                "confidence": 0.94,
                                "evidence_spans": [other_question_text],
                                "counterevidence_spans": [],
                                "context_conditions": [],
                                "observability_limits": [],
                                "forced_choice": False,
                            }
                        ],
                        "applicability_flags": [],
                        "unresolved_axis_ids": [],
                        "verbatim_preserved": True,
                    },
                    {
                        "question_id": "RRQ_SEXUAL_SYSTEM",
                        "axis_results": [],
                        "applicability_flags": [],
                        "unresolved_axis_ids": [],
                        "verbatim_preserved": True,
                    },
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

    classifier = OpenAIRelationshipPhenotypeClassifier(
        api_key="test-key",
        model="gpt-test",
        transport=transport,
    )
    answers = _answer_record() + [
        {
            "question_id": "RRQ_SEXUAL_SYSTEM",
            "fields": [
                {
                    "field_id": "sexual_system",
                    "status": "clear",
                    "answer": other_question_text,
                    "clarification": "",
                }
            ],
        }
    ]
    with pytest.raises(ValueError, match="not present verbatim"):
        classifier.classify_and_freeze(
            session_id="RR-TEST",
            answers=answers,
            semantic_audit=_semantic_audit(),
            questionnaire_path=Path(
                "reference/relationship/relationship_dynamic_questionnaire_v1.json"
            ),
            rubric_path=Path("reference/relationship/relationship_outcome_rubrics_v1.json"),
            protocol_path=Path(
                "reference/relationship/relationship_blind_classifier_protocol_v1.json"
            ),
        )


def test_source_text_corpus_routes_clarifications_to_their_source_question() -> None:
    corpus = source_text_corpus(
        _answer_record(),
        {
            "answers": [
                {
                    "source_question_id": "RRQ_SEXUAL_SYSTEM",
                    "source_field_id": "sexual_system",
                    "answer": "Clarification for sexual-system only.",
                }
            ]
        },
    )

    assert "Clarification for sexual-system only." in corpus["RRQ_SEXUAL_SYSTEM"]
    assert "Clarification for sexual-system only." not in corpus["RRQ_LOVE_EROS_DIRECTION"]


@pytest.mark.parametrize(
    ("axis_id", "direction", "message"),
    (
        ("dyadic_sexual_chemistry", "dyadic", "outside question"),
        ("physical_attraction", "dyadic", "invalid for directional"),
    ),
)
def test_classifier_rejects_off_target_axes_and_scope_direction_mismatches(
    axis_id: str,
    direction: str,
    message: str,
) -> None:
    def transport(url: str, body: bytes, headers: Mapping[str, str], timeout: float) -> bytes:
        return _provider_response(
            evidence="extremely physically attracted",
            axis_id=axis_id,
            direction=direction,
        )

    classifier = OpenAIRelationshipPhenotypeClassifier(
        api_key="test-key",
        model="gpt-test",
        transport=transport,
    )
    with pytest.raises(ValueError, match=message):
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


@pytest.mark.parametrize(
    ("evidence", "duplicate", "message"),
    (
        ("", False, "requires verbatim evidence"),
        ("extremely physically attracted", True, "duplicate axis/direction"),
    ),
)
def test_classifier_rejects_incomplete_or_duplicate_scored_rows(
    evidence: str,
    duplicate: bool,
    message: str,
) -> None:
    def transport(url: str, body: bytes, headers: Mapping[str, str], timeout: float) -> bytes:
        return _provider_response(evidence=evidence, duplicate=duplicate)

    classifier = OpenAIRelationshipPhenotypeClassifier(
        api_key="test-key",
        model="gpt-test",
        transport=transport,
    )
    with pytest.raises(ValueError, match=message):
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


def test_calibration_extractor_refuses_cross_question_duplicate_weighting() -> None:
    classifier = OpenAIRelationshipPhenotypeClassifier(
        api_key="test-key",
        model="gpt-test",
        transport=lambda url, body, headers, timeout: _provider_response(
            evidence="extremely physically attracted"
        ),
    )
    freeze = classifier.classify_and_freeze(
        session_id="RR-TEST",
        answers=_answer_record(),
        semantic_audit=_semantic_audit(),
        questionnaire_path=Path(
            "reference/relationship/relationship_dynamic_questionnaire_v1.json"
        ),
        rubric_path=Path("reference/relationship/relationship_outcome_rubrics_v1.json"),
        protocol_path=Path("reference/relationship/relationship_blind_classifier_protocol_v1.json"),
    )
    first = freeze.output.question_results[0]
    duplicate_question = QuestionPhenotype(
        question_id="RRQ_SEXUAL_SYSTEM",
        axis_results=first.axis_results,
    )
    duplicated = freeze.model_copy(
        update={"output": RelationshipPhenotypeOutput(question_results=(first, duplicate_question))}
    )

    with pytest.raises(ValueError, match="duplicate axis/direction across questions"):
        calibration_phenotype_observations(duplicated)

    mixed_duplicate = first.axis_results[0].model_copy(
        update={"status": "mixed", "ordinal_value": None}
    )
    mixed_conflict = freeze.model_copy(
        update={
            "output": RelationshipPhenotypeOutput(
                question_results=(
                    first,
                    QuestionPhenotype(
                        question_id="RRQ_SEXUAL_SYSTEM",
                        axis_results=(mixed_duplicate,),
                    ),
                )
            )
        }
    )
    with pytest.raises(ValueError, match="duplicate axis/direction across questions"):
        calibration_phenotype_observations(mixed_conflict)

    observations = calibration_phenotype_observations(freeze)
    assert len(observations) == 1
    assert observations[0].phenotype_freeze_sha256 == freeze.freeze_sha256
    assert observations[0].axis_id == "physical_attraction"


def test_calibration_extractor_refuses_axis_with_repeated_unresolved_probe() -> None:
    classifier = OpenAIRelationshipPhenotypeClassifier(
        api_key="test-key",
        model="gpt-test",
        transport=lambda url, body, headers, timeout: _provider_response(
            evidence="extremely physically attracted"
        ),
    )
    freeze = classifier.classify_and_freeze(
        session_id="RR-TEST",
        answers=_answer_record(),
        semantic_audit=_semantic_audit(),
        questionnaire_path=Path(
            "reference/relationship/relationship_dynamic_questionnaire_v1.json"
        ),
        rubric_path=Path("reference/relationship/relationship_outcome_rubrics_v1.json"),
        protocol_path=Path("reference/relationship/relationship_blind_classifier_protocol_v1.json"),
    )
    repeated_unresolved = freeze.model_copy(
        update={
            "output": RelationshipPhenotypeOutput(
                question_results=(
                    freeze.output.question_results[0],
                    QuestionPhenotype(
                        question_id="RRQ_SEXUAL_SYSTEM",
                        axis_results=(),
                        unresolved_axis_ids=("physical_attraction",),
                    ),
                )
            )
        }
    )

    with pytest.raises(ValueError, match="repeated probe remains unresolved"):
        calibration_phenotype_observations(repeated_unresolved)


def test_legacy_freeze_remains_revealable_but_is_not_calibration_eligible() -> None:
    classifier = OpenAIRelationshipPhenotypeClassifier(
        api_key="test-key",
        model="gpt-test",
        transport=lambda url, body, headers, timeout: _provider_response(
            evidence="extremely physically attracted"
        ),
    )
    current = classifier.classify_and_freeze(
        session_id="RR-TEST",
        answers=_answer_record(),
        semantic_audit=_semantic_audit(),
        questionnaire_path=Path(
            "reference/relationship/relationship_dynamic_questionnaire_v1.json"
        ),
        rubric_path=Path("reference/relationship/relationship_outcome_rubrics_v1.json"),
        protocol_path=Path("reference/relationship/relationship_blind_classifier_protocol_v1.json"),
    )
    legacy_payload = current.model_dump(mode="json")
    legacy_payload["schema_version"] = "relationship-phenotype-freeze-v1"
    legacy_payload.pop("validation_contract_version")
    legacy_payload.pop("validation_contract_sha256")
    legacy = RelationshipPhenotypeFreeze.model_validate(legacy_payload)
    historical_freeze_sha256 = canonical_sha256(legacy_payload)

    fingerprint = relationship_fingerprint(
        legacy,
        json.loads(Path("reference/relationship/relationship_outcome_rubrics_v1.json").read_text()),
    )
    assert legacy.freeze_sha256 == historical_freeze_sha256
    assert fingerprint["phenotype_freeze_sha256"] == historical_freeze_sha256
    assert fingerprint["classified_axes"][0]["axis_id"] == "physical_attraction"
    with pytest.raises(ValueError, match="requires a current validated phenotype freeze"):
        calibration_phenotype_observations(legacy)

    forged_legacy_payload = dict(legacy_payload)
    forged_legacy_payload["validation_contract_version"] = VALIDATION_CONTRACT_VERSION
    forged_legacy_payload["validation_contract_sha256"] = VALIDATION_CONTRACT_SHA256
    with pytest.raises(ValueError, match="legacy phenotype freeze cannot claim"):
        RelationshipPhenotypeFreeze.model_validate(forged_legacy_payload)
