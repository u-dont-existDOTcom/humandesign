"""Typed, interpretation-free contracts for the detailed symbolic Model B.

The compiler owns behavioral meanings and chart predicates.  This module only
defines the frozen values that the generic prevalence and scoring engines accept.
None of these records contains a hidden birth tuple or an answer-key field.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

MODEL_B_SCORING_VERSION = "V4/V3.2-detailed-scoring-v1"
RUBRIC_UNIT = "rubric_bits"

FROZEN_SALIENCE_VALUES = frozenset({1.00, 0.90, 0.85, 0.80, 0.75, 0.65, 0.55, 0.45, 0.35, 0.15})
FROZEN_DIRECTNESS_VALUES = frozenset({1.00, 0.75, 0.50, 0.00})
FROZEN_CONTRADICTION_VALUES = frozenset({0.00, 0.25, 0.50, 0.75, 1.00})


@runtime_checkable
class ChartPredicate(Protocol):
    """A compiler-provided, frozen chart predicate."""

    def matches(self, chart: object) -> bool:
        """Return whether ``chart`` contains the predeclared structure."""


@runtime_checkable
class ConditioningDimension(Protocol):
    """A compiler-provided frozen extractor for candidate-relative conditioning."""

    @property
    def dimension_id(self) -> str:
        """Stable ID recorded in denominator audit output."""

    def value(self, chart: object) -> str:
        """Return a canonical value used to match reference charts to a candidate."""


@dataclass(frozen=True, slots=True)
class ConditionalLevel:
    """One predeclared denominator, ordered from most specific to broadest."""

    level_id: str
    parent_anchor_ids: tuple[str, ...] = ()
    dimensions: tuple[ConditioningDimension, ...] = ()

    def __post_init__(self) -> None:
        if not self.level_id:
            raise ValueError("conditional level ID must not be empty")
        if len(self.parent_anchor_ids) != len(set(self.parent_anchor_ids)):
            raise ValueError(f"duplicate parent anchor in conditional level {self.level_id}")
        dimension_ids = tuple(item.dimension_id for item in self.dimensions)
        if len(dimension_ids) != len(set(dimension_ids)):
            raise ValueError(f"duplicate conditioning dimension in level {self.level_id}")

    @property
    def condition_ids(self) -> frozenset[str]:
        dimension_ids = (f"dimension:{item.dimension_id}" for item in self.dimensions)
        anchor_ids = (f"anchor:{item}" for item in self.parent_anchor_ids)
        return frozenset((*dimension_ids, *anchor_ids))


@dataclass(frozen=True, slots=True)
class FrozenAnchorSpec:
    """One atomic frozen rarity anchor and its conditional backoff hierarchy."""

    anchor_id: str
    predicate: ChartPredicate
    conditional_levels: tuple[ConditionalLevel, ...]

    def __post_init__(self) -> None:
        if not self.anchor_id:
            raise ValueError("anchor ID must not be empty")
        if not self.conditional_levels:
            raise ValueError(f"anchor {self.anchor_id} requires a conditional hierarchy")
        level_ids = tuple(level.level_id for level in self.conditional_levels)
        if len(level_ids) != len(set(level_ids)):
            raise ValueError(f"duplicate conditional level ID for anchor {self.anchor_id}")
        if self.conditional_levels[-1].condition_ids:
            raise ValueError(
                f"anchor {self.anchor_id} requires an explicit unconditional terminal backoff"
            )
        previous = self.conditional_levels[0].condition_ids
        for level in self.conditional_levels[1:]:
            current = level.condition_ids
            if not current < previous:
                raise ValueError(
                    f"backoff level {level.level_id} for {self.anchor_id} must remove "
                    "at least one frozen condition and cannot add conditions"
                )
            previous = current


@dataclass(frozen=True, slots=True)
class DurationWeightedChartState:
    """A stable reference-universe chart state with its exact UTC duration."""

    chart: object
    duration_seconds: float

    def __post_init__(self) -> None:
        if not math.isfinite(self.duration_seconds) or self.duration_seconds <= 0.0:
            raise ValueError("reference-state duration must be finite and positive")


@dataclass(frozen=True, slots=True)
class ReferenceUniverse:
    """Frozen provenance and denominator policy for duration prevalence.

    ``state_equivalent_duration_seconds`` makes the protocol's minimum effective
    reference size explicit instead of silently treating differently segmented
    intervals as comparable state counts.
    """

    universe_id: str
    universe_sha256: str
    expected_total_duration_seconds: float
    state_equivalent_duration_seconds: float
    minimum_effective_state_equivalents: float = 500.0
    segmentation: str = "exact-boundary-events"

    def __post_init__(self) -> None:
        if not self.universe_id:
            raise ValueError("reference-universe ID must not be empty")
        if len(self.universe_sha256) != 64 or any(
            character not in "0123456789abcdef" for character in self.universe_sha256
        ):
            raise ValueError("reference-universe hash must be lowercase SHA-256")
        for label, value in (
            ("expected total duration", self.expected_total_duration_seconds),
            ("state-equivalent duration", self.state_equivalent_duration_seconds),
            ("minimum effective state equivalents", self.minimum_effective_state_equivalents),
        ):
            if not math.isfinite(value) or value <= 0.0:
                raise ValueError(f"{label} must be finite and positive")
        if not self.segmentation:
            raise ValueError("reference segmentation description must not be empty")


@dataclass(frozen=True, slots=True)
class StructuralEvidence:
    """Candidate-specific result of one compiler-frozen structural mapping."""

    anchor_id: str
    dependency_keys: tuple[str, ...]
    supports_response: bool
    structural_salience: float
    mapping_directness: float

    def __post_init__(self) -> None:
        if not self.anchor_id:
            raise ValueError("structural evidence requires an anchor ID")
        if not self.dependency_keys or len(self.dependency_keys) != len(set(self.dependency_keys)):
            raise ValueError("structural dependency keys must be nonempty and unique")
        if self.structural_salience not in FROZEN_SALIENCE_VALUES:
            raise ValueError("structural salience is not a frozen V3 value")
        if self.mapping_directness not in FROZEN_DIRECTNESS_VALUES:
            raise ValueError("mapping directness is not a frozen V3 value")

    @property
    def support(self) -> float:
        if not self.supports_response:
            return 0.0
        return self.structural_salience * self.mapping_directness


@dataclass(frozen=True, slots=True)
class EvaluatedPathway:
    """One primary pathway plus optional independent corroborators.

    Behavioral interpretation and response matching happen in the compiler-owned
    rule evaluator.  The generic scorer receives only this mechanical result.
    """

    rule_id: str
    dependency_cluster: str
    pathway_id: str
    effective_confidence: float
    primary: StructuralEvidence
    corroborators: tuple[StructuralEvidence, ...] = ()
    contradiction_severity: float = 0.0

    def __post_init__(self) -> None:
        if not self.rule_id or not self.dependency_cluster or not self.pathway_id:
            raise ValueError("rule, dependency-cluster, and pathway IDs must not be empty")
        if not math.isfinite(self.effective_confidence) or not (
            0.0 <= self.effective_confidence <= 1.0
        ):
            raise ValueError("effective confidence must be in [0, 1]")
        if self.contradiction_severity not in FROZEN_CONTRADICTION_VALUES:
            raise ValueError("contradiction severity is not a frozen V3 value")
        corroborator_ids = tuple(item.anchor_id for item in self.corroborators)
        if len(corroborator_ids) != len(set(corroborator_ids)):
            raise ValueError("corroborator anchor IDs must be unique within a pathway")


@runtime_checkable
class CompiledDetailedRule(Protocol):
    """Minimal adapter a compiled Model B rule must implement."""

    @property
    def rule_id(self) -> str:
        """Stable rule ID from the frozen artifact."""

    def evaluate(self, chart: object, responses: object) -> tuple[EvaluatedPathway, ...]:
        """Mechanically evaluate the frozen rule without candidate truth."""


@runtime_checkable
class PrevalenceEstimateLike(Protocol):
    """Subset of prevalence audit output consumed by the scorer."""

    @property
    def anchor_id(self) -> str: ...

    @property
    def prevalence(self) -> float: ...

    @property
    def universe_id(self) -> str: ...

    @property
    def universe_sha256(self) -> str: ...

    @property
    def denominator_duration_seconds(self) -> float: ...

    @property
    def numerator_duration_seconds(self) -> float: ...

    @property
    def selected_level_id(self) -> str: ...


@runtime_checkable
class ConditionalPrevalenceProvider(Protocol):
    """Candidate-relative prevalence lookup; no answer key is accepted."""

    def estimate(self, anchor_id: str, chart: object) -> PrevalenceEstimateLike:
        """Estimate one predeclared anchor in the frozen reference universe."""
