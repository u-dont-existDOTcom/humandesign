"""Pure implementation of the canonical V4.3 symbolic score equations."""

from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass

from hdmatch.model.v4_3.contracts import (
    CONTRADICTION_SCALE_RUBRIC_BITS,
    CORE_BLOCK_WEIGHTS,
    INDEPENDENT_CORROBORATION_CAP,
    INFORMATION_CAP_RUBRIC_BITS,
    RUBRIC_UNIT,
    V43_SCORING_ENGINE_VERSION,
    ConditionalPrevalenceEstimateLike,
    ConditionalPrevalenceProvenanceLike,
    ConditionalPrevalenceProvider,
    CoreBlock,
    EvaluatedPathway,
    EvaluatedStructuralAnchor,
    ObservationConfidence,
    ObservationEvaluation,
    V43ScoringInput,
)

GLOBAL_PREVALENCE_SOURCE_SCOPE = "declared-global-utc-universe"


@dataclass(frozen=True, slots=True)
class AnchorContribution:
    anchor_id: str
    structural_salience: float
    directness_factor: float
    flexibility_factor: float
    support: float
    prevalence: float
    raw_information_rubric_bits: float
    capped_information_rubric_bits: float
    evidence_rubric_bits: float
    selected_level_id: str
    backoff_ordinal: int
    numerator_duration_microseconds: int
    denominator_duration_microseconds: int
    universe_sha256: str
    policy_version: str
    parent_hierarchy_sha256: str


@dataclass(frozen=True, slots=True)
class PathwayContribution:
    observation_id: str
    pathway_id: str
    effective_confidence: float
    pathway_support: float
    evidence_rubric_bits: float
    primary: AnchorContribution | None
    corroborator: AnchorContribution | None
    contradiction_severity: float
    contradiction_rubric_bits: float


@dataclass(frozen=True, slots=True)
class DependencyClusterContribution:
    dependency_cluster: str
    observation_ids: tuple[str, ...]
    effective_confidence: float
    evidence_pathway_id: str | None
    support_pathway_id: str | None
    contradiction_pathway_id: str | None
    support: float
    evidence_rubric_bits: float
    contradiction_severity: float
    contradiction_rubric_bits: float
    meaningful_contradiction: bool
    pathways: tuple[PathwayContribution, ...]


@dataclass(frozen=True, slots=True)
class CoreBlockContribution:
    block: CoreBlock
    available: bool
    weight: float
    earned_fraction: float | None
    earned_points: float


@dataclass(frozen=True, slots=True)
class V43CandidateScore:
    """Three separate V4.3 measures; rubric bits are not probabilities."""

    scoring_engine_version: str
    rubric_unit: str
    evidence_rubric_bits: float
    contradiction_rubric_bits: float
    net_information: float
    detailed_support: float
    core_fit: float
    meaningful_contradictions: int
    clusters: tuple[DependencyClusterContribution, ...]
    core_blocks: tuple[CoreBlockContribution, ...]
    prevalence_universe_sha256: str
    prevalence_policy_version: str
    prevalence_parent_hierarchy_sha256: str

    def __post_init__(self) -> None:
        if self.scoring_engine_version != V43_SCORING_ENGINE_VERSION:
            raise ValueError("score must identify the canonical V4.3 scoring engine")
        if self.rubric_unit != RUBRIC_UNIT:
            raise ValueError("V4.3 information values must be labeled rubric_bits")
        for label, value in (
            ("evidence rubric bits", self.evidence_rubric_bits),
            ("contradiction rubric bits", self.contradiction_rubric_bits),
        ):
            if not math.isfinite(value) or value < 0.0:
                raise ValueError(f"{label} must be finite and nonnegative")
        if not math.isfinite(self.net_information) or not math.isclose(
            self.net_information,
            self.evidence_rubric_bits - self.contradiction_rubric_bits,
            rel_tol=1e-15,
            abs_tol=1e-15,
        ):
            raise ValueError("NetInformation cannot contain CoreFit or another hidden bonus")
        for label, value in (
            ("DetailedSupport", self.detailed_support),
            ("CoreFit", self.core_fit),
        ):
            if not math.isfinite(value) or not 0.0 <= value <= 100.0:
                raise ValueError(f"{label} must be finite and in [0, 100]")
        if self.meaningful_contradictions < 0:
            raise ValueError("meaningful contradiction count cannot be negative")
        _require_sha256("prevalence universe", self.prevalence_universe_sha256)
        _require_sha256(
            "prevalence parent hierarchy", self.prevalence_parent_hierarchy_sha256
        )
        if not self.prevalence_policy_version:
            raise ValueError("prevalence policy version must not be empty")


