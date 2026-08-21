"""Exact stable-interval ranking for known-date time rectification.

This module is deliberately blind: it accepts candidate states and their already
computed scores, but no answer key or case secret.  A revealed UTC instant can be
located only through the separate :func:`identify_revealed_interval` helper.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from fractions import Fraction

from hdmatch.schemas import CandidateState, ScoredState
from hdmatch.search.candidate_universe import (
    local_date_utc_bounds,
    split_interval_by_local_date,
)

_OVERLAP_SECONDS_TOLERANCE = 1e-6


@dataclass(frozen=True)
class RankedStableInterval:
    """One exact chart-stable interval in a known-date ranking.

    ``start_utc`` and ``end_utc`` retain the full source interval.  A source
    interval may cross a civil-date boundary, so the separately reported
    ``eligible_*`` bounds are its exact intersection with the declared date.
    Every interval is half-open: ``[start, end)``.
    """

    state_id: str
    start_utc: datetime
    end_utc: datetime
    eligible_start_utc: datetime
    eligible_end_utc: datetime
    stable_width: timedelta
    eligible_width: timedelta
    score: ScoredState
    rank_start: int
    rank_end: int

    @property
    def tied(self) -> bool:
        """Whether this interval shares its exact score with another interval."""

        return self.rank_end > self.rank_start

    @property
    def midrank(self) -> Fraction:
        """Return the exact midrank without floating-point rounding."""

        return Fraction(self.rank_start + self.rank_end, 2)


@dataclass(frozen=True)
class RankedIntervalGroup:
    """Intervals sharing exactly the same net rubric-bit score."""

    net_rubric_bits: float
    rank_start: int
    rank_end: int
    intervals: tuple[RankedStableInterval, ...]

    @property
    def tied(self) -> bool:
        return len(self.intervals) > 1

    @property
    def midrank(self) -> Fraction:
        return Fraction(self.rank_start + self.rank_end, 2)


@dataclass(frozen=True)
class KnownDateIntervalRanking:
    """Complete, validated ranking for one local civil date."""

    local_date: date
    timezone_name: str
    date_start_utc: datetime
    date_end_utc: datetime
    groups: tuple[RankedIntervalGroup, ...]

    @property
    def records(self) -> tuple[RankedStableInterval, ...]:
        """Flatten score-ordered groups into deterministic ranking order."""

        return tuple(interval for group in self.groups for interval in group.intervals)

    @property
    def chronological_records(self) -> tuple[RankedStableInterval, ...]:
        """Return the same records ordered by their date-eligible bounds."""

        return tuple(
            sorted(
                self.records,
                key=lambda item: (
                    item.eligible_start_utc,
                    item.eligible_end_utc,
                    item.state_id,
                ),
            )
        )


@dataclass(frozen=True)
class RevealedIntervalIdentification:
    """Post-reveal identification of the stable interval containing truth."""

    true_utc: datetime
    interval: RankedStableInterval


@dataclass(frozen=True)
class _EligibleState:
    state: CandidateState
    start_utc: datetime
    end_utc: datetime
    eligible_start_utc: datetime
    eligible_end_utc: datetime
    score: ScoredState


def _as_utc(value: datetime, label: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{label} must be timezone-aware")
    return value.astimezone(UTC)


def _validate_overlap_metadata(
    state: CandidateState,
    start_utc: datetime,
    end_utc: datetime,
    timezone_name: str,
) -> None:
    expected = split_interval_by_local_date(start_utc, end_utc, timezone_name)
    actual_by_date: dict[date, float] = {}
    for overlap in state.local_date_overlaps:
        if overlap.date in actual_by_date:
            raise ValueError(
                f"state {state.state_id} repeats local-date overlap {overlap.date}"
            )
        actual_by_date[overlap.date] = overlap.seconds
    expected_by_date = {overlap.date: overlap.seconds for overlap in expected}
    if actual_by_date.keys() != expected_by_date.keys():
        raise ValueError(
            f"state {state.state_id} local-date metadata does not match timezone "
            f"{timezone_name}"
        )
    for local_day, expected_seconds in expected_by_date.items():
        if abs(actual_by_date[local_day] - expected_seconds) > _OVERLAP_SECONDS_TOLERANCE:
            raise ValueError(
                f"state {state.state_id} has incorrect overlap seconds for {local_day}"
            )


def _validated_eligible_states(
    states: Iterable[CandidateState],
    scores: Mapping[str, ScoredState],
    local_day: date,
    timezone_name: str,
) -> tuple[datetime, datetime, tuple[_EligibleState, ...]]:
    date_start_utc, date_end_utc = local_date_utc_bounds(local_day, timezone_name)
    materialized = tuple(states)
    if not materialized:
        raise ValueError("known-date candidate universe must not be empty")

    state_ids = [state.state_id for state in materialized]
    if len(set(state_ids)) != len(state_ids):
        raise ValueError("known-date candidate universe contains duplicate state IDs")

    expected_score_ids = set(state_ids)
    actual_score_ids = set(scores)
    missing = sorted(expected_score_ids - actual_score_ids)
    if missing:
        raise ValueError(f"missing scores for states: {', '.join(missing)}")
    extra = sorted(actual_score_ids - expected_score_ids)
    if extra:
        raise ValueError(f"scores contain unknown or wrong-date states: {', '.join(extra)}")

    eligible: list[_EligibleState] = []
    for state in materialized:
        start_utc = _as_utc(state.start_utc, f"state {state.state_id} start_utc")
        end_utc = _as_utc(state.end_utc, f"state {state.state_id} end_utc")
        _validate_overlap_metadata(state, start_utc, end_utc, timezone_name)

        eligible_start = max(start_utc, date_start_utc)
        eligible_end = min(end_utc, date_end_utc)
        if eligible_end <= eligible_start:
            raise ValueError(
                f"state {state.state_id} does not intersect declared local date {local_day}"
            )
        if not any(overlap.date == local_day for overlap in state.local_date_overlaps):
            raise ValueError(
                f"state {state.state_id} has no overlap for declared local date {local_day}"
            )

        score = scores[state.state_id]
        if score.state_id != state.state_id:
            raise ValueError(
                f"score key {state.state_id} contains score for state {score.state_id}"
            )
        if not math.isfinite(score.net_rubric_bits):
            raise ValueError(f"state {state.state_id} has a non-finite net score")
        eligible.append(
            _EligibleState(
                state=state,
                start_utc=start_utc,
                end_utc=end_utc,
                eligible_start_utc=eligible_start,
                eligible_end_utc=eligible_end,
                score=score,
            )
        )

    eligible.sort(
        key=lambda item: (
            item.eligible_start_utc,
            item.eligible_end_utc,
            item.state.state_id,
        )
    )
    cursor = date_start_utc
    for item in eligible:
        if item.eligible_start_utc > cursor:
            raise ValueError(
                "known-date candidate universe has a gap: "
                f"[{cursor.isoformat()}, {item.eligible_start_utc.isoformat()})"
            )
        if item.eligible_start_utc < cursor:
            raise ValueError(
                "known-date candidate universe has overlapping intervals at "
                f"{item.eligible_start_utc.isoformat()}"
            )
        cursor = item.eligible_end_utc
    if cursor < date_end_utc:
        raise ValueError(
            "known-date candidate universe has a gap: "
            f"[{cursor.isoformat()}, {date_end_utc.isoformat()})"
        )
    if cursor > date_end_utc:
        # Eligible ends are clipped, so this is an invariant guard rather than
        # an expected user-input failure.
        raise ValueError("known-date candidate universe extends beyond declared date")
    return date_start_utc, date_end_utc, tuple(eligible)


def rank_known_date_intervals(
    states: Iterable[CandidateState],
    scores: Mapping[str, ScoredState],
    local_date: date,
    timezone_name: str,
) -> KnownDateIntervalRanking:
    """Rank a complete exact stable-interval partition for one local date.

    Scores are ordered descending.  A tie exists only when
    ``net_rubric_bits`` compares exactly equal; no tolerance or secondary
    scientific criterion silently breaks it.  Within a tie, intervals are
    ordered chronologically and then by state ID solely for deterministic
    serialization.
    """

    date_start, date_end, eligible = _validated_eligible_states(
        states, scores, local_date, timezone_name
    )
    by_score: dict[float, list[_EligibleState]] = {}
    for item in eligible:
        by_score.setdefault(item.score.net_rubric_bits, []).append(item)

    groups: list[RankedIntervalGroup] = []
    rank_start = 1
    for net_score in sorted(by_score, reverse=True):
        tied_items = sorted(
            by_score[net_score],
            key=lambda item: (
                item.eligible_start_utc,
                item.eligible_end_utc,
                item.state.state_id,
            ),
        )
        rank_end = rank_start + len(tied_items) - 1
        records = tuple(
            RankedStableInterval(
                state_id=item.state.state_id,
                start_utc=item.start_utc,
                end_utc=item.end_utc,
                eligible_start_utc=item.eligible_start_utc,
                eligible_end_utc=item.eligible_end_utc,
                stable_width=item.end_utc - item.start_utc,
                eligible_width=item.eligible_end_utc - item.eligible_start_utc,
                score=item.score,
                rank_start=rank_start,
                rank_end=rank_end,
            )
            for item in tied_items
        )
        groups.append(
            RankedIntervalGroup(
                net_rubric_bits=net_score,
                rank_start=rank_start,
                rank_end=rank_end,
                intervals=records,
            )
        )
        rank_start = rank_end + 1
    return KnownDateIntervalRanking(
        local_date=local_date,
        timezone_name=timezone_name,
        date_start_utc=date_start,
        date_end_utc=date_end,
        groups=tuple(groups),
    )


def identify_revealed_interval(
    ranking: KnownDateIntervalRanking,
    revealed_true_utc: datetime,
) -> RevealedIntervalIdentification:
    """Identify the ranked interval containing a true UTC instant after reveal.

    Containment is half-open.  Therefore an instant exactly at a boundary
    belongs to the interval beginning there, never the interval ending there.
    This helper accepts no answer-key path or decryption material.
    """

    true_utc = _as_utc(revealed_true_utc, "revealed_true_utc")
    if not ranking.date_start_utc <= true_utc < ranking.date_end_utc:
        raise ValueError(
            "revealed true UTC instant is outside the declared local date's half-open bounds"
        )
    matches = tuple(
        record
        for record in ranking.chronological_records
        if record.eligible_start_utc <= true_utc < record.eligible_end_utc
    )
    if len(matches) != 1:
        raise ValueError(
            f"expected one stable interval containing revealed truth, found {len(matches)}"
        )
    return RevealedIntervalIdentification(true_utc=true_utc, interval=matches[0])
