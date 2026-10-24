#!/usr/bin/env python3
"""Generate full row-by-row 1647 original vs 2003 re-typeset comparison.

The 1647 numbers come only from the independently read high-resolution
photographs (module lilly_1647_photo.py). The 2003 candidate values
remain in distinct comparison columns and are NEVER backfilled into
faint original cells.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from hdmatch.astrology.historical_naibod import (
    DEGREE_COMPONENTS as RETYPE_DEGREE,
)
from hdmatch.astrology.historical_naibod import (
    MINUTE_COMPONENTS as RETYPE_MINUTE,
)
from hdmatch.astrology.lilly_1647_photo import (
    DEGREE_PHOTO_COMPONENTS,
    DEGREE_PHOTO_YEARS,
    MINUTE_LABEL_ABSENT,
    MINUTE_PARTIALLY_LEGIBLE,
    MINUTE_PHOTO_COMPONENTS,
    SOURCE_1647,
    SourceCellStatus,
    minute_status,
)

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent

files = {
    713: "wellcome_original_1647_printed_713.jpg",
    714: "wellcome_original_1647_printed_714.jpg",
    715: "wellcome_original_1647_printed_715.jpg",
}
SHA = {
    713: "cf11fb6cd819549b4f359670a04faded417526ddecf3171ccd7a46f6d68d9776",
    714: "bc76d574f3d57bdd76f533dedbdc6d9cf2b6423d5a841adfd849ee77538b92ac",
    715: "e333f2442238e68a1c7ebed4fdcf9e43691d3f72ed256d2eca2bfca10458216e",
}
for page, file in files.items():
    photo = OUT / "facsimile_pages" / file
    assert photo.is_file(), photo
    assert hashlib.sha256(photo.read_bytes()).hexdigest() == SHA[page]

rows: list[dict[str, object]] = []
for degree in range(91):
    day, hour = DEGREE_PHOTO_COMPONENTS[degree]
    modern_day, modern_hour = RETYPE_DEGREE[degree]
    years = DEGREE_PHOTO_YEARS[degree]
    assert (day, hour) == (modern_day, modern_hour), degree
    status = (
        SourceCellStatus.ADDED_ZERO_IDENTITY.value
        if degree == 0
        else SourceCellStatus.PHOTOGRAPH_CONFIRMED.value
    )
    rows.append(
        {
            "original_printed_page": 713,
            "table": "degree_component",
            "angle_row_label": degree,
            "original_1647_years": years,
            "original_1647_days": day,
            "original_1647_hours": hour,
            "original_status": status,
            "retype_2003_years": degree,
            "retype_2003_days": modern_day,
            "retype_2003_hours": modern_hour,
            "verified_difference": (
                "original_year_column_plus_one_after_68" if years != degree else ""
            ),
            "source_note": (
                "Editorial zero-arc identity, not a printed row"
                if degree == 0
                else "Source table printed on p713, IIIF canvas 747"
            ),
        }
    )
for minute in range(61):
    status = minute_status(minute)
    verified = MINUTE_PHOTO_COMPONENTS.get(minute)
    modern = RETYPE_MINUTE.get(minute)
    if status is SourceCellStatus.PHOTO_PARTIALLY_LEGIBLE:
        assert verified is None
        assert modern is not None
    if status is SourceCellStatus.LABEL_ABSENT:
        assert verified is None and modern is None
    if verified is not None:
        difference = (
            "2003_day_does_not_match_1647_original"
            if modern is not None and modern != verified
            else ""
        )
    else:
        difference = ""
    rows.append(
        {
            "original_printed_page": 714,
            "table": "minute_component",
            "angle_row_label": minute,
            "original_1647_years": "",
            "original_1647_days": verified[0] if verified is not None else "",
            "original_1647_hours": verified[1] if verified is not None else "",
            "original_status": status.value,
            "retype_2003_years": "",
            "retype_2003_days": modern[0] if modern is not None else "",
            "retype_2003_hours": modern[1] if modern is not None else "",
            "verified_difference": difference,
            "source_note": (
                "Printed label 27′ absent from BOTH original copies"
                if minute in MINUTE_LABEL_ABSENT
                else "Printed value faint in BOTH original copies; 2003 digits NOT authenticated"
                if minute in MINUTE_PARTIALLY_LEGIBLE
                else "Source table printed on p714, IIIF canvas 748"
            ),
        }
    )
assert len(rows) == 152
assert sum(r["verified_difference"] == "original_year_column_plus_one_after_68" for r in rows) == 22
assert sum(r["verified_difference"] == "2003_day_does_not_match_1647_original" for r in rows) == 1
assert [
    int(r["angle_row_label"])
    for r in rows
    if r["verified_difference"] == "2003_day_does_not_match_1647_original"
] == [1]
assert sum(r["original_status"] == "photo_partially_legible" for r in rows) == 6

path = OUT / "LILLY_NAIBOD_1647_WELLCOME_VS_2003_BY_ROW.csv"
with path.open("w", encoding="utf-8", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

original_example = {
    "original_1647": {
        "minute_1": {"days": 5, "hours": 4},
        "minute_8": {"days": 44, "hours": 10},
        "minute_27": {"status": "absent", "no_inferred_numeric_cell": True},
        "minute_44": {
            "status": "unverified_original_day_hour",
            "retype_candidate_only": {"days": RETYPE_MINUTE[44][0], "hours": RETYPE_MINUTE[44][1]},
        },
        "degree_69": {"years": 70, "days": 4, "hours": 3},
    },
    "retype_2003": {
        "minute_1": {"days": RETYPE_MINUTE[1][0], "hours": RETYPE_MINUTE[1][1]},
        "minute_8": {"days": RETYPE_MINUTE[8][0], "hours": RETYPE_MINUTE[8][1]},
        "degree_69": {"years": 69, "days": 4, "hours": 3},
    },
    "verified_original_corrections": {
        "degree_year_column_rows_69_to_90": 22,
        "minute_1_day_column": 1,
        "total_table_cells": 23,
        "worked_19_52_prose_2003_only": (
            "2003 concluding prose says 22 years, "
            "original 1647 concluding prose says 20 years; "
            "both tables have the same 19°52' arithmetic"
        ),
    },
}
(OUT / "LILLY_1647_CRITICAL_DIFFERENCES.json").write_text(
    json.dumps(original_example, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)

provenance = {
    "schema": "LILLY_1647_INDEPENDENT_WELLCOME_COLLATION_V1",
    "date": "2026-10-24",
    "root_project_goal": (
        "Historically source-differentiated astrology calculations, "
        "frozen before combined forward-blind human validation; not an empirical claim."
    ),
    "first_edition_witness_A": {
        "repository": "Wellcome Collection",
        "work": "https://wellcomecollection.org/works/s7z7c46y",
        "iiif_manifest": "https://iiif.wellcomecollection.org/presentation/v2/b30338724",
        "printed_page_to_zero_based_canvas": {"713": 747, "714": 748, "715": 749},
        "source_image_file_SHA256": {str(page): SHA[page] for page in SHA},
        "image_resolution": "3141×4249",
        "license": "Public Domain Mark on Wellcome catalogue",
    },
    "first_edition_witness_B": {
        "repository": "Internet Archive ca-william-lilly",
        "source_file": (
            "../gansten-lilly-original-1647-20261024/ORIGINAL_1647_SOURCE_COMPARISON.json"
        ),
        "printed_pages": [713, 714, 715],
        "independently_compared": True,
    },
    "modern_comparison_witness": {
        "edition": "WorldAstrology retypeset Christian Astrology Book III, 2003",
        "file": ("../gansten-lilly-naibod-20261024/LILLY_NAIBOD_2003_RETYPED_LITERAL_CELLS.csv"),
        "retained_unchanged": True,
    },
    "source_transcription": SOURCE_1647,
    "degree_rows_original_excluding_zero": 90,
    "minute_labels_range": [1, 60],
    "minute_labels_physically_present": 59,
    "minute_rows_original_photograph_confirmed": sum(
        r["table"] == "minute_component" and r["original_status"] == "photograph_confirmed"
        for r in rows
    ),
    "minute_rows_ambiguous": sorted(MINUTE_PARTIALLY_LEGIBLE),
    "minute_row_missing": sorted(MINUTE_LABEL_ABSENT),
    "confirmed_source_differences": {
        "original_degree_year_vs_retype": 22,
        "original_minute_day_vs_retype": 1,
        "total_confirmed_table_cell_differences": 23,
        "newly_discovered_minute_1": {"original_1647": "5d4h", "2003_retype": "6d4h"},
    },
    "uncertainty_policy": (
        "Original faint cells are blank in original 1647 columns. "
        "Modern 2003 candidate digits are separate and never auto-filled. "
        "Missing minute 27 remains absent, not inferred. "
        "Original print anomalies are retained, not silently corrected."
    ),
    "full_unambiguous_minute_table_authenticated": False,
    "original_1647_lookup_is_a_complete_historical_timing_key": False,
    "human_predictive_validity": "UNTESTED",
}
(OUT / "SOURCE_PROVENANCE.json").write_text(
    json.dumps(provenance, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)
print(
    json.dumps(
        {
            "result": "PASS",
            "rows": len(rows),
            "original_degree_rows": 90,
            "original_minutes_visible": provenance["minute_rows_original_photograph_confirmed"],
            "ambiguous_minutes": sorted(MINUTE_PARTIALLY_LEGIBLE),
            "missing_minutes": sorted(MINUTE_LABEL_ABSENT),
            "confirmed_retype_differences": 23,
        },
        indent=2,
    )
)
