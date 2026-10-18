#!/usr/bin/env python3
"""Append Leo and Virgo original source photo readings without repeating B07y Leo0."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
PARENT = B.parent / "B07z"
ROOT = B.parents[3]
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V3.json"


def load(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


source = load(B / "PHOTO_SOURCE_COLUMNS_LEO_VIRGO_1647_V1.json")
before = load(PARENT / "ANNUAL_372_SOURCE_PHOTO_OVERLAY_V2.json")
idx = load(WEST)
ch = load(CHINESE)
assert idx["records_count"] == 12472 and ch["sum_source_annotations"] == 142
assert len(before["cells"]) == 372
assert before["one_reader_photo_read_positions_cumulative_B07y_B07z"] == 146
assert before["unresolved_original_photo_glyph_positions_cumulative"] == 2
assert before["not_yet_first_edition_photo_read_positions_cumulative"] == 224
assert source["new_direct_1647_photo_one_reader_entries"] == 59
assert source["new_ambiguous_photo_positions"] == 2
assert source["source_positions_already_audited_in_B07y"] == 1
assert (
    sha(B.parent / "B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg")
    == source["original_photo_sha256"]
)
for f in (
    "Leo_first_half.png",
    "Leo_second_half.png",
    "Virgo_first_half.png",
    "Virgo_second_half.png",
    "virgo_rows0_5.png",
    "virgo_rows15_22.png",
    "virgo_rows18_25.png",
    "leo_rows0_6.png",
):
    assert (B / "evidence" / f).is_file()
    assert (B / "evidence" / f).stat().st_size > 10_000

new = {(r["sign"], r["zodiac_degree"]): r for r in source["entries"]}
assert len(new) == 62
old = {(r["sign"], r["degree"]): r for r in before["cells"]}
assert len(old) == 372
assert all(key in old for key in new)
assert set(key for key, r in new.items() if r["previously_source_read_in_B07y"]) == {("Leo", 0)}
assert set(key for key, r in new.items() if r["unresolved_original_photo_glyph_options"]) == {
    ("Virgo", 1),
    ("Virgo", 18),
}
assert all(
    old[key]["source_read_batch"] is None
    for key, r in new.items()
    if not r["previously_source_read_in_B07y"]
)
assert old["Leo", 0]["first_edition_1647_one_reader_photo_rate"] == [59, 34]
assert new["Leo", 0]["original_photo_literal_rate_minutes_seconds"] == [59, 34]

rows = []
new_diffs = []
for prior in before["cells"]:
    key = (prior["sign"], prior["degree"])
    addition = new.get(key)
    result = dict(prior)
    if addition and not addition["previously_source_read_in_B07y"]:
        got = addition["original_photo_literal_rate_minutes_seconds"]
        unknown = addition["unresolved_original_photo_glyph_options"]
        assert prior["first_edition_1647_one_reader_photo_rate"] is None
        assert prior["unresolved_original_source_glyph_options"] is None
        if got is not None:
            result["first_edition_1647_one_reader_photo_rate"] = got
            result["first_edition_source_photo_verified_by_one_reader"] = True
        else:
            result["unresolved_original_source_glyph_options"] = unknown
        result["source_read_batch"] = "B07aa"
        if got and got != result["frozen_B07x_derivative_candidate"]:
            new_diffs.append(
                {
                    "sign": key[0],
                    "degree": key[1],
                    "derivative_originally_frozen": result["frozen_B07x_derivative_candidate"],
                    "1647_photo_one_reader": got,
                    "independent_second_reader_checked": False,
                }
            )
    result["independent_second_reader_verified"] = False
    result["modern_astro_chart_year_conversion_verified"] = False
    result["real_human_predictive_validation"] = False
    result["runtime_promoted"] = False
    rows.append(result)
assert new_diffs == [
    {
        "sign": "Virgo",
        "degree": 4,
        "derivative_originally_frozen": [54, 53],
        "1647_photo_one_reader": [54, 52],
        "independent_second_reader_checked": False,
    }
]
assert len(rows) == 372
assert sum(r["first_edition_1647_one_reader_photo_rate"] is not None for r in rows) == 205
assert sum(bool(r["unresolved_original_source_glyph_options"]) for r in rows) == 4
assert (
    sum(
        r["first_edition_1647_one_reader_photo_rate"] is None
        and not r["unresolved_original_source_glyph_options"]
        for r in rows
    )
    == 163
)

out = {
    "schema": "LILLY_1647_372_ANNUAL_RATE_B07aa_LEO_VIRGO_SOURCE_APPEND_V3",
    "batch": "B07aa",
    "original_first_edition_photo_sha256": source["original_photo_sha256"],
    "prior_B07z_overlay_sha256": sha(PARENT / "ANNUAL_372_SOURCE_PHOTO_OVERLAY_V2.json"),
    "new_source_Leo_Virgo_sha256": sha(B / "PHOTO_SOURCE_COLUMNS_LEO_VIRGO_1647_V1.json"),
    "source_parent_overlay_unchanged": True,
    "total_original_sign_degree_positions": 372,
    "B07aa_signs": ["Leo", "Virgo"],
    "B07aa_new_legible_one_reader_positions": 59,
    "B07aa_new_ambiguous_glyphs": 2,
    "B07aa_prior_B07y_reused_source_positions_not_recounted": 1,
    "B07aa_new_derivative_conflicts": new_diffs,
    "cumulative_photo_one_reader_legible": 205,
    "cumulative_photo_glyphs_unresolved": 4,
    "cumulative_unexamined_original_positions": 163,
    "West_Lilly_canonical_index_remains": 12472,
    "Chinese_canonical_V3_remains": 142,
    "real_people_independent_predictions_validated": 0,
    "runtime_model_promotions": 0,
    "all_first_edition_372_source_positions_audited": False,
    "independent_primary_source_two_reader_review": False,
    "source_mechanics_natal_astro_timing_validated": False,
    "rows": rows,
}
target = B / "ANNUAL_RATE_PHOTO_OVERLAY_V3.json"
target.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(
    json.dumps(
        {
            "new_photo_legible": 59,
            "new_uncertain": 2,
            "old_reused": 1,
            "new_discrepancies": new_diffs,
            "cumulative_original_photo_legible": 205,
            "cumulative_glyphs_unresolved": 4,
            "cumulative_not_directly_read": 163,
            "sha256": sha(target),
            "Western_still": 12472,
            "Chinese_still": 142,
        },
        indent=2,
    )
)
