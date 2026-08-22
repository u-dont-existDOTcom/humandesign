"""Strict mapping-library-v2 models for the V4.3/V3.6 symbolic model.

This module defines the behavioral-to-structure contract only.  It does not
populate the canonical V3.6 mapping set, score candidates, estimate prevalence,
or perform a search.  Legacy mapping-library-v1 artifacts remain supported by
their legacy loader and cannot be parsed through this schema by accident.
"""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path, PurePosixPath
from typing import Annotated, Final, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.chart.bodygraph import CHANNELS
from hdmatch.chart.ephemeris import CelestialBody
from hdmatch.chart.feature_registry import (
    ChartFeatureVectorV2,
    FeatureCoverage,
    FeatureId,
    RequiredFeatureRegistry,
    require_complete_feature_coverage,
)
from hdmatch.model.mapping_library import (
    MAPPING_DIRECTNESS,
    STRUCTURAL_SALIENCE,
    ContradictionSeverity,
    DirectnessClass,
    StructuralClass,
)
from hdmatch.util import canonical_json_bytes, sha256_json

_SHA256_PATTERN: Final[str] = r"^[a-f0-9]{64}$"
_ID_PATTERN: Final[str] = r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*$"
_CLUSTER_PATTERN: Final[str] = r"^[A-Z][A-Z0-9_]*$"
_TOKEN_PATTERN: Final[str] = r"^[a-z0-9]+(?:_[a-z0-9]+)*$"
_CHANNEL_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^(?:[1-9]|[1-5][0-9]|6[0-4])-(?:[1-9]|[1-5][0-9]|6[0-4])$"
)


class FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class MappingV2Error(ValueError):
    """Raised when a mapping-library-v2 contract cannot be satisfied."""


class MappingStatusV2(StrEnum):
    FROZEN = "frozen"
    UNRESOLVED = "unresolved"
    EMPIRICAL_ONLY = "empirical_only"


class PathwayRoleV2(StrEnum):
    """Typed role of one confidence-bearing rule inside a pathway group."""

    PRIMARY = "primary"
    ALTERNATIVE = "alternative"
    ALTERNATIVE_HANGING = "alternative_hanging"
    DEPENDENT_CARRIER = "dependent_carrier"


class FlexibilityClass(StrEnum):
    F1 = "F1"
    F2 = "F2"
    F3 = "F3"
    F4 = "F4"


FLEXIBILITY_FACTOR: Final[dict[FlexibilityClass, float]] = {
    FlexibilityClass.F1: 1.00,
    FlexibilityClass.F2: 0.75,
    FlexibilityClass.F3: 0.50,
    FlexibilityClass.F4: 0.25,
}


class PredicateOperatorV2(StrEnum):
    EQUALS_ANY = "equals_any"
    CONTAINS_ANY = "contains_any"
    NOT_CONTAINS_ANY = "not_contains_any"
    PROFILE_HAS_LINE = "profile_has_line"
    MATCHES_ACTIVATION = "matches_activation"
    HAS_GATE = "has_gate"


class ContradictionModeV2(StrEnum):
    NONE = "none"
    DIRECT_OPPOSITION = "direct_opposition"


class RevisionClassV2(StrEnum):
    R0 = "R0"
    R1 = "R1"
    R2 = "R2"
    R3 = "R3"
    R4 = "R4"
    R5 = "R5"


class SelectionRiskV2(StrEnum):
    NONE = "none"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"


class SourceRoleV2(StrEnum):
    BEHAVIORAL_TARGET = "behavioral_target"
    METHOD = "method"
    QUESTION_BANK = "question_bank"
    HD_SOURCE = "hd_source"
    PROVENANCE = "provenance"


class MappingConstantsV2(FrozenModel):
    information_cap_rubric_bits: float = 6.0
    contradiction_scale_rubric_bits: float = 4.0
    independent_corroboration_cap: float = 0.15
    unknown_response_policy: Literal["neutral"] = "neutral"
    alternative_pathway_policy: Literal["maximum_not_sum"] = "maximum_not_sum"
    dependency_policy: Literal["strongest_per_cluster"] = "strongest_per_cluster"
    prevalence_weighting: Literal["exact_duration"] = "exact_duration"

    @model_validator(mode="after")
    def frozen_constants(self) -> MappingConstantsV2:
        if self.information_cap_rubric_bits != 6.0:
            raise ValueError("V4.3 information cap is frozen at 6 rubric bits")
        if self.contradiction_scale_rubric_bits != 4.0:
            raise ValueError("V4.3 contradiction scale is frozen at 4 rubric bits")
        if self.independent_corroboration_cap != 0.15:
            raise ValueError("V4.3 corroboration cap is frozen at 15 percent")
        return self


class SourceArtifactV2(FrozenModel):
    source_id: str = Field(pattern=_ID_PATTERN)
    role: SourceRoleV2
    path: str = Field(min_length=1)
    sha256: str = Field(pattern=_SHA256_PATTERN)
    title: str = Field(min_length=1)
    public_url: str | None = None
    retrieved_at_utc: datetime | None = None
    retrieved_content_sha256: str | None = Field(default=None, pattern=_SHA256_PATTERN)

    @field_validator("path")
    @classmethod
    def relative_repository_path(cls, value: str) -> str:
        path = PurePosixPath(value)
        if path.is_absolute() or ".." in path.parts or value != path.as_posix():
            raise ValueError("source path must be a normalized repository-relative path")
        return value

    @model_validator(mode="after")
    def complete_external_provenance(self) -> SourceArtifactV2:
        external = (
            self.public_url,
            self.retrieved_at_utc,
            self.retrieved_content_sha256,
        )
        if any(value is not None for value in external):
            if any(value is None for value in external):
                raise ValueError(
                    "external source provenance requires URL, retrieval time, and content hash"
                )
            assert self.public_url is not None
            assert self.retrieved_at_utc is not None
            if not self.public_url.startswith(("https://", "http://")):
                raise ValueError("external source URL must use HTTP(S)")
            offset = self.retrieved_at_utc.utcoffset()
            if (
                self.retrieved_at_utc.tzinfo is None
                or offset is None
                or offset.total_seconds() != 0
            ):
                raise ValueError("external source retrieval timestamp must be UTC")
            if self.retrieved_at_utc != self.retrieved_at_utc.astimezone(UTC):
                raise ValueError("external source retrieval timestamp must be normalized to UTC")
        return self


class SourceCitationV2(FrozenModel):
    source_id: str = Field(pattern=_ID_PATTERN)
    locator: str = Field(min_length=1)
    rationale: str = Field(min_length=1)


