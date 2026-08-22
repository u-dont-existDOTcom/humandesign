"""Event-based activation boundaries and stable chart-state intervals."""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass, replace
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from pathlib import Path
from typing import Any, Final, Literal, TypeAlias, TypeVar

from .calculator import StableChartFeatures, calculate_chart
from .design_moment import solve_design_moment, solve_personality_moment_from_design
from .ephemeris import (
    DEFAULT_ACTIVATION_BODIES,
    CelestialBody,
    EphemerisConfigurationError,
    EphemerisMode,
    EphemerisProvider,
    SwissEphemerisProvider,
)
from .rave_mandala import (
    GATE_WIDTH_DEGREES,
    LINE_WIDTH_DEGREES,
    RAVE_MANDALA_START_DEGREES,
    longitude_to_gate_line,
)
from .validation import canonical_sha256


class BoundaryResolution(StrEnum):
    GATE = "gate"
    LINE = "line"


class BoundarySearchError(RuntimeError):
    """Base error for fail-closed exact boundary enumeration."""


class BoundaryCompletenessError(BoundarySearchError):
    """Raised when a provider violates a bound required for completeness."""


class BoundaryProvenanceError(BoundarySearchError):
    """Raised when production enumeration lacks verified SWIEPH provenance."""


BoundarySide: TypeAlias = Literal["personality", "design"]
BOUNDARY_POLICY_VERSION: Final[str] = "exact-gate-line-boundaries-v2"


@dataclass(frozen=True, slots=True)
class BoundaryEvent:
    """A discrete activation change on the candidate-birth time axis."""

    at_utc: datetime
    ephemeris_utc: datetime
    side: BoundarySide
    body: CelestialBody
    resolution: BoundaryResolution
    boundary_longitude: float
    before_gate: int
    before_line: int
    after_gate: int
    after_line: int
    root_tolerance_seconds: float


T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class StableInterval:
    """A half-open interval whose complete discrete feature vector is stable."""

    start_utc: datetime
    end_utc: datetime
    representative_utc: datetime
    feature_sha256: str
    features: Any
    boundary_events: tuple[BoundaryEvent, ...]

    @property
    def duration_seconds(self) -> float:
        return (self.end_utc - self.start_utc).total_seconds()


