#!/usr/bin/env python3
"""Version original merchant nativity source scans and apparent nonblindness.

The original 1647 chart date is a *printed source input*, not a proven civil
calendar date, independently calculated chart, or successful life prediction.
Preserve original photos in both separately typeset editions and document
source-observed score arithmetic vs author interpretation as distinct layers.
"""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = ROOT / "tasks/astro-source-audit-multipass-20261005"
INDEX = TASK / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
PARENT = TASK / "batches/B07aw"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def freeze():
    western = load(INDEX)
    chinese = load(CHINESE)
    parent = load(PARENT / "ORIGINAL_NEXT_MERCHANT_NATIVITY_BOUNDARY_1647_1659_V1.json")
    assert western["records_count"] == 12870
    assert western["batches"][-1]["id"] == "B07aw"
    assert western["next"]["chapter"] == "CLXXV"
    assert western["next"]["pdf_page"] == 776
    assert chinese["sum_source_annotations"] == 355
    assert western["source_sha256"] == (parent["original_full_Wellcome_1647_pdf_sha256"])
    images = {}
    for year, frames in ((1647, range(776, 781)), (1659, range(771, 776))):
        for frame in frames:
            if year == 1647 and frame == 776:
                file = PARENT / "evidence/1647_original-776.jpg"
            elif year == 1659 and frame == 771:
                file = PARENT / "evidence/1659_original_djvu_771.jpg"
            else:
                file = (
                    B
                    / "evidence"
                    / (
                        f"first_1647_print-{frame}.jpg"
                        if year == 1647
                        else f"second_1659_djvu_{frame}.jpg"
                    )
                )
            assert file.is_file(), file
            assert file.stat().st_size > 200_000
            physical = frame - (34 if year == 1647 else 29)
            assert 742 <= physical <= 746
            images[f"{year}_printed_{physical}"] = {
                "printed_year": year,
                "original_PDF_or_DjVu_frame": frame,
                "printed_folio": physical,
                "file": str(file.relative_to(ROOT)),
                "sha256": sha(file),
                "bytes": file.stat().st_size,
            }
    assert len(images) == 10
    assert images["1647_printed_742"]["sha256"] == parent["new_first_edition_page_sha256"]
    assert images["1659_printed_742"]["sha256"] == parent["new_second_typeset_edition_page_sha256"]

    temperament = {
        "historical_scheme": "Hot / moist / cold / drie",
        "literal_first_edition_1647_folio743_counts": {"hot": 7, "moist": 6, "cold": 6, "drie": 7},
        "1669_nonexistent_source_verification": False,
        "first_and_second_edition_folio743_single_reader_correspond": True,
        "original_author_source_folio743_conclusion": (
            "Sanguine, Cholerick testimonies narrowly predominate, "
            "but the four humours seem nearly mixed; author says he "
            "personally knows the merchant and sees no clear excess."
        ),
        "original_author_source_folio744_requalification": (
            "Calls him Sanguine / Melancholly, using air-sign luminaries/"
            "planets and natal lord Saturn as separate rationales."
        ),
        "author_already_knows_native_in_source_text": True,
        "retrospective_case_not_blind_or_independent_cohort": True,
    }
    scores = [
        ("Saturn", 8, 12, -4),
        ("Jupiter", 16, 7, 9),
        ("Mars", 17, 5, 12),
        ("Sun", 7, 13, -6),
        ("Venus", 20, 4, 16),
        ("Mercury", 6, 9, -3),
        ("Moon", 10, 7, 3),
        ("Part_of_Fortune", 7, 7, 0),
    ]
    for body, strength, weakness, net in scores:
        assert strength - weakness == net, body
    details = {
        "schema": "LILLY_MERCHANT_B07ax_ORIGINAL_PRINT_PHOTOS_AND_NONBLIND_SCORING_V1",
        "batch": "B07ax",
        "status": "PHOTO_CHECKPOINT_NOT_YET_CANONICAL_RULES",
        "original_1647_Wellcome_full_scan_sha256": western["source_sha256"],
        "1647_printed_original_chapter": "CLXXV",
        "1659_printed_original_chapter": "CLXXV",
        "chapter_title": parent["first_edition_original_chapter_heading"],
        "original_source_photographic_witnesses": images,
        "original_1647_chart_center_source_folio742": {
            "source_printed_year": 1616,
            "source_printed_month_word": "Septemb",
            "source_printed_day": 19,
            "source_printed_clock_text": "2 h. 24. 39 P.M.",
            "source_printed_Latitude": 53,
            "original_calendar_style_resolved": False,
            "source_nativity_birth_place_precise_city_verified": False,
            "original_chart_computed_against_modern_ephemeris": False,
            "birth_time_independent_source_certificate": False,
        },
        "temperament_source_table_and_author_qualifications": temperament,
        "original_1647_planetary_dignity_source_folio744_745": [
            {
                "body": b,
                "source_fortitude_points": pos,
                "source_debility_points": neg,
                "computed_source_net": net,
                "direct_source_claim_empirically_validated_on_person": False,
            }
            for b, pos, neg, net in scores
        ],
        "boundary_next_1647_printed_CLXXVI_manners_starts_folio745": True,
        "source_case_is_known_to_author_no_blind_human_validation": True,
        "theoretical_frameworks_not_automatically_equivalent": True,
        "original_chart_lunisolar_or_epoch_math_verified": False,
        "historical_cases_proven_independently_predictive": 0,
        "runtime_model_promotions": 0,
        "next_unaccepted_Lilly_R": "R12871",
    }
    dest = B / "ORIGINAL_MERCHANT_1647_1659_PHOTO_CHECKPOINT_V1.json"
    save(dest, details)
    print(
        json.dumps(
            {
                "photo_source_witnesses": len(images),
                "original_1647_birth_chart_folio": 742,
                "historical_source_humour_totals": temperament[
                    "literal_first_edition_1647_folio743_counts"
                ],
                "dignity_source_8_bodies": {
                    r["body"]: r["computed_source_net"]
                    for r in details["original_1647_planetary_dignity_source_folio744_745"]
                },
                "photo_checkpoint_sha256": sha(dest),
                "human_predictive_validations": 0,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    freeze()
