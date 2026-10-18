#!/usr/bin/env python3
"""Append-only photographic correction overlay for provisional annual-rate table.

Historical 1647 literal images remain authority. This does not rewrite the
previous B07x derivative candidates or imply complete source collation.
"""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
PARENT = B.parent / "B07x"
ROOT = B.parents[3]
WESTERN = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V3.json"


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


review = j(B / "PHOTO_ADJUDICATION_1647_V1.json")
parent = j(PARENT / "ANNUAL_DIRECTION_MEASURE_372_CANDIDATES_V1.json")
photo = j(PARENT / "ORIGINAL_SOURCE_WINDOW_V1.json")
idx = j(WESTERN)
chinese = j(CHINESE)
assert idx["records_count"] == 12472
assert idx["batches"][-1]["id"] == "B07w"
assert chinese["sum_source_annotations"] == 142
assert photo["accepted_lilly_before"] == 12472
assert parent["source_cells_expected"] == 372
assert parent["direct_original_photo_confirmed"] == 12
assert review["total_manual_review_positions"] == 24
assert review["unambiguous_original_photo_readings"] == 22
assert review["unresolved_original_photo_readings"] == 2
assert (
    sha(B / review["original_source"]["archived_3500_image"])
    == (review["original_source"]["source_3500_sha256"])
)
assert (
    sha(B / review["comparator_source"]["photo_file"])
    == (review["comparator_source"]["photo_sha256"])
)
assert photo["full_source_pdf_sha256"] == review["original_source"]["original_894_frame_pdf_sha256"]
assert not review["full_1647_372_cells_verified"]

historical = {(r["sign"], r["zodiac_degree"]): r for r in parent["tentative_candidate_pairs"]}
assert len(historical) == 372
audits = {}
for r in review["photo_readings"]:
    key = (r["sign"], r["degree"])
    assert key not in audits and key in historical, key
    c = historical[key]
    candidate = [
        c["candidate_original_annual_equator_rate_minutes"],
        c["candidate_original_annual_equator_rate_seconds"],
    ]
    assert candidate == r["inherited_derivative_pair"], (
        key,
        candidate,
        r["inherited_derivative_pair"],
    )
    if r["original_1647_photo_pair"] is not None:
        assert len(r["original_1647_photo_pair"]) == 2
        assert r["comparison_to_derivative"] != "GLYPH_UNRESOLVED_WITH_DERIVATIVE_CONFLICT"
    else:
        assert r["original_1647_glyph_alternatives"]
        assert r["comparison_to_derivative"] == "GLYPH_UNRESOLVED_WITH_DERIVATIVE_CONFLICT"
    assert r["source_page"] == "PDF745/printed711"
    assert not r["runtime_rule_promoted"] and not r["historical_performance_prediction_validated"]
    audits[key] = r
assert len(audits) == 24

out_rows = []
for c in parent["tentative_candidate_pairs"]:
    key = (c["sign"], c["zodiac_degree"])
    new = audits.get(key)
    assert c["source_flags"] is not None
    candidate = [
        c["candidate_original_annual_equator_rate_minutes"],
        c["candidate_original_annual_equator_rate_seconds"],
    ]
    row = {
        "sign": key[0],
        "degree": key[1],
        "B07x_derivative_candidate_as_originally_retained": candidate,
        "B07x_claimed_original_photo_match": bool(c["verified_direct_first_edition_photo"]),
        "B07x_original_source_flags": c["source_flags"],
        "B07y_manual_1647_source_photo_read": (
            new["original_1647_photo_pair"] if new is not None else None
        ),
        "B07y_manual_original_glyph_alternatives": (
            new["original_1647_glyph_alternatives"] if new is not None else None
        ),
        "B07y_review_status": (
            new["comparison_to_derivative"]
            if new is not None
            else "NO_NEW_DIRECT_PHOTO_ADJUDICATION"
        ),
        "B07y_source_verified_by_one_reader": bool(
            new and new["original_1647_photo_pair"] is not None
        ),
        "source_value_may_be_used_as_mathematical_truth": False,
        "source_value_may_be_used_in_person_forecasts": False,
        "source_fidelity_independently_expert_verified": False,
        "source_year_and_astrological_calendar_verified": False,
        "runtime_model_promoted": False,
    }
    # A prior claimed 1647 photo pass is not an independent new verification.
    # The direct B07y photo reading takes precedence without mutating B07x.
    out_rows.append(row)

assert len(out_rows) == 372
assert sum(r["B07y_source_verified_by_one_reader"] for r in out_rows) == 22
assert len([r for r in out_rows if r["B07y_manual_original_glyph_alternatives"]]) == 2
diff = [
    r
    for r in out_rows
    if r["B07y_manual_1647_source_photo_read"] is not None
    and r["B07x_derivative_candidate_as_originally_retained"]
    != r["B07y_manual_1647_source_photo_read"]
]
assert len(diff) == 5
assert {(r["sign"], r["degree"]) for r in diff} == {
    ("Leo", 0),
    ("Capricorn", 13),
    ("Aquarius", 0),
    ("Aquarius", 3),
    ("Pisces", 6),
}
assert [r for r in diff if r["B07x_claimed_original_photo_match"]] == [
    next(r for r in diff if (r["sign"], r["degree"]) == ("Aquarius", 0))
]
data = {
    "schema": "B07y_1647_ANNUAL_RATE_PROVISIONAL_PHOTO_OVERLAY_V1",
    "source_photo_original_1647_sha256": review["original_source"]["source_3500_sha256"],
    "source_photo_original_full_pdf_sha256": review["original_source"][
        "original_894_frame_pdf_sha256"
    ],
    "separate_later_1659_typeset_witness_sha256": review["comparator_source"]["photo_sha256"],
    "inherited_previous_derivative_candidate_sha256": sha(
        PARENT / "ANNUAL_DIRECTION_MEASURE_372_CANDIDATES_V1.json"
    ),
    "original_source_legacy_B07x_untouched": True,
    "total_annual_sign_degree_positions": 372,
    "B07y_current_manually_reviewed_positions": 24,
    "B07y_confirmed_1647_one_reader_positions": 22,
    "B07y_ambiguous_glyph_positions": 2,
    "B07y_conflicts_with_derivative_candidates": 5,
    "B07y_positions_not_directly_read_in_this_batch": 348,
    "separate_western_Lilly_accepted_before_and_after": 12472,
    "separate_chinese_V3_source_notes_retained": 142,
    "reviewer_count_direct_1647": 1,
    "all_372_source_cells_photo_verified": False,
    "actual_human_predictions_validated": 0,
    "runtime_promotions": 0,
    "rows": out_rows,
}
dest = B / "ANNUAL_RATE_372_PHOTO_ADJUDICATION_OVERLAY_V1.json"
dest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(
    json.dumps(
        {
            "total_rows": len(out_rows),
            "current_batch_first_edition_photo_reads": 22,
            "ambiguous_original_glyphs": 2,
            "original_vs_derivative_value_conflicts": len(diff),
            "no_new_photo_reading": 348,
            "shas": {
                "photo_original_1647": data["source_photo_original_1647_sha256"],
                "photo_comparator_1659": data["separate_later_1659_typeset_witness_sha256"],
                "overlay": sha(dest),
            },
            "accepted_registry_records_unchanged": idx["records_count"],
        },
        indent=2,
    )
)