def enumerate_chart_boundaries(
    provider: EphemerisProvider,
    start_utc: datetime,
    end_utc: datetime,
    *,
    bodies: tuple[CelestialBody, ...] = DEFAULT_ACTIVATION_BODIES,
    resolution: BoundaryResolution = BoundaryResolution.LINE,
    root_tolerance_seconds: float = 0.01,
    max_scan_step_seconds: float = 6 * 3600.0,
    event_group_tolerance_seconds: float | None = None,
    require_swieph_provenance: bool = False,
) -> tuple[BoundaryEvent, ...]:
    """Enumerate Personality and Design activation transitions.

    Personality boundaries are solved directly on the birth timeline.  Design
    boundaries are solved directly on the exact Design ephemeris horizon and
    then mapped to birth time by inverting the 88-degree solar-arc equation.
    Candidate scan steps use provider-declared speed bounds, and a Lipschitz
    branch-and-bound search subdivides every interval that could contain a
    crossing even when its endpoints map to the same feature.  Endpoint
    equality is therefore never used as proof that an interval is stable.
    """

    start = _require_utc(start_utc)
    end = _require_utc(end_utc)
    if end <= start:
        raise ValueError("boundary range must have positive duration")
    if (
        root_tolerance_seconds <= 0.0
        or max_scan_step_seconds <= 0.0
        or not math.isfinite(root_tolerance_seconds)
        or not math.isfinite(max_scan_step_seconds)
    ):
        raise ValueError("boundary tolerances and scan step must be positive")
    group_tolerance = (
        root_tolerance_seconds
        if event_group_tolerance_seconds is None
        else event_group_tolerance_seconds
    )
    if not math.isfinite(group_tolerance) or group_tolerance < root_tolerance_seconds:
        raise ValueError("event grouping tolerance must be at least the root tolerance")
    if len(set(bodies)) != len(bodies):
        raise ValueError("bodies must not contain duplicates")
    if require_swieph_provenance:
        _verify_production_provider(provider)

    spacing = LINE_WIDTH_DEGREES if resolution is BoundaryResolution.LINE else GATE_WIDTH_DEGREES
    design_cache: dict[datetime, datetime] = {}
    personality_cache: dict[datetime, datetime] = {}

    def design_time(candidate_utc: datetime) -> datetime:
        try:
            return design_cache[candidate_utc]
        except KeyError:
            birth_sun = provider.position(CelestialBody.SUN, candidate_utc)
            _validate_solar_speed(provider, birth_sun.speed_degrees_per_day, candidate_utc)
            solved = solve_design_moment(
                provider,
                candidate_utc,
                time_tolerance_seconds=root_tolerance_seconds,
            )
            design_sun = provider.position(CelestialBody.SUN, solved.design_utc)
            _validate_solar_speed(
                provider,
                design_sun.speed_degrees_per_day,
                solved.design_utc,
            )
            design_cache[candidate_utc] = solved.design_utc
            return solved.design_utc

    def personality_time(design_utc: datetime) -> datetime:
        try:
            return personality_cache[design_utc]
        except KeyError:
            design_sun = provider.position(CelestialBody.SUN, design_utc)
            _validate_solar_speed(provider, design_sun.speed_degrees_per_day, design_utc)
            solved = solve_personality_moment_from_design(
                provider,
                design_utc,
                time_tolerance_seconds=root_tolerance_seconds,
            )
            birth_sun = provider.position(CelestialBody.SUN, solved.birth_utc)
            _validate_solar_speed(
                provider,
                birth_sun.speed_degrees_per_day,
                solved.birth_utc,
            )
            personality_cache[design_utc] = solved.birth_utc
            return solved.birth_utc

    design_start = design_time(start)
    design_end = design_time(end)
    if design_end <= design_start:
        raise BoundaryCompletenessError(
            "exact Design timeline is not strictly increasing across the requested range"
        )

    events: list[BoundaryEvent] = []
    for side in ("personality", "design"):
        for body in bodies:
            body_speed_bound = provider.max_abs_speed_degrees_per_day(body)
            _validate_speed_bound(body, body_speed_bound)
            scan_longitude_at: Callable[[datetime], float]
            if side == "personality":

                def longitude_at(
                    at_utc: datetime,
                    body: CelestialBody = body,
                    declared_speed_bound: float = body_speed_bound,
                ) -> float:
                    return _bounded_longitude(
                        provider,
                        body,
                        at_utc,
                        declared_speed_bound,
                    )

                speed_bound = body_speed_bound
                scan_start = start
                scan_end = end
                scan_longitude_at = longitude_at
            else:

                def design_longitude_at(
                    ephemeris_utc: datetime,
                    body: CelestialBody = body,
                    declared_speed_bound: float = body_speed_bound,
                ) -> float:
                    return _bounded_longitude(
                        provider,
                        body,
                        ephemeris_utc,
                        declared_speed_bound,
                    )

                def longitude_at(
                    at_utc: datetime,
                    body: CelestialBody = body,
                    declared_speed_bound: float = body_speed_bound,
                ) -> float:
                    return _bounded_longitude(
                        provider,
                        body,
                        design_time(at_utc),
                        declared_speed_bound,
                    )

                speed_bound = body_speed_bound
                scan_start = design_start
                scan_end = design_end
                scan_longitude_at = design_longitude_at
            if speed_bound <= 0.0 or not math.isfinite(speed_bound):
                raise ValueError(f"invalid speed bound for {body.value}: {speed_bound}")

            roots = _enumerate_periodic_crossings(
                scan_longitude_at,
                scan_start,
                scan_end,
                origin_degrees=RAVE_MANDALA_START_DEGREES,
                spacing_degrees=spacing,
                max_speed_degrees_per_day=speed_bound,
                root_tolerance_seconds=root_tolerance_seconds,
                max_scan_step_seconds=max_scan_step_seconds,
            )
            for ephemeris_root, boundary in roots:
                root = (
                    ephemeris_root
                    if side == "personality"
                    else personality_time(ephemeris_root)
                )
                if not start < root < end:
                    continue
                if side == "personality":
                    event = _make_personality_event(
                        longitude_at,
                        start,
                        end,
                        root,
                        boundary,
                        body,
                        resolution,
                        root_tolerance_seconds,
                    )
                else:
                    event = _make_design_event(
                        design_longitude_at,
                        design_start,
                        design_end,
                        root,
                        ephemeris_root,
                        boundary,
                        body,
                        resolution,
                        root_tolerance_seconds,
                    )
                if event is not None:
                    events.append(event)

    grouped = _group_simultaneous_events(
        _deduplicate_events(events, root_tolerance_seconds),
        group_tolerance,
        design_time,
    )
    if require_swieph_provenance:
        _verify_production_provider(provider)
    return grouped


