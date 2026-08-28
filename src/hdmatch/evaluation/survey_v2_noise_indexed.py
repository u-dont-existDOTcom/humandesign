"""Exact bitset acceleration for the survey-v2 reference noise scorer.

Every categorical outcome is represented by a Python-integer candidate bitset.
Scores are accumulated as bit-sliced integers, so ranking is exact without an
N-by-N score matrix. The reference implementation remains the semantic oracle.
"""

from __future__ import annotations

import hashlib
import math
from collections.abc import Hashable, Mapping, Sequence
from dataclasses import dataclass

from hdmatch.evaluation.survey_v2_noise import (
    NoiseCaseResult,
    NoiseScenario,
    _selected_positions,
    _top_k_credit,
)


@dataclass(frozen=True)
class IndexedSurveyScorer:
    rows: tuple[tuple[Hashable, ...], ...]
    partitions: tuple[Mapping[Hashable, int], ...]
    universe_mask: int

    @classmethod
    def build(cls, answer_rows: Sequence[Sequence[Hashable]]) -> IndexedSurveyScorer:
        if not answer_rows or not answer_rows[0]:
            raise ValueError("candidate answer rows cannot be empty")
        rows = tuple(tuple(row) for row in answer_rows)
        width = len(rows[0])
        if any(len(row) != width for row in rows):
            raise ValueError("candidate answer rows must have equal width")
        indices: list[dict[Hashable, list[int]]] = [dict() for _ in range(width)]
        for candidate_index, row in enumerate(rows):
            for feature, value in enumerate(row):
                indices[feature].setdefault(value, []).append(candidate_index)
        byte_count = (len(rows) + 7) // 8
        partitions: list[dict[Hashable, int]] = []
        for feature_indices in indices:
            encoded: dict[Hashable, int] = {}
            for value, candidate_indices in feature_indices.items():
                packed = bytearray(byte_count)
                for candidate_index in candidate_indices:
                    packed[candidate_index >> 3] |= 1 << (candidate_index & 7)
                encoded[value] = int.from_bytes(packed, "little")
            partitions.append(encoded)
        return cls(
            rows=rows,
            partitions=tuple(partitions),
            universe_mask=(1 << len(rows)) - 1,
        )

    @property
    def candidate_count(self) -> int:
        return len(self.rows)

    @property
    def feature_count(self) -> int:
        return len(self.partitions)

    def score_histogram(
        self, observations: Mapping[int, tuple[Hashable, ...] | None]
    ) -> tuple[tuple[int, ...], tuple[int, ...]]:
        """Return exact scaled-score counts and masks; mixed credit is scaled by two."""
        planes, maximum_score = self.score_planes(observations)
        masks = tuple(
            _score_mask(planes, score, self.universe_mask)
            for score in range(maximum_score + 1)
        )
        return tuple(mask.bit_count() for mask in masks), masks

    def score_planes(
        self, observations: Mapping[int, tuple[Hashable, ...] | None]
    ) -> tuple[tuple[int, ...], int]:
        """Accumulate exact scaled scores in bit-sliced binary form."""
        planes: list[int] = []
        maximum_score = 0
        for feature, labels in observations.items():
            if labels is None:
                continue
            if len(labels) == 1:
                bitmap = self.partitions[feature].get(labels[0], 0)
                _add_weighted_bitmap(planes, bitmap, shift=1)
                maximum_score += 2
            else:
                bitmap = 0
                for label in labels:
                    bitmap |= self.partitions[feature].get(label, 0)
                _add_weighted_bitmap(planes, bitmap, shift=0)
                maximum_score += 1
        return tuple(planes), maximum_score

    def leader_mask(self, planes: Sequence[int]) -> int:
        """Return the exact maximum-score candidate mask without score enumeration."""
        candidates = self.universe_mask
        for bitmap in reversed(planes):
            with_one = candidates & bitmap
            if with_one:
                candidates = with_one
            else:
                candidates &= ~bitmap
        return candidates & self.universe_mask

    def rank_masks(self, planes: Sequence[int], true_score: int) -> tuple[int, int]:
        """Return candidates scoring above and equal to an exact scaled score."""
        equal_prefix = self.universe_mask
        greater = 0
        for plane in range(len(planes) - 1, -1, -1):
            bitmap = planes[plane]
            if true_score & (1 << plane):
                equal_prefix &= bitmap
            else:
                greater |= equal_prefix & bitmap
                equal_prefix &= ~bitmap
        if true_score >> len(planes):
            return 0, 0
        return greater & self.universe_mask, equal_prefix & self.universe_mask

    def select_by_entropy(self, leaders: int, remaining: set[int]) -> int:
        leader_count = leaders.bit_count()
        choices: list[tuple[float, int, int]] = []
        for feature in remaining:
            counts = tuple(
                (leaders & partition).bit_count()
                for partition in self.partitions[feature].values()
            )
            entropy = -sum(
                (count / leader_count) * math.log2(count / leader_count)
                for count in counts
                if count
            )
            choices.append((entropy, -feature, feature))
        return max(choices)[2]

    def perturb(
        self,
        feature: int,
        truth: Hashable,
        scenario: NoiseScenario,
        true_index: int,
    ) -> tuple[Hashable, ...] | None:
        """Produce the reference perturbation without scanning candidate rows."""
        if scenario.perturbation in {"ambiguous", "other", "uncertain"}:
            return None
        alternatives = sorted(
            (value for value in self.partitions[feature] if value != truth), key=repr
        )
        if not alternatives:
            return None
        index = int.from_bytes(
            hashlib.sha256(
                (
                    f"{scenario.seed}:{scenario.scenario_id}:"
                    f"{true_index}:{feature}:label"
                ).encode()
            ).digest()[:8],
            "big",
        ) % len(alternatives)
        alternative = alternatives[index]
        if scenario.perturbation == "mixed":
            return (truth, alternative)
        return (alternative,)


