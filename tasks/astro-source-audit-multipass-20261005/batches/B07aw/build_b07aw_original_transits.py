#!/usr/bin/env python3
# ruff: noqa: E501  # Preserve complete historical meanings without truncated source glosses.
"""Original 1647 and 1659 CLXXIV transits source, as bounded source records.

This is historical textual evidence, not astronomical or human validation.
The modern searchable excerpt is a finding aid known to contain errors.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT / "tasks/astro-source-audit-multipass-20261005"
WEST = T / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
PARENT = T / "batches/B07av"
SOURCE_SHA = "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
SECONDARY_SHA = "b911e0f0c62b79bffd461631af6216fd8cfa808f13657c33b260478258b82792"

# Locator string is deliberately *from the faulty secondary transcription*,
# distinct from the photographed original reading / our historical gloss.
CLAIMS = [
    (
        "ephemeris_required",
        "The Transit of the Planets is best found out be an Ephemeris",
        "An ephemeris is the method specified for finding daily planetary transits.",
    ),
    (
        "day_month_query",
        "what day of every moneth",
        "Look up the day of each month on which a particular planetary body crosses a natal reference point.",
    ),
    (
        "natal_cusps",
        "cusps of the houses of the Radicall Figure",
        "The radical chart's house cusps are candidate transit targets.",
    ),
    (
        "natal_planets_nodes_fortune",
        "any of the seven Planets, North Node or South Node or Part of Fortune",
        "The seven natal planetary degrees, two lunar nodes and Part of Fortune are also target degrees.",
    ),
    (
        "natal_aspects",
        "Square dexter or sinister, or Opposition",
        "The source directs checking aspects from the transiting planet to natal positions, including dexter/sinister square and opposition, alongside sextile/trine.",
    ),
    (
        "Jupiter_Venus_on_ascendant",
        "The Transit of Jupiter or Mars by the degree ascending",
        "The *original* 1647 and 1659 printed glyphs are Jupiter OR VENUS, not Jupiter OR Mars as the searchable text claims; their transit of natal Ascendant is alleged beneficial.",
    ),
    (
        "ascendant_actions_body",
        "ascendant signifies the actions of the Body",
        "Lilly explains the alleged Ascendant transit effect by identifying the Ascendant with bodily actions.",
    ),
    (
        "Jupiter_Venus_second_cusp",
        "Transit the custp of the 2nd house",
        "Jupiter or Venus crossing the natal second-house cusp is said to favor obtaining money or buying commodities.",
    ),
    (
        "Jupiter_Venus_third_cusp_kin",
        "Transit the cusp of the 3rd house",
        "The same two benefics crossing or favorably aspecting the natal third-house cusp are associated with kinfolk and neighbors.",
    ),
    (
        "third_house_travel",
        "apt time to set forth upon any Journey",
        "The natal third-house example also alleges a favorable day for beginning a journey.",
    ),
    (
        "other_houses_analogy",
        "in all the rest of the houses",
        "Lilly broadly extends his house-cusp analogy without printing a full twelve-house transit rule list.",
    ),
    (
        "Mars_ascending_choler",
        "If Mars doe transit the degree ascending",
        "Mars crossing natal Ascendant is alleged to occasion choler, passion and wrath.",
    ),
    (
        "Mars_duration_edition_variant",
        "for two or three dayes",
        "The 1647 original explicitly says two or three DAYS; the separately typeset 1659 original prints two or three YEARS. Preserve both printed variants.",
    ),
    (
        "Saturn_ascending_mood",
        "If Saturn doe transit the degree ascending",
        "Saturn crossing natal Ascendant is associated with gravity, sobriety and melancholy in the historical text.",
    ),
    (
        "four_planets_favorable_days",
        "those dayes of the yeer are reputed fortunate",
        "Jupiter, Venus, Sun or Moon is alleged to indicate favorable days when in sextile/trine to nominated natal targets.",
    ),
    (
        "favorable_targets_asc_Mc",
        "degree ascending or culminating",
        "The Ascendant and Midheaven degrees are explicitly listed as natal targets for a benefic sextile/trine.",
    ),
    (
        "favorable_own_radix_places",
        "to their owne places in the Radix",
        "Favorable sextile/trine to the same planet's natal place is another stated condition.",
    ),
    (
        "Saturn_Mars_unfortunate_transits",
        "those dayes are said to be unsuccessfull",
        "Saturn or Mars bodily passing natal ascending or culminating degrees is labeled unfavorable.",
    ),
    (
        "malefic_natal_planet_targets",
        "places of Jupiter, Venus, Sun, or Moon, or South Node",
        "The text also labels Saturn/Mars bodily passing natal Jupiter, Venus, Sun, Moon and descending Node as unfavorable.",
    ),
    (
        "malefic_square_opposition",
        "by Square or Opposition to them",
        "Square or opposition from Saturn/Mars to the listed natal places likewise receives the text's unfavorable-day label.",
    ),
    (
        "source_composition_timestamp",
        "Finither die 7.25 P.M. 14. August 1647.",
        "The original book gives an August 14 1647 closing time and planetary-hour reference: a composition note, not a tested transit outcome.",
    ),
    (
        "boundary_CLXXV_nativity",
        "C H A P. C L X X V.",
        "The original next folio742/PDF776 begins distinct CLXXV, the nativity of an English merchant, closing the physical CLXXIIII transits chapter.",
    ),
]
assert len(CLAIMS) == 22


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def save(p: Path, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def produce():
    idx = load(WEST)
    china = load(CHINA)
    before = load(PARENT / "RULES.json")
    checkpoint = load(B / "RECOVERY_CHECKPOINT.json")
    finding = B / "SECONDARY_SEARCH_NAVIGATOR_TRANSITS.txt"
    text = finding.read_text(encoding="utf-8")
    assert sha(finding) == SECONDARY_SHA and len(text) == 1884
    assert idx["records_count"] == 12846 and idx["batches"][-1]["id"] == "B07av"
    assert idx["next"]["pdf_page"] == 775 and idx["next"]["chapter"] == "CLXXIV"
    assert idx["next"]["printed_chapter_numeral"] == "CLXXIIII"
    assert before["last_record"] == "R12846"
    assert before["next_record"] == "R12847"
    assert china["sum_source_annotations"] == 355
    assert checkpoint["prior_verified_Lilly_historical_records"] == 12846
    assert checkpoint["source_baseline_sha"] == "044bf9ef6012c9e4488aa100d2bac442a29b2c6c"
    assert idx["source_sha256"] == SOURCE_SHA
    photos = {
        "first_edition_transit": PARENT / "evidence/1647_original_775-775.jpg",
        "second_edition_transit": PARENT / "evidence/independent_1659_djvu770.jpg",
        "first_edition_next_CLXXV": B / "evidence/original_1647_pdf776-776.jpg",
        "second_edition_next_CLXXV": B / "evidence/independent_1659_djvu771.jpg",
    }
    photographic = {}
    for name, path in photos.items():
        assert path.exists() and path.stat().st_size > 200_000, (name, path)
        photographic[name] = {
            "path": str(path.relative_to(ROOT)),
            "SHA256": sha(path),
            "exact_bytes": path.stat().st_size,
            "source_year": 1647 if name.startswith("first_") else 1659,
            "original_printed_folio": 741 if name.endswith("transit") else 742,
            "PDF_frame_or_DjVu_frame": 775
            if name == "first_edition_transit"
            else (
                770
                if name == "second_edition_transit"
                else 776
                if name == "first_edition_next_CLXXV"
                else 771
            ),
        }
    entries = []
    for i, (role, needle, meaning) in enumerate(CLAIMS):
        at = text.find(needle)
        assert at >= 0, (role, needle)
        r = {
            "id": f"R{12847 + i}",
            "record_number": 12847 + i,
            "batch": "B07aw",
            "original_1647_printed_chapter_numeral": "CLXXIIII",
            "independent_1659_printed_chapter_numeral": "CLXXIV",
            "editorial_sequence_ordinal": 174,
            "first_edition_original_pdf_frame": 775,
            "original_printed_folio": 741,
            "source_section_role": role,
            "derivative_locator_NOT_original_transcription": needle,
            "secondary_text_absolute_within_excerpt_offset": at,
            "secondary_anchor_utf8_sha256": hashlib.sha256(needle.encode()).hexdigest(),
            "source_historical_meaning_ONLY": meaning,
            "source_first_edition_original_photo_SHA256": photographic["first_edition_transit"][
                "SHA256"
            ],
            "source_second_edition_original_photo_SHA256": photographic["second_edition_transit"][
                "SHA256"
            ],
            "source_one_reader_original_printing_observation": True,
            "source_critical_two_independent_human_readers_verified": False,
            "full_ephemeris_calendar_natal_transits_engine_verified": False,
            "historical_health_mood_money_relationship_claims_empirically_validated": False,
            "source_predictions_tested_on_independent_human_cohort": False,
            "runtime_model_promoted": False,
        }
        if role == "Jupiter_Venus_on_ascendant":
            r["original_1647_and_1659_first_source_planets"] = ["Jupiter", "Venus"]
            r["secondary_searchable_text_wrong_planets"] = ["Jupiter", "Mars"]
            r["literal_original_matches_secondary_text"] = False
        if role == "Mars_duration_edition_variant":
            r["original_first_1647_duration_unit"] = "dayes"
            r["original_second_1659_duration_unit"] = "yeares"
            r["duration_magnitude_in_both_original_editions"] = [2, 3]
            r["edition_variation_does_not_demonstrate_actual_effect"] = True
        if role == "boundary_CLXXV_nativity":
            r["next_original_1647_pdf_frame"] = 776
            r["next_independent_1659_djvu_frame"] = 771
            r["next_printed_chapter_numeral"] = "CLXXV"
            r["source_next_chapter_first_substantive_record_NOT_yet_accepted"] = True
        entries.append(r)
    assert [r["record_number"] for r in entries] == list(range(12847, 12869))
    src = {
        "schema": "LILLY_1647_1659_CLXXIIII_CLXXIV_TRANSIT_EDITION_SOURCE_V1",
        "batch": "B07aw",
        "physical_original_1647_chapter_printed": "CLXXIIII",
        "independently_typeset_1659_original_printed": "CLXXIV",
        "editorial_normalized_ordinal": 174,
        "original_1647_transit_one_page_pdf_frame": 775,
        "original_1647_transit_one_page_printed_folio": 741,
        "original_1647_next_distinct_CLXXV_pdf_frame": 776,
        "independent_1659_transit_djvu_frame": 770,
        "independent_1659_next_CLXXV_djvu_frame": 771,
        "source_original_1647_full_book_pdf_sha256": SOURCE_SHA,
        "original_photo_witnesses": photographic,
        "non_authoritative_searchable_text_sha256": SECONDARY_SHA,
        "two_printed_editions_distinct_Mars_ascendant_duration_units": True,
        "1647_printed_Mars_ascendant_duration": "2 or 3 days",
        "1659_printed_Mars_ascendant_duration": "2 or 3 years",
        "original_1647_1659_Jupiter_or_Venus_ascendant_not_secondary_Jupiter_or_Mars": True,
        "original_1647_1659_ascendant_planets": ["Jupiter", "Venus"],
        "non_authoritative_secondary_planet_names": ["Jupiter", "Mars"],
        "date_of_source_closing_signature": "14 August 1647, planetary hour Venus; date reflects printed book composition statement only",
        "source_all_original_chapter_physical_pages_examined": True,
        "source_critical_professional_collation_complete": False,
        "original_epoch_solar_and_transit_ephemeris_validated": False,
        "chart_derived_human_event_prediction_accuracy_validated": False,
        "independent_real_human_predictions_validated": 0,
        "runtime_promotions": 0,
        "source_historical_record_count": len(entries),
        "first_historical_record": entries[0]["id"],
        "last_historical_record": entries[-1]["id"],
        "next_record": "R12869",
        "next_original_1647_pdf_frame": 776,
        "next_original_first_edition_printed_folio": 742,
        "records": entries,
    }
    save(B / "ORIGINAL_CLXXIV_TRANSITS_TWO_EDITIONS_SOURCE_V1.json", src)
    rulefile = B / "RULES.json"
    rules = {
        "batch": "B07aw",
        "status": "ORIGINAL_1647_ONE_PAGE_TRANSITS_CHAPTER_PHYSICALLY_COVERED_WITH_EDITION_VARIANTS",
        "source_only_historical_notes": True,
        "record_count": len(entries),
        "first_record": entries[0]["id"],
        "last_record": entries[-1]["id"],
        "source_groups": 1,
        "body_pdf_frames": [775],
        "source_original_chapter_first_1647": "CLXXIIII",
        "source_original_chapter_second_1659": "CLXXIV",
        "normalized_editorial_ordinal": 174,
        "physical_chapter_CLXXIV_source_span_covered": True,
        "critical_edition_professional_corroboration_complete": False,
        "empirical_person_outcome_predictions_validated": 0,
        "runtime_promotions": 0,
        "rules": [
            {
                "id": r["id"],
                "record_number": r["record_number"],
                "batch": "B07aw",
                "source_span": "B07aw-S001",
                "original_pdf_frames": [775],
                "source_role": r["source_section_role"],
                "source_anchor_NOT_diplomatic": r["derivative_locator_NOT_original_transcription"],
                "historical_meaning_ONLY": r["source_historical_meaning_ONLY"],
                "original_1647_1659_print_variation_preserved": r["source_section_role"]
                in ("Mars_duration_edition_variant", "Jupiter_Venus_on_ascendant"),
                "source_only_photographic_evidence_attested_by_one_reader": True,
                "independent_human_mood_health_wealth_prediction_validated": False,
                "natal_ephemeris_and_timing_method_verified": False,
                "runtime_model_promoted": False,
            }
            for r in entries
        ],
    }
    save(rulefile, rules)
    acceptance = {
        "batch": "B07aw",
        "Lilly_before": 12846,
        "Ptolemy_retained": 1066,
        "Chinese_V7_retained": 355,
        "new_historical_source_annotations": len(entries),
        "Lilly_after_if_accepted": 12868,
        "Western_after_if_accepted": 13934,
        "next_original_R": "R12869",
        "next_original_PDF": 776,
        "next_original_printed_folio": 742,
        "next_chapter_original_printed": "CLXXV",
        "next_chapter_editorial_ordinal": 175,
        "next_chapter_heading": "The NATIVITY of an English Merchant Astrologically handled",
        "original_1647_transit_source_physical_span_complete": True,
        "professional_two_reader_critical_print_collation_complete": False,
        "source_Mars_two_or_three_days_versus_years_variant_preserved": True,
        "source_Asc_Jupiter_Venus_not_derived_text_Mars": True,
        "observed_human_prediction_accuracy_validated": False,
        "actual_transit_ephemeris_timing_engine_verified": False,
        "source_SHA256": sha(B / "ORIGINAL_CLXXIV_TRANSITS_TWO_EDITIONS_SOURCE_V1.json"),
        "rules_SHA256": sha(rulefile),
        "independent_human_predictions_validated": 0,
        "runtime_promotions": 0,
    }
    save(B / "ACCEPTANCE.json", acceptance)
    print(
        json.dumps(
            {
                "source_notes": len(entries),
                "original_first_1647_mars_duration": "days",
                "original_1659_mars_duration": "years",
                "Asc_Jupiter_Venus_original_only": True,
                "next": acceptance["next_original_R"],
                "source_sha256": acceptance["source_SHA256"],
                "rules_sha256": acceptance["rules_SHA256"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    produce()
