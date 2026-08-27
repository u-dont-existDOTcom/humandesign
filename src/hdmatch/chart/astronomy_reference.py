"""Reference astronomy records kept separate from astrological projections.

The existing AstroHD pipeline intentionally consumes geocentric tropical longitude.
This module preserves richer, provenance-bearing astronomical state so tropical,
sidereal, constellation, and gate systems can be evaluated as competing transforms
of the same frozen source state rather than silently conflated.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .rave_mandala import MandalaPosition, longitude_to_gate_line


class AstronomyReferenceError(RuntimeError):
    """Raised when a reference astronomical state cannot be produced safely."""


class UnsupportedAstronomyProjection(AstronomyReferenceError):
    """Raised when a requested projection has not been implemented and validated."""


class AstronomyModel(BaseModel):
    """Strict immutable base class for frozen astronomy records."""

    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class ObserverOrigin(StrEnum):
    BARYCENTRIC = "barycentric"
    HELIOCENTRIC = "heliocentric"
    GEOCENTRIC = "geocentric"
    TOPOCENTRIC = "topocentric"


class ReferenceFrame(StrEnum):
    ICRF_J2000 = "icrf_j2000"
    EQUATORIAL_OF_DATE = "equatorial_of_date"
    ECLIPTIC_OF_DATE = "ecliptic_of_date"


class ProjectionKind(StrEnum):
    TROPICAL_EQUINOX_OF_DATE = "tropical_equinox_of_date"
    SIDEREAL_NAMED_AYANAMSA = "sidereal_named_ayanamsa"
    IAU_CONSTELLATION = "iau_constellation"
    ASTROHD_GATE = "astrohd_gate"


class EphemerisFileProvenance(AstronomyModel):
    """One immutable file/kernel identity used to derive the state."""

    name: str = Field(min_length=1)
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")


class AstronomyProvenance(AstronomyModel):
    """Enough metadata to reproduce which astronomical convention was requested."""

    provider: str = Field(min_length=1)
    provider_version: str = Field(min_length=1)
    package: str | None = None
    input_time_scale: str = Field(min_length=1)
    origin: ObserverOrigin
    native_frame: ReferenceFrame
    calculation_flags: tuple[str, ...] = ()
    source_files: tuple[EphemerisFileProvenance, ...] = ()
    notes: tuple[str, ...] = ()


class AstronomyState(AstronomyModel):
    """Richer astronomical state from which competing projections can be derived."""

    schema_version: Literal["astronomy-reference-state-v1"] = "astronomy-reference-state-v1"
    observed_at_utc: datetime
    julian_day_ut: float
    body: str = Field(min_length=1)
    provenance: AstronomyProvenance
    ecliptic_longitude_deg: float = Field(ge=0.0, lt=360.0)
    ecliptic_latitude_deg: float = Field(ge=-90.0, le=90.0)
    distance_au: float = Field(gt=0.0)
    right_ascension_deg: float = Field(ge=0.0, lt=360.0)
    declination_deg: float = Field(ge=-90.0, le=90.0)
    cartesian_position_au: tuple[float, float, float]
    cartesian_velocity_au_per_day: tuple[float, float, float]

    @field_validator("observed_at_utc")
    @classmethod
    def normalize_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("observed_at_utc must be timezone-aware")
        return value.astimezone(UTC)


class ProjectionSpec(AstronomyModel):
    kind: ProjectionKind
    description: str
    status: Literal["implemented", "registered_fail_closed"]
    requires: tuple[str, ...] = ()


PROJECTION_SPECS: tuple[ProjectionSpec, ...] = (
    ProjectionSpec(
        kind=ProjectionKind.TROPICAL_EQUINOX_OF_DATE,
        description="Equal 30-degree signs anchored to the moving equinox convention.",
        status="implemented",
        requires=("ecliptic_longitude_deg",),
    ),
    ProjectionSpec(
        kind=ProjectionKind.SIDEREAL_NAMED_AYANAMSA,
        description="Equal 30-degree sidereal signs using an explicitly frozen ayanamsa.",
        status="implemented",
        requires=("ecliptic_longitude_deg", "ayanamsa_name", "ayanamsa_deg"),
    ),
    ProjectionSpec(
        kind=ProjectionKind.IAU_CONSTELLATION,
        description="Actual IAU sky-region membership using full position and boundaries.",
        status="registered_fail_closed",
        requires=("right_ascension_deg", "declination_deg", "IAU boundary dataset"),
    ),
    ProjectionSpec(
        kind=ProjectionKind.ASTROHD_GATE,
        description="Existing AstroHD/Human Design gate projection from tropical longitude.",
        status="implemented",
        requires=("ecliptic_longitude_deg", "validated project gate mapper"),
    ),
)


def projection_spec(kind: ProjectionKind) -> ProjectionSpec:
    """Return the frozen registry entry for one coordinate/projection hypothesis."""

    for spec in PROJECTION_SPECS:
        if spec.kind is kind:
            return spec
    raise UnsupportedAstronomyProjection(f"unregistered astronomy projection: {kind}")


def normalize_longitude(value: float) -> float:
    """Normalize a longitude to the half-open [0, 360) interval."""

    return value % 360.0


def tropical_longitude(state: AstronomyState) -> float:
    """Return the state's explicitly tropical/ecliptic longitude."""

    return state.ecliptic_longitude_deg


