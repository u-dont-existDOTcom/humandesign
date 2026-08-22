"""Exact V4.3 lexicographic interval ranking and substantive ties."""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timedelta
from fractions import Fraction

from hdmatch.model.v4_3.contracts import V43_RANKING_POLICY_VERSION
from hdmatch.model.v4_3.scoring import V43CandidateScore


@dataclass(frozen=True, slots=True)
class ScoredExactInterval:
    candidate_id: str
    utc_start: datetime
    stable_duration_microseconds: int
    score: V43CandidateScore

    def __post_init__(self) -> None:
        if not self.candidate_id:
            raise ValueError("candidate ID must not be empty")
        if self.utc_start.tzinfo is None or self.utc_start.utcoffset() is None:
            raise ValueError("UTC start must be timezone-aware")
        if self.utc_start.utcoffset() != timedelta(0):
            raise ValueError("UTC start must use a zero UTC offset")
        if (
            isinstance(self.stable_duration_microseconds, bool)
            or not isinstance(self.stable_duration_microseconds, int)
            or self.stable_duration_microseconds <= 0
        ):
            raise ValueError("stable interval duration must be exact positive microseconds")
        _validate_score_values(self.score)

    @property
    def substantive_rank_key(self) -> tuple[float, int, float, float, int]:
        """Lower tuple is better; all five fields define substantive identity."""

        return (
            -self.score.net_information,
            self.score.meaningful_contradictions,
            -self.score.detailed_support,
            -self.score.core_fit,
            -self.stable_duration_microseconds,
        )


@dataclass(frozen=True, slots=True)
class RankedExactInterval:
    candidate: ScoredExactInterval
    rank_start: int
    rank_end: int
    midrank: Fraction

    @property
    def substantively_tied(self) -> bool:
        return self.rank_start != self.rank_end


@dataclass(frozen=True, slots=True)
class SubstantiveTieGroup:
    rank_start: int
    rank_end: int
    substantive_rank_key: tuple[float, int, float, float, int]
    candidate_ids: tuple[str, ...]

    @property
    def tied(self) -> bool:
        return self.rank_start != self.rank_end


@dataclass(frozen=True, slots=True)
class V43IntervalRanking:
    ranking_policy_version: str
    records: tuple[RankedExactInterval, ...]
    tie_groups: tuple[SubstantiveTieGroup, ...]


def rank_exact_intervals(
    candidates: tuple[ScoredExactInterval, ...],
) -> V43IntervalRanking:
    """Rank exact intervals without scalarizing the five frozen criteria.

    UTC start and candidate ID order display within a substantive tie only; they
    never break that tie or alter any candidate's rank interval.
    """

    candidate_ids = tuple(candidate.candidate_id for candidate in candidates)
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("candidate IDs must be unique")
    ordered = sorted(
        candidates,
        key=lambda candidate: (
            candidate.substantive_rank_key,
            candidate.utc_start,
            candidate.candidate_id,
        ),
    )
    records: list[RankedExactInterval] = []
    groups: list[SubstantiveTieGroup] = []
    index = 0
    while index < len(ordered):
        key = ordered[index].substantive_rank_key
        end = index + 1
        while end < len(ordered) and ordered[end].substantive_rank_key == key:
            end += 1
        rank_start = index + 1
        rank_end = end
        midrank = Fraction(rank_start + rank_end, 2)
        group = ordered[index:end]
        records.extend(
            RankedExactInterval(
                candidate=candidate,
                rank_start=rank_start,
                rank_end=rank_end,
                midrank=midrank,
            )
            for candidate in group
        )
        groups.append(
            SubstantiveTieGroup(
                rank_start=rank_start,
                rank_end=rank_end,
                substantive_rank_key=key,
                candidate_ids=tuple(candidate.candidate_id for candidate in group),
            )
        )
        index = end
    return V43IntervalRanking(
        ranking_policy_version=V43_RANKING_POLICY_VERSION,
        records=tuple(records),
        tie_groups=tuple(groups),
    )


def _validate_score_values(score: V43CandidateScore) -> None:
    numeric_values = (
        score.evidence_rubric_bits,
        score.contradiction_rubric_bits,
        score.net_information,
        score.detailed_support,
        score.core_fit,
    )
    if not all(math.isfinite(value) for value in numeric_values):
        raise ValueError("ranked V4.3 score values must be finite")
    if not 0.0 <= score.detailed_support <= 100.0:
        raise ValueError("DetailedSupport must be in [0, 100]")
    if not 0.0 <= score.core_fit <= 100.0:
        raise ValueError("CoreFit must be in [0, 100]")
    if score.meaningful_contradictions < 0:
        raise ValueError("meaningful contradiction count cannot be negative")
    if not math.isclose(
        score.net_information,
        score.evidence_rubric_bits - score.contradiction_rubric_bits,
        rel_tol=1e-15,
        abs_tol=1e-15,
    ):
        raise ValueError("NetInformation must not contain CoreFit or another hidden bonus")
