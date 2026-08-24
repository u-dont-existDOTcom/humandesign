"""Composite Model B loader shared by synthetic generation and blind recovery."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from hashlib import sha256
from pathlib import Path
from typing import Any

from hdmatch.model import MappingLibrary, load_mapping_library, score_symbolic
from hdmatch.model_b.artifacts import DetailedAnchor, load_model_b_artifact
from hdmatch.model_b.predicates import detailed_feature_sha256, extract_detailed_anchors
from hdmatch.schemas import BehavioralResponse, CandidateState, ChartFeatures, ScoredState
from hdmatch.util import sha256_file, sha256_json


class FrozenModelB:
    """One frozen composite consumed by both generator and decoder.

    Model A remains an unchanged dependency.  Detailed anchors are extracted and
    committed, but no detailed questionnaire contribution is added while all Model B
    behavioral mappings remain unresolved.
    """

    model_id = "MODEL-B-DETAILED-V1"
    detailed_scoring_status = "unresolved"

    def __init__(
        self,
        artifact_path: str | Path,
        *,
        base_mapping_path: str | Path | None = None,
        project_root: str | Path | None = None,
    ) -> None:
        self.artifact_path = Path(artifact_path)
        self.artifact = load_model_b_artifact(self.artifact_path)
        self.project_root = (
            Path(project_root) if project_root is not None else self.artifact_path.parents[1]
        )
        for source in self.artifact.source_artifacts:
            source_path = self.project_root / source.path
            if not source_path.is_file():
                raise ValueError(f"Model B frozen source is missing: {source.path}")
            if sha256_file(source_path) != source.sha256:
                raise ValueError(f"Model B frozen source hash mismatch: {source.path}")
        if base_mapping_path is None:
            candidate = self.project_root / self.artifact.base_mapping_path
            base_mapping_path = candidate
        self.base_mapping_path = Path(base_mapping_path)
        base_file_hash = sha256(self.base_mapping_path.read_bytes()).hexdigest()
        if base_file_hash != self.artifact.base_mapping_sha256:
            raise ValueError("Model A mapping hash does not match the dependency frozen by Model B")
        self.base_library: MappingLibrary = load_mapping_library(self.base_mapping_path)
        if self.base_library.question_bank_sha256 != self.artifact.question_bank_sha256:
            raise ValueError(
                "Model A question-bank hash does not match the dependency frozen by Model B"
            )
        self._artifact_file_sha256 = sha256(self.artifact_path.read_bytes()).hexdigest()

    @property
    def model_sha256(self) -> str:
        return sha256_json(
            {
                "model_id": self.model_id,
                "artifact_semantic_sha256": self.artifact.sha256(),
                "base_model_semantic_sha256": self.base_library.sha256(),
                "detailed_scoring_status": self.detailed_scoring_status,
            }
        )

    @property
    def mapping_sha256(self) -> str:
        return self._artifact_file_sha256

    @property
    def question_bank_sha256(self) -> str:
        return self.artifact.question_bank_sha256

    @property
    def library(self) -> MappingLibrary:
        """The frozen supported behavioral layer used by the composite."""

        return self.base_library

    @property
    def capability_metadata(self) -> Mapping[str, object]:
        return {
            "behavioral_scoring": "model-a-base-only",
            "detailed_behavioral_mappings": self.detailed_scoring_status,
            "unresolved_detailed_mapping_count": len(self.artifact.behavioral_mappings),
        }

    def score_signature(self, chart: ChartFeatures) -> tuple[Any, ...]:
        return (
            chart.type,
            chart.strategy,
            chart.authority,
            chart.profile,
            chart.defined_centers,
            detailed_feature_sha256(chart, self.artifact),
        )

    def detailed_anchors(self, chart: Mapping[str, object] | object) -> tuple[DetailedAnchor, ...]:
        return extract_detailed_anchors(chart, self.artifact)

    def canonical_answers(self, chart: Mapping[str, object] | object) -> dict[str, str]:
        """Return only sourced answers; unresolved detailed anchors add no answer."""

        return self.base_library.canonical_answers(chart)

    def oracle_responses(self, chart: ChartFeatures) -> Sequence[BehavioralResponse]:
        canonical = self.canonical_answers(chart)
        question_clusters: dict[str, set[str]] = {}
        for mapping in self.base_library.frozen_mappings:
            for question_id in mapping.question_ids:
                question_clusters.setdefault(question_id, set()).add(mapping.dependency_cluster)
        return tuple(
            BehavioralResponse(
                question_id=question_id,
                cluster_id="+".join(sorted(clusters)),
                answer=canonical.get(question_id, "unknown"),
                behavioral_confidence=1.0,
                measurement_reliability=1.0,
            )
            for question_id, clusters in sorted(question_clusters.items())
        )

    def answer_spaces(self) -> Mapping[str, Sequence[str]]:
        return {
            spec.question_id: tuple(
                dict.fromkeys((*[option.token for option in spec.options], "unknown"))
            )
            for spec in self.base_library.answer_specs
        }

    def score(
        self,
        state: CandidateState,
        responses: Iterable[BehavioralResponse],
        prevalence_by_anchor: Mapping[str, float],
    ) -> ScoredState:
        """Score sourced Model A mappings while detailed mappings remain unresolved."""

        result = score_symbolic(
            state.chart_features,
            responses,
            self.base_library,
            prevalence_by_anchor,
        )
        return ScoredState(
            state_id=state.state_id,
            net_rubric_bits=result.net_rubric_bits,
            evidence_rubric_bits=result.evidence_rubric_bits,
            contradiction_rubric_bits=result.contradiction_rubric_bits,
            detailed_support=result.detailed_support,
            core_fit=result.core_fit,
            meaningful_contradictions=result.meaningful_contradictions,
        )