def sidereal_longitude(
    state: AstronomyState,
    *,
    ayanamsa_name: str,
    ayanamsa_deg: float,
) -> float:
    """Project tropical longitude into a named, explicitly frozen sidereal convention."""

    if not ayanamsa_name.strip():
        raise ValueError("ayanamsa_name must be explicit")
    if not 0.0 <= ayanamsa_deg < 360.0:
        raise ValueError("ayanamsa_deg must be in [0, 360)")
    return normalize_longitude(state.ecliptic_longitude_deg - ayanamsa_deg)


def astrohd_gate(state: AstronomyState) -> MandalaPosition:
    """Project the frozen tropical longitude through the validated Rave Mandala mapper."""

    return longitude_to_gate_line(state.ecliptic_longitude_deg)


def iau_constellation(_state: AstronomyState) -> str:
    """Fail closed until a versioned IAU boundary dataset/resolver is checked in."""

    raise UnsupportedAstronomyProjection(
        "IAU constellation lookup requires a versioned boundary dataset; "
        "longitude-only zodiac substitution is scientifically invalid"
    )


class SwissEngine(Protocol):
    """Small typed surface used from pyswisseph without importing it at module import."""

    FLG_SWIEPH: int
    FLG_SPEED: int
    FLG_EQUATORIAL: int
    FLG_XYZ: int

    def calc_ut(
        self,
        jd_ut: float,
        body: int,
        flags: int,
    ) -> tuple[tuple[float, ...], int]: ...


class SwissAstronomyReferenceProvider:
    """Produce richer geocentric Swiss-Ephemeris state with explicit provenance.

    This is deliberately not labelled ICRF/barycentric. It preserves the richer
    Swiss geocentric ecliptic/equatorial/Cartesian outputs while a separate JPL
    differential audit can certify numerical agreement for the research interval.
    """

    def __init__(self, *, engine: SwissEngine, provenance: AstronomyProvenance) -> None:
        if provenance.origin is not ObserverOrigin.GEOCENTRIC:
            raise ValueError("Swiss reference provider v1 is geocentric only")
        if provenance.native_frame is not ReferenceFrame.ECLIPTIC_OF_DATE:
            raise ValueError("Swiss reference provider v1 expects ecliptic_of_date provenance")
        self.engine = engine
        self.provenance = provenance

    def state(
        self,
        *,
        jd_ut: float,
        observed_at_utc: datetime,
        body_name: str,
        body_id: int,
    ) -> AstronomyState:
        """Calculate longitude/latitude/distance, RA/Dec, XYZ, and velocities."""

        base = self.engine.FLG_SWIEPH | self.engine.FLG_SPEED
        ecliptic = self._calculate(jd_ut, body_id, base)
        equatorial = self._calculate(jd_ut, body_id, base | self.engine.FLG_EQUATORIAL)
        cartesian = self._calculate(jd_ut, body_id, base | self.engine.FLG_XYZ)
        return AstronomyState(
            observed_at_utc=observed_at_utc,
            julian_day_ut=jd_ut,
            body=body_name,
            provenance=self.provenance,
            ecliptic_longitude_deg=normalize_longitude(ecliptic[0]),
            ecliptic_latitude_deg=ecliptic[1],
            distance_au=ecliptic[2],
            right_ascension_deg=normalize_longitude(equatorial[0]),
            declination_deg=equatorial[1],
            cartesian_position_au=(cartesian[0], cartesian[1], cartesian[2]),
            cartesian_velocity_au_per_day=(cartesian[3], cartesian[4], cartesian[5]),
        )

    def _calculate(self, jd_ut: float, body_id: int, flags: int) -> tuple[float, ...]:
        values, returned_flags = self.engine.calc_ut(jd_ut, body_id, flags)
        if returned_flags & self.engine.FLG_SWIEPH == 0:
            raise AstronomyReferenceError(
                "Swiss Ephemeris did not report FLG_SWIEPH; refusing silent fallback"
            )
        if len(values) < 6:
            raise AstronomyReferenceError("Swiss Ephemeris returned an incomplete state vector")
        return values