def effective_confidence(confidence: ObservationConfidence) -> float:
    """Return ``behavioral_confidence * measurement_reliability`` or zero.

    Unknown, depends, context-dependent, and unreportable observations are
    mechanically neutral irrespective of their caller-supplied confidence fields.
    """

    return confidence.effective_confidence


def information_rubric_bits(prevalence: float) -> float:
    """Return capped rarity rubric bits, never probability bits."""

    if not math.isfinite(prevalence) or not 0.0 < prevalence <= 1.0:
        raise ValueError("prevalence must be finite and in (0, 1]")
    return min(INFORMATION_CAP_RUBRIC_BITS, -math.log2(prevalence))


def score_v4_3(
    scoring_input: V43ScoringInput,
    prevalence: ConditionalPrevalenceProvider,
) -> V43CandidateScore:
    """Score one candidate without concealed truth or candidate-pool frequencies."""

    provenance = prevalence.provenance
    try:
        _validate_prevalence_provenance(provenance)
    except AttributeError as exc:
        raise ValueError(
            "prevalence provenance lacks a mandatory verified artifact identity"
        ) from exc
    _validate_dependency_control(scoring_input.observations)

    grouped: dict[str, list[ObservationEvaluation]] = defaultdict(list)
    for observation in scoring_input.observations:
        grouped[observation.dependency_cluster].append(observation)
    cluster_contributions = tuple(
        _score_cluster(
            cluster_id,
            tuple(sorted(observations, key=lambda item: item.observation_id)),
            scoring_input.candidate_context,
            prevalence,
            provenance,
        )
        for cluster_id, observations in sorted(grouped.items())
    )
    evidence_total = math.fsum(item.evidence_rubric_bits for item in cluster_contributions)
    contradiction_total = math.fsum(
        item.contradiction_rubric_bits for item in cluster_contributions
    )
    confidence_total = math.fsum(
        item.effective_confidence for item in cluster_contributions
    )
    detailed_support = (
        100.0
        * math.fsum(
            item.effective_confidence * item.support for item in cluster_contributions
        )
        / confidence_total
        if confidence_total
        else 0.0
    )
    core_fit, core_blocks = _score_core_fit(scoring_input)
    return V43CandidateScore(
        scoring_engine_version=V43_SCORING_ENGINE_VERSION,
        rubric_unit=RUBRIC_UNIT,
        evidence_rubric_bits=evidence_total,
        contradiction_rubric_bits=contradiction_total,
        net_information=evidence_total - contradiction_total,
        detailed_support=detailed_support,
        core_fit=core_fit,
        meaningful_contradictions=sum(
            item.meaningful_contradiction for item in cluster_contributions
        ),
        clusters=cluster_contributions,
        core_blocks=core_blocks,
        prevalence_universe_sha256=provenance.universe_sha256,
        prevalence_policy_version=provenance.policy_version,
        prevalence_parent_hierarchy_sha256=provenance.parent_hierarchy_sha256,
    )


