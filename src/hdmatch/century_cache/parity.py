"""Independent golden parity generation for a cache build plan.

Parity is evaluated before any cache rows are generated.  The report binds the
declared cache horizon to the frozen Phase-0 reference source, but does not
claim that the reference contains every boundary in that horizon.
"""

from __future__ import annotations

import json
import math
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from hdmatch.chart.ephemeris import (
    DEFAULT_ACTIVATION_BODIES,
    EphemerisMode,
    SwissEphemerisProvider,
)
from hdmatch.chart.rave_mandala import longitude_to_gate_line
from hdmatch.experiments.canonical import sha256_file
from hdmatch.provenance.swisseph_files import VerifiedEphemerisProvenance

from .evidence import CenturyCacheParityReport


class CenturyCacheParityGenerationError(ValueError):
    """The frozen reference or current Swiss calculation failed parity."""


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class _GoldenSource(_FrozenModel):
    repository: str = Field(min_length=1)
    commit: str = Field(pattern=r"^[a-f0-9]{40}$")
    pyswisseph_package_version: str = Field(min_length=1)
    swiss_library_version: str = Field(min_length=1)
    files: dict[str, str]


class _GoldenUniverse(_FrozenModel):
    start_inclusive: datetime
    end_exclusive: datetime

    @field_validator("start_inclusive", "end_exclusive")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("golden universe timestamps must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def require_positive_range(self) -> _GoldenUniverse:
        if self.end_exclusive <= self.start_inclusive:
            raise ValueError("golden universe range must be positive")
        return self


class _GoldenPosition(_FrozenModel):
    longitude: float
    gate: int = Field(ge=1, le=64)
    line: int = Field(ge=1, le=6)

    @field_validator("longitude")
    @classmethod
    def require_longitude(cls, value: float) -> float:
        if not math.isfinite(value) or not 0.0 <= value < 360.0:
            raise ValueError("golden longitude must be finite and in [0, 360)")
        return value


class _GoldenSample(_FrozenModel):
    utc: datetime
    positions: dict[str, _GoldenPosition]

    @field_validator("utc")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("golden sample timestamp must be timezone-aware")
        return value.astimezone(UTC)


class _GoldenDesignRoot(_FrozenModel):
    birth_utc: datetime
    design_utc: datetime
    target_arc_degrees: float
    time_tolerance_seconds: float
    arc_tolerance_degrees: float

    @field_validator("birth_utc", "design_utc")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("golden Design-root timestamp must be timezone-aware")
        return value.astimezone(UTC)


class _SwissGoldenV1(_FrozenModel):
    schema_version: Literal["swieph-phase0-golden-v1"]
    purpose: str = Field(min_length=1)
    source: _GoldenSource
    universe: _GoldenUniverse
    representative_positions: tuple[_GoldenSample, ...] = Field(min_length=1)
    joel_exact_design_root: _GoldenDesignRoot


def _require_utc(value: datetime, *, label: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise CenturyCacheParityGenerationError(f"{label} must be timezone-aware")
    return value.astimezone(UTC)


def _load_golden(path: Path) -> _SwissGoldenV1:
    if path.is_symlink():
        raise CenturyCacheParityGenerationError(
            "parity reference source must not be a symbolic link"
        )
    try:
        raw = path.read_bytes()
        json.loads(raw)
        return _SwissGoldenV1.model_validate_json(raw, strict=True)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        raise CenturyCacheParityGenerationError(
            "invalid Swiss golden parity reference"
        ) from exc


def _angular_error_degrees(observed: float, expected: float) -> float:
    return abs((observed - expected + 180.0) % 360.0 - 180.0)


def generate_swieph_golden_parity_report(
    provider: SwissEphemerisProvider,
    ephemeris_provenance: VerifiedEphemerisProvenance,
    *,
    golden_reference_path: str | Path,
    reference_source_locator: str,
    engine_validation_sha256: str,
    feature_vector_schema_version: str,
    utc_start: datetime,
    utc_end_exclusive: datetime,
    tolerance_degrees: float = 1e-9,
) -> CenturyCacheParityReport:
    """Recalculate every frozen sample and emit a zero-mismatch parity report."""

    start = _require_utc(utc_start, label="parity UTC start")
    end = _require_utc(utc_end_exclusive, label="parity UTC end")
    if end <= start:
        raise CenturyCacheParityGenerationError("parity range must be positive")
    if not math.isfinite(tolerance_degrees) or tolerance_degrees <= 0.0:
        raise CenturyCacheParityGenerationError(
            "parity tolerance must be positive and finite"
        )

    reference_path = Path(golden_reference_path)
    golden = _load_golden(reference_path)
    if golden.universe.start_inclusive > start or golden.universe.end_exclusive < end:
        raise CenturyCacheParityGenerationError(
            "golden parity reference does not cover the declared cache horizon"
        )

    provider.verify_production_configuration()
    metadata = provider.metadata
    if metadata.requested_ephemeris is not EphemerisMode.SWIEPH:
        raise CenturyCacheParityGenerationError("parity provider does not request SWIEPH")
    source_files = {item.name: item.sha256 for item in ephemeris_provenance.files}
    provider_files = {Path(item.path).name: item.sha256 for item in metadata.files}
    if golden.source.repository != ephemeris_provenance.source_repository or (
        golden.source.commit != ephemeris_provenance.source_commit
    ):
        raise CenturyCacheParityGenerationError(
            "golden source does not match the verified Swiss upstream"
        )
    if golden.source.files != source_files or provider_files != source_files:
        raise CenturyCacheParityGenerationError(
            "golden/provider file hashes do not match verified ephemeris provenance"
        )
    if golden.source.swiss_library_version != metadata.library_version:
        raise CenturyCacheParityGenerationError(
            "golden Swiss library version differs from the production provider"
        )

    expected_bodies = {body.value for body in DEFAULT_ACTIVATION_BODIES}
    comparison_count = 0
    mismatch_count = 0
    max_error = 0.0
    for sample in golden.representative_positions:
        if set(sample.positions) != expected_bodies:
            raise CenturyCacheParityGenerationError(
                "golden sample does not contain the complete activation-body set"
            )
        for body in DEFAULT_ACTIVATION_BODIES:
            calculation = provider.position_with_provenance(body, sample.utc)
            provenance = calculation.provenance
            if provenance.requested_mode is not EphemerisMode.SWIEPH or (
                provenance.returned_mode is not EphemerisMode.SWIEPH
            ):
                raise CenturyCacheParityGenerationError(
                    "golden parity calculation did not return SWIEPH"
                )
            expected = sample.positions[body.value]
            error = _angular_error_degrees(
                calculation.position.longitude,
                expected.longitude,
            )
            max_error = max(max_error, error)
            gate_line = longitude_to_gate_line(calculation.position.longitude)
            if error > tolerance_degrees or (gate_line.gate, gate_line.line) != (
                expected.gate,
                expected.line,
            ):
                mismatch_count += 1
            comparison_count += 1
    provider.verify_production_configuration()
    if mismatch_count:
        raise CenturyCacheParityGenerationError(
            f"Swiss golden parity found {mismatch_count} mismatches"
        )

    return CenturyCacheParityReport(
        schema_version="century-cache-parity-report-v1",
        validation_status="pass",
        engine_validation_sha256=engine_validation_sha256,
        ephemeris_file_set_sha256=(
            ephemeris_provenance.ephemeris_file_set_sha256
        ),
        feature_vector_schema_version=feature_vector_schema_version,
        utc_start=start,
        utc_end_exclusive=end,
        reference_source_locator=reference_source_locator,
        reference_source_sha256=sha256_file(reference_path),
        comparison_count=comparison_count,
        mismatch_count=0,
        tolerance_degrees=tolerance_degrees,
        max_abs_longitude_error_degrees=max_error,
    )
