"""Reference astronomy records kept separate from astrological projections.

The existing AstroHD pipeline intentionally consumes geocentric tropical longitude.
This module preserves richer, provenance-bearing astronomical state so tropical,
sidereal, constellation, and gate systems can be evaluated as competing transforms
of the same frozen source state rather than silently conflated.
"""

from __future__ import annotations

import importlib
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Literal, Protocol

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


class IauConstellationProjection(AstronomyModel):
    """One versioned actual-sky constellation projection result."""

    schema_version: Literal["iau-constellation-projection-v1"] = (
        "iau-constellation-projection-v1"
    )
    name: str = Field(min_length=1)
    abbreviation: str = Field(min_length=2, max_length=4)
    resolver: str = Field(min_length=1)
    resolver_version: str = Field(min_length=1)
    input_frame: Literal["geocentric_true_ecliptic_of_date"] = (
        "geocentric_true_ecliptic_of_date"
    )
    boundary_reference: Literal[
        "IAU-88-Delporte-B1875-Roman1987"
    ] = "IAU-88-Delporte-B1875-Roman1987"


class IauConstellationResolver(Protocol):
    """Explicit pluggable boundary resolver for the A2 astronomy hypothesis."""

    def resolve(self, state: AstronomyState) -> IauConstellationProjection: ...


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
        description=(
            "Actual IAU sky-region membership using the 88 irregular Delporte boundaries."
        ),
        status="implemented",
        requires=(
            "ecliptic longitude/latitude/distance of date",
            "explicit version-pinned IAU boundary resolver",
        ),
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


def iau_constellation(
    state: AstronomyState,
    *,
    resolver: IauConstellationResolver | None = None,
) -> IauConstellationProjection:
    """Resolve actual IAU constellation membership with an explicit boundary engine.

    No longitude-only fallback exists.  Scientific runs must instantiate and pin a
    concrete resolver so the package/boundary implementation is part of provenance.
    """

    if resolver is None:
        raise UnsupportedAstronomyProjection(
            "IAU constellation lookup requires an explicit version-pinned boundary resolver; "
            "longitude-only zodiac substitution is scientifically invalid"
        )
    return resolver.resolve(state)


class AstropyIauConstellationResolver:
    """Resolve IAU-88 membership through Astropy's Delporte/Roman boundary tables.

    Imports are deliberately lazy so the participant server does not require Astropy.
    The supplied astronomy state is interpreted as geocentric *true* ecliptic of date,
    matching the ordinary apparent Swiss output convention.  Astropy then transforms
    the coordinate and its ``get_constellation`` implementation precesses to B1875 and
    applies the Delporte boundaries tabulated by Roman (1987).
    """

    def __init__(self, *, expected_astropy_version: str) -> None:
        if not expected_astropy_version.strip():
            raise ValueError("expected_astropy_version must be explicit")
        try:
            astropy = importlib.import_module("astropy")
            self._coordinates = importlib.import_module("astropy.coordinates")
            self._units = importlib.import_module("astropy.units")
            self._time = importlib.import_module("astropy.time")
        except ModuleNotFoundError as exc:
            raise UnsupportedAstronomyProjection(
                "Astropy IAU resolver requested but Astropy is not installed"
            ) from exc
        observed_version = str(getattr(astropy, "__version__", "unknown"))
        if observed_version != expected_astropy_version:
            raise UnsupportedAstronomyProjection(
                "Astropy IAU resolver version mismatch: "
                f"expected {expected_astropy_version}, observed {observed_version}"
            )
        self.version = observed_version

    def resolve(self, state: AstronomyState) -> IauConstellationProjection:
        if state.provenance.origin is not ObserverOrigin.GEOCENTRIC:
            raise UnsupportedAstronomyProjection(
                "Astropy IAU resolver v1 requires a geocentric astronomy state"
            )
        time = self._time.Time(state.observed_at_utc)
        frame = self._coordinates.GeocentricTrueEcliptic(
            lon=state.ecliptic_longitude_deg * self._units.deg,
            lat=state.ecliptic_latitude_deg * self._units.deg,
            distance=state.distance_au * self._units.au,
            equinox=time,
            obstime=time,
        )
        coordinate = self._coordinates.SkyCoord(frame)
        full_name = _scalar_text(
            self._coordinates.get_constellation(
                coordinate,
                short_name=False,
                constellation_list="iau",
            )
        )
        abbreviation = _scalar_text(
            self._coordinates.get_constellation(
                coordinate,
                short_name=True,
                constellation_list="iau",
            )
        )
        return IauConstellationProjection(
            name=full_name,
            abbreviation=abbreviation,
            resolver="astropy.coordinates.get_constellation",
            resolver_version=self.version,
        )


def _scalar_text(value: Any) -> str:
    text = str(value)
    if not text:
        raise AstronomyReferenceError("constellation resolver returned an empty value")
    return text


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