#!/usr/bin/env python3
"""Confirm original 1647 & 1659 Maginus longitude and 29 partial CLXVI notes.

Source authority: real original printed Wellcome 1647 and independent 1659
typeset photos; modern flattened text only assists locating source phrases.
No full original chapter acceptance or real-person chart prediction.
"""

import argparse
import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
PARENT = B.parent / "B07x"
COMPARE = B.parent / "B07ae"
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"
NOTES = B / "CLXVI_OPENING_SOURCE_PHOTO_29_NOTES_V1.json"
WITNESS = B / "FIRST_SECOND_ORIGINAL_708_710_SOURCE_WITNESS_V1.json"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def freeze(text_path):
    notes = load(NOTES)
    original = load(PARENT / "ORIGINAL_SOURCE_WINDOW_V1.json")
    second = load(COMPARE / "MAGINUS_FIRST_SECOND_EDITION_SOURCE_DISCREPANCY_V1.json")
    idx = load(INDEX)
    china = load(CHINA)
    assert idx["records_count"] == 12472 and idx["batches"][-1]["id"] == "B07w"
    assert idx["next"]["chapter"] == "CLXVI" and idx["next"]["pdf_page"] == 742
    assert china["sum_source_annotations"] == 262
    assert notes["historical_source_claim_count"] == len(notes["records"]) == 29
    assert notes["new_canonical_source_R_records_accepted"] == 0
    assert original["full_source_pdf_sha256"] == notes["whole_original_pdf_sha256"]
    assert second["Wellcome_1647_full_original_pdf_sha256"] == notes["whole_original_pdf_sha256"]
    source_images = {}
    for num in range(742, 745):
        item = original["photos"][str(num)]
        file = PARENT / item["file"]
        assert sha(file) == item["sha256"], (num, file)
        source_images[str(num)] = {
            "original_printed_folio": num - 34,
            "original_pdf_frame": num,
            "file": str(file.relative_to(ROOT)),
            "sha256": sha(file),
            "bytes": file.stat().st_size,
        }
    x = second["source_photos"]["second_edition_1659_printed710_djvu739"]
    file = COMPARE / x["file"]
    assert sha(file) == x["sha256"]
    assert x["printed"] == 710 and x["djvu_page"] == 739
    modern = text_path.read_text(encoding="utf-8")
    begin = modern.index("Of the measure of time in DIRECTIONS.")
    end = modern.index("A Table of the annuall measure in Directions.", begin)
    window = modern[begin:end]
    checks = []
    for i, r in enumerate(notes["records"]):
        assert r["id"] == f"B07ag-P{i + 1:03d}"
        assert r["original_1647_pdf_frame"] in (742, 743, 744)
        assert r["original_1647_printed_folio"] == r["original_1647_pdf_frame"] - 34
        phrase = r["derivative_search_text_anchor"]
        pos = window.find(phrase)
        assert pos >= 0, (r["id"], phrase)
        assert not r["runtime_promoted"]
        r["derivative_anchor_char_offset_in_section"] = pos
        r["derivative_anchor_UTF8_sha256"] = hashlib.sha256(phrase.encode("utf-8")).hexdigest()
        checks.append(
            {
                "record_id": r["id"],
                "source_photo_pdf_frame": r["original_1647_pdf_frame"],
                "source_photo_sha256": source_images[str(r["original_1647_pdf_frame"])]["sha256"],
                "modern_derivative_anchor": phrase,
                "derivative_section_char_offset": pos,
                "derivative_phrase_utf8_sha256": r["derivative_anchor_UTF8_sha256"],
                "source_model_runtime_promoted": False,
            }
        )
    discrepancy = notes["records"][-1]
    assert discrepancy["role"] == "sun_next_longitude_discrepancy"
    assert discrepancy["numeric_1647_original_first_and_second_editions"] == [7, 36]
    assert discrepancy["numeric_modern_searchable_transcription"] == [7, 37]
    assert "[7,36]" not in discrepancy["derivative_search_text_anchor"]
    assert notes["original_chapter_clxvi_fully_critically_documented"] is False
    notes["secondary_text_original_window_sha256"] = hashlib.sha256(
        window.encode("utf-8")
    ).hexdigest()
    notes["first_and_second_1647_1659_original_printed_sun_longitudes_match"] = True
    notes["original_photo_hashes_first_1647"] = {k: v["sha256"] for k, v in source_images.items()}
    notes["second_edition_1659_photo_hash"] = x["sha256"]
    NOTES.write_text(json.dumps(notes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    out = {
        "schema": "LILLY_B07ag_CLXVI_FIRST_EDITION_1647_1659_SOURCE_WITNESS_V1",
        "batch": "B07ag",
        "full_1647_original_pdf_sha256": original["full_source_pdf_sha256"],
        "first_edition_source_photographs": source_images,
        "independent_1659_typeset_photo": {
            "printed_folio": 710,
            "djvu_page": 739,
            "file": str(file.relative_to(ROOT)),
            "sha256": sha(file),
            "bytes": file.stat().st_size,
        },
        "modern_searchable_derivative_section_sha256": notes[
            "secondary_text_original_window_sha256"
        ],
        "original_printing_1647_next_day_sun_longitude": [7, 36],
        "second_printing_1659_next_day_sun_longitude": [7, 36],
        "modern_derivative_transcription_next_day_sun_longitude": [7, 37],
        "source_edition_comparison_status": "FIRST_AND_SECOND_PHYSICAL_PRINT_CONFIRM_7_36",
        "full_CLXVI_source_table_completed": False,
        "complete_1647_astro_ephemeris_annual_direction_engine_verified": False,
        "accepted_new_canonical_Lilly_records": 0,
        "real_human_event_predictions_validated": 0,
        "runtime_promotions": 0,
        "photographic_source_note_receipts": checks,
    }
    WITNESS.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "historical_source_partial_notes": len(checks),
                "source_photos": len(source_images) + 1,
                "original_1647_both_editions_Sun_next_day": [7, 36],
                "derivative_transcription_wrong": [7, 37],
                "record_sha256": sha(NOTES),
                "witness_sha256": sha(WITNESS),
                "accepted_new_Lilly_history_records": 0,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--modern-text", type=Path, required=True)
    freeze(p.parse_args().modern_text)
