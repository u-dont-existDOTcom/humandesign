"""Pure, deterministic V4/V3.2 detailed scoring for Model B.

This scorer consumes candidate-local rule evaluations and frozen reference-universe
prevalence.  It has no answer-key or candidate-truth input.  Its information values
are symbolic rubric bits and are deliberately not exposed as probabilities.
"""

from __future__ import annotations

import math
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass

from hdmatch.model_b.types import (
    MODEL_B_SCORING_VERSION,
    RUBRIC_UNIT,
    CompiledDetailedRule,
    ConditionalPrevalenceProvider,
    EvaluatedPathway,
    PrevalenceEstimateLike,
    StructuralEvidence,
)

INFORMATION_CAP_RUBRIC_BITS = 6.0
CONTRADICTION_CAP_RUBRIC_BITS = 4.0
INDEPENDENT_CORROBORATION_CAP = 0.15


@dataclass(frozen=True, slots=True)
class AnchorContribution:
    anchor_id: str
    support: float
    prevalence: float
    information_rubric_bits: float
    weighted_evidence_rubric_bits: float
    universe_id: str
    universe_sha256: str
    selected_denominator_level: str
    numerator_duration_seconds: float
    denominator_duration_seconds: float
    duration_weighted: bool
    segmentation: str


@dataclass(frozen=True, slots=True)
class PathwayContribution:
    rule_id: str
    pathway_id: str
    dependency_cluster: str
    effective_confidence: float
    support: float
    evidence_rubric_bits: float
    primary: AnchorContribution | None
    corroborator: AnchorContribution | None
    contradiction_severity: float
    contradiction_rubric_bits: float


@dataclass(frozen=True, slots=True)
class ClusterContribution:
    dependency_cluster: str
    effective_confidence: float
    evidence_pathway_id: str
    support_pathway_id: str
    contradiction_pathway_id: str
    support: float
    evidence_rubric_bits: float
    contradiction_severity: float
    contradiction_rubric_bits: float
    evaluated_pathways: tuple[PathwayContribution, ...]


@dataclass(frozen=True, slots=True)
class DetailedSymbolicScore:
    """Transparent Model B score; rubric bits are not probability bits."""

    model_version: str
    rubric_unit: str
    evidence_rubric_bits: float
    contradiction_rubric_bits: float
    net_rubric_bits: float
    detailed_support: float
    meaningful_contradictions: int
    clusters: tuple[ClusterContribution, ...]


def information_rubric_bits(prevalence: float) -> float:
    """Apply the frozen six-rubric-bit cap, including exact zero prevalence."""

    if not math.isfinite(prevalence) or not 0.0 <= prevalence <= 1.0:
        raise ValueError("prevalence must be finite and in [0, 1]")
    if prevalence == 0.0:
        return INFORMATION_CAP_RUBRIC_BITS
    return min(INFORMATION_CAP_RUBRIC_BITS, -math.log2(prevalence))


def evaluate_compiled_rules(
    chart: object,
    responses: object,
    rules: Iterable[CompiledDetailedRule],
) -> tuple[EvaluatedPathway, ...]:
    """Evaluate compiler-owned frozen rules in a deterministic rule-ID order."""

    ordered = sorted(rules, key=lambda rule: rule.rule_id)
    if len({rule.rule_id for rule in ordered}) != len(ordered):
        raise ValueError("compiled Model B rule IDs must be unique")
    return tuple(
        pathway
        for rule in ordered
        for pathway in sorted(rule.evaluate(chart, responses), key=_pathway_identity)
    )


