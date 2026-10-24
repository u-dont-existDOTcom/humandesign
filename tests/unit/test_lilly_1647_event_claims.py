"""Source-attested, UNFROZEN Lilly event-meaning proposal registry tests.

Original first-edition page photographs and short word-for-word excerpts are
individually audited. Symbolic mathematical contacts are not human outcomes.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
from datetime import UTC, datetime
from pathlib import Path

import pytest

from hdmatch.astrology.geometry import GeometryMethod
from hdmatch.astrology.role_directions import (
    ContactConstruction,
    RotationRegime,
    generate_role_timeline,
)
from hdmatch.astrology.sky import snapshot_from_swiss_files

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "docs/astrology-research-map/lilly-event-claims-pretest-20261024"
EPHE = Path(
    os.environ.get(
        "HDMATCH_PRIMARY_DIR_EPHE_DIR",
        str(Path.home() / ".local/share/hdmatch/ephemeris/1800-2399"),
    )
)


@pytest.fixture(scope="module")
def generator():
    file = DIR / "generate_source_claims.py"
    spec = importlib.util.spec_from_file_location("lilly_original_claims", file)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def record():
    return json.loads((DIR / "LILLY_1647_EVENT_CLAIM_CANDIDATES.json").read_text())


def test_claim_register_bounded_source_conditional_and_unfrozen(record, generator) -> None:
    assert len(record["entries"]) == 7
    assert record == generator.compile_register()
    assert record["interpretation_frozen"] is False
    assert record["time_key_selected_for_human_test"] is False
    assert record["human_birth_or_event_records_used"] is False
    assert record["actual_prospective_human_outcomes_scored"] == 0
    assert all(item["status"].startswith("SOURCE_ATTEMPTED_UNFROZEN") for item in record["entries"])
    assert all(
        item["not_a_prediction"] and item["scored_people"] == 0 for item in record["entries"]
    )


def test_actual_original_source_page_ids_and_jpeg_sha256(record) -> None:
    for item in record["entries"]:
        src = item["source"]
        assert src["first_edition"] == 1647
        assert src["excerpt_status"] == "checked_directly_in_1647_photo"
        assert len(src["verbatim_short_original_excerpt"].split()) < 27
        for page, canvas, photo in zip(
            src["printed_pages"], src["zero_based_canvas_indices"], src["photos"], strict=True
        ):
            assert canvas == page + 34
            path = DIR / photo["path"]
            assert path.is_file() and path.stat().st_size > 700_000
            b = path.read_bytes()
            assert b[:2] == bytes.fromhex("ffd8")
            assert hashlib.sha256(b).hexdigest() == photo["sha256"]


def test_historic_condition_vs_analyst_event_proxy_remain_separate(record) -> None:
    assert len(record["source_scope"]["source_conditions"]) == 2
    for item in record["entries"]:
        assert item["historical_conditions"]
        analyst = item["analyst_modern_test_candidate"]
        assert analyst["operational_definition_PROPOSED_NOT_SOURCE"]
        assert analyst["eligibility_PROPOSED_NOT_SOURCE"]
        assert analyst["time_window_status"] == "NOT_DEFINED"
        assert analyst["observation_period_status"] == "NOT_DEFINED"
        assert analyst["base_rate_and_control_group_status"] == "NOT_DEFINED"
        assert item["astronomical_proxy"]["claim_of_complete_Lilly_original_1647_geometry"] is False
    assert record["standard"]["promisor_house_rulership_essential_dignity"] == (
        "NOT_FULLY_CALCULATED"
    )


def test_source_incompatible_unfrozen_alternative_outcomes_not_double_counted(record) -> None:
    item = next(x for x in record["entries"] if x["claim_id"] == "LIL-E07")
    assert item["multiplicity"]["alternative_outcomes_unresolved"]
    assert item["analyst_modern_test_candidate"]["event_code"] == (
        "marriage_or_birth_ALTERNATIVES_NOT_FROZEN"
    )
    assert all(x["multiplicity"]["no_multiple_claim_success_credit"] for x in record["entries"])
    assert record["interpretation_dependency_groups"]["relationship_union"] == [
        "LIL-E03",
        "LIL-E06",
        "LIL-E07",
    ]


def test_pure_geometry_match_excludes_role_reversal_and_different_aspects(
    record, generator
) -> None:
    loss = next(x for x in record["entries"] if x["claim_id"] == "LIL-E04")
    rec = {
        "rotation_regime": "direct_primary_motion",
        "construction": "zodiacal_promissor_ray",
        "promissor": "saturn",
        "significator": "mc",
        "aspect": "square",
    }
    assert generator.matches_role_contact(loss, rec)
    assert generator.matches_role_contact(loss, dict(rec, aspect="opposition"))
    assert not generator.matches_role_contact(loss, dict(rec, aspect="sextile"))
    assert not generator.matches_role_contact(
        loss, dict(rec, rotation_regime="traditional_role_reversed_converse")
    )
    assert not generator.matches_role_contact(
        loss, dict(rec, construction="bodily_conjunction", aspect=None)
    )


def test_source_bodily_venus_marriage_not_reversed_or_jupiter(record, generator) -> None:
    item = next(x for x in record["entries"] if x["claim_id"] == "LIL-E03")
    record_good = {
        "rotation_regime": "direct_primary_motion",
        "construction": "bodily_conjunction",
        "promissor": "venus",
        "significator": "asc",
        "aspect": None,
    }
    assert generator.matches_role_contact(item, record_good)
    assert not generator.matches_role_contact(item, dict(record_good, promissor="jupiter"))
    assert not generator.matches_role_contact(item, dict(record_good, significator="sun"))
    assert not generator.matches_role_contact(
        item, dict(record_good, rotation_regime="modern_reverse_rotation_diagnostic")
    )


def test_source_claims_csv_matches_json(record) -> None:
    with (DIR / "LILLY_1647_EVENT_CLAIM_CANDIDATES.csv").open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == len(record["entries"])
    assert [r["claim_id"] for r in rows] == [x["claim_id"] for x in record["entries"]]
    assert all(r["time_window_frozen"] == "False" for r in rows)
    assert all(r["human_predictive_validity"] == "UNTESTED" for r in rows)
    for row, item in zip(rows, record["entries"], strict=True):
        assert row["promissor"] == item["astronomical_proxy"]["moving_promissor"]
        assert row["significator"] == item["astronomical_proxy"]["natal_significator"]


@pytest.mark.skipif(not EPHE.is_dir(), reason="official Swiss ephemeris missing")
def test_matches_synthetic_geometry_but_does_not_score_events(record, generator) -> None:
    # This synthetic SKY is not actual user/participant life history.
    sky = snapshot_from_swiss_files(
        datetime(2000, 1, 1, 12, tzinfo=UTC),
        latitude_deg=45,
        longitude_east_deg=0,
        ephemeris_directory=EPHE,
    )
    examples = []
    for kind in (ContactConstruction.BODY_CONJUNCTION, ContactConstruction.ZODIACAL_PROMISSOR_RAY):
        role = generate_role_timeline(
            sky,
            construction=kind,
            regime=RotationRegime.DIRECT_PRIMARY_MOTION,
            methods=(GeometryMethod.PROPORTIONAL_SEMI_ARC,),
            max_age_years=125,
        )
        examples += [x.to_dict() for x in role.directions]
    counts = {
        r["claim_id"]: sum(generator.matches_role_contact(r, x) for x in examples)
        for r in record["entries"]
    }
    assert sum(counts.values()) >= 1
    assert len(counts) == 7
    assert all(isinstance(n, int) and 0 <= n < 6 for n in counts.values())
    assert all(r["scored_people"] == 0 for r in record["entries"])
    assert all(
        r["analyst_modern_test_candidate"]["time_window_status"] == "NOT_DEFINED"
        for r in record["entries"]
    )


def test_synthetic_coverage_reports_arcs_without_dates_or_human_labels() -> None:
    data = json.loads((DIR / "LILLY_1647_SYNTHETIC_GEOMETRY_COVERAGE.json").read_text())
    assert data["no_actual_events_or_answers_consulted"] is True
    assert data["no_raw_age_dates_in_this_report"] is True
    assert data["model_interpretations_frozen"] is False
    assert data["age_time_key_for_human_predictions"] == "NOT_SELECTED"
    assert data["synthetic_natal"]["made_up_not_personal"] is True
    assert [row["construction"] for row in data["engine_profiles"]] == [
        "bodily_conjunction",
        "zodiacal_promissor_ray",
    ]
    assert {
        key: value["total_geometric_outputs_across_methods"]
        for key, value in data["matches"].items()
    } == {
        "LIL-E01": 3,
        "LIL-E02": 0,
        "LIL-E03": 0,
        "LIL-E04": 3,
        "LIL-E05": 3,
        "LIL-E06": 0,
        "LIL-E07": 6,
    }
    assert all(item["event_occurred_or_ever_asked"] is None for item in data["matches"].values())
    assert data["zero_pattern_counts_do_not_mean_the_claim_was_falsified"] is True


def test_prior_wellcome_source_locator_corrected_and_numerics_intact() -> None:
    source_folder = ROOT / (
        "docs/astrology-research-map/lilly-1647-independent-table-collation-20261024"
    )
    provenance = json.loads((source_folder / "SOURCE_PROVENANCE.json").read_text())
    assert provenance["first_edition_witness_A"]["printed_page_to_zero_based_canvas"] == {
        "713": 747,
        "714": 748,
        "715": 749,
    }
    from hdmatch.astrology.lilly_1647_photo import DEGREE_PHOTO_COMPONENTS, MINUTE_PHOTO_COMPONENTS

    assert DEGREE_PHOTO_COMPONENTS[69] == (4, 3)
    assert MINUTE_PHOTO_COMPONENTS[1] == (5, 4)
    earlier = json.loads((source_folder / "VERIFICATION.json").read_text())
    assert earlier["new_result"]["verified_numerical_table_cell_differences"] == 23
    with (source_folder / "LILLY_NAIBOD_1647_WELLCOME_VS_2003_BY_ROW.csv").open(
        encoding="utf-8", newline=""
    ) as source:
        rows = list(csv.DictReader(source))
    assert len(rows) == 152
    assert sum(bool(r["verified_difference"]) for r in rows) == 23
    first_degree = next(
        r for r in rows if r["table"] == "degree_component" and r["angle_row_label"] == "1"
    )
    first_minute = next(
        r for r in rows if r["table"] == "minute_component" and r["angle_row_label"] == "1"
    )
    assert "IIIF canvas 747" in first_degree["source_note"]
    assert "IIIF canvas 748" in first_minute["source_note"]
