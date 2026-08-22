from __future__ import annotations

from dataclasses import dataclass

import pytest

from hdmatch.model.v4_3 import (
    CORE_BLOCK_WEIGHTS,
    CoreBlock,
    CoreBlockAvailability,
    CoreBlockEvaluation,
    DirectnessClass,
    EvaluatedContradiction,
    EvaluatedPathway,
    EvaluatedStructuralAnchor,
    FlexibilityClass,
    ObservationConfidence,
    ObservationEvaluation,
    ResponseDisposition,
    StructuralClass,
    V43ScoringInput,
    effective_confidence,
    information_rubric_bits,
    score_v4_3,
)


@dataclass(frozen=True, slots=True)
class Provenance:
    universe_sha256: str = "a" * 64
    policy_version: str = "conditional-prevalence-v4.3-v1"
    parent_hierarchy_sha256: str = "b" * 64
    duration_weighted: bool = True
    conditional: bool = True
    exact_stable_intervals: bool = True
    source_scope: str = "declared-global-utc-universe"


@dataclass(frozen=True, slots=True)
class Estimate:
    anchor_id: str
    prevalence: float
    numerator_duration_microseconds: int
    denominator_duration_microseconds: int
    universe_sha256: str = "a" * 64
    policy_version: str = "conditional-prevalence-v4.3-v1"
    parent_hierarchy_sha256: str = "b" * 64
    selected_level_id: str = "declared-parent"
    backoff_ordinal: int = 0
    duration_weighted: bool = True
    conditional: bool = True
    exact_stable_intervals: bool = True
    source_scope: str = "declared-global-utc-universe"


@dataclass(frozen=True, slots=True)
class FixedPrevalence:
    values: dict[str, tuple[int, int]]
    provenance: Provenance = Provenance()

    def estimate(self, anchor_id: str, candidate_context: object) -> Estimate:
        del candidate_context
        numerator, denominator = self.values[anchor_id]
        return Estimate(
            anchor_id=anchor_id,
            prevalence=numerator / denominator,
            numerator_duration_microseconds=numerator,
            denominator_duration_microseconds=denominator,
            universe_sha256=self.provenance.universe_sha256,
            policy_version=self.provenance.policy_version,
            parent_hierarchy_sha256=self.provenance.parent_hierarchy_sha256,
            duration_weighted=self.provenance.duration_weighted,
            conditional=self.provenance.conditional,
            exact_stable_intervals=self.provenance.exact_stable_intervals,
            source_scope=self.provenance.source_scope,
        )


@dataclass(frozen=True, slots=True)
class ExplodingPrevalence:
    provenance: Provenance = Provenance()

    def estimate(self, anchor_id: str, candidate_context: object) -> Estimate:
        del candidate_context
        raise AssertionError(f"neutral anchor {anchor_id} must not request prevalence")


def _anchor(
    anchor_id: str,
    mechanism_key: str,
    *,
    supports: bool = True,
    structural_class: StructuralClass = StructuralClass.COMPLETE_CHANNEL,
    salience: float = 0.80,
    directness: DirectnessClass = DirectnessClass.DIRECT,
    directness_factor: float = 1.0,
    flexibility: FlexibilityClass = FlexibilityClass.F1_NARROW,
    flexibility_factor: float = 1.0,
) -> EvaluatedStructuralAnchor:
    return EvaluatedStructuralAnchor(
        anchor_id=anchor_id,
        mechanism_keys=(mechanism_key,),
        supports_response=supports,
        structural_class=structural_class,
        structural_salience=salience,
        directness_class=directness,
        directness_factor=directness_factor,
        flexibility_class=flexibility,
        flexibility_factor=flexibility_factor,
    )


def _all_core_blocks(
    *,
    type_strategy: float | None = 1.0,
    authority: float | None = 1.0,
    centers: float | None = 1.0,
    profile: float | None = 1.0,
) -> tuple[CoreBlockEvaluation, ...]:
    values = {
        CoreBlock.TYPE_STRATEGY: type_strategy,
        CoreBlock.AUTHORITY: authority,
        CoreBlock.DIAGNOSTIC_CENTERS: centers,
        CoreBlock.PROFILE: profile,
    }
    return tuple(
        CoreBlockEvaluation(
            block=block,
            availability=(
                CoreBlockAvailability.REPORTABLE
                if fraction is not None
                else CoreBlockAvailability.UNREPORTABLE
            ),
            earned_fraction=fraction,
        )
        for block, fraction in values.items()
    )


