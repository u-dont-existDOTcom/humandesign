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

    def oracle_responses(
        self,
        chart: ChartFeatures | StructuralChartFeatures,
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
    """Compute duration-weighted structural prevalence in a declared universe.

    These values weight the symbolic rubric. They are not probabilities of a
    candidate being true, and are never estimated from answer keys.
    """

    state_tuple = tuple(states)
    total = sum((state.end_utc - state.start_utc).total_seconds() for state in state_tuple)
    if total <= 0.0:
        raise ValueError("candidate universe must contain positive duration")
    anchors: dict[str, float] = {}
    for mapping in library.frozen_mappings:
        if mapping.anchor_id in anchors:
            continue
        assert mapping.chart_feature_predicate is not None
        matching = sum(
            (state.end_utc - state.start_utc).total_seconds()
            for state in state_tuple
            if mapping.chart_feature_predicate.matches(state.chart_features)
        )
        if matching > 0.0:
            anchors[mapping.anchor_id] = matching / total
    return anchors