def score_detailed_symbolic(
    chart: object,
    pathways: Iterable[EvaluatedPathway],
    prevalence: ConditionalPrevalenceProvider,
) -> DetailedSymbolicScore:
    """Score candidate-local frozen evaluations with conditional rarity.

    Unsupported structures add no evidence and no contradiction.  Contradiction is
    charged only when the frozen evaluator supplies an explicit nonzero severity.
    """

    ordered_pathways = tuple(sorted(pathways, key=_pathway_identity))
    _validate_dependency_control(ordered_pathways)
    prevalence_universes: set[tuple[str, str]] = set()
    grouped: dict[str, list[EvaluatedPathway]] = defaultdict(list)
    for pathway in ordered_pathways:
        grouped[pathway.dependency_cluster].append(pathway)

    cluster_results: list[ClusterContribution] = []
    for cluster_id in sorted(grouped):
        cluster_pathways = grouped[cluster_id]
        confidence_values = {item.effective_confidence for item in cluster_pathways}
        if len(confidence_values) != 1:
            raise ValueError(
                "alternative pathways in one dependency cluster must share one "
                f"effective confidence: {cluster_id}"
            )
        cluster_confidence = next(iter(confidence_values))
        scored = tuple(
            _score_pathway(item, prevalence, chart, prevalence_universes)
            for item in cluster_pathways
        )
        evidence_winner = min(
            scored,
            key=lambda item: (-item.evidence_rubric_bits, -item.support, item.pathway_id),
        )
        support_winner = min(
            scored,
            key=lambda item: (-item.support, -item.evidence_rubric_bits, item.pathway_id),
        )
        contradiction_winner = min(
            scored,
            key=lambda item: (
                -item.contradiction_rubric_bits,
                -item.contradiction_severity,
                item.pathway_id,
            ),
        )
        cluster_results.append(
            ClusterContribution(
                dependency_cluster=cluster_id,
                effective_confidence=cluster_confidence,
                evidence_pathway_id=evidence_winner.pathway_id,
                support_pathway_id=support_winner.pathway_id,
                contradiction_pathway_id=contradiction_winner.pathway_id,
                support=support_winner.support,
                evidence_rubric_bits=evidence_winner.evidence_rubric_bits,
                contradiction_severity=contradiction_winner.contradiction_severity,
                contradiction_rubric_bits=contradiction_winner.contradiction_rubric_bits,
                evaluated_pathways=scored,
            )
        )

    clusters = tuple(cluster_results)
    _validate_common_prevalence_provenance(prevalence_universes)
    evidence_total = math.fsum(item.evidence_rubric_bits for item in clusters)
    contradiction_total = math.fsum(item.contradiction_rubric_bits for item in clusters)
    confidence_total = math.fsum(item.effective_confidence for item in clusters)
    detailed_support = (
        100.0
        * math.fsum(item.effective_confidence * item.support for item in clusters)
        / confidence_total
        if confidence_total
        else 0.0
    )
    return DetailedSymbolicScore(
        model_version=MODEL_B_SCORING_VERSION,
        rubric_unit=RUBRIC_UNIT,
        evidence_rubric_bits=evidence_total,
        contradiction_rubric_bits=contradiction_total,
        net_rubric_bits=evidence_total - contradiction_total,
        detailed_support=detailed_support,
        meaningful_contradictions=sum(item.contradiction_severity >= 0.50 for item in clusters),
        clusters=clusters,
    )


def _score_pathway(
    pathway: EvaluatedPathway,
    prevalence: ConditionalPrevalenceProvider,
    chart_context: object,
    prevalence_universes: set[tuple[str, str]],
) -> PathwayContribution:
    primary = _anchor_contribution(
        pathway.primary,
        pathway.effective_confidence,
        prevalence,
        chart_context,
        prevalence_universes,
    )
    independent = tuple(
        item
        for item in pathway.corroborators
        if _structural_dependency_keys(item).isdisjoint(
            _structural_dependency_keys(pathway.primary)
        )
    )
    corroborator_contributions = tuple(
        _anchor_contribution(
            item,
            pathway.effective_confidence,
            prevalence,
            chart_context,
            prevalence_universes,
        )
        for item in independent
    )
    eligible_corroborators = tuple(item for item in corroborator_contributions if item is not None)
    corroborator = (
        min(
            eligible_corroborators,
            key=lambda item: (
                -item.support,
                -item.weighted_evidence_rubric_bits,
                item.anchor_id,
            ),
        )
        if eligible_corroborators
        else None
    )
    primary_support = primary.support if primary is not None else 0.0
    corroborator_support = corroborator.support if corroborator is not None else 0.0
    support = min(
        1.0,
        primary_support + INDEPENDENT_CORROBORATION_CAP * corroborator_support,
    )
    primary_bits = primary.weighted_evidence_rubric_bits if primary is not None else 0.0
    corroborator_bits = (
        corroborator.weighted_evidence_rubric_bits if corroborator is not None else 0.0
    )
    contradiction_bits = (
        pathway.effective_confidence
        * pathway.contradiction_severity
        * CONTRADICTION_CAP_RUBRIC_BITS
    )
    return PathwayContribution(
        rule_id=pathway.rule_id,
        pathway_id=pathway.pathway_id,
        dependency_cluster=pathway.dependency_cluster,
        effective_confidence=pathway.effective_confidence,
        support=support,
        evidence_rubric_bits=(primary_bits + INDEPENDENT_CORROBORATION_CAP * corroborator_bits),
        primary=primary,
        corroborator=corroborator,
        contradiction_severity=pathway.contradiction_severity,
        contradiction_rubric_bits=contradiction_bits,
    )


