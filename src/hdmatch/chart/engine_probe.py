"""Representative fail-closed validation for the production astronomy engine."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Final

from .design_moment import solve_design_moment
from .ephemeris import (
    CelestialBody,
    EphemerisFile,
    EphemerisMode,
    SwissEphemerisProvider,
)
from .rave_mandala import longitude_to_gate_line


class EngineValidationError(RuntimeError):
    """Raised when a representative production-engine invariant fails."""


CANONICAL_PROBE_INSTANTS: Final[tuple[datetime, ...]] = (
    datetime(1926, 8, 22, tzinfo=UTC),
    datetime(1976, 8, 22, 12, tzinfo=UTC),
    datetime(2026, 8, 22, 23, 59, 59, tzinfo=UTC),
)

# Earth and South Node are exact derived oppositions.  Every other scored body
# makes a direct Swiss calculation and therefore receives its own probe record.
DIRECT_PRODUCTION_BODIES: Final[tuple[CelestialBody, ...]] = (
    CelestialBody.SUN,
    CelestialBody.MOON,
    CelestialBody.NORTH_NODE,
    CelestialBody.MERCURY,
    CelestialBody.VENUS,
    CelestialBody.MARS,
    CelestialBody.JUPITER,
    CelestialBody.SATURN,
    CelestialBody.URANUS,
    CelestialBody.NEPTUNE,
    CelestialBody.PLUTO,
)


@dataclass(frozen=True, slots=True)
class RepresentativeCalculationProbe:
    at_utc: datetime
    body: CelestialBody
    longitude: float
    speed_degrees_per_day: float
    gate: int
    line: int
    requested_mode: EphemerisMode
    returned_mode: EphemerisMode
    requested_flags: int
    returned_flags: int
    ephemeris_mask: int
    used_file_name: str
    used_file_sha256: str


@dataclass(frozen=True, slots=True)
class DesignRootProbe:
    personality_utc: datetime
    design_utc: datetime
    target_arc_degrees: float
    solved_arc_degrees: float
    residual_degrees: float
    time_tolerance_seconds: float
    arc_tolerance_degrees: float


@dataclass(frozen=True, slots=True)
class ProductionEngineValidation:
    """Deterministic evidence required before authoritative cache generation."""

    schema_version: str
    validation_status: str
    provider: str
    library_version: str
    ephemeris_path: str
    ephemeris_requested: EphemerisMode
    ephemeris_returned: EphemerisMode
    requested_flags: int
    ephemeris_mask: int
    files: tuple[EphemerisFile, ...]
    calculation_probes: tuple[RepresentativeCalculationProbe, ...]
    design_root_probes: tuple[DesignRootProbe, ...]
    gate_line_deterministic: bool
    design_root_converged: bool


def validate_production_engine(
    provider: SwissEphemerisProvider,
    *,
    instants: tuple[datetime, ...] = CANONICAL_PROBE_INSTANTS,
    bodies: tuple[CelestialBody, ...] = DIRECT_PRODUCTION_BODIES,
    design_time_tolerance_seconds: float = 0.01,
    design_arc_tolerance_degrees: float = 1e-8,
) -> ProductionEngineValidation:
    """Probe SWIEPH at representative times and fail on any inconsistency.

    The provider enforces the exact returned ephemeris mask on every direct
    calculation, including all iterative Sun calls made by the Design solver.
    This function additionally retains representative returned flags and proves
    deterministic Gate/Line derivation and Design-root convergence.
    """

    if not instants:
        raise ValueError("at least one representative probe instant is required")
    if not bodies:
        raise ValueError("at least one directly calculated body is required")
    if any(body in (CelestialBody.EARTH, CelestialBody.SOUTH_NODE) for body in bodies):
        raise ValueError("representative body probes must name direct Swiss calculations")

    metadata = provider.metadata
    if metadata.ephemeris_path is None:
        raise EngineValidationError("production provider has no explicit ephemeris path")
    if metadata.requested_ephemeris is not EphemerisMode.SWIEPH:
        raise EngineValidationError("production provider did not request SWIEPH")
    if metadata.requested_flags is None or metadata.ephemeris_mask is None:
        raise EngineValidationError("production provider has incomplete requested-flag metadata")

    calculations: list[RepresentativeCalculationProbe] = []
    roots: list[DesignRootProbe] = []
    for raw_instant in instants:
        instant = _require_utc(raw_instant)
        for body in bodies:
            first = provider.position_with_provenance(body, instant)
            second = provider.position_with_provenance(body, instant)
            if first != second:
                raise EngineValidationError(
                    f"non-deterministic Swiss position for {body.value} at {instant.isoformat()}"
                )
            gate_line = longitude_to_gate_line(first.position.longitude)
            repeated_gate_line = longitude_to_gate_line(second.position.longitude)
            if gate_line != repeated_gate_line:
                raise EngineValidationError(
                    f"non-deterministic Gate/Line derivation for {body.value} "
                    f"at {instant.isoformat()}"
                )
            provenance = first.provenance
            calculations.append(
                RepresentativeCalculationProbe(
                    at_utc=instant,
                    body=body,
                    longitude=first.position.longitude,
                    speed_degrees_per_day=first.position.speed_degrees_per_day,
                    gate=gate_line.gate,
                    line=gate_line.line,
                    requested_mode=provenance.requested_mode,
                    returned_mode=provenance.returned_mode,
                    requested_flags=provenance.requested_flags,
                    returned_flags=provenance.returned_flags,
                    ephemeris_mask=provenance.ephemeris_mask,
                    used_file_name=provenance.used_file.path.rsplit("/", 1)[-1],
                    used_file_sha256=provenance.used_file.sha256,
                )
            )

        root = solve_design_moment(
            provider,
            instant,
            time_tolerance_seconds=design_time_tolerance_seconds,
            arc_tolerance_degrees=design_arc_tolerance_degrees,
        )
        if abs(root.residual_degrees) > root.arc_tolerance_degrees:
            raise EngineValidationError(
                f"Design root did not converge at {instant.isoformat()}: "
                f"residual={root.residual_degrees}"
            )
        roots.append(
            DesignRootProbe(
                personality_utc=instant,
                design_utc=root.design_utc,
                target_arc_degrees=root.target_arc_degrees,
                solved_arc_degrees=root.solved_arc_degrees,
                residual_degrees=root.residual_degrees,
                time_tolerance_seconds=root.time_tolerance_seconds,
                arc_tolerance_degrees=root.arc_tolerance_degrees,
            )
        )

    returned_modes = {probe.returned_mode for probe in calculations}
    if returned_modes != {EphemerisMode.SWIEPH}:
        raise EngineValidationError(f"representative probes returned modes={returned_modes!r}")

    return ProductionEngineValidation(
        schema_version="production-engine-validation-v1",
        validation_status="pass",
        provider=metadata.provider,
        library_version=metadata.library_version,
        ephemeris_path=metadata.ephemeris_path,
        ephemeris_requested=EphemerisMode.SWIEPH,
        ephemeris_returned=EphemerisMode.SWIEPH,
        requested_flags=metadata.requested_flags,
        ephemeris_mask=metadata.ephemeris_mask,
        files=metadata.files,
        calculation_probes=tuple(calculations),
        design_root_probes=tuple(roots),
        gate_line_deterministic=True,
        design_root_converged=True,
    )


def _require_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("engine probe timestamps must be timezone-aware")
    return value.astimezone(UTC)