_ACTIVATION_FEATURES: Final[frozenset[FeatureId]] = frozenset(
    {
        FeatureId.PLANETARY_ACTIVATIONS,
        FeatureId.ACTIVATION_SIDE,
        FeatureId.ACTIVATION_CARRIER,
        FeatureId.ACTIVATION_GATE,
        FeatureId.ACTIVATION_LINE,
        FeatureId.NODE_ACTIVATIONS,
        FeatureId.CARDINAL_ACTIVATIONS,
        FeatureId.COLOR,
        FeatureId.TONE,
        FeatureId.BASE,
    }
)
_GATE_FEATURES: Final[frozenset[FeatureId]] = frozenset(
    {
        FeatureId.ACTIVE_GATES,
        FeatureId.HANGING_GATES,
        FeatureId.DORMANT_GATES,
        FeatureId.POSSIBLE_BRIDGES,
        FeatureId.REPEATED_GATES,
        FeatureId.PLANETARY_ACTIVATIONS,
        FeatureId.NODE_ACTIVATIONS,
        FeatureId.CARDINAL_ACTIVATIONS,
    }
)
_CONTAINS_FEATURES: Final[frozenset[FeatureId]] = frozenset(
    {
        FeatureId.CENTERS,
        FeatureId.COMPLETE_CHANNELS,
        FeatureId.ACTIVE_GATES,
        FeatureId.HANGING_GATES,
        FeatureId.DORMANT_GATES,
        FeatureId.REPEATED_GATES,
        FeatureId.CIRCUITRY_CHANNEL_METADATA,
    }
)
_SCALAR_FEATURES: Final[frozenset[FeatureId]] = frozenset(
    {
        FeatureId.TYPE,
        FeatureId.STRATEGY,
        FeatureId.AUTHORITY,
        FeatureId.PROFILE,
        FeatureId.DEFINITION,
        FeatureId.CROSS_COMPONENTS,
        FeatureId.CROSS_NAME,
        FeatureId.CIRCUITRY_STATUS,
        FeatureId.ADVANCED_STATUS,
    }
)


class StructuralPredicateV2(FrozenModel):
    """One structural anchor over the canonical chart-feature registry.

    ``values`` handles scalar and collection predicates.  Activation predicates
    instead use explicit side/carrier/Gate/Line qualifiers so a Gate-only
    predicate cannot be confused with a side- or carrier-specific predicate.
    """

    feature_id: FeatureId
    operator: PredicateOperatorV2
    values: tuple[str, ...] = ()
    side: Literal["personality", "design"] | None = None
    carrier: CelestialBody | None = None
    gate: int | None = Field(default=None, ge=1, le=64)
    line: int | None = Field(default=None, ge=1, le=6)
    minimum_occurrences: int | None = Field(default=None, ge=2)

    @model_validator(mode="after")
    def validate_predicate_shape(self) -> StructuralPredicateV2:
        if len(self.values) != len(set(self.values)):
            raise ValueError("predicate values must be unique")
        if self.values != tuple(sorted(self.values)):
            raise ValueError("predicate values must use canonical sorted order")

        has_activation_qualifier = any(
            value is not None
            for value in (self.side, self.carrier, self.gate, self.line, self.minimum_occurrences)
        )
        if self.operator in {
            PredicateOperatorV2.EQUALS_ANY,
            PredicateOperatorV2.CONTAINS_ANY,
            PredicateOperatorV2.NOT_CONTAINS_ANY,
            PredicateOperatorV2.PROFILE_HAS_LINE,
        }:
            if not self.values or has_activation_qualifier:
                raise ValueError("value predicates require values and no activation qualifiers")
        elif self.values:
            raise ValueError("activation/Gate predicates cannot also carry generic values")

        if self.operator is PredicateOperatorV2.EQUALS_ANY and (
            self.feature_id not in _SCALAR_FEATURES
        ):
            raise ValueError(
                f"equals_any has no unambiguous semantics for {self.feature_id.value}"
            )

        if self.operator is PredicateOperatorV2.PROFILE_HAS_LINE:
            if self.feature_id is not FeatureId.PROFILE or len(self.values) != 1:
                raise ValueError("profile_has_line requires exactly one Profile line")
            if self.values[0] not in {"1", "2", "3", "4", "5", "6"}:
                raise ValueError("Profile line must be 1 through 6")
        elif self.feature_id is FeatureId.PROFILE and self.operator not in {
            PredicateOperatorV2.EQUALS_ANY,
            PredicateOperatorV2.PROFILE_HAS_LINE,
        }:
            raise ValueError("Profile supports equals_any or profile_has_line only")

        if self.operator in {
            PredicateOperatorV2.CONTAINS_ANY,
            PredicateOperatorV2.NOT_CONTAINS_ANY,
        } and self.feature_id not in _CONTAINS_FEATURES:
            raise ValueError("contains predicates require a collection-valued feature")
        if self.operator is PredicateOperatorV2.MATCHES_ACTIVATION:
            if self.feature_id not in _ACTIVATION_FEATURES:
                raise ValueError("matches_activation requires an activation feature")
            qualifiers = (self.side, self.carrier, self.gate, self.line)
            if not any(value is not None for value in qualifiers):
                raise ValueError("matches_activation requires at least one exact qualifier")
            if self.minimum_occurrences is not None:
                raise ValueError("matches_activation cannot set minimum occurrences")
        if self.operator is PredicateOperatorV2.HAS_GATE:
            if self.feature_id not in _GATE_FEATURES or self.gate is None:
                raise ValueError("has_gate requires a Gate-valued feature and exact Gate")
            if self.line is not None:
                raise ValueError("has_gate cannot silently add a Line condition")
            if (
                self.minimum_occurrences is not None
                and self.feature_id is not FeatureId.REPEATED_GATES
            ):
                raise ValueError("minimum occurrences is only valid for repeated Gates")

        if self.side is not None and self.feature_id not in _ACTIVATION_FEATURES | {
            FeatureId.HANGING_GATES,
            FeatureId.DORMANT_GATES,
        }:
            raise ValueError("side qualifier requires activation or qualified edge data")
        if self.carrier is not None and self.feature_id not in _ACTIVATION_FEATURES:
            raise ValueError("planetary carrier requires activation data")
        if self.line is not None and self.feature_id not in _ACTIVATION_FEATURES:
            raise ValueError("Line qualifier requires activation data")
        if self.feature_id is FeatureId.NODE_ACTIVATIONS and self.carrier not in {
            None,
            CelestialBody.NORTH_NODE,
            CelestialBody.SOUTH_NODE,
        }:
            raise ValueError("Node activation carrier must be North or South Node")
        if self.feature_id is FeatureId.CARDINAL_ACTIVATIONS and self.carrier not in {
            None,
            CelestialBody.SUN,
            CelestialBody.EARTH,
        }:
            raise ValueError("cardinal activation carrier must be Sun or Earth")
        if self.feature_id is FeatureId.COMPLETE_CHANNELS:
            for channel in self.values:
                _require_channel(channel)
        if self.feature_id is FeatureId.CROSS_COMPONENTS and any(
            _cross_component_gates(value) is None for value in self.values
        ):
            raise ValueError("Cross components require exact psun/pearth|dsun/dearth Gates")
        if self.feature_id in {FeatureId.COLOR, FeatureId.TONE, FeatureId.BASE}:
            raise ValueError(
                "advanced substructure lacks a frozen unambiguous V4.3 predicate selector"
            )
        return self

    @property
    def required_feature_ids(self) -> tuple[FeatureId, ...]:
        required = {self.feature_id}
        if self.feature_id in _ACTIVATION_FEATURES:
            required.add(FeatureId.PLANETARY_ACTIVATIONS)
            if self.side is not None:
                required.add(FeatureId.ACTIVATION_SIDE)
            if self.carrier is not None:
                required.add(FeatureId.ACTIVATION_CARRIER)
            if self.gate is not None:
                required.add(FeatureId.ACTIVATION_GATE)
            if self.line is not None:
                required.add(FeatureId.ACTIVATION_LINE)
        if self.feature_id in {FeatureId.HANGING_GATES, FeatureId.DORMANT_GATES}:
            required.add(FeatureId.ACTIVE_GATES)
        if self.feature_id is FeatureId.CIRCUITRY_CHANNEL_METADATA:
            required.update({FeatureId.CIRCUITRY_STATUS, FeatureId.COMPLETE_CHANNELS})
        if self.feature_id is FeatureId.CROSS_NAME:
            required.add(FeatureId.CROSS_COMPONENTS)
        if self.feature_id in {FeatureId.COLOR, FeatureId.TONE, FeatureId.BASE}:
            required.update({FeatureId.ADVANCED_STATUS, FeatureId.PLANETARY_ACTIVATIONS})
        return tuple(sorted(required, key=lambda item: item.value))

    @property
    def anchor_id(self) -> str:
        return f"anchor-v2:{sha256_json(self)}"

    @property
    def dependency_keys(self) -> frozenset[str]:
        """Return exact frozen structural mechanisms, never feature-family buckets.

        Dependency control is about reuse of the same chart mechanism.  A key such
        as ``feature:channels.complete`` would incorrectly make Channel 1-8 and
        Channel 10-20 dependent.  The keys below therefore retain exact values and
        qualifiers.  Channel predicates also expose both component Gate keys, and
        Cross-component predicates expose all four cardinal-position keys, so the
        known compound/singleton double-counting cases deliberately collide.

        Cross-name predicates cannot know their cardinal components at compile
        time.  The canonical runtime adapter augments them from the exact candidate
        row before scoring.
        """

        keys: set[str] = set()
        if self.feature_id in {FeatureId.TYPE, FeatureId.STRATEGY}:
            keys.add("architecture:type_strategy")
        for value in self.values:
            keys.add(f"value:{self.feature_id.value}:{value}")
        if self.gate is not None:
            keys.add(f"gate:{self.gate}")
        if self.operator is PredicateOperatorV2.MATCHES_ACTIVATION:
            qualifiers = (
                self.side or "any-side",
                self.carrier.value if self.carrier is not None else "any-carrier",
                str(self.gate) if self.gate is not None else "any-gate",
                str(self.line) if self.line is not None else "any-line",
            )
            keys.add(f"activation:{':'.join(qualifiers)}")
            if self.feature_id is FeatureId.CARDINAL_ACTIVATIONS:
                keys.add(f"cardinal:{qualifiers[0]}:{qualifiers[1]}:{qualifiers[2]}")
        if self.feature_id is FeatureId.COMPLETE_CHANNELS:
            for channel in self.values:
                left, right = channel.split("-")
                keys.update({f"channel:{channel}", f"gate:{left}", f"gate:{right}"})
        if self.feature_id is FeatureId.CROSS_COMPONENTS:
            for value in self.values:
                components = _cross_component_gates(value)
                if components is None:
                    continue
                keys.add(f"cross:{value}")
                positions = (
                    "personality:sun",
                    "personality:earth",
                    "design:sun",
                    "design:earth",
                )
                for position, gate in zip(positions, components, strict=True):
                    keys.add(f"gate:{gate}")
                    keys.add(f"cardinal:{position}:{gate}")
        if not keys:
            # Exact predicate identity is a legitimate mechanism for predicates
            # whose structure has no more specific cross-family relationship.
            keys.add(f"predicate:{self.anchor_id}")
        return frozenset(keys)


