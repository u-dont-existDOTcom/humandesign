"""Finite-decoy AstroHD null controls: profile-dependent first-place non-uniqueness."""

from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

TASK = Path(__file__).resolve().parents[2] / "tasks/astrohd-v15-structural-null-20261015"
sys.path.insert(0, str(TASK))
spec = importlib.util.spec_from_file_location("audit_panel_null", TASK / "audit_panel_null.py")
assert spec and spec.loader
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def test_synthetic_panel_preserves_score_ties_and_forced_rank_first():
    toy = Counter({0: 100, 47: 2, 63: 1})
    result = audit.audit_sample(toy)
    assert result["panel_decoys"] == 103
    assert result["all_coded_profile_combinations"] == 3125
    assert result["mathematically_forced_first_profiles"] == 956
    assert result["unscorable_zero_evidence"] == 324
    assert result["provisional_owner_development"]["structural_forced_first"]
    assert result["provisional_owner_development"]["rank_best"] == 1
    assert result["provisional_owner_development"]["other_candidate_ties"] == 3
    assert result["all_supported_control"]["other_candidate_ties"] == 1


def test_frozen_actual_panel_null_exactly_reproduces_aggregate():
    """This is an arithmetic fixture of a development panel, not a human experiment."""
    result = json.loads((TASK / "AGGREGATE_PANEL_RESULT.json").read_text())
    assert result["panel_decoys"] == 9999
    assert result["all_coded_profile_combinations"] == 3125
    assert result["scorable_profiles"] == 2801
    assert result["mathematically_forced_first_profiles"] == 956
    assert result["sample_rank_best_first_profiles"] == 1037
    assert result["sample_unique_first_profiles"] == 166
    assert result["sample_first_despite_negative_profiles"] == 81
    assert result["provisional_owner_development"]["rule_vote_signs"] == [1, 1, 1, 1, 0, 1]
    assert result["provisional_owner_development"]["rank_best"] == 1
    assert result["provisional_owner_development"]["other_candidate_ties"] == 0
    assert result["neutral_profile_count_is_not_population_prevalence"]
    assert result["not_a_full_century_scan"]
    assert result["no_private_birth_input_in_public_result"]


def test_invalid_feature_masks_rejected_instead_of_silent_skipping():
    import pytest

    for bad in (Counter({64: 1}), Counter({-1: 1}), Counter({1: -1})):
        with pytest.raises(ValueError):
            audit.audit_sample(bad)
