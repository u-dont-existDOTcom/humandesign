#!/usr/bin/env python3
"""Original 1647 CLXVII last physical p725 and repeated-proof 1659 p725/p726.

Each original printed source observation is scoped to one photographed
reading. Do not assert historical chart accuracy or event occurrence.
"""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
W = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
C = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
ORIG_PDF = "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
PHOTOS = {
    "1647_p725": (
        "1647_original-759.jpg",
        "c3f616bd2eaaf142053961f01c735045327af79734b2cd631cd38a0c7bada91a",
        725,
        759,
    ),
    "1647_p726": (
        "1647_original-760.jpg",
        "6f8edbf6145112d2402c99e3a656e28364ec7a165345a113f6310d154a085994",
        726,
        760,
    ),
    "1659_p725": (
        "1659_original_djvu_754.jpg",
        "69333eefb445bbe69a70e62a5dd10278ebb2c16e4b88e4af49091804cfaa576d",
        725,
        754,
    ),
    "1659_p726": (
        "1659_original_djvu_755.jpg",
        "1732f78ff6d8ea84de89bd3a7309b82550d4795113ba9e234b524f8146e03d6c",
        726,
        755,
    ),
}
# The first three source columns are *historical tables*, not actual predictions.
# Original source transcript is a single-reader photograph-based locator.
CASES = [
    (
        "Mid-heaven original starting point",
        "Mid-heaven to Promittors, 14.39 Scorpio",
        None,
        None,
        759,
    ),
    ("Mid-heaven to Venus terms", "To Termes of ♀", 77, "4 December", 759),
    ("Mid-heaven to Mars antiscion", "Contrantiscion ♂", 176, "13 March", 759),
    ("Mid-heaven to eleventh house", "The eleventh house", 186, "23 March", 759),
    ("Mid-heaven to Scorpio heart", "Scorpions heart", 241, "17 May", 759),
    ("Mid-heaven to Mercury terms", "To Termes of ☿", 357, "10 September", 759),
    ("Solar original starting point", "☉ unto Promittors 6.37 Libra", None, None, 759),
    ("Solar to Bulls eye", "The Bulls eye", 33, "21 October", 759),
    ("Solar to dexter triangle of Sun", "△ ☉ dex.", 59, "16 November", 759),
    ("Solar to terms of Mars", "To Termes of ♂", 283, "28 June", 759),
    ("Moon original starting point", "☽ unto Promittors 1.44 Gemini", None, None, 759),
    ("Moon to Mercury dexter trine", "△ ☿ dex.", 22, "10 October", 759),
    ("Moon to Bulls eye", "The Bulls eye", 33, "21 October", 759),
    ("Moon to dexter trine of Venus", "△ ♀ dex.", 63, "20 November", 759),
    ("Moon to terms of Mars", "To Termes of ♂", 344, "28 August", 759),
    (
        "CLXVII closes after original multi-significator table",
        "Bottom of original p725 tabular section",
        None,
        None,
        759,
    ),
    ("New independently printed CHAP CLXVIII", "CHAP. CLXVIII.", None, None, 760),
    ("New judgment chapter heading", "How to judge upon a Figure of Profections.", None, None, 760),
    (
        "Next chapter relates current sign to radical house",
        "Sign ascending in the Profection, what place it had in the Radix",
        None,
        None,
        760,
    ),
    (
        "Next chapter distinguishes angles succedents cadents",
        "four Angles, or Succedants, or Cadents",
        None,
        None,
        760,
    ),
    (
        "Next chapter distinguishes present from natal factors",
        "in Nativity as in this Progressionall Revolution",
        None,
        None,
        760,
    ),
    ("Next chapter gives a five-factor list", "five things", None, None, 760),
]
assert len(CASES) == 22


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(file, x):
    file.write_text(json.dumps(x, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def create():
    west = read(W)
    china = read(C)
    assert west["records_count"] == 12649 and west["batches"][-1]["id"] == "B07an"
    assert west["next"]["pdf_page"] == 759 and west["next"]["chapter"] == "CLXVII"
    assert china["sum_source_annotations"] == 355
    images = {}
    for name, (file, expected, folio, frame) in PHOTOS.items():
        path = B / "evidence" / file
        assert path.is_file()
        digest = sha(path)
        if expected is not None:
            assert digest == expected, (name, digest)
        assert path.stat().st_size > 200000
        images[name] = {
            "path": "evidence/" + file,
            "original_printed_folio": folio,
            "original_page_image_index": frame,
            "sha256": digest,
            "byte_length": path.stat().st_size,
            "source_is_original_printed": True,
        }
    records = []
    for i, (role, locator, day, date, pdf) in enumerate(CASES):
        rid = 12650 + i
        r = {
            "id": f"R{rid}",
            "record_number": rid,
            "batch": "B07ao",
            "source_span": "B07ao-S001" if pdf == 759 else "B07ao-S002",
            "original_pdf_frames": [pdf],
            "original_printed_folio": pdf - 34,
            "role": role.replace(" ", "_").replace("-", "_").lower(),
            "source_photo_locator_not_critical_diplomatic_quote": locator,
            "original_source_tabular_annual_arc_day": day,
            "original_source_tabular_calendar_date_as_printed": date,
            "source_one_reader_attested": True,
            "independent_fully_critical_edition_verified": False,
            "original_1647_ephemeris_or_calendar_parity_validated": False,
            "original_historical_human_event_outcome_observed": False,
            "runtime_astrology_promoted": False,
        }
        records.append(r)
    assert [x["id"] for x in records] == [f"R{i}" for i in range(12650, 12672)]
    source = {
        "schema": "LILLY_1647_1659_CLXVII_LAST_P725_CLXVIII_NEXT_P726_SOURCE_V1",
        "batch": "B07ao",
        "source_full_first_1647_Wellcome_PDF_SHA256": ORIG_PDF,
        "original_printed_1647_pages": [725, 726],
        "separately_typeset_original_1659_pages": [725, 726],
        "source_photo_images": images,
        "original_CLXVII_last_p725_tabular_sections": ["Mid-heaven", "Sun", "Moon"],
        "original_source_p725_full_row_by_row_critical_comparison_complete": False,
        "original_printed_CLXVIII_begins_pdf760": True,
        "original_source_CLXVII_physical_span_fully_covered_as_pages": True,
        "original_CLXVII_source_critical_diplomatic_validation_complete": False,
        "historical_claims_source_count": len(records),
        "source_first_record": "R12650",
        "source_last_record": "R12671",
        "source_next_record": "R12672",
        "source_next_original_PDF": 760,
        "source_next_printed_chapter": "CLXVIII",
        "human_outcomes_prospectively_tested": 0,
        "verified_life_event_predictions": 0,
        "runtime_promotions": 0,
        "record_rows": records,
    }
    file = B / "ORIGINAL_CLXVII_END_CLXVIII_SOURCE_V1.json"
    save(file, source)
    rule = {
        "batch": "B07ao",
        "status": "ORIGINAL_CLXVII_PHYSICAL_SPAN_CLOSED_SOURCE_NOT_ALL_NUMERIC_CELLS_COLLATED",
        "record_count": 22,
        "first_record": "R12650",
        "last_record": "R12671",
        "source_groups": 2,
        "body_pdf_frames": [759, 760],
        "physical_original_CLXVII_source_complete": True,
        "critical_historical_all_cells_and_edition_variants_verified": False,
        "original_calendar_astro_engine_verified": False,
        "human_predictions_validated": 0,
        "runtime_promotions": 0,
        "rules": records,
    }
    save(B / "RULES.json", rule)
    a = {
        "batch": "B07ao",
        "Lilly_before": 12649,
        "Ptolemy_retained": 1066,
        "Chinese_V7_retained": 355,
        "historical_records_added": 22,
        "Lilly_if_accepted": 12671,
        "Western_if_accepted": 13737,
        "next_R": "R12672",
        "next_pdf_page": 760,
        "next_printed_page": 726,
        "next_original_chapter": "CLXVIII",
        "previous_chapter": "CLXVII",
        "original_first_CLXVII_physical_source_span_covered": True,
        "critical_original_first_CLXVII_numerical_comparison_complete": False,
        "third_1640_example_discrepancy_is_separately_in_B07an": True,
        "records_sha256": sha(file),
        "rules_sha256": sha(B / "RULES.json"),
        "human_predictive_validations": 0,
        "runtime_promotions": 0,
    }
    save(B / "ACCEPTANCE.json", a)
    print(
        json.dumps(
            {
                "records": len(records),
                "photographed_original_pages": 4,
                "source_physical_last_1647_p": 725,
                "next_CHAP": "CLXVIII",
                "next": "R12672",
                "rules_sha256": sha(B / "RULES.json"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    create()