def _score_cluster(
    cluster_id: str,
    observations: tuple[ObservationEvaluation, ...],
    candidate_context: object,
    prevalence: ConditionalPrevalenceProvider,
    provenance: ConditionalPrevalenceProvenanceLike,
) -> DependencyClusterContribution:
    scored = tuple(
        _score_pathway(
            observation.observation_id,
            pathway,
            effective_confidence(observation.confidence),
            candidate_context,
            prevalence,
            provenance,
        )
        for observation in observations
        for pathway in sorted(observation.pathways, key=lambda item: item.pathway_id)
    )
    if not scored:
        ceff = max(
            (effective_confidence(observation.confidence) for observation in observations),
            default=0.0,
        )
        return DependencyClusterContribution(
            dependency_cluster=cluster_id,
            observation_ids=tuple(item.observation_id for item in observations),
            effective_confidence=ceff,
            evidence_pathway_id=None,
            support_pathway_id=None,
            contradiction_pathway_id=None,
            support=0.0,
            evidence_rubric_bits=0.0,
            contradiction_severity=0.0,
            contradiction_rubric_bits=0.0,
            meaningful_contradiction=False,
            pathways=(),
        )

    evidence_winner = min(
        scored,
        key=lambda item: (
            -item.evidence_rubric_bits,
            -item.pathway_support,
            item.observation_id,
            item.pathway_id,
        ),
    )
    # The dependency-controlled positive-evidence winner is also the observation
    # used in the DetailedSupport numerator and denominator.  Selecting a second
    # support-only winner would let one cluster borrow confidence from one
    # observation and support from another.
    positive_winner = evidence_winner if evidence_winner.evidence_rubric_bits > 0.0 else None
    support_winner = positive_winner or min(
        scored,
        key=lambda item: (
            -item.effective_confidence,
            -item.pathway_support,
            item.observation_id,
            item.pathway_id,
        ),
    )
    contradiction_winner = min(
        scored,
        key=lambda item: (
            -item.contradiction_rubric_bits,
            -item.contradiction_severity,
            item.observation_id,
            item.pathway_id,
        ),
    )
    return DependencyClusterContribution(
        dependency_cluster=cluster_id,
        observation_ids=tuple(item.observation_id for item in observations),
        effective_confidence=support_winner.effective_confidence,
        evidence_pathway_id=(
            f"{positive_winner.observation_id}:{positive_winner.pathway_id}"
            if positive_winner is not None
            else None
        ),
        support_pathway_id=f"{support_winner.observation_id}:{support_winner.pathway_id}",
        contradiction_pathway_id=(
            f"{contradiction_winner.observation_id}:{contradiction_winner.pathway_id}"
        ),
        support=support_winner.pathway_support,
        evidence_rubric_bits=evidence_winner.evidence_rubric_bits,
        contradiction_severity=contradiction_winner.contradiction_severity,
        contradiction_rubric_bits=contradiction_winner.contradiction_rubric_bits,
        meaningful_contradiction=any(
            item.contradiction_severity >= 0.50 for item in scored
        ),
        pathways=scored,
    )


def _score_pathway(
    observation_id: str,
    pathway: EvaluatedPathway,
    ceff: float,
    candidate_context: object,
    prevalence: ConditionalPrevalenceProvider,
    provenance: ConditionalPrevalenceProvenanceLike,
) -> PathwayContribution:
    primary = _score_anchor(
        pathway.primary,
        ceff,
        candidate_context,
        prevalence,
        provenance,
    )
    corroborator = (
        _score_anchor(
            pathway.corroborator,
            ceff,
            candidate_context,
            prevalence,
            provenance,
        )
        if primary is not None and pathway.corroborator is not None
        else None
    )
    primary_support = primary.support if primary is not None else 0.0
    corroborator_support = corroborator.support if corroborator is not None else 0.0
    pathway_support = min(
        1.0,
        primary_support + INDEPENDENT_CORROBORATION_CAP * corroborator_support,
    )
    primary_evidence = primary.evidence_rubric_bits if primary is not None else 0.0
    corroborator_evidence = (
        corroborator.evidence_rubric_bits if corroborator is not None else 0.0
    )
    contradiction_severity = pathway.contradiction.active_severity
    contradiction = ceff * contradiction_severity * CONTRADICTION_SCALE_RUBRIC_BITS
    return PathwayContribution(
        observation_id=observation_id,
        pathway_id=pathway.pathway_id,
        effective_confidence=ceff,
        pathway_support=pathway_support,
        evidence_rubric_bits=(
            primary_evidence + INDEPENDENT_CORROBORATION_CAP * corroborator_evidence
        ),
        primary=primary,
        corroborator=corroborator,
        contradiction_severity=contradiction_severity,
        contradiction_rubric_bits=contradiction,
    )


