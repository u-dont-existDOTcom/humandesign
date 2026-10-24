"""Photographic original 1647 Lilly/Naibod table collation, no guessed cells.

Source: independent Wellcome full-resolution 1647 printed pp713-715,
cross-checked with original ca-william-lilly first-edition page photos.
The original is NOT the 2003 WorldAstrology retypeset: distinct witnesses.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import pytest

from hdmatch.astrology.historical_naibod import (
    DEGREE_COMPONENTS as RETYPE_DEGREE,
)
from hdmatch.astrology.historical_naibod import (
    MINUTE_COMPONENTS as RETYPE_MINUTE,
)
from hdmatch.astrology.historical_naibod import (
    literal_naibod_lookup,
)
from hdmatch.astrology.lilly_1647_photo import (
    DEGREE_PHOTO_COMPONENTS,
    DEGREE_PHOTO_YEARS,
    MINUTE_LABEL_ABSENT,
    MINUTE_PARTIALLY_LEGIBLE,
    MINUTE_PHOTO_COMPONENTS,
    SOURCE_1647,
    SourceCellStatus,
    SourceWitnessUnavailable,
    independent_photo_lookup,
    minute_status,
)
from hdmatch.astrology.naibod_original_1647 import original_1647_critical_comparison

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/astrology-research-map/lilly-1647-independent-table-collation-20261024"


def test_two_first_edition_photo_sources_are_distinct_and_one_is_high_resolution() -> None:
    provenance = json.loads((DOC / "SOURCE_PROVENANCE.json").read_text())
    sources = provenance["first_edition_witness_A"]
    assert sources["image_resolution"] == "3141×4249"
    assert sources["printed_page_to_zero_based_canvas"] == {"713": 746, "714": 747, "715": 748}
    for page, digest in sources["source_image_file_SHA256"].items():
        photo = DOC / "facsimile_pages" / f"wellcome_original_1647_printed_{page}.jpg"
        assert photo.stat().st_size > 1_000_000
        assert hashlib.sha256(photo.read_bytes()).hexdigest() == digest
        # The pinned source digest is authoritative. Avoid requiring Pillow
        # in the existing research Python environment.
        assert photo.read_bytes().startswith(bytes.fromhex("ffd8"))
    assert provenance["first_edition_witness_B"]["independently_compared"] is True


def test_source_differentiation_exact_original_minute_one_not_retype() -> None:
    original = independent_photo_lookup(0, 1)
    modern = literal_naibod_lookup(0, 1)
    assert (original.source_minute_days, original.source_minute_hours) == (5, 4)
    assert (modern.literal_minute_days, modern.literal_minute_hours) == (6, 4)
    assert (original.result_years, original.result_days, original.result_hours) == (0, 5, 4)
    assert (modern.resulting_years, modern.resulting_days, modern.resulting_hours) == (0, 6, 4)
    assert original.original_minute_status == "photograph_confirmed"
    assert "1647" in original.witness and original.witness == SOURCE_1647


def test_original_1647_exact_carried_degree_years_and_first_minute_combine() -> None:
    source = independent_photo_lookup(69, 1)
    modern = literal_naibod_lookup(69, 1)
    prior_partial = original_1647_critical_comparison(69, 1)
    assert (source.result_years, source.result_days, source.result_hours) == (70, 9, 7)
    assert (modern.resulting_years, modern.resulting_days, modern.resulting_hours) == (69, 10, 7)
    # Older partial implementation got original year correct but REUSED
    # minute-one modern 6d, which this new independent 1647 read corrects.
    assert (prior_partial.resulting_years, prior_partial.resulting_days) == (70, 10)
    assert source.source_years == 70


def test_whole_1647_degree_component_cells_independently_match_modern_day_hours() -> None:
    assert len(DEGREE_PHOTO_COMPONENTS) == 91
    assert len(DEGREE_PHOTO_YEARS) == 91
    assert DEGREE_PHOTO_COMPONENTS == RETYPE_DEGREE
    assert DEGREE_PHOTO_YEARS[68] == 68
    assert DEGREE_PHOTO_YEARS[69] == 70
    assert DEGREE_PHOTO_YEARS[90] == 91
    assert sum(DEGREE_PHOTO_YEARS[k] != k for k in range(1, 91)) == 22
    assert DEGREE_PHOTO_COMPONENTS[80] == (62, 24)


def test_reliably_read_original_minute_rows_only_one_confirmed_numeric_mismatch() -> None:
    assert len(MINUTE_PHOTO_COMPONENTS) == 54  # incl editorial 0'
    assert frozenset({27}) == MINUTE_LABEL_ABSENT
    assert frozenset({25, 28, 39, 41, 44, 48}) == MINUTE_PARTIALLY_LEGIBLE
    differences = {
        k: (v, RETYPE_MINUTE[k])
        for k, v in MINUTE_PHOTO_COMPONENTS.items()
        if k in RETYPE_MINUTE and v != RETYPE_MINUTE[k]
    }
    assert differences == {1: ((5, 4), (6, 4))}
    assert MINUTE_PHOTO_COMPONENTS[8] == (44, 10)
    assert MINUTE_PHOTO_COMPONENTS[60] == (374, 14)
    assert minute_status(27) is SourceCellStatus.LABEL_ABSENT
    assert minute_status(44) is SourceCellStatus.PHOTO_PARTIALLY_LEGIBLE
    assert minute_status(0) is SourceCellStatus.ADDED_ZERO_IDENTITY


@pytest.mark.parametrize("minute", sorted(MINUTE_PARTIALLY_LEGIBLE))
def test_faint_minute_original_fails_closed_instead_of_using_retype(minute: int) -> None:
    with pytest.raises(SourceWitnessUnavailable, match="not securely legible"):
        independent_photo_lookup(11, minute)


def test_missing_minute_27_remains_absent_not_imputed() -> None:
    with pytest.raises(SourceWitnessUnavailable, match="label is absent"):
        independent_photo_lookup(0, 27)


def test_selected_original_printed_anomalies_remain_unfixed() -> None:
    one = independent_photo_lookup(0, 1)
    eight = independent_photo_lookup(0, 8)
    degree80 = independent_photo_lookup(80, 0)
    assert (one.result_days, one.result_hours) == (5, 4)
    assert (eight.result_days, eight.result_hours) == (44, 10)
    assert degree80.source_degree_hours == 24
    assert (degree80.result_years, degree80.result_days, degree80.result_hours) == (81, 63, 0)
    assert all("not_continuous_time_key" in x.to_dict() for x in (one, eight, degree80))


def test_original_worked_examples_same_as_first_edition_photo() -> None:
    first = independent_photo_lookup(11, 55)
    second = independent_photo_lookup(19, 52)
    assert (first.result_years, first.result_days, first.result_hours) == (12, 33, 14)
    assert (second.result_years, second.result_days, second.result_hours) == (20, 57, 21)
    assert literal_naibod_lookup(19, 52).resulting_years == 20
    # The extra '22 years' in 2003 prose is not the original printed text.


def test_full_row_registry_marks_unverified_cells_blank() -> None:
    with (DOC / "LILLY_NAIBOD_1647_WELLCOME_VS_2003_BY_ROW.csv").open(
        newline="", encoding="utf-8"
    ) as source:
        rows = list(csv.DictReader(source))
    assert len(rows) == 152
    degrees = [r for r in rows if r["table"] == "degree_component"]
    minutes = [r for r in rows if r["table"] == "minute_component"]
    assert len(degrees) == 91 and len(minutes) == 61
    verified_diff = [r for r in rows if r["verified_difference"]]
    assert len(verified_diff) == 23
    assert sum("original_year" in r["verified_difference"] for r in verified_diff) == 22
    assert sum("2003_day" in r["verified_difference"] for r in verified_diff) == 1
    first = next(r for r in minutes if r["angle_row_label"] == "1")
    assert (first["original_1647_days"], first["retype_2003_days"]) == ("5", "6")
    for r in minutes:
        row = int(r["angle_row_label"])
        if row in MINUTE_LABEL_ABSENT | MINUTE_PARTIALLY_LEGIBLE:
            assert not r["original_1647_days"] and not r["original_1647_hours"]
        if row in MINUTE_PARTIALLY_LEGIBLE:
            assert r["retype_2003_days"] and r["retype_2003_hours"]
    assert sum(r["original_status"] == "photograph_confirmed" for r in minutes) == 53


def test_source_lookup_rejects_fractions_and_out_of_table_range() -> None:
    with pytest.raises(TypeError):
        independent_photo_lookup(2.0, 1)
    with pytest.raises(TypeError):
        independent_photo_lookup(20, True)
    for degree, minute in ((-1, 0), (91, 0), (0, 60), (0, -1)):
        with pytest.raises(ValueError, match="range"):
            independent_photo_lookup(degree, minute)


def test_cli_and_default_previous_code_still_usable(capsys) -> None:
    from hdmatch.astrology.lilly_1647_photo import main

    assert main(["--degrees", "69", "--minutes", "1"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["result_years"] == 70
    assert result["result_days"] == 9
    assert result["not_continuous_time_key"] is True
    with pytest.raises(SystemExit) as bad:
        main(["--degrees", "11", "--minutes", "44"])
    assert bad.value.code == 2
    assert literal_naibod_lookup(0, 1).literal_minute_days == 6
    assert original_1647_critical_comparison(0, 1).literal_days_from_minutes == 6


def test_second_1647_photo_copy_is_real_and_has_separate_hashes() -> None:
    """Wellcome and older Internet Archive copies are different physical scans."""
    prior = ROOT / "docs/astrology-research-map/gansten-lilly-original-1647-20261024"
    earlier = json.loads((prior / "ORIGINAL_1647_SOURCE_COMPARISON.json").read_text())
    assert earlier["original_1647_read"] is True
    wellcome = json.loads((DOC / "SOURCE_PROVENANCE.json").read_text())
    for page in ("713", "714", "715"):
        previous = earlier["original_source"]["file_images"][page]
        older_file = prior / previous["file"]
        recent_file = DOC / "facsimile_pages" / f"wellcome_original_1647_printed_{page}.jpg"
        assert older_file.is_file() and recent_file.is_file()
        assert hashlib.sha256(older_file.read_bytes()).hexdigest() == previous["sha256"]
        assert (
            previous["sha256"]
            != wellcome["first_edition_witness_A"]["source_image_file_SHA256"][page]
        )
        assert older_file.stat().st_size != recent_file.stat().st_size
