"""Synthetic-only date-aware Western chart/event null-scoring regression tests."""

from __future__ import annotations

import hashlib

import pytest

from hdmatch.astrology import western_private_natal_bridge as bridge
from hdmatch.astrology.western_event_only_scoring import (
    ChartPrediction,
    OutcomeRecord,
    PositiveEvent,
    build_positive_event_matrix,
    chart_from_sanitized_receipt,
    exploratory_label_permutation,
    positive_event_alignment,
)
from hdmatch.astrology.western_forward_blind import SOURCE_CANDIDATES, Interval

GOOD_DOMAIN = "documented_formal_role_gain"
BAD_DOMAIN = "documented_involuntary_role_loss"


def fixture_event(domain: str, lower: float, upper: float) -> PositiveEvent:
    return PositiveEvent(
        domain=domain,
        age=Interval(lower, upper),
        evidence_hash=hashlib.sha256(f"fictional-{domain}-{lower}".encode()).hexdigest(),
    )


def fixture_chart(label: str, low: float, high: float) -> ChartPrediction:
    return ChartPrediction(
        pseudonymous_chart=label,
        windows_by_domain=(
            (GOOD_DOMAIN, (Interval(low, high),)),
            (BAD_DOMAIN, ()),
        ),
        prediction_receipt_sha256=hashlib.sha256(label.encode()).hexdigest(),
    )


def test_identically_matched_two_chart_event_matrix_and_exact_null() -> None:
    cases = (
        OutcomeRecord("CASE-A", (fixture_event(GOOD_DOMAIN, 30.1, 30.2),)),
        OutcomeRecord("CASE-B", (fixture_event(GOOD_DOMAIN, 40.1, 40.2),)),
    )
    charts = (fixture_chart("CHART-X", 30, 31), fixture_chart("CHART-Y", 40, 41))
    matrix = build_positive_event_matrix(cases, charts)
    assert matrix["matrix"] == [[1.0, 0.0], [0.0, 1.0]]
    assert matrix["human_predictive_validity"] == "UNTESTED"
    assert matrix["event_counts_by_case"] == [1, 1]
    null = exploratory_label_permutation(
        matrix,
        externally_unblinded_true_chart_indices=[0, 1],
    )
    assert null["test"]["observed_diagonal_sum"] == 2.0
    assert null["test"]["permutation_null_probability_greater_or_equal"] == 0.5
    assert null["cohort_match_exchangeability_unproven"] is True
    assert null["absent_events_and_true_negatives_never_inferred"] is True
    assert "NOT_VALIDATED" in null["status"]


def test_year_only_uncertain_date_is_fractionally_credited_not_exact_day() -> None:
    case = OutcomeRecord("CASE-A", (fixture_event(GOOD_DOMAIN, 30, 31),))
    score = positive_event_alignment(case, fixture_chart("PRED", 30.5, 31.5))
    assert score["observed_positive_event_count"] == 1
    assert score["event_conditional_alignment"] == pytest.approx(0.5)
    assert score["partly_overlapping_uncertain_event_intervals"] == 1
    assert score["per_event"][0]["fraction_of_dated_event_interval_covered"] == 0.5


def test_two_overlapping_source_contacts_cannot_double_count_year_event() -> None:
    chart = ChartPrediction(
        pseudonymous_chart="CHART",
        windows_by_domain=((GOOD_DOMAIN, (Interval(30, 32),)),),
        prediction_receipt_sha256="a" * 64,
    )
    case = OutcomeRecord("CASE-A", (fixture_event(GOOD_DOMAIN, 30.2, 30.7),))
    assert positive_event_alignment(case, chart)["event_conditional_alignment"] == 1.0
    with pytest.raises(ValueError, match="sorted disjoint"):
        ChartPrediction("DUP", ((GOOD_DOMAIN, (Interval(30, 32), Interval(31, 33))),), "a" * 64)


