"""Modern diagnostic Western pilot: strict engineering tests, no human data."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import pytest

from hdmatch.astrology.western_forward_blind import (
    DIAGNOSTIC_NAME,
    NOT_READY_REASONS,
    SOURCE_CANDIDATES,
    TENTATIVE_PILOT_PRIMARY,
    Contact,
    Interval,
    contact_uncertainty_envelopes,
    eligible_exposure,
    interval_intersection,
    label_permutation_null,
    measure_intervals,
    merged_intervals,
    sealed_prediction_receipt,
)


def test_full_historical_candidate_registry_not_cherry_picked() -> None:
    assert DIAGNOSTIC_NAME == "WESTERN_PRIMARY_DIRECTIONS_MODERN_DIAGNOSTIC_V0"
    assert len(SOURCE_CANDIDATES) == 8
    assert len(set(SOURCE_CANDIDATES)) == 8
    assert len(TENTATIVE_PILOT_PRIMARY) == 2
    assert len(NOT_READY_REASONS) == 6
    assert set(TENTATIVE_PILOT_PRIMARY) | set(NOT_READY_REASONS) == set(SOURCE_CANDIDATES)
    assert "L1647-MC-JUP-SOFT" in NOT_READY_REASONS
    source = Path(__file__).resolve().parents[2] / (
        "docs/astrology-research-map/primary-direction-event-hypotheses-20261024"
    )
    original = json.loads((source / "LILLY_1647_EVENT_CANDIDATES.json").read_text())
    aspects = json.loads((source / "ASPECT_SOURCE_COVERAGE_DIAGNOSTIC.json").read_text())
    names = {entry["id"] for entry in original["source_to_construct_rules"]}
    names.update(entry["id"] for entry in aspects["families"])
    assert names == set(SOURCE_CANDIDATES)


def test_half_open_interval_union_does_not_double_count_overlapping_contacts() -> None:
    domain = Interval(18, 65)
    windows = [Interval(19, 21), Interval(20, 23), Interval(30, 32), Interval(31, 33)]
    assert merged_intervals(windows, domain) == (Interval(19, 23), Interval(30, 33))
    assert measure_intervals(windows, domain) == 7.0
    assert measure_intervals([Interval(10, 19), Interval(64, 70)], domain) == 2
    with pytest.raises(ValueError):
        Interval(2, 2)
    with pytest.raises(ValueError):
        Interval(math.inf, 3)


def test_eligibility_and_ascertainment_change_denominator_explicitly() -> None:
    forecast = [Interval(19, 21), Interval(20, 23), Interval(29, 32)]
    eligible = [Interval(18, 26), Interval(30, 35)]
    independently_coded = [Interval(20, 25), Interval(32, 35)]
    result = eligible_exposure(forecast, eligible, independently_coded)
    assert result["assessed_eligible_years"] == 8
    assert result["direction_exposure_years"] == 3
    assert result["unexposed_eligible_years"] == 5
    assert result["fraction_of_eligible_years_exposed"] == pytest.approx(3 / 8)
    assert result["status"] == "EXPOSURE_ONLY_NOT_EVENT_PROBABILITY"
    assert eligible_exposure([Interval(20, 21)], [], [])["status"] == "UNASCERTAINED"
    assert interval_intersection([Interval(0, 1)], [Interval(2, 4)]) == ()


def test_full_discrete_minute_uncertainty_envelope_no_best_minute_selection() -> None:
    rule = "L1647-MC-JUP-BODY"
    samples = {
        -1: [Contact("same", rule, 29.75)],
        0: [Contact("same", rule, 30.0)],
        1: [Contact("same", rule, 30.25)],
    }
    result = contact_uncertainty_envelopes(samples)
    assert len(result) == 1
    assert result[0].timing == Interval(29.25, 30.75)
    assert result[0].sampled_birth_minute_offsets == (-1, 0, 1)
    assert result[0].historical_model_ready is False
    assert result[0].reason == "TENTATIVE_MODERN_PILOT_CANDIDATE_NOT_HUMAN_MODEL_FROZEN"


def test_missing_contact_at_any_plausible_minute_remains_unscoreable() -> None:
    items = contact_uncertainty_envelopes(
        {
            -1: [Contact("x", "L1647-MC-SAT-BODY", 40)],
            0: [],
            1: [Contact("x", "L1647-MC-SAT-BODY", 40.5)],
        }
    )
    assert items[0].timing is None
    assert items[0].possible_range_for_review == Interval(39.5, 41.0)
    assert items[0].reason == "CONTACT_DISAPPEARS_FOR_SOME_PLAUSIBLE_BIRTHTIMES"


def test_unspecified_historical_conditions_remain_unscored() -> None:
    result = contact_uncertainty_envelopes({0: [Contact("jup-sof", "L1647-MC-JUP-SOFT", 45)]})
    assert result[0].reason == "UNSCORED_HISTORICAL_OR_MODERN_OUTCOME_CONDITION"
    assert result[0].timing is None
    assert result[0].possible_range_for_review == Interval(44.5, 45.5)
    assert result[0].historical_model_ready is False


def test_timing_samples_reject_cherry_picked_minutes_and_duplicate_contacts() -> None:
    jup = Contact("x", "L1647-MC-JUP-BODY", 31)
    for bad in [
        {-5: [jup], 0: [jup], 5: [jup]},
        {-2: [jup], -1: [jup], 0: [jup]},
        {1: [jup]},
    ]:
        with pytest.raises(ValueError):
            contact_uncertainty_envelopes(bad)
    with pytest.raises(ValueError, match="duplicate"):
        contact_uncertainty_envelopes({0: [jup, jup]})
    with pytest.raises(ValueError, match="same contact identity"):
        contact_uncertainty_envelopes(
            {-1: [jup], 0: [Contact("x", "L1647-MC-SAT-BODY", 31)], 1: [jup]}
        )


def test_permutation_null_exact_and_ties_conservative() -> None:
    good = label_permutation_null([[1, 0], [0, 1]], [0, 1])
    assert good["null_method"] == "EXACT_N_FACTORIAL_LABEL_PERMUTATION"
    assert good["observed_diagonal_sum"] == 2
    assert good["null_assignments_examined"] == 2
    assert good["permutation_null_probability_greater_or_equal"] == 0.5
    assert (
        label_permutation_null([[0, 0], [0, 0]], [0, 1])[
            "permutation_null_probability_greater_or_equal"
        ]
        == 1.0
    )


def test_label_permutation_rejects_incomplete_or_tainted_matrix() -> None:
    for a, b in [
        ([[0]], [0]),
        ([[0, 1], [1]], [0, 1]),
        ([[1, float("nan")], [1, 2]], [0, 1]),
        ([[1, 2], [0, 1]], [0, 0]),
    ]:
        with pytest.raises(ValueError):
            label_permutation_null(a, b)


def test_monte_carlo_null_is_seeded_and_reproducible_for_nine_plus() -> None:
    matrix = [[float(i == j) for j in range(9)] for i in range(9)]
    first = label_permutation_null(matrix, list(range(9)), seed=55, monte_carlo_draws=250)
    second = label_permutation_null(matrix, list(range(9)), seed=55, monte_carlo_draws=250)
    assert first == second
    assert first["null_method"] == "FIXED_SEED_MONTE_CARLO_WITH_ADD_ONE_CORRECTION"
    assert 0 < first["permutation_null_probability_greater_or_equal"] <= 1
    assert first["null_assignments_examined"] == 250


def test_pre_outcome_commitment_is_canonical_and_never_contains_birth_or_events() -> None:
    source = Contact("CASE-001-JUP", "L1647-MC-JUP-BODY", 32)
    windows = contact_uncertainty_envelopes({0: [source]})
    proof = "a" * 64
    kwargs = {
        "pseudonymous_participant_id": "TEST-SYNTHETIC-NO-HUMAN",
        "birth_input_sha256": proof,
        "chart_features_sha256": "b" * 64,
        "calculation_code_sha256": "c" * 64,
        "rules_sha256": "d" * 64,
        "birth_time_quality": "certified_minute",
        "windows": windows,
        "comparison_design_sha256": "e" * 64,
    }
    a = sealed_prediction_receipt(**kwargs)
    b = sealed_prediction_receipt(**kwargs)
    assert a == b
    assert a["human_predictive_accuracy"] == "UNTESTED"
    assert a["historical_Argolus_or_Lilly_exactness"] == "UNRESOLVED"
    assert len(a["all_eight_source_candidate_ids"]) == 8
    assert len(a["other_source_candidate_statuses"]) == 6
    asserted_hash = a.pop("commitment_sha256")
    from hdmatch.astrology.western_forward_blind import canonical

    assert hashlib.sha256(canonical(a)).hexdigest() == asserted_hash
    serialized = canonical(a).decode("utf-8").lower()
    assert "date_of_birth" not in serialized
    assert "birth_place" not in serialized
    assert "medical" not in serialized
    assert "outcome_answers" not in serialized

    with pytest.raises(ValueError, match="SHA-256"):
        sealed_prediction_receipt(**{**kwargs, "birth_input_sha256": "BAD"})
    with pytest.raises(ValueError, match="quality"):
        sealed_prediction_receipt(**{**kwargs, "birth_time_quality": "unspecified"})


def test_original_96_chart_synthetic_exposure_inputs_remain_compatible() -> None:
    parent = Path(__file__).resolve().parents[2] / (
        "docs/astrology-research-map/primary-direction-synthetic-panel-20261024"
    )
    cases = json.loads((parent / "SYNTHETIC_PANEL_EXPOSURES.json").read_text())
    assert len(cases) == 96
    envelopes = []
    for contacts in cases.values():
        source_contacts = [
            Contact(
                key=record["key"],
                rule_id=record["rule_id"],
                symbolic_age_years=record["age"],
            )
            for record in contacts
        ]
        envelopes.extend(contact_uncertainty_envelopes({0: source_contacts}))
    assert len(envelopes) == 216
    assert all(x.historical_model_ready is False for x in envelopes)
    assert all(x.source_rule_id in SOURCE_CANDIDATES for x in envelopes)
    # This is input compatibility only; it does NOT recreate the 96 charts,
    # score known people's events, or claim predictive validation.


def test_feasibility_exactly_reuses_original_96_chart_source_records() -> None:
    import importlib.util

    root = Path(__file__).resolve().parents[2]
    folder = root / "docs/astrology-research-map/western-primary-direction-blind-pilot-20261025"
    spec = importlib.util.spec_from_file_location(
        "source_only_western_pilot_demo", folder / "build_synthetic_pilot_feasibility.py"
    )
    assert spec and spec.loader
    demo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(demo)
    result = json.loads((folder / "SYNTHETIC_PILOT_FEASIBILITY.json").read_text())
    assert json.loads(demo.canonical(demo.build())) == result
    assert result["existing_frozen_96_synthetic_charts"] == 96
    assert sum(result["all_eight_source_candidate_contacts"].values()) == 216
    assert result["tentative_two_occupational_contact_counts"] == {
        "L1647-MC-JUP-BODY": 9,
        "L1647-MC-SAT-BODY": 11,
    }
    assert result["fraction_of_unconditional_age_interval_exposed"] == pytest.approx(
        0.004232710829565605,
    )
    assert result["source_qualified_historical_prediction_accuracy"] == "UNTESTED"
    assert result["actual_role_opportunity_or_documented_outcomes"] == "NONE"


def test_current_pilot_integrity_manifest_proves_no_human_outcomes() -> None:
    import importlib.util

    root = Path(__file__).resolve().parents[2]
    folder = root / "docs/astrology-research-map/western-primary-direction-blind-pilot-20261025"
    spec = importlib.util.spec_from_file_location(
        "verified_modern_western_scaffold", folder / "build_verification.py"
    )
    assert spec and spec.loader
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    saved = json.loads((folder / "VERIFICATION.json").read_text())
    assert verifier.build() == saved
    assert saved["real_participants_or_events_used"] is False
    assert saved["actual_trial_ready"] is False
    assert saved["empirical_predictive_validity"] == "UNTESTED"
    for path, proof in saved["file_hashes"].items():
        f = root / path
        assert f.stat().st_size == proof["bytes"]
        assert hashlib.sha256(f.read_bytes()).hexdigest() == proof["sha256"]
