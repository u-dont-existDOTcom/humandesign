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
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum
from hashlib import sha256
from pathlib import Path
from threading import RLock
from types import ModuleType
from typing import Final, Protocol, runtime_checkable

from hdmatch.provenance.swisseph_files import REQUIRED_EPHEMERIS_FILES
from hdmatch.util import canonical_json_bytes


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


class EphemerisMode(StrEnum):
    """Swiss Ephemeris calculation modes encoded in the returned flag mask."""

    JPLEPH = "JPLEPH"
    SWIEPH = "SWIEPH"
    MOSEPH = "MOSEPH"


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
class EphemerisCalculationProvenance:
    """Returned-mode evidence for one public position calculation.

    Earth and South Node positions are exact oppositions derived from a direct
    Sun or North Node calculation.  ``calculated_body`` and ``derivation`` make
    that relationship explicit while preserving the returned flags from the
    underlying Swiss calculation.
    """

    requested_body: CelestialBody
    calculated_body: CelestialBody
    at_utc: datetime
    requested_mode: EphemerisMode
    returned_mode: EphemerisMode
    requested_flags: int
    returned_flags: int
    ephemeris_mask: int
    ephemeris_path: str
    used_file: EphemerisFile
    derivation: str | None = None


@dataclass(frozen=True, slots=True)
class PositionCalculation:
    """A position bundled with the flags and file that produced it."""

    position: EclipticPosition
    provenance: EphemerisCalculationProvenance


@dataclass(frozen=True, slots=True)
class EphemerisMetadata:
    provider: str
    library_version: str
    files: tuple[EphemerisFile, ...]
    calculation_flags: tuple[str, ...]
    coordinate_frame: str
    node_convention: NodeConvention
    ephemeris_path: str | None = None
    requested_ephemeris: EphemerisMode | None = None
    requested_flags: int | None = None
    ephemeris_mask: int | None = None


@dataclass(frozen=True, slots=True)
class SwissCalculationAuditSnapshot:
    """Deterministic all-call evidence captured inside the Swiss wrapper.

    The trace hashes every successful ``calc_ut`` return in call order before
    the returned-mode check can raise.  A persisted caller may summarize this
    snapshot, but only deterministic replay can establish a new in-process
    verified calculation capability.
    """

    requested_flags: int
    ephemeris_mask: int
    swieph_flag: int
    calculation_call_count: int
    requested_flags_counts: tuple[tuple[int, int], ...]
    returned_flags_counts: tuple[tuple[int, int], ...]
    returned_mode_bits_counts: tuple[tuple[int, int], ...]
    calculated_body_counts: tuple[tuple[str, int], ...]
    used_file_counts: tuple[tuple[str, str, int, int], ...]
    calculation_trace_sha256: str
    first_calculation_sha256: str | None
    final_calculation_sha256: str | None
    entry_provider_configuration_sha256: str
    exit_provider_configuration_sha256: str
    entry_ephemeris_file_set_sha256: str
    exit_ephemeris_file_set_sha256: str


