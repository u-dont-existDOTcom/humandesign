#!/usr/bin/env python3
# ruff: noqa: E501  # Historical source phrases and documentary notes.
"""Lilly original 1647 CLXXI source p732–734, corroborated by typeset 1659.

Physical primary-source history only. Preserve separate Part of Fortune and
second-house profection trigger, complete twelve houses, and partial source
septennial Alfridary sequences. Do not infer moral, health, wealth outcomes.
"""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
BASE = B.parent
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
NAV = B / "SECONDARY_CLXXI_NAVIGATOR.txt"
FULL_1647_PDF_SHA = "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
PHOTOS = {
    "1647_printed732": BASE / "B07aq/evidence/original_1647-766.jpg",
    "1647_printed733": B / "evidence/1647_original-767.jpg",
    "1647_printed734": B / "evidence/1647_original-768.jpg",
    "1659_printed732": BASE / "B07ar/evidence/original_1659_djvu_761.jpg",
    "1659_printed733": B / "evidence/original_1659_djvu_762.jpg",
    "1659_printed734": B / "evidence/original_1659_djvu_763.jpg",
}
HOUSES = [
    (
        1,
        766,
        "When either of these come to be the ascendant in an annuall Profection",
        "Claims unexpectedly obtained wealth and success, conditional on annual profection first-house sign and people represented by it.",
    ),
    (
        2,
        766,
        "When to the 2nd",
        "Source claims previously anticipated goods, purchases and sale proceeds.",
    ),
    (3, 766, "When to the 3rd", "Source claims relative/kin support and improved estate."),
    (
        4,
        766,
        "When to the 4th",
        "Source claims financial benefit from parents, property, buildings and inheritance.",
    ),
    (
        5,
        767,
        "When to the 5th",
        "Claims benefits through friends, writing, correspondence and pleasure including cards/dice.",
    ),
    (
        6,
        767,
        "When to the 6th",
        "Source claims labor of servants and smaller livestock is profitable.",
    ),
    (
        7,
        767,
        "When to the 7th",
        "Source imagines gains through wife, older women, legal cases and public opponents.",
    ),
    (
        8,
        767,
        "When to the 8th",
        "Source claims inheritance/estate through wills and wife-related parties, warning about lending.",
    ),
    (
        9,
        767,
        "When to the 9th",
        "Source claims journeys and religious contacts may bring financial gain.",
    ),
    (
        10,
        767,
        "When to the 10th",
        "Source claims office/preferment, conditioned by qualification and merit.",
    ),
    (
        11,
        767,
        "When to the 11th",
        "Source claims friends, monetary lending, recovery of debts and superior's favors.",
    ),
    (
        12,
        767,
        "When to the 12th",
        "Source makes old allegation about dishonesty and losses through large cattle; historical moral rhetoric, not an actual-person claim.",
    ),
]
OTHER = [
    (
        766,
        "dual_part_fortune_and_second_house_trigger",
        "The significations of the Profectionall Signe of PART OF FORTUNE, and Signe of the 2nd house.",
        "The author treats Part of Fortune and natal second-house sign as two distinct starting significators for the same profection table.",
    ),
    (
        766,
        "annual_first_house_profection_setup",
        "or to be the Signe of the 1st",
        "The source explicitly links selected origin sign arriving as first sign of annual profection.",
    ),
    (
        766,
        "first_house_people_qualified",
        "deal with such men as the Signe ascending represents",
        "First-house gain claim includes a qualifier concerning dealings with sign-represented people.",
    ),
    (
        767,
        "tenth_house_source_capability_qualification",
        "as qualified or capable",
        "Tenth-house honors are expressly conditioned by merit and ability.",
    ),
    (
        767,
        "other_old_author_references",
        "may read John Schoner",
        "Author names Schoner, Junctinus, Ranzovius, Hermes and Origanus as older reference authorities; not independently audited here.",
    ),
    (
        767,
        "year_lord_Chronocrator_alias",
        "Lord of the yeer and Chroneverator, or Chronocrator, are all one",
        "Original equates lord of the year with labels Chronocrator and alternative spelling; not a demonstrated astronomy relation.",
    ),
    (
        767,
        "septennial_alfridary_description",
        "Lords of the Septenniall yeers",
        "The text frames its described Alfridary lords as successive seven-year periods, not a standard complete lifelong sequence.",
    ),
    (
        767,
        "dayborn_limited_source_sequence",
        "if the Native be borne by day",
        "Source day-birth opening sequence: Sun first seven years, Venus next seven, Mercury next seven; later sequence not explicitly enumerated here.",
    ),
    (
        767,
        "nightborn_limited_source_sequence",
        "If one is born in the night",
        "Source night-birth opening sequence: Moon first seven years, Saturn next seven, Jupiter next seven, completed at top next printed page.",
    ),
    (
        768,
        "next_CLXXII_original_chapter_boundary",
        "C H A P. C L X X I I .",
        "A physical horizontal divider separates following CLXXII Of Revolutions beginning on same 1647 printed734 page; new topic is not part of CLXXI.",
    ),
]
assert len(HOUSES) == 12 and len(OTHER) == 10


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def load(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def save(file, x):
    Path(file).write_text(json.dumps(x, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def freeze():
    west = load(WEST)
    china = load(CHINA)
    assert west["records_count"] == 12742 and west["batches"][-1]["id"] == "B07ar"
    assert west["next"]["chapter"] == "CLXXI" and west["next"]["pdf_page"] == 766
    assert china["sum_source_annotations"] == 355
    derivative = NAV.read_text(encoding="utf-8")
    assert sha(NAV) == "6a72a0cabe518a07fcc2a14fd617702cacb707c3be99e11a0389cf8d4bf91c4f"
    witnesses = {}
    for k, file in PHOTOS.items():
        assert file.is_file() and file.stat().st_size > 250000, k
        witnesses[k] = {
            "relative_original_photo": str(file.relative_to(ROOT)),
            "source_image_sha256": sha(file),
            "file_bytes": file.stat().st_size,
            "edition_year": int(k[:4]),
            "printed_page": int(k[-3:]),
        }
    readings = []
    for house, frame, anchor, meaning in HOUSES:
        assert anchor in derivative, (house, anchor)
        readings.append((frame, f"part_fortune_second_house_{house:02d}", house, anchor, meaning))
    for frame, role, anchor, meaning in OTHER:
        assert anchor in derivative, (role, anchor)
        readings.append((frame, role, None, anchor, meaning))
    assert len(readings) == 22
    notes = []
    for n, (frame, role, house, anchor, meaning) in enumerate(readings):
        printed = frame - 34
        source1 = witnesses[f"1647_printed{printed}"]
        source2 = witnesses[f"1659_printed{printed}"]
        notes.append(
            {
                "id": f"R{12743 + n}",
                "record_number": 12743 + n,
                "batch": "B07as",
                "role": role,
                "historical_house": house,
                "original_1647_pdf_frame": frame,
                "original_printed_folio": printed,
                "original_1647_first_ed_photo_sha256": source1["source_image_sha256"],
                "original_1659_separately_typeset_photo_sha256": source2["source_image_sha256"],
                "derivative_navigation_anchor_not_diplomatic": anchor,
                "derivative_excerpt_codepoint_position": derivative.index(anchor),
                "source_historical_interpretation_only": meaning,
                "historical_source_verification_one_informed_reader": True,
                "original_full_edition_expert_collation": False,
                "real_person_health_morality_wealth_forecast_validated": False,
                "original_birth_hour_calendar_chart_engine_verified": False,
                "runtime_promoted": False,
            }
        )
    assert [r["record_number"] for r in notes] == list(range(12743, 12765))
    assert [r["historical_house"] for r in notes[:12]] == list(range(1, 13))
    assert notes[-1]["role"] == "next_CLXXII_original_chapter_boundary"
    source = {
        "schema": "LILLY_1647_1659_CLXXI_PART_FORTUNE_SECOND_HOUSE_ALFRIDARY_SOURCE_V1",
        "batch": "B07as",
        "source_original_book_Wellcome_1647_full_pdf_SHA256": FULL_1647_PDF_SHA,
        "source_original_1647_physical_printed_folios": [732, 733, 734],
        "source_first_and_separate_second_original_printings": witnesses,
        "source_secondary_searchable_excerpt_SHA256": sha(NAV),
        "source_twelve_house_cases_documented": True,
        "source_beginning_original_1647_PDF": 766,
        "next_new_CLXXII_heading_1647_PDF": 768,
        "historical_source_Alfridary_day_first_three_7year_lords": ["Sun", "Venus", "Mercury"],
        "historical_source_Alfridary_night_first_three_7year_lords": ["Moon", "Saturn", "Jupiter"],
        "source_full_life_cycle_sequence_in_this_chapter": False,
        "original_full_diplomatic_expert_critical_edition_verified": False,
        "source_authority_is_not_actual_human_prediction_data": True,
        "new_source_only_annotations": 22,
        "Lilly_before": 12742,
        "Lilly_after_if_accepted": 12764,
        "Ptolemy_retained": 1066,
        "Chinese_V7_retained": 355,
        "next_original_R": "R12765",
        "next_original_PDF": 768,
        "next_printed_chapter": "CLXXII",
        "independent_actual_human_forecasts_validated": 0,
        "runtime_promotions": 0,
        "records": notes,
    }
    dest = B / "ORIGINAL_CLXXI_FORTUNE_12_HOUSES_AND_ALFRIDARY_22_SOURCE_NOTES_V1.json"
    save(dest, source)
    rules = {
        "batch": "B07as",
        "status": "LILLY_1647_CLXXI_PART_OF_FORTUNE_12_HOUSES_AND_PARTIAL_ALFRIDARY_SOURCE",
        "record_count": 22,
        "first_record": "R12743",
        "last_record": "R12764",
        "source_groups": 3,
        "body_pdf_frames": [766, 767, 768],
        "old_original_1647_CLXXI_physical_span_covered": True,
        "independent_full_source_expert_critical_edition_verified": False,
        "real_person_predicted_life_events_validated": 0,
        "runtime_promotions": 0,
        "rules": [
            {
                "id": r["id"],
                "record_number": r["record_number"],
                "batch": "B07as",
                "source_span": f"B07as-S{r['original_1647_pdf_frame'] - 765:03d}",
                "original_pdf_frames": [r["original_1647_pdf_frame"]],
                "role": r["role"],
                "source_anchor_not_diplomatic": r["derivative_navigation_anchor_not_diplomatic"],
                "historical_meaning_only": r["source_historical_interpretation_only"],
                "first_edition_source_sha256": r["original_1647_first_ed_photo_sha256"],
                "second_edition_source_sha256": r["original_1659_separately_typeset_photo_sha256"],
                "historical_source_documented": True,
                "independent_real_person_accuracy_verified": False,
                "runtime_model_promoted": False,
            }
            for r in notes
        ],
    }
    save(B / "RULES.json", rules)
    acceptance = {
        "batch": "B07as",
        "Lilly_before": 12742,
        "Ptolemy_retained": 1066,
        "Chinese_V7_retained": 355,
        "new_historical_source_notes": 22,
        "Lilly_after_if_accepted": 12764,
        "Western_after_if_accepted": 13830,
        "next_R": "R12765",
        "next_original_PDF": 768,
        "next_chapter": "CLXXII",
        "next_original_printed_folio": 734,
        "CLXXI_original_physical_span_covered": True,
        "full_original_diplomatic_philology_verified": False,
        "source_Alfridary_more_than_first_three_planets_assumed": False,
        "original_1647_natal_chart_calendar_engine_verified": False,
        "human_predictions_validated": 0,
        "runtime_promotions": 0,
        "source_records_SHA256": sha(dest),
        "rules_SHA256": sha(B / "RULES.json"),
    }
    save(B / "ACCEPTANCE.json", acceptance)
    print(
        json.dumps(
            {
                "historical_house_cases": 12,
                "separate_other_source_claims": 10,
                "source_new_notes": 22,
                "day_Alfridary_source": source[
                    "historical_source_Alfridary_day_first_three_7year_lords"
                ],
                "night_Alfridary_source": source[
                    "historical_source_Alfridary_night_first_three_7year_lords"
                ],
                "next_original": "R12765 CLXXII printed734/PDF768",
                "source_records_sha256": sha(dest),
                "rules_sha256": sha(B / "RULES.json"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    freeze()
