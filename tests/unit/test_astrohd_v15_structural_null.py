"""Proof-level AstroHD five-domain/six-clause null controls (no astronomy needed)."""

from __future__ import annotations

import importlib.util
import itertools
import math
from pathlib import Path

import pytest

TASK = Path(__file__).resolve().parents[2] / "tasks/astrohd-v15-structural-null-20261015"
spec = importlib.util.spec_from_file_location("structural_null", TASK / "audit_structural_null.py")
assert spec and spec.loader
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def test_exhaustive_five_domain_state_space_and_forced_winner_count():
    summary = audit.enumerate_profiles()
    assert summary["total_profiles"] == 5**5 == 3125
    assert summary["unscorable_zero_evidence"] == 324
    assert summary["scorable_forced_first"] == 956
    assert summary["not_guaranteed_first"] == 1845
    assert summary["includes_contradictory_clause"] == 1845
    assert summary["distinct_reachable_clause_vectors"] == 162
    assert summary["forced_first_fraction_of_all_profiles"] == pytest.approx(0.30592)


def test_all_nonnegative_scored_signs_force_full_signature_first():
    # This is a proof over the entire six-bit mask space, not sampled dates.
    for signs in itertools.product((0, 1), repeat=6):
        state = audit.signature_stats(signs)
        if signs == (0,) * 6:
            assert not state["scoreable"]
            assert not state["guaranteed_joint_first_with_any_candidate_panel"]
            continue
        assert state["guaranteed_joint_first_with_any_candidate_panel"]
        assert state["target_best_rank_in_complete_mask_space"] == 1
        assert state["target_score"] == state["maximum_score_any_six_bit_mask"]
        # For every abstention there is one extra unconstrained bit.
        assert state["target_ties_in_complete_mask_space"] == 2 ** signs.count(0)


def test_a_negative_sign_defeats_full_signature_in_complete_mask_space():
    # Present negatives reduce the target score; there exists a mask omitting them.
    for signs in itertools.product((-1, 0, 1), repeat=6):
        if -1 not in signs:
            continue
        target = audit.signature_stats(signs)
        assert target["target_best_rank_in_complete_mask_space"] > 1
        assert not target["guaranteed_joint_first_with_any_candidate_panel"]


def test_submitted_case_has_only_three_supported_domains_and_two_maximizing_masks():
    signs = audit.decoder.answer_signs(audit.OWNER_PROVISIONAL_PROFILE)
    assert signs == (1, 1, 1, 1, 0, 1)
    assert sum(v == "supported" for v in audit.OWNER_PROVISIONAL_PROFILE.values()) == 3
    target = audit.signature_stats(signs)
    assert target["target_score"] == 5
    assert target["winning_masks"] == (47, 63)
    assert target["target_ties_in_complete_mask_space"] == 2
    assert target["guaranteed_joint_first_with_any_candidate_panel"]


def test_frozen_century_bins_prove_bounds_without_another_scan():
    summary = audit.report()
    data = summary["century_tie_bounds_for_five_positive_one_abstention"]
    assert data["source_verified_total_minute_grid"] == 52_596_001
    assert data["source_verified_six_clause_maxima"] == 9
    assert data["five_active_clause_winner_count_lower_bound"] == 9
    assert data["five_active_clause_winner_count_upper_bound"] == 624
    assert data["minimum_other_tied_minutes"] == 8
    assert data["maximum_other_tied_minutes"] == 623
    assert data["probability_no_ties_if_uniform_sample_lower_bound"] == pytest.approx(
        0.8882960630251989, abs=1e-12
    )
    assert data["probability_no_ties_if_uniform_sample_upper_bound"] == pytest.approx(
        0.998480135367564, abs=1e-12
    )
    assert summary["model_hash_matches_frozen_century"]
    assert not summary["provisional_profile_participant_confirmed"]


def test_no_tie_sampling_math_and_input_rejection():
    assert (
        audit.no_tie_probability(
            other_minutes=0, comparison_minutes=9999, candidate_pool_without_target=52_596_000
        )
        == 1
    )
    assert (
        audit.no_tie_probability(
            other_minutes=5, comparison_minutes=6, candidate_pool_without_target=10
        )
        == 0.0
    )
    # Full coverage of a finite pool cannot miss an existing tie.
    assert (
        audit.no_tie_probability(
            other_minutes=1, comparison_minutes=10, candidate_pool_without_target=10
        )
        == 0.0
    )
    assert math.isclose(
        audit.no_tie_probability(
            other_minutes=1, comparison_minutes=2, candidate_pool_without_target=10
        ),
        9 / 10 * 8 / 9,
    )
    with pytest.raises(ValueError):
        audit.no_tie_probability(
            other_minutes=-1, comparison_minutes=10, candidate_pool_without_target=10
        )


def test_mutated_scan_receipt_not_accepted():
    import json

    bad = json.loads(audit.SIX_SCAN.read_text())
    bad["verification"]["aggregate_rejection_and_maximum_counts"][5] += 1
    with pytest.raises(ValueError, match="not admissible"):
        audit.century_bounds(bad)


def test_report_contains_no_personal_birth_input_and_no_false_claim():
    report = audit.report()
    assert report["classification"] == "EXACT_COMBINATORIAL_DEVELOPMENT_AUDIT_NOT_HUMAN_VALIDATION"
    assert report["no_personal_data_in_artifact"] is True
    assert report["zero_extra_astro_scans"] is True
    assert report["provisional_signs"] == [1, 1, 1, 1, 0, 1]
    assert "birth" not in report["target_feature_mask"].lower()
