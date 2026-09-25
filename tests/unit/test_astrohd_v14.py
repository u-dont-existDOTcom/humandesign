"""Executable regressions for owner-authorized cross-book development."""
from pathlib import Path
import copy
import sys
from types import SimpleNamespace
import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from owner_method_admission import admit
from run_astrohd_v14_staged import default_config, operation_projection, sparse_fit, ranking
from run_astrohd_v14_mixed import fit_mixed
from screen_astrohd_v14_century import interpolate, house_possible
from hdmatch.evaluation.astrohd_v14_rules import conditions, deduplicate


def test_combination_succeeds_without_either_book_succeeding_alone():
    x = np.array([[1, 1], [1, 0], [0, 1]], dtype=np.int8)
    result = fit_mixed(x, [{"source_id": "A"}, {"source_id": "B"}])
    assert result["selected_count"] == 2
    assert result["minimum_cardinality_certified"]
    assert all(np.any(x[1:, i] == x[0, i]) for i in (0, 1))
    assert np.all(x[0].sum() > x[1:].sum(axis=1))


def test_neutral_other_book_column_not_pruned_by_composition_solver():
    x = np.array([[1, 0], [0, 0]], dtype=np.int8)
    result = fit_mixed(x, [{"source_id": "A"}, {"source_id": "B"}])
    assert result["selected_count"] == 2
    # Membership alone does not prove the second book adds predictive value.
    assert x[0, 1] == x[1, 1]


def test_indistinguishable_times_remain_ties():
    x = np.array([[1, 1], [1, 1], [1, 0], [0, 1]], dtype=np.int8)
    result = sparse_fit(x, default_config([4]))
    assert result["full_library_identical_competitor_indices"] == [1]
    assert not result["minute_identified"]
    rows = [{"utc": str(i)} for i in range(4)]
    rank = ranking(x, result["selection"], rows)
    assert (rank["rank_best"], rank["rank_worst"]) == (1, 2)


def test_actual_config_change_is_rejected_before_execution():
    config = default_config([100, 1000])
    contract = {"owner_outcome_id": "astrohd-owner-cross-rulebook-v14-20260924",
                "protected_dimensions": copy.deepcopy(operation_projection(config)["protected_dimensions"]),
                "required_operations": ["raw_stack", "lineage_dedup", "nested_challenges"]}
    admit(contract, operation_projection(config))
    config["composition"] = "each_book_must_independently_succeed"
    with pytest.raises(ValueError, match="OWNER_DIMENSION_CHANGED"):
        admit(contract, operation_projection(config))


def test_source_directional_rule_uses_sidereal_houses():
    snapshot = SimpleNamespace(sidereal_longitudes={"venus": 340.0},
        sidereal_whole_houses={"venus": 4}, sidereal_speeds={"venus": 1.0}, day_chart=False)
    result = conditions(snapshot, "phaladeepika", "venus")
    assert result["directional"] == result["exaltation"] == 1
    snapshot.sidereal_whole_houses["venus"] = 10
    assert conditions(snapshot, "phaladeepika", "venus")["directional"] == 0


def test_lineage_dedup_keeps_distinct_operational_rule():
    rows = [{"rule_id": key, "lineage_key": lineage, "supported_domain_ids": []}
            for key, lineage in [("A", "same"), ("B", "same"), ("C", "different")]]
    result = deduplicate(rows)
    assert len(result) == 2
    assert result[0]["contributing_rule_ids"] == ["A", "B"]


def test_cache_last_endpoint_is_not_penultimate_value():
    result = interpolate((np.array([350.0, 370.0, 390.0]), 3.0), 0.0, np.array([0.25]))
    assert result[0] == 30.0


def test_numerical_house_guard_handles_zero_degree_wrap():
    cusps = np.array([[350, 20, 50, 80, 110, 140, 170, 200, 230, 260, 290, 320]], dtype=float)
    assert house_possible(np.array([0.0]), cusps, 1)[0]
    assert not house_possible(np.array([180.0]), cusps, 1)[0]
