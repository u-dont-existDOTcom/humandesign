"""Exact candidate-blind adaptive simulations under declared answer perturbations."""

from __future__ import annotations

import hashlib
import math
import statistics
from collections import Counter
from collections.abc import Hashable, Mapping, Sequence
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


Perturbation = Literal["wrong", "ambiguous", "other", "uncertain", "mixed", "counterevidence"]


class NoiseScenario(_FrozenModel):
    scenario_id: str = Field(min_length=1)
    perturbation: Perturbation
    fraction: float = Field(ge=0.0, le=1.0)
    minimum_perturbed_answers: int = Field(default=0, ge=0)
    seed: int = 20260827


DEFAULT_NOISE_SCENARIOS = (
    NoiseScenario(
        scenario_id="one_wrong_classification",
        perturbation="wrong",
        fraction=0.0,
        minimum_perturbed_answers=1,
    ),
    NoiseScenario(scenario_id="wrong_05pct", perturbation="wrong", fraction=0.05),
    NoiseScenario(scenario_id="wrong_10pct", perturbation="wrong", fraction=0.10),
    NoiseScenario(scenario_id="wrong_20pct", perturbation="wrong", fraction=0.20),
    NoiseScenario(scenario_id="ambiguous_05pct", perturbation="ambiguous", fraction=0.05),
    NoiseScenario(scenario_id="ambiguous_10pct", perturbation="ambiguous", fraction=0.10),
    NoiseScenario(scenario_id="ambiguous_20pct", perturbation="ambiguous", fraction=0.20),
    NoiseScenario(scenario_id="other_10pct", perturbation="other", fraction=0.10),
    NoiseScenario(scenario_id="uncertain_10pct", perturbation="uncertain", fraction=0.10),
    NoiseScenario(scenario_id="mixed_10pct", perturbation="mixed", fraction=0.10),
    NoiseScenario(
        scenario_id="counterevidence_10pct", perturbation="counterevidence", fraction=0.10
    ),
)


class NoiseCaseResult(_FrozenModel):
    scenario_id: str
    true_index: int = Field(ge=0)
    best_rank: int = Field(ge=1)
    worst_rank: int = Field(ge=1)
    midrank: float = Field(ge=1.0)
    percentile: float = Field(ge=0.0, le=1.0)
    top1_credit: float = Field(ge=0.0, le=1.0)
    top5_credit: float = Field(ge=0.0, le=1.0)
    top10_credit: float = Field(ge=0.0, le=1.0)
    candidate_survival_count: int = Field(ge=1)
    extra_tie_breakers: int = Field(ge=0)
    perturbed_answer_count: int = Field(ge=0)
    true_candidate_survived: bool
    selection_uses_birth_metadata: Literal[False] = False
    selection_uses_true_candidate: Literal[False] = False
    selection_uses_candidate_rank: Literal[False] = False
    target_blind_stopping: Literal[True] = True


class NoiseScenarioSummary(_FrozenModel):
    scenario_id: str
    case_count: int = Field(ge=1)
    top1: float = Field(ge=0.0, le=1.0)
    top5: float = Field(ge=0.0, le=1.0)
    top10: float = Field(ge=0.0, le=1.0)
    median_rank: float = Field(ge=1.0)
    mean_percentile: float = Field(ge=0.0, le=1.0)
    median_candidate_survival: float = Field(ge=1.0)
    true_candidate_survival_rate: float = Field(ge=0.0, le=1.0)
    median_extra_tie_breakers: float = Field(ge=0.0)
    maximum_extra_tie_breakers: int = Field(ge=0)


def simulate_noise_case(
    answer_rows: Sequence[Sequence[Hashable]],
    *,
    base_feature_count: int,
    true_index: int,
    scenario: NoiseScenario,
) -> NoiseCaseResult:
    """Rescore the complete universe after each candidate-blind adaptive answer."""
    if not answer_rows or not answer_rows[0]:
        raise ValueError("candidate answer rows cannot be empty")
    width = len(answer_rows[0])
    if any(len(row) != width for row in answer_rows):
        raise ValueError("candidate answer rows must have equal width")
    if not 0 < base_feature_count <= width:
        raise ValueError("base_feature_count must be within answer width")
    if not 0 <= true_index < len(answer_rows):
        raise IndexError("true_index is outside candidate rows")

    true_answers = answer_rows[true_index]
    count = max(
        scenario.minimum_perturbed_answers,
        math.ceil(base_feature_count * scenario.fraction),
    )
    count = min(count, base_feature_count)
    selected = _selected_positions(base_feature_count, count, scenario, true_index)
    observations: dict[int, tuple[Hashable, ...] | None] = {
        position: _perturb(answer_rows, position, true_answers[position], scenario, true_index)
        if position in selected
        else (true_answers[position],)
        for position in range(base_feature_count)
    }
    scores = _scores(answer_rows, observations)
    asked = 0
    remaining = set(range(base_feature_count, width))
    while remaining and _leader_count(scores) != 1:
        leaders = tuple(index for index, score in enumerate(scores) if score == max(scores))
        feature = _select_by_entropy(answer_rows, leaders, remaining)
        remaining.remove(feature)
        asked += 1
        observations[feature] = (true_answers[feature],)
        scores = _scores(answer_rows, observations)

    rank = _rank(scores, true_index)
    leaders = tuple(index for index, score in enumerate(scores) if score == max(scores))
    candidate_count = len(answer_rows)
    return NoiseCaseResult(
        scenario_id=scenario.scenario_id,
        true_index=true_index,
        best_rank=rank[0],
        worst_rank=rank[1],
        midrank=(rank[0] + rank[1]) / 2,
        percentile=(
            1.0
            if candidate_count == 1
            else 1 - (((rank[0] + rank[1]) / 2 - 1) / (candidate_count - 1))
        ),
        top1_credit=_top_k_credit(rank, 1),
        top5_credit=_top_k_credit(rank, 5),
        top10_credit=_top_k_credit(rank, 10),
        candidate_survival_count=len(leaders),
        extra_tie_breakers=asked,
        perturbed_answer_count=count,
        true_candidate_survived=true_index in leaders,
    )


