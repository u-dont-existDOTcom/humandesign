"""Deterministic bridge from cacheable M2 chart state to Parquet rows.

The semantic feature registry and the physical storage registry are distinct
artifacts with distinct hashes.  This adapter binds both identities and emits
every physical feature explicitly; it never turns an absent capability into a
false boolean or an empty structural value.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
from collections.abc import Iterator
from datetime import datetime
from typing import Final, cast

from pydantic import BaseModel, JsonValue

from hdmatch.chart.boundaries import (
    BOUNDARY_POLICY_VERSION,
    StableInterval,
    audit_interval_partition,
    build_production_chart_state_intervals,
    canonical_boundary_event_string,
)
from hdmatch.chart.calculator import ChartComputation
from hdmatch.chart.ephemeris import SwissEphemerisProvider
from hdmatch.chart.feature_registry import (
    CACHEABLE_M0_M2_REGISTRY,
    CacheableChartStateV2,
    ChartFeatureVectorV2,
    FeatureCoverageError,
    FeatureId,
    RequiredFeatureRegistry,
    cacheable_serialization_session,
    require_complete_feature_coverage,
)
from hdmatch.chart.rave_mandala import RAVE_MANDALA_VERSION
from hdmatch.chart.validation import canonical_sha256
from hdmatch.experiments.canonical import canonical_json_bytes, sha256_json

from .models import (
    CenturyStateRecord,
    ExactStateBatchProvenance,
    ExactStateUniverseProvenance,
    FeatureColumnSpec,
    FeatureStorageType,
    FeatureValue,
    canonical_rows_sha256,
    discrete_chart_identity_sha256,
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
_EXACT_STATE_BATCH_FACTORY_TOKEN: Final[object] = object()
_EXACT_STATE_SHARD_SET_FACTORY_TOKEN: Final[object] = object()
_EXACT_STATE_RECONCILIATION_MINT_TOKEN: Final[object] = object()
_EXACT_STATE_MINT_BINDING_KEY: Final[bytes] = secrets.token_bytes(32)


class ExactStateBatchError(ValueError):
    """Production boundary output could not be certified as exact cache rows."""


def _factory_private_binding(kind: str, provenance: BaseModel) -> str:
    payload = canonical_json_bytes(
        {
            "kind": kind,
            "provenance": provenance.model_dump(mode="json"),
        }
    )
    return hmac.new(
        _EXACT_STATE_MINT_BINDING_KEY,
        payload,
        digestmod=hashlib.sha256,
    ).hexdigest()


class VerifiedExactStateBatch:
    """One bounded build job minted only by the production exact-state factory."""

    __slots__ = ("_factory_token", "_mint_binding", "_provenance", "_rows")
    _factory_token: object
    _mint_binding: str
    _provenance: ExactStateBatchProvenance
    _rows: tuple[CenturyStateRecord, ...]

    def __init__(
        self,
        *,
        rows: tuple[CenturyStateRecord, ...],
        provenance: ExactStateBatchProvenance,
        _factory_token: object,
    ) -> None:
        if _factory_token is not _EXACT_STATE_BATCH_FACTORY_TOKEN:
            raise ExactStateBatchError(
                "verified exact-state batches must be created by the production factory"
            )
        object.__setattr__(self, "_rows", rows)
        object.__setattr__(self, "_provenance", provenance)
        object.__setattr__(self, "_factory_token", _factory_token)
        object.__setattr__(
            self,
            "_mint_binding",
            _factory_private_binding("bounded-exact-state-batch", provenance),
        )

    def __setattr__(self, name: str, value: object) -> None:
        del name, value
        raise AttributeError("VerifiedExactStateBatch is immutable")

    @property
    def rows(self) -> tuple[CenturyStateRecord, ...]:
        return self._rows

    @property
    def provenance(self) -> ExactStateBatchProvenance:
        return self._provenance


class VerifiedExactShardSet:
    """Composable aggregate of bounded batches accepted by the canonical writer.

    Persisted batch receipts are resumability claims, not proof.  A future
    cross-process assembler must production-replay each persisted job before it
    can recreate the in-process batch tokens consumed here.
    """

    __slots__ = ("_batches", "_factory_token", "_mint_binding", "_provenance")
    _batches: tuple[VerifiedExactStateBatch, ...]
    _factory_token: object
    _mint_binding: str
    _provenance: ExactStateUniverseProvenance

    def __init__(
        self,
        *,
        batches: tuple[VerifiedExactStateBatch, ...],
        provenance: ExactStateUniverseProvenance,
        _factory_token: object,
    ) -> None:
        if _factory_token is not _EXACT_STATE_SHARD_SET_FACTORY_TOKEN:
            raise ExactStateBatchError(
                "verified exact shard sets must be created by the production assembler"
            )
        object.__setattr__(self, "_batches", batches)
        object.__setattr__(self, "_provenance", provenance)
        object.__setattr__(self, "_factory_token", _factory_token)
        object.__setattr__(
            self,
            "_mint_binding",
            _factory_private_binding("exact-state-shard-set", provenance),
        )

    def __setattr__(self, name: str, value: object) -> None:
        del name, value
        raise AttributeError("VerifiedExactShardSet is immutable")

    @property
    def batches(self) -> tuple[VerifiedExactStateBatch, ...]:
        return self._batches

    @property
    def provenance(self) -> ExactStateUniverseProvenance:
        return self._provenance

    def iter_rows(self) -> Iterator[CenturyStateRecord]:
        for batch in self._batches:
            yield from batch.rows


def validate_verified_exact_state_batch(
    batch: VerifiedExactStateBatch,
) -> ExactStateBatchProvenance:
    """Recheck the private factory token and every row/provenance binding."""

    if not isinstance(batch, VerifiedExactStateBatch) or (
        batch._factory_token is not _EXACT_STATE_BATCH_FACTORY_TOKEN
    ):
        raise ExactStateBatchError("exact-state batch lacks the production factory token")
    rows = batch.rows
    provenance = batch.provenance
    if not hmac.compare_digest(
        batch._mint_binding,
        _factory_private_binding("bounded-exact-state-batch", provenance),
    ):
        raise ExactStateBatchError("exact-state batch factory-private binding changed")
    if not rows or len(rows) != provenance.interval_count:
        raise ExactStateBatchError("exact-state batch row count changed")
    if rows[0].utc_start != provenance.utc_start or (
        rows[-1].utc_end != provenance.utc_end_exclusive
    ):
        raise ExactStateBatchError("exact-state batch range changed")
    logical_hash = canonical_rows_sha256(rows)
    if logical_hash != provenance.canonical_rows_sha256 or (
        logical_hash != provenance.logical_universe_sha256
    ):
        raise ExactStateBatchError("exact-state batch canonical row hash changed")
    if sum(len(row.boundary_events) for row in rows) != provenance.boundary_event_count:
        raise ExactStateBatchError("exact-state batch boundary-event count changed")
    first = rows[0]
    row_identity_fields = (
        "feature_vector_schema_version",
        "semantic_feature_registry_sha256",
        "feature_registry_sha256",
        "astronomy_engine_version",
        "ephemeris_file_set_sha256",
        "node_convention",
        "mandala_mapping_version",
        "mandala_mapping_sha256",
        "bodygraph_mapping_sha256",
    )
    for row in rows[1:]:
        if any(getattr(row, field) != getattr(first, field) for field in row_identity_fields):
            raise ExactStateBatchError(
                "exact-state batch rows do not share frozen production identities"
            )
    row_derived_bindings = {
        "feature-vector schema": (
            provenance.feature_vector_schema_version,
            first.feature_vector_schema_version,
        ),
        "semantic feature registry": (
            provenance.semantic_feature_registry_sha256,
            first.semantic_feature_registry_sha256,
        ),
        "physical feature registry": (
            provenance.feature_registry_sha256,
            first.feature_registry_sha256,
        ),
        "chart engine": (
            provenance.chart_engine_version,
            first.astronomy_engine_version,
        ),
        "ephemeris file set": (
            provenance.ephemeris_file_set_sha256,
            first.ephemeris_file_set_sha256,
        ),
        "node convention": (provenance.node_convention, first.node_convention),
        "Mandala version": (
            provenance.mandala_mapping_version,
            first.mandala_mapping_version,
        ),
        "Mandala mapping": (
            provenance.mandala_mapping_sha256,
            first.mandala_mapping_sha256,
        ),
        "Bodygraph mapping": (
            provenance.bodygraph_mapping_sha256,
            first.bodygraph_mapping_sha256,
        ),
    }
    for label, (actual, derived) in row_derived_bindings.items():
        if actual != derived:
            raise ExactStateBatchError(
                f"exact-state batch {label} differs from immutable rows"
            )
    for previous, current in zip(rows, rows[1:], strict=False):
        if previous.utc_end != current.utc_start:
            raise ExactStateBatchError("exact-state batch contains a gap or overlap")
        if discrete_chart_identity_sha256(previous) == discrete_chart_identity_sha256(
            current
        ):
            raise ExactStateBatchError("exact-state batch is not maximal")
    if provenance.boundary_policy_version != BOUNDARY_POLICY_VERSION:
        raise ExactStateBatchError("exact-state batch boundary policy changed")
    return provenance


def _sharded_rows_sha256(batches: tuple[VerifiedExactStateBatch, ...]) -> str:
    digest = hashlib.sha256()
    for batch in batches:
        for row in batch.rows:
            digest.update(canonical_json_bytes(row.model_dump(mode="json")))
            digest.update(b"\n")
    return digest.hexdigest()


def _source_batch_hashes(
    provenances: tuple[ExactStateBatchProvenance, ...],
) -> tuple[str, ...]:
    return tuple(
        sha256_json(provenance.model_dump(mode="json")) for provenance in provenances
    )


def _assembly_plan_sha256(
    provenances: tuple[ExactStateBatchProvenance, ...],
    source_hashes: tuple[str, ...],
) -> str:
    return sha256_json(
        {
            "schema_version": "exact-state-assembly-plan-v1",
            "batches": [
                {
                    "provenance_sha256": receipt_hash,
                    "utc_end_exclusive": provenance.utc_end_exclusive,
                    "utc_start": provenance.utc_start,
                }
                for provenance, receipt_hash in zip(
                    provenances, source_hashes, strict=True
                )
            ],
        }
    )


def _no_merge_reconciliation_report_sha256(batch_count: int) -> str:
    return sha256_json(
        {
            "schema_version": "exact-state-reconciliation-report-v1",
            "artificial_cut_count": max(0, batch_count - 1),
            "merged_artificial_cut_count": 0,
            "status": "pass-no-merge-required",
        }
    )


def assemble_verified_exact_shard_set(
    batches: tuple[VerifiedExactStateBatch, ...],
) -> VerifiedExactShardSet:
    """Mint aggregate provenance from ordered in-process verified build jobs.

    An artificial job cut through one stable state requires a full computation
    at the merged representative and a new Design timestamp.  This Phase-1
    assembler fails closed on that condition; the replay/reconciliation factory
    must resolve it before passing batches here.
    """

    if not batches:
        raise ExactStateBatchError("exact shard-set assembly requires a batch")
    provenances = tuple(validate_verified_exact_state_batch(batch) for batch in batches)
    first = provenances[0]
    uniform_fields = (
        "boundary_policy_version",
        "feature_vector_schema_version",
        "semantic_feature_registry_sha256",
        "feature_registry_sha256",
        "chart_engine_version",
        "ephemeris_file_set_sha256",
        "node_convention",
        "mandala_mapping_version",
        "mandala_mapping_sha256",
        "bodygraph_mapping_sha256",
        "design_root_time_tolerance_seconds",
        "design_root_arc_tolerance_degrees",
    )
    for candidate_provenance in provenances[1:]:
        if any(
            getattr(candidate_provenance, field) != getattr(first, field)
            for field in uniform_fields
        ):
            raise ExactStateBatchError(
                "exact build batches do not share frozen production identities"
            )
    for previous, current in zip(batches, batches[1:], strict=False):
        if previous.provenance.utc_end_exclusive != current.provenance.utc_start:
            raise ExactStateBatchError("exact build batches contain a gap or overlap")
        if discrete_chart_identity_sha256(
            previous.rows[-1]
        ) == discrete_chart_identity_sha256(current.rows[0]):
            raise ExactStateBatchError(
                "artificial batch cut splits one stable state; production replay must "
                "recompute the merged representative and Design timestamp"
            )

    source_hashes = _source_batch_hashes(provenances)
    assembly_plan_sha256 = _assembly_plan_sha256(provenances, source_hashes)
    reconciliation_report_sha256 = _no_merge_reconciliation_report_sha256(
        len(batches)
    )
    logical_hash = _sharded_rows_sha256(batches)
    aggregate_provenance = ExactStateUniverseProvenance(
        verification_status="pass",
        assembly_plan_sha256=assembly_plan_sha256,
        ordered_source_batch_provenance_sha256s=source_hashes,
        reconciliation_report_sha256=reconciliation_report_sha256,
        utc_start=first.utc_start,
        utc_end_exclusive=provenances[-1].utc_end_exclusive,
        batch_count=len(batches),
        interval_count=sum(item.interval_count for item in provenances),
        boundary_event_count=sum(item.boundary_event_count for item in provenances),
        boundary_policy_version=first.boundary_policy_version,
        canonical_rows_sha256=logical_hash,
        logical_universe_sha256=logical_hash,
        feature_vector_schema_version=first.feature_vector_schema_version,
        semantic_feature_registry_sha256=first.semantic_feature_registry_sha256,
        feature_registry_sha256=first.feature_registry_sha256,
        chart_engine_version=first.chart_engine_version,
        ephemeris_file_set_sha256=first.ephemeris_file_set_sha256,
        node_convention=first.node_convention,
        mandala_mapping_version=first.mandala_mapping_version,
        mandala_mapping_sha256=first.mandala_mapping_sha256,
        bodygraph_mapping_sha256=first.bodygraph_mapping_sha256,
        design_root_time_tolerance_seconds=(
            first.design_root_time_tolerance_seconds
        ),
        design_root_arc_tolerance_degrees=(
            first.design_root_arc_tolerance_degrees
        ),
    )
    shard_set = VerifiedExactShardSet(
        batches=batches,
        provenance=aggregate_provenance,
        _factory_token=_EXACT_STATE_SHARD_SET_FACTORY_TOKEN,
    )
    validate_verified_exact_shard_set(shard_set)
    return shard_set


def validate_verified_exact_shard_set(
    shard_set: VerifiedExactShardSet,
) -> ExactStateUniverseProvenance:
    """Recheck aggregate token, source batches, counts, ranges, and logical hash."""

    if not isinstance(shard_set, VerifiedExactShardSet) or (
        shard_set._factory_token is not _EXACT_STATE_SHARD_SET_FACTORY_TOKEN
    ):
        raise ExactStateBatchError("exact shard set lacks the production factory token")
    batches = shard_set.batches
    if not batches:
        raise ExactStateBatchError("exact shard set contains no batches")
    provenances = tuple(validate_verified_exact_state_batch(batch) for batch in batches)
    provenance = shard_set.provenance
    if not hmac.compare_digest(
        shard_set._mint_binding,
        _factory_private_binding("exact-state-shard-set", provenance),
    ):
        raise ExactStateBatchError("exact shard-set factory-private binding changed")
    if provenance.batch_count != len(batches):
        raise ExactStateBatchError("exact shard-set batch count changed")
    for previous, current in zip(batches, batches[1:], strict=False):
        if previous.provenance.utc_end_exclusive != current.provenance.utc_start:
            raise ExactStateBatchError("exact shard-set sources contain a gap or overlap")
        if discrete_chart_identity_sha256(
            previous.rows[-1]
        ) == discrete_chart_identity_sha256(current.rows[0]):
            raise ExactStateBatchError(
                "exact shard-set sources are not maximal across a batch boundary"
            )
    first = provenances[0]
    uniform_bindings = {
        "boundary policy": (
            provenance.boundary_policy_version,
            first.boundary_policy_version,
        ),
        "feature-vector schema": (
            provenance.feature_vector_schema_version,
            first.feature_vector_schema_version,
        ),
        "semantic feature registry": (
            provenance.semantic_feature_registry_sha256,
            first.semantic_feature_registry_sha256,
        ),
        "physical feature registry": (
            provenance.feature_registry_sha256,
            first.feature_registry_sha256,
        ),
        "chart engine": (provenance.chart_engine_version, first.chart_engine_version),
        "ephemeris file set": (
            provenance.ephemeris_file_set_sha256,
            first.ephemeris_file_set_sha256,
        ),
        "node convention": (provenance.node_convention, first.node_convention),
        "Mandala version": (
            provenance.mandala_mapping_version,
            first.mandala_mapping_version,
        ),
        "Mandala mapping": (
            provenance.mandala_mapping_sha256,
            first.mandala_mapping_sha256,
        ),
        "Bodygraph mapping": (
            provenance.bodygraph_mapping_sha256,
            first.bodygraph_mapping_sha256,
        ),
        "Design-root time tolerance": (
            provenance.design_root_time_tolerance_seconds,
            first.design_root_time_tolerance_seconds,
        ),
        "Design-root arc tolerance": (
            provenance.design_root_arc_tolerance_degrees,
            first.design_root_arc_tolerance_degrees,
        ),
    }
    for label, (actual, source) in uniform_bindings.items():
        if actual != source:
            raise ExactStateBatchError(
                f"exact shard-set {label} differs from source batches"
            )
    for source_provenance in provenances[1:]:
        if any(
            getattr(source_provenance, field) != getattr(first, field)
            for field in (
                "boundary_policy_version",
                "feature_vector_schema_version",
                "semantic_feature_registry_sha256",
                "feature_registry_sha256",
                "chart_engine_version",
                "ephemeris_file_set_sha256",
                "node_convention",
                "mandala_mapping_version",
                "mandala_mapping_sha256",
                "bodygraph_mapping_sha256",
                "design_root_time_tolerance_seconds",
                "design_root_arc_tolerance_degrees",
            )
        ):
            raise ExactStateBatchError(
                "exact shard-set sources do not share frozen production identities"
            )
    source_hashes = _source_batch_hashes(provenances)
    if provenance.ordered_source_batch_provenance_sha256s != source_hashes:
        raise ExactStateBatchError("exact shard-set source batch receipts changed")
    if provenance.assembly_plan_sha256 != _assembly_plan_sha256(
        provenances, source_hashes
    ):
        raise ExactStateBatchError("exact shard-set assembly plan changed")
    if provenance.reconciliation_report_sha256 != (
        _no_merge_reconciliation_report_sha256(len(batches))
    ):
        raise ExactStateBatchError("exact shard-set reconciliation report changed")
    if provenance.interval_count != sum(item.interval_count for item in provenances):
        raise ExactStateBatchError("exact shard-set interval count changed")
    if provenance.boundary_event_count != sum(
        item.boundary_event_count for item in provenances
    ):
        raise ExactStateBatchError("exact shard-set boundary-event count changed")
    if provenance.utc_start != provenances[0].utc_start or (
        provenance.utc_end_exclusive != provenances[-1].utc_end_exclusive
    ):
        raise ExactStateBatchError("exact shard-set range changed")
    logical_hash = _sharded_rows_sha256(batches)
    if logical_hash != provenance.canonical_rows_sha256 or (
        logical_hash != provenance.logical_universe_sha256
    ):
        raise ExactStateBatchError("exact shard-set canonical row hash changed")
    return provenance


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


def _stable_interval_partition_sha256(
    intervals: tuple[StableInterval, ...],
) -> str:
    return sha256_json(
        [
            {
                "boundary_events": [
                    canonical_boundary_event_string(event)
                    for event in interval.boundary_events
                ],
                "end_utc": interval.end_utc,
                "feature_sha256": interval.feature_sha256,
                "representative_utc": interval.representative_utc,
                "start_utc": interval.start_utc,
            }
            for interval in intervals
        ]
    )


def build_verified_exact_state_batch(
    provider: SwissEphemerisProvider,
    start_utc: datetime,
    end_utc: datetime,
    *,
    root_tolerance_seconds: float = 0.01,
    required_registry: RequiredFeatureRegistry = CACHEABLE_M0_M2_REGISTRY,
) -> VerifiedExactStateBatch:
    """Build and certify a bounded SWIEPH exact-state batch.

    This is the only production factory for rows accepted by the canonical cache
    writer.  It owns boundary enumeration, representative computations, and the
    bounded serialization session; callers cannot submit preselected time slices.
    """

    if required_registry.sha256() != CACHEABLE_M0_M2_REGISTRY.sha256():
        raise ExactStateBatchError(
            "canonical exact-state batches require the frozen cacheable M0-M2 registry"
        )

    representative_computations: dict[datetime, ChartComputation] = {}
    try:
        intervals = build_production_chart_state_intervals(
            provider,
            start_utc,
            end_utc,
            root_tolerance_seconds=root_tolerance_seconds,
            representative_computations=representative_computations,
        )
        audit_interval_partition(intervals, start_utc, end_utc)
    except (TypeError, ValueError, RuntimeError) as exc:
        raise ExactStateBatchError(
            f"production exact-boundary enumeration failed: {exc}"
        ) from exc

    cacheable_rows = []
    try:
        with cacheable_serialization_session(provider) as session:
            for interval in intervals:
                computation = representative_computations.get(
                    interval.representative_utc
                )
                if computation is None:
                    raise ExactStateBatchError(
                        "boundary engine did not retain the representative computation"
                    )
                computed_stable_hash = canonical_sha256(computation.stable_features)
                if interval.features != computation.stable_features:
                    raise ExactStateBatchError(
                        "interval features differ from its representative full computation"
                    )
                if interval.feature_sha256 != computed_stable_hash or (
                    computation.chart_features_sha256 != computed_stable_hash
                ):
                    raise ExactStateBatchError(
                        "interval stable-feature hash differs from its representative "
                        "full computation"
                    )
                boundary_events = tuple(
                    sorted(
                        canonical_boundary_event_string(event)
                        for event in interval.boundary_events
                    )
                )
                cacheable = session.serialize_cacheable_chart_state(
                    computation,
                    provider=provider,
                    utc_start=interval.start_utc,
                    utc_end=interval.end_utc,
                    boundary_events=boundary_events,
                )
                cacheable_rows.append(
                    cacheable_chart_state_to_century_record(
                        cacheable,
                        required_registry=required_registry,
                    )
                )
    except ExactStateBatchError:
        raise
    except (TypeError, ValueError, RuntimeError) as exc:
        raise ExactStateBatchError(
            f"production exact-state serialization failed: {exc}"
        ) from exc

    rows = tuple(cacheable_rows)
    if not rows:
        raise ExactStateBatchError("exact-state serialization produced no rows")
    if len(rows) != len(intervals):
        raise ExactStateBatchError("exact-state serialization changed the interval count")
    for previous, current in zip(rows, rows[1:], strict=False):
        if previous.utc_end != current.utc_start:
            raise ExactStateBatchError("serialized exact-state rows contain a gap or overlap")
        if discrete_chart_identity_sha256(previous) == discrete_chart_identity_sha256(
            current
        ):
            raise ExactStateBatchError(
                "serialized exact-state rows are not a maximal partition"
            )

    first_computation = representative_computations.get(
        intervals[0].representative_utc
    )
    if first_computation is None:  # pragma: no cover - checked during serialization
        raise ExactStateBatchError("first representative computation is missing")
    first_metadata = first_computation.metadata
    for interval in intervals:
        computation = representative_computations.get(interval.representative_utc)
        if computation is None:  # pragma: no cover - checked during serialization
            raise ExactStateBatchError("representative computation is missing")
        if computation.metadata != first_metadata:
            raise ExactStateBatchError(
                "representative computations do not share identical frozen "
                "engine/mapping/tolerance metadata"
            )

    first = rows[0]
    logical_hash = canonical_rows_sha256(rows)
    provenance = ExactStateBatchProvenance(
        verification_status="pass",
        utc_start=rows[0].utc_start,
        utc_end_exclusive=rows[-1].utc_end,
        interval_count=len(rows),
        boundary_event_count=sum(len(row.boundary_events) for row in rows),
        boundary_policy_version=BOUNDARY_POLICY_VERSION,
        stable_interval_partition_sha256=_stable_interval_partition_sha256(intervals),
        canonical_rows_sha256=logical_hash,
        logical_universe_sha256=logical_hash,
        feature_vector_schema_version=first.feature_vector_schema_version,
        semantic_feature_registry_sha256=first.semantic_feature_registry_sha256,
        feature_registry_sha256=first.feature_registry_sha256,
        chart_engine_version=first.astronomy_engine_version,
        ephemeris_file_set_sha256=first.ephemeris_file_set_sha256,
        node_convention=first.node_convention,
        mandala_mapping_version=first.mandala_mapping_version,
        mandala_mapping_sha256=first.mandala_mapping_sha256,
        bodygraph_mapping_sha256=first.bodygraph_mapping_sha256,
        design_root_time_tolerance_seconds=(
            first_metadata.design_time_tolerance_seconds
        ),
        design_root_arc_tolerance_degrees=(
            first_metadata.design_arc_tolerance_degrees
        ),
    )
    batch = VerifiedExactStateBatch(
        rows=rows,
        provenance=provenance,
        _factory_token=_EXACT_STATE_BATCH_FACTORY_TOKEN,
    )
    validate_verified_exact_state_batch(batch)
    return batch


def _mint_reconciled_exact_state_batch(
    rows: tuple[CenturyStateRecord, ...],
    *,
    source_batch: VerifiedExactStateBatch,
    stable_interval_partition_sha256: str,
    _reconciliation_factory_token: object,
) -> VerifiedExactStateBatch:
    """Mint a bounded batch after overlap reconciliation has rederived its rows.

    This is intentionally private to the century-cache package.  The Phase-2
    reconciler must first validate factory-minted source batches and recompute
    every clipped or merged representative through the strict Swiss provider.
    Arbitrary callers cannot obtain the private production-factory token.
    """

    if _reconciliation_factory_token is not _EXACT_STATE_RECONCILIATION_MINT_TOKEN:
        raise ExactStateBatchError("reconciled mint lacks the factory capability")
    source_provenance = validate_verified_exact_state_batch(source_batch)
    if not rows:
        raise ExactStateBatchError("reconciled exact-state batch must not be empty")
    if len(stable_interval_partition_sha256) != 64:
        raise ExactStateBatchError("reconciled interval partition hash is invalid")
    for previous, current in zip(rows, rows[1:], strict=False):
        if previous.utc_end != current.utc_start:
            raise ExactStateBatchError("reconciled exact-state rows contain a gap or overlap")
        if discrete_chart_identity_sha256(previous) == discrete_chart_identity_sha256(
            current
        ):
            raise ExactStateBatchError("reconciled exact-state rows are not maximal")

    first = rows[0]
    logical_hash = canonical_rows_sha256(rows)
    provenance = ExactStateBatchProvenance(
        verification_status="pass",
        utc_start=first.utc_start,
        utc_end_exclusive=rows[-1].utc_end,
        interval_count=len(rows),
        boundary_event_count=sum(len(row.boundary_events) for row in rows),
        boundary_policy_version=source_provenance.boundary_policy_version,
        stable_interval_partition_sha256=stable_interval_partition_sha256,
        canonical_rows_sha256=logical_hash,
        logical_universe_sha256=logical_hash,
        feature_vector_schema_version=first.feature_vector_schema_version,
        semantic_feature_registry_sha256=first.semantic_feature_registry_sha256,
        feature_registry_sha256=first.feature_registry_sha256,
        chart_engine_version=first.astronomy_engine_version,
        ephemeris_file_set_sha256=first.ephemeris_file_set_sha256,
        node_convention=first.node_convention,
        mandala_mapping_version=first.mandala_mapping_version,
        mandala_mapping_sha256=first.mandala_mapping_sha256,
        bodygraph_mapping_sha256=first.bodygraph_mapping_sha256,
        design_root_time_tolerance_seconds=(
            source_provenance.design_root_time_tolerance_seconds
        ),
        design_root_arc_tolerance_degrees=(
            source_provenance.design_root_arc_tolerance_degrees
        ),
    )
    batch = VerifiedExactStateBatch(
        rows=rows,
        provenance=provenance,
        _factory_token=_EXACT_STATE_BATCH_FACTORY_TOKEN,
    )
    validate_verified_exact_state_batch(batch)
    return batch
