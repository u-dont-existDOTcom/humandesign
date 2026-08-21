"""Strict ephemeris protocol and fail-closed Swiss Ephemeris adapter.

Swiss Ephemeris can silently substitute its analytical Moshier ephemeris when a
requested data file is unavailable.  The adapter therefore verifies both the
returned calculation flag and, where Swiss exposes it, the actual file path.
See the upstream programming manual:
https://www.astro.com/swisseph/swephprg.2.10.pdf (sections 2.6 and 3.3.2), and
the official source: https://github.com/aloistr/swisseph/blob/master/sweph.c.
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from hashlib import sha256
from pathlib import Path
from threading import RLock
from types import ModuleType
from typing import Final, Protocol, runtime_checkable


class EphemerisError(RuntimeError):
    """Base error for deterministic ephemeris failures."""


class EphemerisConfigurationError(EphemerisError):
    """Raised when local files or a frozen convention are missing."""


class EphemerisFallbackError(EphemerisError):
    """Raised whenever Swiss Ephemeris did not use the requested local files."""


class CelestialBody(StrEnum):
    SUN = "sun"
    EARTH = "earth"
    MOON = "moon"
    NORTH_NODE = "north_node"
    SOUTH_NODE = "south_node"
    MERCURY = "mercury"
    VENUS = "venus"
    MARS = "mars"
    JUPITER = "jupiter"
    SATURN = "saturn"
    URANUS = "uranus"
    NEPTUNE = "neptune"
    PLUTO = "pluto"


class NodeConvention(StrEnum):
    TRUE = "true"
    MEAN = "mean"


DEFAULT_ACTIVATION_BODIES: Final[tuple[CelestialBody, ...]] = tuple(CelestialBody)


@dataclass(frozen=True, slots=True)
class EclipticPosition:
    """Geocentric tropical ecliptic longitude and instantaneous speed."""

    longitude: float
    speed_degrees_per_day: float


@dataclass(frozen=True, slots=True)
class EphemerisFile:
    path: str
    sha256: str
    size_bytes: int


@dataclass(frozen=True, slots=True)
class EphemerisMetadata:
    provider: str
    library_version: str
    files: tuple[EphemerisFile, ...]
    calculation_flags: tuple[str, ...]
    coordinate_frame: str
    node_convention: NodeConvention


@runtime_checkable
class EphemerisProvider(Protocol):
    """The complete astronomical interface required by the chart engine."""

    @property
    def metadata(self) -> EphemerisMetadata:
        """Return immutable provenance for all position calculations."""

    def position(self, body: CelestialBody, at_utc: datetime) -> EclipticPosition:
        """Calculate one geocentric tropical ecliptic position at UTC."""

    def max_abs_speed_degrees_per_day(self, body: CelestialBody) -> float:
        """Return a conservative declared speed bound used by event search."""

    def min_solar_speed_degrees_per_day(self) -> float:
        """Return a positive lower bound for the apparent solar speed."""


# Conservative geocentric apparent bounds over the intended historical range.
# They intentionally exceed ordinary observed maxima; completeness audits must
# still compare detected events against an independent fine scan.
_MAX_SPEEDS: Final[dict[CelestialBody, float]] = {
    CelestialBody.SUN: 1.1,
    CelestialBody.EARTH: 1.1,
    CelestialBody.MOON: 16.0,
    CelestialBody.NORTH_NODE: 0.3,
    CelestialBody.SOUTH_NODE: 0.3,
    CelestialBody.MERCURY: 2.5,
    CelestialBody.VENUS: 1.5,
    CelestialBody.MARS: 1.0,
    CelestialBody.JUPITER: 0.3,
    CelestialBody.SATURN: 0.2,
    CelestialBody.URANUS: 0.1,
    CelestialBody.NEPTUNE: 0.08,
    CelestialBody.PLUTO: 0.06,
}
_MIN_SOLAR_SPEED: Final[float] = 0.9
_SWISS_LOCK = RLock()


class SwissEphemerisProvider:
    """Geocentric tropical Swiss-file provider with no fallback permission.

    ``ephemeris_files`` must enumerate the local ``.se1`` files authorized for
    use.  Every file is hashed at construction.  The parent directory is reset
    before every call because the upstream C library stores this path globally.
    """

    def __init__(
        self,
        ephemeris_files: tuple[str | Path, ...],
        *,
        node_convention: NodeConvention = NodeConvention.TRUE,
        _swe_module: ModuleType | None = None,
    ) -> None:
        if not ephemeris_files:
            raise EphemerisConfigurationError(
                "at least one declared local ephemeris file is required"
            )

        paths = tuple(Path(item).expanduser().resolve(strict=False) for item in ephemeris_files)
        root = paths[0].parent
        if any(path.parent != root for path in paths):
            raise EphemerisConfigurationError(
                "declared Swiss planetary/moon files must share one direct parent directory"
            )
        records: list[EphemerisFile] = []
        for path in sorted(paths):
            if not path.is_file():
                raise EphemerisConfigurationError(f"declared ephemeris file is missing: {path}")
            if path.suffix != ".se1":
                raise EphemerisConfigurationError(
                    f"declared ephemeris file must end in .se1: {path}"
                )
            records.append(
                EphemerisFile(
                    path=str(path),
                    sha256=_sha256_file(path),
                    size_bytes=path.stat().st_size,
                )
            )

        if _swe_module is None:
            try:
                _swe_module = importlib.import_module("swisseph")
            except ModuleNotFoundError as exc:
                raise EphemerisConfigurationError(
                    "pyswisseph is required; install hdmatch[ephemeris]"
                ) from exc

        self._swe = _swe_module
        self._root = root
        self._declared = frozenset(paths)
        self._node_convention = node_convention
        version = str(getattr(self._swe, "version", "unknown"))
        self._metadata = EphemerisMetadata(
            provider="swiss_ephemeris_local_files",
            library_version=version,
            files=tuple(records),
            calculation_flags=("SEFLG_SWIEPH", "SEFLG_SPEED", "geocentric", "tropical"),
            coordinate_frame="geocentric_apparent_tropical_ecliptic_of_date",
            node_convention=node_convention,
        )

    @property
    def metadata(self) -> EphemerisMetadata:
        return self._metadata

    def max_abs_speed_degrees_per_day(self, body: CelestialBody) -> float:
        return _MAX_SPEEDS[body]

    def min_solar_speed_degrees_per_day(self) -> float:
        return _MIN_SOLAR_SPEED

    def position(self, body: CelestialBody, at_utc: datetime) -> EclipticPosition:
        at_utc = _require_utc(at_utc)
        if body is CelestialBody.EARTH:
            sun = self.position(CelestialBody.SUN, at_utc)
            return EclipticPosition((sun.longitude + 180.0) % 360.0, sun.speed_degrees_per_day)
        if body is CelestialBody.SOUTH_NODE:
            north = self.position(CelestialBody.NORTH_NODE, at_utc)
            return EclipticPosition(
                (north.longitude + 180.0) % 360.0,
                north.speed_degrees_per_day,
            )

        planet_id, file_index = self._planet_id_and_file_index(body)
        flags = int(self._swe.FLG_SWIEPH) | int(self._swe.FLG_SPEED)
        julian_day = _julian_day_ut(self._swe, at_utc)

        with _SWISS_LOCK:
            self._swe.set_ephe_path(str(self._root))
            values, returned_flags = self._swe.calc_ut(julian_day, planet_id, flags)
            if returned_flags & int(self._swe.FLG_MOSEPH):
                raise EphemerisFallbackError(
                    f"Swiss Ephemeris silently used Moshier for {body.value} "
                    f"at {at_utc.isoformat()}"
                )
            if not returned_flags & int(self._swe.FLG_SWIEPH):
                raise EphemerisFallbackError(
                    f"Swiss-file flag absent for {body.value} at {at_utc.isoformat()}; "
                    f"returned flags={returned_flags}"
                )
            self._verify_current_file(file_index, body, at_utc)

        return EclipticPosition(float(values[0]) % 360.0, float(values[3]))

    def _planet_id_and_file_index(self, body: CelestialBody) -> tuple[int, int]:
        names = {
            CelestialBody.SUN: ("SUN", 0),
            CelestialBody.MOON: ("MOON", 1),
            CelestialBody.MERCURY: ("MERCURY", 0),
            CelestialBody.VENUS: ("VENUS", 0),
            CelestialBody.MARS: ("MARS", 0),
            CelestialBody.JUPITER: ("JUPITER", 0),
            CelestialBody.SATURN: ("SATURN", 0),
            CelestialBody.URANUS: ("URANUS", 0),
            CelestialBody.NEPTUNE: ("NEPTUNE", 0),
            CelestialBody.PLUTO: ("PLUTO", 0),
        }
        if body is CelestialBody.NORTH_NODE:
            node_name = "TRUE_NODE" if self._node_convention is NodeConvention.TRUE else "MEAN_NODE"
            return int(getattr(self._swe, node_name)), 1
        try:
            name, index = names[body]
        except KeyError as exc:  # pragma: no cover - enum exhaustiveness guard
            raise ValueError(f"unsupported Swiss body: {body}") from exc
        return int(getattr(self._swe, name)), index

    def _verify_current_file(
        self,
        file_index: int,
        body: CelestialBody,
        at_utc: datetime,
    ) -> None:
        getter = getattr(self._swe, "get_current_file_data", None)
        if getter is None:
            raise EphemerisFallbackError(
                "Swiss binding lacks get_current_file_data; used-file provenance cannot be verified"
            )
        used_path, _start, _end, _denum = getter(file_index)
        if not used_path:
            raise EphemerisFallbackError(
                f"Swiss did not report a local file for {body.value} at {at_utc.isoformat()}"
            )
        resolved = Path(str(used_path)).resolve(strict=False)
        if resolved not in self._declared:
            raise EphemerisFallbackError(
                f"Swiss used undeclared ephemeris file {resolved} for {body.value}"
            )


def _sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _require_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("ephemeris timestamps must be timezone-aware")
    return value.astimezone(UTC)


def _julian_day_ut(swe: ModuleType, at_utc: datetime) -> float:
    hour = (
        at_utc.hour
        + at_utc.minute / 60.0
        + at_utc.second / 3600.0
        + at_utc.microsecond / 3_600_000_000.0
    )
    return float(swe.julday(at_utc.year, at_utc.month, at_utc.day, hour, swe.GREG_CAL))
