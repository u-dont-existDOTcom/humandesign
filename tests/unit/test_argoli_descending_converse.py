"""Exact original-print Argoli examples and bounded converse-pole comparison.

No actual participant birth data or human outcomes are used. The later fixed
400-coordinate mathematical panel is first executed AFTER methods are committed.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

from hdmatch.astrology.argoli_1610_direction_conventions import (
    angular_separation_deg,
    source_motivated_converse_comparison,
    wrapped_source_arc,
)
from hdmatch.astrology.geometry import EquatorialPoint

ROOT = Path(__file__).resolve().parents[2]
W = ROOT / "docs/astrology-research-map/argoli-descending-converse-20261025"


def info() -> dict:
    return json.loads((W / "SOURCE_METHOD_ALIGNMENT.json").read_text())


def module():
    spec = importlib.util.spec_from_file_location(
        "source_converse_generation", W / "build_converse_comparison.py"
    )
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_1610_and_1667_direct_descending_arc_parity() -> None:
    assert wrapped_source_arc((381, 20), (340, 3)) == (41, 17)
    assert wrapped_source_arc((21, 20), (340, 3)) == (41, 17)
    assert wrapped_source_arc((387, 1), (340, 3)) == (46, 58)
    original = info()
    families = {p["id"]: p for p in original["matched_worked_examples"]}
    assert families["SUN_TO_MARS_SEXTILE_DESCENSION"]["status"].startswith("EXACT_AGREEMENT")
    assert families["SUN_TO_JUPITER_SEXTILE_DESCENSION"]["printed_result_both"] == [46, 58]


def test_1610_alternative_ascensions_match_direct_descensions() -> None:
    assert wrapped_source_arc((201, 20), (160, 3)) == (41, 17)
    assert wrapped_source_arc((207, 1), (160, 3)) == (46, 58)
    assert info()["matched_method_passages"][1]["same_source_method"] is True


def test_1667_page33_printed_106_not_160_preserved_as_second_error() -> None:
    results = info()["matched_worked_examples"]
    x = next(r for r in results if r["id"] == "SUN_TO_JUPITER_SEXTILE_ALTERNATE_ASCENSION")
    assert x["printed_minued"] == [207, 1]
    assert x["correct_subtrahend_in_1610_and_1667_prose"] == [160, 3]
    assert x["misprinted_1667_table_subtrahend"] == [106, 3]
    assert wrapped_source_arc((207, 1), (106, 3)) == (100, 58)
    assert wrapped_source_arc((207, 1), (160, 3)) == (46, 58)
    assert x["later_printed_operand_error_degrees"] == 54
    assert x["status"].startswith("MICHIGAN_1667_P33_106_FOR_160")
    assert info()["earlier_print_discrepancy_crossreference"]["parent_example"].startswith(
        "1610 original p41 gives 43d22m"
    )


def test_descending_vs_converse_source_roles_not_universal_claims() -> None:
    c = info()["first_editions"]
    assert [x["chapter"] for x in c["1610"]["chapters"]] == ["XIV", "XV", "XVI", "XVII"]
    assert [x["chapter"] for x in c["1667"]["chapters"]] == ["XVI", "XVII", "XIIX"]
    assert info()["matched_method_passages"][2]["same_source_method"].startswith("UNRESOLVED")
    assert info()["human_predictive_accuracy"] == "UNTESTED"
    assert info()["human_data_seen"] is False


def test_all_original_witness_hashes_and_bsb_canvas_binding() -> None:
    a = info()
    for entry in a["original_source_files"]:
        f = W / entry["path"]
        assert f.stat().st_size == entry["bytes"]
        assert hashlib.sha256(f.read_bytes()).hexdigest() == entry["sha256"]
    parent = ROOT / a["first_editions"]["1610"]["institutional_manifest"]
    assert (
        hashlib.sha256(parent.read_bytes()).hexdigest()
        == (a["first_editions"]["1610"]["manifest_sha256"])
    )


def test_source_only_validates_older_original_pdf_and_examples() -> None:
    x = module().source_check()
    assert x["wrong_operand_difference_degrees"] == 54
    assert x["four_matched_worked_direction_arcs"][
        "SUN_TO_JUPITER_SEXTILE_ALTERNATE_ASCENSION"
    ] == [46, 58]
    assert x["source_1644_status"] == "UNREAD_429_OR_403"
    assert x["human_outcomes_evaluated"] is False


def test_swapped_pole_not_equivalent_to_negating_direction() -> None:
    report = source_motivated_converse_comparison(
        53.0,
        222.17357,
        EquatorialPoint(186.1673, -2.6734),
        EquatorialPoint(261.13, -23.151),
    )
    assert report.absolute_difference_converse_vs_naive_deg > 0.01
    assert angular_separation_deg(
        report.converse_using_promissor_circle_deg,
        report.naive_360_minus_direct_deg,
    ) == pytest.approx(report.absolute_difference_converse_vs_naive_deg)
    assert report.authenticity == "SOURCE_MOTIVATED_RESEARCH_VARIANT_NOT_COMPLETE_ARGOLI"
    assert report.human_prediction_accuracy == "UNTESTED"


def test_input_rejection_prevents_fitting_source_table_coordinates() -> None:
    with pytest.raises(ValueError):
        wrapped_source_arc((1, 60), (0, 0))
    with pytest.raises(ValueError):
        wrapped_source_arc((1, -1), (0, 0))
    with pytest.raises(ValueError):
        wrapped_source_arc((1, 0.2), (0, 0))
    with pytest.raises(ValueError):
        wrapped_source_arc((800, 1), (1, 1))


def test_new_holdout_400_only_after_precommit() -> None:
    report = json.loads((W / "CONVERSE_SOURCE_AND_GEOMETRY_REPORT.json").read_text())
    assert report["predictive_accuracy"] == "UNTESTED"
    assert report["development"]["seed"] == 20261025
    assert report["development"]["n"] == 500
    held = report["mathematical_holdout"]
    assert held["seed"] == 20261029
    assert held["n"] == 400
    assert held["n_disagree_over_one_degree"] > 0
    assert held["n_disagree_over_five_degrees"] > 0
    assert report["source_exact_complete_1610_Argoli"] == "NOT_AUTHENTICATED"
    build = module().build()[0]
    assert build == report


def test_complete_math_panel_replay_bitwise_identical() -> None:
    result = json.loads((W / "REPLAY_VERIFICATION.json").read_text())
    code = importlib.util.spec_from_file_location(
        "argoli_converse_replay", W / "verify_converse_replay.py"
    )
    assert code is not None and code.loader is not None
    helper = importlib.util.module_from_spec(code)
    code.loader.exec_module(helper)
    assert helper.replay() == result
    assert result["status"] == "TWO_OF_TWO_OUTPUT_FILES_BITWISE_IDENTICAL"
    assert result["fixed_source_and_math_precommit"] == ("b7eb138099aba840edd4dc748241ad41a5d8dec8")
    assert result["holdout_over_one_degree"] == 277
    assert result["holdout_over_five_degrees"] == 148
    assert result["human_predictive_accuracy"] == "UNTESTED"


def test_sha256_verification_covers_all_original_images_and_converse_code() -> None:
    saved = json.loads((W / "VERIFICATION.json").read_text())
    source = importlib.util.spec_from_file_location(
        "argoli_descending_integrity", W / "build_source_verification.py"
    )
    assert source is not None and source.loader is not None
    helper = importlib.util.module_from_spec(source)
    source.loader.exec_module(helper)
    assert helper.manifest() == saved
    assert saved["original_1644_printing_compared"] is False
    assert saved["source_witness_images"] == 10
    assert saved["derived_detail_crops_not_independent_evidence"] == 1
    assert saved["all_human_predictive_accuracy"] == "UNTESTED"
    for rel, meta in saved["file_sha256"].items():
        content = (ROOT / rel).read_bytes()
        assert hashlib.sha256(content).hexdigest() == meta["sha256"]
        assert len(content) == meta["bytes"]
