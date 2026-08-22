"""Zstandard Parquet encoding for registry-defined century-cache rows."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from hdmatch.experiments.canonical import canonical_json_bytes

from .models import (
    CenturyStateRecord,
    FeatureColumnSpec,
    FeatureStorageType,
    FeatureValue,
)


class CenturyCacheDependencyError(RuntimeError):
    """The optional cache serialization dependency is unavailable."""


class CenturyCacheParquetError(ValueError):
    """A physical Parquet shard violates the cache storage contract."""


def _pyarrow_modules() -> tuple[Any, Any]:
    try:
        import pyarrow as pa  # type: ignore[import-untyped]
        import pyarrow.parquet as pq  # type: ignore[import-untyped]
    except ModuleNotFoundError as exc:  # pragma: no cover - exercised without cache extra
        raise CenturyCacheDependencyError(
            "century-cache Parquet support requires pyarrow; install hdmatch[cache]"
        ) from exc
    return pa, pq


def _activation_type(pa: Any) -> Any:
    return pa.list_(
        pa.field(
            "element",
            pa.struct(
                [
                    pa.field("body", pa.string(), nullable=False),
                    pa.field("side", pa.string(), nullable=False),
                    pa.field("gate", pa.int8(), nullable=False),
                    pa.field("line", pa.int8(), nullable=False),
                    pa.field("color", pa.int8(), nullable=True),
                    pa.field("tone", pa.int8(), nullable=True),
                    pa.field("base", pa.int8(), nullable=True),
                ]
            ),
        )
    )


def _feature_arrow_type(pa: Any, storage_type: FeatureStorageType) -> Any:
    return {
        FeatureStorageType.BOOLEAN: pa.bool_(),
        FeatureStorageType.INT64: pa.int64(),
        FeatureStorageType.FLOAT64: pa.float64(),
        FeatureStorageType.STRING: pa.string(),
        FeatureStorageType.STRING_LIST: pa.list_(pa.field("element", pa.string())),
        FeatureStorageType.INT64_LIST: pa.list_(pa.field("element", pa.int64())),
        FeatureStorageType.ACTIVATION_LIST: _activation_type(pa),
        FeatureStorageType.JSON: pa.binary(),
    }[storage_type]


def expected_arrow_schema(registry: tuple[FeatureColumnSpec, ...]) -> Any:
    pa, _ = _pyarrow_modules()
    fields = [
        pa.field("schema_version", pa.string(), nullable=False),
        pa.field("state_id", pa.string(), nullable=False),
        pa.field("utc_start", pa.timestamp("us", tz="UTC"), nullable=False),
        pa.field("utc_end", pa.timestamp("us", tz="UTC"), nullable=False),
        pa.field("duration_seconds", pa.float64(), nullable=False),
        pa.field("representative_utc", pa.timestamp("us", tz="UTC"), nullable=False),
        pa.field("design_timestamp", pa.timestamp("us", tz="UTC"), nullable=False),
        pa.field("chart_features_sha256", pa.string(), nullable=False),
        pa.field("feature_vector_schema_version", pa.string(), nullable=False),
        pa.field("feature_registry_sha256", pa.string(), nullable=False),
        pa.field("astronomy_engine_version", pa.string(), nullable=False),
        pa.field("ephemeris_file_set_sha256", pa.string(), nullable=False),
        pa.field("node_convention", pa.string(), nullable=False),
        pa.field("mandala_mapping_version", pa.string(), nullable=False),
        pa.field("mandala_mapping_sha256", pa.string(), nullable=False),
        pa.field("bodygraph_mapping_sha256", pa.string(), nullable=False),
        pa.field(
            "boundary_events",
            pa.list_(pa.field("element", pa.string())),
            nullable=False,
        ),
    ]
    fields.extend(
        pa.field(
            item.parquet_column_name,
            _feature_arrow_type(pa, item.storage_type),
            nullable=item.nullable,
        )
        for item in registry
    )
    return pa.schema(fields)


def _validate_activation_list(feature_id: str, value: object) -> None:
    if not isinstance(value, list):
        raise CenturyCacheParquetError(f"feature {feature_id} requires an activation list")
    expected_keys = {"body", "side", "gate", "line", "color", "tone", "base"}
    for activation in value:
        if not isinstance(activation, dict) or set(activation) != expected_keys:
            raise CenturyCacheParquetError(
                f"feature {feature_id} contains an invalid activation record"
            )
        if not isinstance(activation["body"], str) or not activation["body"]:
            raise CenturyCacheParquetError(f"feature {feature_id} has an invalid body")
        if activation["side"] not in {"personality", "design"}:
            raise CenturyCacheParquetError(f"feature {feature_id} has an invalid side")
        gate = activation["gate"]
        line = activation["line"]
        if isinstance(gate, bool) or not isinstance(gate, int) or not 1 <= gate <= 64:
            raise CenturyCacheParquetError(f"feature {feature_id} has an invalid Gate")
        if isinstance(line, bool) or not isinstance(line, int) or not 1 <= line <= 6:
            raise CenturyCacheParquetError(f"feature {feature_id} has an invalid Line")
        for name, upper in (("color", 6), ("tone", 6), ("base", 5)):
            component = activation[name]
            if component is not None and (
                isinstance(component, bool)
                or not isinstance(component, int)
                or not 1 <= component <= upper
            ):
                raise CenturyCacheParquetError(
                    f"feature {feature_id} has an invalid {name}"
                )


def _validate_feature_value(spec: FeatureColumnSpec, value: object) -> None:
    if value is None:
        if not spec.nullable:
            raise CenturyCacheParquetError(
                f"feature {spec.feature_id} is explicitly unknown but is not nullable"
            )
        return
    valid = False
    if spec.storage_type is FeatureStorageType.BOOLEAN:
        valid = isinstance(value, bool)
    elif spec.storage_type is FeatureStorageType.INT64:
        valid = isinstance(value, int) and not isinstance(value, bool)
    elif spec.storage_type is FeatureStorageType.FLOAT64:
        valid = isinstance(value, float)
    elif spec.storage_type is FeatureStorageType.STRING:
        valid = isinstance(value, str)
    elif spec.storage_type is FeatureStorageType.STRING_LIST:
        valid = isinstance(value, list) and all(isinstance(item, str) for item in value)
    elif spec.storage_type is FeatureStorageType.INT64_LIST:
        valid = isinstance(value, list) and all(
            isinstance(item, int) and not isinstance(item, bool) for item in value
        )
    elif spec.storage_type is FeatureStorageType.ACTIVATION_LIST:
        _validate_activation_list(spec.feature_id, value)
        valid = True
    elif spec.storage_type is FeatureStorageType.JSON:
        canonical_json_bytes(value)
        valid = True
    if not valid:
        raise CenturyCacheParquetError(
            f"feature {spec.feature_id} does not match storage type {spec.storage_type.value}"
        )


def validate_row_features(
    row: CenturyStateRecord, registry: tuple[FeatureColumnSpec, ...]
) -> None:
    values = row.feature_mapping()
    expected_ids = tuple(item.feature_id for item in registry)
    actual_ids = tuple(values)
    if actual_ids != expected_ids:
        missing = sorted(set(expected_ids) - set(actual_ids))
        extra = sorted(set(actual_ids) - set(expected_ids))
        raise CenturyCacheParquetError(
            f"row {row.state_id} feature registry mismatch; missing={missing}, extra={extra}"
        )
    for spec in registry:
        _validate_feature_value(spec, values[spec.feature_id])


def _physical_row(
    row: CenturyStateRecord, registry: tuple[FeatureColumnSpec, ...]
) -> dict[str, object]:
    validate_row_features(row, registry)
    payload: dict[str, object] = {
        "schema_version": row.schema_version,
        "state_id": row.state_id,
        "utc_start": row.utc_start,
        "utc_end": row.utc_end,
        "duration_seconds": row.duration_seconds,
        "representative_utc": row.representative_utc,
        "design_timestamp": row.design_timestamp,
        "chart_features_sha256": row.chart_features_sha256,
        "feature_vector_schema_version": row.feature_vector_schema_version,
        "feature_registry_sha256": row.feature_registry_sha256,
        "astronomy_engine_version": row.astronomy_engine_version,
        "ephemeris_file_set_sha256": row.ephemeris_file_set_sha256,
        "node_convention": row.node_convention,
        "mandala_mapping_version": row.mandala_mapping_version,
        "mandala_mapping_sha256": row.mandala_mapping_sha256,
        "bodygraph_mapping_sha256": row.bodygraph_mapping_sha256,
        "boundary_events": list(row.boundary_events),
    }
    values = row.feature_mapping()
    for spec in registry:
        value = values[spec.feature_id]
        payload[spec.parquet_column_name] = (
            canonical_json_bytes(value)
            if spec.storage_type is FeatureStorageType.JSON and value is not None
            else value
        )
    return payload


def _logical_row(
    payload: dict[str, object], registry: tuple[FeatureColumnSpec, ...]
) -> CenturyStateRecord:
    boundary_events = payload.get("boundary_events")
    if not isinstance(boundary_events, list) or not all(
        isinstance(item, str) for item in boundary_events
    ):
        raise CenturyCacheParquetError("boundary_events payload is not a string list")
    payload["boundary_events"] = tuple(boundary_events)
    feature_values: list[FeatureValue] = []
    for spec in registry:
        value = payload.pop(spec.parquet_column_name)
        if spec.storage_type is FeatureStorageType.JSON and value is not None:
            if not isinstance(value, bytes):
                raise CenturyCacheParquetError(
                    f"feature {spec.feature_id} JSON payload is not binary"
                )
            value = json.loads(value)
        feature_values.append(
            FeatureValue.model_validate(
                {"feature_id": spec.feature_id, "value": value}, strict=True
            )
        )
    return CenturyStateRecord.model_validate(
        {**payload, "feature_values": tuple(feature_values)}, strict=True
    )


def write_parquet_shard_new(
    path: str | Path,
    rows: tuple[CenturyStateRecord, ...],
    registry: tuple[FeatureColumnSpec, ...],
) -> Path:
    """Atomically create one internally Zstandard-compressed Parquet shard."""

    if not rows:
        raise CenturyCacheParquetError("cannot write an empty century-cache shard")
    pa, pq = _pyarrow_modules()
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise FileExistsError(f"century-cache shard already exists: {destination}")
    table = pa.Table.from_pylist(
        [_physical_row(row, registry) for row in rows],
        schema=expected_arrow_schema(registry),
    )
    descriptor, temporary_name = tempfile.mkstemp(
        dir=destination.parent, prefix=f".{destination.name}.", suffix=".tmp"
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        pq.write_table(
            table,
            temporary,
            compression="zstd",
            version="2.6",
            data_page_version="2.0",
            use_dictionary=False,
            write_statistics=True,
        )
        with temporary.open("rb") as handle:
            os.fsync(handle.fileno())
        try:
            os.link(temporary, destination)
        except FileExistsError:
            raise FileExistsError(
                f"century-cache shard already exists: {destination}"
            ) from None
    finally:
        temporary.unlink(missing_ok=True)
    return destination


def read_parquet_shard(
    path: str | Path,
    registry: tuple[FeatureColumnSpec, ...],
) -> tuple[CenturyStateRecord, ...]:
    """Read one shard and reject schema or compression substitutions."""

    _, pq = _pyarrow_modules()
    source = Path(path)
    try:
        parquet_file = pq.ParquetFile(source)
        table = parquet_file.read()
    except (OSError, ValueError) as exc:
        raise CenturyCacheParquetError(f"cannot read Parquet shard: {source.name}") from exc
    expected_schema = expected_arrow_schema(registry)
    if not table.schema.equals(expected_schema, check_metadata=True):
        raise CenturyCacheParquetError(f"Parquet schema mismatch: {source.name}")
    metadata = parquet_file.metadata
    for group_index in range(metadata.num_row_groups):
        row_group = metadata.row_group(group_index)
        for column_index in range(row_group.num_columns):
            if row_group.column(column_index).compression != "ZSTD":
                raise CenturyCacheParquetError(
                    f"Parquet column is not Zstandard-compressed: {source.name}"
                )
    try:
        return tuple(_logical_row(row, registry) for row in table.to_pylist())
    except (KeyError, TypeError, ValueError) as exc:
        raise CenturyCacheParquetError(
            f"invalid logical row payload in shard: {source.name}"
        ) from exc