def simulate_noise_case_indexed(
    scorer: IndexedSurveyScorer,
    *,
    base_feature_count: int,
    true_index: int,
    scenario: NoiseScenario,
) -> NoiseCaseResult:
    """Accelerated exact equivalent of ``simulate_noise_case``."""
    if not 0 < base_feature_count <= scorer.feature_count:
        raise ValueError("base_feature_count must be within answer width")
    if not 0 <= true_index < scorer.candidate_count:
        raise IndexError("true_index is outside candidate rows")
    true_answers = scorer.rows[true_index]
    count = max(
        scenario.minimum_perturbed_answers,
        math.ceil(base_feature_count * scenario.fraction),
    )
    count = min(count, base_feature_count)
    selected = _selected_positions(base_feature_count, count, scenario, true_index)
    observations: dict[int, tuple[Hashable, ...] | None] = {
        position: scorer.perturb(position, true_answers[position], scenario, true_index)
        if position in selected
        else (true_answers[position],)
        for position in range(base_feature_count)
    }
    asked = 0
    remaining = set(range(base_feature_count, scorer.feature_count))
    planes, _ = scorer.score_planes(observations)
    leaders = scorer.leader_mask(planes)
    while remaining and leaders.bit_count() != 1:
        feature = scorer.select_by_entropy(leaders, remaining)
        remaining.remove(feature)
        asked += 1
        observations[feature] = (true_answers[feature],)
        planes, _ = scorer.score_planes(observations)
        leaders = scorer.leader_mask(planes)

    true_score = _candidate_scaled_score(true_answers, observations)
    greater_mask, tied_mask = scorer.rank_masks(planes, true_score)
    tied = tied_mask.bit_count()
    higher = greater_mask.bit_count()
    rank = (higher + 1, higher + tied)
    candidate_count = scorer.candidate_count
    midrank = (rank[0] + rank[1]) / 2
    leader_index = (leaders & -leaders).bit_length() - 1
    differences = tuple(
        feature
        for feature in range(scorer.feature_count)
        if scorer.rows[leader_index][feature] != true_answers[feature]
    )
    return NoiseCaseResult(
        scenario_id=scenario.scenario_id,
        true_index=true_index,
        best_rank=rank[0],
        worst_rank=rank[1],
        midrank=midrank,
        percentile=(
            1.0
            if candidate_count == 1
            else 1 - ((midrank - 1) / (candidate_count - 1))
        ),
        top1_credit=_top_k_credit(rank, 1),
        top5_credit=_top_k_credit(rank, 5),
        top10_credit=_top_k_credit(rank, 10),
        candidate_survival_count=leaders.bit_count(),
        true_score_tie_size=tied,
        overtaking_candidate_count=higher,
        extra_tie_breakers=asked,
        perturbed_answer_count=count,
        perturbed_feature_indices=tuple(sorted(selected)),
        leading_competitor_difference_indices=differences,
        true_candidate_survived=bool(leaders & (1 << true_index)),
        stopping_criterion_reached=leaders.bit_count() == 1,
    )


def _add_weighted_bitmap(planes: list[int], bitmap: int, *, shift: int) -> None:
    plane = shift
    carry = bitmap
    while carry:
        while plane >= len(planes):
            planes.append(0)
        next_carry = planes[plane] & carry
        planes[plane] ^= carry
        carry = next_carry
        plane += 1


def _score_mask(planes: Sequence[int], score: int, universe_mask: int) -> int:
    if score >> len(planes):
        return 0
    mask = universe_mask
    for plane, bitmap in enumerate(planes):
        if score & (1 << plane):
            mask &= bitmap
        else:
            mask &= ~bitmap
    return mask & universe_mask


def _candidate_scaled_score(
    row: Sequence[Hashable], observations: Mapping[int, tuple[Hashable, ...] | None]
) -> int:
    score = 0
    for feature, labels in observations.items():
        if labels is None:
            continue
        if len(labels) == 1:
            score += 2 * int(row[feature] == labels[0])
        else:
            score += int(row[feature] in labels)
    return score
