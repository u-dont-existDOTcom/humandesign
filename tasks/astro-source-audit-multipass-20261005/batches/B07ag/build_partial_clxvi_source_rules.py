#!/usr/bin/env python3
"""Prepare 29 historical Lilly opening claims for PARTIAL printed CLXVI admission.

Never label the quantitative printed chapter complete: original year/degree
tables, 7 unresolved old glyphs and historical predictive tests remain open.
"""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
ORIGINAL = B.parent / "B07x"
COMPARE = B.parent / "B07ae"
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


data = j(B / "CLXVI_OPENING_SOURCE_PHOTO_29_NOTES_V1.json")
witness = j(B / "FIRST_SECOND_ORIGINAL_708_710_SOURCE_WITNESS_V1.json")
index = j(WEST)
china = j(CHINA)
assert index["records_count"] == 12472
assert index["batches"][-1]["id"] == "B07w"
assert index["next"]["chapter"] == "CLXVI"
assert index["next"]["pdf_page"] == 742
assert china["sum_source_annotations"] == 262
assert data["historical_source_claim_count"] == 29
assert len(witness["photographic_source_note_receipts"]) == 29
assert witness["original_printing_1647_next_day_sun_longitude"] == [7, 36]
assert witness["second_printing_1659_next_day_sun_longitude"] == [7, 36]
assert witness["modern_derivative_transcription_next_day_sun_longitude"] == [7, 37]
assert not data["original_chapter_clxvi_fully_critically_documented"]

expected = list(range(12473, 12502))
group = {742: "B07ag-S001", 743: "B07ag-S002", 744: "B07ag-S003"}
rules = []
for i, n in enumerate(data["records"]):
    assert n["id"] == f"B07ag-P{i + 1:03d}"
    assert (
        n["derivative_anchor_UTF8_sha256"]
        == hashlib.sha256(n["derivative_search_text_anchor"].encode("utf-8")).hexdigest()
    )
    assert n["original_1647_pdf_frame"] in group
    number = 12473 + i
    assert number == expected[i]
    record = {
        "id": f"R{number}",
        "record_number": number,
        "batch": "B07ag",
        "candidate_source_note_id": n["id"],
        "source_span": group[n["original_1647_pdf_frame"]],
        "original_pdf_frames": [n["original_1647_pdf_frame"]],
        "role": n["role"],
        "source_anchor_not_diplomatic": n["derivative_search_text_anchor"],
        "historical_meaning_only": n["historical_source_reading"],
        "qualification": (
            "FIRST_AND_SECOND_ORIGINAL_EDITION_OVERRIDE_MODERN_DERIVATIVE"
            if n["role"] == "sun_next_longitude_discrepancy"
            else "partial 1647 original source; modern derivative only for search; "
            "all prediction outcomes and true epoch astronomy unvalidated"
        ),
        "original_printed_next_day_sun_longitude_degrees_minutes": [7, 36]
        if n["role"] == "sun_next_longitude_discrepancy"
        else None,
        "modern_derivative_mistranscribed_next_day_sun_longitude": [7, 37]
        if n["role"] == "sun_next_longitude_discrepancy"
        else None,
        "historical_source_documented": True,
        "independent_real_event_timing_accuracy_validated": False,
        "independent_health_or_death_prediction_validated": False,
        "independent_relationship_or_financial_prediction_validated": False,
        "independent_faith_personality_or_crime_label_validated": False,
        "original_directions_angle_date_conversion_verified": False,
        "original_1647_fixed_star_modern_epoch_parity_verified": False,
        "real_person_health_safety_social_status_advice_authorized": False,
        "runtime_model_promoted": False,
    }
    rules.append(record)
assert len(rules) == 29
assert all(r["historical_source_documented"] for r in rules)
assert all(not r["runtime_model_promoted"] for r in rules)
result = {
    "batch": "B07ag",
    "status": "ORIGINAL_1647_CLXVI_OPENING_PARTIAL_SOURCE_ONLY",
    "printed_chapter": "CLXVI_Of_the_measure_of_time_in_DIRECTIONS_FIRST_PART",
    "record_count": len(rules),
    "first_record": "R12473",
    "last_record": "R12501",
    "source_groups": 3,
    "body_pdf_frames": [742, 743, 744],
    "following_original_printed_table_starts_pdf": 745,
    "original_full_chapter_CLXVI_completed": False,
    "all_372_1647_original_annual_rate_glyphs_independently_verified": False,
    "no_read_numbered_chapter_165_added_yet": True,
    "modern_original_1647_and_1659_source_correction": [7, 36],
    "searchable_derivative_wrong_transcription": [7, 37],
    "historical_arc_to_age_engine_verified": False,
    "empirical_real_person_predictions_validated": 0,
    "runtime_promotions": 0,
    "rules": rules,
}
rfile = B / "RULES.json"
rfile.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
accept = {
    "batch": "B07ag",
    "scope": (
        "First 1647 printed pages708–710 of numbered CLXVI "
        "time directions, source-only, not full chapter"
    ),
    "prior_Lilly": 12472,
    "prior_Ptolemy": 1066,
    "parallel_Chinese_V5": 262,
    "partial_historical_annotations_added": 29,
    "lilly_after": 12501,
    "western_after": 13567,
    "next_original_source_id": "R12502",
    "next_original_source_pdf_frame": 745,
    "next_original_printed_folio": 711,
    "next_heading_printed_numeral": "CLXVI",
    "next_source_unit": (
        "Annual-measure 12 signs×31 rates first edition printed711, exact glyph uncertainty"
    ),
    "source_groups": 3,
    "source_photos": 4,
    "original_printed_sun_longitude_7_36": True,
    "diplomatic_1647_CLXVI_full_chapter_complete": False,
    "original_1647_annual_rate_glyphs_all_expert_verified": False,
    "rules_sha256": sha(rfile),
    "source_witness_sha256": sha(B / "FIRST_SECOND_ORIGINAL_708_710_SOURCE_WITNESS_V1.json"),
    "real_human_predictions_validated": 0,
    "runtime_promotions": 0,
}
(B / "ACCEPTANCE.json").write_text(
    json.dumps(accept, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(
    json.dumps(
        {
            "partial_source_records": len(rules),
            "first": result["first_record"],
            "last": result["last_record"],
            "next": accept["next_original_source_id"],
            "rules_sha256": sha(rfile),
            "source_1647_and_1659_both": [7, 36],
            "predecessor_canonical_index_unchanged": index["records_count"],
        },
        indent=2,
    )
)
