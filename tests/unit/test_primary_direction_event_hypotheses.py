"""Primary-source candidate packet, witness integrity and diagnostic projection.

No personal natal data, life outcomes or test-participant responses are loaded.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from hdmatch.astrology.event_hypothesis_windows import project_unfrozen_candidate_windows

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs" / "astrology-research-map" / "primary-direction-event-hypotheses-20261024"
REGISTRY = json.loads((DOC / "LILLY_1647_EVENT_CANDIDATES.json").read_text(encoding="utf-8"))


def fake_timeline(
    rows: list[dict[str, object]],
    *,
    key: str = "ptolemy_one_degree_per_year",
) -> dict[str, object]:
    return {
        "schema_version": "astro-primary-directions-conjunction-timeline-v1",
        "scope": (
            "seven classical body promissors; bodily conjunctions to "
            "other classical bodies and exact Asc/MC; no rays/terms/antiscia"
        ),
        "technique_provenance": {
            "time_key": key,
            "no_event_interpretation": True,
        },
        "directions": rows,
    }


def contact(
    promissor: str,
    significator: str,
    age: float,
    *,
    method: str = "placidean_under_pole",
    sense: str = "direct",
    key: str = "ptolemy_one_degree_per_year",
) -> dict[str, object]:
    return {
        "method": method,
        "time_key": key,
        "promissor": promissor,
        "significator": significator,
        "contact": "body_to_angle",
        "direction": sense,
        "symbolic_age_years": age,
        "model_date_utc": "2030-04-20T12:00:00+00:00",
    }


def test_registry_four_source_families_unfrozen_and_not_empirical() -> None:
    assert REGISTRY["status"] == "SOURCE_BACKED_INTERPRETATION_CANDIDATES_UNFROZEN"
    assert REGISTRY["human_validation"] == "NONE"
    assert REGISTRY["scoring_stage"] == "NOT_DEFINED_OR_FROZEN"
    assert REGISTRY["calibration"] == "NO_CALIBRATED_PROBABILITIES"
    assert REGISTRY["study_readiness"] == "NOT_READY_FOR_UNTOUCHED_HUMAN_TEST"
    assert REGISTRY["parent_status"].endswith("_OPEN")
    assert REGISTRY["person_specific_outcome_records_accessed_during_this_run"] is False
    assert "not" in REGISTRY["blindness_disclosure"].lower()
    rules = REGISTRY["source_to_construct_rules"]
    assert len(rules) == 4
    assert len({r["id"] for r in rules}) == len(rules)
    assert {(r["promissor"], r["target_role"]) for r in rules} == {
        ("jupiter", "mc"),
        ("saturn", "mc"),
        ("jupiter", "asc"),
        ("mars", "asc"),
    }
    assert all(r["source_anchor_exact"] and r["modern_bounded_event"] for r in rules)
    assert all(r["qualifications"] and r["source_pages"] for r in rules)
    assert all(r["source_anchor_page"] in r["source_pages"] for r in rules)


def test_each_primary_witness_image_matches_declared_sha256() -> None:
    images = REGISTRY["source"]["images"]
    assert set(images) == {"657", "658", "659", "668", "669", "670"}
    for page, details in images.items():
        assert details["image_id"] == f"b30338724_{int(page) + 34:04}.jp2"
        path = DOC / details["path"]
        assert path.is_file()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == details["sha256"]


def test_modern_diagnostic_parameters_never_promoted_to_historical_facts() -> None:
    params = REGISTRY["experimental_pre_freeze_defaults_not_lilly_claims"]
    assert params["diagnostic_profile"] == "body_conjunctions"
    assert params["diagnostic_key"] == "ptolemy_one_degree_per_year"
    assert params["direction_sense"].startswith("software_direct_only_")
    assert params["half_window_width_years"] == 0.5
    assert params["min_age_years"] == 18
    assert params["max_age_years"] == 65
    assert "historically" in params["note"].lower() or "not a human" in params["note"].lower()


def test_exact_geometry_duplicate_not_counted_as_second_confirmation() -> None:
    rows = [
        contact("jupiter", "mc", 30.0, method="placidean_under_pole"),
        contact("jupiter", "mc", 30.0, method="proportional_semi_arc"),
        contact("jupiter", "mc", 30.0, method="regiomontanian_position_circle"),
    ]
    out = project_unfrozen_candidate_windows(fake_timeline(rows), REGISTRY)
    assert out["raw_matching_geometry_records"] == 3
    assert out["unique_contact_exposure_groups"] == 1
    assert out["source_rule_count"] == 4
    w = out["windows"][0]
    assert w["source_rule_id"] == "L1647-MC-JUP-BODY"
    assert w["window_age_lower_inclusive"] == 29.5
    assert w["window_age_upper_exclusive"] == 30.5
    assert len(w["method_ids"]) == w["number_of_equivalent_method_records"] == 3
    assert w["is_not_independent_confirmation"] is True


def test_distinct_method_ages_remain_competing_not_pooled() -> None:
    rows = [
        contact("jupiter", "mc", 30.0, method="placidean_under_pole"),
        contact("jupiter", "mc", 32.0, method="proportional_semi_arc"),
    ]
    out = project_unfrozen_candidate_windows(fake_timeline(rows), REGISTRY)
    assert out["unique_contact_exposure_groups"] == 2
    assert all(not x["is_not_independent_confirmation"] for x in out["windows"])


def test_direction_and_unknown_contacts_not_retrospectively_selected() -> None:
    rows = [
        contact("jupiter", "mc", 30.0, sense="converse"),
        contact("mars", "asc", 33.0, sense="direct"),
        contact("venus", "asc", 34.0, sense="direct"),
    ]
    out = project_unfrozen_candidate_windows(fake_timeline(rows), REGISTRY)
    assert [x["source_rule_id"] for x in out["windows"]] == ["L1647-ASC-MARS-BODY"]


def test_half_open_boundary_age_window_is_clipped() -> None:
    rows = [contact("saturn", "mc", 18.1), contact("mars", "asc", 64.9)]
    out = project_unfrozen_candidate_windows(fake_timeline(rows), REGISTRY)
    by_rule = {x["source_rule_id"]: x for x in out["windows"]}
    assert by_rule["L1647-MC-SAT-BODY"]["window_age_lower_inclusive"] == 18.0
    assert by_rule["L1647-MC-SAT-BODY"]["window_age_upper_exclusive"] == 18.6
    assert by_rule["L1647-ASC-MARS-BODY"]["window_age_lower_inclusive"] == 64.4
    assert by_rule["L1647-ASC-MARS-BODY"]["window_age_upper_exclusive"] == 65.0


def test_wrong_schema_key_and_provenance_rejected() -> None:
    rows = [contact("jupiter", "mc", 29.0)]
    good = fake_timeline(rows)
    for modification in ("schema_version", "scope", "technique_provenance", "key"):
        altered = deepcopy(good)
        if modification == "schema_version":
            altered["schema_version"] = "other"
        elif modification == "scope":
            altered["scope"] = "zodiacal rays"
        elif modification == "technique_provenance":
            altered["technique_provenance"]["no_event_interpretation"] = False
        else:
            altered["technique_provenance"]["time_key"] = "naibod_59m08s_fixed_diagnostic"
        with pytest.raises(ValueError):
            project_unfrozen_candidate_windows(altered, REGISTRY)


def test_unexpected_geometry_fails_closed_instead_of_auto_fitting() -> None:
    rows = [contact("jupiter", "mc", 30.0, method="invented_best_fit")]
    with pytest.raises(ValueError, match="undeclared geometry"):
        project_unfrozen_candidate_windows(fake_timeline(rows), REGISTRY)


def test_preexisting_synthetic_no_adult_direct_exposures_remains_zero() -> None:
    fixture = (
        ROOT
        / "docs/astrology-research-map/gansten-primary-timeline-20261024/examples"
        / "synthetic_2000_timeline.json"
    )
    timeline = json.loads(fixture.read_text(encoding="utf-8"))
    out = project_unfrozen_candidate_windows(timeline, REGISTRY)
    assert out["unique_contact_exposure_groups"] == 0
    assert out["raw_matching_geometry_records"] == 0
    assert out["windows"] == []
    assert out["status"].startswith("DIAGNOSTIC_ONLY")