def _input(
    *observations: ObservationEvaluation,
    core_blocks: tuple[CoreBlockEvaluation, ...] | None = None,
) -> V43ScoringInput:
    return V43ScoringInput(
        candidate_context={"candidate": "public"},
        observations=observations,
        core_blocks=core_blocks or _all_core_blocks(),
    )


def test_effective_confidence_multiplies_and_unknown_states_are_zero() -> None:
    assert effective_confidence(ObservationConfidence(0.8, 0.5)) == pytest.approx(0.4)
    for disposition in (
        ResponseDisposition.UNKNOWN,
        ResponseDisposition.DEPENDS,
        ResponseDisposition.CONTEXT_DEPENDENT,
        ResponseDisposition.UNREPORTABLE,
    ):
        assert effective_confidence(ObservationConfidence(1.0, 1.0, disposition)) == 0.0


def test_information_rubric_bits_are_capped_and_require_positive_prevalence() -> None:
    assert information_rubric_bits(0.25) == pytest.approx(2.0)
    assert information_rubric_bits(2**-12) == 6.0
    with pytest.raises(ValueError, match="prevalence"):
        information_rubric_bits(0.0)


def test_exact_formula_includes_salience_directness_flexibility_and_contradiction() -> None:
    primary = _anchor(
        "channel:1-8",
        "channel-family:1-8",
        directness=DirectnessClass.STRONG,
        directness_factor=0.75,
        flexibility=FlexibilityClass.F2_MODERATE,
        flexibility_factor=0.75,
    )
    corroborator = _anchor(
        "cardinal:personality-sun:1.1",
        "cardinal:personality-sun",
        structural_class=StructuralClass.CARDINAL_SUN_EARTH,
        salience=0.75,
    )
    cluster = ObservationEvaluation(
        observation_id="OBS-EXPRESSION",
        dependency_cluster="EXPRESSION",
        confidence=ObservationConfidence(0.8, 0.5),
        pathways=(
            EvaluatedPathway(
                pathway_id="primary-plus-corr",
                primary=primary,
                corroborators=(corroborator,),
                contradiction=EvaluatedContradiction(True, 0.50),
            ),
        ),
    )

    score = score_v4_3(
        _input(
            cluster,
            core_blocks=_all_core_blocks(
                type_strategy=1.0,
                authority=0.5,
                centers=None,
                profile=0.0,
            ),
        ),
        FixedPrevalence(
            {
                "channel:1-8": (1, 4),
                "cardinal:personality-sun:1.1": (1, 2),
            }
        ),
    )

    # Primary: .4 * (.8 * .75) * .75 * 2 = .36.
    # Corroborator before cap: .4 * (.75 * 1) * 1 * 1 = .30; capped to .045.
    assert score.evidence_rubric_bits == pytest.approx(0.405)
    assert score.contradiction_rubric_bits == pytest.approx(0.4 * 0.5 * 4.0)
    assert score.net_information == pytest.approx(0.405 - 0.8)
    assert score.detailed_support == pytest.approx(100 * (0.60 + 0.15 * 0.75))
    # CoreFit is a separate 100-point ratio: (30 + 15 + 0) / (30 + 30 + 15).
    assert score.core_fit == pytest.approx(60.0)
    assert score.net_information != pytest.approx(score.core_fit + 0.405 - 0.8)
    assert score.meaningful_contradictions == 1


def test_mutation_guard_flexibility_factor_cannot_be_omitted_or_changed() -> None:
    with pytest.raises(ValueError, match="flexibility"):
        _anchor(
            "channel",
            "channel",
            flexibility=FlexibilityClass.F3_BROAD,
            flexibility_factor=1.0,
        )

    cluster = ObservationEvaluation(
        observation_id="OBS-FLEX",
        dependency_cluster="FLEX",
        confidence=ObservationConfidence(1.0, 1.0),
        pathways=(
            EvaluatedPathway(
                "p",
                _anchor(
                    "channel",
                    "channel",
                    flexibility=FlexibilityClass.F3_BROAD,
                    flexibility_factor=0.5,
                ),
            ),
        ),
    )
    score = score_v4_3(_input(cluster), FixedPrevalence({"channel": (1, 4)}))
    assert score.evidence_rubric_bits == pytest.approx(0.8 * 0.5 * 2.0)


