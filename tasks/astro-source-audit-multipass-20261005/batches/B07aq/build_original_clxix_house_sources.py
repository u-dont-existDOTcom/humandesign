#!/usr/bin/env python3
# ruff: noqa: E501  # Preserve historical source/working-interpretation prose.
"""Lilly 1647 CLXIX original house interpretations and missing-eleventh repair.

Physical first edition and independently typeset 1659 edition both include
the 11th-house paragraph; a modern searchable derivative omits it. This
preserves source history, not evidence of actual human astrological accuracy.
"""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
BASE = B.parent
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
NAV = B / "SECONDARY_CLXIX_NAVIGATOR_OMITS_ELEVENTH.txt"
FULL_ORIGINAL_PDF_SHA = "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"

PHOTOS = {
    "1647_folio729": BASE / "B07ap/evidence/1647_original-763.jpg",
    "1647_folio730": B / "evidence/original_1647-764.jpg",
    "1647_folio731": B / "evidence/original_1647-765.jpg",
    "1659_folio729": BASE / "B07ap/evidence/1659_original_djvu_758.jpg",
    "1659_folio730": B / "evidence/original_1659_djvu_759.jpg",
    "1659_folio731": B / "evidence/original_1659_djvu_760.jpg",
}
HOUSE_MEANINGS = [
    (
        1,
        763,
        "When the Progression of the Ascendant or the Moon",
        "History claims cheerfulness and time for material provision and clothing.",
    ),
    (
        2,
        763,
        "When to the 2nd house",
        "Historical claim of trade, buying/selling and growth of property.",
    ),
    (
        3,
        763,
        "When to the 3rd",
        "Historical claim about travel, kin and interactions with religious people.",
    ),
    (
        4,
        763,
        "When to the 4th",
        "Historical positive property/inheritance/building images coexist with grief/water hazards.",
    ),
    (
        5,
        763,
        "When to the 5th",
        "Historical pleasure, age-specific socializing and correspondence/agreements.",
    ),
    (6, 763, "When to the 6th", "Historical illness/enmity/servant and contracting warnings."),
    (
        7,
        763,
        "When to the 7th",
        "Historical marriage and open conflicts, explicitly conditional on other significators.",
    ),
    (
        8,
        763,
        "When to the 8th",
        "Historical material loss, slander and qualified mortality rhetoric; not clinical proof.",
    ),
    (
        9,
        764,
        "When to the 9th",
        "Historical long journeys, learning and religious/chemical study images.",
    ),
    (
        10,
        764,
        "When to the 10th",
        "Historical ambition, public office, occupational progress and capability qualifier.",
    ),
    (
        11,
        764,
        None,
        "ORIGINAL-ONLY: 11th-house friends, cheerful disposition, prosperity, husbanding time and private fortune.",
    ),
    (
        12,
        764,
        "When to the 12th",
        "Historical illness, enmity, confinement and horse-related cautions, qualified by natal 12th.",
    ),
]
ADDITIONAL = [
    (
        763,
        "fifth_age_context",
        "according to the yeers of his age",
        "House 5 pleasure interpretation is conditioned by the person's age.",
    ),
    (
        763,
        "seventh_other_significators",
        "the other Significators concurring",
        "House 7 marriage claim explicitly needs corroborating significators.",
    ),
    (
        764,
        "eighth_Hyleg_mortal_direction",
        "if the Hyleg come to any mortall Direction",
        "House 8 mortality remark requires an additional Hyleg direction; source-only rhetoric.",
    ),
    (
        764,
        "tenth_if_capable",
        "if capable",
        "Public advancement is qualified by ability/social circumstance.",
    ),
    (
        764,
        "twelfth_natal_house_qualifier",
        "unlesse the 12th house in the Radix was fortunate",
        "Old 12th house warnings contain a natal configuration exception.",
    ),
    (
        764,
        "arabic_source_translation_warning",
        "being ill translated out of the Arabick",
        "Author attributes contradictions in older rules to poor Arabic translation.",
    ),
    (
        764,
        "infortune_annual_revolution_house",
        "when the ascendant comes to the body of an Infortune",
        "Author says contextual house of a malefic in annual revolution modifies the interpretation.",
    ),
    (
        764,
        "year_lord_and_house_lords",
        "they also judge much by the Lord of the yeer",
        "The source additionally refers to ruler of the year and all houses.",
    ),
    (
        765,
        "next_CLXX_physical_heading",
        "C H A P. C L X X.",
        "Physical next CHAP CLXX Midheaven/Sun profections starts printed731, distinct source unit.",
    ),
]