class PrevalenceParentLevelV2(FrozenModel):
    """One predeclared conditional level, ordered most-specific to root."""

    level_id: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    parent_feature_ids: tuple[FeatureId, ...]

    @model_validator(mode="after")
    def canonical_features(self) -> PrevalenceParentLevelV2:
        if len(self.parent_feature_ids) != len(set(self.parent_feature_ids)):
            raise ValueError("prevalence parent features must be unique")
        if self.parent_feature_ids != tuple(
            sorted(self.parent_feature_ids, key=lambda item: item.value)
        ):
            raise ValueError("prevalence parent features must use canonical sorted order")
        return self


class ResponseContradictionV2(FrozenModel):
    mode: ContradictionModeV2
    opposing_response_tokens: tuple[str, ...]
    severity: ContradictionSeverity
    rationale: str = Field(min_length=1)

    @field_validator("opposing_response_tokens")
    @classmethod
    def canonical_tokens(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) != len(set(value)) or value != tuple(sorted(value)):
            raise ValueError("contradiction tokens must be unique and sorted")
        for token in value:
            if re.fullmatch(_TOKEN_PATTERN, token) is None:
                raise ValueError(f"invalid contradiction response token: {token}")
        return value

    @model_validator(mode="after")
    def mode_controls_penalty(self) -> ResponseContradictionV2:
        if self.mode is ContradictionModeV2.NONE:
            if self.opposing_response_tokens or self.severity is not ContradictionSeverity.NONE:
                raise ValueError("no-contradiction rule cannot carry tokens or severity")
        elif not self.opposing_response_tokens or self.severity is ContradictionSeverity.NONE:
            raise ValueError("direct opposition requires tokens and nonzero severity")
        return self


