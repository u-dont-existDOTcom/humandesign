from __future__ import annotations

from dataclasses import dataclass

import pytest

from hdmatch.model_b.prevalence import PrevalenceEstimate
from hdmatch.model_b.scoring import (
    information_rubric_bits,
    score_detailed_symbolic,
)
from hdmatch.model_b.types import EvaluatedPathway, StructuralEvidence


@dataclass(frozen=True)
class FixedPrevalence:
    values: dict[str, float]

    def estimate(self, anchor_id: str, chart: object) -> PrevalenceEstimate:
        del chart
        value = self.values[anchor_id]
        return PrevalenceEstimate(
            anchor_id=anchor_id,
            universe_id="frozen-reference",
            universe_sha256="c" * 64,
            selected_level_id="declared-parent",
            selected_parent_anchor_ids=(),
            selected_conditioning_values=(),
            numerator_duration_seconds=100.0 * value,
            denominator_duration_seconds=100.0,
            effective_state_equivalents=500.0,
            minimum_reference_size_met=True,
            prevalence=value,
            duration_weighted=True,
            segmentation="exact-boundary-events",
            backoff_level=0,
            attempts=(),
        )


@dataclass(frozen=True)
class ExplodingPrevalence:
    def estimate(self, anchor_id: str, chart: object) -> PrevalenceEstimate:
        raise AssertionError(f"unsupported anchor {anchor_id} must not request prevalence")


def _evidence(
    anchor_id: str,
    dependency_key: str,
    *,
    supports: bool = True,
    salience: float = 1.0,
    directness: float = 1.0,
) -> StructuralEvidence:
    return StructuralEvidence(
        anchor_id=anchor_id,
        dependency_keys=(dependency_key,),
        supports_response=supports,
        structural_salience=salience,
        mapping_directness=directness,
    )


def _pathway(
    cluster: str,
    pathway_id: str,
    primary: StructuralEvidence,
    *,
    confidence: float = 1.0,
    corroborators: tuple[StructuralEvidence, ...] = (),
    contradiction: float = 0.0,
) -> EvaluatedPathway:
    return EvaluatedPathway(
        rule_id=f"rule-{pathway_id}",
        dependency_cluster=cluster,
        pathway_id=pathway_id,
        effective_confidence=confidence,
        primary=primary,
        corroborators=corroborators,
        contradiction_severity=contradiction,
    )


def test_information_values_are_rubric_bits_and_single_anchor_is_capped() -> None:
    assert information_rubric_bits(0.25) == pytest.approx(2.0)
    assert information_rubric_bits(2**-12) == 6.0
    assert information_rubric_bits(0.0) == 6.0
    with pytest.raises(ValueError, match="prevalence"):
        information_rubric_bits(1.1)


def test_unsupported_structure_is_neutral_and_does_not_request_prevalence() -> None:
    pathway = _pathway("cluster", "missing", _evidence("a", "a", supports=False))

    result = score_detailed_symbolic({}, (pathway,), ExplodingPrevalence())

    assert result.rubric_unit == "rubric_bits"
    assert result.evidence_rubric_bits == 0.0
    assert result.contradiction_rubric_bits == 0.0
    assert result.net_rubric_bits == 0.0
    assert result.detailed_support == 0.0


def test_structural_dependency_cannot_receive_full_credit_in_two_clusters() -> None:
    first = _pathway("cluster-a", "a", _evidence("channel", "shared-channel-family"))
    second = _pathway("cluster-b", "b", _evidence("gate", "shared-channel-family"))

    with pytest.raises(ValueError, match="reused across clusters"):
        score_detailed_symbolic(
            {},
            (first, second),
            FixedPrevalence({"channel": 0.25, "gate": 0.5}),
        )


def test_exact_anchor_identity_cannot_be_hidden_by_different_dependency_keys() -> None:
    first = _pathway("cluster-a", "a", _evidence("same-anchor", "key-a"))
    second = _pathway("cluster-b", "b", _evidence("same-anchor", "key-b"))

    with pytest.raises(ValueError, match="reused across clusters"):
        score_detailed_symbolic(
            {},
            (first, second),
            FixedPrevalence({"same-anchor": 0.25}),
        )


def test_alternatives_compete_and_only_independent_corroborator_gets_15_percent() -> None:
    weak = _pathway(
        "cluster",
        "weak",
        _evidence("weak", "weak", salience=0.45),
    )
    strong = _pathway(
        "cluster",
        "strong",
        _evidence("primary", "primary", salience=0.8),
        corroborators=(
            _evidence("dependent", "primary", salience=1.0),
            _evidence("independent", "independent", salience=1.0),
        ),
    )
    provider = FixedPrevalence(
        {"weak": 0.25, "primary": 0.25, "dependent": 0.01, "independent": 0.25}
    )

    result = score_detailed_symbolic({}, (weak, strong), provider)
    cluster = result.clusters[0]
    selected = next(item for item in cluster.evaluated_pathways if item.pathway_id == "strong")

    assert cluster.evidence_pathway_id == "strong"
    assert selected.primary is not None
    assert selected.corroborator is not None
    assert selected.corroborator.anchor_id == "independent"
    assert cluster.support == pytest.approx(0.8 + 0.15)
    assert cluster.evidence_rubric_bits == pytest.approx(0.8 * 2.0 + 0.15 * 2.0)


def test_explicit_contradiction_is_capped_and_missing_structure_does_not_create_it() -> None:
    explicit = _pathway(
        "cluster",
        "explicit-opposite",
        _evidence("missing", "missing", supports=False),
        confidence=0.5,
        contradiction=1.0,
    )

    result = score_detailed_symbolic({}, (explicit,), ExplodingPrevalence())

    assert result.evidence_rubric_bits == 0.0
    assert result.contradiction_rubric_bits == pytest.approx(2.0)
    assert result.meaningful_contradictions == 1


def test_score_is_deterministic_under_pathway_input_permutation() -> None:
    values = (
        _pathway("cluster-b", "b", _evidence("b", "b"), confidence=0.75),
        _pathway("cluster-a", "a", _evidence("a", "a"), confidence=0.5),
    )
    provider = FixedPrevalence({"a": 0.5, "b": 0.25})

    forward = score_detailed_symbolic({"context": "candidate"}, values, provider)
    reverse = score_detailed_symbolic({"context": "candidate"}, reversed(values), provider)

    assert forward == reverse
    assert tuple(item.dependency_cluster for item in forward.clusters) == (
        "cluster-a",
        "cluster-b",
    )
