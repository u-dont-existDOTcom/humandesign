#!/usr/bin/env python3
"""Independent 1659 printing vs seven unresolved 1647 glyphs, no substitutions."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
SOURCE = B.parent / "B07ad/ANNUAL_RATE_PHOTO_OVERLAY_V6.json"
FIRST = B / "evidence/original_1647_annual_table_pdf745_3500.jpg"
SECOND = B / "evidence/second_edition_1659_annual_table_page740.jpg"
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V3.json"


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


old = j(SOURCE)
assert old["cumulative_one_reader_legible_original_1647"] == 365
assert old["cumulative_original_print_unresolved_positions"] == 7
assert old["cumulative_positions_without_any_original_photo_attempt"] == 0
assert sha(FIRST) == old["historical_original_pdf745_photo_sha256"]
assert sha(SECOND) == "4e7d5c7601f64109e134f77b47dce237d9832370afbadaccda9691740f4f39ac"
assert j(WEST)["records_count"] == 12472
assert j(CHINA)["sum_source_annotations"] == 142

TENTATIVE = {
    ("Virgo", 1): ([55, 10], "VISIBLE_BUT_NOT_BLINDLY_CONFIRMED"),
    ("Capricorn", 9): ([66, 32], "VISIBLE_BUT_NOT_BLINDLY_CONFIRMED"),
}
EXPECTED = {
    ("Virgo", 1): [[55, 10], [55, 13]],
    ("Virgo", 18): [[53, 58], [53, 59]],
    ("Capricorn", 9): [[66, 32], [66, 39]],
    ("Capricorn", 15): [[65, 57], [66, 2]],
    ("Aquarius", 5): [[62, 33], [62, 35]],
    ("Aquarius", 6): [[62, 22], [62, 24]],
    ("Pisces", 24): [[53, 43], [54, 43]],
}
rows = {(r["sign"], r["degree"]): r for r in old["rows"]}
actual = {k: rows[k] for k in EXPECTED}
assert all(r["first_edition_1647_one_reader_photo_rate"] is None for r in actual.values())
assert all(
    r["unresolved_original_source_glyph_options"] == EXPECTED[key] for key, r in actual.items()
)
entries = []
for (sign, degree), original in EXPECTED.items():
    candidate, quality = TENTATIVE.get(
        (sign, degree), (None, "LOW_RESOLUTION_SECOND_EDITION_NOT_DECISIVE")
    )
    if candidate is not None:
        assert candidate in original
    crop = f"1659_cell_{sign}_{degree:02d}.png"
    assert (B / "evidence" / crop).is_file()
    entries.append(
        {
            "sign": sign,
            "degree": degree,
            "original_pdf_frame": 745,
            "original_printed_folio": 711,
            "source_original_first_edition_reading": None,
            "original_first_edition_photo_glyph_candidates": original,
            "later_1659_independent_typesetting_tentative_reading": candidate,
            "later_1659_printed_photo_page": 711,
            "later_1659_djvu_frame": 740,
            "later_photo_crop": crop,
            "later_photo_crop_sha256": sha(B / "evidence" / crop),
            "later_1659_printing_reading_confidence": quality,
            "cross_edition_source_status": (
                "TENTATIVE_SUPPORT_FOR_ONE_1647_GLYPH_CANDIDATE"
                if candidate is not None
                else "LATER_PRINT_LOW_RESOLUTION_NOT_DECISIVE"
            ),
            "original_1647_glyph_status_after_second_edition": "UNRESOLVED",
            "original_1647_value_silently_replaced": False,
            "authoritative_birth_chart_calculation_allowed": False,
            "independent_human_event_accuracy_validated": False,
            "runtime_promoted": False,
        }
    )
assert len(entries) == 7
assert (
    sum(x["later_1659_independent_typesetting_tentative_reading"] is not None for x in entries) == 2
)
obj = {
    "schema": "LILLY_1647_1659_SEVEN_UNKNOWN_YEAR_RATE_GLYPHS_CROSS_EDITION_V1",
    "batch": "B07af",
    "first_edition_source": (
        "Lilly Christian Astrology original Wellcome 1647 b30338724 PDF745 printed711"
    ),
    "source_first_edition_full_pdf_sha256": (
        "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
    ),
    "source_first_edition_photo_sha256": sha(FIRST),
    "source_second_edition": (
        "Lilly Christian Astrology original second printed edition 1659, "
        "Wikimedia Commons DjVu printed711 frame740"
    ),
    "source_second_edition_original_image_sha256": sha(SECOND),
    "source_previous_B07ad_photo_status_SHA256": sha(SOURCE),
    "source_first_edition_unresolved_before": 7,
    "source_first_edition_unresolved_after": 7,
    "source_second_edition_tentative_glyph_matches": 2,
    "source_second_edition_indeterminate_positions": 5,
    "source_full_paper_original_372_positions_visually_attempted": True,
    "source_first_edition_original_365_legible_7_unresolved_unchanged": True,
    "do_not_promote_substitutions_from_1659_to_1647": True,
    "independent_human_historian_or_second_reader_verified": False,
    "later_second_print_is_not_a_blinded_source_reader": True,
    "real_human_astrological_prediction_validated": 0,
    "model_runtime_promotions": 0,
    "historical_western_Lilly_canonical_unchanged": 12472,
    "historical_chinese_V3_canonical_unchanged": 142,
    "entries": entries,
}
target = B / "SEVEN_UNRESOLVED_FIRST_EDITION_GLYPHS_1659_COMPARISON_V1.json"
target.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(
    json.dumps(
        {
            "first_edition_original_missing_still": 7,
            "second_edition_tentative": 2,
            "second_edition_indeterminate": 5,
            "source_comparison_sha256": sha(target),
            "indices_unchanged": True,
        },
        indent=2,
    )
)