def test_no_recorded_events_are_missing_evidence_not_true_negative() -> None:
    eventless = OutcomeRecord("SYN-NO-RECORD", ())
    chart = fixture_chart("CHART-A", 30, 32)
    assert positive_event_alignment(eventless, chart)["event_conditional_alignment"] is None
    outcome = build_positive_event_matrix(
        (eventless, OutcomeRecord("HAS-EVENT", (fixture_event(GOOD_DOMAIN, 30, 31),))),
        (chart, fixture_chart("CHART-B", 40, 41)),
    )
    assert outcome["status"] == "NOT_SCOREABLE_EVENTLESS_RECORDS_MUST_BE_REPORTED"
    assert outcome["positive_event_cases"] == 1
    assert outcome["matrix"] is None
    assert outcome["no_documented_event_cases"] == ["SYN-NO-RECORD"]
    with pytest.raises(ValueError, match="cannot score"):
        exploratory_label_permutation(outcome, externally_unblinded_true_chart_indices=[0, 1])


def _sealed_synthetic_receipt() -> dict:
    """Not a real natal chart; all fields are public invented code fixtures."""
    return {
        "schema": "PRIVATE_SOURCE_BOUND_WESTERN_DIAGNOSTIC_RECEIPT_V0",
        "private_input_digest_scheme": ("HMAC-SHA256_WITH_EXTERNAL_32_BYTE_OR_LONGER_KEY"),
        "human_predictive_accuracy": "UNTESTED",
        "method_contract": bridge.METHOD_SPEC,
        "source_rule_files_sha256": bridge.SOURCE_FILES,
        "ephemeris_source_sha256": bridge.EXPECTED_EPHEMERIS,
        "ephemeris_requested_and_returned_mode": ("SWIEPH verified for all seven classical bodies"),
        "sealed_diagnostic_receipt": {
            "schema": "WESTERN_DIRECTION_MODERN_DIAGNOSTIC_PREDICTION_RECEIPT_V0",
            "historical_Argolus_or_Lilly_exactness": "UNRESOLVED",
            "all_eight_source_candidate_ids": SOURCE_CANDIDATES,
            "windows": [
                {
                    "contact_key": "BODY-JUP-1",
                    "source_rule_id": "L1647-MC-JUP-BODY",
                    "reason": "TENTATIVE_MODERN_PILOT_CANDIDATE_NOT_HUMAN_MODEL_FROZEN",
                    "timing": {"start": 30.0, "end": 31.0},
                },
                {
                    "contact_key": "BODY-JUP-2",
                    "source_rule_id": "L1647-MC-JUP-BODY",
                    "reason": "TENTATIVE_MODERN_PILOT_CANDIDATE_NOT_HUMAN_MODEL_FROZEN",
                    "timing": {"start": 30.5, "end": 31.5},
                },
                {
                    "contact_key": "UNRESOLVED-RAY",
                    "source_rule_id": "L1647-MC-JUP-SOFT",
                    "reason": "UNSCORED_HISTORICAL_OR_MODERN_OUTCOME_CONDITION",
                    "timing": None,
                    "possible_range_for_review": {"start": 25, "end": 27},
                },
                {
                    "contact_key": "AMBIGUOUS-BIRTH",
                    "source_rule_id": "L1647-MC-SAT-BODY",
                    "reason": "CONTACT_DISAPPEARS_FOR_SOME_PLAUSIBLE_BIRTHTIMES",
                    "timing": None,
                },
            ],
        },
    }


def test_sanitized_receipt_maps_only_provisional_body_windows() -> None:
    chart = chart_from_sanitized_receipt(
        _sealed_synthetic_receipt(),
        pseudonymous_chart="TEST-CHART-C",
    )
    assert chart.windows_by_domain == (
        (GOOD_DOMAIN, (Interval(30, 31.5),)),
        (BAD_DOMAIN, ()),
    )
    assert len(chart.prediction_receipt_sha256) == 64


