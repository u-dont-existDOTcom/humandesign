"""Regression checks for the precommitted synthetic-only direction coverage."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
from datetime import datetime, timedelta
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/astrology-research-map/primary-direction-synthetic-panel-20261024"
PREVIOUS = ROOT / "docs/astrology-research-map/primary-direction-event-hypotheses-20261024"


def read(name: str) -> dict:
    return json.loads((DOC / name).read_text(encoding="utf-8"))


def module():
    spec = importlib.util.spec_from_file_location(
        "reproducible_synthetic_coverage", DOC / "build_synthetic_panel.py"
    )
    assert spec and spec.loader
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_protocol_was_frozen_and_has_no_human_inputs() -> None:
    p = read("PANEL_PLAN.json")
    digest = hashlib.sha256((DOC / "PANEL_PLAN.json").read_bytes()).hexdigest()
    assert digest == "948a1289b5f891c7f7870632ad116fb16ea6409d1bed575483c07c9901fbc0d0"
    assert digest in (DOC / "PLAN_FREEZE.sha256").read_text()
    assert p["n_cases"] == 96 and p["seed"] == 20261024
    assert p["no_human_outcomes"] is True and p["study_frozen"] is False
    assert p["geometry"] == "proportional_semi_arc"
    assert p["direction"].startswith("software direct")
    assert p["birth_time_sensitivity"]["offsets_minutes"] == [-15, -5, 5, 15]


def test_inputs_are_exactly_regenerable_without_ephemeris() -> None:
    frozen = read("SYNTHETIC_PANEL_INPUTS.json")
    assert module().build_inputs(read("PANEL_PLAN.json")) == frozen
    assert frozen["selection_frozen_before_astronomy"]
    assert len(frozen["synthetic_cases"]) == 96
    assert len(frozen["sensitivity_case_ids"]) == 24
    assert len({r["id"] for r in frozen["synthetic_cases"]}) == 96
    assert all(10 <= abs(r["latitude_deg"]) <= 55 for r in frozen["synthetic_cases"])
    assert len({(r["month_stratum"], r["latitude_deg"]) for r in frozen["synthetic_cases"]}) == 96


def test_all_rule_contacts_are_traceable_and_never_an_outcome_score() -> None:
    file = read("SYNTHETIC_PANEL_EXPOSURES.json")
    body_rules = read("PANEL_PLAN.json")["rules"]
    assert "4 previous" in body_rules
    records = read("SYNTHETIC_PANEL_COVERAGE.json")
    assert records["no_human_natal_or_event_records"]
    assert records["observational_outcome_scoring"] == "NOT_PERFORMED"
    assert records["contact_coverage"]["candidate_rule_count"] == 8
    assert len(file) == 96
    assert sum(len(v) for v in file.values()) == 216
    for exposures in file.values():
        assert len({e["key"] for e in exposures}) == len(exposures)
        assert all(18 <= e["age"] < 65 for e in exposures)
        assert all(e["kind"] in ("body", "aspect") for e in exposures)


def test_chart_csv_and_coverage_recompute_from_exposure_data() -> None:
    with (DOC / "SYNTHETIC_PANEL_CHART_ROWS.csv").open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    exposures = read("SYNTHETIC_PANEL_EXPOSURES.json")
    summary = read("SYNTHETIC_PANEL_COVERAGE.json")["contact_coverage"]
    assert len(rows) == summary["n_charts"] == 96
    assert sum(int(row["all_exposures"]) for row in rows) == 216
    assert sum(int(row["body_exposures"]) for row in rows) == 47
    assert sum(int(row["aspect_exposures"]) for row in rows) == 169
    assert summary["zero_body_chart_count"] == 56
    assert summary["zero_aspect_chart_count"] == 5
    assert summary["zero_any_chart_count"] == 1
    assert summary["mean_exposures_per_synthetic_chart"] == pytest.approx(2.25)
    assert all(int(row["all_exposures"]) == len(exposures[row["id"]]) for row in rows)


def test_geometry_parity_is_evidence_of_same_geometry_not_independence() -> None:
    geom = read("SYNTHETIC_PANEL_COVERAGE.json")["angle_geometry_parity"]
    assert geom["charts_checked"] == 12
    assert geom["groups_checked"] == 30
    assert geom["max_spread_years"] < 1e-8
    assert geom["mismatches"] == []


def test_precommitted_birth_time_uncertainty_breaks_one_year_window() -> None:
    source = read("BIRTH_TIME_PERTURBATION.json")
    assert source["outcome_records_used"] is False
    assert source["status"].startswith("COMPUTATIONAL_STABILITY")
    assert len(source["selected_synthetic_case_ids"]) == 24
    shifts = {r["offset_minutes"]: r for r in source["offset_summaries"]}
    assert set(shifts) == {-15, -5, 5, 15}
    for offset in shifts:
        row = shifts[offset]
        assert row["baseline_contact_denominator"] == 54
        assert row["within_half_year"] == 0
        assert row["within_one_year"] == 0
        assert row["matched_rule_branches"] <= 54
        assert row["median_abs_shift_years_if_common"] is not None
        assert row["median_abs_shift_years_if_common"] > 1.0
    assert shifts[-5]["matched_rule_branches"] == 54
    assert shifts[5]["matched_rule_branches"] == 54
    assert 1.24 < shifts[-5]["median_abs_shift_years_if_common"] < 1.27
    assert 1.24 < shifts[5]["median_abs_shift_years_if_common"] < 1.27
    assert 3.7 < shifts[-15]["median_abs_shift_years_if_common"] < 3.82
    assert 3.7 < shifts[15]["median_abs_shift_years_if_common"] < 3.82


def test_independent_sidereal_rotation_explains_five_minute_age_change() -> None:
    # This checks a physically independent calculation (Swiss houses)
    # rather than trusting the primary-directions age-conversion routine.
    swe = pytest.importorskip("swisseph")
    inp = read("SYNTHETIC_PANEL_INPUTS.json")
    case = next(c for c in inp["synthetic_cases"] if c["id"] == inp["sensitivity_case_ids"][0])
    dt = datetime.fromisoformat(case["birth_utc"])

    def ramc(t: datetime) -> float:
        hour = t.hour + t.minute / 60 + t.second / 3600
        jd = swe.julday(t.year, t.month, t.day, hour)
        _cusps, ascmc = swe.houses_ex(jd, case["latitude_deg"], case["longitude_east_deg"], b"P", 0)
        return ascmc[2]

    delta = (ramc(dt + timedelta(minutes=5)) - ramc(dt)) % 360
    assert 1.252 < delta < 1.255
    assert delta / 5 == pytest.approx(0.250684, abs=0.0004)


def test_historical_uncertainties_remain_explicit_and_unresolved() -> None:
    text = (DOC / "HISTORICAL_CONDITION_AND_DIRECTION_AUDIT.md").read_text()
    claims = read("HISTORICAL_CONDITION_AND_DIRECTION_AUDIT.json")
    assert "both" in text.lower() and "remains open" in text.lower()
    assert claims["human_validation"] == "NONE"
    assert all(row["status"].startswith("SOURCE_VERIFIED") for row in claims["anchors"])
    aspect = json.loads((PREVIOUS / "ASPECT_SOURCE_COVERAGE_DIAGNOSTIC.json").read_text())
    jupiter = next(x for x in aspect["families"] if x["id"] == "L1647-MC-JUP-SOFT")
    assert jupiter["status"] == "CONDITIONAL_NOT_ELIGIBLE_FOR_HUMAN_SCORING"


def test_artifact_hash_manifest_recomputes_and_includes_primary_witnesses() -> None:
    spec = importlib.util.spec_from_file_location(
        "source_and_data_verification", DOC / "build_verification.py"
    )
    assert spec and spec.loader
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    receipt = read("VERIFICATION.json")
    assert helper.build() == receipt
    assert receipt["human_predictive_validity"] == "UNTESTED"
    items = receipt["archive_inputs"]
    assert len(items) >= 23
    assert sum("/witness_pages/" in path for path in items) == 7
    for path, data in items.items():
        file = ROOT / path
        assert hashlib.sha256(file.read_bytes()).hexdigest() == data["sha256"]