def build_stable_intervals(
    start_utc: datetime,
    end_utc: datetime,
    events: tuple[BoundaryEvent, ...],
    feature_at: Callable[[datetime], T],
) -> tuple[StableInterval, ...]:
    """Evaluate interval midpoints and merge only identical complete vectors."""

    start = _require_utc(start_utc)
    end = _require_utc(end_utc)
    if end <= start:
        raise ValueError("stable interval range must have positive duration")
    relevant_events = tuple(event for event in events if start < event.at_utc < end)
    cuts = (start, *sorted({event.at_utc for event in relevant_events}), end)
    intervals: list[StableInterval] = []
    for left, right in zip(cuts, cuts[1:], strict=False):
        if right <= left:
            continue
        representative = left + (right - left) / 2
        features = feature_at(representative)
        feature_hash = canonical_sha256(features)
        ending_events = tuple(event for event in relevant_events if event.at_utc == right)
        current = StableInterval(
            start_utc=left,
            end_utc=right,
            representative_utc=representative,
            feature_sha256=feature_hash,
            features=features,
            boundary_events=ending_events,
        )
        if intervals and intervals[-1].feature_sha256 == current.feature_sha256:
            previous = intervals.pop()
            intervals.append(
                StableInterval(
                    start_utc=previous.start_utc,
                    end_utc=current.end_utc,
                    representative_utc=previous.start_utc
                    + (current.end_utc - previous.start_utc) / 2,
                    feature_sha256=current.feature_sha256,
                    features=current.features,
                    boundary_events=previous.boundary_events + current.boundary_events,
                )
            )
        else:
            intervals.append(current)
    audit_interval_partition(tuple(intervals), start, end)
    return tuple(intervals)


def build_chart_state_intervals(
    provider: EphemerisProvider,
    start_utc: datetime,
    end_utc: datetime,
    *,
    bodies: tuple[CelestialBody, ...] = DEFAULT_ACTIVATION_BODIES,
    root_tolerance_seconds: float = 0.01,
    event_group_tolerance_seconds: float | None = None,
    require_swieph_provenance: bool = False,
) -> tuple[StableInterval, ...]:
    """Construct exact line-level stable intervals for the full chart vector."""

    events = enumerate_chart_boundaries(
        provider,
        start_utc,
        end_utc,
        bodies=bodies,
        resolution=BoundaryResolution.LINE,
        root_tolerance_seconds=root_tolerance_seconds,
        event_group_tolerance_seconds=event_group_tolerance_seconds,
        require_swieph_provenance=require_swieph_provenance,
    )

    def feature_at(at_utc: datetime) -> StableChartFeatures:
        return calculate_chart(
            provider,
            at_utc,
            bodies=bodies,
            design_time_tolerance_seconds=root_tolerance_seconds,
        ).stable_features

    return build_stable_intervals(start_utc, end_utc, events, feature_at)


