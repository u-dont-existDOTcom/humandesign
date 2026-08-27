"""Frozen response-generation and candidate-scoring adapters."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from hashlib import sha256
from pathlib import Path

from hdmatch.model import MappingLibrary, load_mapping_library, score_symbolic
from hdmatch.schemas import (
    BehavioralResponse,
    CandidateState,
    ChartFeatures,
    ScoredState,
    StructuralChartFeatures,
)

ScoreSignature = tuple[str, str, str, str, tuple[str, ...]]
ChartLike = ChartFeatures | StructuralChartFeatures


class FrozenSymbolicModel:
    """One immutable model used by both synthetic generator and blind decoder."""

    def __init__(self, mapping_path: str | Path) -> None:
        self.mapping_path = Path(mapping_path)
        self.library = load_mapping_library(self.mapping_path)
        self._mapping_file_sha256 = sha256(self.mapping_path.read_bytes()).hexdigest()

    @property
    def model_sha256(self) -> str:
        return self.library.sha256()

    @property
    def mapping_sha256(self) -> str:
        return self._mapping_file_sha256

    @property
    def question_bank_sha256(self) -> str:
        return self.library.question_bank_sha256

    @staticmethod
    def scoring_signature(chart: ChartLike) -> ScoreSignature:
        """Return every chart field the frozen predicate schema can currently see.

        MappingLibrary v1 predicates are intentionally limited to type, strategy,
        authority, profile and defined-center membership.  Gates/channels remain in
        the century cache for structural audit and future model versions, but they
        cannot change the present symbolic score.  If the predicate schema expands,
        this signature must expand in the same model-version change.
        """

        return (
            chart.type,
            chart.strategy,
            chart.authority,
            chart.profile,
            tuple(sorted(chart.defined_centers)),
        )

    def oracle_responses(
        self,
        chart: ChartLike,
    ) -> Sequence[BehavioralResponse]:
        canonical = self.library.canonical_answers(chart)
        responses: list[BehavioralResponse] = []
        question_clusters: dict[str, set[str]] = {}
        for mapping in self.library.frozen_mappings:
            for question_id in mapping.question_ids:
                question_clusters.setdefault(question_id, set()).add(
                    mapping.dependency_cluster
                )
        for question_id, cluster_set in sorted(question_clusters.items()):
            answer = canonical.get(question_id, "unknown")
            clusters = sorted(cluster_set)
            responses.append(
                BehavioralResponse(
                    question_id=question_id,
                    cluster_id="+".join(clusters),
                    answer=answer,
                    behavioral_confidence=1.0,
                    measurement_reliability=1.0,
                )
            )
        return tuple(responses)

    def answer_spaces(self) -> Mapping[str, Sequence[str]]:
        return {
            spec.question_id: tuple(
                dict.fromkeys((*[option.token for option in spec.options], "unknown"))
            )
            for spec in self.library.answer_specs
        }

    def score(
        self,
        state: CandidateState,
        responses: Iterable[BehavioralResponse],
        prevalence_by_anchor: Mapping[str, float],
    ) -> ScoredState:
        score = score_symbolic(
            state.chart_features,
            responses,
            self.library,
            prevalence_by_anchor,
        )
        return ScoredState(
            state_id=state.state_id,
            net_rubric_bits=score.net_rubric_bits,
            evidence_rubric_bits=score.evidence_rubric_bits,
            contradiction_rubric_bits=score.contradiction_rubric_bits,
            detailed_support=score.detailed_support,
            core_fit=score.core_fit,
            meaningful_contradictions=score.meaningful_contradictions,
        )


def candidate_prevalence(
    states: Iterable[CandidateState], library: MappingLibrary
) -> dict[str, float]:
    """Compute duration-weighted prevalence once per model-visible signature.

    Repeated century intervals often differ in gates or exact timing while being
    identical to the current MappingLibrary predicate surface.  Aggregating their
    duration first is mathematically identical to testing every interval separately
    and avoids millions of redundant predicate evaluations.
    """

    grouped: dict[ScoreSignature, tuple[float, ChartLike]] = {}
    total = 0.0
    for state in states:
        duration = (state.end_utc - state.start_utc).total_seconds()
        if duration <= 0.0:
            continue
        total += duration
        chart = state.chart_features
        signature = _scoring_signature(chart)
        previous = grouped.get(signature)
        if previous is None:
            grouped[signature] = (duration, chart)
        else:
            grouped[signature] = (previous[0] + duration, previous[1])
    if total <= 0.0:
        raise ValueError("candidate universe must contain positive duration")

    anchors: dict[str, float] = {}
    for mapping in library.frozen_mappings:
        if mapping.anchor_id in anchors:
            continue
        assert mapping.chart_feature_predicate is not None
        matching = sum(
            duration
            for duration, chart in grouped.values()
            if mapping.chart_feature_predicate.matches(chart)
        )
        if matching > 0.0:
            anchors[mapping.anchor_id] = matching / total
    return anchors


def _scoring_signature(chart: ChartLike) -> ScoreSignature:
    return (
        chart.type,
        chart.strategy,
        chart.authority,
        chart.profile,
        tuple(sorted(chart.defined_centers)),
    )