def test_alternative_pathways_compete_instead_of_summing() -> None:
    cluster = ObservationEvaluation(
        observation_id="OBS-ALT",
        dependency_cluster="ALTERNATIVES",
        confidence=ObservationConfidence(1.0, 1.0),
        pathways=(
            EvaluatedPathway("a", _anchor("a", "a")),
            EvaluatedPathway("b", _anchor("b", "b")),
        ),
    )
    score = score_v4_3(
        _input(cluster),
        FixedPrevalence({"a": (1, 4), "b": (1, 2)}),
    )

    assert score.evidence_rubric_bits == pytest.approx(0.8 * 2.0)
    assert score.evidence_rubric_bits != pytest.approx(0.8 * 3.0)
    assert score.clusters[0].evidence_pathway_id == "OBS-ALT:a"


def test_only_strongest_independent_corroborator_receives_fifteen_percent() -> None:
    primary = _anchor("primary", "shared")
    dependent = _anchor(
        "dependent-gate",
        "shared",
        structural_class=StructuralClass.PROMINENT_PLANETARY_ACTIVATION,
        salience=0.45,
    )
    strongest = _anchor(
        "strong-independent",
        "independent-strong",
        structural_class=StructuralClass.CARDINAL_SUN_EARTH,
        salience=0.75,
    )
    weaker = _anchor(
        "weak-independent",
        "independent-weak",
        structural_class=StructuralClass.PROMINENT_PLANETARY_ACTIVATION,
        salience=0.45,
    )
    cluster = ObservationEvaluation(
        observation_id="OBS-CORR",
        dependency_cluster="CORR",
        confidence=ObservationConfidence(1.0, 1.0),
        pathways=(
            EvaluatedPathway(
                "p",
                primary,
                corroborators=(dependent, weaker, strongest),
            ),
        ),
    )
    score = score_v4_3(
        _input(cluster),
        FixedPrevalence(
            {
                "primary": (1, 2),
                "strong-independent": (1, 2),
                # Neither the dependent nor weaker alternative may be queried.
            }
        ),
    )
    pathway = score.clusters[0].pathways[0]

    assert pathway.corroborator is not None
    assert pathway.corroborator.anchor_id == "strong-independent"
    assert pathway.pathway_support == pytest.approx(0.8 + 0.15 * 0.75)
    assert pathway.evidence_rubric_bits == pytest.approx(0.8 + 0.15 * 0.75)


def test_channel_and_component_gate_cannot_double_count_across_clusters() -> None:
    channel = ObservationEvaluation(
        observation_id="OBS-CHANNEL",
        dependency_cluster="CHANNEL_DESCRIPTION",
        confidence=ObservationConfidence(1.0, 1.0),
        pathways=(EvaluatedPathway("channel", _anchor("channel:1-8", "family:1-8")),),
    )
    gate = ObservationEvaluation(
        observation_id="OBS-GATE",
        dependency_cluster="GATE_PARAPHRASE",
        confidence=ObservationConfidence(1.0, 1.0),
        pathways=(
            EvaluatedPathway(
                "gate",
                _anchor(
                    "gate:1",
                    "family:1-8",
                    structural_class=StructuralClass.PROMINENT_PLANETARY_ACTIVATION,
                    salience=0.45,
                ),
            ),
        ),
    )

    with pytest.raises(ValueError, match="reused across dependency clusters"):
        score_v4_3(
            _input(channel, gate),
            FixedPrevalence({"channel:1-8": (1, 2), "gate:1": (1, 2)}),
        )