def build_production_chart_state_intervals(
    provider: SwissEphemerisProvider,
    start_utc: datetime,
    end_utc: datetime,
    *,
    bodies: tuple[CelestialBody, ...] = DEFAULT_ACTIVATION_BODIES,
    root_tolerance_seconds: float = 0.01,
) -> tuple[StableInterval, ...]:
    """Canonical SWIEPH-only entrypoint with grouping frozen to root tolerance."""

    return build_chart_state_intervals(
        provider,
        start_utc,
        end_utc,
        bodies=bodies,
        root_tolerance_seconds=root_tolerance_seconds,
        event_group_tolerance_seconds=root_tolerance_seconds,
        require_swieph_provenance=True,
    )


def audit_interval_partition(
    intervals: tuple[StableInterval, ...],
    expected_start_utc: datetime,
    expected_end_utc: datetime,
) -> None:
    """Raise if intervals contain gaps, overlaps, or identical adjacent states."""

    expected_start = _require_utc(expected_start_utc)
    expected_end = _require_utc(expected_end_utc)
    if not intervals:
        raise ValueError("interval partition must not be empty")
    if intervals[0].start_utc != expected_start or intervals[-1].end_utc != expected_end:
        raise ValueError("interval partition does not cover the requested range")
    for previous, current in zip(intervals, intervals[1:], strict=False):
        if previous.end_utc != current.start_utc:
            raise ValueError("interval partition has a gap or overlap")
        if previous.feature_sha256 == current.feature_sha256:
            raise ValueError("identical adjacent intervals must be merged")
    if any(item.end_utc <= item.start_utc for item in intervals):
        raise ValueError("interval partition contains a non-positive interval")


def _enumerate_periodic_crossings(
    longitude_at: Callable[[datetime], float],
    start: datetime,
    end: datetime,
    *,
    origin_degrees: float,
    spacing_degrees: float,
    max_speed_degrees_per_day: float,
    root_tolerance_seconds: float,
    max_scan_step_seconds: float,
) -> tuple[tuple[datetime, float], ...]:
    speed_per_second = max_speed_degrees_per_day / 86400.0
    safe_step = spacing_degrees / (4.0 * speed_per_second)
    scan_step = min(max_scan_step_seconds, safe_step)
    knots: list[tuple[datetime, float]] = []
    current = start
    raw = longitude_at(current) % 360.0
    unwrapped = raw
    knots.append((current, unwrapped))
    while current < end:
        following = min(end, current + timedelta(seconds=scan_step))
        following_raw = longitude_at(following) % 360.0
        unwrapped += _signed_angular_delta(raw, following_raw)
        knots.append((following, unwrapped))
        current, raw = following, following_raw

    roots: list[tuple[datetime, float]] = []
    for (left_time, left_value), (right_time, right_value) in zip(knots, knots[1:], strict=False):
        _search_possible_crossings(
            longitude_at,
            left_time,
            right_time,
            left_value,
            right_value,
            origin_degrees,
            spacing_degrees,
            speed_per_second,
            root_tolerance_seconds,
            roots,
        )
    roots.sort(key=lambda item: item[0])
    deduplicated: list[tuple[datetime, float]] = []
    for root in roots:
        if deduplicated:
            previous = deduplicated[-1]
            close = abs((root[0] - previous[0]).total_seconds()) <= root_tolerance_seconds
            same_boundary = math.isclose(root[1], previous[1], abs_tol=1e-10)
            if close and same_boundary:
                continue
        if start < root[0] < end:
            deduplicated.append(root)
    return tuple(deduplicated)


