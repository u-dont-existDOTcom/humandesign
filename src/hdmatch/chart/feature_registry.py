"""Cacheable V4.3 M0-M2 chart features and required-feature coverage.

This module contains no behavioral interpretation and no search/ranking code.
It serializes the discrete chart state that can be reused by later scorers.  A
feature whose mechanics are not provenance-backed is represented by an explicit
capability status; it is never represented by an empty collection that could be
misread as a genuine negative chart feature.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from types import TracebackType
from typing import Final, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.provenance.swisseph_files import REQUIRED_EPHEMERIS_FILES
from hdmatch.util import canonical_json_bytes, sha256_file, sha256_json

from .bodygraph import CHANNELS, Bodygraph, Center, GateActivation, derive_bodygraph
from .calculator import ChartComputation
from .ephemeris import (
    CelestialBody,
    EphemerisMetadata,
    EphemerisMode,
    SwissEphemerisProvider,
)

_SHA256_PATTERN: Final[str] = r"^[a-f0-9]{64}$"
_CHANNEL_PATTERN: Final[str] = r"^(?:[1-9]|[1-5][0-9]|6[0-4])-(?:[1-9]|[1-5][0-9]|6[0-4])$"
_ACTIVATION_SIDES: Final[tuple[str, str]] = ("personality", "design")
_CARDINAL_POSITIONS: Final[tuple[str, ...]] = (
    "personality:sun",
    "personality:earth",
    "design:sun",
    "design:earth",
)
_NODE_POSITIONS: Final[tuple[str, ...]] = (
    "personality:north_node",
    "personality:south_node",
    "design:north_node",
    "design:south_node",
)
_SESSION_FACTORY_TOKEN: Final[object] = object()


class FrozenModel(BaseModel):
    """Strict immutable base for hash-stable cache records."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class FeatureTier(StrEnum):
    """Cache layers: core architecture, topology, activations, and optional layers.

    The historical protocol labels advanced substructure as Layer 4.  M3 is
    reserved for future validated line-behavior metadata; Gate/Line coordinates
    themselves remain mandatory M2 activation data.
    """

    M0 = "M0"
    M1 = "M1"
    M2 = "M2"
    M3 = "M3"
    M4 = "M4"


class FeatureId(StrEnum):
    """Canonical feature families addressable by frozen mapping predicates."""

    TYPE = "architecture.type"
    STRATEGY = "architecture.strategy"
    AUTHORITY = "architecture.authority"
    CENTERS = "architecture.defined_centers"
    PROFILE = "architecture.profile"
    DEFINITION = "architecture.definition"
    DEFINITION_TOPOLOGY = "architecture.definition_topology"
    COMPLETE_CHANNELS = "channels.complete"
    ACTIVE_GATES = "gates.active"
    HANGING_GATES = "gates.hanging"
    DORMANT_GATES = "gates.dormant"
    POSSIBLE_BRIDGES = "definition.possible_bridges"
    ACTIVATION_SIDE = "activations.side"
    ACTIVATION_CARRIER = "activations.planetary_carrier"
    ACTIVATION_GATE = "activations.gate"
    ACTIVATION_LINE = "activations.line"
    NODE_ACTIVATIONS = "activations.nodes"
    CARDINAL_ACTIVATIONS = "activations.cardinal_sun_earth"
    REPEATED_GATES = "activations.repeated_gates"
    PLANETARY_ACTIVATIONS = "activations.all_planetary"
    CROSS_COMPONENTS = "incarnation_cross.cardinal_components"
    CROSS_NAME = "incarnation_cross.name"
    CIRCUITRY_STATUS = "circuitry.status"
    CIRCUITRY_CHANNEL_METADATA = "circuitry.channel_metadata"
    ADVANCED_STATUS = "advanced_substructure.status"
    COLOR = "advanced_substructure.color"
    TONE = "advanced_substructure.tone"
    BASE = "advanced_substructure.base"


class CapabilityStatus(StrEnum):
    AVAILABLE = "available"
    UNAVAILABLE_UNVALIDATED = "unavailable_unvalidated"


class AdvancedField(StrEnum):
    COLOR = "color"
    TONE = "tone"
    BASE = "base"


class GateEdgeKind(StrEnum):
    HANGING = "hanging"
    DORMANT = "dormant"


class FeatureCoverageError(ValueError):
    """Raised before scoring when a required feature has no usable value."""


class FeatureDefinition(FrozenModel):
    feature_id: FeatureId
    tier: FeatureTier
    cache_field: str = Field(min_length=1)
    description: str = Field(min_length=1)
    conditional_capability: bool = False


