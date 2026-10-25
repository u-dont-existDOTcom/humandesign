"""Cross-edition original-image anchored arithmetic, never human evaluation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from hdmatch.astrology.argoli_printed_arithmetic import (
    printed_arc_discrepancy_minutes,
    subtract_degree_minute_seconds,
    subtract_degree_minutes,
)

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/astrology-research-map/argoli-aligned-1610-1667-20261025"


def source() -> dict:
    return json.loads((DOC / "ARGOLI_ALIGNED_EXAMPLES.json").read_text(encoding="utf-8"))


def test_three_original_print_examples_match_literal_operands() -> None:
    findings = {rec["id"]: rec for rec in source()["worked_examples"]}
    assert set(findings) == {
        "FORTUNE_TO_OPPOSITION_SUN",
        "SATURN_POSITION_POLE",
        "SATURN_TO_OPPOSITION_SUN",
    }
    fortune = findings["FORTUNE_TO_OPPOSITION_SUN"]
    result = subtract_degree_minutes(
        fortune["first_operand_deg_min"], fortune["second_operand_deg_min"]
    )
    assert result == (37, 39)
    assert list(result) == fortune["printed_1610_deg_min"]
    assert list(result) == fortune["printed_1667_deg_min"]

    pole = findings["SATURN_POSITION_POLE"]
    result_pole = subtract_degree_minute_seconds(
        pole["first_operand_deg_min_sec"], pole["subtrahend_deg_min_sec"]
    )
    assert result_pole == (14, 14, 30)
    assert list(result_pole) == pole["printed_1610_deg_min_sec"]
    assert list(result_pole) == pole["printed_1667_deg_min_sec"]


def test_two_degree_1667_printing_error_is_preserved_not_corrected() -> None:
    example = next(
        rec for rec in source()["worked_examples"] if rec["id"] == "SATURN_TO_OPPOSITION_SUN"
    )
    computed = subtract_degree_minutes(
        example["first_operand_deg_min"], example["second_operand_deg_min"]
    )
    assert computed == (43, 22)
    assert list(computed) == example["printed_1610_deg_min"]
    assert list(computed) != example["printed_1667_deg_min"]
    assert example["printed_1667_deg_min"] == [45, 22]
    assert (
        printed_arc_discrepancy_minutes(computed, example["printed_1667_deg_min"])
        == example["printed_1667_error_in_arc_minutes"]
        == 120
    )
    assert example["source_certainty"].startswith("Both readings visually examined")
    assert source()["edition_1644"]["status"].startswith("LOCATED_ONLY")


def test_original_1610_bsb_manifest_and_iiif_page_labels_are_exact() -> None:
    info = source()["source_hierarchy"]["edition_1610"]
    document = DOC / "BSB_1610_1760_leaf_IIIF_manifest.json"
    assert hashlib.sha256(document.read_bytes()).hexdigest() == (info["full_iiif_manifest_sha256"])
    manifest = json.loads(document.read_text())
    assert len(manifest["sequences"][0]["canvases"]) == 1760
    assert manifest["license"] == "https://rightsstatements.org/vocab/NoC-NC/1.0/"
    for page in info["pages"]:
        leaf = page["iiif_leaf"]
        canvas = manifest["sequences"][0]["canvases"][leaf - 1]
        assert canvas["label"].startswith(str(page["printed"]) + " ")
        assert canvas["images"][0]["resource"]["@id"].startswith(
            f"https://api.digitale-sammlungen.de/iiif/image/v2/bsb11218073_{leaf:05d}/"
        )
        f = DOC / page["file"]
        assert hashlib.sha256(f.read_bytes()).hexdigest() == page["sha256"]


def test_original_1667_images_and_parent_michigan_scan_are_fixed() -> None:
    data = source()["source_hierarchy"]["edition_1667"]
    raw = ROOT / data["parent_original_pdf"]
    assert hashlib.sha256(raw.read_bytes()).hexdigest() == (data["parent_original_pdf_sha256"])
    for page in data["pages"]:
        file = DOC / page["file"]
        assert hashlib.sha256(file.read_bytes()).hexdigest() == page["sha256"]
    assert data["pages"][0]["printed"] == 29
    assert data["pages"][1]["printed"] == 30
    assert source()["chapter_alignment"]["status"].startswith("MATCHED_CHAPTER_")


def test_arithmetic_rejects_invalid_operands_without_wrap_or_guess() -> None:
    with pytest.raises(ValueError):
        subtract_degree_minutes([12, 60], [2, 0])
    with pytest.raises(ValueError):
        subtract_degree_minutes([1, 0], [2, 0])
    with pytest.raises(ValueError):
        subtract_degree_minutes([10], [2, 0])
    with pytest.raises(ValueError):
        subtract_degree_minutes([10, 0.5], [2, 0])
    with pytest.raises(ValueError):
        subtract_degree_minute_seconds([1, 0, 0], [2, 0, 0])
    with pytest.raises(ValueError):
        subtract_degree_minute_seconds([1, 0, 60], [0, 0, 0])
    with pytest.raises(ValueError):
        printed_arc_discrepancy_minutes([40, 99], [44, 2])


def test_no_human_outcomes_and_no_whole_edition_equivalence_claims() -> None:
    data = source()
    assert data["no_private_natal_data_used"] is True
    assert data["empirical_human_predictive_accuracy"] == "UNTESTED"
    assert data["historical_method_status"].endswith("_UNRESOLVED")
    assert data["edition_1644"]["status"] == "LOCATED_ONLY_PRIMARY_METHOD_PAGES_NOT_VIEWED"
    assert data["source_hierarchy"]["edition_1667"]["pages"][0]["chapter"] == "XV"
    assert data["source_hierarchy"]["edition_1610"]["pages"][0]["chapter"] == "XIII"


def test_full_source_evidence_manifest_recomputes_from_original_images() -> None:
    import importlib.util

    path = DOC / "build_verification.py"
    spec = importlib.util.spec_from_file_location("argoli_original_source_manifest", path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    saved = json.loads((DOC / "VERIFICATION.json").read_text())
    assert mod.build() == saved
    assert saved["original_1610_primary_pages_checked"] == [39, 40, 41]
    assert saved["original_1667_primary_pages_checked"] == [29, 30]
    assert saved["inspected_1667_original_arithmetic_discrepancy_arc_minutes"] == 120
    assert saved["source_1644_homologous_passages"] == "UNRESOLVED"
    assert saved["human_predictive_accuracy"] == "UNTESTED"
    assert len(saved["hashed_files"]) >= 11
    for relative, proof in saved["hashed_files"].items():
        f = ROOT / relative
        assert f.stat().st_size == proof["bytes"]
        assert hashlib.sha256(f.read_bytes()).hexdigest() == proof["sha256"]