def _score_anchor(
    anchor: EvaluatedStructuralAnchor,
    ceff: float,
    candidate_context: object,
    prevalence: ConditionalPrevalenceProvider,
    provenance: ConditionalPrevalenceProvenanceLike,
) -> AnchorContribution | None:
    if anchor.support == 0.0:
        return None
    estimate = prevalence.estimate(anchor.anchor_id, candidate_context)
    try:
        _validate_prevalence_estimate(anchor.anchor_id, estimate, provenance)
    except AttributeError as exc:
        raise ValueError(
            "prevalence estimate lacks a mandatory verified artifact identity"
        ) from exc
    raw_bits = -math.log2(estimate.prevalence)
    capped_bits = information_rubric_bits(estimate.prevalence)
    evidence = ceff * anchor.support * anchor.flexibility_factor * capped_bits
    return AnchorContribution(
        anchor_id=anchor.anchor_id,
        structural_salience=anchor.structural_salience,
        directness_factor=anchor.directness_factor,
        flexibility_factor=anchor.flexibility_factor,
        support=anchor.support,
        prevalence=estimate.prevalence,
        raw_information_rubric_bits=raw_bits,
        capped_information_rubric_bits=capped_bits,
        evidence_rubric_bits=evidence,
        selected_level_id=estimate.selected_level_id,
        backoff_ordinal=estimate.backoff_ordinal,
        numerator_duration_microseconds=estimate.numerator_duration_microseconds,
        denominator_duration_microseconds=estimate.denominator_duration_microseconds,
        universe_sha256=estimate.universe_sha256,
        policy_version=estimate.policy_version,
        parent_hierarchy_sha256=estimate.parent_hierarchy_sha256,
    )


def _score_core_fit(
    scoring_input: V43ScoringInput,
) -> tuple[float, tuple[CoreBlockContribution, ...]]:
    if not math.isclose(math.fsum(CORE_BLOCK_WEIGHTS.values()), 100.0):
        raise RuntimeError("frozen V4.3 CoreFit weights must sum to 100")
    contributions: list[CoreBlockContribution] = []
    earned_points = 0.0
    available_points = 0.0
    for evaluation in sorted(scoring_input.core_blocks, key=lambda item: item.block.value):
        weight = CORE_BLOCK_WEIGHTS[evaluation.block]
        if evaluation.earned_fraction is None:
            contribution = CoreBlockContribution(
                block=evaluation.block,
                available=False,
                weight=weight,
                earned_fraction=None,
                earned_points=0.0,
            )
        else:
            points = weight * evaluation.earned_fraction
            earned_points += points
            available_points += weight
            contribution = CoreBlockContribution(
                block=evaluation.block,
                available=True,
                weight=weight,
                earned_fraction=evaluation.earned_fraction,
                earned_points=points,
            )
        contributions.append(contribution)
    core_fit = 100.0 * earned_points / available_points if available_points else 0.0
    return core_fit, tuple(contributions)


def _validate_dependency_control(
    observations: tuple[ObservationEvaluation, ...],
) -> None:
    clusters_by_dependency_key: dict[str, set[str]] = defaultdict(set)
    for observation in observations:
        for pathway in observation.pathways:
            for anchor in (
                pathway.primary,
                *((pathway.corroborator,) if pathway.corroborator is not None else ()),
            ):
                for key in anchor.dependency_keys:
                    clusters_by_dependency_key[key].add(observation.dependency_cluster)
    repeated = {
        key: tuple(sorted(cluster_ids))
        for key, cluster_ids in sorted(clusters_by_dependency_key.items())
        if len(cluster_ids) > 1
    }
    if repeated:
        raise ValueError(f"structural mechanisms reused across dependency clusters: {repeated}")