class ResponseRuleV2(FrozenModel):
    response_dimension_id: str = Field(pattern=_ID_PATTERN)
    canonical_response_token: str = Field(pattern=_TOKEN_PATTERN)
    support_response_tokens: tuple[str, ...] = Field(min_length=1)
    unknown_response_tokens: tuple[str, ...]
    unknown_policy: Literal["neutral"] = "neutral"
    contradiction: ResponseContradictionV2

    @model_validator(mode="after")
    def disjoint_canonical_tokens(self) -> ResponseRuleV2:
        groups = (
            self.support_response_tokens,
            self.unknown_response_tokens,
            self.contradiction.opposing_response_tokens,
        )
        for group in groups:
            if len(group) != len(set(group)) or group != tuple(sorted(group)):
                raise ValueError("response token groups must be unique and sorted")
            for token in group:
                if re.fullmatch(_TOKEN_PATTERN, token) is None:
                    raise ValueError(f"invalid response token: {token}")
        support, unknown, contradiction = (set(group) for group in groups)
        if self.canonical_response_token not in support:
            raise ValueError("canonical response token must be a support token")
        if support & unknown or support & contradiction or unknown & contradiction:
            raise ValueError("support, unknown, and contradiction tokens must be disjoint")
        return self


class StructuralPathwayV2(FrozenModel):
    pathway_id: str = Field(pattern=_ID_PATTERN)
    predicate: StructuralPredicateV2
    structural_class: StructuralClass
    structural_salience: float = Field(ge=0.0, le=1.0)
    directness_class: DirectnessClass
    mapping_directness: float = Field(ge=0.0, le=1.0)
    flexibility_class: FlexibilityClass
    flexibility_factor: float = Field(ge=0.0, le=1.0)
    prevalence_parent_hierarchy: tuple[PrevalenceParentLevelV2, ...] = Field(min_length=1)
    sources: tuple[SourceCitationV2, ...] = Field(min_length=1)
    rationale: str = Field(min_length=1)

    @model_validator(mode="after")
    def frozen_factors_and_backoff(self) -> StructuralPathwayV2:
        allowed_classes = _structural_classes_for_feature(self.predicate.feature_id)
        if self.structural_class not in allowed_classes:
            allowed = ", ".join(sorted(item.value for item in allowed_classes))
            raise ValueError(
                f"feature {self.predicate.feature_id.value} requires structural class in "
                f"[{allowed}]"
            )
        if self.structural_salience != STRUCTURAL_SALIENCE[self.structural_class]:
            raise ValueError("structural salience must equal the frozen V4.3 constant")
        if self.mapping_directness != MAPPING_DIRECTNESS[self.directness_class]:
            raise ValueError("mapping directness must equal the frozen V4.3 constant")
        if self.flexibility_factor != FLEXIBILITY_FACTOR[self.flexibility_class]:
            raise ValueError("flexibility factor must equal the frozen V4.3 class factor")
        _validate_prevalence_hierarchy(self.prevalence_parent_hierarchy)
        return self

    @property
    def required_feature_ids(self) -> tuple[FeatureId, ...]:
        required = set(self.predicate.required_feature_ids)
        for level in self.prevalence_parent_hierarchy:
            required.update(level.parent_feature_ids)
        return tuple(sorted(required, key=lambda item: item.value))


class CorroboratingPathwayV2(FrozenModel):
    pathway: StructuralPathwayV2
    independent_of_pathway_ids: tuple[str, ...] = Field(min_length=1)
    independence_rationale: str = Field(min_length=1)
    contribution_cap: float = 0.15

    @field_validator("independent_of_pathway_ids")
    @classmethod
    def canonical_pathway_ids(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) != len(set(value)) or value != tuple(sorted(value)):
            raise ValueError("corroborator independence IDs must be unique and sorted")
        return value

    @field_validator("contribution_cap")
    @classmethod
    def frozen_contribution_cap(cls, value: float) -> float:
        if value != 0.15:
            raise ValueError("independent corroboration is capped at 15 percent")
        return value


class FrozenMappingRuleSourceV2(FrozenModel):
    rule_id: str = Field(pattern=_ID_PATTERN)
    observation_id: str = Field(pattern=_ID_PATTERN)
    status: Literal[MappingStatusV2.FROZEN] = MappingStatusV2.FROZEN
    behavioral_statement: str = Field(min_length=1)
    behavioral_confidence: float = Field(gt=0.0, le=1.0)
    measurement_reliability: float = Field(ge=0.0, le=1.0)
    source_dependency_cluster: str = Field(pattern=_CLUSTER_PATTERN)
    dependency_cluster: str = Field(pattern=_CLUSTER_PATTERN)
    pathway_group_id: str = Field(pattern=_CLUSTER_PATTERN)
    pathway_role: PathwayRoleV2
    primary_rule_id: str = Field(pattern=_ID_PATTERN)
    elicitation_stage: str = Field(min_length=1)
    revision_class: RevisionClassV2
    selection_risk: SelectionRiskV2
    candidate_direction_visible: bool
    question_ids: tuple[str, ...]
    response_rule: ResponseRuleV2
    primary_pathway: StructuralPathwayV2
    alternative_pathways: tuple[StructuralPathwayV2, ...]
    corroborating_pathway: CorroboratingPathwayV2 | None
    sources: tuple[SourceCitationV2, ...] = Field(min_length=1)
    rationale: str = Field(min_length=1)

    @model_validator(mode="after")
    def explicit_pathway_roles(self) -> FrozenMappingRuleSourceV2:
        if self.pathway_group_id != self.dependency_cluster:
            raise ValueError("pathway group must equal the scoring dependency cluster")
        if self.pathway_role is PathwayRoleV2.PRIMARY:
            if self.primary_rule_id != self.rule_id:
                raise ValueError("primary pathway role must link to its own rule ID")
        elif self.primary_rule_id == self.rule_id:
            raise ValueError("non-primary pathway role must link to another primary rule")
        if "alternative_pathways" not in self.model_fields_set:
            raise ValueError("allowed alternatives must be explicit, even when empty")
        pathway_ids = (
            self.primary_pathway.pathway_id,
            *(path.pathway_id for path in self.alternative_pathways),
        )
        if len(pathway_ids) != len(set(pathway_ids)):
            raise ValueError("primary and alternative pathway IDs must be unique")
        if self.corroborating_pathway is not None:
            corroborator = self.corroborating_pathway
            if corroborator.pathway.pathway_id in pathway_ids:
                raise ValueError("corroborator pathway ID must be unique")
            if set(corroborator.independent_of_pathway_ids) != set(pathway_ids):
                raise ValueError("corroborator must declare independence from every main pathway")
            corr_keys = corroborator.pathway.predicate.dependency_keys
            for pathway in (self.primary_pathway, *self.alternative_pathways):
                if corr_keys & pathway.predicate.dependency_keys:
                    raise ValueError(
                        "corroborator shares structural dependency with a main pathway"
                    )
        if len(self.question_ids) != len(set(self.question_ids)):
            raise ValueError("question IDs must be unique")
        return self