class SwissCalculationAuditCapture:
    """Bounded mutable recorder exposed only through the provider context."""

    __slots__ = (
        "_call_count",
        "_calculated_body_counts",
        "_closed",
        "_digest",
        "_entry_ephemeris_file_set_sha256",
        "_entry_provider_configuration_sha256",
        "_ephemeris_mask",
        "_exit_ephemeris_file_set_sha256",
        "_exit_provider_configuration_sha256",
        "_final_sha256",
        "_first_sha256",
        "_requested_flags",
        "_requested_flags_counts",
        "_returned_flags_counts",
        "_returned_mode_bits_counts",
        "_swieph_flag",
        "_used_file_counts",
    )

    def __init__(
        self,
        *,
        requested_flags: int,
        ephemeris_mask: int,
        swieph_flag: int,
    ) -> None:
        self._requested_flags = requested_flags
        self._ephemeris_mask = ephemeris_mask
        self._swieph_flag = swieph_flag
        self._call_count = 0
        self._requested_flags_counts: dict[int, int] = {}
        self._returned_flags_counts: dict[int, int] = {}
        self._returned_mode_bits_counts: dict[int, int] = {}
        self._calculated_body_counts: dict[str, int] = {}
        self._used_file_counts: dict[tuple[str, str, int], int] = {}
        self._digest = sha256()
        self._first_sha256: str | None = None
        self._final_sha256: str | None = None
        self._entry_provider_configuration_sha256: str | None = None
        self._exit_provider_configuration_sha256: str | None = None
        self._entry_ephemeris_file_set_sha256: str | None = None
        self._exit_ephemeris_file_set_sha256: str | None = None
        self._closed = False

    def _record(
        self,
        *,
        body: CelestialBody,
        at_utc: datetime,
        returned_flags: int,
        used_file: EphemerisFile | None,
        longitude: float,
        speed_degrees_per_day: float,
    ) -> None:
        if self._closed:  # pragma: no cover - provider owns capture lifetime
            raise RuntimeError("Swiss calculation audit capture is already closed")
        self._call_count += 1
        returned_mode_bits = returned_flags & self._ephemeris_mask
        payload = canonical_json_bytes(
            {
                "at_utc": at_utc.astimezone(UTC).isoformat(),
                "body": body.value,
                "call_index": self._call_count,
                "requested_flags": self._requested_flags,
                "returned_flags": returned_flags,
                "returned_mode_bits": returned_mode_bits,
                "returned_longitude": longitude,
                "returned_speed_degrees_per_day": speed_degrees_per_day,
                "schema_version": "swiss-calculation-audit-call-v1",
                "used_file": (
                    None
                    if used_file is None
                    else {
                        "bytes": used_file.size_bytes,
                        "name": Path(used_file.path).name,
                        "sha256": used_file.sha256,
                    }
                ),
            }
        )
        call_sha256 = sha256(payload).hexdigest()
        if self._first_sha256 is None:
            self._first_sha256 = call_sha256
        self._final_sha256 = call_sha256
        self._digest.update(payload)
        self._digest.update(b"\n")
        self._requested_flags_counts[self._requested_flags] = (
            self._requested_flags_counts.get(self._requested_flags, 0) + 1
        )
        self._returned_flags_counts[returned_flags] = (
            self._returned_flags_counts.get(returned_flags, 0) + 1
        )
        self._returned_mode_bits_counts[returned_mode_bits] = (
            self._returned_mode_bits_counts.get(returned_mode_bits, 0) + 1
        )
        self._calculated_body_counts[body.value] = (
            self._calculated_body_counts.get(body.value, 0) + 1
        )
        if used_file is not None:
            file_key = (
                Path(used_file.path).name,
                used_file.sha256,
                used_file.size_bytes,
            )
            self._used_file_counts[file_key] = self._used_file_counts.get(file_key, 0) + 1

    def _set_entry_hashes(
        self,
        *,
        provider_configuration_sha256: str,
        ephemeris_file_set_sha256: str,
    ) -> None:
        self._entry_provider_configuration_sha256 = provider_configuration_sha256
        self._entry_ephemeris_file_set_sha256 = ephemeris_file_set_sha256

    def _set_exit_hashes(
        self,
        *,
        provider_configuration_sha256: str,
        ephemeris_file_set_sha256: str,
    ) -> None:
        self._exit_provider_configuration_sha256 = provider_configuration_sha256
        self._exit_ephemeris_file_set_sha256 = ephemeris_file_set_sha256

    def _close(self) -> None:
        self._closed = True

    def snapshot(self) -> SwissCalculationAuditSnapshot:
        """Return the deterministic trace summary after the context exits."""

        if not self._closed:
            raise RuntimeError("Swiss calculation audit is still active")
        if (
            self._entry_provider_configuration_sha256 is None
            or self._exit_provider_configuration_sha256 is None
            or self._entry_ephemeris_file_set_sha256 is None
            or self._exit_ephemeris_file_set_sha256 is None
        ):
            raise RuntimeError("Swiss calculation audit lacks bounded entry/exit hashes")
        return SwissCalculationAuditSnapshot(
            requested_flags=self._requested_flags,
            ephemeris_mask=self._ephemeris_mask,
            swieph_flag=self._swieph_flag,
            calculation_call_count=self._call_count,
            requested_flags_counts=tuple(sorted(self._requested_flags_counts.items())),
            returned_flags_counts=tuple(sorted(self._returned_flags_counts.items())),
            returned_mode_bits_counts=tuple(
                sorted(self._returned_mode_bits_counts.items())
            ),
            calculated_body_counts=tuple(sorted(self._calculated_body_counts.items())),
            used_file_counts=tuple(
                (*file_key, count)
                for file_key, count in sorted(self._used_file_counts.items())
            ),
            calculation_trace_sha256=self._digest.hexdigest(),
            first_calculation_sha256=self._first_sha256,
            final_calculation_sha256=self._final_sha256,
            entry_provider_configuration_sha256=(
                self._entry_provider_configuration_sha256
            ),
            exit_provider_configuration_sha256=(
                self._exit_provider_configuration_sha256
            ),
            entry_ephemeris_file_set_sha256=(
                self._entry_ephemeris_file_set_sha256
            ),
            exit_ephemeris_file_set_sha256=(
                self._exit_ephemeris_file_set_sha256
            ),
        )


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
        self._records_by_path = {Path(record.path): record for record in records}
        self._node_convention = node_convention
        self._requested_flags = int(self._swe.FLG_SWIEPH) | int(self._swe.FLG_SPEED)
        self._ephemeris_mask = _ephemeris_mask(self._swe)
        self._active_calculation_audit: SwissCalculationAuditCapture | None = None
        version = str(getattr(self._swe, "version", "unknown"))
        self._metadata = EphemerisMetadata(
            provider="swiss_ephemeris_local_files",
            library_version=version,
            files=tuple(records),
            calculation_flags=("SEFLG_SWIEPH", "SEFLG_SPEED", "geocentric", "tropical"),
            coordinate_frame="geocentric_apparent_tropical_ecliptic_of_date",
            node_convention=node_convention,
            ephemeris_path=str(root),
            requested_ephemeris=EphemerisMode.SWIEPH,
            requested_flags=self._requested_flags,
            ephemeris_mask=self._ephemeris_mask,
        )

    @property
    def metadata(self) -> EphemerisMetadata:
        return self._metadata

    def max_abs_speed_degrees_per_day(self, body: CelestialBody) -> float:
        return _MAX_SPEEDS[body]

    def min_solar_speed_degrees_per_day(self) -> float:
        return _MIN_SOLAR_SPEED

    def verify_declared_files_unchanged(self) -> None:
        """Re-hash the declared file set and fail if bytes changed in place.

        Construction-time hashes are provenance, not a permanent guarantee
        about mutable local files.  Long-running production boundary builds
        call this before and after enumeration so their evidence remains bound
        to the exact bytes recorded in :attr:`metadata`.
        """

        for record in self._metadata.files:
            path = Path(record.path)
            if not path.is_file():
                raise EphemerisConfigurationError(
                    f"declared ephemeris file disappeared after initialization: {path}"
                )
            current_size = path.stat().st_size
            current_sha256 = _sha256_file(path)
            if current_size != record.size_bytes or current_sha256 != record.sha256:
                raise EphemerisConfigurationError(
                    f"declared ephemeris file changed after initialization: {path}"
                )

    def verify_production_configuration(self) -> None:
        """Prove the static SWIEPH request and current declared-file binding.

        This preflight complements, but does not replace, the exact returned
        mask equality enforced inside every :meth:`position_with_provenance`
        call.
        """

        requested_mode_bits = self._requested_flags & self._ephemeris_mask
        expected = int(self._swe.FLG_SWIEPH)
        if requested_mode_bits != expected:
            raise EphemerisConfigurationError(
                "production provider request mask is not exactly SWIEPH: "
                f"requested mode bits={requested_mode_bits}, expected={expected}"
            )
        self.verify_declared_files_unchanged()

    def calculation_audit_identity_hashes(self) -> tuple[str, str]:
        """Return current path-free provider/file identities after byte checks."""

        self.verify_production_configuration()
        return self._audit_identity_hashes()

    @contextmanager
    def capture_calculation_audit(self) -> Iterator[SwissCalculationAuditCapture]:
        """Capture every direct Swiss return for one bounded production job.

        Captures deliberately cannot nest: overlapping traces would make it
        unclear which persisted receipt owns a calculation.  Returned flags are
        recorded before fail-closed mode validation, so an injected fallback is
        represented in the failed in-memory capture even though no passing
        receipt can be written.
        """

        if self._active_calculation_audit is not None:
            raise EphemerisConfigurationError(
                "Swiss calculation audit captures cannot be nested"
            )
        self.verify_production_configuration()
        entry_configuration_sha256, entry_file_set_sha256 = self._audit_identity_hashes()
        capture = SwissCalculationAuditCapture(
            requested_flags=self._requested_flags,
            ephemeris_mask=self._ephemeris_mask,
            swieph_flag=int(self._swe.FLG_SWIEPH),
        )
        capture._set_entry_hashes(
            provider_configuration_sha256=entry_configuration_sha256,
            ephemeris_file_set_sha256=entry_file_set_sha256,
        )
        self._active_calculation_audit = capture
        try:
            yield capture
        finally:
            try:
                self.verify_production_configuration()
                exit_configuration_sha256, exit_file_set_sha256 = (
                    self._audit_identity_hashes()
                )
                capture._set_exit_hashes(
                    provider_configuration_sha256=exit_configuration_sha256,
                    ephemeris_file_set_sha256=exit_file_set_sha256,
                )
            finally:
                capture._close()
                self._active_calculation_audit = None

    def position(self, body: CelestialBody, at_utc: datetime) -> EclipticPosition:
        return self.position_with_provenance(body, at_utc).position

    def position_with_provenance(
        self,
        body: CelestialBody,
        at_utc: datetime,
    ) -> PositionCalculation:
        """Calculate a position and retain exact returned-mode evidence."""

        at_utc = _require_utc(at_utc)
        if body is CelestialBody.EARTH:
            sun = self.position_with_provenance(CelestialBody.SUN, at_utc)
            return PositionCalculation(
                position=EclipticPosition(
                    (sun.position.longitude + 180.0) % 360.0,
                    sun.position.speed_degrees_per_day,
                ),
                provenance=replace(
                    sun.provenance,
                    requested_body=body,
                    derivation="opposition_of_sun",
                ),
            )
        if body is CelestialBody.SOUTH_NODE:
            north = self.position_with_provenance(CelestialBody.NORTH_NODE, at_utc)
            return PositionCalculation(
                position=EclipticPosition(
                    (north.position.longitude + 180.0) % 360.0,
                    north.position.speed_degrees_per_day,
                ),
                provenance=replace(
                    north.provenance,
                    requested_body=body,
                    derivation="opposition_of_north_node",
                ),
            )

        planet_id, file_index = self._planet_id_and_file_index(body)
        julian_day = _julian_day_ut(self._swe, at_utc)

        with _SWISS_LOCK:
            self._swe.set_ephe_path(str(self._root))
            values, returned_flags = self._swe.calc_ut(
                julian_day,
                planet_id,
                self._requested_flags,
            )
            returned_mode_bits = int(returned_flags) & self._ephemeris_mask
            if returned_mode_bits != int(self._swe.FLG_SWIEPH):
                audit = self._active_calculation_audit
                if audit is not None:
                    audit._record(
                        body=body,
                        at_utc=at_utc,
                        returned_flags=int(returned_flags),
                        used_file=None,
                        longitude=float(values[0]) % 360.0,
                        speed_degrees_per_day=float(values[3]),
                    )
                returned_label = _returned_mode_label(self._swe, returned_mode_bits)
                raise EphemerisFallbackError(
                    f"requested SWIEPH but calculation returned {returned_label} "
                    f"for {body.value} at {at_utc.isoformat()}; "
                    f"returned flags={returned_flags}, ephemeris mask={returned_mode_bits}"
                )
            used_file = self._verify_current_file(file_index, body, at_utc)
            audit = self._active_calculation_audit
            if audit is not None:
                audit._record(
                    body=body,
                    at_utc=at_utc,
                    returned_flags=int(returned_flags),
                    used_file=used_file,
                    longitude=float(values[0]) % 360.0,
                    speed_degrees_per_day=float(values[3]),
                )

        return PositionCalculation(
            position=EclipticPosition(float(values[0]) % 360.0, float(values[3])),
            provenance=EphemerisCalculationProvenance(
                requested_body=body,
                calculated_body=body,
                at_utc=at_utc,
                requested_mode=EphemerisMode.SWIEPH,
                returned_mode=EphemerisMode.SWIEPH,
                requested_flags=self._requested_flags,
                returned_flags=int(returned_flags),
                ephemeris_mask=self._ephemeris_mask,
                ephemeris_path=str(self._root),
                used_file=used_file,
            ),
        )

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

    def _audit_identity_hashes(self) -> tuple[str, str]:
        by_name = {Path(item.path).name: item for item in self._metadata.files}
        if set(by_name) != set(REQUIRED_EPHEMERIS_FILES):
            raise EphemerisConfigurationError(
                "Swiss audit requires exactly the canonical ephemeris file set"
            )
        path_free_files = [
            {
                "name": name,
                "sha256": by_name[name].sha256,
                "bytes": by_name[name].size_bytes,
            }
            for name in REQUIRED_EPHEMERIS_FILES
        ]
        file_set_sha256 = sha256(canonical_json_bytes(path_free_files)).hexdigest()
        configuration_sha256 = sha256(
            canonical_json_bytes(
                {
                    "calculation_flags": self._metadata.calculation_flags,
                    "coordinate_frame": self._metadata.coordinate_frame,
                    "ephemeris_file_set_sha256": file_set_sha256,
                    "ephemeris_mask": self._ephemeris_mask,
                    "library_version": self._metadata.library_version,
                    "node_convention": self._node_convention.value,
                    "provider": self._metadata.provider,
                    "requested_ephemeris": EphemerisMode.SWIEPH.value,
                    "requested_flags": self._requested_flags,
                    "schema_version": "swiss-provider-configuration-v1",
                    "swieph_flag": int(self._swe.FLG_SWIEPH),
                }
            )
        ).hexdigest()
        return configuration_sha256, file_set_sha256

    def _verify_current_file(
        self,
        file_index: int,
        body: CelestialBody,
        at_utc: datetime,
    ) -> EphemerisFile:
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
        return self._records_by_path[resolved]


