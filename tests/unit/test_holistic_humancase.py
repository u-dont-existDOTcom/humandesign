from __future__ import annotations

import pytest

from hdmatch.human.dataset import HumanCase
from hdmatch.human.holistic_humancase import (
    decode_question_answer_label,
    human_case_to_positive_evidence,
    human_cases_to_positive_evidence,
)
from hdmatch.schemas import BehavioralResponse


def _typed_case() -> HumanCase:
    return HumanCase(
        participant_id="p1",
        cohort="development",
        responses={},
        response_records=(
            BehavioralResponse(
                question_id="social.childhood",
                cluster_id="social-style",
                answer="selective-but-warm",
                behavioral_confidence=0.8,
                measurement_reliability=1.0,
                example_text="Had a few close friends.",
            ),
            BehavioralResponse(
                question_id="social.current",
                cluster_id="social-style",
                answer="other: outgoing in trusted groups",
                behavioral_confidence=0.6,
                measurement_reliability=1.0,
            ),
            BehavioralResponse(
                question_id="decision.signal",
                cluster_id="decision-signal",
                answer="unknown/context-dependent",
                behavioral_confidence=0.4,
                measurement_reliability=0.5,
            ),
        ),
        chart_features={"type": "Projector", "gate:10": 1},
        birth_year=1985,
        metadata={"site": "senegal-pilot", "sex": "M"},
    )


def test_rich_answers_become_positive_labels_with_question_opportunities() -> None:
    record, chart, opportunities, _clusters = human_case_to_positive_evidence(
        _typed_case(),
        metadata_match_fields=("site", "sex"),
    )
    decoded = dict(decode_question_answer_label(label) for label in record.observed_labels)
    assert decoded["social.childhood"] == "selective-but-warm"
    assert decoded["social.current"] == "other: outgoing in trusted groups"
    assert decoded["decision.signal"] == "unknown/context-dependent"
    assert all(
        opportunities[label] == decode_question_answer_label(label)[0]
        for label in record.observed_labels
    )
    assert record.match_strata == {
        "birth_year": "1985",
        "site": "senegal-pilot",
        "sex": "M",
    }
    assert chart.owner_participant_id == "p1"
    assert chart.chart_features == record.chart_features


def test_dependency_cluster_caps_correlated_question_weight() -> None:
    record, _chart, _opportunities, clusters = human_case_to_positive_evidence(_typed_case())
    by_question = {
        decode_question_answer_label(label)[0]: record.evidence_weights[label]
        for label in record.observed_labels
    }
    # social childhood/current share one dependency cluster, so their base
    # confidence weights 0.8 and 0.6 are divided by two instead of counting as
    # two independent observations.
    assert by_question["social.childhood"] == pytest.approx(0.4)
    assert by_question["social.current"] == pytest.approx(0.3)
    assert by_question["decision.signal"] == pytest.approx(0.2)
    social_labels = [
        label
        for label in record.observed_labels
        if decode_question_answer_label(label)[0].startswith("social.")
    ]
    assert {clusters[label] for label in social_labels} == {"social-style"}


def test_other_is_preserved_and_only_explicit_unknown_answer_is_omitted() -> None:
    record, _chart, _opportunities, _clusters = human_case_to_positive_evidence(
        _typed_case(),
        excluded_answers={"decision.signal": ("unknown/context-dependent",)},
    )
    answers = {
        decode_question_answer_label(label) for label in record.observed_labels
    }
    assert (
        "social.current",
        "other: outgoing in trusted groups",
    ) in answers
    assert ("decision.signal", "unknown/context-dependent") not in answers


def test_legacy_flat_case_uses_question_as_singleton_dependency_cluster() -> None:
    case = HumanCase(
        participant_id="legacy",
        cohort="development",
        responses={"q1": "yes", "q2": "no"},
        response_reliability={"q1": 0.7, "q2": 0.9},
        chart_features={"f": "x"},
        birth_year=1990,
    )
    record, _chart, opportunities, clusters = human_case_to_positive_evidence(case)
    by_question = {
        decode_question_answer_label(label)[0]: record.evidence_weights[label]
        for label in record.observed_labels
    }
    assert by_question == {"q1": pytest.approx(0.7), "q2": pytest.approx(0.9)}
    for label in record.observed_labels:
        question_id, _answer = decode_question_answer_label(label)
        assert opportunities[label] == question_id
        assert clusters[label] == question_id


def test_multi_case_conversion_records_explicitly_empty_people_as_skipped() -> None:
    empty = HumanCase(
        participant_id="empty",
        cohort="development",
        responses={"q": "unknown"},
        chart_features={"f": "z"},
    )
    converted = human_cases_to_positive_evidence(
        (_typed_case(), empty),
        excluded_answers={
            "decision.signal": ("unknown/context-dependent",),
            "q": ("unknown",),
        },
    )
    assert [record.participant_id for record in converted.records] == ["p1"]
    assert converted.skipped_no_scorable_evidence == ("empty",)


def test_validation_case_is_rejected_to_avoid_true_chart_leakage() -> None:
    case = HumanCase(
        participant_id="v1",
        cohort="validation",
        responses={"q": "a"},
        chart_features={"f": 1},
    )
    with pytest.raises(ValueError, match="DEVELOPMENT-only"):
        human_case_to_positive_evidence(case)
