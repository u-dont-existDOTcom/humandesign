#!/usr/bin/env python3
"""Reproducible, source-backed verification manifest for second Lilly 1647 scan."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from hdmatch.astrology.historical_naibod import (
    DEGREE_COMPONENTS as modern_degree,
)
from hdmatch.astrology.historical_naibod import (
    MINUTE_COMPONENTS as modern_minute,
)
from hdmatch.astrology.lilly_1647_photo import (
    DEGREE_PHOTO_COMPONENTS,
    DEGREE_PHOTO_YEARS,
    MINUTE_LABEL_ABSENT,
    MINUTE_PARTIALLY_LEGIBLE,
    MINUTE_PHOTO_COMPONENTS,
    independent_photo_lookup,
)

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
# Pin the historical parent as provenance. The script must remain replayable
# from the subsequently committed research branch and its shallow clone,
# where git HEAD no longer equals the original parent revision.
parent = "931784fb7ae691a80eb42a3c2cd0bcbeac942274"

provenance = json.loads((HERE / "SOURCE_PROVENANCE.json").read_text())
with (HERE / "LILLY_NAIBOD_1647_WELLCOME_VS_2003_BY_ROW.csv").open(
    encoding="utf-8", newline=""
) as stream:
    rows = list(csv.DictReader(stream))
assert len(rows) == 152
assert modern_degree == DEGREE_PHOTO_COMPONENTS
assert len(DEGREE_PHOTO_YEARS) == 91
assert len(MINUTE_PHOTO_COMPONENTS) == 54
assert len(MINUTE_PARTIALLY_LEGIBLE) == 6
assert frozenset({27}) == MINUTE_LABEL_ABSENT
assert [
    k
    for k in MINUTE_PHOTO_COMPONENTS
    if k in modern_minute and MINUTE_PHOTO_COMPONENTS[k] != modern_minute[k]
] == [1]

for page, source_hash in provenance["first_edition_witness_A"]["source_image_file_SHA256"].items():
    image = HERE / "facsimile_pages" / f"wellcome_original_1647_printed_{page}.jpg"
    assert image.is_file()
    assert hashlib.sha256(image.read_bytes()).hexdigest() == source_hash

previous_original = (
    ROOT
    / "docs/astrology-research-map/gansten-lilly-original-1647-20261024"
    / "ORIGINAL_1647_SOURCE_COMPARISON.json"
)
previous_modern = (
    ROOT
    / "docs/astrology-research-map/gansten-lilly-naibod-20261024"
    / "LILLY_NAIBOD_2003_RETYPED_LITERAL_CELLS.csv"
)
assert previous_original.is_file() and previous_modern.is_file()
earlier = json.loads(previous_original.read_text())
assert earlier["original_1647_read"]
assert earlier["discrepancies"]["year_69"]["1647_years"] == 70
assert earlier["discrepancies"]["worked_19_52"]["1647_final_years"] == 20
assert (
    independent_photo_lookup(0, 1).result_days,
    independent_photo_lookup(69, 1).result_years,
    independent_photo_lookup(69, 1).result_days,
) == (5, 70, 9)

retyped_cells = [r for r in rows if r["verified_difference"]]
assert len(retyped_cells) == 23
assert sum("original_year" in r["verified_difference"] for r in retyped_cells) == 22
assert sum("2003_day" in r["verified_difference"] for r in retyped_cells) == 1
files = [
    "src/hdmatch/astrology/lilly_1647_photo.py",
    "tests/unit/test_lilly_1647_photo.py",
    "docs/astrology-research-map/lilly-1647-independent-table-collation-20261024/regenerate_collation.py",
    "docs/astrology-research-map/lilly-1647-independent-table-collation-20261024/README.md",
    "docs/astrology-research-map/lilly-1647-independent-table-collation-20261024/CONTINUATION_CHECKPOINT.md",
    "docs/astrology-research-map/lilly-1647-independent-table-collation-20261024/RESEARCH_DECISION_AND_RESUME_LOG.md",
    "docs/astrology-research-map/lilly-1647-independent-table-collation-20261024/LILLY_NAIBOD_1647_WELLCOME_VS_2003_BY_ROW.csv",
    "docs/astrology-research-map/lilly-1647-independent-table-collation-20261024/LILLY_1647_CRITICAL_DIFFERENCES.json",
    "docs/astrology-research-map/lilly-1647-independent-table-collation-20261024/SOURCE_PROVENANCE.json",
]
files.extend(
    str(path.relative_to(ROOT)) for path in sorted((HERE / "facsimile_pages").glob("*.jpg"))
)
assert len(files) == 12
assert all((ROOT / name).is_file() for name in files)

manifest = {
    "schema": "LILLY_1647_INDEPENDENT_PHOTO_AND_2003_RETYPE_AUDIT_V1",
    "date": "2026-10-24",
    "branch": "research/lilly-1647-minute-collation-20261024",
    "parent_commit": parent,
    "purpose": (
        "accurately sourced competing astrology calculations, frozen "
        "before joint forward-blind empirical test"
    ),
    "state": "SUBTASK_COMPLETE_PARENT_OPEN_RESEARCH_ONLY",
    "independent_sources": [
        "Wellcome high-resolution first-edition color scan b30338724 printed pp713–715",
        "Internet Archive ca-william-lilly different 1647 first-edition copy, previously preserved",
        "WorldAstrology modern 2003 retypeset, comparison only and untouched",
    ],
    "new_result": {
        "first_edition_photo_minute_1": {"days": 5, "hours": 4},
        "modern_retype_minute_1": {"days": 6, "hours": 4},
        "verified_degree_year_differences": 22,
        "verified_minute_day_differences": 1,
        "verified_numerical_table_cell_differences": 23,
        "minute_rows_original_photo_read": 53,
        "minute_rows_faint_original": sorted(MINUTE_PARTIALLY_LEGIBLE),
        "minute_row_absent": 27,
        "original_1647_all_degree_day_hour_values_checked": True,
        "original_1647_full_minute_table_uncertainty_resolved": False,
        "2003_retype_19degree52prose_22vs1647original20": True,
    },
    "assurance": {
        "tests": "122 passed",
        "test_command": (
            "PYTHONPATH=src "
            "HDMATCH_PRIMARY_DIR_EPHE_DIR=$HOME/.local/share/hdmatch/ephemeris/1800-2399 "
            "$HOME/humandesign/.venv/bin/python -m pytest -q "
            "tests/unit/test_lilly_1647_photo.py tests/unit/test_placidus_1657_latin.py "
            "tests/unit/test_solar_primary_source_scope.py tests/unit/test_solar_time_keys.py "
            "tests/unit/test_naibod_original_1647.py tests/unit/test_historical_naibod.py "
            "tests/unit/test_primary_direction_roles.py "
            "tests/unit/test_primary_direction_aspects.py "
            "tests/unit/test_primary_directions.py tests/unit/test_astronomy_reference.py "
            "tests/unit/test_relationship_western_rrf.py"
        ),
        "ruff": "passed",
        "mypy": "passed (13 source modules)",
        "existing_default_time_key_unchanged": True,
        "old_2003_text_and_partial_original_comparator_unchanged": True,
        "future_predictive_validity": "untested",
        "uses_human_personal_birth_data": False,
    },
    "previous_retype_csv_sha256": hashlib.sha256(previous_modern.read_bytes()).hexdigest(),
    "previous_original_correction_sha256": hashlib.sha256(
        previous_original.read_bytes()
    ).hexdigest(),
    "first_edition_source_images_sha256": provenance["first_edition_witness_A"][
        "source_image_file_SHA256"
    ],
    "files": {
        name: {
            "bytes": (ROOT / name).stat().st_size,
            "sha256": hashlib.sha256((ROOT / name).read_bytes()).hexdigest(),
        }
        for name in files
    },
    "HDD_use": "Store on local NVMe; /mnt/hdd nearly full.",
}
(HERE / "VERIFICATION.json").write_text(
    json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)
print(
    json.dumps(
        {
            "status": "PASS",
            "new_files": len(files),
            "photo_confirmed_minute_1": "5d4h",
            "verified_table_cell_differences": 23,
            "uncertain_minutes": sorted(MINUTE_PARTIALLY_LEGIBLE),
            "verification_sha256": hashlib.sha256(
                (HERE / "VERIFICATION.json").read_bytes()
            ).hexdigest(),
        },
        indent=2,
    )
)
