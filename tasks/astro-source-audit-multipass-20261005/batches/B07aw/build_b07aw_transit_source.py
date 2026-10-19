#!/usr/bin/env python3
"""Preserve original 1647 & independently typeset 1659 single-page transit source.

SOURCE-ONLY. This is an informed photographic reading of historic beliefs,
not evidence that an actual person has a predicted transit event. The 1647
'days' / 1659 'years' disagreement is a MATERIAL independent-edition variant
and MUST NOT be silently reconciled with a secondary transcription.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = ROOT / "tasks/astro-source-audit-multipass-20261005"
INDEX = TASK / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
OLDER = TASK / "batches/B07av"
FIRST_ORIGINAL = OLDER / "evidence/1647_original-775.jpg"
SECOND_PRINT = OLDER / "evidence/1659_original_djvu_770.jpg"

# Each source sentence is a distinct, historically testable CONDITION or
# documentary boundary, not a successful prognosis. Literal anchors are
# short photograph-confirmed snippets; their English summaries are glosses.
CLAIMS = [
    (
        "original_chapter_number_and_title",
        "CHAP. CLXXIIII.",
        "The first 1647 printing heads this transit section CLXXIIII; the "
        "separately typeset 1659 edition prints CLXXIV. Both call it "
        "'Of the TRANSIT of the Planets.'",
        "Physical separate chapter after radix-return material, original "
        "printed741; distinct later editorial ordinal 174.",
    ),
    (
        "ephemeris_calendar_lookup",
        "best found out by an Ephemeris",
        "Lilly directs the astrologer to an ephemeris to find which day of "
        "each month a moving planet transits a natal reference.",
        "A specified dated ephemeris and the natal radix/chart are necessary.",
    ),
    (
        "transit_over_house_cusps",
        "cusps of the houses of the Radicall Figure",
        "Actual planetary bodies passing natal house cusps are described as transit triggers.",
        "All natal house cusps and time-dependent planetary positions must "
        "be calculated independently; house system is not established here.",
    ),
    (
        "transit_over_natal_planets",
        "wherein any of the seven Planets",
        "Planetary transit can contact the degree of one of the seven planets recorded at birth.",
        "The historical seven visible bodies only, natal positions frozen.",
    ),
    (
        "transit_over_nodes_fortuna",
        "or was in at the Birth",
        "The text includes symbols for the lunar nodes and Part of Fortune "
        "among degrees to inspect at birth.",
        "Retain original glyph/source context; do not equate textual mention "
        "to a correctly calculated natal placement.",
    ),
    (
        "transit_aspects_house_cusps",
        "behold any of those cusps",
        "The source also counts a transiting body's aspect to a natal "
        "house cusp, not just direct bodily passage.",
        "Requires independently calculable exact aspect angle and orb; "
        "the source does not supply orb tolerances in this section.",
    ),
    (
        "transit_aspects_natal_planets",
        "the degrees wherein the Planets were",
        "The source includes aspects by a transiting body to natal planet degrees.",
        "Requires the planetary targets fixed independently of outcomes.",
    ),
    (
        "original_aspect_kind_dexter_sinister",
        "dexter or sinister",
        "The listed aspects include sextile, trine, square and opposition "
        "with dexter/sinister distinctions.",
        "Keep the historical aspect direction convention; do not invent "
        "an aspect-orb rule or modern quantified reliability.",
    ),
    (
        "jupiter_venus_ascendant_favorable",
        "healthfull, cheerfull",
        "Lilly claims a Jupiter or Venus passage over the radix "
        "ascendant signals a cheerful, successful day.",
        "Historical subjective/health and success claim only, no measured individual outcome.",
    ),
    (
        "ascendant_body_actions_rationale",
        "ascendent signifies the actions of the Body",
        "The stated rationale for the ascendant reading connects it with bodily action.",
        "Historical symbolic correspondence, not biomedical evidence.",
    ),
    (
        "jupiter_venus_second_house_money",
        "to buy any Commodity",
        "Jupiter/Venus crossing the natal second cusp is deemed a day "
        "to acquire money or purchase goods.",
        "No actual money, market behavior or financial outcome validated.",
    ),
    (
        "third_house_good_neighbours",
        "Kindred or good Neighbours",
        "Lilly assigns favorable effects from kin or neighbors to a "
        "Jupiter/Venus good transit of the natal third house.",
        "Historical family/social claim, not verified interpersonal behavior.",
    ),
    (
        "third_house_journeys",
        "upon any Journey",
        "The same third-house passage/aspect is presented as an appropriate time for travel.",
        "No travel outcome, distance or safety accuracy established.",
    ),
    (
        "third_house_aspect_not_only_body",
        "behold it with a good aspect",
        "The third-house benefit can follow a 'good aspect', not only "
        "physical passage across the cusp.",
        "Do not substitute modern categories of favorable aspects without "
        "a traceable source convention.",
    ),
    (
        "analogy_to_other_houses",
        "all the rest of the houses",
        "The author extends the interpretive pattern to the remaining "
        "houses without specifying every outcome here.",
        "Explicitly broad/open texture; don't invent eleven additional "
        "detailed outcome predictions from this sentence.",
    ),
    (
        "mars_ascendant_choler_passion",
        "to Choler or Passion",
        "Mars passing the natal ascendant is alleged to provoke anger or an occasion for wrath.",
        "Old temperament language, NOT observed aggression or diagnosed mental-health status.",
    ),
    (
        "mars_ascendant_duration_edition_conflict",
        "for two or three dayes",
        "1647 literally prints 'for two or three dayes' whereas the 1659 "
        "printing literally reads 'for two or three years'.",
        "MATERIAL duration conflict (days vs years); neither is chosen "
        "as the true timing rule or human-tested.",
    ),
    (
        "saturn_ascendant_melancholy",
        "Gravity, to Sobernesse, to Melancholy",
        "Saturn crossing the natal ascending degree is alleged to lead "
        "to gravity, sobriety and melancholy.",
        "Old temperament assertion, not clinical depression assessment.",
    ),
    (
        "jupiter_venus_luminaries_favorable_aspects",
        "generally those dayes of the yeer are reputed fortunate",
        "The author treats days with Jupiter, Venus, Sun or Moon sextiles "
        "or trines to natal Ascendant/Midheaven as favorable.",
        "Four named bodies and specified aspect types; historic assertion.",
    ),
    (
        "favorable_natal_return_positions",
        "to their owne places in the Radix",
        "The same favorable classification includes transits/aspects to "
        "the named planets' own birth degrees.",
        "Separate the natal-return target from the angular-cusp target.",
    ),
    (
        "saturn_mars_unfavorable_angles",
        "said to be unsuccessefull",
        "Saturn or Mars crossing the rising or culminating degree is "
        "presented as a traditionally unfavorable date.",
        "Unverified event/health/financial conclusion.",
    ),
    (
        "saturn_mars_unfavorable_natal_targets",
        "the places of",
        "The same unfavorable classification extends to selected natal "
        "locations of Jupiter, Venus, Sun, Moon and a lunar node.",
        "The exact historically typeset glyph targets and direction need "
        "separate source treatment for calculation.",
    ),
    (
        "saturn_mars_square_opposition",
        "or by",
        "Squares and oppositions by Saturn/Mars to those birth locations "
        "are included in unfavorable transit judgments.",
        "The historical text gives no probability, formal falsification "
        "rule or independently measured effect.",
    ),
    (
        "end_of_author_transits_discussion",
        "Finiter",
        "The 1647 source transit discussion terminates at the foot of "
        "printed page741 with a dated authorial note.",
        "Source date/planetary-hour marks remain documentary provenance; "
        "this does not prove a correct chart calculation.",
    ),
    (
        "next_chapter_merchant_separate",
        "The NATIVITY of an English Merchant",
        "The next original printed page742/PDF776 begins distinct "
        "CHAP. CLXXV about an English merchant's nativity.",
        "Physical source boundary only, no merchants' factual biography "
        "or predictive-accuracy claim has been confirmed.",
    ),
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build() -> None:
    index = read(INDEX)
    china = read(CHINESE)
    conflict = read(B / "ORIGINAL_1647_1659_MARS_TRANSIT_DURATION_SOURCE_CONFLICT_V1.json")
    boundary = read(B / "ORIGINAL_NEXT_MERCHANT_NATIVITY_BOUNDARY_1647_1659_V1.json")
    assert index["records_count"] == 12845
    assert index["batches"][-1]["id"] == "B07av"
    assert index["next"]["pdf_page"] == 775
    assert index["next"]["editorial_source_sequence_ordinal"] == 174
    assert index["read_numbered_chapters"] == list(range(1, 174))
    assert china["sum_source_annotations"] == 355
    assert len(CLAIMS) == 25
    assert conflict["first_edition_quote_exact_span"] == "for two or three dayes"
    assert conflict["second_edition_quote_exact_span"] == "for two or three years"
    assert sha(FIRST_ORIGINAL) == conflict["original_first_edition_full_page_sha256"]
    assert sha(SECOND_PRINT) == conflict["original_second_edition_full_page_sha256"]
    assert sha(B / conflict["first_edition_source_crop"]) == conflict["first_crop_sha256"]
    assert sha(B / conflict["second_edition_source_crop"]) == conflict["second_crop_sha256"]
    assert sha(B / "evidence/1647_original-776.jpg") == boundary["new_first_edition_page_sha256"]
    assert (
        sha(B / "evidence/1659_original_djvu_771.jpg")
        == boundary["new_second_typeset_edition_page_sha256"]
    )
    assert boundary["first_edition_original_chapter_heading"].startswith("The NATIVITY")
    assert boundary["second_edition_original_chapter_numeral"] == "CLXXV"
    assert index["source_sha256"] == boundary["original_full_Wellcome_1647_pdf_sha256"]

    sources = {
        "first_1647_741": {
            "file": str(FIRST_ORIGINAL.relative_to(ROOT)),
            "original_pdf_frame": 775,
            "printed_folio": 741,
            "source_edition_year": 1647,
            "SHA256": sha(FIRST_ORIGINAL),
            "bytes": FIRST_ORIGINAL.stat().st_size,
        },
        "second_1659_741": {
            "file": str(SECOND_PRINT.relative_to(ROOT)),
            "original_djvu_frame": 770,
            "printed_folio": 741,
            "source_edition_year": 1659,
            "SHA256": sha(SECOND_PRINT),
            "bytes": SECOND_PRINT.stat().st_size,
        },
        "first_1647_742": {
            "file": (
                "tasks/astro-source-audit-multipass-20261005/batches/"
                "B07aw/evidence/1647_original-776.jpg"
            ),
            "original_pdf_frame": 776,
            "printed_folio": 742,
            "source_edition_year": 1647,
            "SHA256": boundary["new_first_edition_page_sha256"],
            "bytes": boundary["new_first_edition_page_bytes"],
        },
        "second_1659_742": {
            "file": (
                "tasks/astro-source-audit-multipass-20261005/batches/"
                "B07aw/evidence/1659_original_djvu_771.jpg"
            ),
            "original_djvu_frame": 771,
            "printed_folio": 742,
            "source_edition_year": 1659,
            "SHA256": boundary["new_second_typeset_edition_page_sha256"],
            "bytes": boundary["new_second_typeset_edition_page_bytes"],
        },
    }
    claims = []
    for i, (role, source_short_anchor, meaning, limits) in enumerate(CLAIMS):
        is_boundary = role == "next_chapter_merchant_separate"
        record = {
            "id": f"R{12846 + i}",
            "record_number": 12846 + i,
            "batch": "B07aw",
            "source_span": "B07aw-S002" if is_boundary else "B07aw-S001",
            "original_pdf_frames": [776] if is_boundary else [775],
            "original_printed_folio": 742 if is_boundary else 741,
            "original_printed_chapter_numeral": "CLXXV" if is_boundary else "CLXXIIII",
            "second_printed_chapter_numeral": "CLXXV" if is_boundary else "CLXXIV",
            "role": role,
            "source_short_photo_anchor_or_locator": source_short_anchor,
            "source_anchor_is_full_diplomatic_transcription": False,
            "historical_meaning_only": meaning,
            "source_preconditions_and_uncertainty": limits,
            "first_1647_original_source_image_SHA256": (
                sources["first_1647_742"]["SHA256"]
                if is_boundary
                else sources["first_1647_741"]["SHA256"]
            ),
            "second_1659_original_source_image_SHA256": (
                sources["second_1659_742"]["SHA256"]
                if is_boundary
                else sources["second_1659_741"]["SHA256"]
            ),
            "historical_source_documented_by_one_reader": True,
            "independent_source_expert_critical_edition_verified": False,
            "actual_birth_time_ephemeris_and_natal_house_engine_verified": False,
            "personal_mood_health_money_or_risk_predictions_validated": False,
            "independent_blinded_actual_human_predictive_accuracy_verified": False,
            "runtime_model_promoted": False,
        }
        if role == "mars_ascendant_duration_edition_conflict":
            record["first_printing_1647_literal_duration"] = "two or three dayes"
            record["second_printing_1659_literal_duration"] = "two or three years"
            record["source_duration_choice_prohibited_without_new_evidence"] = True
        claims.append(record)
    assert [r["record_number"] for r in claims] == list(range(12846, 12871))
    assert sum(r["role"] == "mars_ascendant_duration_edition_conflict" for r in claims) == 1
    body = {
        "schema": "LILLY_1647_1659_ORIGINAL_TRANSIT_SOURCE_DOCUMENTARY_25_V1",
        "batch": "B07aw",
        "first_source_chapter_original_1647": "CLXXIIII",
        "second_source_chapter_original_1659": "CLXXIV",
        "original_editions_both_title": "Of the TRANSIT of the Planets.",
        "first_source_pdf_frame": 775,
        "first_source_printed_folio": 741,
        "physical_source_continues_into_next_chapter_only_on_pdf776": True,
        "next_distinct_source_original_printed_chapter": "CLXXV",
        "next_distinct_source_heading": boundary["first_edition_original_chapter_heading"],
        "photo_evidence": sources,
        "original_1647_1659_transit_duration_conflict_SHA256": sha(
            B / "ORIGINAL_1647_1659_MARS_TRANSIT_DURATION_SOURCE_CONFLICT_V1.json"
        ),
        "original_next_merchant_source_boundary_SHA256": sha(
            B / "ORIGINAL_NEXT_MERCHANT_NATIVITY_BOUNDARY_1647_1659_V1.json"
        ),
        "old_Lilly_historical_records": 12845,
        "old_Ptolemy_historical_records": 1066,
        "parallel_Chinese_V7_historical_records": 355,
        "new_source_documentary_rule_count": len(claims),
        "next_unaccepted_source_record": "R12871",
        "next_original_pdf_frame": 776,
        "first_1647_source_physically_covered": True,
        "historical_source_first_1647_complete_expert_diplomatic_collation": False,
        "source_validated_against_actual_human_transit_outcomes": False,
        "modern_calendar_ephemeris_natal_house_parity_validated": False,
        "independent_blinded_real_people_predictions_validated": 0,
        "runtime_astrological_rule_promotions": 0,
        "records": claims,
    }
    path = B / "CLXXIIII_TRANSITS_ORIGINAL_1647_1659_25_SOURCE_NOTES_V1.json"
    write(path, body)
    rules = {
        "batch": "B07aw",
        "status": "ONE_PHYSICAL_SOURCE_TRANSITS_CLXXIIII_1647_CLXXIV_1659",
        "record_count": len(claims),
        "first_record": "R12846",
        "last_record": "R12870",
        "source_groups": 2,
        "body_pdf_frames": [775, 776],
        "original_chapter_physical_source_covered": True,
        "1659_source_days_vs_years_conflict_preserved": True,
        "actual_person_event_validation_count": 0,
        "runtime_promotions": 0,
        "rules": claims,
    }
    write(B / "RULES.json", rules)
    accept = {
        "batch": "B07aw",
        "Lilly_before": 12845,
        "Ptolemy_retained": 1066,
        "Chinese_V7_retained": 355,
        "historical_annotations_added": len(claims),
        "Lilly_after_if_admitted": 12870,
        "Western_after_if_admitted": 13936,
        "next_record": "R12871",
        "next_original_pdf_frame": 776,
        "next_original_printed_folio": 742,
        "next_source_chapter": "CLXXV",
        "next_editorial_chapter_ordinal": 175,
        "next_source_title": "The NATIVITY of an English Merchant Astrologically handled.",
        "transit_chapter_original_1647": "CLXXIIII",
        "transit_chapter_original_1659": "CLXXIV",
        "physical_source_transit_chapter_full_page_seen": True,
        "expert_fully_collated_diplomatic_editions": False,
        "actual_transit_event_predictive_accuracy_validated": False,
        "rules_SHA256": sha(B / "RULES.json"),
        "source_full_document_SHA256": sha(path),
        "human_predictive_validation_count": 0,
        "runtime_promotions": 0,
    }
    write(B / "ACCEPTANCE.json", accept)
    print(
        json.dumps(
            {
                "new_documentary_rules": len(claims),
                "source_edition_duration_conflict": "1647 days versus 1659 years",
                "following_merchant_original_page": 776,
                "next_historical_record": "R12871",
                "notes_SHA256": sha(path),
                "rules_SHA256": sha(B / "RULES.json"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    build()
