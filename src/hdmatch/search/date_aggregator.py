"""Frozen date-level aggregation over exact chart-state intervals."""

from __future__ import annotations

import math
from collections import defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import date
from enum import StrEnum

from hdmatch.schemas import CandidateState, RankedDate, ScoredState


class AggregationMode(StrEnum):
    BEST_STATE = "best_state"
    DURATION_WEIGHTED_MEAN = "duration_weighted_mean"
    DURATION_WEIGHTED_EVIDENCE = "duration_weighted_evidence"


@dataclass(frozen=True)
class DateContribution:
    score: ScoredState
    seconds: float


def _log2_weighted_sum(contributions: list[DateContribution]) -> float:
    total = sum(item.seconds for item in contributions)
    values = [item.score.net_rubric_bits for item in contributions]
    ceiling = max(values)
    scaled = sum(
        (item.seconds / total) * 2.0 ** (item.score.net_rubric_bits - ceiling)
        for item in contributions
    )
    return ceiling + math.log2(scaled)


def _aggregate(contributions: list[DateContribution], mode: AggregationMode) -> float:
    if mode == AggregationMode.BEST_STATE:
        return max(item.score.net_rubric_bits for item in contributions)
    if mode == AggregationMode.DURATION_WEIGHTED_MEAN:
        total = sum(item.seconds for item in contributions)
        return sum(item.score.net_rubric_bits * item.seconds for item in contributions) / total
    return _log2_weighted_sum(contributions)


def aggregate_dates(
    states: Iterable[CandidateState],
    scores: Mapping[str, ScoredState],
    mode: AggregationMode,
    threshold_rubric_bits: float = 0.0,
) -> tuple[RankedDate, ...]:
    grouped: dict[date, list[DateContribution]] = defaultdict(list)
    for state in states:
        try:
            score = scores[state.state_id]
        except KeyError as exc:
            raise ValueError(f"missing score for state {state.state_id}") from exc
        for overlap in state.local_date_overlaps:
            grouped[overlap.date].append(DateContribution(score, overlap.seconds))
    provisional: list[tuple[date, float, ScoredState, float]] = []
    for local_date, contributions in grouped.items():
        total = sum(item.seconds for item in contributions)
        above = sum(
            item.seconds
            for item in contributions
            if item.score.net_rubric_bits >= threshold_rubric_bits
        )
        best = max(
            (item.score for item in contributions),
            key=lambda item: (
                item.net_rubric_bits,
                -item.meaningful_contradictions,
                item.detailed_support,
                item.core_fit,
                item.state_id,
            ),
        )
        provisional.append((local_date, _aggregate(contributions, mode), best, above / total))
    provisional.sort(key=lambda item: (-item[1], str(item[0])))
    result: list[RankedDate] = []
    position = 0
    while position < len(provisional):
        end = position + 1
        while end < len(provisional) and math.isclose(
            provisional[end][1], provisional[position][1], rel_tol=1e-12, abs_tol=1e-12
        ):
            end += 1
        midrank = (position + 1 + end) / 2.0
        tied = end - position > 1
        for local_date, aggregate_score, best, support in provisional[position:end]:
            result.append(
                RankedDate(
                    local_date=local_date,
                    date_score=aggregate_score,
                    date_rank=midrank,
                    best_state=best,
                    duration_weighted_support=support,
                    tied=tied,
                )
            )
        position = end
    result.sort(key=lambda item: (item.date_rank, item.local_date))
    return tuple(result)
