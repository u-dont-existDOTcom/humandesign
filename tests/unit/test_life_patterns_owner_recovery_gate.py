from __future__ import annotations

import json
from pathlib import Path

from hdmatch.evaluation.life_patterns_owner_recovery_gate import (
    OwnerRecoverySignature,
    evaluate_owner_recovery_regression,
)


BASELINE_PATH = Path("reference/research/life_patterns_astrohd_owner_recovery_baseline_v1.json")


def _baseline() -> OwnerRecoverySignature:
    payload = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    signature = payload["historical_signature"]
    return OwnerRecoverySignature(
        search_procedure_id=payload["search_procedure_id"],
        exact_recorded_rank_hourly=signature["exact_recorded_rank_hourly"],
        correct_date_top_distinct_refined_neighborhood=signature[
            "correct_date_top_distinct_refined_neighborhood"
        ],
        refined_peak_offset_minutes=signature["refined_peak_offset_minutes"],
    )


def test_historical_signature_passes_its_own_regression_gate() -> None:
    baseline = _baseline()

    result = evaluate_owner_recovery_regression(candidate=baseline, baseline=baseline)

    assert result.passed is True
    assert result.reasons == ()


def test_wrong_date_fails_even_when_rank_and_time_are_good() -> None:
    baseline = _baseline()
    candidate = baseline.model_copy(
        update={"correct_date_top_distinct_refined_neighborhood": False}
    )

    result = evaluate_owner_recovery_regression(candidate=candidate, baseline=baseline)

    assert result.passed is False
    assert result.correct_date_recovered is False


def test_worse_rank_fails() -> None:
    baseline = _baseline()
    candidate = baseline.model_copy(update={"exact_recorded_rank_hourly": 3})

    result = evaluate_owner_recovery_regression(candidate=candidate, baseline=baseline)

    assert result.passed is False
    assert result.exact_rank_not_worse is False


def test_larger_time_offset_fails() -> None:
    baseline = _baseline()
    candidate = baseline.model_copy(update={"refined_peak_offset_minutes": -12.0})

    result = evaluate_owner_recovery_regression(candidate=candidate, baseline=baseline)

    assert result.passed is False
    assert result.refined_time_not_worse is False


def test_different_search_procedure_cannot_claim_equivalence() -> None:
    baseline = _baseline()
    candidate = baseline.model_copy(update={"search_procedure_id": "different-procedure"})

    result = evaluate_owner_recovery_regression(candidate=candidate, baseline=baseline)

    assert result.passed is False
    assert result.same_search_procedure is False
