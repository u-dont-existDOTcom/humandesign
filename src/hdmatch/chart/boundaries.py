"""Event-based activation boundaries and stable chart-state intervals."""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any, TypeVar

from .calculator import StableChartFeatures, calculate_chart
from .design_moment import solve_design_moment
from .ephemeris import DEFAULT_ACTIVATION_BODIES, CelestialBody, EphemerisProvider
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


@dataclass(frozen=True, slots=True)
class BoundaryEvent:
    """A discrete activation change on the candidate-birth time axis."""

    at_utc: datetime
    ephemeris_utc: datetime
    side: str
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
    ephemeris_time_quantum_seconds: float = 41e-6,
) -> tuple[BoundaryEvent, ...]:
    """Enumerate Personality and Design activation transitions.

    Candidate scan steps are derived from each provider-declared maximum speed
    so a body moves at most one quarter of a requested sector per initial
    bracket.  Within brackets, a Lipschitz branch-and-bound search subdivides
    every interval that could contain a boundary even when its endpoints map to
    the same feature.  Thus endpoint equality is never used as proof that an
    interval is stable.
    """

    start = _require_utc(start_utc)
    end = _require_utc(end_utc)
    if end <= start:
        raise ValueError("boundary range must have positive duration")
    if (
        root_tolerance_seconds <= 0.0
        or max_scan_step_seconds <= 0.0
        or ephemeris_time_quantum_seconds <= 0.0
    ):
        raise ValueError("boundary tolerances and scan step must be positive")
    if len(set(bodies)) != len(bodies):
        raise ValueError("bodies must not contain duplicates")

    spacing = LINE_WIDTH_DEGREES if resolution is BoundaryResolution.LINE else GATE_WIDTH_DEGREES
    design_cache: dict[datetime, datetime] = {}

    def design_time(candidate_utc: datetime) -> datetime:
        try:
            return design_cache[candidate_utc]
        except KeyError:
            solved = solve_design_moment(
                provider,
                candidate_utc,
                time_tolerance_seconds=root_tolerance_seconds,
            ).design_utc
            design_cache[candidate_utc] = solved
            return solved

    events: list[BoundaryEvent] = []
    for side in ("personality", "design"):
        for body in bodies:
            if side == "personality":

                def longitude_at(at_utc: datetime, body: CelestialBody = body) -> float:
                    return provider.position(body, at_utc).longitude

                speed_bound = provider.max_abs_speed_degrees_per_day(body)
                absolute_position_uncertainty = (
                    speed_bound * ephemeris_time_quantum_seconds / 86400.0
                )
            else:

                def longitude_at(at_utc: datetime, body: CelestialBody = body) -> float:
                    return provider.position(body, design_time(at_utc)).longitude

                speed_bound = (
                    provider.max_abs_speed_degrees_per_day(body)
                    * provider.max_abs_speed_degrees_per_day(CelestialBody.SUN)
                    / provider.min_solar_speed_degrees_per_day()
                )
                absolute_position_uncertainty = (
                    provider.max_abs_speed_degrees_per_day(body)
                    * (root_tolerance_seconds + ephemeris_time_quantum_seconds)
                    / 86400.0
                )
            if speed_bound <= 0.0 or not math.isfinite(speed_bound):
                raise ValueError(f"invalid speed bound for {body.value}: {speed_bound}")

            roots = _enumerate_periodic_crossings(
                longitude_at,
                start,
                end,
                origin_degrees=RAVE_MANDALA_START_DEGREES,
                spacing_degrees=spacing,
                max_speed_degrees_per_day=speed_bound,
                absolute_position_uncertainty_degrees=absolute_position_uncertainty,
                root_tolerance_seconds=root_tolerance_seconds,
                max_scan_step_seconds=max_scan_step_seconds,
            )
            for root, boundary in roots:
                event = _make_event(
                    longitude_at,
                    design_time,
                    start,
                    end,
                    root,
                    boundary,
                    side,
                    body,
                    resolution,
                    root_tolerance_seconds,
                )
                if event is not None:
                    events.append(event)

    return tuple(
        sorted(
            _deduplicate_events(events, root_tolerance_seconds),
            key=lambda item: (item.at_utc, item.side, item.body.value),
        )
    )


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
) -> tuple[StableInterval, ...]:
    """Construct exact line-level stable intervals for the full chart vector."""

    events = enumerate_chart_boundaries(
        provider,
        start_utc,
        end_utc,
        bodies=bodies,
        resolution=BoundaryResolution.LINE,
        root_tolerance_seconds=root_tolerance_seconds,
    )

    def feature_at(at_utc: datetime) -> StableChartFeatures:
        return calculate_chart(
            provider,
            at_utc,
            bodies=bodies,
            design_time_tolerance_seconds=root_tolerance_seconds,
        ).stable_features

    return build_stable_intervals(start_utc, end_utc, events, feature_at)


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
    absolute_position_uncertainty_degrees: float,
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
            absolute_position_uncertainty_degrees,
            root_tolerance_seconds,
            roots,
        )
    roots.sort(key=lambda item: item[0])
    deduplicated: list[tuple[datetime, float]] = []
    for root in roots:
        if deduplicated and abs((root[0] - deduplicated[-1][0]).total_seconds()) <= (
            root_tolerance_seconds
        ):
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
    absolute_position_uncertainty_degrees: float,
    tolerance_seconds: float,
    roots: list[tuple[datetime, float]],
) -> None:
    duration = (right_time - left_time).total_seconds()
    reach = speed_per_second * duration + absolute_position_uncertainty_degrees
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
        absolute_position_uncertainty_degrees,
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
        absolute_position_uncertainty_degrees,
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


