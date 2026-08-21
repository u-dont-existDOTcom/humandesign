"""Historical IANA civil-time resolution with explicit ambiguity handling."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from importlib import metadata
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


class TimezoneResolutionError(ValueError):
    """Base class for invalid local-time resolution requests."""


class NonexistentLocalTimeError(TimezoneResolutionError):
    """Raised when a wall-clock tuple falls in a forward offset jump."""


class AmbiguousLocalTimeError(TimezoneResolutionError):
    """Raised when a caller requires one UTC instant but does not choose a fold."""


class LocalTimeStatus(StrEnum):
    UNIQUE = "unique"
    AMBIGUOUS = "ambiguous"
    NONEXISTENT = "nonexistent"


@dataclass(frozen=True, slots=True)
class ResolvedInstant:
    """One round-trip-valid interpretation of a local wall-clock tuple."""

    fold: int
    local: datetime
    utc: datetime
    utc_offset: timedelta


@dataclass(frozen=True, slots=True)
class LocalTimeResolution:
    """All valid UTC interpretations of one supplied local tuple."""

    supplied_local: datetime
    iana_timezone: str
    status: LocalTimeStatus
    candidates: tuple[ResolvedInstant, ...]
    tzdb_version: str
    pre_standard_time_uncertain: bool

    def require_unique(self) -> ResolvedInstant:
        """Return the sole interpretation or raise a status-specific error."""

        if self.status is LocalTimeStatus.NONEXISTENT:
            raise NonexistentLocalTimeError(
                f"{self.supplied_local.isoformat()} does not exist in {self.iana_timezone}"
            )
        if self.status is LocalTimeStatus.AMBIGUOUS:
            raise AmbiguousLocalTimeError(
                f"{self.supplied_local.isoformat()} is ambiguous in {self.iana_timezone}; "
                "evaluate both folds or specify one"
            )
        return self.candidates[0]


def timezone_database_version() -> str:
    """Return the packaged or system IANA database version when discoverable."""

    try:
        return f"tzdata-{metadata.version('tzdata')}"
    except metadata.PackageNotFoundError:
        pass

    for path in (Path("/usr/share/zoneinfo/tzdata.zi"), Path("/usr/lib/zoneinfo/tzdata.zi")):
        try:
            first_line = path.read_text(encoding="utf-8", errors="replace").splitlines()[0]
        except (OSError, IndexError):
            continue
        if first_line.startswith("# version "):
            return f"system-{first_line.removeprefix('# version ').strip()}"
    return "system-unknown"


def resolve_local_datetime(
    supplied_local: datetime,
    iana_timezone: str,
    *,
    fold: int | None = None,
) -> LocalTimeResolution:
    """Resolve a naive civil tuple against historical IANA transition data.

    Unknown ambiguous folds return both candidates in UTC order.  Supplying a
    fold selects that candidate.  Nonexistent times return a result with no
    candidates; callers that require a single value can use ``require_unique``.
    Aware inputs are rejected so the exact original wall-clock tuple is never
    silently reinterpreted.
    """

    if supplied_local.tzinfo is not None:
        raise ValueError("supplied_local must be a naive wall-clock datetime")
    if fold not in (None, 0, 1):
        raise ValueError("fold must be None, 0, or 1")
    if not iana_timezone or "/" not in iana_timezone and iana_timezone != "UTC":
        raise ValueError("an explicit IANA timezone name is required")

    try:
        zone = ZoneInfo(iana_timezone)
    except ZoneInfoNotFoundError as exc:
        raise TimezoneResolutionError(f"unknown IANA timezone: {iana_timezone}") from exc

    possible: dict[datetime, ResolvedInstant] = {}
    folds = (fold,) if fold is not None else (0, 1)
    for candidate_fold in folds:
        aware = supplied_local.replace(tzinfo=zone, fold=candidate_fold)
        utc = aware.astimezone(UTC)
        round_trip = utc.astimezone(zone)
        if round_trip.replace(tzinfo=None) != supplied_local:
            continue
        # For a unique time ZoneInfo canonicalizes the round trip to fold=0.
        # Accept a requested fold=1 only when it denotes the same unique UTC
        # instant; distinct UTC values below are what establish ambiguity.
        offset = aware.utcoffset()
        if offset is None:
            continue
        possible.setdefault(
            utc,
            ResolvedInstant(
                fold=candidate_fold,
                local=aware,
                utc=utc,
                utc_offset=offset,
            ),
        )

    candidates = tuple(possible[key] for key in sorted(possible))
    if not candidates:
        status = LocalTimeStatus.NONEXISTENT
    elif len(candidates) == 1:
        status = LocalTimeStatus.UNIQUE
    else:
        status = LocalTimeStatus.AMBIGUOUS

    # zoneinfo intentionally exposes transition results, not a standardization
    # history API.  Flag pre-1900 tuples conservatively, and always flag local
    # mean-time-style second offsets.  This is a warning, not a correction.
    unusual_offset = any(item.utc_offset.total_seconds() % 60 != 0 for item in candidates)
    pre_standard_uncertain = supplied_local.year < 1900 or unusual_offset

    return LocalTimeResolution(
        supplied_local=supplied_local,
        iana_timezone=iana_timezone,
        status=status,
        candidates=candidates,
        tzdb_version=timezone_database_version(),
        pre_standard_time_uncertain=pre_standard_uncertain,
    )
