"""Chart-blind behavioral target helpers for the CF-003 secondary study.

This module is separate from the published astronomical predictor in cf003.py.
The behavioral classifier is not allowed to see planet names, chart data, predictor
scores, or the evaluator-only construct-to-planet map until its source-bounded
construct ratings are frozen.

Scientific status:
- development/secondary target candidate;
- does not alter TN-001, LiteratureModelV1, or the main Life Patterns score;
- existing participants are exploratory;
- prospective use requires freezing the target contract/mapping/software before
  opening new participants' target responses.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from statistics import fmean
from typing import Iterable, Mapping, Sequence

from .cf003 import CF003_CANDIDATE_BODIES

CF003_CONSTRUCT_IDS: tuple[str, ...] = (
    "T01",
    "T02",
    "T03",
    "T04",
    "T05",
    "T06",
    "T07",
    "T08",
    "T09",
    "T10",
)

CF003_CONSTRUCT_TO_PLANET: Mapping[str, str] = {
    "T01": "venus",
    "T02": "pluto",
    "T03": "moon",
    "T04": "saturn",
    "T05": "sun",
    "T06": "uranus",
    "T07": "mercury",
    "T08": "jupiter",
    "T09": "mars",
    "T10": "neptune",
}


@dataclass(frozen=True, slots=True)
class EvidenceQuote:
    turn_id: str
    quote: str


@dataclass(frozen=True, slots=True)
class BehavioralConstructScore:
    construct_id: str
    dominance_rating: int | None
    evidence_sufficient: bool
    support_quotes: tuple[EvidenceQuote, ...] = ()
    counterevidence_quotes: tuple[EvidenceQuote, ...] = ()
    conditions: tuple[str, ...] = ()
    time_frame: str = "unknown"
    confidence: str = "low"
    reason: str = ""

    def __post_init__(self) -> None:
        if self.construct_id not in CF003_CONSTRUCT_IDS:
            raise ValueError(f"unknown construct_id: {self.construct_id}")
        if self.dominance_rating is not None and (
            isinstance(self.dominance_rating, bool)
            or not isinstance(self.dominance_rating, int)
            or not 0 <= self.dominance_rating <= 4
        ):
            raise ValueError("dominance_rating must be an integer 0..4 or null")
        if self.evidence_sufficient != (self.dominance_rating is not None):
            raise ValueError("evidence_sufficient must be true iff dominance_rating is non-null")
        if self.confidence not in {"low", "medium", "high"}:
            raise ValueError("confidence must be low, medium, or high")
        if len(self.support_quotes) > 3 or len(self.counterevidence_quotes) > 3:
            raise ValueError("at most three support and three counterevidence quotes")


@dataclass(frozen=True, slots=True)
class CF003BehavioralComparison:
    predictor_rank_groups: tuple[tuple[str, ...], ...]
    behavioral_rank_groups: tuple[tuple[str, ...], ...]
    predictor_top_set: tuple[str, ...]
    primary_top_set_mean_behavioral_midrank: float
    spearman_rho: float | None
    predictor_top3_inclusive: tuple[str, ...]
    behavioral_top3_inclusive: tuple[str, ...]
    top3_overlap_count: int
    top3_jaccard: float


@dataclass(frozen=True, slots=True)
class CF003CohortPair:
    participant_id: str
    predictor_scores: Mapping[str, float]
    behavioral_scores: Mapping[str, float]


@dataclass(frozen=True, slots=True)
class CF003PermutationResult:
    observed_mean_top_set_midrank: float
    permutation_count: int
    equal_or_better_count: int
    p_value: float


def _finite_complete_scores(
    scores: Mapping[str, float], *, labels: Sequence[str]
) -> dict[str, float]:
    normalized: dict[str, float] = {}
    for label, value in scores.items():
        key = str(label).strip().lower()
        if key in normalized:
            raise ValueError(f"duplicate score label after normalization: {key}")
        number = float(value)
        if not math.isfinite(number):
            raise ValueError(f"score for {label} must be finite")
        normalized[key] = number
    expected = set(labels)
    if set(normalized) != expected:
        missing = sorted(expected - set(normalized))
        extra = sorted(set(normalized) - expected)
        raise ValueError(f"scores must be complete; missing={missing}, extra={extra}")
    return normalized


def rank_score_groups(
    scores: Mapping[str, float],
    *,
    label_order: Sequence[str] = CF003_CANDIDATE_BODIES,
) -> tuple[tuple[str, ...], ...]:
    """Return descending tie groups without inventing a tie-breaker."""

    normalized = _finite_complete_scores(scores, labels=label_order)
    order = {label: index for index, label in enumerate(label_order)}
    values = sorted(set(normalized.values()), reverse=True)
    return tuple(
        tuple(
            sorted(
                (label for label, score in normalized.items() if score == value),
                key=order.__getitem__,
            )
        )
        for value in values
    )


def midranks_descending(
    scores: Mapping[str, float],
    *,
    label_order: Sequence[str] = CF003_CANDIDATE_BODIES,
) -> dict[str, float]:
    groups = rank_score_groups(scores, label_order=label_order)
    out: dict[str, float] = {}
    next_rank = 1
    for group in groups:
        end_rank = next_rank + len(group) - 1
        midrank = (next_rank + end_rank) / 2.0
        for label in group:
            out[label] = midrank
        next_rank = end_rank + 1
    return out


def inclusive_top_k(
    scores: Mapping[str, float],
    k: int,
    *,
    label_order: Sequence[str] = CF003_CANDIDATE_BODIES,
) -> tuple[str, ...]:
    if not 1 <= k <= len(label_order):
        raise ValueError("k must be within the label universe")
    normalized = _finite_complete_scores(scores, labels=label_order)
    ordered_values = sorted(normalized.values(), reverse=True)
    threshold = ordered_values[k - 1]
    order = {label: index for index, label in enumerate(label_order)}
    return tuple(
        sorted(
            (label for label, score in normalized.items() if score >= threshold),
            key=order.__getitem__,
        )
    )


def _pearson(xs: Sequence[float], ys: Sequence[float]) -> float | None:
    if len(xs) != len(ys) or not xs:
        raise ValueError("correlation inputs must be non-empty and equal length")
    mean_x = fmean(xs)
    mean_y = fmean(ys)
    dx = [value - mean_x for value in xs]
    dy = [value - mean_y for value in ys]
    denom = math.sqrt(sum(value * value for value in dx) * sum(value * value for value in dy))
    if denom == 0:
        return None
    return sum(a * b for a, b in zip(dx, dy, strict=True)) / denom


def compare_cf003_rankings(
    predictor_scores: Mapping[str, float],
    behavioral_scores: Mapping[str, float],
) -> CF003BehavioralComparison:
    predictor = _finite_complete_scores(predictor_scores, labels=CF003_CANDIDATE_BODIES)
    behavioral = _finite_complete_scores(behavioral_scores, labels=CF003_CANDIDATE_BODIES)
    predictor_groups = rank_score_groups(predictor)
    behavioral_groups = rank_score_groups(behavioral)
    behavior_midranks = midranks_descending(behavioral)
    predictor_midranks = midranks_descending(predictor)
    top_set = predictor_groups[0]
    primary = fmean(behavior_midranks[label] for label in top_set)

    ordered = list(CF003_CANDIDATE_BODIES)
    rho = _pearson(
        [predictor_midranks[label] for label in ordered],
        [behavior_midranks[label] for label in ordered],
    )
    predictor_top3 = inclusive_top_k(predictor, 3)
    behavioral_top3 = inclusive_top_k(behavioral, 3)
    intersection = set(predictor_top3) & set(behavioral_top3)
    union = set(predictor_top3) | set(behavioral_top3)

    return CF003BehavioralComparison(
        predictor_rank_groups=predictor_groups,
        behavioral_rank_groups=behavioral_groups,
        predictor_top_set=top_set,
        primary_top_set_mean_behavioral_midrank=primary,
        spearman_rho=rho,
        predictor_top3_inclusive=predictor_top3,
        behavioral_top3_inclusive=behavioral_top3,
        top3_overlap_count=len(intersection),
        top3_jaccard=len(intersection) / len(union),
    )


def validate_behavioral_classifier_result(
    payload: Mapping[str, object],
    *,
    answer_text_by_turn_id: Mapping[str, str],
) -> tuple[BehavioralConstructScore, ...]:
    """Validate a classifier result against exact participant-answer source."""

    raw_items = payload.get("construct_scores")
    if not isinstance(raw_items, list):
        raise ValueError("construct_scores must be a list")
    if len(raw_items) != len(CF003_CONSTRUCT_IDS):
        raise ValueError("construct_scores must contain exactly ten items")

    parsed: list[BehavioralConstructScore] = []
    seen: set[str] = set()
    for raw in raw_items:
        if not isinstance(raw, Mapping):
            raise ValueError("each construct score must be an object")
        construct_id = str(raw.get("construct_id", ""))
        if construct_id in seen:
            raise ValueError(f"duplicate construct score: {construct_id}")
        seen.add(construct_id)

        def quotes(field: str) -> tuple[EvidenceQuote, ...]:
            value = raw.get(field, [])
            if not isinstance(value, list):
                raise ValueError(f"{field} must be a list")
            out: list[EvidenceQuote] = []
            for quote_item in value:
                if not isinstance(quote_item, Mapping):
                    raise ValueError(f"{field} items must be objects")
                turn_id = str(quote_item.get("turn_id", ""))
                quote = str(quote_item.get("quote", ""))
                source = answer_text_by_turn_id.get(turn_id)
                if source is None:
                    raise ValueError(f"quote references unknown turn: {turn_id}")
                if not quote or quote not in source:
                    raise ValueError(f"quote for {construct_id} is not an exact answer substring")
                out.append(EvidenceQuote(turn_id=turn_id, quote=quote))
            return tuple(out)

        rating = raw.get("dominance_rating")
        if rating is not None:
            if isinstance(rating, bool) or not isinstance(rating, int):
                raise ValueError("dominance_rating must be integer or null")

        conditions_raw = raw.get("conditions", [])
        if not isinstance(conditions_raw, list) or any(
            not isinstance(value, str) for value in conditions_raw
        ):
            raise ValueError("conditions must be a list of strings")

        score = BehavioralConstructScore(
            construct_id=construct_id,
            dominance_rating=rating,
            evidence_sufficient=bool(raw.get("evidence_sufficient")),
            support_quotes=quotes("support_quotes"),
            counterevidence_quotes=quotes("counterevidence_quotes"),
            conditions=tuple(conditions_raw),
            time_frame=str(raw.get("time_frame", "unknown")),
            confidence=str(raw.get("confidence", "low")),
            reason=str(raw.get("reason", "")),
        )
        if score.dominance_rating is not None and score.dominance_rating > 0:
            if not score.support_quotes:
                raise ValueError(f"positive rating for {construct_id} needs exact support source")
        if score.dominance_rating == 0 and not (
            score.counterevidence_quotes or score.support_quotes
        ):
            raise ValueError(f"zero rating for {construct_id} needs explicit source, not absence")
        parsed.append(score)

    if seen != set(CF003_CONSTRUCT_IDS):
        raise ValueError("construct score IDs do not match the frozen ten-construct universe")
    order = {value: index for index, value in enumerate(CF003_CONSTRUCT_IDS)}
    return tuple(sorted(parsed, key=lambda score: order[score.construct_id]))


def construct_scores_to_planets(
    scores: Sequence[BehavioralConstructScore],
) -> dict[str, float]:
    if {score.construct_id for score in scores} != set(CF003_CONSTRUCT_IDS):
        raise ValueError("all ten frozen constructs are required")
    out: dict[str, float] = {}
    for score in scores:
        if score.dominance_rating is None:
            raise ValueError("behavioral ten-way ranking is incomplete")
        out[CF003_CONSTRUCT_TO_PLANET[score.construct_id]] = float(score.dominance_rating)
    return _finite_complete_scores(out, labels=CF003_CANDIDATE_BODIES)


def cohort_primary_statistic(pairs: Sequence[CF003CohortPair]) -> float:
    if not pairs:
        raise ValueError("at least one participant pair is required")
    return fmean(
        compare_cf003_rankings(
            pair.predictor_scores, pair.behavioral_scores
        ).primary_top_set_mean_behavioral_midrank
        for pair in pairs
    )


def apply_global_label_permutation(
    behavioral_scores: Mapping[str, float],
    permutation: Sequence[str],
) -> dict[str, float]:
    """Apply one shared label permutation to a complete behavioral profile."""

    if len(permutation) != len(CF003_CANDIDATE_BODIES) or set(permutation) != set(
        CF003_CANDIDATE_BODIES
    ):
        raise ValueError("permutation must contain each candidate body exactly once")
    source = _finite_complete_scores(behavioral_scores, labels=CF003_CANDIDATE_BODIES)
    return {
        target_label: source[source_label]
        for target_label, source_label in zip(CF003_CANDIDATE_BODIES, permutation, strict=True)
    }


def permutation_test_from_global_label_maps(
    pairs: Sequence[CF003CohortPair],
    permutations: Iterable[Sequence[str]],
) -> CF003PermutationResult:
    """One-sided null: lower mean predicted-top behavioral rank is better."""

    observed = cohort_primary_statistic(pairs)
    total = 0
    equal_or_better = 0
    for permutation in permutations:
        total += 1
        permuted_pairs = [
            CF003CohortPair(
                participant_id=pair.participant_id,
                predictor_scores=pair.predictor_scores,
                behavioral_scores=apply_global_label_permutation(
                    pair.behavioral_scores, permutation
                ),
            )
            for pair in pairs
        ]
        statistic = cohort_primary_statistic(permuted_pairs)
        if statistic <= observed:
            equal_or_better += 1
    if total == 0:
        raise ValueError("at least one permutation is required")
    return CF003PermutationResult(
        observed_mean_top_set_midrank=observed,
        permutation_count=total,
        equal_or_better_count=equal_or_better,
        p_value=(equal_or_better + 1) / (total + 1),
    )


def sample_global_label_permutations(
    count: int,
    *,
    seed: int,
) -> tuple[tuple[str, ...], ...]:
    if count < 1:
        raise ValueError("count must be positive")
    canonical = tuple(CF003_CANDIDATE_BODIES)
    maximum = math.factorial(len(canonical))
    if count > maximum:
        raise ValueError(f"count cannot exceed the {maximum} unique label permutations")
    rng = random.Random(seed)
    seen: set[tuple[str, ...]] = set()
    while len(seen) < count:
        candidate = list(canonical)
        rng.shuffle(candidate)
        seen.add(tuple(candidate))
        if len(seen) == math.factorial(len(canonical)):
            break
    return tuple(sorted(seen))
