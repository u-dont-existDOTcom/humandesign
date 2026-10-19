#!/usr/bin/env python3
# ruff: noqa: E501  # Keep original source descriptions complete for audit.
"""Original 1647 CLXXII solar revolution opening: exact printed mechanics.

Treat original 1647 and separately typeset 1659 folios734–735 as physical
documentary witnesses, not empirical human outcome or independently verified
seventeenth-century astronomy/civil calendar. Preserve fractional seconds.
"""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
BASE = B.parent
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
FULL_BOOK_SHA = "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
PHOTO = {
    "original_1647_printed734": BASE / "B07as/evidence/1647_original-768.jpg",
    "original_1647_printed735": B / "evidence/1647_original-769.jpg",
    "independent_1659_printed734": BASE / "B07as/evidence/original_1659_djvu_763.jpg",
    "independent_1659_printed735": B / "evidence/1659_original_djvu_764.jpg",
}
OBS = [
    (
        768,
        "CLXXII_physical_heading",
        "Distinct printed CHAP CLXXII Of Revolutions begins below the CLXXI page734 divider.",
    ),
    (
        768,
        "definition_sun_return",
        "A historical solar revolution is defined as Sun returning to natal radix exact zodiacal longitude.",
    ),
    (
        768,
        "natal_solar_hour_accuracy",
        "The text asks natal solar place at the actual hour of birth, not just the natal civil date.",
    ),
    (
        768,
        "one_arcminute_24minute_time_warning",
        "Lilly warns that one arcminute error of solar motion causes approximately 24 minutes timing error.",
    ),
    (
        768,
        "ephemeris_next_day_compare",
        "Select annual return-day ephemeris Sun longitude nearest natal zodiacal longitude, subtract remaining arcminutes.",
    ),
    (
        768,
        "motion_to_fractional_day",
        "Divide remaining solar longitude arc by full diurnal Sun motion and scale by 24 hours for return time.",
    ),
    (
        768,
        "historical_alt_authors",
        "Author cites Maginus and Argol as alternative procedures; neither is independently verified here.",
    ),
    (
        768,
        "historic_31st_year_case",
        "Announces a sample revolution for a native in the thirty-first year.",
    ),
    (
        769,
        "origanus_solar_noon_year_1646",
        "Origanus 19 September 1646 at noon places Sun at 6 degrees 12 arcminutes Libra.",
    ),
    (769, "natal_radix_solar_6_37_Libra", "Natal source Sun is 6 degrees 37 minutes Libra."),
    (
        769,
        "source_solar_remaining_25_arcminutes",
        "Subtracting the source noon return-day Sun from natal Sun leaves 25 arcminutes.",
    ),
    (
        769,
        "source_sun_diurnal_59_10",
        "Daily solar motion from ephemeris is 59 arcminutes 10 arcseconds.",
    ),
    (
        769,
        "maginus_nearest_daily_59_08",
        "Old Maginus table uses nearby 59 arcminutes 8 arcseconds, not exact 59 arcminutes 10 seconds.",
    ),
    (
        769,
        "twenty_arcminute_fractional_hours",
        "Historical Maginus 20-arcminute cell contributes 8 hours 7 minutes 2 seconds.",
    ),
    (
        769,
        "five_arcminute_fractional_hours",
        "Historical Maginus 5-arcminute cell contributes 2 hours 1 minute 45 seconds.",
    ),
    (
        769,
        "sum_fractional_10h08m47s",
        "Source table cell sums yield 10 hours 8 minutes 47 seconds; later text quotes time only through minutes.",
    ),
    (
        769,
        "Frankfurt_19Sep1646_10h08m",
        "Lilly dates solar return at Frankfurt 19 September 1646 around 10 hours 8 minutes after noon.",
    ),
    (
        769,
        "Westward_meridian_subtract_1h07m",
        "Source corrects westward meridian offset by subtracting 1 hour 7 minutes from Frankfurt's time.",
    ),
    (
        769,
        "local_9h01m_after_noon",
        "After source's whole-minute truncation, meridian correction yields 9 hours 1 minute after noon.",
    ),
    (
        769,
        "house_table_latitude53_noon_12h26m",
        "The historical 53-degree latitude house table contributes 12 hours 26 minutes in Lilly's account.",
    ),
    (
        769,
        "equation_time_16min",
        "Source appends an equation of time of 16 minutes to the house-table calculation.",
    ),
    (769, "combined_21h43m", "The historical 9h01m + 12h26m + 0h16m equals 21h43m."),
    (
        769,
        "midheaven_23Aquarius",
        "The author's resulting house-table example locates MC at 23 degrees Aquarius.",
    ),
    (
        769,
        "ascendant_0Cancer32",
        "The author's resulting ascendant is Cancer 0 degrees 32 minutes.",
    ),
]
assert len(OBS) == 24


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def save(p, data):
    Path(p).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def freeze():
    west = j(WEST)
    china = j(CHINA)
    assert west["records_count"] == 12764 and west["batches"][-1]["id"] == "B07as"
    assert west["next"]["chapter"] == "CLXXII" and west["next"]["pdf_page"] == 768
    assert china["sum_source_annotations"] == 355
    images = {}
    for key, file in PHOTO.items():
        assert file.is_file() and file.stat().st_size > 150000, key
        images[key] = {
            "repository_path": str(file.relative_to(ROOT)),
            "source_year": 1647 if "1647" in key else 1659,
            "printed_folio": 734 if "734" in key else 735,
            "raw_image_SHA256": sha(file),
            "raw_image_bytes": file.stat().st_size,
        }
    # The original source rounds/truncates 10:08:47 to 10:08 before
    # applying the westward meridian subtraction: do not silently
    # declare the result an exact astronomical civil time.
    hms20 = [8, 7, 2]
    hms5 = [2, 1, 45]

    def to_seconds(hms):
        return hms[0] * 3600 + hms[1] * 60 + hms[2]

    def from_seconds(sec):
        return [sec // 3600, (sec // 60) % 60, sec % 60]

    hms25 = from_seconds(to_seconds(hms20) + to_seconds(hms5))
    assert hms25 == [10, 8, 47]
    truncated = [10, 8]
    westward = [1, 7]
    adjusted = [9, 1]
    assert 60 * truncated[0] + truncated[1] - 60 * westward[0] - westward[1] == 541
    assert 60 * adjusted[0] + adjusted[1] == 541
    combine = [12, 26]
    equa = [0, 16]
    combined = [21, 43]
    assert sum(x[0] * 60 + x[1] for x in (adjusted, combine, equa)) == (
        combined[0] * 60 + combined[1]
    )
    records = []
    for idx, (frame, role, gloss) in enumerate(OBS):
        source = "original_1647_printed734" if frame == 768 else "original_1647_printed735"
        second = "independent_1659_printed734" if frame == 768 else "independent_1659_printed735"
        records.append(
            {
                "id": f"R{12765 + idx}",
                "record_number": 12765 + idx,
                "batch": "B07at",
                "source_span": "B07at-S001" if frame == 768 else "B07at-S002",
                "original_pdf_frames": [frame],
                "original_1647_printed_folio": frame - 34,
                "role": role,
                "source_photographic_documentary_gloss_not_verbatim_quote": gloss,
                "original_first_edition_photo_sha256": images[source]["raw_image_SHA256"],
                "original_independent_1659_print_photo_sha256": images[second]["raw_image_SHA256"],
                "source_one_reader_review": True,
                "source_original_linguistic_critical_expert_review": False,
                "old_epoch_EPHEMERIS_calendar_meridian_parity_verified": False,
                "real_person_life_event_predictions_validated": False,
                "runtime_promoted": False,
            }
        )
    assert [r["record_number"] for r in records] == list(range(12765, 12789))
    literal = {
        "example_year_written": 1646,
        "calendar_style_independently_confirmed": False,
        "historical_source_month_day": "September 19",
        "original_natal_longitude_sign": "Libra",
        "original_natal_longitude_deg_min": [6, 37],
        "original_ephemeris_noon_deg_min": [6, 12],
        "remaining_arcminutes": 25,
        "source_sun_daily_motion_arcminute_arcsecond": [59, 10],
        "historical_nearby_table_rate_arcminute_arcsecond": [59, 8],
        "twenty_arcminute_time_hms": hms20,
        "five_arcminute_time_hms": hms5,
        "source_sum_unrounded_time_hms": hms25,
        "printed_later_minute_level_time_hm": truncated,
        "source_westward_meridian_subtract_hm": westward,
        "source_local_time_after_noon_hm": adjusted,
        "house_table_latitude_degrees": 53,
        "house_table_noon_hm": combine,
        "source_equation_of_time_hm": equa,
        "source_house_table_final_hm": combined,
        "source_MC_zodiac_sign": "Aquarius",
        "source_MC_zodiac_degrees": 23,
        "source_ascendant_sign": "Cancer",
        "source_ascendant_deg_min": [0, 32],
        "printed_arithmetic_checked_not_actual_1646_sun_ephemeris": True,
    }
    source_data = {
        "schema": "LILLY_ORIGINAL_1647_1659_CLXXII_SOLAR_REVOLUTION_OPENING_V1",
        "batch": "B07at",
        "original_full_1647_book_PDF_SHA256": FULL_BOOK_SHA,
        "documentary_witness_photos": images,
        "initial_first_1647_physical_source_frames": [768, 769],
        "initial_printed_folios": [734, 735],
        "original_CLXXII_full_source_physical_span_read": False,
        "original_Lilly_solar_return_algorithm_ephemeris_correctness_verified": False,
        "solar_return_example_1646_true_birth_hour_calendar_and_meridian_parity_verified": False,
        "original_first_second_editions_read_by_separate_expert": False,
        "historical_source_claims_to_add": len(records),
        "prior_accepted_Lilly_historical_annotations": 12764,
        "Chinese_V7_historical_retained": 355,
        "next_original_record_if_accepted": f"R{12765 + len(records)}",
        "next_original_PDF_if_accepted": 770,
        "source_fractional_seconds_truncated_not_exactly_reconciled": True,
        "independent_real_life_predictions_validated": 0,
        "runtime_promotions": 0,
        "original_1646_literal_versus_computed_arithmetic": literal,
        "records": records,
    }
    save(B / "ORIGINAL_CLXXII_RETURN_INTERPOLATION_OPENING_V1.json", source_data)
    rules = {
        "batch": "B07at",
        "status": "FIRST_ORIGINAL_1647_CLXXII_SOLAR_REVOLUTION_OPENING_SOURCE_ONLY",
        "record_count": len(records),
        "first_record": records[0]["id"],
        "last_record": records[-1]["id"],
        "body_pdf_frames": [768, 769],
        "source_groups": 2,
        "next_original_record": f"R{12765 + len(records)}",
        "source_full_CLXXII_complete": False,
        "1646_example_historical_astronomy_validated": False,
        "independent_real_human_predictions_validated": 0,
        "runtime_promotions": 0,
        "rules": [
            {
                "id": r["id"],
                "record_number": r["record_number"],
                "batch": "B07at",
                "source_span": r["source_span"],
                "original_pdf_frames": r["original_pdf_frames"],
                "role": r["role"],
                "historical_meaning_only": r[
                    "source_photographic_documentary_gloss_not_verbatim_quote"
                ],
                "first_original_photo_sha256": r["original_first_edition_photo_sha256"],
                "independent_1659_print_photo_sha256": r[
                    "original_independent_1659_print_photo_sha256"
                ],
                "historical_source_documented_by_one_reader": True,
                "original_natal_chart_and_timing_engine_verified": False,
                "real_person_prediction_validated": False,
                "runtime_model_promoted": False,
            }
            for r in records
        ],
    }
    save(B / "RULES.json", rules)
    accept = {
        "batch": "B07at",
        "Lilly_before": 12764,
        "Ptolemy_retained": 1066,
        "Chinese_V7_retained": 355,
        "new_historical_source_records": len(records),
        "Lilly_after_if_accepted": 12764 + len(records),
        "Western_after_if_accepted": 12764 + len(records) + 1066,
        "next_original_R": f"R{12765 + len(records)}",
        "next_original_PDF": 770,
        "next_original_printed_folio": 736,
        "next_chapter": "CLXXII",
        "full_CLXXII_source_chapter_finished": False,
        "solar_return_old_ephemeris_calendar_math_independently_verified": False,
        "source_photo_and_arithmetic_SHA256": sha(
            B / "ORIGINAL_CLXXII_RETURN_INTERPOLATION_OPENING_V1.json"
        ),
        "rules_SHA256": sha(B / "RULES.json"),
        "actual_human_predictions_validated": 0,
        "runtime_promotions": 0,
    }
    save(B / "ACCEPTANCE.json", accept)
    print(
        json.dumps(
            {
                "records": len(records),
                "first": rules["first_record"],
                "last": rules["last_record"],
                "next": accept["next_original_R"],
                "source_photo_sha": [row["raw_image_SHA256"] for row in images.values()],
                "first_1646_return_arithmetic_hms": hms25,
                "old_1646_house_time_hm": combined,
                "source_sha256": accept["source_photo_and_arithmetic_SHA256"],
                "rules_sha256": accept["rules_SHA256"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    freeze()
