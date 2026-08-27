"""Information-theoretic discrimination audits for frozen participant models."""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from collections.abc import Callable, Hashable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from statistics import median
from typing import TypeVar

from hdmatch.schemas import CandidateState

Fingerprint = TypeVar("Fingerprint", bound=Hashable)


@dataclass(frozen=True)
class PartitionAudit:
    """Discrimination ceiling for a partition of candidate states."""

    state_count: int
    group_count: int
    singleton_groups: int
    min_tie_size: int
    median_tie_size: float
    p90_tie_size: int
    max_tie_size: int
    state_uniform_entropy_bits: float
    duration_weighted_entropy_bits: float
    state_uniform_residual_bits: float
    duration_weighted_residual_bits: float
    exact_state_ceiling: float
    top5_state_ceiling: float
    top10_state_ceiling: float


@dataclass(frozen=True)
class GreedyQuestionStep:
    question_id: str
    cumulative_entropy_bits: float
    incremental_bits: float
    fingerprint_groups: int
    max_tie_size: int


def audit_partition(
    states: Sequence[CandidateState],
    fingerprint: Callable[[CandidateState], Fingerprint],
) -> PartitionAudit:
    """Measure how well a deterministic fingerprint can distinguish candidate states.

    The interval-uniform metrics treat each cached structural interval as one candidate.
    Duration-weighted metrics instead use a uniform-in-time prior over the cache range.
    """

    if not states:
        raise ValueError("candidate universe must not be empty")

    counts: Counter[Fingerprint] = Counter()
    durations: dict[Fingerprint, float] = defaultdict(float)
    interval_durations: list[float] = []
    for state in states:
        key = fingerprint(state)
        counts[key] += 1
        duration = (state.end_utc - state.start_utc).total_seconds()
        if duration <= 0.0:
            raise ValueError("candidate intervals must have positive duration")
        durations[key] += duration
        interval_durations.append(duration)

    tie_sizes = sorted(counts.values())
    n_states = len(states)
    state_entropy = _entropy_from_weights(counts.values())
    duration_entropy = _entropy_from_weights(durations.values())
    interval_duration_entropy = _entropy_from_weights(interval_durations)
    return PartitionAudit(
        state_count=n_states,
        group_count=len(counts),
        singleton_groups=sum(size == 1 for size in tie_sizes),
        min_tie_size=tie_sizes[0],
        median_tie_size=float(median(tie_sizes)),
        p90_tie_size=_nearest_rank_percentile(tie_sizes, 0.90),
        max_tie_size=tie_sizes[-1],
        state_uniform_entropy_bits=state_entropy,
        duration_weighted_entropy_bits=duration_entropy,
        state_uniform_residual_bits=max(0.0, math.log2(n_states) - state_entropy),
        duration_weighted_residual_bits=max(
            0.0, interval_duration_entropy - duration_entropy
        ),
        exact_state_ceiling=len(counts) / n_states,
        top5_state_ceiling=sum(min(5, size) for size in tie_sizes) / n_states,
        top10_state_ceiling=sum(min(10, size) for size in tie_sizes) / n_states,
    )


def greedy_question_sequence(
    states: Sequence[CandidateState],
    answers_by_state: Mapping[str, Mapping[str, str]],
    *,
    question_ids: Iterable[str] | None = None,
) -> tuple[GreedyQuestionStep, ...]:
    """Greedily choose questions by noiseless interval-uniform information gain."""

    if not states:
        raise ValueError("candidate universe must not be empty")
    state_ids = {state.state_id for state in states}
    if not state_ids.issubset(answers_by_state):
        missing = sorted(state_ids - answers_by_state.keys())
        raise KeyError(f"missing predicted answers for states: {missing[:3]}")

    if question_ids is None:
        available = sorted(
            {
                question_id
                for state_id in state_ids
                for question_id in answers_by_state[state_id]
            }
        )
    else:
        available = sorted(set(question_ids))

    selected: list[str] = []
    remaining = set(available)
    previous_entropy = 0.0
    result: list[GreedyQuestionStep] = []
    while remaining:
        best_question: str | None = None
        best_entropy = -1.0
        best_counts: Counter[tuple[str, ...]] | None = None
        for question_id in sorted(remaining):
            trial = (*selected, question_id)
            counts: Counter[tuple[str, ...]] = Counter(
                tuple(answers_by_state[state.state_id].get(q, "unknown") for q in trial)
                for state in states
            )
            entropy = _entropy_from_weights(counts.values())
            if entropy > best_entropy + 1e-12:
                best_question = question_id
                best_entropy = entropy
                best_counts = counts
        assert best_question is not None
        assert best_counts is not None
        incremental = best_entropy - previous_entropy
        selected.append(best_question)
        remaining.remove(best_question)
        result.append(
            GreedyQuestionStep(
                question_id=best_question,
                cumulative_entropy_bits=best_entropy,
                incremental_bits=incremental,
                fingerprint_groups=len(best_counts),
                max_tie_size=max(best_counts.values()),
            )
        )
        previous_entropy = best_entropy
    return tuple(result)


def _entropy_from_weights(weights: Iterable[int | float]) -> float:
    values = tuple(float(weight) for weight in weights)
    total = sum(values)
    if total <= 0.0:
        raise ValueError("entropy weights must have positive total")
    return -sum(
        (weight / total) * math.log2(weight / total)
        for weight in values
        if weight > 0.0
    )


def _nearest_rank_percentile(sorted_values: Sequence[int], quantile: float) -> int:
    if not 0.0 < quantile <= 1.0:
        raise ValueError("quantile must be in (0, 1]")
    if not sorted_values:
        raise ValueError("percentile input must not be empty")
    index = max(0, math.ceil(quantile * len(sorted_values)) - 1)
    return sorted_values[index]
