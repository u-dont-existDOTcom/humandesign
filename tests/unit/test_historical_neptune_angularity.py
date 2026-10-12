"""Synthetic-only checks: a historical orb definition is not trait evidence."""

import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest

MODULE = (
    Path(__file__).resolve().parents[2]
    / "tasks/life-patterns-context-specificity-20261012/neptune_angularity_theory.py"
)
spec = spec_from_file_location("historical_neptune_rule", MODULE)
assert spec is not None and spec.loader is not None
mod = module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def test_twelve_house_six_degree_rule_and_wrapped_signs():
    within = mod.twelfth_side_neptune_near_ascendant(280, 274.5, 12)
    assert within.qualified and within.signed_before_ascendant_degrees == 5.5
    assert within.interpretive_status == "THEORY_ONLY_NOT_PREDICTIVE_EVIDENCE"
    assert mod.twelfth_side_neptune_near_ascendant(2, 357, 12).qualified
    assert not mod.twelfth_side_neptune_near_ascendant(280, 273.9, 12).qualified
    assert not mod.twelfth_side_neptune_near_ascendant(280, 274.5, 1).qualified
    assert not mod.twelfth_side_neptune_near_ascendant(274.5, 280, 12).qualified


def test_no_birth_data_or_clinical_inference_in_geometric_result():
    obj = mod.twelfth_side_neptune_near_ascendant(278, 273, 12)
    assert set(obj.__dataclass_fields__) == {
        "qualified",
        "signed_before_ascendant_degrees",
        "actual_house",
        "maximum_orb_degrees",
        "interpretive_status",
    }
    for invalid in (-1, 0, 30, 100):
        with pytest.raises(ValueError):
            mod.twelfth_side_neptune_near_ascendant(278, 273, 12, invalid)
    with pytest.raises(ValueError):
        mod.twelfth_side_neptune_near_ascendant(278, float("nan"), 12)
    with pytest.raises(ValueError):
        mod.twelfth_side_neptune_near_ascendant(278, 273, 0)