def _anchor_contribution(
    evidence: StructuralEvidence,
    effective_confidence: float,
    prevalence_provider: ConditionalPrevalenceProvider,
    chart_context: object,
    prevalence_universes: set[tuple[str, str]],
) -> AnchorContribution | None:
    if evidence.support == 0.0:
        return None
    estimate = prevalence_provider.estimate(evidence.anchor_id, chart_context)
    _validate_estimate(evidence.anchor_id, estimate)
    prevalence_universes.add((estimate.universe_id, estimate.universe_sha256))
    bits = information_rubric_bits(estimate.prevalence)
    weighted = effective_confidence * evidence.support * bits
    return AnchorContribution(
        anchor_id=evidence.anchor_id,
        support=evidence.support,
        prevalence=estimate.prevalence,
        information_rubric_bits=bits,
        weighted_evidence_rubric_bits=weighted,
        universe_id=estimate.universe_id,
        universe_sha256=estimate.universe_sha256,
        selected_denominator_level=estimate.selected_level_id,
        numerator_duration_seconds=estimate.numerator_duration_seconds,
        denominator_duration_seconds=estimate.denominator_duration_seconds,
        duration_weighted=estimate.duration_weighted,
        segmentation=estimate.segmentation,
    )


def _validate_estimate(anchor_id: str, estimate: PrevalenceEstimateLike) -> None:
    if estimate.anchor_id != anchor_id:
        raise ValueError(
            f"prevalence provider returned anchor {estimate.anchor_id} for {anchor_id}"
        )
    if estimate.denominator_duration_seconds <= 0.0:
        raise ValueError(f"prevalence denominator must be positive for {anchor_id}")
    if not estimate.universe_id:
        raise ValueError(f"prevalence universe ID must not be empty for {anchor_id}")
    if len(estimate.universe_sha256) != 64 or any(
        character not in "0123456789abcdef" for character in estimate.universe_sha256
    ):
        raise ValueError(f"prevalence universe hash must be lowercase SHA-256 for {anchor_id}")
    if not 0.0 <= estimate.numerator_duration_seconds <= estimate.denominator_duration_seconds:
        raise ValueError(f"invalid prevalence duration ratio for {anchor_id}")
    ratio = estimate.numerator_duration_seconds / estimate.denominator_duration_seconds
    if not math.isclose(ratio, estimate.prevalence, rel_tol=1e-12, abs_tol=1e-15):
        raise ValueError(f"prevalence does not equal duration ratio for {anchor_id}")
    if estimate.duration_weighted is not True:
        raise ValueError(f"prevalence must be duration weighted for {anchor_id}")
    if estimate.segmentation != "exact-boundary-events":
        raise ValueError(f"prevalence must use exact boundary segmentation for {anchor_id}")


def _validate_common_prevalence_provenance(
    universes: set[tuple[str, str]],
) -> None:
    if len(universes) > 1:
        raise ValueError("one Model B score cannot mix prevalence reference universes")


def _validate_dependency_control(pathways: tuple[EvaluatedPathway, ...]) -> None:
    clusters_by_key: dict[str, set[str]] = defaultdict(set)
    for pathway in pathways:
        structures = (pathway.primary, *pathway.corroborators)
        for structure in structures:
            for key in _structural_dependency_keys(structure):
                clusters_by_key[key].add(pathway.dependency_cluster)
    reused = {
        key: tuple(sorted(clusters))
        for key, clusters in sorted(clusters_by_key.items())
        if len(clusters) > 1
    }
    if reused:
        raise ValueError(f"structural dependencies reused across clusters: {reused}")


def _structural_dependency_keys(evidence: StructuralEvidence) -> frozenset[str]:
    """Always include exact-anchor identity even if a compiler dependency is incomplete."""

    return frozenset((*evidence.dependency_keys, f"anchor:{evidence.anchor_id}"))


def _pathway_identity(pathway: EvaluatedPathway) -> tuple[str, str, str]:
    return pathway.dependency_cluster, pathway.pathway_id, pathway.rule_id
