#!/usr/bin/env python3
# ruff: noqa: E501  # Historical source meanings and navigational anchors.
"""Lilly 1647 vs actual 1659 printed CLXX Midheaven/Sun house categories.

SOURCE ONLY. Astronomical natal calendar or human predictive results are
not tested. Original pages are authoritative, secondary transcription used
only for searchable phrase location.
"""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
BASE = B.parent
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
NAV = B / "SECONDARY_CLXX_SOURCE_NAVIGATOR.txt"
BOOK_SHA = "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"

IMAGES = {
    "1647_folio731": BASE / "B07aq/evidence/original_1647-765.jpg",
    "1647_folio732": BASE / "B07aq/evidence/original_1647-766.jpg",
    "1659_folio731": BASE / "B07aq/evidence/original_1659_djvu_760.jpg",
    "1659_folio732": B / "evidence/original_1659_djvu_761.jpg",
}
HOUSES = [
    (
        1,
        765,
        "When either the Signe culminating in the Radix",
        "Profectional ascension of either natal Midheaven sign or solar sign linked in old text with public profession and rank.",
    ),
    (2, 765, "When to the 2nd house", "Historical proceeds or material reward from previous work."),
    (
        3,
        765,
        "When to the 3rd house",
        "Historical ambivalent year, kin/neighbors/travel risks related to sixth-from-tenth geometry.",
    ),
    (
        4,
        765,
        "When to the 4th house",
        "Historical reputation trouble, familial disagreement and antagonistic neighbors.",
    ),
    (
        5,
        765,
        "When to the 5th",
        "Historical child-related joy if children present; otherwise pleasures and expense.",
    ),
    (
        6,
        765,
        "When to the 6th hosue",
        "Historical household/husbandry activities but alleged lack of honor-related success.",
    ),
    (
        7,
        765,
        "When to the 7th",
        "Historical reputation gain if capable and alleged ancestry/family-loss warnings.",
    ),
    (8, 765, "When to the 8th", "Historical slander, fear and melancholy attributed to enemies."),
    (
        9,
        766,
        "When to the 9th",
        "Historical honorable long journeys and contact with foreigners or distant people.",
    ),
    (10, 766, "When to the 10th", "Historical successful/famous year and high credit."),
    (
        11,
        766,
        "When to the 11th",
        "Historical mutually supportive friendships, joy and growing network.",
    ),
    (
        12,
        766,
        "When to the 12th",
        "Historical damage to reputation/elite patrons, envy and possible loss of kin.",
    ),
]
EXTRA = [
    (
        765,
        "midheaven_sun_joint_trigger",
        "When either the Signe culminating in the Radix, or wherein then the Sun was",
        "The rule explicitly covers both natal Midheaven sign and Sun sign, not one isolated Sun-sign claim.",
    ),
    (
        765,
        "third_house_geometry_6_from10",
        "6th house from the 10th",
        "Text bases its third-house qualification on derivative house-six from the tenth.",
    ),
    (
        765,
        "fifth_conditional_children",
        "he that hath none",
        "The historical fifth-house rule splits effects based on children present or absent.",
    ),
    (
        765,
        "seventh_capability_conditional",
        "then if the Native be capable",
        "The historical seventh-house rank claim is explicitly qualified by capability.",
    ),
    (
        766,
        "next_CLXXI_physical_boundary",
        "C H A P. C L X X I.",
        "A horizontal divider precedes new chapter CLXXI on Part of Fortune and second-house profections.",
    ),
]
assert len(HOUSES) + len(EXTRA) == 17


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def save(p, v):
    Path(p).write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def freeze():
    west = j(INDEX)
    china = j(CHINA)
    assert west["records_count"] == 12725 and west["batches"][-1]["id"] == "B07aq"
    assert west["next"]["chapter"] == "CLXX" and west["next"]["pdf_page"] == 765
    assert china["sum_source_annotations"] == 355
    modern = NAV.read_text(encoding="utf-8")
    assert sha(NAV) == "858d02ad703c5d21bb8c5b847f16832e79fd5348ca0fcea81673a721c49bf3bd"
    assert "When to the 11th" in modern and "When to the 12th" in modern
    assert "C H A P. C L X X I." in modern
    photos = {}
    for name, p in IMAGES.items():
        assert p.is_file() and p.stat().st_size > 250000
        photos[name] = {
            "source_relative_path": str(p.relative_to(ROOT)),
            "file_bytes": p.stat().st_size,
            "file_sha256": sha(p),
            "printing_year": int(name[:4]),
            "original_printed_folio": int(name[-3:]),
        }
    assert len(photos) == 4
    observations = []
    for house, frame, anchor, gloss in HOUSES:
        observations.append((frame, f"sun_mid_haven_house_{house:02d}", house, anchor, gloss))
    for frame, role, anchor, gloss in EXTRA:
        observations.append((frame, role, None, anchor, gloss))
    rows = []
    for i, (frame, role, house, anchor, gloss) in enumerate(observations):
        assert anchor in modern, (role, anchor)
        fo = frame - 34
        old = photos[f"1647_folio{fo}"]
        later = photos[f"1659_folio{fo}"]
        rows.append(
            {
                "id": f"R{12726 + i}",
                "record_number": 12726 + i,
                "batch": "B07ar",
                "source_group": "B07ar-S001" if frame == 765 else "B07ar-S002",
                "original_first_1647_pdf_frame": frame,
                "original_printed_folio": fo,
                "role": role,
                "profection_house": house,
                "historical_source_description_not_personal_fact": gloss,
                "modern_secondary_anchor_nondiplomatic": anchor,
                "secondary_anchor_char_offset": modern.index(anchor),
                "original_first_edition_photo_sha256": old["file_sha256"],
                "original_second_edition_photo_sha256": later["file_sha256"],
                "primary_source_read_by_one_reader": True,
                "source_independent_critical_edition_review_complete": False,
                "actual_natal_chart_calendar_engine_verified": False,
                "individual_health_character_finance_prediction_validated": False,
                "runtime_promoted": False,
            }
        )
    assert len(rows) == 17
    assert [x["record_number"] for x in rows] == list(range(12726, 12743))
    data = {
        "schema": "LILLY_ORIGINAL_1647_1659_CLXX_MIDHEAVEN_SUN_TWELVE_HOUSE_SOURCE_V1",
        "batch": "B07ar",
        "original_book_full_1647_pdf_sha256": BOOK_SHA,
        "original_CLXX_chapter_primary_physical_frames": [765, 766],
        "next_CLXXI_chapter_starts_on_pdf_frame": 766,
        "all_four_original_first_second_printed_photo_sha256s": photos,
        "modern_secondary_text_excerpt_sha256": sha(NAV),
        "twelve_historical_house_positions_source_read": True,
        "source_reliance_on_independently_typeset_original_printings": True,
        "source_original_1647_full_critical_diplomatic_second_reader_complete": False,
        "personal_astrological_predictive_accuracy_verified": False,
        "full_1647_epoch_calendar_engine_verified": False,
        "source_record_count": 17,
        "source_first": "R12726",
        "source_last": "R12742",
        "source_next": "R12743",
        "source_next_original_pdf": 766,
        "historical_Lilly_before": 12725,
        "historical_Lilly_after_if_accepted": 12742,
        "parallel_Chinese_V7": 355,
        "actual_human_forecasts_validated": 0,
        "runtime_promotions": 0,
        "records": rows,
    }
    path = B / "ORIGINAL_CLXX_MIDHEAVEN_SUN_17_SOURCE_NOTES_V1.json"
    save(path, data)
    rules = {
        "batch": "B07ar",
        "status": "ORIGINAL_1647_1659_CLXX_MIDHEAVEN_SUN_HOUSE_SOURCE",
        "record_count": 17,
        "first_record": "R12726",
        "last_record": "R12742",
        "source_groups": 2,
        "body_pdf_frames": [765, 766],
        "original_printed_CLXX_source_physically_covered": True,
        "original_CLXX_full_expert_critical_edition_verified": False,
        "independent_real_human_outcome_validations": 0,
        "runtime_promotions": 0,
        "rules": [
            {
                "id": r["id"],
                "record_number": r["record_number"],
                "batch": "B07ar",
                "source_span": r["source_group"],
                "original_pdf_frames": [r["original_first_1647_pdf_frame"]],
                "role": r["role"],
                "historical_meaning_only": r["historical_source_description_not_personal_fact"],
                "source_anchor_not_diplomatic": r["modern_secondary_anchor_nondiplomatic"],
                "first_1647_photo_sha256": r["original_first_edition_photo_sha256"],
                "second_1659_photo_sha256": r["original_second_edition_photo_sha256"],
                "historical_source_documented": True,
                "original_natal_model_verified": False,
                "independent_actual_human_forecast_validated": False,
                "runtime_model_promoted": False,
            }
            for r in rows
        ],
    }
    save(B / "RULES.json", rules)
    accept = {
        "batch": "B07ar",
        "Lilly_before": 12725,
        "Ptolemy_retained": 1066,
        "Chinese_V7_retained": 355,
        "new_historical_source_notes": 17,
        "Lilly_after_if_accepted": 12742,
        "Western_after_if_accepted": 13808,
        "next_historical_R": "R12743",
        "next_original_PDF": 766,
        "next_printed_chapter": "CLXXI",
        "next_printed_folio": 732,
        "next_source_scope": "Part of Fortune and second-house sign profections, below already recorded divider",
        "source_original_CLXX_physical_span_covered": True,
        "full_original_source_critical_edition_verified": False,
        "birth_calendar_and_real_person_predictions_verified": False,
        "source_notes_SHA256": sha(path),
        "rules_SHA256": sha(B / "RULES.json"),
        "human_prediction_validations": 0,
        "runtime_promotions": 0,
    }
    save(B / "ACCEPTANCE.json", accept)
    print(
        json.dumps(
            {
                "original_house_positions": 12,
                "historical_source_annotations": 17,
                "original_printing_images": len(photos),
                "next_R": accept["next_historical_R"],
                "first_edition_next_chapter_original_page": 766,
                "notes_sha256": sha(path),
                "rules_sha256": sha(B / "RULES.json"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    freeze()
