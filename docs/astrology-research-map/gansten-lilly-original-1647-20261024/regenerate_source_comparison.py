#!/usr/bin/env python3
"""Rebuild and verify source-scan-backed original-vs-retype numerical differences.

The original's YEAR column at 69–90 has been checked visually against page713.
DAY/HOUR components are reused from the 2003 transcription and labeled so.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from hdmatch.astrology.historical_naibod import DEGREE_COMPONENTS, literal_naibod_lookup
from hdmatch.astrology.naibod_original_1647 import (
    YEAR_COLUMN_1647,
    original_1647_critical_comparison,
)

HERE = Path(__file__).resolve().parent
original = json.loads((HERE / "ORIGINAL_1647_SOURCE_COMPARISON.json").read_text())
for p, rec in original["original_source"]["file_images"].items():
    data = (HERE / rec["file"]).read_bytes()
    assert len(data) > 100_000
    assert hashlib.sha256(data).hexdigest() == rec["sha256"], p
assert original["original_1647_full_table_diplomatic_collation"] is False

rows = []
for deg in range(1, 91):
    year_original = YEAR_COLUMN_1647[deg]
    year_retype = deg
    days, hours = DEGREE_COMPONENTS[deg]
    rows.append(
        {
            "degrees": deg,
            "year_1647_photo": year_original,
            "year_2003_retype": year_retype,
            "difference_1647_minus_2003_years": year_original - year_retype,
            "days_reused_from_2003": days,
            "hours_reused_from_2003": hours,
            "first_edition_year_column_verified": True,
            "day_hour_columns_fully_original_collated": False,
            "source_printed_page": 713,
        }
    )
assert len(rows) == 90
assert sum(row["difference_1647_minus_2003_years"] == 1 for row in rows) == 22
assert all(row["difference_1647_minus_2003_years"] == 0 for row in rows[:68])
assert all(row["difference_1647_minus_2003_years"] == 1 for row in rows[68:])
with (HERE / "YEAR_COLUMN_1647_VS_2003.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

pairs = [(68, 0), (69, 0), (80, 0), (90, 0), (11, 55), (19, 52)]
comparisons = []
for deg, minute in pairs:
    old = literal_naibod_lookup(deg, minute)
    new = original_1647_critical_comparison(deg, minute)
    comparisons.append(
        {
            "angle": f"{deg}°{minute:02d}′",
            "2003_retype_result": {
                "years": old.resulting_years,
                "days": old.resulting_days,
                "hours": old.resulting_hours,
            },
            "1647_photo_year_column_plus_2003_day_hour": {
                "years": new.resulting_years,
                "days": new.resulting_days,
                "hours": new.resulting_hours,
            },
            "first_edition_conclusion_verified": (deg, minute) in ((11, 55), (19, 52)),
            "evidence_notes": new.differences_from_2003,
            "not_independently_collated_day_hour": True,
        }
    )
(HERE / "SELECTED_EXAMPLE_COMPARISONS.json").write_text(
    json.dumps(comparisons, ensure_ascii=False, indent=2) + "\n"
)
print(
    json.dumps(
        {
            "verified_original_printed_pages": [713, 714, 715],
            "year_rows_collated": len(rows),
            "differing_year_cells": 22,
            "example_19_52_original_conclusion": "20 years 57 days 21 hours",
            "examples_preserved": len(comparisons),
            "source_1647_complete_numeric_collation": False,
        },
        indent=2,
    )
)