LITERAL_11TH = (
    "When to the eleventh, it signifies a cheerfull heart and person, "
    "the encrease of the Native's Friends, it imports the yeer "
    "to be very prosperous in all worldly affaires, and it invites "
    "the Native to bestirre himselfe and husband time well, whereby "
    "he may much advance his private fortune, &c."
)


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


def load(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def save(f, v):
    Path(f).write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def freeze():
    index = load(INDEX)
    chinese = load(CHINA)
    assert index["records_count"] == 12704
    assert index["batches"][-1]["id"] == "B07ap"
    assert index["next"]["chapter"] == "CLXIX" and index["next"]["pdf_page"] == 763
    assert chinese["sum_source_annotations"] == 355
    text = NAV.read_text(encoding="utf-8")
    assert sha(NAV) == "fa2f78a87c05bb1dee27ba400f6c5bd840364fd7c4962c8697373b5dec0f9bcc"
    assert "When to the 10th" in text
    assert "When to the 12th" in text
    assert all(
        k not in text for k in ("When to the eleventh", "When to the 11th", "When to the 11 th")
    )
    witnesses = {}
    for label, file in PHOTOS.items():
        assert file.is_file(), label
        assert file.stat().st_size > 250000, label
        witnesses[label] = {
            "relative_file": str(file.relative_to(ROOT)),
            "sha256": sha(file),
            "bytes": file.stat().st_size,
            "source_year": int(label[:4]),
            "printed_folio": int(label[-3:]),
        }
    assert len(witnesses) == 6
    entries = []
    for h, frame, anchor, meaning in HOUSE_MEANINGS:
        role = f"ascendant_or_moon_profection_house_{h:02d}"
        if anchor is not None:
            assert anchor in text, (role, anchor)
            offset = text.index(anchor)
        else:
            assert h == 11
            offset = None
        entries.append((frame, role, anchor, meaning, h, offset))
    for frame, role, anchor, meaning in ADDITIONAL:
        assert anchor in text, (role, anchor)
        entries.append((frame, role, anchor, meaning, None, text.index(anchor)))
    assert len(entries) == 21
    rows = []
    receipts = []
    for i, (frame, role, anchor, meaning, house, offset) in enumerate(entries):
        label = str(frame - 34)
        original_first = witnesses["1647_folio" + label]
        second = witnesses["1659_folio" + label]
        original_only = house == 11
        row = {
            "id": f"R{12705 + i}",
            "record_number": 12705 + i,
            "batch": "B07aq",
            "source_group": f"B07aq-S{frame - 762:03d}",
            "role": role,
            "original_1647_pdf_frame": frame,
            "original_1647_printed_folio": frame - 34,
            "profection_house_number": house,
            "source_historical_meaning_not_predictive_evidence": meaning,
            "source_first_1647_photo_SHA256": original_first["sha256"],
            "source_second_1659_photo_SHA256": second["sha256"],
            "modern_derivative_navigator_anchor": anchor,
            "modern_derivative_relative_offset": offset,
            "original_print_missing_in_modern_derivative": original_only,
            "first_edition_11th_manual_cleaned_transcription_if_relevant": LITERAL_11TH
            if original_only
            else None,
            "physical_original_edition_read_by_one_reader": True,
            "independent_diplomatic_second_researcher_collation": False,
            "source_actual_human_health_money_reputation_prediction_validated": False,
            "runtime_promoted": False,
        }
        rows.append(row)
        receipts.append(
            {
                "id": row["id"],
                "source_years": [1647, 1659],
                "original_1647_folio": frame - 34,
                "original_1647_photo_sha256": original_first["sha256"],
                "original_1659_photo_sha256": second["sha256"],
                "modern_searchable_excerpt_present": anchor is not None,
                "navigator_sha256": sha(NAV),
                "one_reader_not_double_blind": True,
            }
        )
    assert [r["record_number"] for r in rows] == list(range(12705, 12726))
    assert sum(r["original_print_missing_in_modern_derivative"] for r in rows) == 1
    out = {
        "schema": "LILLY_FIRST_SECOND_EDITIONS_CLXIX_ASC_MOON_HOUSE_SOURCE_21_V1",
        "batch": "B07aq",
        "source": "William Lilly original 1647 first edition vs separately typeset 1659 second edition",
        "original_1647_full_pdf_SHA256": FULL_ORIGINAL_PDF_SHA,
        "source_original_first_CLXIX_physical_frames": [763, 764],
        "source_next_distinct_CLXX_heading_frame": 765,
        "source_six_original_primary_images": witnesses,
        "searchable_derivative_excerpt_sha256": sha(NAV),
        "source_original_eleven_house_article_excerpt_cleaned_by_one_reader": LITERAL_11TH,
        "source_original_1647_and_1659_both_contain_11th": True,
        "secondary_modern_html_transcription_omits_house11": True,
        "all_twelve_house_positions_documented_from_original": True,
        "new_documentary_source_notes": len(rows),
        "Lilly_before": 12704,
        "Lilly_if_accepted": 12725,
        "Ptolemy_retained": 1066,
        "Chinese_V7_retained": 355,
        "first_CLXIX_physical_text_span_covered": True,
        "full_independent_expert_critical_edition_verified": False,
        "full_verified_astro_birth_chart_era_engine": False,
        "actual_human_predictive_validations": 0,
        "runtime_promotions": 0,
        "source_rows": rows,
    }
    doc = B / "FIRST_SECOND_ORIGINAL_CLXIX_HOUSES_21_NOTES_V1.json"
    save(doc, out)
    witness = {
        "batch": "B07aq",
        "physical_source_years": [1647, 1659],
        "full_original_1647_pdf_SHA256": FULL_ORIGINAL_PDF_SHA,
        "source_photo_metadata": witnesses,
        "manually_transcribed_clean_11th_from_original_first_edition": LITERAL_11TH,
        "original_first_and_second_printings_agree_eleventh_present": True,
        "modern_secondary_11th_omitted": True,
        "modern_excerpt_SHA256": sha(NAV),
        "original_full_diplomatic_character_collation_independent": False,
        "human_predicted_results_validated": 0,
        "runtime_promotions": 0,
        "source_row_proofs": receipts,
    }
    proof = B / "PHOTO_ELEVENTH_1647_1659_SOURCE_WITNESS_V1.json"
    save(proof, witness)
    rule = {
        "batch": "B07aq",
        "status": "ORIGINAL_1647_CLXIX_PROFECTIONS_HOUSES_SOURCE_WITH_MISSING_MODERN_ELEVENTH_REPAIRED",
        "record_count": 21,
        "first_record": "R12705",
        "last_record": "R12725",
        "source_groups": 3,
        "body_pdf_frames": [763, 764, 765],
        "twelve_house_source_positions": True,
        "eleventh_missing_in_modern_derivative_not_first_or_second_original": True,
        "first_CLXIX_physical_span_complete": True,
        "critical_expert_diplomatic_edition_complete": False,
        "source_calendar_natal_engine_verified": False,
        "independent_human_predictions_validated": 0,
        "runtime_promotions": 0,
        "rules": [
            {
                "id": r["id"],
                "record_number": r["record_number"],
                "batch": "B07aq",
                "source_span": r["source_group"],
                "original_pdf_frames": [r["original_1647_pdf_frame"]],
                "role": r["role"],
                "source_anchor_not_diplomatic": r["modern_derivative_navigator_anchor"],
                "original_1647_photo_sha256": r["source_first_1647_photo_SHA256"],
                "source_1659_photo_sha256": r["source_second_1659_photo_SHA256"],
                "historical_meaning_only": r["source_historical_meaning_not_predictive_evidence"],
                "historical_source_documented": True,
                "source_missing_in_secondary_html": r[
                    "original_print_missing_in_modern_derivative"
                ],
                "actual_human_event_prediction_validated": False,
                "clinical_mortality_criminal_character_finance_claim_validated": False,
                "runtime_model_promoted": False,
            }
            for r in rows
        ],
    }
    save(B / "RULES.json", rule)
    acceptance = {
        "batch": "B07aq",
        "Lilly_before": 12704,
        "Ptolemy_retained": 1066,
        "Chinese_V7_retained": 355,
        "new_historical_source_notes": 21,
        "Lilly_if_accepted": 12725,
        "Western_if_accepted": 13791,
        "next_R": "R12726",
        "next_original_pdf_frame": 765,
        "next_original_printed_folio": 731,
        "next_chapter": "CLXX",
        "next_source": "Mid-heaven and Sun profection through houses; new chapter heading already documented",
        "CLXIX_original_physical_span_covered": True,
        "CLXIX_original_11th_present_both_originals": True,
        "CLXIX_11th_missing_modern_transcription": True,
        "original_full_source_expert_critical_collation": False,
        "original_1647_birth_chart_calendar_engine_verified": False,
        "source_notes_sha256": sha(doc),
        "source_witness_sha256": sha(proof),
        "rules_sha256": sha(B / "RULES.json"),
        "human_predictions_validated": 0,
        "runtime_promotions": 0,
    }
    save(B / "ACCEPTANCE.json", acceptance)
    print(
        json.dumps(
            {
                "documented_houses": 12,
                "modern_missing_house": 11,
                "source_original_two_independently_typeset_prints": True,
                "new_historical_notes": 21,
                "next_R": acceptance["next_R"],
                "next_original_PDF": 765,
                "source_notes_sha256": sha(doc),
                "source_witness_sha256": sha(proof),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    freeze()
