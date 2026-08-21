"""Pure V4/V3 symbolic support, contradiction, and rubric-bit scoring."""

from __future__ import annotations

import math
from collections import defaultdict
from collections.abc import Iterable, Mapping
from typing import Any, Protocol

from pydantic import BaseModel, ConfigDict, Field

from hdmatch.model.dependencies import (
    ClusterContribution,
    collapse_dependency_clusters,
    validate_dependency_control,
)
from hdmatch.model.mapping_library import MappingLibrary, StructuralClass
from hdmatch.questionnaire.response import NormalizedResponse, normalize_answer_token


class ScoredCluster(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    cluster_id: str
    mapping_id: str
    anchor_id: str
    effective_confidence: float = Field(ge=0.0, le=1.0)
    support: float = Field(ge=0.0, le=1.0)
    evidence_rubric_bits: float = Field(ge=0.0)
    contradiction_severity: float = Field(ge=0.0, le=1.0)
    contradiction_rubric_bits: float = Field(ge=0.0)


class SymbolicScore(BaseModel):
    """A transparent rubric result; no field is a probability."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    evidence_rubric_bits: float
    contradiction_rubric_bits: float
    net_rubric_bits: float
    detailed_support: float = Field(ge=0.0, le=100.0)
    core_fit: float = Field(ge=0.0, le=100.0)
    meaningful_contradictions: int = Field(ge=0)
    scored_clusters: tuple[ScoredCluster, ...]
    unresolved_question_ids: tuple[str, ...]


class BehavioralResponseLike(Protocol):
    question_id: str
    answer: str
    behavioral_confidence: float
    measurement_reliability: float


def information_bits(prevalence: float, *, cap: float = 6.0) -> float:
    """Convert duration-weighted prevalence to capped symbolic rubric bits."""

    if not 0.0 < prevalence <= 1.0:
        raise ValueError("prevalence must be in (0, 1]")
    return min(cap, -math.log2(prevalence))


def score_symbolic(
    chart: Mapping[str, Any] | object,
    responses: Iterable[NormalizedResponse | BehavioralResponseLike],
    library: MappingLibrary,
    prevalence_by_anchor: Mapping[str, float],
) -> SymbolicScore:
    """Score one chart using only frozen mappings and observed response tokens.

    Missing structures are neutral. A contradiction is applied only when a frozen rule
    explicitly names the observed answer as behaviorally opposing the chart predicate.
    """

    validate_dependency_control(library)
    normalized = tuple(_coerce_response(response) for response in responses)
    mappings_by_question: dict[str, list[Any]] = defaultdict(list)
    for mapping in library.frozen_mappings:
        for question_id in mapping.question_ids:
            mappings_by_question[question_id].append(mapping)

    raw_contributions: list[ClusterContribution] = []
    unresolved_questions: set[str] = set()
    cluster_confidence: dict[str, float] = defaultdict(float)
    core_support: dict[StructuralClass, list[tuple[str, float, float]]] = defaultdict(list)

    for response in normalized:
        question_mappings = mappings_by_question.get(response.question_id, [])
        if not question_mappings:
            unresolved_questions.add(response.question_id)
            continue

        for mapping in question_mappings:
            cluster_confidence[mapping.dependency_cluster] = max(
                cluster_confidence[mapping.dependency_cluster], response.effective_confidence
            )
            assert mapping.chart_feature_predicate is not None
            assert mapping.predicted_response is not None
            assert mapping.structural_salience is not None
            assert mapping.mapping_directness is not None
            assert mapping.structural_class is not None
            predicate_matches = mapping.chart_feature_predicate.matches(chart)
            support = 0.0
            evidence = 0.0
            contradiction_severity = 0.0
            contradiction = 0.0
            if predicate_matches:
                if response.answer_token in mapping.predicted_response.support_answer_tokens:
                    support = min(1.0, mapping.structural_salience * mapping.mapping_directness)
                    if mapping.anchor_id not in prevalence_by_anchor:
                        raise KeyError(f"missing prevalence for anchor {mapping.anchor_id}")
                    bits = information_bits(
                        prevalence_by_anchor[mapping.anchor_id],
                        cap=library.constants.information_cap_rubric_bits,
                    )
                    evidence = response.effective_confidence * support * bits
                if (
                    mapping.contradiction_rule is not None
                    and response.answer_token in mapping.contradiction_rule.answer_tokens
                ):
                    contradiction_severity = float(mapping.contradiction_rule.severity)
                    contradiction = (
                        response.effective_confidence
                        * contradiction_severity
                        * library.constants.contradiction_cap_rubric_bits
                    )
            core_support[mapping.structural_class].append(
                (
                    mapping.dependency_cluster,
                    mapping.mapping_directness if support else 0.0,
                    response.effective_confidence,
                )
            )
            raw_contributions.append(
                ClusterContribution(
                    cluster_id=mapping.dependency_cluster,
                    mapping_id=mapping.mapping_id,
                    anchor_id=mapping.anchor_id,
                    effective_confidence=response.effective_confidence,
                    support=support,
                    evidence_rubric_bits=evidence,
                    contradiction_severity=contradiction_severity,
                    contradiction_rubric_bits=contradiction,
                )
            )

    collapsed = collapse_dependency_clusters(raw_contributions)
    scored_clusters = tuple(
        ScoredCluster(
            cluster_id=item.cluster_id,
            mapping_id=item.mapping_id,
            anchor_id=item.anchor_id,
            effective_confidence=item.effective_confidence,
            support=item.support,
            evidence_rubric_bits=item.evidence_rubric_bits,
            contradiction_severity=item.contradiction_severity,
            contradiction_rubric_bits=item.contradiction_rubric_bits,
        )
        for item in collapsed
    )
    evidence_total = sum(item.evidence_rubric_bits for item in collapsed)
    contradiction_total = sum(item.contradiction_rubric_bits for item in collapsed)
    detailed_denominator = sum(cluster_confidence.values())
    detailed_numerator = sum(
        cluster_confidence[item.cluster_id] * item.support for item in collapsed
    )
    detailed_support = (
        100.0 * detailed_numerator / detailed_denominator if detailed_denominator else 0.0
    )
    core_fit = _core_fit(core_support, library)
    return SymbolicScore(
        evidence_rubric_bits=evidence_total,
        contradiction_rubric_bits=contradiction_total,
        net_rubric_bits=evidence_total - contradiction_total,
        detailed_support=detailed_support,
        core_fit=core_fit,
        meaningful_contradictions=sum(item.contradiction_severity >= 0.50 for item in collapsed),
        scored_clusters=scored_clusters,
        unresolved_question_ids=tuple(sorted(unresolved_questions)),
    )


def _coerce_response(
    response: NormalizedResponse | BehavioralResponseLike,
) -> NormalizedResponse:
    if isinstance(response, NormalizedResponse):
        return response
    question_id = response.question_id
    answer_token = normalize_answer_token(response.answer)
    return NormalizedResponse(
        question_id=str(question_id),
        answer_token=answer_token,
        behavioral_confidence=float(response.behavioral_confidence),
        measurement_reliability=float(response.measurement_reliability),
    )


def _core_fit(
    contributions: Mapping[StructuralClass, list[tuple[str, float, float]]],
    library: MappingLibrary,
) -> float:
    block_for_class = {
        StructuralClass.TYPE_STRATEGY: "type_strategy",
        StructuralClass.AUTHORITY: "authority",
        StructuralClass.DIAGNOSTIC_CENTER: "diagnostic_centers",
        StructuralClass.PROFILE: "profile",
    }
    earned = 0.0
    available = 0.0
    for structural_class, block_name in block_for_class.items():
        values = contributions.get(structural_class, [])
        if not values:
            continue
        by_cluster: dict[str, tuple[float, float]] = {}
        for cluster_id, support, confidence in values:
            current = by_cluster.get(cluster_id, (0.0, 0.0))
            by_cluster[cluster_id] = (max(current[0], support), max(current[1], confidence))
        confidence_total = sum(confidence for _, confidence in by_cluster.values())
        if confidence_total == 0.0:
            continue
        fraction = (
            sum(support * confidence for support, confidence in by_cluster.values())
            / confidence_total
        )
        weight = library.constants.core_weights[block_name]
        earned += weight * fraction
        available += weight
    return 100.0 * earned / available if available else 0.0
