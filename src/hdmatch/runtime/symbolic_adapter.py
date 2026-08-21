"""Frozen response-generation and candidate-scoring adapters."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from hashlib import sha256
from pathlib import Path
from typing import Any, Final, Protocol

from hdmatch.model import MappingLibrary, load_mapping_library, score_symbolic
from hdmatch.model_b.mapping_library import FrozenModelB
from hdmatch.model_b_v2_new import MODEL_ID as _MODEL_B_V2_NEW_ID
from hdmatch.model_b_v2_new import FrozenModelBV2New, PreparedPrevalence
from hdmatch.schemas import BehavioralResponse, CandidateState, ChartFeatures, ScoredState

MODEL_A_ID = "MODEL-A-CORE-V1"
MODEL_B_ID = "MODEL-B-DETAILED-V1"
MODEL_B_V2_NEW_ID: Final[str] = _MODEL_B_V2_NEW_ID


class RuntimeSymbolicModel(Protocol):
    """Shared blind-safe interface for separately frozen symbolic models."""

    @property
    def model_id(self) -> str: ...

    @property
    def library(self) -> MappingLibrary: ...

    @property
    def model_sha256(self) -> str: ...

    @property
    def mapping_sha256(self) -> str: ...

    @property
    def question_bank_sha256(self) -> str: ...

    @property
    def capability_metadata(self) -> Mapping[str, object]: ...

    def score_signature(self, chart: ChartFeatures) -> tuple[Any, ...]: ...

    def oracle_responses(self, chart: ChartFeatures) -> Sequence[BehavioralResponse]: ...

    def answer_spaces(self) -> Mapping[str, Sequence[str]]: ...

    def score(
        self,
        state: CandidateState,
        responses: Iterable[BehavioralResponse],
        prevalence_by_anchor: Any,
    ) -> ScoredState: ...


class FrozenSymbolicModel:
    """One immutable model used by both synthetic generator and blind decoder."""

    def __init__(
        self,
        mapping_path: str | Path,
        *,
        model_id: str = MODEL_A_ID,
    ) -> None:
        self.mapping_path = Path(mapping_path)
        self.library = load_mapping_library(self.mapping_path)
        self._mapping_file_sha256 = sha256(self.mapping_path.read_bytes()).hexdigest()
        self._model_id = model_id

    @property
    def model_id(self) -> str:
        return self._model_id

    @property
    def model_sha256(self) -> str:
        return self.library.sha256()

    @property
    def mapping_sha256(self) -> str:
        return self._mapping_file_sha256

    @property
    def question_bank_sha256(self) -> str:
        return self.library.question_bank_sha256

    @property
    def capability_metadata(self) -> Mapping[str, object]:
        return {
            "behavioral_scoring": "frozen-core",
            "detailed_behavioral_mappings": "not-applicable",
        }

    def score_signature(self, chart: ChartFeatures) -> tuple[Any, ...]:
        return (
            chart.type,
            chart.strategy,
            chart.authority,
            chart.profile,
            chart.defined_centers,
        )

    def oracle_responses(self, chart: ChartFeatures) -> Sequence[BehavioralResponse]:
        canonical = self.library.canonical_answers(chart)
        responses: list[BehavioralResponse] = []
        question_clusters: dict[str, set[str]] = {}
        for mapping in self.library.frozen_mappings:
            for question_id in mapping.question_ids:
                question_clusters.setdefault(question_id, set()).add(mapping.dependency_cluster)
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


def load_runtime_model(
    model_id: str,
    *,
    model_a_mapping_path: str | Path,
    model_b_artifact_path: str | Path | None = None,
    model_b_v2_compiled_path: str | Path | None = None,
    model_b_v2_freeze_path: str | Path | None = None,
) -> RuntimeSymbolicModel:
    """Load one explicit model identity; never infer a favorable artifact."""

    if model_id == MODEL_A_ID:
        return FrozenSymbolicModel(model_a_mapping_path)
    if model_id == MODEL_B_ID:
        if model_b_artifact_path is None:
            raise ValueError("Model B requires an explicit frozen artifact path")
        return FrozenModelB(
            model_b_artifact_path,
            base_mapping_path=model_a_mapping_path,
        )
    if model_id == MODEL_B_V2_NEW_ID:
        if model_b_v2_compiled_path is None or model_b_v2_freeze_path is None:
            raise ValueError(
                "MODEL-B-DETAILED-V2-NEW requires explicit compiled and freeze artifacts"
            )
        return FrozenModelBV2New(
            model_b_v2_compiled_path,
            model_b_v2_freeze_path,
            base_mapping_path=model_a_mapping_path,
        )
    raise ValueError(f"unsupported symbolic model ID: {model_id}")


def prepare_runtime_prevalence(
    model: RuntimeSymbolicModel,
    states: Sequence[CandidateState],
) -> Mapping[str, float] | PreparedPrevalence:
    """Prepare the model-specific public prevalence context.

    Model A and structural-only Model B V1 retain their existing flat
    candidate-universe prevalence.  The prospective V2 model fails closed on a
    typed context prepared from the complete exact reference universe.
    """

    if isinstance(model, FrozenModelBV2New):
        return model.prepare_prevalence(states)
    return candidate_prevalence(states, model.library)


def runtime_model_public_paths(model: RuntimeSymbolicModel) -> tuple[Path, ...]:
    """Return additional public model inputs that recovery must preflight."""

    if isinstance(model, FrozenModelBV2New):
        return (model.compiled_artifact_path, model.freeze_receipt_path)
    return ()


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
