from __future__ import annotations

import inspect
from itertools import product

from hdmatch.evaluation.survey_v2_noise import (
    DEFAULT_NOISE_SCENARIOS,
    NoiseScenario,
    _scores,
    simulate_noise_case,
)
from hdmatch.evaluation.survey_v2_noise_indexed import (
    IndexedSurveyScorer,
    simulate_noise_case_indexed,
)

UNIVERSES = (
    ((0, 0, "a"), (0, 0, "a")),
    ((0, 0, "a"), (0, 0, "b"), (0, 1, "a")),
    tuple(product((0, 1), repeat=4)),
    (
        (0, 0, "a", "late-1"),
        (0, 0, "a", "late-2"),
        (1, 0, "b", "late-1"),
        (1, 1, "b", "late-2"),
    ),
)


def test_indexed_scorer_exhaustively_matches_reference_scenarios() -> None:
    scenarios = DEFAULT_NOISE_SCENARIOS + (
        NoiseScenario(
            scenario_id="all-other", perturbation="other", fraction=1.0
        ),
        NoiseScenario(
            scenario_id="all-mixed", perturbation="mixed", fraction=1.0
        ),
    )
    for rows in UNIVERSES:
        scorer = IndexedSurveyScorer.build(rows)
        base_count = len(rows[0]) - 1
        for scenario in scenarios:
            for true_index in range(len(rows)):
                reference = simulate_noise_case(
                    rows,
                    base_feature_count=base_count,
                    true_index=true_index,
                    scenario=scenario,
                )
                indexed = simulate_noise_case_indexed(
                    scorer,
                    base_feature_count=base_count,
                    true_index=true_index,
                    scenario=scenario,
                )
                assert indexed == reference


def test_bit_sliced_histogram_matches_every_reference_candidate_score() -> None:
    rows = UNIVERSES[-1]
    scorer = IndexedSurveyScorer.build(rows)
    observation_sets = (
        {0: (0,), 1: (0,), 2: ("a",)},
        {0: None, 1: (1,), 2: ("a", "b")},
        {0: (1,), 1: None, 2: None, 3: ("late-2",)},
    )
    for observations in observation_sets:
        reference = _scores(rows, observations)
        counts, masks = scorer.score_histogram(observations)
        reconstructed = [0.0] * len(rows)
        for scaled_score, mask in enumerate(masks):
            for candidate_index in range(len(rows)):
                if mask & (1 << candidate_index):
                    reconstructed[candidate_index] = scaled_score / 2
        assert reconstructed == reference
        assert sum(counts) == len(rows)


def test_indexed_selector_has_no_birth_target_rank_or_prose_inputs() -> None:
    selector_parameters = set(inspect.signature(IndexedSurveyScorer.select_by_entropy).parameters)
    simulation_parameters = set(inspect.signature(simulate_noise_case_indexed).parameters)
    forbidden = {
        "birth_date",
        "birth_time",
        "birth_place",
        "target_rank",
        "participant_prose",
        "post_reveal_evidence",
    }
    assert selector_parameters.isdisjoint(forbidden | {"true_index"})
    assert simulation_parameters.isdisjoint(forbidden)
