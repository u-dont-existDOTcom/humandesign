#!/usr/bin/env python3
"""Append Libra/Scorpio source-photo readings, keep earlier 1647 records immutable."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
PREV = B.parent / "B07aa"
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V3.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


new = j(B / "PHOTO_SOURCE_LIBRA_SCORPIO_V1.json")
old = j(PREV / "ANNUAL_RATE_PHOTO_OVERLAY_V3.json")
assert j(WEST)["records_count"] == 12472 and j(CHINA)["sum_source_annotations"] == 142
assert old["cumulative_photo_one_reader_legible"] == 205
assert old["cumulative_photo_glyphs_unresolved"] == 4
assert old["cumulative_unexamined_original_positions"] == 163
assert (
    sha(B.parent / "B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg")
    == (new["photo_parent_sha256"])
)
assert new["source_positions_total"] == 62
assert new["new_original_photo_positions"] == 58
assert new["prior_B07y_source_overlap"] == 4
assert new["unresolved_this_pass"] == 0

prior = {(r["sign"], r["degree"]): r for r in old["rows"]}
source = {(r["sign"], r["degree"]): r for r in new["records"]}
assert len(prior) == 372 and len(source) == 62
assert all((s, k) in source for s in ("Libra", "Scorpio") for k in range(31))
overlaps = {key for key, r in source.items() if r["previous_B07y_photo_reading"]}
assert overlaps == {("Libra", 7), ("Libra", 21), ("Libra", 22), ("Libra", 23)}
assert all(prior[key]["source_read_batch"] == "B07y" for key in overlaps)
assert all(prior[key]["source_read_batch"] is None for key in source if key not in overlaps)
assert len(list((B / "evidence").glob("*_half.png"))) == 4
differences = []
rows = []
for earlier in old["rows"]:
    key = (earlier["sign"], earlier["degree"])
    now = source.get(key)
    row = dict(earlier)
    if now is not None:
        reading = [now["original_1647_rate_arcminutes"], now["original_1647_rate_arcseconds"]]
        if key in overlaps:
            assert row["first_edition_1647_one_reader_photo_rate"] == reading
            assert row["source_read_batch"] == "B07y"
        else:
            assert row["first_edition_1647_one_reader_photo_rate"] is None
            assert row["unresolved_original_source_glyph_options"] is None
            row["first_edition_1647_one_reader_photo_rate"] = reading
            row["first_edition_source_photo_verified_by_one_reader"] = True
            row["source_read_batch"] = "B07ab"
            if row["frozen_B07x_derivative_candidate"] != reading:
                differences.append(
                    {
                        "sign": key[0],
                        "degree": key[1],
                        "original_1647": reading,
                        "B07x_derivative": row["frozen_B07x_derivative_candidate"],
                        "only_one_original_photo_reader": True,
                    }
                )
    assert not row["runtime_promoted"]
    rows.append(row)

assert differences == [
    {
        "sign": "Scorpio",
        "degree": 6,
        "original_1647": [58, 32],
        "B07x_derivative": [58, 22],
        "only_one_original_photo_reader": True,
    },
    {
        "sign": "Scorpio",
        "degree": 21,
        "original_1647": [61, 39],
        "B07x_derivative": [61, 29],
        "only_one_original_photo_reader": True,
    },
]
assert len(rows) == 372
assert sum(r["first_edition_1647_one_reader_photo_rate"] is not None for r in rows) == 263
assert sum(bool(r["unresolved_original_source_glyph_options"]) for r in rows) == 4
assert (
    sum(
        r["first_edition_1647_one_reader_photo_rate"] is None
        and not r["unresolved_original_source_glyph_options"]
        for r in rows
    )
    == 105
)
out = {
    "schema": "LILLY_1647_B07ab_ANNUAL_RATE_PHOTO_OVERLAY_V4",
    "batch": "B07ab",
    "parent_B07aa_sha256": sha(PREV / "ANNUAL_RATE_PHOTO_OVERLAY_V3.json"),
    "original_full_1647_source_sha256": new["full_original_pdf_sha256"],
    "original_photo_pdf745_sha256": new["photo_parent_sha256"],
    "source_packet_sha256": sha(B / "PHOTO_SOURCE_LIBRA_SCORPIO_V1.json"),
    "source_372_positions": 372,
    "added_Libra_Scorpio_source_readings": 58,
    "old_source_photo_overlaps_unmodified": 4,
    "new_derivative_source_conflicts": differences,
    "cumulative_one_reader_original_photo_legible": 263,
    "cumulative_original_glyphs_unresolved": 4,
    "not_read_original_table_remaining": 105,
    "new_source_reviewer_count": 1,
    "independent_two_reader_agreement_verified": False,
    "full_table_original_photo_complete": False,
    "genuine_17th_century_astronomical_method_parity_verified": False,
    "empirical_real_person_predictions_validated": 0,
    "runtime_promotions": 0,
    "Lilly_canonical_source_index_retained": 12472,
    "Chinese_V3_canonical_source_index_retained": 142,
    "rows": rows,
}
target = B / "ANNUAL_RATE_PHOTO_OVERLAY_V4.json"
target.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(
    json.dumps(
        {
            "rows": len(rows),
            "new": 58,
            "cumulative": 263,
            "unknown": 105,
            "unclear": 4,
            "new_discrepancies": differences,
            "overlay_sha256": sha(target),
        },
        indent=2,
    )
)