def test_reject_malicious_historically_unready_scoring_and_plain_hash() -> None:
    fixture = _sealed_synthetic_receipt()
    fixture["private_input_digest_scheme"] = "SHA256_UNSALTED_DOB"
    with pytest.raises(ValueError, match="privacy-safe"):
        chart_from_sanitized_receipt(fixture, pseudonymous_chart="TEST-CHART-C")

    fixture = _sealed_synthetic_receipt()
    unresolved = fixture["sealed_diagnostic_receipt"]["windows"][2]
    unresolved["timing"] = {"start": 25, "end": 27}
    with pytest.raises(ValueError, match="unresolved"):
        chart_from_sanitized_receipt(fixture, pseudonymous_chart="TEST-CHART-C")

    fixture = _sealed_synthetic_receipt()
    fixture["sealed_diagnostic_receipt"]["windows"][0]["contact_key"] = "BODY-JUP-2"
    with pytest.raises(ValueError, match="duplicate"):
        chart_from_sanitized_receipt(fixture, pseudonymous_chart="TEST-CHART-C")


def test_event_boundaries_invalid_unconfirmed_precision_and_bad_evidence_hash() -> None:
    with pytest.raises(ValueError, match="adult"):
        fixture_event(GOOD_DOMAIN, 16, 17)
    with pytest.raises(ValueError, match="unsupported"):
        fixture_event("freeform_joy", 30, 31)
    with pytest.raises(ValueError, match="SHA-256"):
        PositiveEvent(GOOD_DOMAIN, Interval(30, 31), "date_goes_here")
    with pytest.raises(ValueError, match="negative-event"):
        OutcomeRecord("CASE-A", (), "COMPLETE_NO_EVENTS_CONFIRMED")


def test_score_matrix_requires_distinct_cases_and_matched_chart_cohort() -> None:
    a = OutcomeRecord("CASE-A", (fixture_event(GOOD_DOMAIN, 30, 31),))
    x = fixture_chart("CHART-A", 30, 31)
    with pytest.raises(ValueError, match="n>=2"):
        build_positive_event_matrix((a,), (x,))
    with pytest.raises(ValueError, match="unique"):
        build_positive_event_matrix((a, a), (x, fixture_chart("CHART-B", 40, 41)))
    with pytest.raises(ValueError, match="unique"):
        build_positive_event_matrix(
            (a, OutcomeRecord("CASE-B", (fixture_event(GOOD_DOMAIN, 40, 41),))),
            (x, x),
        )


def test_duplicate_assessor_event_record_cannot_inflate_hit_count() -> None:
    first = fixture_event(GOOD_DOMAIN, 30, 31)
    with pytest.raises(ValueError, match="duplicate independent"):
        OutcomeRecord("CASE-WITH-TWICE-SAME-EVENT", (first, first))


def test_wrong_method_ephemeris_or_missing_original_sources_fail_closed() -> None:
    normal = _sealed_synthetic_receipt()
    for corrupted in [
        {**normal, "method_contract": {"geometry": "proportional_semi_arc"}},
        {**normal, "ephemeris_source_sha256": {}},
        {**normal, "source_rule_files_sha256": {}},
        {**normal, "ephemeris_requested_and_returned_mode": "MOSHIER"},
    ]:
        with pytest.raises(ValueError):
            chart_from_sanitized_receipt(corrupted, pseudonymous_chart="TEST-X")


def test_research_source_provenance_manifest_has_zero_actual_outcomes() -> None:
    import importlib.util
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    folder = root / "docs/astrology-research-map/western-event-only-blind-score-20261025"
    spec = importlib.util.spec_from_file_location(
        "western_event_score_source_manifest",
        folder / "build_verification.py",
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    saved = json.loads((folder / "VERIFICATION.json").read_text())
    assert mod.manifest() == saved
    assert saved["human_predictive_validity"] == "UNTESTED"
    assert saved["astro_databank_free_sample"] == "DISCOVERED_BINARY_NOT_DOWNLOADED"
    assert saved["read_any_real_event_nodes"] is False
    assert saved["actual_participants_or_events"] == 0
    for rel, meta in saved["file_sha256"].items():
        file = root / rel
        assert hashlib.sha256(file.read_bytes()).hexdigest() == meta["sha256"]
        assert file.stat().st_size == meta["bytes"]
