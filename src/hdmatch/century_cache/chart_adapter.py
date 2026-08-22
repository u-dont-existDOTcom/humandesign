"""Deterministic bridge from cacheable M2 chart state to Parquet rows.

The semantic feature registry and the physical storage registry are distinct
artifacts with distinct hashes.  This adapter binds both identities and emits
every physical feature explicitly; it never turns an absent capability into a
false boolean or an empty structural value.
"""

from __future__ import annotations

from typing import Final, cast

from pydantic import BaseModel, JsonValue

from hdmatch.chart.feature_registry import (
    CACHEABLE_M0_M2_REGISTRY,
    CacheableChartStateV2,
    ChartFeatureVectorV2,
    FeatureCoverageError,
    FeatureId,
    RequiredFeatureRegistry,
    require_complete_feature_coverage,
)
from hdmatch.chart.rave_mandala import RAVE_MANDALA_VERSION

from .models import (
    CenturyStateRecord,
    FeatureColumnSpec,
    FeatureStorageType,
    FeatureValue,
    feature_registry_sha256,
)

_PHYSICAL_STORAGE_TYPES: Final[dict[FeatureId, FeatureStorageType]] = {
    FeatureId.ACTIVATION_CARRIER: FeatureStorageType.STRING_LIST,
    FeatureId.ACTIVATION_GATE: FeatureStorageType.INT64_LIST,
    FeatureId.ACTIVATION_LINE: FeatureStorageType.INT64_LIST,
    FeatureId.ACTIVATION_SIDE: FeatureStorageType.STRING_LIST,
    FeatureId.ACTIVE_GATES: FeatureStorageType.JSON,
    FeatureId.ADVANCED_STATUS: FeatureStorageType.STRING,
    FeatureId.AUTHORITY: FeatureStorageType.STRING,
    FeatureId.CARDINAL_ACTIVATIONS: FeatureStorageType.ACTIVATION_LIST,
    FeatureId.CENTERS: FeatureStorageType.JSON,
    FeatureId.CIRCUITRY_STATUS: FeatureStorageType.STRING,
    FeatureId.COMPLETE_CHANNELS: FeatureStorageType.JSON,
    FeatureId.CROSS_COMPONENTS: FeatureStorageType.STRING,
    FeatureId.DEFINITION: FeatureStorageType.STRING,
    FeatureId.DEFINITION_TOPOLOGY: FeatureStorageType.JSON,
    FeatureId.DORMANT_GATES: FeatureStorageType.INT64_LIST,
    FeatureId.HANGING_GATES: FeatureStorageType.INT64_LIST,
    FeatureId.NODE_ACTIVATIONS: FeatureStorageType.ACTIVATION_LIST,
    FeatureId.PLANETARY_ACTIVATIONS: FeatureStorageType.ACTIVATION_LIST,
    FeatureId.POSSIBLE_BRIDGES: FeatureStorageType.JSON,
    FeatureId.PROFILE: FeatureStorageType.STRING,
    FeatureId.REPEATED_GATES: FeatureStorageType.JSON,
    FeatureId.STRATEGY: FeatureStorageType.STRING,
    FeatureId.TYPE: FeatureStorageType.STRING,
}


def _compile_physical_registry() -> tuple[FeatureColumnSpec, ...]:
    semantic_ids = CACHEABLE_M0_M2_REGISTRY.feature_ids
    physical_ids = set(_PHYSICAL_STORAGE_TYPES)
    if physical_ids != set(semantic_ids):
        missing = sorted(item.value for item in set(semantic_ids) - physical_ids)
        extra = sorted(item.value for item in physical_ids - set(semantic_ids))
        raise RuntimeError(
            "physical M0-M2 feature registry differs from the semantic registry; "
            f"missing={missing}, extra={extra}"
        )
    return tuple(
        FeatureColumnSpec(
            feature_id=feature_id.value,
            storage_type=_PHYSICAL_STORAGE_TYPES[feature_id],
            nullable=False,
        )
        for feature_id in semantic_ids
    )


CACHEABLE_M0_M2_FEATURE_COLUMNS: Final[tuple[FeatureColumnSpec, ...]] = _compile_physical_registry()
CACHEABLE_M0_M2_FEATURE_COLUMNS_SHA256: Final[str] = feature_registry_sha256(
    CACHEABLE_M0_M2_FEATURE_COLUMNS
)
CACHEABLE_M0_M2_SEMANTIC_REGISTRY_SHA256: Final[str] = CACHEABLE_M0_M2_REGISTRY.sha256()


def _model_list(items: tuple[BaseModel, ...]) -> list[JsonValue]:
    return [cast(JsonValue, item.model_dump(mode="json")) for item in items]


