"""Original 1647 first-edition photographic check, kept apart from 2003 retype.

The physical comparison is established from image-backed evidence (see
SOURCE_COMPARISON.md and the three public-domain page photographs).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from hdmatch.astrology.historical_naibod import literal_naibod_lookup
from hdmatch.astrology.naibod_original_1647 import (
    YEAR_COLUMN_1647,
    original_1647_critical_comparison,
)

HERE = Path(__file__).resolve().parents[2]


def test_original_first_edition_year_column_has_carried_year_at_69() -> None:
    assert len(YEAR_COLUMN_1647) == 91
    assert YEAR_COLUMN_1647[68] == 68
    assert YEAR_COLUMN_1647[69] == 70
    assert YEAR_COLUMN_1647[70] == 71
    assert YEAR_COLUMN_1647[80] == 81
    assert YEAR_COLUMN_1647[90] == 91
    assert all(YEAR_COLUMN_1647[d] == d + 1 for d in range(69, 91))


def test_original_first_edition_68_to_69_no_artificial_backwards_year() -> None:
    old68 = literal_naibod_lookup(68, 0)
    old69 = literal_naibod_lookup(69, 0)
    newer68 = original_1647_critical_comparison(68, 0)
    newer69 = original_1647_critical_comparison(69, 0)
    assert old68.resulting_years == newer68.resulting_years == 68
    assert old69.resulting_years == 69
    assert newer69.resulting_years == 70
    assert newer69.resulting_days == 4
    assert newer69.resulting_hours == 3
    assert newer69.resulting_years > newer68.resulting_years
    assert any("2003_retype" in x for x in newer69.differences_from_2003)


def test_original_first_edition_p715_conclusion_resolves_2003_transcript() -> None:
    ret = literal_naibod_lookup(19, 52)
    orig = original_1647_critical_comparison(19, 52)
    assert (orig.resulting_years, orig.resulting_days, orig.resulting_hours) == (20, 57, 21)
    assert orig.resulting_years == ret.resulting_years
    assert any(
        "original_1647_worked_conclusion:twenty_years" in x for x in orig.differences_from_2003
    )
    assert all(
        "shared_or_unresolved_source_anomaly:Printed p.715" not in x
        for x in orig.differences_from_2003
    )


def test_first_worked_example_agrees_across_witnesses() -> None:
    retype = literal_naibod_lookup(11, 55)
    original = original_1647_critical_comparison(11, 55)
    assert (
        original.resulting_years,
        original.resulting_days,
        original.resulting_hours,
    ) == (12, 33, 14)
    assert (
        retype.resulting_years,
        retype.resulting_days,
        retype.resulting_hours,
    ) == (12, 33, 14)
    assert not original.differences_from_2003


def test_second_witness_preserves_anomalies_not_silent_repair() -> None:
    original8 = original_1647_critical_comparison(11, 8)
    original44 = original_1647_critical_comparison(11, 44)
    original60 = original_1647_critical_comparison(80, 0)
    assert any("shared_or_unresolved" in x for x in original8.differences_from_2003)
    assert any("shared_or_unresolved" in x for x in original44.differences_from_2003)
    assert original60.first_edition_degree_years == 81
    assert original60.literal_hours_from_degree == 24
    assert original60.resulting_hours == 0
    with pytest.raises(ValueError, match="missing: 27"):
        original_1647_critical_comparison(22, 27)


def test_original_comparison_provenance_is_not_full_witness_claim() -> None:
    x = original_1647_critical_comparison(75, 55).to_dict()
    assert x["not_continuous_timeline_key"] is True
    assert x["candidate_status"] == "source_compared_not_full_original_collation"
    assert "NOT an exhaustive" in x["source_limits"]
    assert "1647" in x["witness"]
    assert "2003_retype" in str(x["differences_from_2003"])


def test_frozen_2003_witness_and_continuous_keys_do_not_change() -> None:
    previous = literal_naibod_lookup(69, 0)
    assert previous.resulting_years == 69
    from hdmatch.astrology.timeline import TimeKey, degrees_per_symbolic_year

    assert len(TimeKey) == 4
    assert degrees_per_symbolic_year(TimeKey.NAIBOD_59M08S_FIXED_DIAGNOSTIC) == (59 * 60 + 8) / 3600
    assert degrees_per_symbolic_year(TimeKey.PTOLEMY_ONE_EQUINOCTIAL_DEGREE_PER_YEAR) == 1


def test_first_edition_evidence_metadata_and_cited_pages() -> None:
    doc = (
        HERE
        / "docs/astrology-research-map/gansten-lilly-original-1647-20261024"
        / "ORIGINAL_1647_SOURCE_COMPARISON.json"
    )
    evidence = json.loads(doc.read_text())
    assert evidence["source_first_edition_printed_pages"] == [713, 714, 715]
    assert evidence["pdf_page_numbers_1_based"] == [735, 736, 737]
    assert evidence["original_1647_read"] is True
    assert evidence["original_1647_full_table_diplomatic_collation"] is False
    assert evidence["discrepancies"]["year_69"]["1647_years"] == 70
    assert evidence["discrepancies"]["worked_19_52"]["1647_final_years"] == 20
    for page in [713, 714, 715]:
        evidence_file = doc.parent / "facsimile_pages" / f"lilly_1647_printed_{page}.jpg"
        assert evidence_file.is_file() and evidence_file.stat().st_size > 100_000


def test_original_witness_comparator_does_not_inherit_retype_only_warnings() -> None:
    result = original_1647_critical_comparison(69, 0)
    assert any("original_1647_year_column" in x for x in result.differences_from_2003)
    assert not any("shared_or_unresolved" in x for x in result.differences_from_2003)
    assert result.resulting_years == 70


def test_standalone_cli_outputs_original_and_retype_side_by_side(capsys) -> None:
    from hdmatch.astrology.naibod_original_1647 import main

    assert main(["--degrees", "69", "--minutes", "0"]) == 0
    doc = json.loads(capsys.readouterr().out)
    assert doc["resulting_years"] == 70
    assert doc["first_edition_degree_years"] == 70
    assert doc["not_continuous_timeline_key"] is True
    assert doc["candidate_status"] == "source_compared_not_full_original_collation"
    with pytest.raises(SystemExit) as exc:
        main(["--degrees", "22", "--minutes", "27"])
    assert exc.value.code == 2


def test_source_images_have_exact_verified_hashes() -> None:
    import hashlib

    doc = HERE / "docs/astrology-research-map/gansten-lilly-original-1647-20261024"
    records = json.loads((doc / "ORIGINAL_1647_SOURCE_COMPARISON.json").read_text())
    for page, meta in records["original_source"]["file_images"].items():
        img = (doc / meta["file"]).read_bytes()
        assert len(img) > 100_000, page
        assert hashlib.sha256(img).hexdigest() == meta["sha256"], page


def test_year_column_csv_has_exactly_22_original_differences() -> None:
    import csv

    doc = HERE / "docs/astrology-research-map/gansten-lilly-original-1647-20261024"
    with (doc / "YEAR_COLUMN_1647_VS_2003.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 90
    assert sum(int(row["difference_1647_minus_2003_years"]) for row in rows) == 22
    assert all(int(row["difference_1647_minus_2003_years"]) == 0 for row in rows[:68])
    assert all(int(row["difference_1647_minus_2003_years"]) == 1 for row in rows[68:])
    assert all(row["day_hour_columns_fully_original_collated"] == "False" for row in rows)