def _search_possible_crossings(
    longitude_at: Callable[[datetime], float],
    left_time: datetime,
    right_time: datetime,
    left_value: float,
    right_value: float,
    origin: float,
    spacing: float,
    speed_per_second: float,
    tolerance_seconds: float,
    roots: list[tuple[datetime, float]],
) -> None:
    duration = (right_time - left_time).total_seconds()
    reach = speed_per_second * duration
    possible_low = max(left_value - reach, right_value - reach)
    possible_high = min(left_value + reach, right_value + reach)
    levels = _levels_between(origin, spacing, possible_low, possible_high)
    if not levels:
        return

    if duration <= tolerance_seconds:
        for level in levels:
            left_delta = left_value - level
            right_delta = right_value - level
            if left_delta == 0.0 or right_delta == 0.0 or left_delta * right_delta < 0.0:
                root = _bisect_level(
                    longitude_at,
                    left_time,
                    right_time,
                    left_value,
                    right_value,
                    level,
                    tolerance_seconds,
                )
                roots.append((root, level % 360.0))
        return

    midpoint = left_time + (right_time - left_time) / 2
    raw_midpoint = longitude_at(midpoint) % 360.0
    midpoint_value = _unwrap_near(raw_midpoint, (left_value + right_value) / 2.0)
    _search_possible_crossings(
        longitude_at,
        left_time,
        midpoint,
        left_value,
        midpoint_value,
        origin,
        spacing,
        speed_per_second,
        tolerance_seconds,
        roots,
    )
    _search_possible_crossings(
        longitude_at,
        midpoint,
        right_time,
        midpoint_value,
        right_value,
        origin,
        spacing,
        speed_per_second,
        tolerance_seconds,
        roots,
    )


def _bisect_level(
    longitude_at: Callable[[datetime], float],
    left_time: datetime,
    right_time: datetime,
    left_value: float,
    right_value: float,
    level: float,
    tolerance_seconds: float,
) -> datetime:
    if left_value == level:
        return left_time
    if right_value == level:
        return right_time
    left_delta = left_value - level
    right_delta = right_value - level
    if left_delta * right_delta > 0.0:
        raise ValueError("root bisection requires a sign-changing bracket")
    while (right_time - left_time).total_seconds() > tolerance_seconds:
        midpoint = left_time + (right_time - left_time) / 2
        raw = longitude_at(midpoint) % 360.0
        midpoint_value = _unwrap_near(raw, (left_value + right_value) / 2.0)
        midpoint_delta = midpoint_value - level
        if midpoint_delta == 0.0:
            return midpoint
        if left_delta * midpoint_delta <= 0.0:
            right_time, right_value, right_delta = midpoint, midpoint_value, midpoint_delta
        else:
            left_time, left_value, left_delta = midpoint, midpoint_value, midpoint_delta
    return left_time + (right_time - left_time) / 2


def _make_personality_event(
    longitude_at: Callable[[datetime], float],
    start: datetime,
    end: datetime,
    root: datetime,
    boundary: float,
    body: CelestialBody,
    resolution: BoundaryResolution,
    tolerance: float,
) -> BoundaryEvent | None:
    probe_seconds = max(1.0, tolerance * 4.0)
    before_time = max(start, root - timedelta(seconds=probe_seconds))
    after_time = min(end, root + timedelta(seconds=probe_seconds))
    before = longitude_to_gate_line(longitude_at(before_time))
    after = longitude_to_gate_line(longitude_at(after_time))
    if resolution is BoundaryResolution.LINE:
        changed = (before.gate, before.line) != (after.gate, after.line)
    else:
        changed = before.gate != after.gate
    if not changed:
        return None
    return BoundaryEvent(
        at_utc=root,
        ephemeris_utc=root,
        side="personality",
        body=body,
        resolution=resolution,
        boundary_longitude=boundary,
        before_gate=before.gate,
        before_line=before.line,
        after_gate=after.gate,
        after_line=after.line,
        root_tolerance_seconds=tolerance,
    )