def chart_feature_vector_to_feature_values(
    vector: ChartFeatureVectorV2,
    *,
    required_registry: RequiredFeatureRegistry = CACHEABLE_M0_M2_REGISTRY,
) -> tuple[FeatureValue, ...]:
    """Serialize all physical M0-M2 families after capability validation.

    ``required_registry`` lets a caller demand extra mapping capabilities before
    cache construction.  An unavailable conditional family fails explicitly;
    it is never encoded as ``False``, ``[]``, or ``None``.
    """

    if vector.feature_registry_sha256 != CACHEABLE_M0_M2_SEMANTIC_REGISTRY_SHA256:
        raise FeatureCoverageError(
            "M2 vector is not bound to the frozen cacheable semantic registry"
        )
    require_complete_feature_coverage(vector, required_registry)
    physical_ids = set(_PHYSICAL_STORAGE_TYPES)
    unsupported = sorted(item.value for item in set(required_registry.feature_ids) - physical_ids)
    if unsupported:
        raise FeatureCoverageError(
            "required capabilities have no frozen century-cache representation; "
            f"unsupported={unsupported}"
        )

    architecture = vector.architecture
    activations = vector.activations
    values: dict[FeatureId, object] = {
        FeatureId.TYPE: architecture.type,
        FeatureId.STRATEGY: architecture.strategy,
        FeatureId.AUTHORITY: architecture.authority,
        FeatureId.CENTERS: {
            "defined": list(architecture.defined_centers),
            "undefined": list(architecture.undefined_centers),
        },
        FeatureId.PROFILE: architecture.profile,
        FeatureId.DEFINITION: architecture.definition,
        FeatureId.DEFINITION_TOPOLOGY: [
            list(component) for component in architecture.definition_components
        ],
        FeatureId.COMPLETE_CHANNELS: _model_list(vector.complete_channels),
        FeatureId.ACTIVE_GATES: _model_list(vector.active_gates),
        FeatureId.HANGING_GATES: list(vector.hanging_gates),
        FeatureId.DORMANT_GATES: list(vector.dormant_gates),
        FeatureId.POSSIBLE_BRIDGES: _model_list(vector.possible_bridges),
        FeatureId.ACTIVATION_SIDE: [item.side for item in activations],
        FeatureId.ACTIVATION_CARRIER: [item.body.value for item in activations],
        FeatureId.ACTIVATION_GATE: [item.gate for item in activations],
        FeatureId.ACTIVATION_LINE: [item.line for item in activations],
        FeatureId.NODE_ACTIVATIONS: _model_list(vector.node_activations),
        FeatureId.CARDINAL_ACTIVATIONS: _model_list(vector.cardinal_activations),
        FeatureId.REPEATED_GATES: _model_list(vector.repeated_gates),
        FeatureId.PLANETARY_ACTIVATIONS: _model_list(activations),
        FeatureId.CROSS_COMPONENTS: vector.incarnation_cross.cardinal_component_key,
        FeatureId.CIRCUITRY_STATUS: vector.circuitry.status.value,
        FeatureId.ADVANCED_STATUS: vector.advanced_substructure.status.value,
    }
    if set(values) != physical_ids:
        missing = sorted(item.value for item in physical_ids - set(values))
        extra = sorted(item.value for item in set(values) - physical_ids)
        raise RuntimeError(
            f"M2 adapter emitted a non-canonical feature set; missing={missing}, extra={extra}"
        )
    return tuple(
        FeatureValue(
            feature_id=feature_id.value,
            value=cast(JsonValue, values[feature_id]),
        )
        for feature_id in CACHEABLE_M0_M2_REGISTRY.feature_ids
    )


def cacheable_chart_state_to_century_record(
    state: CacheableChartStateV2,
    *,
    required_registry: RequiredFeatureRegistry = CACHEABLE_M0_M2_REGISTRY,
) -> CenturyStateRecord:
    """Convert one exact cacheable chart state without changing its metadata."""

    vector = state.chart_features
    if state.feature_registry_sha256 != CACHEABLE_M0_M2_SEMANTIC_REGISTRY_SHA256:
        raise FeatureCoverageError(
            "cacheable state is not bound to the frozen M0-M2 semantic registry"
        )
    return CenturyStateRecord(
        state_id=state.state_id,
        utc_start=state.utc_start,
        utc_end=state.utc_end,
        duration_seconds=state.duration_seconds,
        representative_utc=state.representative_utc,
        design_timestamp=state.design_timestamp,
        chart_features_sha256=state.chart_features_sha256,
        feature_vector_schema_version=state.feature_vector_schema_version,
        semantic_feature_registry_sha256=state.feature_registry_sha256,
        feature_registry_sha256=CACHEABLE_M0_M2_FEATURE_COLUMNS_SHA256,
        astronomy_engine_version=vector.provenance.chart_engine_version,
        ephemeris_file_set_sha256=vector.provenance.ephemeris_file_set_sha256,
        node_convention=vector.provenance.node_convention,
        mandala_mapping_version=RAVE_MANDALA_VERSION,
        mandala_mapping_sha256=vector.provenance.mandala_mapping_sha256,
        bodygraph_mapping_sha256=vector.provenance.bodygraph_mapping_sha256,
        boundary_events=state.boundary_events,
        feature_values=chart_feature_vector_to_feature_values(
            vector,
            required_registry=required_registry,
        ),
    )