class UnresolvedMappingRuleSourceV2(FrozenModel):
    rule_id: str = Field(pattern=_ID_PATTERN)
    observation_id: str = Field(pattern=_ID_PATTERN)
    status: Literal[MappingStatusV2.UNRESOLVED] = MappingStatusV2.UNRESOLVED
    behavioral_statement: str = Field(min_length=1)
    behavioral_confidence: float = Field(gt=0.0, le=1.0)
    measurement_reliability: float = Field(ge=0.0, le=1.0)
    dependency_cluster: str = Field(pattern=_CLUSTER_PATTERN)
    elicitation_stage: str = Field(min_length=1)
    revision_class: RevisionClassV2
    selection_risk: SelectionRiskV2
    candidate_direction_visible: bool
    question_ids: tuple[str, ...]
    sources: tuple[SourceCitationV2, ...] = Field(min_length=1)
    unresolved_reason: str = Field(min_length=1)


class EmpiricalOnlyMappingRuleSourceV2(FrozenModel):
    rule_id: str = Field(pattern=_ID_PATTERN)
    observation_id: str = Field(pattern=_ID_PATTERN)
    status: Literal[MappingStatusV2.EMPIRICAL_ONLY] = MappingStatusV2.EMPIRICAL_ONLY
    behavioral_statement: str = Field(min_length=1)
    behavioral_confidence: float = Field(gt=0.0, le=1.0)
    measurement_reliability: float = Field(ge=0.0, le=1.0)
    dependency_cluster: str = Field(pattern=_CLUSTER_PATTERN)
    elicitation_stage: str = Field(min_length=1)
    revision_class: RevisionClassV2
    selection_risk: SelectionRiskV2
    candidate_direction_visible: bool
    question_ids: tuple[str, ...]
    sources: tuple[SourceCitationV2, ...] = Field(min_length=1)
    empirical_reason: str = Field(min_length=1)


MappingRuleSourceV2 = Annotated[
    FrozenMappingRuleSourceV2
    | UnresolvedMappingRuleSourceV2
    | EmpiricalOnlyMappingRuleSourceV2,
    Field(discriminator="status"),
]


