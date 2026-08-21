from __future__ import annotations

from pathlib import Path

import pytest

from hdmatch.model.compiler import build_mapping_library
from hdmatch.model.dependencies import ClusterContribution, collapse_dependency_clusters
from hdmatch.model.reliability import effective_confidence
from hdmatch.model.symbolic_score import information_bits, score_symbolic
from hdmatch.questionnaire.response import NormalizedResponse

ROOT = Path(__file__).parents[2]


def _response(question_id: str, answer_token: str, reliability: float = 1.0) -> NormalizedResponse:
    return NormalizedResponse(
        question_id=question_id,
        answer_token=answer_token,
        behavioral_confidence=1.0,
        measurement_reliability=reliability,
    )


def test_information_bits_are_capped_and_validated() -> None:
    assert information_bits(0.25) == pytest.approx(2.0)
    assert information_bits(2**-10) == pytest.approx(6.0)
    with pytest.raises(ValueError, match="prevalence"):
        information_bits(0.0)


def test_effective_confidence_cannot_increase_evidence() -> None:
    assert effective_confidence(0.75, 1.0) == pytest.approx(0.75)
    assert effective_confidence(0.75, 0.25) == pytest.approx(0.1875)
    with pytest.raises(ValueError, match="measurement_reliability"):
        effective_confidence(0.75, 1.01)


def test_repeated_authority_questions_receive_one_cluster_credit() -> None:
    library = build_mapping_library(ROOT)
    chart = {
        "type": "Projector",
        "strategy": "Wait for the Invitation",
        "authority": "Splenic",
        "profile": "2/4",
        "defined_centers": ("G", "Spleen", "Throat"),
    }
    prevalence = {mapping.anchor_id: 0.25 for mapping in library.frozen_mappings}
    score = score_symbolic(
        chart,
        (
            _response("D01", "an_immediate_quiet_sense", reliability=0.5),
            _response("D02", "brief_and_nonrepeating", reliability=0.5),
        ),
        library,
        prevalence,
    )

    assert score.evidence_rubric_bits == pytest.approx(1.0)
    assert score.contradiction_rubric_bits == 0.0
    assert score.net_rubric_bits == pytest.approx(1.0)
    assert score.detailed_support == pytest.approx(100.0)
    assert score.core_fit == pytest.approx(100.0)
    assert len(score.scored_clusters) == 1


def test_type_and_sacral_energy_paraphrases_do_not_double_count() -> None:
    library = build_mapping_library(ROOT)
    chart = {
        "type": "generator",
        "strategy": "wait_to_respond",
        "authority": "sacral",
        "profile": "1/3",
        "defined_centers": ("sacral", "g", "root"),
    }
    prevalence = {mapping.anchor_id: 0.25 for mapping in library.frozen_mappings}
    score = score_symbolic(
        chart,
        (
            _response(
                "S05",
                "sustain_daily_workforce_energy_indefinitely_if_sleep_and_health_are_adequate",
            ),
            _response("C08", "physical_energy_renew_through_doing_the_right_work"),
        ),
        library,
        prevalence,
    )

    assert score.evidence_rubric_bits == pytest.approx(2.0)
    assert len(score.scored_clusters) == 1


def test_reliability_only_downweights_and_explicit_opposite_contradicts() -> None:
    library = build_mapping_library(ROOT)
    chart = {
        "type": "Projector",
        "strategy": "Wait for the Invitation",
        "authority": "Emotional",
        "profile": "2/4",
        "defined_centers": ("G", "Solar Plexus", "Throat"),
    }
    prevalence = {mapping.anchor_id: 0.25 for mapping in library.frozen_mappings}
    full = score_symbolic(
        chart,
        (_response("D01", "an_immediate_quiet_sense"),),
        library,
        prevalence,
    )
    quarter = score_symbolic(
        chart,
        (_response("D01", "an_immediate_quiet_sense", reliability=0.25),),
        library,
        prevalence,
    )

    assert full.evidence_rubric_bits == 0.0
    assert full.contradiction_rubric_bits == pytest.approx(4.0)
    assert full.meaningful_contradictions == 1
    assert quarter.contradiction_rubric_bits == pytest.approx(1.0)
    assert quarter.net_rubric_bits > full.net_rubric_bits


def test_missing_support_is_neutral_and_unresolved_is_reported() -> None:
    library = build_mapping_library(ROOT)
    chart = {
        "type": "Reflector",
        "strategy": "Wait a Lunar Cycle",
        "authority": "Lunar",
        "profile": "1/3",
        "defined_centers": (),
    }
    prevalence = {mapping.anchor_id: 0.5 for mapping in library.frozen_mappings}
    score = score_symbolic(
        chart,
        (
            _response("D01", "no_stable_pattern"),
            _response("T01", "presenting_something_distinctly_your_own"),
        ),
        library,
        prevalence,
    )

    assert score.evidence_rubric_bits == 0.0
    assert score.contradiction_rubric_bits == 0.0
    assert score.unresolved_question_ids == ("T01",)


def test_cluster_collapse_is_deterministic_for_alternative_pathways() -> None:
    values = (
        ClusterContribution("C", "MAP-B", "b", 1.0, 0.8, 2.0, 0.0, 0.0),
        ClusterContribution("C", "MAP-A", "a", 1.0, 0.8, 2.0, 0.0, 0.0),
    )

    assert collapse_dependency_clusters(values)[0].mapping_id == "MAP-A"