def summarize_noise_cases(cases: Sequence[NoiseCaseResult]) -> NoiseScenarioSummary:
    if not cases:
        raise ValueError("at least one noise case is required")
    scenario_ids = {case.scenario_id for case in cases}
    if len(scenario_ids) != 1:
        raise ValueError("noise cases must share one scenario_id")
    return NoiseScenarioSummary(
        scenario_id=next(iter(scenario_ids)),
        case_count=len(cases),
        top1=statistics.fmean(case.top1_credit for case in cases),
        top5=statistics.fmean(case.top5_credit for case in cases),
        top10=statistics.fmean(case.top10_credit for case in cases),
        median_rank=statistics.median(case.midrank for case in cases),
        mean_percentile=statistics.fmean(case.percentile for case in cases),
        median_candidate_survival=statistics.median(
            case.candidate_survival_count for case in cases
        ),
        true_candidate_survival_rate=statistics.fmean(
            case.true_candidate_survived for case in cases
        ),
        median_extra_tie_breakers=statistics.median(case.extra_tie_breakers for case in cases),
        maximum_extra_tie_breakers=max(case.extra_tie_breakers for case in cases),
    )


def _selected_positions(
    width: int, count: int, scenario: NoiseScenario, true_index: int
) -> set[int]:
    ordered = sorted(
        range(width),
        key=lambda position: hashlib.sha256(
            f"{scenario.seed}:{scenario.scenario_id}:{true_index}:{position}".encode()
        ).digest(),
    )
    return set(ordered[:count])


def _perturb(
    rows: Sequence[Sequence[Hashable]],
    position: int,
    truth: Hashable,
    scenario: NoiseScenario,
    true_index: int,
) -> tuple[Hashable, ...] | None:
    if scenario.perturbation in {"ambiguous", "other", "uncertain"}:
        return None
    alternatives = sorted(
        {row[position] for row in rows if row[position] != truth}, key=repr
    )
    if not alternatives:
        return None
    index = int.from_bytes(
        hashlib.sha256(
            f"{scenario.seed}:{scenario.scenario_id}:{true_index}:{position}:label".encode()
        ).digest()[:8],
        "big",
    ) % len(alternatives)
    alternative = alternatives[index]
    if scenario.perturbation == "mixed":
        return (truth, alternative)
    return (alternative,)


def _scores(
    rows: Sequence[Sequence[Hashable]], observations: Mapping[int, tuple[Hashable, ...] | None]
) -> list[float]:
    scores = []
    for row in rows:
        score = 0.0
        for position, labels in observations.items():
            if labels is None:
                continue
            if len(labels) == 1:
                score += float(row[position] == labels[0])
            else:
                score += 0.5 * float(row[position] in labels)
        scores.append(score)
    return scores


def _leader_count(scores: Sequence[float]) -> int:
    best = max(scores)
    return sum(score == best for score in scores)


def _select_by_entropy(
    rows: Sequence[Sequence[Hashable]], leaders: Sequence[int], remaining: set[int]
) -> int:
    choices = []
    for feature in remaining:
        counts = Counter(rows[index][feature] for index in leaders)
        entropy = -sum(
            (count / len(leaders)) * math.log2(count / len(leaders))
            for count in counts.values()
        )
        choices.append((entropy, -feature, feature))
    return max(choices)[2]


def _rank(scores: Sequence[float], true_index: int) -> tuple[int, int]:
    true_score = scores[true_index]
    higher = sum(score > true_score for score in scores)
    tied = sum(score == true_score for score in scores)
    return higher + 1, higher + tied


def _top_k_credit(rank: tuple[int, int], k: int) -> float:
    best, worst = rank
    tie_size = worst - best + 1
    return max(0, min(worst, k) - best + 1) / tie_size
