"""Zstandard Parquet encoding for registry-defined century-cache rows."""

from __future__ import annotations

import json
import os
import tempfile
import uuid
from collections.abc import Iterator
from dataclasses import dataclass
from itertools import zip_longest
from pathlib import Path
from typing import Any

from hdmatch.experiments.canonical import canonical_json_bytes, sha256_file

from .models import (
    PARQUET_SHARD_HARD_CAP_BYTES,
    PARQUET_SHARD_TARGET_BYTES,
    CenturyCacheShard,
    CenturyStateRecord,
    FeatureColumnSpec,
    FeatureStorageType,
    FeatureValue,
    canonical_rows_sha256,
    parquet_schema_sha256,
)
from .streaming import canonical_row_json_line


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
        pa.field("semantic_feature_registry_sha256", pa.string(), nullable=False),
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
        "semantic_feature_registry_sha256": row.semantic_feature_registry_sha256,
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


def iter_parquet_shard_rows(
    path: str | Path,
    registry: tuple[FeatureColumnSpec, ...],
    *,
    batch_size: int = 1024,
) -> Iterator[CenturyStateRecord]:
    """Decode a shard in bounded Arrow batches after physical validation."""

    if batch_size <= 0:
        raise CenturyCacheParquetError("Parquet streaming batch size must be positive")
    _, pq = _pyarrow_modules()
    source = Path(path)
    try:
        parquet_file = pq.ParquetFile(source)
    except (OSError, ValueError) as exc:
        raise CenturyCacheParquetError(f"cannot read Parquet shard: {source.name}") from exc
    expected_schema = expected_arrow_schema(registry)
    if not parquet_file.schema_arrow.equals(expected_schema, check_metadata=True):
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
        for batch in parquet_file.iter_batches(batch_size=batch_size):
            for payload in batch.to_pylist():
                yield _logical_row(payload, registry)
    except (KeyError, OSError, TypeError, ValueError) as exc:
        raise CenturyCacheParquetError(
            f"invalid logical row payload in shard: {source.name}"
        ) from exc


@dataclass(frozen=True, slots=True)
class BoundedShardWriteAudit:
    """Resource-bound evidence from one streaming shard-writing session."""

    shard_count: int
    row_count: int
    maximum_buffered_canonical_bytes: int
    target_bytes: int
    hard_cap_bytes: int


class BoundedParquetShardWriter:
    """Write a row stream into deterministic, hard-capped Parquet shards.

    The current buffer is bounded by canonical logical-row bytes.  A completed
    candidate is measured on disk and recursively split at row boundaries if it
    exceeds the physical hard cap.  No previously emitted shard rows are kept.
    """

    def __init__(
        self,
        directory: str | Path,
        registry: tuple[FeatureColumnSpec, ...],
        *,
        target_bytes: int = PARQUET_SHARD_TARGET_BYTES,
        hard_cap_bytes: int = PARQUET_SHARD_HARD_CAP_BYTES,
    ) -> None:
        if target_bytes <= 0:
            raise CenturyCacheParquetError("Parquet shard target must be positive")
        if hard_cap_bytes < target_bytes:
            raise CenturyCacheParquetError(
                "Parquet shard hard cap must not be smaller than its target"
            )
        self._directory = Path(directory)
        if not self._directory.is_dir():
            raise CenturyCacheParquetError(
                "bounded shard writer requires an existing staging directory"
            )
        self._registry = registry
        self._target_bytes = target_bytes
        self._hard_cap_bytes = hard_cap_bytes
        self._buffer: list[CenturyStateRecord] = []
        self._buffer_bytes = 0
        self._maximum_buffer_bytes = 0
        self._shards: list[CenturyCacheShard] = []
        self._row_count = 0
        self._finished = False

    def append(self, row: CenturyStateRecord) -> None:
        if self._finished:
            raise CenturyCacheParquetError("bounded shard writer is already finished")
        row_bytes = len(canonical_row_json_line(row))
        if self._buffer and self._buffer_bytes + row_bytes > self._target_bytes:
            self._flush(tuple(self._buffer))
            self._buffer.clear()
            self._buffer_bytes = 0
        self._buffer.append(row)
        self._buffer_bytes += row_bytes
        self._maximum_buffer_bytes = max(
            self._maximum_buffer_bytes,
            self._buffer_bytes,
        )
        self._row_count += 1

    def finish(self) -> tuple[tuple[CenturyCacheShard, ...], BoundedShardWriteAudit]:
        if self._finished:
            raise CenturyCacheParquetError("bounded shard writer is already finished")
        self._finished = True
        if self._buffer:
            self._flush(tuple(self._buffer))
            self._buffer.clear()
            self._buffer_bytes = 0
        if not self._shards:
            raise CenturyCacheParquetError("cannot finalize an empty cache shard stream")
        return (
            tuple(self._shards),
            BoundedShardWriteAudit(
                shard_count=len(self._shards),
                row_count=self._row_count,
                maximum_buffered_canonical_bytes=self._maximum_buffer_bytes,
                target_bytes=self._target_bytes,
                hard_cap_bytes=self._hard_cap_bytes,
            ),
        )

    def _flush(self, rows: tuple[CenturyStateRecord, ...]) -> None:
        candidate = self._directory / (
            f".shard-candidate-{len(self._shards):06d}-{uuid.uuid4().hex}.parquet.zst"
        )
        try:
            write_parquet_shard_new(candidate, rows, self._registry)
            byte_count = candidate.stat().st_size
            if byte_count > self._hard_cap_bytes:
                if len(rows) == 1:
                    raise CenturyCacheParquetError(
                        "one logical row exceeds the Parquet shard hard cap"
                    )
                candidate.unlink()
                split = len(rows) // 2
                self._flush(rows[:split])
                self._flush(rows[split:])
                return

            expected = iter(rows)
            observed = iter_parquet_shard_rows(candidate, self._registry)
            sentinel = object()
            for expected_row, observed_row in zip_longest(
                expected,
                observed,
                fillvalue=sentinel,
            ):
                if expected_row != observed_row:
                    raise CenturyCacheParquetError(
                        "Parquet round-trip changed streamed logical rows"
                    )

            filename = f"states-{len(self._shards):06d}.parquet.zst"
            destination = self._directory / filename
            try:
                os.link(candidate, destination)
            except FileExistsError:
                raise FileExistsError(
                    f"century-cache shard already exists: {destination}"
                ) from None
            self._shards.append(
                CenturyCacheShard(
                    filename=filename,
                    sha256=sha256_file(destination),
                    row_count=len(rows),
                    utc_start=rows[0].utc_start,
                    utc_end_exclusive=rows[-1].utc_end,
                    canonical_rows_sha256=canonical_rows_sha256(rows),
                    parquet_schema_sha256=parquet_schema_sha256(self._registry),
                    byte_count=byte_count,
                )
            )
        finally:
            candidate.unlink(missing_ok=True)