def _make_event(
    longitude_at: Callable[[datetime], float],
    design_time: Callable[[datetime], datetime],
    start: datetime,
    end: datetime,
    root: datetime,
    boundary: float,
    side: str,
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
    exact_root = _first_representable_feature_transition(
        longitude_at,
        before_time,
        after_time,
        before=(before.gate, before.line),
        after=(after.gate, after.line),
        resolution=resolution,
    )
    ephemeris_utc = exact_root if side == "personality" else design_time(exact_root)
    return BoundaryEvent(
        at_utc=exact_root,
        ephemeris_utc=ephemeris_utc,
        side=side,
        body=body,
        resolution=resolution,
        boundary_longitude=boundary,
        before_gate=before.gate,
        before_line=before.line,
        after_gate=after.gate,
        after_line=after.line,
        root_tolerance_seconds=tolerance,
    )


def _first_representable_feature_transition(
    longitude_at: Callable[[datetime], float],
    left: datetime,
    right: datetime,
    *,
    before: tuple[int, int],
    after: tuple[int, int],
    resolution: BoundaryResolution,
) -> datetime:
    """Return the first changed Python-datetime instant in a proven root bracket.

    The Lipschitz branch-and-bound search proves that every possible line or
    gate crossing is bracketed.  This final discrete bisection binds the public
    half-open interval boundary to the chart engine's one-microsecond datetime
    input quantum instead of exposing the midpoint of a floating root bracket.
    A third state inside the already isolated bracket is a proof failure and is
    rejected rather than silently sampled away.
    """

    quantum = timedelta(microseconds=1)

    def discrete_feature(at_utc: datetime) -> tuple[int, int]:
        value = longitude_to_gate_line(longitude_at(at_utc))
        if resolution is BoundaryResolution.GATE:
            return value.gate, 0
        return value.gate, value.line

    before_key = (before[0], 0) if resolution is BoundaryResolution.GATE else before
    after_key = (after[0], 0) if resolution is BoundaryResolution.GATE else after
    if discrete_feature(left) != before_key or discrete_feature(right) != after_key:
        raise ValueError("boundary bracket endpoints do not match declared adjacent states")

    while right - left > quantum:
        span_microseconds = (right - left) // quantum
        midpoint = left + quantum * (span_microseconds // 2)
        midpoint_key = discrete_feature(midpoint)
        if midpoint_key == before_key:
            left = midpoint
        elif midpoint_key == after_key:
            right = midpoint
        else:
            raise ValueError("multiple feature transitions occurred inside one boundary bracket")
    return right


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
