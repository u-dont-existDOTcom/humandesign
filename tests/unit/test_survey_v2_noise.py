from __future__ import annotations

from hdmatch.evaluation.survey_v2_noise import (
    NoiseScenario,
    simulate_noise_case,
    summarize_noise_cases,
)


def test_wrong_answer_rescores_full_universe_and_preserves_blind_stopping() -> None:
    rows = (("a", 1, "x"), ("b", 1, "y"), ("b", 2, "x"))
    case = simulate_noise_case(
        rows,
        base_feature_count=2,
        true_index=0,
        scenario=NoiseScenario(
            scenario_id="one-wrong", perturbation="wrong", fraction=0, minimum_perturbed_answers=1
        ),
    )
    assert case.best_rank >= 1
    assert case.worst_rank <= 3
    assert case.perturbed_answer_count == 1
    assert case.target_blind_stopping
    assert not case.selection_uses_true_candidate


def test_other_abstains_and_mixed_is_partial_not_forced_choice() -> None:
    rows = (("a", "x"), ("b", "x"), ("b", "y"))
    other = simulate_noise_case(
        rows,
        base_feature_count=1,
        true_index=0,
        scenario=NoiseScenario(
            scenario_id="other", perturbation="other", fraction=1
        ),
    )
    mixed = simulate_noise_case(
        rows,
        base_feature_count=1,
        true_index=0,
        scenario=NoiseScenario(
            scenario_id="mixed", perturbation="mixed", fraction=1
        ),
    )
    assert other.extra_tie_breakers == 1
    assert mixed.perturbed_answer_count == 1
    summary = summarize_noise_cases((other,))
    assert summary.case_count == 1
    assert 0 <= summary.top10 <= 1