def _validate_prevalence_provenance(
    provenance: ConditionalPrevalenceProvenanceLike,
) -> None:
    for label, value in (
        ("prevalence artifact", provenance.artifact_sha256),
        ("prevalence plan", provenance.plan_sha256),
        ("prevalence mapping library", provenance.mapping_library_sha256),
        ("prevalence mapping source", provenance.mapping_source_library_sha256),
        ("prevalence mapping-derived plan", provenance.mapping_prevalence_plan_sha256),
        ("prevalence required-feature registry", provenance.required_feature_registry_sha256),
        ("prevalence cache manifest", provenance.cache_manifest_sha256),
        ("prevalence cache trust lock", provenance.cache_trust_lock_sha256),
        ("prevalence cache build plan", provenance.cache_build_plan_sha256),
        ("prevalence semantic registry", provenance.semantic_feature_registry_sha256),
        ("prevalence physical registry", provenance.physical_feature_registry_sha256),
        ("prevalence reconciliation", provenance.reconciliation_aggregate_sha256),
        ("prevalence engine validation", provenance.engine_validation_sha256),
        ("prevalence ephemeris file set", provenance.ephemeris_file_set_sha256),
        ("prevalence universe", provenance.universe_sha256),
        ("prevalence parent hierarchy", provenance.parent_hierarchy_sha256),
    ):
        _require_sha256(label, value)
    if provenance.anchor_ids != tuple(sorted(set(provenance.anchor_ids))):
        raise ValueError("prevalence anchor inventory must be sorted and unique")
    if not provenance.policy_version:
        raise ValueError("prevalence policy version must not be empty")
    if not provenance.boundary_policy_version:
        raise ValueError("prevalence boundary policy version must not be empty")
    if provenance.duration_weighted is not True:
        raise ValueError("prevalence must be duration weighted")
    if provenance.conditional is not True:
        raise ValueError("conditional prevalence policy must be active")
    if provenance.exact_stable_intervals is not True:
        raise ValueError("prevalence must use exact stable intervals")
    if provenance.source_scope != GLOBAL_PREVALENCE_SOURCE_SCOPE:
        raise ValueError("candidate-file prevalence is forbidden")


def _validate_prevalence_estimate(
    anchor_id: str,
    estimate: ConditionalPrevalenceEstimateLike,
    provenance: ConditionalPrevalenceProvenanceLike,
) -> None:
    if anchor_id not in provenance.anchor_ids:
        raise ValueError(f"prevalence anchor is absent from the frozen plan: {anchor_id}")
    if estimate.anchor_id != anchor_id:
        raise ValueError(f"prevalence provider returned {estimate.anchor_id} for {anchor_id}")
    if estimate.numerator_duration_microseconds <= 0:
        raise ValueError("a matched prevalence anchor requires positive numerator duration")
    if estimate.denominator_duration_microseconds <= 0:
        raise ValueError("prevalence denominator duration must be positive")
    if estimate.numerator_duration_microseconds > estimate.denominator_duration_microseconds:
        raise ValueError("prevalence numerator cannot exceed denominator")
    expected = (
        estimate.numerator_duration_microseconds / estimate.denominator_duration_microseconds
    )
    if not math.isfinite(estimate.prevalence) or not math.isclose(
        estimate.prevalence,
        expected,
        rel_tol=1e-15,
        abs_tol=0.0,
    ):
        raise ValueError("prevalence must equal its exact duration ratio")
    if not estimate.selected_level_id or estimate.backoff_ordinal < 0:
        raise ValueError("prevalence estimate requires a selected conditional/backoff level")
    for attribute in (
        "artifact_sha256",
        "plan_sha256",
        "mapping_library_sha256",
        "mapping_prevalence_plan_sha256",
        "required_feature_registry_sha256",
        "cache_manifest_sha256",
        "universe_sha256",
        "policy_version",
        "parent_hierarchy_sha256",
        "duration_weighted",
        "conditional",
        "exact_stable_intervals",
        "source_scope",
    ):
        if getattr(estimate, attribute) != getattr(provenance, attribute):
            raise ValueError(f"prevalence estimate/provenance mismatch: {attribute}")


def _require_sha256(label: str, value: str) -> None:
    if len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
        raise ValueError(f"{label} hash must be lowercase SHA-256")
