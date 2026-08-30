"""Pinned engine, timezone, and full-state identity provenance."""

from __future__ import annotations

import math
from dataclasses import asdict
from hashlib import sha256
from pathlib import Path
from typing import Literal
from zoneinfo import TZPATH

from pydantic import Field, model_validator

from hdmatch.chart.bodygraph import bodygraph_constants_sha256
from hdmatch.chart.calculator import CHART_ENGINE_VERSION
from hdmatch.chart.ephemeris import CelestialBody, EphemerisProvider
from hdmatch.chart.rave_mandala import mandala_constants_sha256
from hdmatch.chart.timezone import timezone_database_version
from hdmatch.natal_time.models import SHA256_PATTERN, NatalTimeModel
from hdmatch.util import sha256_file, sha256_json

STATE_IDENTITY_VERSION = "natal-full-state-identity-v1"
ENUMERATOR_VERSION = "natal-civil-day-enumerator-v2"
CANONICALIZER_VERSION = "hdmatch-canonical-json-v1"
BOUNDARY_METHOD = "lipschitz-engine-grid-event-search-plus-independent-verification-v2"
SWISS_JULIAN_DAY_QUANTUM_MICROSECONDS = math.ulp(2_451_544.5) * 86_400_000_000.0


class StateIdentityField(NatalTimeModel):
    path: str = Field(min_length=1)
    value_kind: Literal["discrete", "continuous_diagnostic", "provenance"]
    included: bool
    exclusion_reason: str | None = None

    @model_validator(mode="after")
    def exclusion_is_explained(self) -> StateIdentityField:
        if self.included and self.exclusion_reason is not None:
            raise ValueError("included state fields cannot have an exclusion reason")
        if not self.included and not self.exclusion_reason:
            raise ValueError("excluded state fields require an explicit reason")
        return self


class StateIdentitySpecification(NatalTimeModel):
    schema_version: Literal["natal-state-identity-spec-v1"] = "natal-state-identity-spec-v1"
    identity_version: Literal["natal-full-state-identity-v1"] = "natal-full-state-identity-v1"
    fields: tuple[StateIdentityField, ...] = Field(min_length=1)
    reduced_signature_is_identity: Literal[False] = False

    @model_validator(mode="after")
    def unique_fields(self) -> StateIdentitySpecification:
        paths = [field.path for field in self.fields]
        if len(paths) != len(set(paths)):
            raise ValueError("state-identity field paths must be unique")
        return self

    @property
    def content_sha256(self) -> str:
        return sha256_json(self.model_dump(mode="json"))


class EphemerisFileProvenance(NatalTimeModel):
    name: str
    sha256: str = Field(pattern=SHA256_PATTERN)
    size_bytes: int = Field(ge=0)


class EngineProvenance(NatalTimeModel):
    schema_version: Literal["natal-engine-provenance-v2"] = "natal-engine-provenance-v2"
    repository_commit: str = Field(min_length=7)
    chart_engine_version: str
    dependency_lock_sha256: str = Field(pattern=SHA256_PATTERN)
    runtime_or_container_sha256: str = Field(pattern=SHA256_PATTERN)
    ephemeris_provider: str
    ephemeris_library_version: str
    ephemeris_files: tuple[EphemerisFileProvenance, ...]
    ephemeris_metadata_sha256: str = Field(pattern=SHA256_PATTERN)
    mandala_constants_sha256: str = Field(pattern=SHA256_PATTERN)
    bodygraph_constants_sha256: str = Field(pattern=SHA256_PATTERN)
    timezone_database_version: str
    timezone_file_sha256: str = Field(pattern=SHA256_PATTERN)
    canonicalizer_version: Literal["hdmatch-canonical-json-v1"] = "hdmatch-canonical-json-v1"
    enumerator_version: Literal["natal-civil-day-enumerator-v2"] = "natal-civil-day-enumerator-v2"
    boundary_method: Literal[
        "lipschitz-engine-grid-event-search-plus-independent-verification-v2"
    ] = "lipschitz-engine-grid-event-search-plus-independent-verification-v2"
    datetime_input_resolution_microseconds: Literal[1] = 1
    ephemeris_julian_day_quantum_microseconds: float | None = Field(default=None, gt=0.0)
    maximum_equal_ephemeris_time_span_microseconds: int = Field(ge=0)
    astronomical_microsecond_precision_claimed: Literal[False] = False
    boundary_root_tolerance_seconds: float = Field(gt=0.0, le=1.0)
    rounding_convention: Literal["first_changed_representable_microsecond"] = (
        "first_changed_representable_microsecond"
    )

    @property
    def content_sha256(self) -> str:
        return sha256_json(self.model_dump(mode="json"))