def test_repeated_dependency_cluster_collapses_and_duplicate_observation_fails() -> None:
    cluster = ObservationEvaluation(
        observation_id="OBS",
        dependency_cluster="DUPLICATE",
        confidence=ObservationConfidence(1.0, 1.0),
        pathways=(EvaluatedPathway("p", _anchor("a", "shared")),),
    )
    paraphrase = ObservationEvaluation(
        observation_id="OBS-PARAPHRASE",
        dependency_cluster="DUPLICATE",
        confidence=ObservationConfidence(1.0, 1.0),
        pathways=(EvaluatedPathway("p", _anchor("b", "shared")),),
    )
    score = score_v4_3(
        _input(cluster, paraphrase),
        FixedPrevalence({"a": (1, 2), "b": (1, 2)}),
    )
    assert score.evidence_rubric_bits == pytest.approx(0.8)
    assert score.detailed_support == pytest.approx(80.0)

    with pytest.raises(ValueError, match="unique IDs"):
        _input(cluster, cluster)


def test_contradictions_use_formula_and_strongest_instance_not_sum() -> None:
    cluster = ObservationEvaluation(
        observation_id="OBS-OPPOSITION",
        dependency_cluster="OPPOSITION",
        confidence=ObservationConfidence(0.75, 0.5),
        pathways=(
            EvaluatedPathway(
                "moderate",
                _anchor("neutral-a", "a", supports=False),
                contradiction=EvaluatedContradiction(True, 0.5),
            ),
            EvaluatedPathway(
                "strong",
                _anchor("neutral-b", "b", supports=False),
                contradiction=EvaluatedContradiction(True, 0.75),
            ),
        ),
    )
    score = score_v4_3(_input(cluster), ExplodingPrevalence())

    assert score.contradiction_rubric_bits == pytest.approx(0.75 * 0.5 * 0.75 * 4)
    assert score.contradiction_rubric_bits != pytest.approx(
        0.75 * 0.5 * (0.5 + 0.75) * 4
    )
    assert score.clusters[0].contradiction_pathway_id == "OBS-OPPOSITION:strong"


def test_unknown_cannot_be_coerced_and_neutral_unknown_does_not_call_prevalence() -> None:
    with pytest.raises(ValueError, match="cannot be coerced"):
        ObservationEvaluation(
            observation_id="OBS-UNKNOWN",
            dependency_cluster="UNKNOWN",
            confidence=ObservationConfidence(1.0, 1.0, ResponseDisposition.UNKNOWN),
            pathways=(EvaluatedPathway("coerced", _anchor("a", "a")),),
        )

    neutral = ObservationEvaluation(
        observation_id="OBS-UNKNOWN",
        dependency_cluster="UNKNOWN",
        confidence=ObservationConfidence(1.0, 1.0, ResponseDisposition.DEPENDS),
        pathways=(EvaluatedPathway("neutral", _anchor("a", "a", supports=False)),),
    )
    score = score_v4_3(_input(neutral), ExplodingPrevalence())
    assert score.net_information == 0.0
    assert score.detailed_support == 0.0


def test_core_fit_requires_all_blocks_and_excludes_only_explicit_unreportables() -> None:
    assert sum(CORE_BLOCK_WEIGHTS.values()) == 100.0
    with pytest.raises(ValueError, match="all four frozen core blocks"):
        V43ScoringInput(candidate_context={}, observations=(), core_blocks=_all_core_blocks()[:3])

    score = score_v4_3(
        _input(
            core_blocks=_all_core_blocks(
                type_strategy=1.0,
                authority=None,
                centers=0.5,
                profile=0.0,
            )
        ),
        ExplodingPrevalence(),
    )
    assert score.core_fit == pytest.approx((30.0 + 12.5) / (30.0 + 25.0 + 15.0) * 100)
    assert score.net_information == 0.0


@pytest.mark.parametrize(
    ("provenance", "message"),
    [
        (Provenance(duration_weighted=False), "duration weighted"),
        (Provenance(conditional=False), "conditional prevalence"),
        (Provenance(exact_stable_intervals=False), "exact stable intervals"),
        (Provenance(source_scope="candidate-file"), "candidate-file prevalence"),
    ],
)
def test_prevalence_mutations_fail_closed(provenance: Provenance, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        score_v4_3(_input(), FixedPrevalence({}, provenance))