class MappingLibrarySourceV2(FrozenModel):
    schema_version: Literal["mapping-library-v2-source"] = "mapping-library-v2-source"
    model_version: Literal["V4.3/V3.6-symbolic-v2"] = "V4.3/V3.6-symbolic-v2"
    protocol_version: Literal["V4.3"] = "V4.3"
    behavioral_target_version: Literal["V3.6"] = "V3.6"
    calculation_tier: Literal["M2"] = "M2"
    scoring_tier: Literal["M2"] = "M2"
    behavioral_target_source_id: str = Field(pattern=_ID_PATTERN)
    method_source_ids: tuple[str, ...] = Field(min_length=1)
    question_bank_source_id: str | None = Field(default=None, pattern=_ID_PATTERN)
    source_artifacts: tuple[SourceArtifactV2, ...] = Field(min_length=1)
    constants: MappingConstantsV2 = Field(default_factory=MappingConstantsV2)
    declared_frozen_rule_ids: tuple[str, ...] = Field(min_length=1)
    declared_observation_ids: tuple[str, ...] = Field(min_length=1)
    declared_required_feature_ids: tuple[FeatureId, ...] = Field(min_length=1)
    mappings: tuple[MappingRuleSourceV2, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_inventory_and_sources(self) -> MappingLibrarySourceV2:
        _require_unique_sorted(self.declared_frozen_rule_ids, "declared frozen rule IDs")
        _require_unique_sorted(self.declared_observation_ids, "declared observation IDs")
        _require_unique_feature_ids(self.declared_required_feature_ids)
        rule_ids = tuple(item.rule_id for item in self.mappings)
        observation_ids = tuple(item.observation_id for item in self.mappings)
        if len(rule_ids) != len(set(rule_ids)):
            raise ValueError("mapping rule IDs must be unique")
        if len(observation_ids) != len(set(observation_ids)):
            raise ValueError("mapping observation IDs must be unique")
        if set(observation_ids) != set(self.declared_observation_ids):
            raise ValueError("declared observation inventory differs from mapping records")
        frozen_ids = tuple(
            sorted(
                item.rule_id
                for item in self.mappings
                if isinstance(item, FrozenMappingRuleSourceV2)
            )
        )
        if frozen_ids != self.declared_frozen_rule_ids:
            raise ValueError("declared frozen-rule inventory differs from frozen mappings")
        frozen_by_rule_id = {item.rule_id: item for item in self.frozen_mappings}
        groups: dict[str, list[FrozenMappingRuleSourceV2]] = {}
        for frozen_mapping in self.frozen_mappings:
            groups.setdefault(frozen_mapping.pathway_group_id, []).append(frozen_mapping)
            primary = frozen_by_rule_id.get(frozen_mapping.primary_rule_id)
            if primary is None:
                raise ValueError(
                    f"mapping {frozen_mapping.rule_id} links to an unknown primary rule"
                )
            if primary.pathway_role is not PathwayRoleV2.PRIMARY:
                raise ValueError(
                    f"mapping {frozen_mapping.rule_id} links to a non-primary pathway role"
                )
            if primary.pathway_group_id != frozen_mapping.pathway_group_id:
                raise ValueError(
                    f"mapping {frozen_mapping.rule_id} links across pathway groups"
                )
        for group_id, group in groups.items():
            primaries = [
                item for item in group if item.pathway_role is PathwayRoleV2.PRIMARY
            ]
            if len(primaries) != 1:
                raise ValueError(
                    f"pathway group {group_id} must declare exactly one primary rule"
                )
        pathway_ids = tuple(
            pathway.pathway_id
            for mapping in self.frozen_mappings
            for pathway in _source_rule_pathways(mapping)
        )
        if len(pathway_ids) != len(set(pathway_ids)):
            raise ValueError("source pathway IDs must be globally unique")
        _validate_bound_source_roles(
            source_artifacts=self.source_artifacts,
            behavioral_target_source_id=self.behavioral_target_source_id,
            method_source_ids=self.method_source_ids,
            question_bank_source_id=self.question_bank_source_id,
        )
        source_ids = tuple(item.source_id for item in self.source_artifacts)
        known_sources = set(source_ids)
        for mapping_record in self.mappings:
            citations = list(mapping_record.sources)
            if isinstance(mapping_record, FrozenMappingRuleSourceV2):
                citations.extend(mapping_record.primary_pathway.sources)
                for pathway in mapping_record.alternative_pathways:
                    citations.extend(pathway.sources)
                if mapping_record.corroborating_pathway is not None:
                    citations.extend(mapping_record.corroborating_pathway.pathway.sources)
            unknown = {item.source_id for item in citations} - known_sources
            if unknown:
                raise ValueError(
                    f"mapping {mapping_record.rule_id} cites unknown sources: "
                    f"{sorted(unknown)}"
                )
        return self

    @property
    def frozen_mappings(self) -> tuple[FrozenMappingRuleSourceV2, ...]:
        return tuple(
            item for item in self.mappings if isinstance(item, FrozenMappingRuleSourceV2)
        )

    def canonical_bytes(self) -> bytes:
        return canonical_json_bytes(self)

    def sha256(self) -> str:
        return sha256_json(self)


class CompiledPathwayV2(FrozenModel):
    pathway_id: str
    anchor_id: str = Field(pattern=r"^anchor-v2:[a-f0-9]{64}$")
    predicate: StructuralPredicateV2
    dependency_keys: tuple[str, ...] = Field(min_length=1)
    structural_class: StructuralClass
    structural_salience: float
    directness_class: DirectnessClass
    mapping_directness: float
    flexibility_class: FlexibilityClass
    flexibility_factor: float
    prevalence_parent_hierarchy: tuple[PrevalenceParentLevelV2, ...] = Field(min_length=1)
    required_feature_ids: tuple[FeatureId, ...] = Field(min_length=1)
    sources: tuple[SourceCitationV2, ...] = Field(min_length=1)
    rationale: str = Field(min_length=1)

    @model_validator(mode="after")
    def matches_derived_fields(self) -> CompiledPathwayV2:
        if self.anchor_id != self.predicate.anchor_id:
            raise ValueError("compiled anchor ID differs from its predicate")
        if self.dependency_keys != tuple(sorted(self.predicate.dependency_keys)):
            raise ValueError("compiled dependency keys differ from the predicate")
        source = StructuralPathwayV2(
            pathway_id=self.pathway_id,
            predicate=self.predicate,
            structural_class=self.structural_class,
            structural_salience=self.structural_salience,
            directness_class=self.directness_class,
            mapping_directness=self.mapping_directness,
            flexibility_class=self.flexibility_class,
            flexibility_factor=self.flexibility_factor,
            prevalence_parent_hierarchy=self.prevalence_parent_hierarchy,
            sources=self.sources,
            rationale=self.rationale,
        )
        if self.required_feature_ids != source.required_feature_ids:
            raise ValueError("compiled pathway required features differ from derivation")
        return self


class CompiledCorroboratingPathwayV2(FrozenModel):
    pathway: CompiledPathwayV2
    independent_of_pathway_ids: tuple[str, ...] = Field(min_length=1)
    independence_rationale: str = Field(min_length=1)
    contribution_cap: float = 0.15

    @field_validator("contribution_cap")
    @classmethod
    def frozen_contribution_cap(cls, value: float) -> float:
        if value != 0.15:
            raise ValueError("independent corroboration is capped at 15 percent")
        return value


class CompiledMappingRuleV2(FrozenModel):
    rule_id: str = Field(pattern=_ID_PATTERN)
    observation_id: str = Field(pattern=_ID_PATTERN)
    behavioral_statement: str = Field(min_length=1)
    behavioral_confidence: float = Field(gt=0.0, le=1.0)
    measurement_reliability: float = Field(ge=0.0, le=1.0)
    source_dependency_cluster: str = Field(pattern=_CLUSTER_PATTERN)
    dependency_cluster: str = Field(pattern=_CLUSTER_PATTERN)
    pathway_group_id: str = Field(pattern=_CLUSTER_PATTERN)
    pathway_role: PathwayRoleV2
    primary_rule_id: str = Field(pattern=_ID_PATTERN)
    elicitation_stage: str = Field(min_length=1)
    revision_class: RevisionClassV2
    selection_risk: SelectionRiskV2
    candidate_direction_visible: bool
    question_ids: tuple[str, ...]
    response_rule: ResponseRuleV2
    primary_pathway: CompiledPathwayV2
    alternative_pathways: tuple[CompiledPathwayV2, ...]
    corroborating_pathway: CompiledCorroboratingPathwayV2 | None
    sources: tuple[SourceCitationV2, ...] = Field(min_length=1)
    rationale: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_compiled_roles(self) -> CompiledMappingRuleV2:
        if self.pathway_group_id != self.dependency_cluster:
            raise ValueError(
                "compiled pathway group must equal the scoring dependency cluster"
            )
        if self.pathway_role is PathwayRoleV2.PRIMARY:
            if self.primary_rule_id != self.rule_id:
                raise ValueError("compiled primary role must link to its own rule ID")
        elif self.primary_rule_id == self.rule_id:
            raise ValueError("compiled non-primary role must link to another primary rule")
        pathway_ids = (
            self.primary_pathway.pathway_id,
            *(path.pathway_id for path in self.alternative_pathways),
        )
        if len(pathway_ids) != len(set(pathway_ids)):
            raise ValueError("compiled primary and alternative pathway IDs must be unique")
        if self.corroborating_pathway is not None:
            corroborator = self.corroborating_pathway
            if corroborator.pathway.pathway_id in pathway_ids:
                raise ValueError("compiled corroborator pathway ID must be unique")
            if set(corroborator.independent_of_pathway_ids) != set(pathway_ids):
                raise ValueError(
                    "compiled corroborator must declare independence from every main pathway"
                )
            corr_keys = set(corroborator.pathway.dependency_keys)
            for pathway in (self.primary_pathway, *self.alternative_pathways):
                if corr_keys & set(pathway.dependency_keys):
                    raise ValueError(
                        "compiled corroborator shares dependency with a main pathway"
                    )
        if len(self.question_ids) != len(set(self.question_ids)):
            raise ValueError("compiled question IDs must be unique")
        return self


class MappingLibraryV2(FrozenModel):
    schema_version: Literal["mapping-library-v2"] = "mapping-library-v2"
    model_version: Literal["V4.3/V3.6-symbolic-v2"] = "V4.3/V3.6-symbolic-v2"
    protocol_version: Literal["V4.3"] = "V4.3"
    behavioral_target_version: Literal["V3.6"] = "V3.6"
    calculation_tier: Literal["M2"] = "M2"
    scoring_tier: Literal["M2"] = "M2"
    source_library_sha256: str = Field(pattern=_SHA256_PATTERN)
    behavioral_target_source_id: str = Field(pattern=_ID_PATTERN)
    method_source_ids: tuple[str, ...] = Field(min_length=1)
    question_bank_source_id: str | None = Field(default=None, pattern=_ID_PATTERN)
    source_artifacts: tuple[SourceArtifactV2, ...] = Field(min_length=1)
    constants: MappingConstantsV2
    declared_frozen_rule_ids: tuple[str, ...] = Field(min_length=1)
    declared_observation_ids: tuple[str, ...] = Field(min_length=1)
    required_feature_registry: RequiredFeatureRegistry
    required_feature_registry_sha256: str = Field(pattern=_SHA256_PATTERN)
    rules: tuple[CompiledMappingRuleV2, ...] = Field(min_length=1)
    unresolved_mappings: tuple[UnresolvedMappingRuleSourceV2, ...]
    empirical_only_mappings: tuple[EmpiricalOnlyMappingRuleSourceV2, ...]

    @model_validator(mode="after")
    def validate_compiled_contract(self) -> MappingLibraryV2:
        _validate_bound_source_roles(
            source_artifacts=self.source_artifacts,
            behavioral_target_source_id=self.behavioral_target_source_id,
            method_source_ids=self.method_source_ids,
            question_bank_source_id=self.question_bank_source_id,
        )
        if self.required_feature_registry_sha256 != self.required_feature_registry.sha256():
            raise ValueError("required-feature registry hash mismatch")
        if tuple(sorted(item.rule_id for item in self.rules)) != self.declared_frozen_rule_ids:
            raise ValueError("compiled rules differ from declared frozen inventory")
        rules_by_id = {item.rule_id: item for item in self.rules}
        pathway_groups: dict[str, list[CompiledMappingRuleV2]] = {}
        for rule in self.rules:
            pathway_groups.setdefault(rule.pathway_group_id, []).append(rule)
            primary = rules_by_id.get(rule.primary_rule_id)
            if primary is None:
                raise ValueError(f"compiled rule {rule.rule_id} has unknown primary linkage")
            if primary.pathway_role is not PathwayRoleV2.PRIMARY:
                raise ValueError(
                    f"compiled rule {rule.rule_id} links to a non-primary role"
                )
            if primary.pathway_group_id != rule.pathway_group_id:
                raise ValueError(f"compiled rule {rule.rule_id} links across pathway groups")
        for group_id, group in pathway_groups.items():
            primaries = [
                item for item in group if item.pathway_role is PathwayRoleV2.PRIMARY
            ]
            if len(primaries) != 1:
                raise ValueError(
                    f"compiled pathway group {group_id} must have exactly one primary"
                )
        compiled_rule_ids = (
            *(item.rule_id for item in self.rules),
            *(item.rule_id for item in self.unresolved_mappings),
            *(item.rule_id for item in self.empirical_only_mappings),
        )
        if len(compiled_rule_ids) != len(set(compiled_rule_ids)):
            raise ValueError("compiled artifact mapping rule IDs must be unique")
        compiled_observations = (
            *(item.observation_id for item in self.rules),
            *(item.observation_id for item in self.unresolved_mappings),
            *(item.observation_id for item in self.empirical_only_mappings),
        )
        if len(compiled_observations) != len(set(compiled_observations)):
            raise ValueError("compiled artifact observation IDs must be unique")
        if set(compiled_observations) != set(self.declared_observation_ids):
            raise ValueError("compiled observations differ from declared observation inventory")
        pathway_ids = tuple(
            pathway.pathway_id
            for rule in self.rules
            for pathway in _compiled_rule_pathways(rule)
        )
        if len(pathway_ids) != len(set(pathway_ids)):
            raise ValueError("compiled pathway IDs must be globally unique")
        prevalence_contracts: dict[str, tuple[PrevalenceParentLevelV2, ...]] = {}
        for rule in self.rules:
            for pathway in _compiled_rule_pathways(rule):
                previous = prevalence_contracts.setdefault(
                    pathway.anchor_id,
                    pathway.prevalence_parent_hierarchy,
                )
                if previous != pathway.prevalence_parent_hierarchy:
                    raise ValueError(
                        "one structural anchor cannot declare multiple prevalence hierarchies"
                    )
        known_sources = {item.source_id for item in self.source_artifacts}
        for mapping in self.rules:
            citations = list(mapping.sources)
            for pathway in _compiled_rule_pathways(mapping):
                citations.extend(pathway.sources)
            unknown = {item.source_id for item in citations} - known_sources
            if unknown:
                raise ValueError(
                    f"compiled mapping {mapping.rule_id} cites unknown sources: "
                    f"{sorted(unknown)}"
                )
        for unresolved_mapping in self.unresolved_mappings:
            _require_known_mapping_sources(
                unresolved_mapping.rule_id,
                unresolved_mapping.sources,
                known_sources,
            )
        for empirical_mapping in self.empirical_only_mappings:
            _require_known_mapping_sources(
                empirical_mapping.rule_id,
                empirical_mapping.sources,
                known_sources,
            )
        derived = {
            feature_id
            for rule in self.rules
            for pathway in _compiled_rule_pathways(rule)
            for feature_id in pathway.required_feature_ids
        }
        if derived != set(self.required_feature_registry.feature_ids):
            raise ValueError("compiled mapping feature union differs from required registry")
        return self

    def canonical_bytes(self) -> bytes:
        return canonical_json_bytes(self)

    def sha256(self) -> str:
        return sha256_json(self)

    def require_feature_coverage(self, chart: object) -> FeatureCoverage:
        validated = MappingLibraryV2.model_validate(self.model_dump(mode="json"))
        return require_complete_feature_coverage(chart, validated.required_feature_registry)


def load_mapping_library_source_v2(path: str | Path) -> MappingLibrarySourceV2:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if (
        not isinstance(payload, dict)
        or payload.get("schema_version") != "mapping-library-v2-source"
    ):
        raise MappingV2Error(
            "expected mapping-library-v2-source; legacy artifacts are fixtures only"
        )
    return MappingLibrarySourceV2.model_validate(payload)


def load_mapping_library_v2(path: str | Path) -> MappingLibraryV2:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema_version") != "mapping-library-v2":
        raise MappingV2Error("expected compiled mapping-library-v2")
    return MappingLibraryV2.model_validate(payload)


def require_mapping_feature_coverage(
    chart: ChartFeatureVectorV2 | object,
    library: MappingLibraryV2,
) -> FeatureCoverage:
    """Mandatory pre-scoring fail-closed feature gate."""

    return library.require_feature_coverage(chart)


def _validate_prevalence_hierarchy(levels: tuple[PrevalenceParentLevelV2, ...]) -> None:
    ids = tuple(item.level_id for item in levels)
    if len(ids) != len(set(ids)):
        raise ValueError("prevalence hierarchy level IDs must be unique")
    if levels[-1].parent_feature_ids:
        raise ValueError("prevalence hierarchy must end with an explicit root backoff")
    for current, following in zip(levels, levels[1:], strict=False):
        current_set = set(current.parent_feature_ids)
        following_set = set(following.parent_feature_ids)
        if not following_set < current_set:
            raise ValueError("each prevalence backoff must be a strict parent-feature subset")


def _require_channel(value: str) -> None:
    if _CHANNEL_PATTERN.fullmatch(value) is None:
        raise ValueError(f"invalid channel identifier: {value}")
    left, right = (int(item) for item in value.split("-"))
    if left >= right or value not in {channel.identifier for channel in CHANNELS}:
        raise ValueError(f"channel is not canonical: {value}")


def _cross_component_gates(value: str) -> tuple[int, int, int, int] | None:
    match = re.fullmatch(
        r"([1-9]|[1-5][0-9]|6[0-4])/([1-9]|[1-5][0-9]|6[0-4])\|"
        r"([1-9]|[1-5][0-9]|6[0-4])/([1-9]|[1-5][0-9]|6[0-4])",
        value,
    )
    if match is None:
        return None
    first, second, third, fourth = match.groups()
    return int(first), int(second), int(third), int(fourth)


def _require_unique_sorted(values: tuple[str, ...], label: str) -> None:
    if len(values) != len(set(values)) or values != tuple(sorted(values)):
        raise ValueError(f"{label} must be unique and sorted")


def _require_unique_feature_ids(values: tuple[FeatureId, ...]) -> None:
    if len(values) != len(set(values)) or values != tuple(
        sorted(values, key=lambda item: item.value)
    ):
        raise ValueError("declared required feature IDs must be unique and sorted")


def _compiled_rule_pathways(rule: CompiledMappingRuleV2) -> tuple[CompiledPathwayV2, ...]:
    pathways = (rule.primary_pathway, *rule.alternative_pathways)
    if rule.corroborating_pathway is not None:
        pathways = (*pathways, rule.corroborating_pathway.pathway)
    return pathways


def _source_rule_pathways(rule: FrozenMappingRuleSourceV2) -> tuple[StructuralPathwayV2, ...]:
    pathways = (rule.primary_pathway, *rule.alternative_pathways)
    if rule.corroborating_pathway is not None:
        pathways = (*pathways, rule.corroborating_pathway.pathway)
    return pathways


def _validate_bound_source_roles(
    *,
    source_artifacts: tuple[SourceArtifactV2, ...],
    behavioral_target_source_id: str,
    method_source_ids: tuple[str, ...],
    question_bank_source_id: str | None,
) -> None:
    source_ids = tuple(item.source_id for item in source_artifacts)
    if len(source_ids) != len(set(source_ids)):
        raise ValueError("source artifact IDs must be unique")
    if source_ids != tuple(sorted(source_ids)):
        raise ValueError("source artifacts must use canonical source-ID order")
    artifacts = {item.source_id: item for item in source_artifacts}
    if behavioral_target_source_id not in artifacts:
        raise ValueError("behavioral-target source binding is missing")
    if artifacts[behavioral_target_source_id].role is not SourceRoleV2.BEHAVIORAL_TARGET:
        raise ValueError("behavioral-target source must have behavioral_target role")
    _require_unique_sorted(method_source_ids, "method source IDs")
    if any(item not in artifacts for item in method_source_ids):
        raise ValueError("method source binding is missing")
    if any(artifacts[item].role is not SourceRoleV2.METHOD for item in method_source_ids):
        raise ValueError("method source IDs must resolve to method-role artifacts")
    if question_bank_source_id is not None:
        if question_bank_source_id not in artifacts:
            raise ValueError("question-bank source binding is missing")
        if artifacts[question_bank_source_id].role is not SourceRoleV2.QUESTION_BANK:
            raise ValueError("question-bank source must have question_bank role")


def _require_known_mapping_sources(
    rule_id: str,
    citations: tuple[SourceCitationV2, ...],
    known_sources: set[str],
) -> None:
    unknown = {item.source_id for item in citations} - known_sources
    if unknown:
        raise ValueError(
            f"compiled mapping {rule_id} cites unknown sources: {sorted(unknown)}"
        )


def _structural_classes_for_feature(feature_id: FeatureId) -> frozenset[StructuralClass]:
    exact: dict[FeatureId, StructuralClass] = {
        FeatureId.TYPE: StructuralClass.TYPE_STRATEGY,
        FeatureId.STRATEGY: StructuralClass.TYPE_STRATEGY,
        FeatureId.AUTHORITY: StructuralClass.AUTHORITY,
        FeatureId.CENTERS: StructuralClass.DIAGNOSTIC_CENTER,
        FeatureId.PROFILE: StructuralClass.PROFILE,
        FeatureId.DEFINITION: StructuralClass.DEFINITION,
        FeatureId.DEFINITION_TOPOLOGY: StructuralClass.DEFINITION,
        FeatureId.POSSIBLE_BRIDGES: StructuralClass.DEFINITION,
        FeatureId.COMPLETE_CHANNELS: StructuralClass.COMPLETE_CHANNEL,
        FeatureId.CARDINAL_ACTIVATIONS: StructuralClass.CARDINAL_ACTIVATION,
        FeatureId.CROSS_COMPONENTS: StructuralClass.CARDINAL_ACTIVATION,
        FeatureId.CROSS_NAME: StructuralClass.CARDINAL_ACTIVATION,
        FeatureId.REPEATED_GATES: StructuralClass.REPEATED_GATE_OR_NODE,
        FeatureId.NODE_ACTIVATIONS: StructuralClass.REPEATED_GATE_OR_NODE,
        FeatureId.HANGING_GATES: StructuralClass.HANGING_GATE,
        FeatureId.DORMANT_GATES: StructuralClass.HANGING_GATE,
        FeatureId.ACTIVE_GATES: StructuralClass.GENERIC_SYMBOLISM,
        FeatureId.CIRCUITRY_STATUS: StructuralClass.GENERIC_SYMBOLISM,
        FeatureId.CIRCUITRY_CHANNEL_METADATA: StructuralClass.GENERIC_SYMBOLISM,
        FeatureId.ADVANCED_STATUS: StructuralClass.GENERIC_SYMBOLISM,
        FeatureId.COLOR: StructuralClass.GENERIC_SYMBOLISM,
        FeatureId.TONE: StructuralClass.GENERIC_SYMBOLISM,
        FeatureId.BASE: StructuralClass.GENERIC_SYMBOLISM,
    }
    if feature_id in exact:
        return frozenset({exact[feature_id]})
    if feature_id in _ACTIVATION_FEATURES:
        return frozenset({StructuralClass.PROMINENT_ACTIVATION})
    return frozenset({StructuralClass.GENERIC_SYMBOLISM})
