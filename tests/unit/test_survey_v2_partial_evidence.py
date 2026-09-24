from __future__ import annotations

from fractions import Fraction

import pytest

from hdmatch.evaluation.survey_v2_partial_evidence import (
    candidate_field_value,
    compile_partial_evidence,
    score_candidate,
    score_candidate_scaled,
)
from hdmatch.schemas import StructuralChartFeatures


def _features(profile: str = "2/5") -> StructuralChartFeatures:
    return StructuralChartFeatures(
        type="Projector",
        strategy="Wait for the Invitation",
        authority="Splenic",
        profile=profile,
        definition="Split",
        defined_centers=("Spleen", "Heart", "G"),
        channels=("1-8", "23-43", "24-61"),
        activation_gates={
            "personality:moon": 24,
            "design:mars": 61,
        },
    )


def _model() -> dict:
    return {
        "mappings": [
            {
                "id": "PROFILE_24",
                "predicate": {"feature": "profile", "equals": "2/4"},
            },
            {
                "id": "PROFILE_LINE5_PROJECTION",
                "predicate": {"feature": "profile_has_line", "line": 5},
            },
        ],
        "contradictions": [],
    }


def _field_map() -> dict:
    return {
        "field_dependencies": [
            {
                "field_id": "baseline:PROFILE_24",
                "dependency_cluster_id": "DC:PROFILE_STRUCTURE",
                "source_mapping_ids": ["PROFILE_24"],
                "source_predicates": ["profile=2/4"],
            },
            {
                "field_id": "baseline:PROFILE_LINE5_PROJECTION",
                "dependency_cluster_id": "DC:PROFILE_STRUCTURE",
                "source_mapping_ids": ["PROFILE_LINE5_PROJECTION"],
                "source_predicates": ["profile_has_line=5"],
            },
            {
                "field_id": "channel:1-8",
                "dependency_cluster_id": "DC:ORIGINAL_CONTRIBUTION",
                "source_mapping_ids": [],
                "source_predicates": ["channel=1-8"],
            },
            {
                "field_id": "personality:moon",
                "dependency_cluster_id": "DC:PERSONALITY:MOON",
                "source_mapping_ids": [],
                "source_predicates": ["activation:personality:moon=gate:<label>"],
            },
        ]
    }



def test_profile_cluster_macro_average_preserves_mixed_partial_credit() -> None:
    evidence = {
        "observations": [
            {
                "probe_id": "q1",
                "field_id": "baseline:PROFILE_24",
                "labels": [0, 1],
                "reliability": "0.65",
            },
            {
                "probe_id": "projection",
                "field_id": "baseline:PROFILE_LINE5_PROJECTION",
                "labels": [1],
                "reliability": "0.65",
            },
        ]
    }
    compiled = compile_partial_evidence(
        evidence=evidence,
        field_dependency_map=_field_map(),
        model=_model(),
    )
    target = score_candidate(_features("2/5"), compiled)
    competitor = score_candidate(_features("2/4"), compiled)
    assert compiled.score_scale == 80
    assert score_candidate_scaled(_features("2/5"), compiled) == 39
    assert score_candidate_scaled(_features("2/4"), compiled) == 13
    assert target == Fraction(39, 80)
    assert competitor == Fraction(13, 80)
    assert target - competitor == Fraction(13, 40)


def test_channel_and_activation_candidate_values_follow_frozen_normalization() -> None:
    evidence = {
        "observations": [
            {
                "probe_id": "channel",
                "field_id": "channel:1-8",
                "labels": [1],
                "reliability": "1",
            },
            {
                "probe_id": "moon",
                "field_id": "personality:moon",
                "labels": ["gate:24"],
                "reliability": "1",
            },
        ]
    }
    compiled = compile_partial_evidence(
        evidence=evidence,
        field_dependency_map=_field_map(),
        model=_model(),
    )
    values = {
        field.field_id: candidate_field_value(_features(), field)
        for field in compiled.fields
    }
    assert values["channel:1-8"] == 1
    assert values["personality:moon"] == "gate:24"
    assert score_candidate(_features(), compiled) == Fraction(2, 1)


def test_duplicate_probe_identity_fails_closed() -> None:
    evidence = {
        "observations": [
            {
                "probe_id": "same",
                "field_id": "baseline:PROFILE_24",
                "labels": [1],
                "reliability": "0.5",
            },
            {
                "probe_id": "same",
                "field_id": "baseline:PROFILE_LINE5_PROJECTION",
                "labels": [1],
                "reliability": "0.5",
            },
        ]
    }
    with pytest.raises(ValueError, match="duplicate probe_id"):
        compile_partial_evidence(
            evidence=evidence,
            field_dependency_map=_field_map(),
            model=_model(),
        )
