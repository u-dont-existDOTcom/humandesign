#!/usr/bin/env python3
# ruff: noqa: E501  # Preserve complete historical source descriptions.
"""Last original CLXXII comparison text and CLXXIII physical source boundary.

Original first edition 1647 printed 736–738 and separately typeset second
edition 1659; old apparent illness, criminal/moral, finance and marriage
claims are historical assertions, not validated individual outcomes.
"""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
FULL = "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"

NOTES = [
    (
        770,
        "example_return_chart_31st_year",
        "A historical horoscope figure is printed for the 31st year of the exemplar nativity.",
    ),
    (
        770,
        "example_birth_period_Sep19_1646",
        "The printed source chart references the 19 September 1646 solar revolution example.",
    ),
    (
        770,
        "old_apparent_time_with_equation",
        "The drawing distinguishes a historical local time and apparent time in an unverified old timekeeping system.",
    ),
    (
        770,
        "compare_birth_to_revolution",
        "Lilly instructs comparing the natal figure with the annual solar-return figure.",
    ),
    (
        770,
        "house_cusps_and_lords",
        "House cusps, their lords and principal significators are checked for agreement or difference.",
    ),
    (
        770,
        "return_natal_ascendant_matching",
        "When the annual ascendant agrees with the natal ascendant the source alleges favorable effects.",
    ),
    (
        770,
        "annual_asc_lord_combust",
        "The favorable ascendant assessment is reversed conditionally if its planetary lord is combust.",
    ),
    (
        770,
        "natal_moon_strength_qualified_exception",
        "A strong natal Moon in its dignity is described as mitigating the annual danger, especially in nocturnal charts.",
    ),
    (
        770,
        "return_ascendant_square_or_opposition",
        "Annual ascendant in square or opposition to natal ascendant introduces a conditional adverse reading.",
    ),
    (
        771,
        "revolution_from_natal_6th_12th_7th",
        "Return ascendant falling at natal 6th, 12th or 7th is said to indicate old illness or adversity, especially if those natal houses were afflicted.",
    ),
    (
        771,
        "natal_7th_rises_disputes_marriage",
        "Natal seventh-house sign rising annually is linked historically to disputes, desire for marriage or marriage.",
    ),
    (
        771,
        "annual_placement_money_significators",
        "The annual houses containing lord of second, Part Fortune or Jupiter are assigned patrimony claims.",
    ),
    (
        771,
        "malefic_rays_conditioned_on_year_lord",
        "The author conditions severe peril on hostile rays of malefics and contact of the Lord of the Year.",
    ),
    (
        771,
        "annual_planet_configuration_opposite_radix",
        "Even apparently good annual planetary positions can be read adversely when opposite their natal/radical configuration.",
    ),
    (
        772,
        "separate_next_CLXXIII_heading",
        "A physically distinct CHAP CLXXIII begins on printed738 after previous CLXXII ends; its Saturn return content is NOT admitted in this batch.",
    ),
]
assert len(NOTES) == 15


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def save(p, value):
    Path(p).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def freeze():
    old = j(WEST)
    china = j(CHINA)
    prev = j(B.parent / "B07at/ORIGINAL_CLXXII_RETURN_INTERPOLATION_OPENING_V1.json")
    prepared = j(B / "SOURCE_EVIDENCE_PREP_ONLY_V1.json")
    assert old["records_count"] == 12788 and old["batches"][-1]["id"] == "B07at"
    assert old["next"]["chapter"] == "CLXXII" and old["next"]["pdf_page"] == 770
    assert len(old["partial_numbered_chapters"]) == 1
    assert not old["partial_numbered_chapters"][0]["complete"]
    assert china["sum_source_annotations"] == 355
    assert prev["independent_real_life_predictions_validated"] == 0
    assert prepared["publication_status"] == "SOURCE_PHOTOS_ONLY_UNACCEPTED"
    assert len(prepared["historical_first_edition_source_photographs"]) == 4
    for item in prepared["historical_first_edition_source_photographs"]:
        file = B / item["relative_evidence_file"]
        assert sha(file) == item["sha256"]
        assert file.stat().st_size == item["exact_bytes"]
    photos = {}
    for page in (770, 771, 772):
        p = B / "evidence" / f"1647_original-{page}.jpg"
        assert p.is_file() and p.stat().st_size > 300000
        photos[f"1647_pdf{page}"] = {
            "source_year": 1647,
            "source_original_pdf_frame": page,
            "original_printed_folio": page - 34,
            "repository_path": str(p.relative_to(ROOT)),
            "sha256": sha(p),
            "bytes": p.stat().st_size,
        }
    for frame in (765, 766, 767):
        p = B / "evidence" / f"1659_original_djvu_{frame}.jpg"
        assert p.is_file() and p.stat().st_size > 200000
        photos[f"1659_djvu{frame}"] = {
            "source_year": 1659,
            "original_djvu_frame": frame,
            "original_printed_folio": frame - 29,
            "repository_path": str(p.relative_to(ROOT)),
            "sha256": sha(p),
            "bytes": p.stat().st_size,
        }
    assert len(photos) == 6
    records = []
    for idx, (frame, role, description) in enumerate(NOTES):
        assert frame in (770, 771, 772)
        a = photos[f"1647_pdf{frame}"]
        b = photos[f"1659_djvu{frame - 5}"]
        records.append(
            {
                "id": f"R{12789 + idx}",
                "record_number": 12789 + idx,
                "batch": "B07au",
                "source_span": f"B07au-S{frame - 769:03d}",
                "original_pdf_frames": [frame],
                "first_printed_original_folio": frame - 34,
                "role": role,
                "source_historical_interpretation_not_a_literal_quote": description,
                "source_1647_original_image_SHA256": a["sha256"],
                "source_1659_separately_typeset_photo_SHA256": b["sha256"],
                "original_source_one_reader_only": True,
                "original_edition_expert_philology_completed": False,
                "old_astrological_natal_annual_calendar_parity_completed": False,
                "historical_personal_health_wealth_marriage_crime_claim_validated": False,
                "independently_tested_actual_human_prediction": False,
                "runtime_promoted": False,
            }
        )
    assert [r["record_number"] for r in records] == list(range(12789, 12804))
    doc = {
        "schema": "LILLY_1647_CLXXII_ANNUAL_RETURN_RADIX_COMPARISON_AND_CLXXIII_BOUNDARY_V1",
        "batch": "B07au",
        "original_full_first_edition_PDF_SHA256": FULL,
        "source_original_physical_printed_folios": [736, 737, 738],
        "source_four_prepared_1647_PDF_photos_SHA256": {
            p["physical_source_first_edition_pdf_frame"]: p["sha256"]
            for p in prepared["historical_first_edition_source_photographs"]
        },
        "source_new_edition_photos": photos,
        "source_CLXXII_physically_covered_through_original_pdf_771": True,
        "separate_source_next_CLXXIII_heading_starts_pdf_772": True,
        "critical_source_edition_expert_collation_complete": False,
        "source_full_1647_solar_return_accurate_chart_engine_verified": False,
        "old_health_finance_marriage_status_claims_emprically_validated": False,
        "new_documentary_historical_source_notes": len(records),
        "Lilly_before": 12788,
        "Chinese_V7_retained": 355,
        "next_R": "R12804",
        "next_original_pdf": 772,
        "next_printed_chapter": "CLXXIII",
        "independent_real_human_prediction_validations": 0,
        "runtime_promotions": 0,
        "records": records,
    }
    path = B / "ORIGINAL_CLXXII_CHART_COMPARISON_AND_NEXT_CLXXIII_V1.json"
    save(path, doc)
    rules = {
        "batch": "B07au",
        "status": "LILLY_ORIGINAL_1647_CLXXII_PHYSICAL_END_ANNUAL_RADIX_COMPARISON",
        "record_count": len(records),
        "first_record": "R12789",
        "last_record": "R12803",
        "source_groups": 3,
        "body_pdf_frames": [770, 771, 772],
        "source_CLXXII_original_physical_span_covered": True,
        "expert_original_edition_perfect_collation_completed": False,
        "original_solar_return_and_human_predictions_validated": False,
        "runtime_promotions": 0,
        "rules": [
            {
                "id": r["id"],
                "record_number": r["record_number"],
                "batch": "B07au",
                "source_span": r["source_span"],
                "original_pdf_frames": r["original_pdf_frames"],
                "role": r["role"],
                "historical_meaning_only": r[
                    "source_historical_interpretation_not_a_literal_quote"
                ],
                "1647_photo_SHA256": r["source_1647_original_image_SHA256"],
                "1659_photo_SHA256": r["source_1659_separately_typeset_photo_SHA256"],
                "source_only_not_verified_human_event": True,
                "source_life_health_moral_personal_advice_allowed": False,
                "original_chart_engine_ephemeris_verified": False,
                "runtime_model_promoted": False,
            }
            for r in records
        ],
    }
    save(B / "RULES.json", rules)
    a = {
        "batch": "B07au",
        "Lilly_before": 12788,
        "Ptolemy_retained": 1066,
        "Chinese_V7_retained": 355,
        "new_historical_source_records": len(records),
        "Lilly_if_accepted": 12803,
        "Western_if_accepted": 13869,
        "first_CLXXII_physical_source_span_complete": True,
        "first_CLXXII_source_critical_expert_collation_complete": False,
        "next_original_R": "R12804",
        "next_original_pdf": 772,
        "next_original_printed_folio": 738,
        "next_chapter": "CLXXIII",
        "new_source_SHA256": sha(path),
        "rules_SHA256": sha(B / "RULES.json"),
        "independent_actual_human_predictive_validations": 0,
        "runtime_promotions": 0,
    }
    save(B / "ACCEPTANCE.json", a)
    print(
        json.dumps(
            {
                "notes": len(records),
                "source_pages": len(photos),
                "first": "R12789",
                "last": "R12803",
                "next": "R12804 CLXXIII",
                "unreviewed_future_first_edition_photo": 773,
                "original_source_SHA256": a["new_source_SHA256"],
                "rules_sha256": a["rules_SHA256"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    freeze()
