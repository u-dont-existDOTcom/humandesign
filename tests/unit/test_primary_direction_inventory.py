"""Research-only candidate inventory checks; no human data and no model freeze."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from hdmatch.astrology.lilly_1647_photo import MINUTE_PARTIALLY_LEGIBLE
from hdmatch.astrology.source_witness_scope import (
    WitnessStatus,
    placidus_1657_latin_role_assessment,
    solar_key_source_assessment,
)

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/astrology-research-map/primary-direction-candidate-inventory-20261024"
FILE = DOC / "PRIMARY_DIRECTION_PRE_FREEZE_INVENTORY.json"


@pytest.fixture(scope="module")
def inventory():
    return json.loads(FILE.read_text())


def test_research_arm_list_is_bounded_unfrozen_and_not_predictive(inventory) -> None:
    arms = inventory["arms"]
    assert len(arms) == 12
    assert len({a["id"] for a in arms}) == 12
    assert inventory["human_prediction_mapping_frozen"] is False
    assert inventory["all_source_engineering_only"] is True
    assert inventory["status"].startswith("UNFROZEN")
    assert all(a["interpretation_frozen"] is False for a in arms)
    assert all(a["real_human_prediction_validated"] is False for a in arms)
    assert all(a["human_study_admitted_by_this_inventory"] is False for a in arms)
    assert inventory["not_new_mandatory_source_gate"] is True


def test_unverified_1647_source_rows_not_promoted_to_continuous_key(inventory) -> None:
    assert inventory["original_Lilly_1647_absent_minute_label"] == [27]
    assert inventory["original_Lilly_1647_faint_minutes"] == sorted(MINUTE_PARTIALLY_LEGIBLE)
    witness = next(a for a in inventory["arms"] if a["id"] == "PD11")
    assert witness["cli_flags"] is None
    assert witness["source_support"] == "incomplete_original_table"
    assert "Not continuous" in witness["limitations"]


def test_latin_placidus_cumulative_solar_key_attested_but_not_full_rules(inventory) -> None:
    label = solar_key_source_assessment("placidus_cumulative_true_solar_ra")
    assert label.status is WitnessStatus.COMPATIBLE_SELECTED_RULE
    arm = next(a for a in inventory["arms"] if a["id"] == "PD02")
    assert arm["source_support"] == label.status.value
    assert arm["cli_flags"][-1] == "placidus_cumulative_true_solar_ra"
    assert "not fully certified" in arm["limitations"]


def test_brahe_exact_midnight_endpoints_remain_unverified(inventory) -> None:
    label = solar_key_source_assessment("brahe_true_midnight_birth_day")
    assert label.status is WitnessStatus.PARTIAL_SOURCE_SUPPORT
    arm = next(a for a in inventory["arms"] if a["id"] == "PD03")
    assert arm["source_support"] == label.status.value
    assert "not proved" in arm["limitations"]


def test_original_1657_disallows_placidus_converse_zodiacal_attribution(inventory) -> None:
    assessment = placidus_1657_latin_role_assessment(
        "zodiacal_promissor_ray", "traditional_role_reversed_converse"
    )
    assert assessment.status is WitnessStatus.INCOMPATIBLE_WITNESS
    assert inventory["source_Witness_Placidus_converse_zodiacal"] == assessment.to_dict()
    arm = next(a for a in inventory["arms"] if a["id"] == "PD07")
    assert arm["source_support"] == "incompatible_as_placidus_1657"
    assert arm["cli_flags"] is not None
    assert "NOT historically attributable" in arm["limitations"]


def test_two_labellings_of_same_288_arcs_share_one_duplicate_group(inventory) -> None:
    group = inventory["double_count_warning"]
    assert group["ids"] == ["PD07", "PD08"]
    assert "288/288" in group["earlier_frozen_math_scope"]
    assert group["source_interpretations_not_assumed_identical"] is True
    dup = [r for r in inventory["arms"] if r["geometric_duplicate_group"]]
    assert len(dup) == 2
    assert {x["geometric_duplicate_group"] for x in dup} == {"fixed_ray_swapped_roles"}


def test_generator_json_is_reproducible(inventory) -> None:
    path = DOC / "generate_inventory.py"
    spec = importlib.util.spec_from_file_location("independent_research_inventory", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.build() == inventory


def test_csv_mirrors_all_json_arm_rows(inventory) -> None:
    import csv

    with (DOC / "PRIMARY_DIRECTION_PRE_FREEZE_INVENTORY.csv").open(
        encoding="utf-8", newline=""
    ) as source:
        rows = list(csv.DictReader(source))
    assert len(rows) == len(inventory["arms"]) == 12
    assert [r["id"] for r in rows] == [a["id"] for a in inventory["arms"]]
    for row, arm in zip(rows, inventory["arms"], strict=True):
        assert row["source_support"] == arm["source_support"]
        assert row["cli_flags"] == " ".join(arm["cli_flags"] or [])
        assert row["real_human_prediction_validated"] == "False"
        assert row["interpretation_frozen"] == "False"