class RequiredFeatureRegistry(FrozenModel):
    schema_version: Literal["required-feature-registry-v1"] = "required-feature-registry-v1"
    feature_vector_schema_version: Literal["chart-feature-vector-v2"] = (
        "chart-feature-vector-v2"
    )
    features: tuple[FeatureDefinition, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def canonical_unique_features(self) -> RequiredFeatureRegistry:
        identities = tuple(item.feature_id for item in self.features)
        if len(identities) != len(set(identities)):
            raise ValueError("required feature registry contains duplicate feature IDs")
        if identities != tuple(sorted(identities, key=lambda item: item.value)):
            raise ValueError("required feature registry must be sorted by feature ID")
        return self

    def canonical_bytes(self) -> bytes:
        return canonical_json_bytes(self)

    def sha256(self) -> str:
        return sha256_json(self)

    @property
    def feature_ids(self) -> tuple[FeatureId, ...]:
        return tuple(item.feature_id for item in self.features)


class FeatureCoverage(FrozenModel):
    schema_version: Literal["required-feature-coverage-v1"] = (
        "required-feature-coverage-v1"
    )
    registry_sha256: str = Field(pattern=_SHA256_PATTERN)
    required_count: int = Field(ge=1)
    available_count: int = Field(ge=0)
    required_feature_coverage: float = Field(ge=0.0, le=1.0)
    missing_feature_ids: tuple[FeatureId, ...]

    @model_validator(mode="after")
    def counts_are_consistent(self) -> FeatureCoverage:
        if self.available_count + len(self.missing_feature_ids) != self.required_count:
            raise ValueError("feature coverage counts are inconsistent")
        expected = self.available_count / self.required_count
        if self.required_feature_coverage != expected:
            raise ValueError("feature coverage ratio is inconsistent with counts")
        return self


class ActivationFeature(FrozenModel):
    body: CelestialBody
    side: Literal["personality", "design"]
    gate: int = Field(ge=1, le=64)
    line: int = Field(ge=1, le=6)
    color: int | None = Field(default=None, ge=1, le=6)
    tone: int | None = Field(default=None, ge=1, le=6)
    base: int | None = Field(default=None, ge=1, le=5)

    @property
    def position(self) -> str:
        return f"{self.side}:{self.body.value}"


class ArchitectureFeatures(FrozenModel):
    type: str = Field(min_length=1)
    strategy: str = Field(min_length=1)
    authority: str = Field(min_length=1)
    profile: str = Field(pattern=r"^[1-6]/[1-6]$")
    definition: str = Field(min_length=1)
    defined_centers: tuple[str, ...]
    undefined_centers: tuple[str, ...]
    definition_components: tuple[tuple[str, ...], ...]

    @model_validator(mode="after")
    def validate_center_partition(self) -> ArchitectureFeatures:
        all_centers = {item.value for item in Center}
        defined = set(self.defined_centers)
        undefined = set(self.undefined_centers)
        if len(defined) != len(self.defined_centers):
            raise ValueError("defined centers must be unique")
        if len(undefined) != len(self.undefined_centers):
            raise ValueError("undefined centers must be unique")
        if defined & undefined or defined | undefined != all_centers:
            raise ValueError("defined and undefined centers must partition all nine centers")
        if self.defined_centers != tuple(sorted(self.defined_centers)):
            raise ValueError("defined centers must use canonical sorted order")
        if self.undefined_centers != tuple(sorted(self.undefined_centers)):
            raise ValueError("undefined centers must use canonical sorted order")
        if any(component != tuple(sorted(component)) for component in self.definition_components):
            raise ValueError("Definition component centers must use canonical sorted order")
        if self.definition_components != tuple(sorted(self.definition_components)):
            raise ValueError("Definition components must use canonical sorted order")
        flattened = [center for component in self.definition_components for center in component]
        if len(flattened) != len(set(flattened)) or set(flattened) != defined:
            raise ValueError("Definition components must partition the defined centers")
        return self


class CompleteChannelFeature(FrozenModel):
    channel: str = Field(pattern=_CHANNEL_PATTERN)
    gate_a: int = Field(ge=1, le=64)
    gate_b: int = Field(ge=1, le=64)
    center_a: str = Field(min_length=1)
    center_b: str = Field(min_length=1)

    @model_validator(mode="after")
    def identifier_matches_gates(self) -> CompleteChannelFeature:
        expected = f"{min(self.gate_a, self.gate_b)}-{max(self.gate_a, self.gate_b)}"
        if self.channel != expected or self.gate_a >= self.gate_b:
            raise ValueError("complete channel must use ascending canonical gates")
        return self


class ActiveGateFeature(FrozenModel):
    gate: int = Field(ge=1, le=64)
    activation_count: int = Field(ge=1)
    activation_positions: tuple[str, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def count_matches_positions(self) -> ActiveGateFeature:
        if self.activation_count != len(self.activation_positions):
            raise ValueError("active-gate count must equal activation-position count")
        if len(self.activation_positions) != len(set(self.activation_positions)):
            raise ValueError("active-gate activation positions must be unique")
        return self


class IncompleteChannelEdge(FrozenModel):
    channel: str = Field(pattern=_CHANNEL_PATTERN)
    active_gate: int = Field(ge=1, le=64)
    missing_gate: int = Field(ge=1, le=64)
    active_center: str = Field(min_length=1)
    missing_gate_center: str = Field(min_length=1)
    kind: GateEdgeKind

    @model_validator(mode="after")
    def edge_matches_channel(self) -> IncompleteChannelEdge:
        channel_gates = {int(value) for value in self.channel.split("-")}
        if channel_gates != {self.active_gate, self.missing_gate}:
            raise ValueError("incomplete edge gates must equal the channel gates")
        return self


class PossibleBridgeFeature(FrozenModel):
    missing_gate: int = Field(ge=1, le=64)
    active_complement_gate: int = Field(ge=1, le=64)
    channel: str = Field(pattern=_CHANNEL_PATTERN)
    definition_component_indexes: tuple[int, int]

    @model_validator(mode="after")
    def bridge_is_canonical(self) -> PossibleBridgeFeature:
        left, right = self.definition_component_indexes
        if not (0 <= left < right):
            raise ValueError("bridge component indexes must be ascending and distinct")
        return self


class ChannelCircuitry(FrozenModel):
    channel: str = Field(pattern=_CHANNEL_PATTERN)
    circuit: str = Field(min_length=1)
    subcircuit: str | None = Field(default=None, min_length=1)


class CircuitryFeatures(FrozenModel):
    status: CapabilityStatus
    source_sha256: str | None = Field(default=None, pattern=_SHA256_PATTERN)
    channels: tuple[ChannelCircuitry, ...] | None = None

    @model_validator(mode="after")
    def status_matches_values(self) -> CircuitryFeatures:
        if self.status is CapabilityStatus.AVAILABLE:
            if self.source_sha256 is None or self.channels is None:
                raise ValueError("available circuitry requires a source hash and channel values")
        elif self.source_sha256 is not None or self.channels is not None:
            raise ValueError("unavailable circuitry cannot carry inferred values")
        return self


class CrossDerivation(FrozenModel):
    cardinal_component_key: str = Field(
        pattern=r"^[1-9][0-9]?/[1-9][0-9]?\|[1-9][0-9]?/[1-9][0-9]?$"
    )
    name_status: CapabilityStatus
    name: str | None = Field(default=None, min_length=1)
    name_catalog_sha256: str | None = Field(default=None, pattern=_SHA256_PATTERN)

    @model_validator(mode="after")
    def status_matches_name(self) -> CrossDerivation:
        gate_values = tuple(
            int(value)
            for axis in self.cardinal_component_key.split("|")
            for value in axis.split("/")
        )
        if any(not 1 <= value <= 64 for value in gate_values):
            raise ValueError("Cross cardinal component gates must be in 1..64")
        if self.name_status is CapabilityStatus.AVAILABLE:
            if self.name is None or self.name_catalog_sha256 is None:
                raise ValueError("available Cross name requires name and catalog hash")
        elif self.name is not None or self.name_catalog_sha256 is not None:
            raise ValueError("unavailable Cross naming cannot carry a guessed value")
        return self


class AdvancedSubstructure(FrozenModel):
    status: CapabilityStatus
    enabled_fields: tuple[AdvancedField, ...]
    source_sha256: str | None = Field(default=None, pattern=_SHA256_PATTERN)

    @model_validator(mode="after")
    def status_matches_enabled_fields(self) -> AdvancedSubstructure:
        if len(self.enabled_fields) != len(set(self.enabled_fields)):
            raise ValueError("advanced enabled fields must be unique")
        field_order = {field: index for index, field in enumerate(AdvancedField)}
        if self.enabled_fields != tuple(
            sorted(self.enabled_fields, key=field_order.__getitem__)
        ):
            raise ValueError("advanced enabled fields must use canonical order")
        if self.status is CapabilityStatus.AVAILABLE:
            if not self.enabled_fields or self.source_sha256 is None:
                raise ValueError("available advanced substructure requires fields and source hash")
        elif self.enabled_fields or self.source_sha256 is not None:
            raise ValueError("unavailable advanced substructure cannot carry inferred fields")
        return self


class EphemerisFileIdentity(FrozenModel):
    name: str = Field(min_length=1)
    sha256: str = Field(pattern=_SHA256_PATTERN)
    bytes: int = Field(gt=0)


class FeatureVectorProvenance(FrozenModel):
    chart_engine_version: str = Field(min_length=1)
    astronomy_provider: str = Field(min_length=1)
    astronomy_library_version: str = Field(min_length=1)
    ephemeris_requested: Literal[EphemerisMode.SWIEPH] = EphemerisMode.SWIEPH
    ephemeris_requested_flags: int = Field(gt=0)
    ephemeris_mask: int = Field(gt=0)
    ephemeris_files: tuple[EphemerisFileIdentity, ...] = Field(min_length=1)
    ephemeris_file_set_sha256: str = Field(pattern=_SHA256_PATTERN)
    node_convention: Literal["true"]
    mandala_mapping_sha256: str = Field(pattern=_SHA256_PATTERN)
    bodygraph_mapping_sha256: str = Field(pattern=_SHA256_PATTERN)
    design_target_arc_degrees: float
    design_time_tolerance_seconds: float = Field(gt=0.0)
    design_arc_tolerance_degrees: float = Field(gt=0.0)

    @model_validator(mode="after")
    def verify_file_set_hash(self) -> FeatureVectorProvenance:
        names = tuple(item.name for item in self.ephemeris_files)
        if names != REQUIRED_EPHEMERIS_FILES:
            raise ValueError(
                "ephemeris file identities must use the canonical pinned file order"
            )
        expected = sha256_json([item.model_dump(mode="json") for item in self.ephemeris_files])
        if self.ephemeris_file_set_sha256 != expected:
            raise ValueError("ephemeris file-set hash does not match file identities")
        return self


class ChartFeatureVectorV2(FrozenModel):
    """Strict, cacheable discrete chart state for the V4.3 M0-M2 registry."""

    schema_version: Literal["chart-feature-vector-v2"] = "chart-feature-vector-v2"
    calculation_tier: Literal["M2"] = "M2"
    feature_registry_sha256: str = Field(pattern=_SHA256_PATTERN)
    architecture: ArchitectureFeatures
    activations: tuple[ActivationFeature, ...] = Field(min_length=1)
    cardinal_activations: tuple[ActivationFeature, ...] = Field(min_length=4, max_length=4)
    node_activations: tuple[ActivationFeature, ...] = Field(min_length=4, max_length=4)
    active_gates: tuple[ActiveGateFeature, ...] = Field(min_length=1)
    repeated_gates: tuple[ActiveGateFeature, ...]
    complete_channels: tuple[CompleteChannelFeature, ...]
    incomplete_channel_edges: tuple[IncompleteChannelEdge, ...]
    hanging_gates: tuple[int, ...]
    dormant_gates: tuple[int, ...]
    possible_bridges: tuple[PossibleBridgeFeature, ...]
    incarnation_cross: CrossDerivation
    circuitry: CircuitryFeatures
    advanced_substructure: AdvancedSubstructure
    provenance: FeatureVectorProvenance

    @model_validator(mode="after")
    def validate_complete_vector(self) -> ChartFeatureVectorV2:
        if self.feature_registry_sha256 != CACHEABLE_M0_M2_REGISTRY.sha256():
            raise ValueError("feature vector is not bound to the cacheable M0-M2 registry")
        expected_positions = {
            f"{side}:{body.value}" for side in _ACTIVATION_SIDES for body in CelestialBody
        }
        expected_position_order = tuple(
            f"{side}:{body.value}" for side in _ACTIVATION_SIDES for body in CelestialBody
        )
        by_position = {item.position: item for item in self.activations}
        if len(by_position) != len(self.activations):
            raise ValueError("activation side/carrier positions must be unique")
        if set(by_position) != expected_positions:
            missing = sorted(expected_positions - set(by_position))
            extra = sorted(set(by_position) - expected_positions)
            raise ValueError(f"complete M2 activations required; missing={missing}, extra={extra}")
        if tuple(item.position for item in self.activations) != expected_position_order:
            raise ValueError("complete M2 activations must use canonical side/carrier order")
        _require_projection(self.cardinal_activations, by_position, _CARDINAL_POSITIONS, "cardinal")
        _require_projection(self.node_activations, by_position, _NODE_POSITIONS, "Node")
        _validate_architecture_projection(self)
        _validate_active_gate_projection(self)
        _validate_channel_projection(self)
        expected_cross = (
            f"{self.cardinal_activations[0].gate}/{self.cardinal_activations[1].gate}|"
            f"{self.cardinal_activations[2].gate}/{self.cardinal_activations[3].gate}"
        )
        if self.incarnation_cross.cardinal_component_key != expected_cross:
            raise ValueError("Cross component key differs from cardinal activations")
        _validate_advanced_values(self)
        _validate_circuitry_values(self)
        return self

    def canonical_bytes(self) -> bytes:
        return canonical_json_bytes(self)

    def sha256(self) -> str:
        return sha256_json(self)

    @property
    def available_feature_ids(self) -> frozenset[FeatureId]:
        available = set(CACHEABLE_M0_M2_REGISTRY.feature_ids)
        if self.incarnation_cross.name_status is CapabilityStatus.AVAILABLE:
            available.add(FeatureId.CROSS_NAME)
        if self.circuitry.status is CapabilityStatus.AVAILABLE:
            available.add(FeatureId.CIRCUITRY_CHANNEL_METADATA)
        if self.advanced_substructure.status is CapabilityStatus.AVAILABLE:
            enabled = set(self.advanced_substructure.enabled_fields)
            if AdvancedField.COLOR in enabled:
                available.add(FeatureId.COLOR)
            if AdvancedField.TONE in enabled:
                available.add(FeatureId.TONE)
            if AdvancedField.BASE in enabled:
                available.add(FeatureId.BASE)
        return frozenset(available)


class CacheableChartStateV2(FrozenModel):
    """One exact half-open interval row suitable for the future century store."""

    schema_version: Literal["cacheable-chart-state-v2"] = "cacheable-chart-state-v2"
    state_id: str = Field(min_length=1)
    utc_start: datetime
    utc_end: datetime
    duration_seconds: float = Field(gt=0.0)
    representative_utc: datetime
    design_timestamp: datetime
    feature_vector_schema_version: Literal["chart-feature-vector-v2"] = (
        "chart-feature-vector-v2"
    )
    feature_registry_sha256: str = Field(pattern=_SHA256_PATTERN)
    chart_features_sha256: str = Field(pattern=_SHA256_PATTERN)
    chart_features: ChartFeatureVectorV2
    boundary_events: tuple[str, ...]

    @field_validator("utc_start", "utc_end", "representative_utc", "design_timestamp")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("cacheable-state timestamps must be timezone-aware")
        return value.astimezone(UTC)

    @field_validator("boundary_events")
    @classmethod
    def require_canonical_boundary_events(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        if any(not value for value in values):
            raise ValueError("boundary-event identifiers must not be empty")
        if values != tuple(sorted(set(values))):
            raise ValueError("boundary events must be sorted and unique")
        return values

    @model_validator(mode="after")
    def verify_bindings(self) -> CacheableChartStateV2:
        expected_duration = (self.utc_end - self.utc_start).total_seconds()
        if expected_duration <= 0.0 or self.duration_seconds != expected_duration:
            raise ValueError("cacheable state duration must equal its exact UTC interval")
        if not self.utc_start <= self.representative_utc < self.utc_end:
            raise ValueError("state representative UTC must lie inside the half-open interval")
        if self.design_timestamp >= self.representative_utc:
            raise ValueError("state Design timestamp must precede the representative UTC")
        if self.feature_registry_sha256 != self.chart_features.feature_registry_sha256:
            raise ValueError("state feature-registry hash differs from chart features")
        if self.chart_features_sha256 != self.chart_features.sha256():
            raise ValueError("state chart-feature hash differs from serialized features")
        return self


_FEATURE_DEFINITIONS: Final[dict[FeatureId, FeatureDefinition]] = {
    definition.feature_id: definition
    for definition in (
        FeatureDefinition(
            feature_id=FeatureId.TYPE,
            tier=FeatureTier.M0,
            cache_field="architecture.type",
            description="Mechanically derived Human Design Type.",
        ),
        FeatureDefinition(
            feature_id=FeatureId.STRATEGY,
            tier=FeatureTier.M0,
            cache_field="architecture.strategy",
            description="Strategy paired with the mechanically derived Type.",
        ),
        FeatureDefinition(
            feature_id=FeatureId.AUTHORITY,
            tier=FeatureTier.M0,
            cache_field="architecture.authority",
            description="Mechanically derived Authority.",
        ),
        FeatureDefinition(
            feature_id=FeatureId.CENTERS,
            tier=FeatureTier.M0,
            cache_field="architecture.defined_centers",
            description="Explicit defined and undefined Center partition.",
        ),
        FeatureDefinition(
            feature_id=FeatureId.PROFILE,
            tier=FeatureTier.M0,
            cache_field="architecture.profile",
            description="Personality/Design Sun-line Profile.",
        ),
        FeatureDefinition(
            feature_id=FeatureId.DEFINITION,
            tier=FeatureTier.M0,
            cache_field="architecture.definition",
            description="Definition class.",
        ),
        FeatureDefinition(
            feature_id=FeatureId.DEFINITION_TOPOLOGY,
            tier=FeatureTier.M0,
            cache_field="architecture.definition_components",
            description="Exact connected components underlying Definition.",
        ),
        FeatureDefinition(
            feature_id=FeatureId.COMPLETE_CHANNELS,
            tier=FeatureTier.M1,
            cache_field="complete_channels",
            description="Complete mechanically activated channels.",
        ),
        FeatureDefinition(
            feature_id=FeatureId.ACTIVE_GATES,
            tier=FeatureTier.M1,
            cache_field="active_gates",
            description="All active gates with exact activation positions.",
        ),
        FeatureDefinition(
            feature_id=FeatureId.HANGING_GATES,
            tier=FeatureTier.M1,
            cache_field="hanging_gates",
            description="Incomplete channel edges whose active gate is in a defined Center.",
        ),
        FeatureDefinition(
            feature_id=FeatureId.DORMANT_GATES,
            tier=FeatureTier.M1,
            cache_field="dormant_gates",
            description="Incomplete channel edges whose active gate is in an undefined Center.",
        ),
        FeatureDefinition(
            feature_id=FeatureId.POSSIBLE_BRIDGES,
            tier=FeatureTier.M1,
            cache_field="possible_bridges",
            description="Missing gates that would join separate Definition components.",
        ),
        FeatureDefinition(
            feature_id=FeatureId.ACTIVATION_SIDE,
            tier=FeatureTier.M2,
            cache_field="activations.side",
            description="Personality versus Design side for every activation.",
        ),
        FeatureDefinition(
            feature_id=FeatureId.ACTIVATION_CARRIER,
            tier=FeatureTier.M2,
            cache_field="activations.body",
            description="Planetary/body carrier for every activation.",
        ),
        FeatureDefinition(
            feature_id=FeatureId.ACTIVATION_GATE,
            tier=FeatureTier.M2,
            cache_field="activations.gate",
            description="Gate for every side/carrier activation.",
        ),
        FeatureDefinition(
            feature_id=FeatureId.ACTIVATION_LINE,
            tier=FeatureTier.M2,
            cache_field="activations.line",
            description="Line for every side/carrier activation.",
        ),
        FeatureDefinition(
            feature_id=FeatureId.NODE_ACTIVATIONS,
            tier=FeatureTier.M2,
            cache_field="node_activations",
            description="Both Nodes on Personality and Design sides under the frozen convention.",
        ),
        FeatureDefinition(
            feature_id=FeatureId.CARDINAL_ACTIVATIONS,
            tier=FeatureTier.M2,
            cache_field="cardinal_activations",
            description="Personality and Design Sun/Earth Gate/Line activations.",
        ),
        FeatureDefinition(
            feature_id=FeatureId.REPEATED_GATES,
            tier=FeatureTier.M2,
            cache_field="repeated_gates",
            description="Gates appearing at two or more side/carrier positions.",
        ),
        FeatureDefinition(
            feature_id=FeatureId.PLANETARY_ACTIVATIONS,
            tier=FeatureTier.M2,
            cache_field="activations",
            description="All declared planetary carriers, not a post-hoc prominence subset.",
        ),
        FeatureDefinition(
            feature_id=FeatureId.CROSS_COMPONENTS,
            tier=FeatureTier.M2,
            cache_field="incarnation_cross.cardinal_component_key",
            description="Cross component key derived only from the four cardinal gates.",
        ),
        FeatureDefinition(
            feature_id=FeatureId.CROSS_NAME,
            tier=FeatureTier.M2,
            cache_field="incarnation_cross.name",
            description="Named Cross from a provenance-backed catalog when available.",
            conditional_capability=True,
        ),
        FeatureDefinition(
            feature_id=FeatureId.CIRCUITRY_STATUS,
            tier=FeatureTier.M2,
            cache_field="circuitry.status",
            description="Explicit circuitry capability status.",
        ),
        FeatureDefinition(
            feature_id=FeatureId.CIRCUITRY_CHANNEL_METADATA,
            tier=FeatureTier.M2,
            cache_field="circuitry.channels",
            description="Channel circuit/subcircuit metadata from a frozen source table.",
            conditional_capability=True,
        ),
        FeatureDefinition(
            feature_id=FeatureId.ADVANCED_STATUS,
            tier=FeatureTier.M2,
            cache_field="advanced_substructure.status",
            description="Explicit advanced-substructure capability status.",
        ),
        FeatureDefinition(
            feature_id=FeatureId.COLOR,
            tier=FeatureTier.M4,
            cache_field="activations.color",
            description="Color when independently validated and enabled.",
            conditional_capability=True,
        ),
        FeatureDefinition(
            feature_id=FeatureId.TONE,
            tier=FeatureTier.M4,
            cache_field="activations.tone",
            description="Tone when independently validated and enabled.",
            conditional_capability=True,
        ),
        FeatureDefinition(
            feature_id=FeatureId.BASE,
            tier=FeatureTier.M4,
            cache_field="activations.base",
            description="Base when independently validated and enabled.",
            conditional_capability=True,
        ),
    )
}

_CACHEABLE_M0_M2_FEATURE_IDS: Final[tuple[FeatureId, ...]] = (
    FeatureId.TYPE,
    FeatureId.STRATEGY,
    FeatureId.AUTHORITY,
    FeatureId.CENTERS,
    FeatureId.PROFILE,
    FeatureId.DEFINITION,
    FeatureId.DEFINITION_TOPOLOGY,
    FeatureId.COMPLETE_CHANNELS,
    FeatureId.ACTIVE_GATES,
    FeatureId.HANGING_GATES,
    FeatureId.DORMANT_GATES,
    FeatureId.POSSIBLE_BRIDGES,
    FeatureId.ACTIVATION_SIDE,
    FeatureId.ACTIVATION_CARRIER,
    FeatureId.ACTIVATION_GATE,
    FeatureId.ACTIVATION_LINE,
    FeatureId.NODE_ACTIVATIONS,
    FeatureId.CARDINAL_ACTIVATIONS,
    FeatureId.REPEATED_GATES,
    FeatureId.PLANETARY_ACTIVATIONS,
    FeatureId.CROSS_COMPONENTS,
    FeatureId.CIRCUITRY_STATUS,
    FeatureId.ADVANCED_STATUS,
)


def compile_required_feature_registry(
    feature_ids: Iterable[FeatureId | str],
) -> RequiredFeatureRegistry:
    """Compile and deterministically hash the union of mapping-required families."""

    parsed: set[FeatureId] = set()
    for raw in feature_ids:
        try:
            parsed.add(raw if isinstance(raw, FeatureId) else FeatureId(raw))
        except ValueError as exc:
            raise FeatureCoverageError(f"unknown required feature family: {raw}") from exc
    if not parsed:
        raise FeatureCoverageError("required feature registry cannot be empty")
    return RequiredFeatureRegistry(
        features=tuple(_FEATURE_DEFINITIONS[item] for item in sorted(parsed, key=lambda x: x.value))
    )


CACHEABLE_M0_M2_REGISTRY: Final[RequiredFeatureRegistry] = compile_required_feature_registry(
    _CACHEABLE_M0_M2_FEATURE_IDS
)


def assess_required_feature_coverage(
    chart: object,
    registry: RequiredFeatureRegistry,
) -> FeatureCoverage:
    """Return explicit coverage; reduced/non-V2 vectors have zero usable coverage."""

    available = (
        chart.available_feature_ids
        if isinstance(chart, ChartFeatureVectorV2)
        else frozenset()
    )
    missing = tuple(item for item in registry.feature_ids if item not in available)
    count = len(registry.features)
    available_count = count - len(missing)
    return FeatureCoverage(
        registry_sha256=registry.sha256(),
        required_count=count,
        available_count=available_count,
        required_feature_coverage=available_count / count,
        missing_feature_ids=missing,
    )


def require_complete_feature_coverage(
    chart: object,
    registry: RequiredFeatureRegistry,
) -> FeatureCoverage:
    """Fail before predicate evaluation unless every required feature is usable."""

    coverage = assess_required_feature_coverage(chart, registry)
    if coverage.required_feature_coverage != 1.0:
        missing = ", ".join(item.value for item in coverage.missing_feature_ids)
        raise FeatureCoverageError(
            "required feature coverage is below 1.0; "
            f"schema={type(chart).__name__}, missing=[{missing}]"
        )
    return coverage


class _CacheableSerializationSession:
    """Bounded, fail-closed file-integrity scope for high-volume serialization.

    Construction is deliberately restricted to :func:`cacheable_serialization_session`.
    Values produced inside the scope are provisional until clean context exit has
    reverified the exact Swiss files captured on entry.
    """

    __slots__ = ("_active", "_closed", "_metadata", "_provider")

    def __init__(
        self,
        provider: SwissEphemerisProvider,
        *,
        _factory_token: object,
    ) -> None:
        if _factory_token is not _SESSION_FACTORY_TOKEN:
            raise FeatureCoverageError(
                "cacheable serialization sessions must be created by the public factory"
            )
        self._provider = provider
        self._metadata: EphemerisMetadata | None = None
        self._active = False
        self._closed = False

    def __enter__(self) -> _CacheableSerializationSession:
        if self._active or self._closed:
            raise FeatureCoverageError("cacheable serialization session cannot be reopened")
        self._metadata = _verify_production_provider_boundary(self._provider)
        self._active = True
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> Literal[False]:
        del exc_type, exc_value, traceback
        try:
            if self._metadata is not None:
                _verify_production_provider_boundary(
                    self._provider,
                    expected_metadata=self._metadata,
                )
        finally:
            self._active = False
            self._closed = True
        return False

    def serialize_chart_feature_vector(
        self,
        computation: ChartComputation,
        *,
        provider: SwissEphemerisProvider,
        circuitry: CircuitryFeatures | None = None,
        cross_name: str | None = None,
        cross_name_catalog_sha256: str | None = None,
        advanced_substructure: AdvancedSubstructure | None = None,
        advanced_values: Mapping[str, Mapping[AdvancedField | str, int]] | None = None,
    ) -> ChartFeatureVectorV2:
        metadata = self._require_active_binding(computation, provider)
        assert metadata.requested_flags is not None
        assert metadata.ephemeris_mask is not None
        return _serialize_chart_feature_vector(
            computation,
            ephemeris_requested_flags=metadata.requested_flags,
            ephemeris_mask=metadata.ephemeris_mask,
            circuitry=circuitry,
            cross_name=cross_name,
            cross_name_catalog_sha256=cross_name_catalog_sha256,
            advanced_substructure=advanced_substructure,
            advanced_values=advanced_values,
        )

    def serialize_cacheable_chart_state(
        self,
        computation: ChartComputation,
        *,
        provider: SwissEphemerisProvider,
        utc_start: datetime,
        utc_end: datetime,
        boundary_events: Iterable[str] = (),
        circuitry: CircuitryFeatures | None = None,
    ) -> CacheableChartStateV2:
        vector = self.serialize_chart_feature_vector(
            computation,
            provider=provider,
            circuitry=circuitry,
        )
        return _cacheable_state_from_vector(
            computation,
            vector,
            utc_start=utc_start,
            utc_end=utc_end,
            boundary_events=boundary_events,
        )

    def _require_active_binding(
        self,
        computation: ChartComputation,
        provider: SwissEphemerisProvider,
    ) -> EphemerisMetadata:
        if not self._active or self._closed or self._metadata is None:
            raise FeatureCoverageError("cacheable serialization session is not active")
        if provider is not self._provider:
            raise FeatureCoverageError(
                "cacheable serialization session cannot be used with a different provider"
            )
        if provider.metadata != self._metadata:
            raise FeatureCoverageError(
                "Swiss provider metadata changed during cacheable serialization session"
            )
        if computation.metadata.ephemeris != self._metadata:
            raise FeatureCoverageError(
                "chart computation ephemeris metadata differs from the active session"
            )
        return self._metadata


def cacheable_serialization_session(
    provider: SwissEphemerisProvider,
) -> _CacheableSerializationSession:
    """Create a bounded high-volume serialization scope.

    The returned object must be used as a context manager.  The provider and
    exact ``.se1`` bytes are verified once at entry and once at exit; each row
    remains bound to the captured immutable metadata without redundant disk I/O.
    Do not publish rows before successful context exit.
    """

    return _CacheableSerializationSession(
        provider,
        _factory_token=_SESSION_FACTORY_TOKEN,
    )


def serialize_chart_feature_vector(
    computation: ChartComputation,
    *,
    provider: SwissEphemerisProvider,
    circuitry: CircuitryFeatures | None = None,
    cross_name: str | None = None,
    cross_name_catalog_sha256: str | None = None,
    advanced_substructure: AdvancedSubstructure | None = None,
    advanced_values: Mapping[str, Mapping[AdvancedField | str, int]] | None = None,
) -> ChartFeatureVectorV2:
    """Safely serialize one chart with entry/exit file-integrity verification."""

    with cacheable_serialization_session(provider) as session:
        return session.serialize_chart_feature_vector(
            computation,
            provider=provider,
            circuitry=circuitry,
            cross_name=cross_name,
            cross_name_catalog_sha256=cross_name_catalog_sha256,
            advanced_substructure=advanced_substructure,
            advanced_values=advanced_values,
        )


def _serialize_chart_feature_vector(
    computation: ChartComputation,
    *,
    ephemeris_requested_flags: int,
    ephemeris_mask: int,
    circuitry: CircuitryFeatures | None = None,
    cross_name: str | None = None,
    cross_name_catalog_sha256: str | None = None,
    advanced_substructure: AdvancedSubstructure | None = None,
    advanced_values: Mapping[str, Mapping[AdvancedField | str, int]] | None = None,
) -> ChartFeatureVectorV2:
    """Serialize one chart already bound to an active production session."""

    circuitry_value = circuitry or CircuitryFeatures(
        status=CapabilityStatus.UNAVAILABLE_UNVALIDATED
    )
    advanced_value = advanced_substructure or AdvancedSubstructure(
        status=CapabilityStatus.UNAVAILABLE_UNVALIDATED,
        enabled_fields=(),
    )
    raw_advanced = advanced_values or {}
    _validate_advanced_input(advanced_value, raw_advanced)
    activations = tuple(
        ActivationFeature(
            body=item.body,
            side=item.side,
            gate=item.gate,
            line=item.line,
            color=_advanced_value(
                raw_advanced,
                f"{item.side}:{item.body.value}",
                AdvancedField.COLOR,
            ),
            tone=_advanced_value(
                raw_advanced,
                f"{item.side}:{item.body.value}",
                AdvancedField.TONE,
            ),
            base=_advanced_value(
                raw_advanced,
                f"{item.side}:{item.body.value}",
                AdvancedField.BASE,
            ),
        )
        for item in computation.activations
    )
    by_position = {item.position: item for item in activations}
    cardinal = tuple(by_position[position] for position in _CARDINAL_POSITIONS)
    nodes = tuple(by_position[position] for position in _NODE_POSITIONS)
    active_gates = _active_gate_features(activations)
    repeated_gates = tuple(item for item in active_gates if item.activation_count >= 2)
    complete_channels = _complete_channel_features(computation)
    incomplete_edges = _incomplete_channel_edges(computation)
    hanging = tuple(
        sorted(
            item.active_gate
            for item in incomplete_edges
            if item.kind is GateEdgeKind.HANGING
        )
    )
    dormant = tuple(
        sorted(
            item.active_gate
            for item in incomplete_edges
            if item.kind is GateEdgeKind.DORMANT
        )
    )
    bridges = _possible_bridges(computation, incomplete_edges)
    personality_sun, personality_earth, design_sun, design_earth = cardinal
    cross = CrossDerivation(
        cardinal_component_key=(
            f"{personality_sun.gate}/{personality_earth.gate}|"
            f"{design_sun.gate}/{design_earth.gate}"
        ),
        name_status=(
            CapabilityStatus.AVAILABLE
            if cross_name is not None and cross_name_catalog_sha256 is not None
            else CapabilityStatus.UNAVAILABLE_UNVALIDATED
        ),
        name=cross_name,
        name_catalog_sha256=cross_name_catalog_sha256,
    )
    ephemeris_by_name = {
        Path(item.path).name: item for item in computation.metadata.ephemeris.files
    }
    ephemeris_files = tuple(
        EphemerisFileIdentity(
            name=name,
            sha256=item.sha256,
            bytes=item.size_bytes,
        )
        for name in REQUIRED_EPHEMERIS_FILES
        for item in (ephemeris_by_name[name],)
    )
    if not ephemeris_files:
        raise FeatureCoverageError("cacheable M2 vectors require hashed ephemeris files")
    provenance = FeatureVectorProvenance(
        chart_engine_version=computation.metadata.chart_engine_version,
        astronomy_provider=computation.metadata.ephemeris.provider,
        astronomy_library_version=computation.metadata.ephemeris.library_version,
        ephemeris_requested_flags=ephemeris_requested_flags,
        ephemeris_mask=ephemeris_mask,
        ephemeris_files=ephemeris_files,
        ephemeris_file_set_sha256=sha256_json(
            [item.model_dump(mode="json") for item in ephemeris_files]
        ),
        node_convention="true",
        mandala_mapping_sha256=computation.metadata.mandala_constants_sha256,
        bodygraph_mapping_sha256=computation.metadata.bodygraph_constants_sha256,
        design_target_arc_degrees=computation.metadata.design_target_arc_degrees,
        design_time_tolerance_seconds=computation.metadata.design_time_tolerance_seconds,
        design_arc_tolerance_degrees=computation.metadata.design_arc_tolerance_degrees,
    )
    vector = ChartFeatureVectorV2(
        feature_registry_sha256=CACHEABLE_M0_M2_REGISTRY.sha256(),
        architecture=_architecture_features(computation.bodygraph),
        activations=activations,
        cardinal_activations=cardinal,
        node_activations=nodes,
        active_gates=active_gates,
        repeated_gates=repeated_gates,
        complete_channels=complete_channels,
        incomplete_channel_edges=incomplete_edges,
        hanging_gates=hanging,
        dormant_gates=dormant,
        possible_bridges=bridges,
        incarnation_cross=cross,
        circuitry=circuitry_value,
        advanced_substructure=advanced_value,
        provenance=provenance,
    )
    require_complete_feature_coverage(vector, CACHEABLE_M0_M2_REGISTRY)
    return vector


def serialize_cacheable_chart_state(
    computation: ChartComputation,
    *,
    provider: SwissEphemerisProvider,
    utc_start: datetime,
    utc_end: datetime,
    boundary_events: Iterable[str] = (),
    circuitry: CircuitryFeatures | None = None,
) -> CacheableChartStateV2:
    """Safely serialize one already-derived exact interval; find no boundaries."""

    with cacheable_serialization_session(provider) as session:
        return session.serialize_cacheable_chart_state(
            computation,
            provider=provider,
            utc_start=utc_start,
            utc_end=utc_end,
            boundary_events=boundary_events,
            circuitry=circuitry,
        )


def _cacheable_state_from_vector(
    computation: ChartComputation,
    vector: ChartFeatureVectorV2,
    *,
    utc_start: datetime,
    utc_end: datetime,
    boundary_events: Iterable[str],
) -> CacheableChartStateV2:
    start = _require_utc(utc_start)
    end = _require_utc(utc_end)
    representative = _require_utc(computation.personality_utc)
    state_id = "STATE-V2-" + sha256_json(
        {
            "utc_start": start.isoformat(),
            "utc_end": end.isoformat(),
            "chart_features_sha256": vector.sha256(),
        }
    )[:24].upper()
    return CacheableChartStateV2(
        state_id=state_id,
        utc_start=start,
        utc_end=end,
        duration_seconds=(end - start).total_seconds(),
        representative_utc=representative,
        design_timestamp=computation.design_utc,
        feature_registry_sha256=vector.feature_registry_sha256,
        chart_features_sha256=vector.sha256(),
        chart_features=vector,
        boundary_events=tuple(boundary_events),
    )


def _verify_production_provider_boundary(
    provider: SwissEphemerisProvider,
    *,
    expected_metadata: EphemerisMetadata | None = None,
) -> EphemerisMetadata:
    if not isinstance(provider, SwissEphemerisProvider):
        raise FeatureCoverageError(
            "cacheable M2 serialization requires the strict SwissEphemerisProvider"
        )
    metadata = provider.metadata
    if expected_metadata is not None:
        _verify_declared_ephemeris_files(expected_metadata)
    if expected_metadata is not None and metadata != expected_metadata:
        raise FeatureCoverageError(
            "Swiss provider metadata changed during cacheable serialization session"
        )
    if metadata.provider != "swiss_ephemeris_local_files":
        raise FeatureCoverageError(
            "cacheable M2 serialization requires exact local Swiss-file provider identity"
        )
    if metadata.requested_ephemeris is not EphemerisMode.SWIEPH:
        raise FeatureCoverageError(
            "cacheable M2 vector requires an engine that explicitly requested SWIEPH"
        )
    if metadata.requested_flags is None or metadata.ephemeris_mask is None:
        raise FeatureCoverageError(
            "cacheable M2 vector requires explicit ephemeris request and mode-mask flags"
        )
    if metadata.node_convention.value != "true":
        raise FeatureCoverageError(
            "cacheable M2 serialization requires the frozen true-Node convention"
        )
    expected_names = {"sepl_18.se1", "semo_18.se1"}
    observed_names = {Path(item.path).name for item in metadata.files}
    if observed_names != expected_names or len(metadata.files) != len(expected_names):
        raise FeatureCoverageError(
            "cacheable M2 serialization requires exactly sepl_18.se1 and semo_18.se1"
        )
    if expected_metadata is None:
        _verify_declared_ephemeris_files(metadata)
    return metadata


def _verify_declared_ephemeris_files(metadata: EphemerisMetadata) -> None:
    for item in metadata.files:
        path = Path(item.path)
        if not path.is_file():
            raise FeatureCoverageError(
                f"declared production ephemeris file is no longer available: {path.name}"
            )
        if path.stat().st_size != item.size_bytes or sha256_file(path) != item.sha256:
            raise FeatureCoverageError(
                f"declared production ephemeris bytes changed after provider setup: {path.name}"
            )


def _validate_advanced_input(
    capability: AdvancedSubstructure,
    values: Mapping[str, Mapping[AdvancedField | str, int]],
) -> None:
    if capability.status is CapabilityStatus.UNAVAILABLE_UNVALIDATED:
        if values:
            raise FeatureCoverageError(
                "advanced values were supplied while advanced substructure is unavailable"
            )
        return
    expected_positions = {
        f"{side}:{body.value}" for side in _ACTIVATION_SIDES for body in CelestialBody
    }
    observed_positions = set(values)
    if observed_positions != expected_positions:
        missing = sorted(expected_positions - observed_positions)
        extra = sorted(observed_positions - expected_positions)
        raise FeatureCoverageError(
            "enabled advanced input must cover exactly every activation position; "
            f"missing={missing}, extra={extra}"
        )
    enabled = set(capability.enabled_fields)
    for position, by_field in values.items():
        parsed_fields: set[AdvancedField] = set()
        for raw_field in by_field:
            try:
                parsed_fields.add(
                    raw_field
                    if isinstance(raw_field, AdvancedField)
                    else AdvancedField(raw_field)
                )
            except ValueError as exc:
                raise FeatureCoverageError(
                    f"unknown advanced field at {position}: {raw_field}"
                ) from exc
        if parsed_fields != enabled or len(by_field) != len(enabled):
            raise FeatureCoverageError(
                f"advanced fields at {position} differ from the enabled field set"
            )


def _active_gate_features(
    activations: tuple[ActivationFeature, ...],
) -> tuple[ActiveGateFeature, ...]:
    positions: dict[int, list[str]] = {}
    for activation in activations:
        positions.setdefault(activation.gate, []).append(activation.position)
    return tuple(
        ActiveGateFeature(
            gate=gate,
            activation_count=len(values),
            activation_positions=tuple(sorted(values)),
        )
        for gate, values in sorted(positions.items())
    )


def _complete_channel_features(
    computation: ChartComputation,
) -> tuple[CompleteChannelFeature, ...]:
    complete = set(computation.bodygraph.channels)
    return tuple(
        CompleteChannelFeature(
            channel=channel.identifier,
            gate_a=min(channel.gate_a, channel.gate_b),
            gate_b=max(channel.gate_a, channel.gate_b),
            center_a=channel.center_a.value,
            center_b=channel.center_b.value,
        )
        for channel in CHANNELS
        if channel.identifier in complete
    )


def _incomplete_channel_edges(
    computation: ChartComputation,
) -> tuple[IncompleteChannelEdge, ...]:
    active_gates = set(computation.bodygraph.active_gates)
    defined = set(computation.bodygraph.defined_centers)
    result: list[IncompleteChannelEdge] = []
    for channel in CHANNELS:
        left_active = channel.gate_a in active_gates
        right_active = channel.gate_b in active_gates
        if left_active == right_active:
            continue
        if left_active:
            active_gate, missing_gate = channel.gate_a, channel.gate_b
            active_center, missing_center = channel.center_a, channel.center_b
        else:
            active_gate, missing_gate = channel.gate_b, channel.gate_a
            active_center, missing_center = channel.center_b, channel.center_a
        result.append(
            IncompleteChannelEdge(
                channel=channel.identifier,
                active_gate=active_gate,
                missing_gate=missing_gate,
                active_center=active_center.value,
                missing_gate_center=missing_center.value,
                kind=(
                    GateEdgeKind.HANGING
                    if active_center in defined
                    else GateEdgeKind.DORMANT
                ),
            )
        )
    return tuple(sorted(result, key=lambda item: (item.channel, item.active_gate)))


def _possible_bridges(
    computation: ChartComputation,
    edges: tuple[IncompleteChannelEdge, ...],
) -> tuple[PossibleBridgeFeature, ...]:
    component_by_center = {
        center.value: index
        for index, component in enumerate(computation.bodygraph.definition_components)
        for center in component
    }
    result: list[PossibleBridgeFeature] = []
    for edge in edges:
        left = component_by_center.get(edge.active_center)
        right = component_by_center.get(edge.missing_gate_center)
        if left is None or right is None or left == right:
            continue
        result.append(
            PossibleBridgeFeature(
                missing_gate=edge.missing_gate,
                active_complement_gate=edge.active_gate,
                channel=edge.channel,
                definition_component_indexes=(min(left, right), max(left, right)),
            )
        )
    return tuple(
        sorted(
            result,
            key=lambda item: (
                item.missing_gate,
                item.active_complement_gate,
                item.channel,
                item.definition_component_indexes,
            ),
        )
    )


def _validate_active_gate_projection(vector: ChartFeatureVectorV2) -> None:
    positions_by_gate: dict[int, list[str]] = {}
    for activation in vector.activations:
        positions_by_gate.setdefault(activation.gate, []).append(activation.position)
    expected = tuple(
        (gate, tuple(sorted(positions))) for gate, positions in sorted(positions_by_gate.items())
    )
    actual = tuple((item.gate, item.activation_positions) for item in vector.active_gates)
    if actual != expected:
        raise ValueError("active gates are inconsistent with activations")
    expected_repeated = tuple(item for item in vector.active_gates if item.activation_count >= 2)
    if vector.repeated_gates != expected_repeated:
        raise ValueError("repeated gates are inconsistent with activation counts")


def _validate_architecture_projection(vector: ChartFeatureVectorV2) -> None:
    bodygraph = derive_bodygraph(
        GateActivation(
            body=item.body,
            side=item.side,
            longitude=0.0,
            gate=item.gate,
            line=item.line,
        )
        for item in vector.activations
    )
    expected = _architecture_features(bodygraph)
    if vector.architecture != expected:
        raise ValueError(
            "declared architecture differs from the BodyGraph mechanically derived "
            "from activations"
        )
    if tuple(item.channel for item in vector.complete_channels) != bodygraph.channels:
        raise ValueError(
            "declared complete channels differ from the BodyGraph mechanically derived "
            "from activations"
        )


def _validate_channel_projection(vector: ChartFeatureVectorV2) -> None:
    active_gates = {item.gate for item in vector.active_gates}
    expected_channel_specs = tuple(
        channel
        for channel in CHANNELS
        if channel.gate_a in active_gates and channel.gate_b in active_gates
    )
    expected_channel_ids = tuple(channel.identifier for channel in expected_channel_specs)
    if tuple(item.channel for item in vector.complete_channels) != expected_channel_ids:
        raise ValueError("complete channels are inconsistent with active gates")
    for actual, expected in zip(vector.complete_channels, expected_channel_specs, strict=True):
        if (
            actual.gate_a,
            actual.gate_b,
            {actual.center_a, actual.center_b},
        ) != (
            min(expected.gate_a, expected.gate_b),
            max(expected.gate_a, expected.gate_b),
            {expected.center_a.value, expected.center_b.value},
        ):
            raise ValueError("complete channel metadata differs from frozen channel mechanics")
    edges = {
        (item.channel, item.active_gate, item.missing_gate)
        for item in vector.incomplete_channel_edges
    }
    expected_edges: set[tuple[str, int, int]] = set()
    for channel in CHANNELS:
        active = [gate for gate in (channel.gate_a, channel.gate_b) if gate in active_gates]
        if len(active) == 1:
            missing = channel.gate_b if active[0] == channel.gate_a else channel.gate_a
            expected_edges.add((channel.identifier, active[0], missing))
    if edges != expected_edges:
        raise ValueError("incomplete channel edges are inconsistent with active gates")
    if vector.incomplete_channel_edges != tuple(
        sorted(
            vector.incomplete_channel_edges,
            key=lambda item: (item.channel, item.active_gate),
        )
    ):
        raise ValueError("incomplete channel edges must use canonical order")
    defined = set(vector.architecture.defined_centers)
    channel_by_id = {channel.identifier: channel for channel in CHANNELS}
    for edge in vector.incomplete_channel_edges:
        channel = channel_by_id[edge.channel]
        if edge.active_gate == channel.gate_a:
            expected_active_center = channel.center_a.value
            expected_missing_center = channel.center_b.value
        else:
            expected_active_center = channel.center_b.value
            expected_missing_center = channel.center_a.value
        if (
            edge.active_center != expected_active_center
            or edge.missing_gate_center != expected_missing_center
        ):
            raise ValueError(
                "incomplete channel edge Center metadata differs from frozen channel mechanics"
            )
        expected_kind = (
            GateEdgeKind.HANGING
            if edge.active_center in defined
            else GateEdgeKind.DORMANT
        )
        if edge.kind is not expected_kind:
            raise ValueError("incomplete channel edge kind differs from Center state")
    if vector.hanging_gates != tuple(
        sorted(
            item.active_gate
            for item in vector.incomplete_channel_edges
            if item.kind is GateEdgeKind.HANGING
        )
    ):
        raise ValueError("hanging gates are inconsistent with incomplete channel edges")
    if vector.dormant_gates != tuple(
        sorted(
            item.active_gate
            for item in vector.incomplete_channel_edges
            if item.kind is GateEdgeKind.DORMANT
        )
    ):
        raise ValueError("dormant gates are inconsistent with incomplete channel edges")
    component_by_center = {
        center: index
        for index, component in enumerate(vector.architecture.definition_components)
        for center in component
    }
    expected_bridges: list[tuple[int, int, str, tuple[int, int]]] = []
    for edge in vector.incomplete_channel_edges:
        left = component_by_center.get(edge.active_center)
        right = component_by_center.get(edge.missing_gate_center)
        if left is None or right is None or left == right:
            continue
        expected_bridges.append(
            (
                edge.missing_gate,
                edge.active_gate,
                edge.channel,
                (min(left, right), max(left, right)),
            )
        )
    actual_bridges = [
        (
            item.missing_gate,
            item.active_complement_gate,
            item.channel,
            item.definition_component_indexes,
        )
        for item in vector.possible_bridges
    ]
    if actual_bridges != sorted(expected_bridges):
        raise ValueError("possible bridges are inconsistent with Definition topology")


def _validate_advanced_values(vector: ChartFeatureVectorV2) -> None:
    enabled = set(vector.advanced_substructure.enabled_fields)
    for activation in vector.activations:
        values = {
            AdvancedField.COLOR: activation.color,
            AdvancedField.TONE: activation.tone,
            AdvancedField.BASE: activation.base,
        }
        for field, value in values.items():
            if field in enabled and value is None:
                raise ValueError(f"enabled {field.value} is missing at {activation.position}")
            if field not in enabled and value is not None:
                raise ValueError(f"disabled {field.value} cannot carry a value")


def _validate_circuitry_values(vector: ChartFeatureVectorV2) -> None:
    if vector.circuitry.status is not CapabilityStatus.AVAILABLE:
        return
    assert vector.circuitry.channels is not None
    declared = tuple(item.channel for item in vector.circuitry.channels)
    if len(declared) != len(set(declared)):
        raise ValueError("circuitry channels must be unique")
    complete = tuple(item.channel for item in vector.complete_channels)
    if declared != complete:
        raise ValueError("available circuitry must classify every complete channel exactly once")


def _architecture_features(bodygraph: Bodygraph) -> ArchitectureFeatures:
    all_centers = {item.value for item in Center}
    defined = {item.value for item in bodygraph.defined_centers}
    return ArchitectureFeatures(
        type=bodygraph.type.value,
        strategy=bodygraph.strategy.value,
        authority=bodygraph.authority.value,
        profile=bodygraph.profile,
        definition=bodygraph.definition.value,
        defined_centers=tuple(sorted(defined)),
        undefined_centers=tuple(sorted(all_centers - defined)),
        definition_components=tuple(
            tuple(center.value for center in component)
            for component in bodygraph.definition_components
        ),
    )


def _require_projection(
    projection: tuple[ActivationFeature, ...],
    by_position: Mapping[str, ActivationFeature],
    expected_positions: tuple[str, ...],
    label: str,
) -> None:
    if tuple(item.position for item in projection) != expected_positions:
        raise ValueError(f"{label} activation projection has wrong positions or order")
    if projection != tuple(by_position[position] for position in expected_positions):
        raise ValueError(f"{label} activation projection differs from full activations")


def _advanced_value(
    values: Mapping[str, Mapping[AdvancedField | str, int]],
    position: str,
    field: AdvancedField,
) -> int | None:
    by_field = values.get(position)
    if by_field is None:
        return None
    raw = by_field.get(field)
    if raw is None:
        raw = by_field.get(field.value)
    return raw


def _require_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("cacheable-state timestamps must be timezone-aware")
    return value.astimezone(UTC)


if set(_FEATURE_DEFINITIONS) != set(FeatureId):
    raise RuntimeError("every feature family requires exactly one frozen definition")
