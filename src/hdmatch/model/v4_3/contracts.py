"""Interpretation-free contracts for the canonical V4.3 scoring engine.

The future mapping-library-v2 compiler owns behavioral meanings and chart
predicates.  It must collapse repeated questions into one dependency-cluster
evaluation before adapting them to these records.  The scorer never imports a
legacy mapping type and never receives concealed truth or answer-key data.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Final, Protocol, runtime_checkable

V43_PROTOCOL_VERSION = "V4.3"
V43_SCORING_ENGINE_VERSION = "v4.3-exact-symbolic-score-v1"
V43_RANKING_POLICY_VERSION = "v4.3-lexicographic-rank-v1"
MAPPING_LIBRARY_V2_SCHEMA = "mapping-library-v2"
RUBRIC_UNIT = "rubric_bits"
INFORMATION_CAP_RUBRIC_BITS = 6.0
CONTRADICTION_SCALE_RUBRIC_BITS = 4.0
INDEPENDENT_CORROBORATION_CAP = 0.15


class StructuralClass(StrEnum):
    TYPE_STRATEGY = "type_strategy"
    AUTHORITY = "authority"
    DIAGNOSTIC_CENTER = "diagnostic_center"
    PROFILE = "profile"
    COMPLETE_CHANNEL = "complete_channel"
    CARDINAL_SUN_EARTH = "cardinal_sun_earth"
    DEFINITION = "definition"
    REPEATED_GATE_OR_NODE = "repeated_gate_or_node"
    PROMINENT_PLANETARY_ACTIVATION = "prominent_planetary_activation"
    ORDINARY_HANGING_GATE = "ordinary_hanging_gate"
    GENERIC_SYMBOLISM = "generic_symbolism"


STRUCTURAL_SALIENCE: Final[Mapping[StructuralClass, float]] = MappingProxyType({
    StructuralClass.TYPE_STRATEGY: 1.00,
    StructuralClass.AUTHORITY: 1.00,
    StructuralClass.DIAGNOSTIC_CENTER: 0.90,
    StructuralClass.PROFILE: 0.85,
    StructuralClass.COMPLETE_CHANNEL: 0.80,
    StructuralClass.CARDINAL_SUN_EARTH: 0.75,
    StructuralClass.DEFINITION: 0.65,
    StructuralClass.REPEATED_GATE_OR_NODE: 0.55,
    StructuralClass.PROMINENT_PLANETARY_ACTIVATION: 0.45,
    StructuralClass.ORDINARY_HANGING_GATE: 0.35,
    StructuralClass.GENERIC_SYMBOLISM: 0.15,
})


class DirectnessClass(StrEnum):
    DIRECT = "direct"
    STRONG = "strong"
    PLAUSIBLE = "plausible"
    NONE = "none"


DIRECTNESS_FACTORS: Final[Mapping[DirectnessClass, float]] = MappingProxyType({
    DirectnessClass.DIRECT: 1.00,
    DirectnessClass.STRONG: 0.75,
    DirectnessClass.PLAUSIBLE: 0.50,
    DirectnessClass.NONE: 0.00,
})


class FlexibilityClass(StrEnum):
    F1_NARROW = "F1"
    F2_MODERATE = "F2"
    F3_BROAD = "F3"
    F4_VERY_FLEXIBLE = "F4"


FLEXIBILITY_FACTORS: Final[Mapping[FlexibilityClass, float]] = MappingProxyType({
    FlexibilityClass.F1_NARROW: 1.00,
    FlexibilityClass.F2_MODERATE: 0.75,
    FlexibilityClass.F3_BROAD: 0.50,
    FlexibilityClass.F4_VERY_FLEXIBLE: 0.25,
})


class ResponseDisposition(StrEnum):
    SCORABLE = "scorable"
    UNKNOWN = "unknown"
    DEPENDS = "depends"
    CONTEXT_DEPENDENT = "context_dependent"
    UNREPORTABLE = "unreportable"

    @property
    def is_scorable(self) -> bool:
        return self is ResponseDisposition.SCORABLE


@dataclass(frozen=True, slots=True)
class ObservationConfidence:
    behavioral_confidence: float
    measurement_reliability: float
    disposition: ResponseDisposition = ResponseDisposition.SCORABLE

    def __post_init__(self) -> None:
        _require_unit_interval("behavioral confidence", self.behavioral_confidence)
        _require_unit_interval("measurement reliability", self.measurement_reliability)

    @property
    def effective_confidence(self) -> float:
        if not self.disposition.is_scorable:
            return 0.0
        return self.behavioral_confidence * self.measurement_reliability


@dataclass(frozen=True, slots=True)
class EvaluatedStructuralAnchor:
    """One compiler-frozen structural anchor evaluated for one candidate.

    ``mechanism_keys`` must name every structural dependency needed to prevent
    reuse, for example a complete Channel and both of its component Gates share
    one channel-family mechanism key.  Exact anchor identity is added by the
    scorer even if the compiler supplies an incomplete key set.
    """

    anchor_id: str
    mechanism_keys: tuple[str, ...]
    supports_response: bool
    structural_class: StructuralClass
    structural_salience: float
    directness_class: DirectnessClass
    directness_factor: float
    flexibility_class: FlexibilityClass
    flexibility_factor: float

    def __post_init__(self) -> None:
        if not self.anchor_id:
            raise ValueError("structural anchor ID must not be empty")
        if not self.mechanism_keys:
            raise ValueError("structural anchors require at least one mechanism key")
        if len(self.mechanism_keys) != len(set(self.mechanism_keys)):
            raise ValueError("structural mechanism keys must be unique")
        if any(not key for key in self.mechanism_keys):
            raise ValueError("structural mechanism keys must not be empty")
        if self.structural_salience != STRUCTURAL_SALIENCE[self.structural_class]:
            raise ValueError("structural salience differs from the frozen V4.3 factor")
        if self.directness_factor != DIRECTNESS_FACTORS[self.directness_class]:
            raise ValueError("mapping directness differs from the frozen V4.3 factor")
        if self.flexibility_factor != FLEXIBILITY_FACTORS[self.flexibility_class]:
            raise ValueError("interpretive flexibility differs from the frozen V4.3 factor")

    @property
    def support(self) -> float:
        if not self.supports_response:
            return 0.0
        return self.structural_salience * self.directness_factor

    @property
    def dependency_keys(self) -> frozenset[str]:
        return frozenset((*self.mechanism_keys, f"anchor:{self.anchor_id}"))


@dataclass(frozen=True, slots=True)
class EvaluatedContradiction:
    """A predeclared opposing-behavior rule evaluated for one candidate."""

    opposes_response: bool = False
    severity: float = 0.0

    def __post_init__(self) -> None:
        _require_unit_interval("contradiction severity", self.severity)

    @property
    def active_severity(self) -> float:
        return self.severity if self.opposes_response else 0.0


@dataclass(frozen=True, slots=True)
class EvaluatedPathway:
    pathway_id: str
    primary: EvaluatedStructuralAnchor
    corroborator: EvaluatedStructuralAnchor | None = None
    contradiction: EvaluatedContradiction = field(default_factory=EvaluatedContradiction)

    def __post_init__(self) -> None:
        if not self.pathway_id:
            raise ValueError("pathway ID must not be empty")
        if self.corroborator is not None:
            if not isinstance(self.corroborator, EvaluatedStructuralAnchor):
                raise TypeError("a pathway accepts at most one explicit corroborator")
            if not self.corroborator.dependency_keys.isdisjoint(
                self.primary.dependency_keys
            ):
                raise ValueError(
                    "the single explicit corroborator must be structurally independent"
                )


@dataclass(frozen=True, slots=True)
class ObservationEvaluation:
    """One atomic observation with alternative structural pathways.

    The scorer groups records by ``dependency_cluster`` and keeps only the
    strongest legitimate contribution in each metric.  Repeated questionnaire
    paraphrases can therefore remain auditable without multiplying evidence.
    """

    observation_id: str
    dependency_cluster: str
    confidence: ObservationConfidence
    pathways: tuple[EvaluatedPathway, ...]

    def __post_init__(self) -> None:
        if not self.observation_id:
            raise ValueError("observation ID must not be empty")
        if not self.dependency_cluster:
            raise ValueError("dependency-cluster ID must not be empty")
        pathway_ids = tuple(pathway.pathway_id for pathway in self.pathways)
        if len(pathway_ids) != len(set(pathway_ids)):
            raise ValueError("alternative pathway IDs must be unique within a cluster")
        if not self.confidence.disposition.is_scorable:
            active_support = any(
                anchor.supports_response
                for pathway in self.pathways
                for anchor in (
                    pathway.primary,
                    *((pathway.corroborator,) if pathway.corroborator is not None else ()),
                )
            )
            active_contradiction = any(
                pathway.contradiction.opposes_response for pathway in self.pathways
            )
            if active_support or active_contradiction:
                raise ValueError(
                    "unknown/depends/context-dependent responses cannot be coerced "
                    "into support or contradiction"
                )


class CoreBlock(StrEnum):
    TYPE_STRATEGY = "type_strategy"
    AUTHORITY = "authority"
    DIAGNOSTIC_CENTERS = "diagnostic_centers"
    PROFILE = "profile"


CORE_BLOCK_WEIGHTS: Final[Mapping[CoreBlock, float]] = MappingProxyType({
    CoreBlock.TYPE_STRATEGY: 30.0,
    CoreBlock.AUTHORITY: 30.0,
    CoreBlock.DIAGNOSTIC_CENTERS: 25.0,
    CoreBlock.PROFILE: 15.0,
})


class CoreBlockAvailability(StrEnum):
    REPORTABLE = "reportable"
    UNREPORTABLE = "unreportable"


@dataclass(frozen=True, slots=True)
class CoreBlockEvaluation:
    """Output of the mapping adapter's exact V3/V4 block rule."""

    block: CoreBlock
    availability: CoreBlockAvailability
    earned_fraction: float | None

    def __post_init__(self) -> None:
        if self.availability is CoreBlockAvailability.REPORTABLE:
            if self.earned_fraction is None:
                raise ValueError("reportable core blocks require an earned fraction")
            _require_unit_interval("core earned fraction", self.earned_fraction)
        elif self.earned_fraction is not None:
            raise ValueError("unreportable core blocks cannot carry earned points")