def full_state_identity_specification() -> StateIdentitySpecification:
    included = [
        *(
            StateIdentityField(
                path=f"activations.{side}.{body.value}.{attribute}",
                value_kind="discrete",
                included=True,
            )
            for side in ("personality", "design")
            for body in CelestialBody
            for attribute in ("gate", "line")
        ),
        *(
            StateIdentityField(path=f"bodygraph.{name}", value_kind="discrete", included=True)
            for name in (
                "active_gates",
                "channels",
                "defined_centers",
                "definition_components",
                "type",
                "strategy",
                "authority",
                "profile",
                "definition",
            )
        ),
        StateIdentityField(path="chart_engine_version", value_kind="provenance", included=True),
        StateIdentityField(path="mandala_constants_sha256", value_kind="provenance", included=True),
        StateIdentityField(
            path="bodygraph_constants_sha256", value_kind="provenance", included=True
        ),
        StateIdentityField(
            path="advanced_substructure_status", value_kind="provenance", included=True
        ),
    ]
    excluded = [
        StateIdentityField(
            path="personality_utc",
            value_kind="continuous_diagnostic",
            included=False,
            exclusion_reason="candidate coordinate; interval membership already carries it",
        ),
        StateIdentityField(
            path="design_utc",
            value_kind="continuous_diagnostic",
            included=False,
            exclusion_reason=(
                "continuous solved diagnostic; discrete design activations are included"
            ),
        ),
        StateIdentityField(
            path="activations[*].longitude",
            value_kind="continuous_diagnostic",
            included=False,
            exclusion_reason=(
                "continuous diagnostic; gate and line transitions define discrete state"
            ),
        ),
        StateIdentityField(
            path="ephemeris_speed_degrees_per_day",
            value_kind="continuous_diagnostic",
            included=False,
            exclusion_reason="boundary-proof diagnostic, not a downstream discrete chart field",
        ),
        StateIdentityField(
            path="design_root_diagnostics",
            value_kind="continuous_diagnostic",
            included=False,
            exclusion_reason=(
                "solver provenance is pinned; all eligible discrete outputs are included"
            ),
        ),
    ]
    return StateIdentitySpecification(fields=tuple((*included, *excluded)))


def build_engine_provenance(
    provider: EphemerisProvider,
    *,
    repository_commit: str,
    dependency_lock_path: str | Path,
    runtime_or_container_sha256: str,
    iana_timezone: str,
    boundary_root_tolerance_seconds: float = 0.000001,
) -> EngineProvenance:
    metadata = provider.metadata
    is_swiss_binary64 = metadata.provider == "swiss_ephemeris_local_files"
    return EngineProvenance(
        repository_commit=repository_commit,
        chart_engine_version=CHART_ENGINE_VERSION,
        dependency_lock_sha256=sha256_file(dependency_lock_path),
        runtime_or_container_sha256=runtime_or_container_sha256,
        ephemeris_provider=metadata.provider,
        ephemeris_library_version=metadata.library_version,
        ephemeris_files=tuple(
            EphemerisFileProvenance(
                name=Path(item.path).name,
                sha256=item.sha256,
                size_bytes=item.size_bytes,
            )
            for item in metadata.files
        ),
        ephemeris_metadata_sha256=sha256_json(asdict(metadata)),
        mandala_constants_sha256=mandala_constants_sha256(),
        bodygraph_constants_sha256=bodygraph_constants_sha256(),
        timezone_database_version=timezone_database_version(),
        timezone_file_sha256=timezone_file_sha256(iana_timezone),
        ephemeris_julian_day_quantum_microseconds=(
            SWISS_JULIAN_DAY_QUANTUM_MICROSECONDS if is_swiss_binary64 else None
        ),
        maximum_equal_ephemeris_time_span_microseconds=(40 if is_swiss_binary64 else 0),
        boundary_root_tolerance_seconds=boundary_root_tolerance_seconds,
    )


def timezone_file_sha256(iana_timezone: str) -> str:
    relative = Path(*iana_timezone.split("/"))
    for root in TZPATH:
        candidate = Path(root) / relative
        if candidate.is_file():
            return sha256_file(candidate)
    raise ValueError(f"cannot checksum timezone data for {iana_timezone}")


def synthetic_runtime_digest(label: str) -> str:
    """Create a conspicuously synthetic runtime commitment for unit fixtures."""

    return sha256(f"synthetic-runtime:{label}".encode()).hexdigest()


def default_activation_field_count() -> int:
    """Expose the expected number of personality/design body activations."""

    return len(CelestialBody) * 2