def _make_design_event(
    design_longitude_at: Callable[[datetime], float],
    design_start: datetime,
    design_end: datetime,
    personality_root: datetime,
    design_root: datetime,
    boundary: float,
    body: CelestialBody,
    resolution: BoundaryResolution,
    tolerance: float,
) -> BoundaryEvent | None:
    """Create a birth-axis event from a directly solved Design crossing."""

    probe_seconds = max(1.0, tolerance * 4.0)
    before_time = max(design_start, design_root - timedelta(seconds=probe_seconds))
    after_time = min(design_end, design_root + timedelta(seconds=probe_seconds))
    before = longitude_to_gate_line(design_longitude_at(before_time))
    after = longitude_to_gate_line(design_longitude_at(after_time))
    if resolution is BoundaryResolution.LINE:
        changed = (before.gate, before.line) != (after.gate, after.line)
    else:
        changed = before.gate != after.gate
    if not changed:
        return None
    return BoundaryEvent(
        at_utc=personality_root,
        ephemeris_utc=design_root,
        side="design",
        body=body,
        resolution=resolution,
        boundary_longitude=boundary,
        before_gate=before.gate,
        before_line=before.line,
        after_gate=after.gate,
        after_line=after.line,
        root_tolerance_seconds=tolerance,
    )


def _deduplicate_events(
    events: list[BoundaryEvent],
    tolerance_seconds: float,
) -> tuple[BoundaryEvent, ...]:
    ordered = sorted(events, key=lambda item: (item.side, item.body.value, item.at_utc))
    result: list[BoundaryEvent] = []
    for event in ordered:
        if result:
            previous = result[-1]
            same_series = previous.side == event.side and previous.body is event.body
            same_boundary = math.isclose(
                previous.boundary_longitude,
                event.boundary_longitude,
                abs_tol=1e-10,
            )
            close = abs((previous.at_utc - event.at_utc).total_seconds()) <= tolerance_seconds
            if same_series and same_boundary and close:
                continue
        result.append(event)
    return tuple(result)


def _group_simultaneous_events(
    events: tuple[BoundaryEvent, ...],
    tolerance_seconds: float,
    design_time: Callable[[datetime], datetime],
) -> tuple[BoundaryEvent, ...]:
    """Assign one deterministic cut to events unresolved within tolerance.

    Independent root solves for genuinely simultaneous structures (notably
    Sun/Earth and the two Nodes) may differ by microseconds.  Treating those
    estimates as separate cuts would manufacture non-physical sliver states.
    Groups use a bounded diameter rather than transitive chaining, and their
    canonical timestamp is the midpoint of the earliest/latest estimates.
    """

    ordered = sorted(
        events,
        key=lambda item: (
            item.at_utc,
            item.side,
            item.body.value,
            item.resolution.value,
            item.boundary_longitude,
        ),
    )
    clusters: list[list[BoundaryEvent]] = []
    for event in ordered:
        if not clusters:
            clusters.append([event])
            continue
        first = clusters[-1][0]
        if (event.at_utc - first.at_utc).total_seconds() <= tolerance_seconds:
            clusters[-1].append(event)
        else:
            clusters.append([event])

    grouped: list[BoundaryEvent] = []
    for cluster in clusters:
        first_at = cluster[0].at_utc
        last_at = cluster[-1].at_utc
        canonical_at = first_at + (last_at - first_at) / 2
        canonical_design_at: datetime | None = None
        if any(item.side == "design" for item in cluster):
            canonical_design_at = design_time(canonical_at)
        for event in cluster:
            ephemeris_utc = (
                canonical_at
                if event.side == "personality"
                else _require_design_time(canonical_design_at)
            )
            grouped.append(
                replace(
                    event,
                    at_utc=canonical_at,
                    ephemeris_utc=ephemeris_utc,
                )
            )
    return tuple(
        sorted(
            grouped,
            key=lambda item: (
                item.at_utc,
                item.side,
                item.body.value,
                item.resolution.value,
                item.boundary_longitude,
            ),
        )
    )