@dataclass(frozen=True, slots=True)
class V43ScoringInput:
    candidate_context: object
    observations: tuple[ObservationEvaluation, ...]
    core_blocks: tuple[CoreBlockEvaluation, ...]

    def __post_init__(self) -> None:
        observation_ids = tuple(item.observation_id for item in self.observations)
        if len(observation_ids) != len(set(observation_ids)):
            raise ValueError("observation evaluations must have unique IDs")
        blocks = tuple(block.block for block in self.core_blocks)
        if len(blocks) != len(set(blocks)):
            raise ValueError("core block evaluations must be unique")
        if set(blocks) != set(CoreBlock):
            raise ValueError("all four frozen core blocks must be explicit")


@runtime_checkable
class V43EvaluationProvider(Protocol):
    """Adapter boundary intended for a future mapping-library-v2 compiler."""

    @property
    def mapping_library_sha256(self) -> str:
        """Canonical SHA-256 of the frozen mapping artifact."""

    @property
    def required_feature_ids(self) -> frozenset[str]:
        """Complete registry compiled from every frozen predicate."""

    def evaluate(self, candidate: object, responses: object) -> V43ScoringInput:
        """Evaluate without concealed truth, ranks, or answer-key access."""


@runtime_checkable
class ConditionalPrevalenceProvenanceLike(Protocol):
    @property
    def anchor_ids(self) -> tuple[str, ...]: ...

    @property
    def artifact_sha256(self) -> str: ...

    @property
    def plan_sha256(self) -> str: ...

    @property
    def mapping_library_sha256(self) -> str: ...

    @property
    def mapping_source_library_sha256(self) -> str: ...

    @property
    def mapping_prevalence_plan_sha256(self) -> str: ...

    @property
    def required_feature_registry_sha256(self) -> str: ...

    @property
    def cache_manifest_sha256(self) -> str: ...

    @property
    def cache_trust_lock_sha256(self) -> str: ...

    @property
    def cache_build_plan_sha256(self) -> str: ...

    @property
    def semantic_feature_registry_sha256(self) -> str: ...

    @property
    def physical_feature_registry_sha256(self) -> str: ...

    @property
    def reconciliation_aggregate_sha256(self) -> str: ...

    @property
    def engine_validation_sha256(self) -> str: ...

    @property
    def ephemeris_file_set_sha256(self) -> str: ...

    @property
    def boundary_policy_version(self) -> str: ...

    @property
    def universe_sha256(self) -> str: ...

    @property
    def policy_version(self) -> str: ...

    @property
    def parent_hierarchy_sha256(self) -> str: ...

    @property
    def duration_weighted(self) -> bool: ...

    @property
    def conditional(self) -> bool: ...

    @property
    def exact_stable_intervals(self) -> bool: ...

    @property
    def source_scope(self) -> str: ...


