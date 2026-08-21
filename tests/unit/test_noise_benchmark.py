from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from hdmatch.evaluation.failures import FailureClassification, FailureRecord
from hdmatch.evaluation.metrics import (
    CaseRankMetrics,
    aggregate_rank_metrics,
    evaluate_ranked_case,
)
from hdmatch.evaluation.noise_benchmark import (
    DeclaredNoiseSettings,
    NoiseBenchmarkInputError,
    NoiseRunMetadata,
    NoiseTier,
    RevealedNoiseTierEvaluation,
    compare_revealed_noise_tiers,
)
from hdmatch.evaluation.report import EvaluationReport
from hdmatch.experiments.canonical import sha256_json

_HASH_A = "a" * 64
_HASH_B = "b" * 64
_HASH_C = "c" * 64
_HASH_D = "d" * 64
_HASH_E = "e" * 64
_HASH_F = "f" * 64


def _case_metric(case_id: str, true_rank: int) -> CaseRankMetrics:
    ranked_ids = [
        *(f"D{index}" for index in range(2, true_rank + 1)),
        "D1",
        *(f"D{index}" for index in range(true_rank + 1, 7)),
    ]
    candidates = [
        {"local_date": candidate_id, "date_score": float(6 - index)}
        for index, candidate_id in enumerate(ranked_ids)
    ]
    return evaluate_ranked_case(
        case_id=case_id,
        candidates=candidates,
        true_candidate_id="D1",
    )


def _evaluation(
    tier: NoiseTier,
    true_rank: int,
    *,
    unevaluable_case_id: str = "C2",
) -> EvaluationReport:
    case = _case_metric("C1", true_rank)
    failure = FailureRecord(
        case_id=unevaluable_case_id,
        classification=FailureClassification.SEARCH_BUG,
        explanation="The candidate universe omitted this case.",
        evidence={},
    )
    return EvaluationReport(
        experiment_id=f"EXP-{tier.value}",
        created_at_utc=datetime(2026, 8, 21, tzinfo=UTC),
        prediction_sha256=_HASH_A,
        freeze_sha256=_HASH_B,
        reveal_sha256=_HASH_C,
        blind_input_sha256=_HASH_D,
        model_sha256=_HASH_E,
        question_bank_sha256=_HASH_F,
        mapping_sha256=_HASH_A,
        revealed_target_set_sha256=_HASH_C,
        aggregate=aggregate_rank_metrics([case], total_case_count=2),
        cases=(case,),
        failures=(failure,),
        failure_counts={"search_bug": 1},
        restoration_curves=(),
        leave_one_cluster_out=(),
    )


def _settings(tier: NoiseTier) -> DeclaredNoiseSettings:
    values = {
        NoiseTier.ORACLE: (0.0, 0.0, 0.0, (1.0,), (1.0,)),
        NoiseTier.LOW: (0.05, 0.02, 0.0, (0.75, 1.0), (0.75, 1.0)),
        NoiseTier.MEDIUM: (0.15, 0.10, 0.10, (0.5, 0.75, 1.0), (0.5, 0.75, 1.0)),
        NoiseTier.ADVERSARIAL: (
            0.30,
            0.25,
            0.20,
            (0.25, 0.5, 0.75),
            (0.25, 0.5, 0.75),
        ),
    }[tier]
    return DeclaredNoiseSettings(
        missing_rate=values[0],
        flip_rate=values[1],
        cluster_dropout_rate=values[2],
        behavioral_confidence_values=values[3],
        measurement_reliability_values=values[4],
        conditioning="chart-independent-except-declared-measurement-domain",
    )


def _tier_evaluation(
    tier: NoiseTier,
    true_rank: int,
    *,
    model_id: str = "MODEL-A-CORE-V1",
    candidate_universe: str = "known_month",
    candidate_universe_sha256: str = _HASH_B,
    unevaluable_case_id: str = "C2",
    noise: DeclaredNoiseSettings | None = None,
) -> RevealedNoiseTierEvaluation:
    evaluation = _evaluation(tier, true_rank, unevaluable_case_id=unevaluable_case_id)
    metadata = NoiseRunMetadata(
        experiment_id=evaluation.experiment_id,
        tier=tier,
        model_id=model_id,
        model_sha256=evaluation.model_sha256,
        candidate_universe=candidate_universe,
        candidate_universe_sha256=candidate_universe_sha256,
        case_set_sha256=_HASH_C,
        declared_case_count=evaluation.aggregate.case_count,
        aggregation_rule="duration_weighted_evidence",
        run_manifest_sha256=_HASH_F,
        evaluation_sha256=sha256_json(evaluation),
        noise=noise or _settings(tier),
    )
    return RevealedNoiseTierEvaluation(metadata=metadata, evaluation=evaluation)


def _all_tiers() -> list[RevealedNoiseTierEvaluation]:
    return [
        _tier_evaluation(NoiseTier.ORACLE, 1),
        _tier_evaluation(NoiseTier.LOW, 2),
        _tier_evaluation(NoiseTier.MEDIUM, 4),
        _tier_evaluation(NoiseTier.ADVERSARIAL, 6),
    ]


