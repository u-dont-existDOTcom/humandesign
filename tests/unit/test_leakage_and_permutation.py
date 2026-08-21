from __future__ import annotations

import pytest

from hdmatch.evaluation.leakage import (
    LeakageDetectedError,
    assert_no_blind_leakage,
    assert_no_prediction_leakage,
    scan_blind_payload,
    scan_prediction_payload,
)
from hdmatch.evaluation.permutation import (
    empirical_p_value,
    generate_null_assignments,
    permutation_test,
    stratified_permutation,
)


def _safe_blind_payload() -> dict[str, object]:
    return {
        "schema_version": "blind-cases-v1",
        "cases": [
            {
                "case_id": "C1",
                "known_birth_year": 2000,
                "known_birth_month": 1,
                "candidate_universe": "known_month",
                "iana_timezone": "Europe/Istanbul",
                "responses": [
                    {
                        "question_id": "Q1",
                        "answer": "A",
                        "example_text": "I focus best in quiet places.",
                    }
                ],
            }
        ],
    }


def test_leakage_scanner_allows_declared_month_year_but_finds_secrets_dates_and_paths() -> None:
    assert scan_blind_payload(_safe_blind_payload()).passed

    payload = _safe_blind_payload()
    case = payload["cases"][0]  # type: ignore[index]
    case["true_local_date"] = "2000-01-02"  # type: ignore[index]
    case["responses"][0]["example_text"] = (  # type: ignore[index]
        "Born on January 2; details are in /home/evaluator/answer_key.json."
    )
    report = scan_blind_payload(payload)
    assert not report.passed
    codes = {finding.code for finding in report.findings}
    assert "secret-field" in codes
    assert "written-date-clue" in codes
    assert "absolute-path-leak" in codes
    assert "secret-artifact-path" in codes
    with pytest.raises(LeakageDetectedError):
        assert_no_blind_leakage(payload)


def test_known_birth_day_allowed_only_for_known_date_universe() -> None:
    known_date = {
        "case_id": "C",
        "candidate_universe": "known_date",
        "known_birth_year": 2000,
        "known_birth_month": 1,
        "known_birth_day": 2,
        "responses": [],
    }
    assert scan_blind_payload(known_date).passed
    known_date["candidate_universe"] = "known_month"
    assert not scan_blind_payload(known_date).passed


def test_prediction_scan_rejects_truth_derived_ranks_and_hidden_identifiers() -> None:
    safe = {
        "schema_version": "predictions-v1",
        "predictions": [
            {
                "case_id": "C1",
                "ranked_dates": [
                    {
                        "local_date": "2000-01-02",
                        "date_rank": 1,
                        "date_score": 3.0,
                        "best_state": {
                            "state_id": "S1",
                            "start_utc": "2000-01-02T00:00:00Z",
                            "end_utc": "2000-01-02T01:00:00Z",
                        },
                    }
                ],
                "zero_cluster": {"ranked_dates": []},
            }
        ],
    }
    assert scan_prediction_payload(safe).passed
    contaminated = {
        **safe,
        "predictions": [
            {
                **safe["predictions"][0],  # type: ignore[index]
                "true_date_rank": 1,
                "true_utc": "2000-01-02T00:00:00Z",
                "hidden_state_id": "S1",
            }
        ],
    }
    report = scan_prediction_payload(contaminated)
    assert not report.passed
    assert {item.code for item in report.findings} == {"truth-derived-prediction-field"}
    with pytest.raises(LeakageDetectedError):
        assert_no_prediction_leakage(contaminated)


def test_stratified_permutation_is_reproducible_person_level_and_stratum_safe() -> None:
    people = ["P1", "P2", "P3", "P4"]
    strata = {"P1": "A", "P2": "A", "P3": "B", "P4": "B"}
    first = stratified_permutation(people, strata=strata, seed=7)
    second = stratified_permutation(people, strata=strata, seed=7)
    assert first == second
    assert set(first) == set(people)
    assert set(first.values()) == set(people)
    assert all(strata[person] == strata[donor] for person, donor in first.items())
    with pytest.raises(ValueError, match="unique"):
        stratified_permutation(["P1", "P1"], seed=1)


def test_permutation_null_uses_plus_one_p_value_and_reports_singletons() -> None:
    assert empirical_p_value(10, [1, 2, 3], alternative="greater") == 0.25
    assignments = generate_null_assignments(["P1", "P2"], permutations=4, seed=3)
    assert len(assignments) == 4
    result = permutation_test(
        ["P1", "P2", "P3"],
        observed_statistic=1.0,
        statistic_for_assignment=lambda assignment: float(
            sum(person == donor for person, donor in assignment.items())
        ),
        strata={"P1": "A", "P2": "A", "P3": "singleton"},
        permutations=25,
        seed=10,
    )
    assert result.permutations == 25
    assert result.fixed_singleton_strata == ("singleton",)
    assert 0 < result.p_value <= 1