@runtime_checkable
class ConditionalPrevalenceEstimateLike(Protocol):
    @property
    def anchor_id(self) -> str: ...

    @property
    def artifact_sha256(self) -> str: ...

    @property
    def plan_sha256(self) -> str: ...

    @property
    def mapping_library_sha256(self) -> str: ...

    @property
    def mapping_prevalence_plan_sha256(self) -> str: ...

    @property
    def required_feature_registry_sha256(self) -> str: ...

    @property
    def cache_manifest_sha256(self) -> str: ...

    @property
    def prevalence(self) -> float: ...

    @property
    def numerator_duration_microseconds(self) -> int: ...

    @property
    def denominator_duration_microseconds(self) -> int: ...

    @property
    def universe_sha256(self) -> str: ...

    @property
    def policy_version(self) -> str: ...

    @property
    def parent_hierarchy_sha256(self) -> str: ...

    @property
    def selected_level_id(self) -> str: ...

    @property
    def backoff_ordinal(self) -> int: ...

    @property
    def duration_weighted(self) -> bool: ...

    @property
    def conditional(self) -> bool: ...

    @property
    def exact_stable_intervals(self) -> bool: ...

    @property
    def source_scope(self) -> str: ...


@runtime_checkable
class ConditionalPrevalenceCandidateBindingLike(Protocol):
    """Capability minted by a provider after verifying exact cache membership."""

    @property
    def state_id(self) -> str: ...

    @property
    def candidate_record_sha256(self) -> str: ...

    @property
    def cache_manifest_sha256(self) -> str: ...

    @property
    def universe_sha256(self) -> str: ...

    @property
    def mapping_library_sha256(self) -> str: ...


@runtime_checkable
class ConditionalPrevalenceProvider(Protocol):
    @property
    def provenance(self) -> ConditionalPrevalenceProvenanceLike:
        """Frozen reference-universe and conditional-policy provenance."""

    def estimate(
        self, anchor_id: str, candidate_context: object
    ) -> ConditionalPrevalenceEstimateLike:
        """Return one duration-weighted global-universe conditional estimate."""

    def bind_candidate_record(
        self,
        candidate_record: object,
        *,
        cache_manifest_sha256: str,
        mapping_library_sha256: str,
    ) -> ConditionalPrevalenceCandidateBindingLike:
        """Verify row membership and return a cache-/mapping-bound capability."""


def _require_unit_interval(label: str, value: float) -> None:
    if not math.isfinite(value) or not 0.0 <= value <= 1.0:
        raise ValueError(f"{label} must be finite and in [0, 1]")