def test_comparison_preserves_tiers_failures_unevaluable_and_declared_noise() -> None:
    report = compare_revealed_noise_tiers(tuple(reversed(_all_tiers())))

    assert [item.tier for item in report.tiers] == list(NoiseTier)
    assert report.claim_boundary == "synthetic-engineering-validation-only"
    assert report.case_count_policy == "fixed-declared-case-set-unevaluable-zero-credit"
    assert all(item.unevaluable_case_ids == ("C2",) for item in report.tiers)
    assert all(item.evaluated_case_ids == ("C1",) for item in report.tiers)
    assert all(item.failures == item.source.evaluation.failures for item in report.tiers)
    assert report.tiers[2].declared_noise.missing_rate == 0.15
    assert report.tiers[3].declared_noise.measurement_reliability_values == (
        0.25,
        0.5,
        0.75,
    )

    oracle, low, medium, adversarial = report.tiers
    assert oracle.degradation_from_oracle.top_1 == 0.0
    assert low.degradation_from_oracle.top_1 == pytest.approx(0.5)
    assert medium.degradation_from_oracle.top_3 == pytest.approx(0.5)
    assert adversarial.degradation_from_oracle.top_5 == pytest.approx(0.5)
    assert adversarial.degradation_from_oracle.mean_reciprocal_rank == pytest.approx(
        (1.0 / 2.0) - (1.0 / 12.0)
    )


@pytest.mark.parametrize(
    ("replacement", "expected"),
    [
        (
            _tier_evaluation(NoiseTier.LOW, 2, model_id="MODEL-B-DETAILED-V1"),
            "model_id",
        ),
        (
            _tier_evaluation(NoiseTier.LOW, 2, candidate_universe="known_date"),
            "candidate_universe",
        ),
        (
            _tier_evaluation(
                NoiseTier.LOW,
                2,
                candidate_universe_sha256=_HASH_D,
            ),
            "candidate_universe_sha256",
        ),
    ],
)
def test_comparison_rejects_incompatible_run_metadata(
    replacement: RevealedNoiseTierEvaluation, expected: str
) -> None:
    evaluations = _all_tiers()
    evaluations[1] = replacement

    with pytest.raises(NoiseBenchmarkInputError, match=expected):
        compare_revealed_noise_tiers(evaluations)


def test_comparison_requires_every_tier_once() -> None:
    with pytest.raises(NoiseBenchmarkInputError, match="missing required tiers"):
        compare_revealed_noise_tiers(_all_tiers()[:-1])

    duplicated = [*_all_tiers(), _tier_evaluation(NoiseTier.LOW, 2)]
    with pytest.raises(NoiseBenchmarkInputError, match="duplicate tier"):
        compare_revealed_noise_tiers(duplicated)


def test_comparison_rejects_changed_case_set_even_with_same_declared_hash() -> None:
    evaluations = _all_tiers()
    evaluations[-1] = _tier_evaluation(
        NoiseTier.ADVERSARIAL,
        6,
        unevaluable_case_id="C3",
    )

    with pytest.raises(NoiseBenchmarkInputError, match="oracle case set"):
        compare_revealed_noise_tiers(evaluations)


def test_tier_binding_rejects_wrong_denominator_or_evaluation_hash() -> None:
    evaluation = _evaluation(NoiseTier.LOW, 2)
    wrong_count = NoiseRunMetadata(
        experiment_id=evaluation.experiment_id,
        tier=NoiseTier.LOW,
        model_id="MODEL-A-CORE-V1",
        model_sha256=evaluation.model_sha256,
        candidate_universe="known_month",
        candidate_universe_sha256=_HASH_B,
        case_set_sha256=_HASH_C,
        declared_case_count=3,
        aggregation_rule="duration_weighted_evidence",
        run_manifest_sha256=_HASH_F,
        evaluation_sha256=sha256_json(evaluation),
        noise=_settings(NoiseTier.LOW),
    )
    with pytest.raises(ValidationError, match="declared case count"):
        RevealedNoiseTierEvaluation(metadata=wrong_count, evaluation=evaluation)

    wrong_hash = NoiseRunMetadata(
        experiment_id=evaluation.experiment_id,
        tier=NoiseTier.LOW,
        model_id="MODEL-A-CORE-V1",
        model_sha256=evaluation.model_sha256,
        candidate_universe="known_month",
        candidate_universe_sha256=_HASH_B,
        case_set_sha256=_HASH_C,
        declared_case_count=2,
        aggregation_rule="duration_weighted_evidence",
        run_manifest_sha256=_HASH_F,
        evaluation_sha256=_HASH_D,
        noise=_settings(NoiseTier.LOW),
    )
    with pytest.raises(ValidationError, match="evaluation_sha256"):
        RevealedNoiseTierEvaluation(metadata=wrong_hash, evaluation=evaluation)


def test_oracle_label_cannot_hide_noise_or_degraded_reliability() -> None:
    noisy_oracle = DeclaredNoiseSettings(
        missing_rate=0.01,
        flip_rate=0.0,
        cluster_dropout_rate=0.0,
        behavioral_confidence_values=(1.0,),
        measurement_reliability_values=(0.75,),
        conditioning="chart-independent-except-declared-measurement-domain",
    )
    evaluations = _all_tiers()
    evaluations[0] = _tier_evaluation(
        NoiseTier.ORACLE,
        1,
        noise=noisy_oracle,
    )

    with pytest.raises(NoiseBenchmarkInputError, match="zero noise and unit reliability"):
        compare_revealed_noise_tiers(evaluations)