def _require_design_time(value: datetime | None) -> datetime:
    if value is None:  # pragma: no cover - guarded by caller's side check
        raise BoundarySearchError("grouped Design event lacks an exact Design timestamp")
    return value


def _validate_speed_bound(body: CelestialBody, speed_bound: float) -> None:
    if speed_bound <= 0.0 or not math.isfinite(speed_bound):
        raise BoundaryCompletenessError(
            f"invalid completeness speed bound for {body.value}: {speed_bound}"
        )


def _bounded_longitude(
    provider: EphemerisProvider,
    body: CelestialBody,
    at_utc: datetime,
    declared_speed_bound: float,
) -> float:
    position = provider.position(body, at_utc)
    observed = position.speed_degrees_per_day
    if not math.isfinite(observed):
        raise BoundaryCompletenessError(
            f"non-finite observed speed for {body.value} at {at_utc.isoformat()}"
        )
    if abs(observed) > declared_speed_bound + 1e-10:
        raise BoundaryCompletenessError(
            f"observed speed exceeds declared completeness bound for {body.value} "
            f"at {at_utc.isoformat()}: observed={observed}, bound={declared_speed_bound}"
        )
    return position.longitude


def _validate_solar_speed(
    provider: EphemerisProvider,
    observed_speed: float,
    at_utc: datetime,
) -> None:
    maximum = provider.max_abs_speed_degrees_per_day(CelestialBody.SUN)
    minimum = provider.min_solar_speed_degrees_per_day()
    _validate_speed_bound(CelestialBody.SUN, maximum)
    if minimum <= 0.0 or not math.isfinite(minimum) or minimum > maximum:
        raise BoundaryCompletenessError(
            f"invalid solar speed bounds for Design mapping: min={minimum}, max={maximum}"
        )
    if not math.isfinite(observed_speed) or not (
        minimum - 1e-10 <= observed_speed <= maximum + 1e-10
    ):
        raise BoundaryCompletenessError(
            f"observed solar speed violates Design completeness bounds at "
            f"{at_utc.isoformat()}: observed={observed_speed}, min={minimum}, max={maximum}"
        )


def _verify_production_provider(provider: EphemerisProvider) -> None:
    if not isinstance(provider, SwissEphemerisProvider):
        raise BoundaryProvenanceError(
            "production boundary enumeration requires SwissEphemerisProvider"
        )
    metadata = provider.metadata
    if (
        metadata.requested_ephemeris is not EphemerisMode.SWIEPH
        or metadata.requested_flags is None
        or metadata.ephemeris_mask is None
    ):
        raise BoundaryProvenanceError(
            "production boundary enumeration lacks an explicit SWIEPH request"
        )
    names = {Path(item.path).name for item in metadata.files}
    required = {"sepl_18.se1", "semo_18.se1"}
    if not required.issubset(names):
        raise BoundaryProvenanceError(
            "production boundary enumeration requires sepl_18.se1 and semo_18.se1"
        )
    try:
        provider.verify_production_configuration()
    except EphemerisConfigurationError as exc:
        raise BoundaryProvenanceError(str(exc)) from exc


def _levels_between(origin: float, spacing: float, low: float, high: float) -> tuple[float, ...]:
    if high < low:
        return ()
    first = math.ceil((low - origin) / spacing - 1e-12)
    last = math.floor((high - origin) / spacing + 1e-12)
    return tuple(origin + index * spacing for index in range(first, last + 1))


def _signed_angular_delta(previous: float, following: float) -> float:
    return (following - previous + 180.0) % 360.0 - 180.0


def _unwrap_near(raw: float, reference: float) -> float:
    return raw + 360.0 * round((reference - raw) / 360.0)


def _require_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("boundary timestamps must be timezone-aware")
    return value.astimezone(UTC)