def _ephemeris_mask(swe: ModuleType) -> int:
    """Resolve the ephemeris-mode mask across PySwissEph binding versions.

    PySwissEph 2.10.03 does not expose ``FLG_EPHMASK`` even though the C API
    defines the mask as JPLEPH | SWIEPH | MOSEPH.  Reconstructing that exact
    mask is therefore part of the production compatibility contract.
    """

    try:
        calculated = (
            int(swe.FLG_JPLEPH)
            | int(swe.FLG_SWIEPH)
            | int(swe.FLG_MOSEPH)
        )
    except AttributeError as exc:
        raise EphemerisConfigurationError(
            "Swiss binding lacks one or more ephemeris-mode flag constants"
        ) from exc
    exposed = getattr(swe, "FLG_EPHMASK", None)
    if exposed is not None and int(exposed) != calculated:
        raise EphemerisConfigurationError(
            "Swiss binding FLG_EPHMASK disagrees with JPLEPH|SWIEPH|MOSEPH"
        )
    return calculated


def _returned_mode_label(swe: ModuleType, mode_bits: int) -> str:
    labels = {
        int(swe.FLG_JPLEPH): EphemerisMode.JPLEPH.value,
        int(swe.FLG_SWIEPH): EphemerisMode.SWIEPH.value,
        int(swe.FLG_MOSEPH): f"{EphemerisMode.MOSEPH.value} (Moshier)",
    }
    return labels.get(mode_bits, f"UNKNOWN({mode_bits})")


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
