#!/usr/bin/env python3
# ruff: noqa: E501  # Verbatim source labels retained for documentary reproducibility.
"""Freeze unpromoted 1647/1659 CLXXIII planetary-return matrix and CLXXIV boundary."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = "tasks/astro-source-audit-multipass-20261005"
INDEX = ROOT / TASK / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
PREP = B / "SOURCE_PHOTO_CHECKPOINT_V1.json"
CANDIDATE = B / "CLXXIII_42_SOURCE_CANDIDATES_V1.json"
SECONDARY = B / "SECONDARY_FINDING_AID_CLXXIII.txt"
PHRASES = {
    "Saturn": "Of SATURNE.",
    "Jupiter": "Of JUPITER.",
    "Mars": "Of MARS.",
    "Venus": "Of VENUS.",
    "Mercury": "Of MERCURY.",
    "Moon": "Of MOON.",
}
PLANETS = tuple(PHRASES)
TARGETS = {"Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"}


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def save(file, data):
    Path(file).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def freeze():
    prior = j(INDEX)
    chinese = j(CHINA)
    photo = j(PREP)
    candidate = j(CANDIDATE)
    text = SECONDARY.read_text(encoding="utf-8")
    assert prior["records_count"] == 12803
    assert prior["batches"][-1]["id"] == "B07au"
    assert prior["next"]["chapter"] == "CLXXIII" and prior["next"]["pdf_page"] == 772
    assert chinese["sum_source_annotations"] == 355
    assert candidate["candidate_42_historical_source_cases"] == 42
    assert len(candidate["records"]) == 42
    assert photo["status"] == "PHOTO_SOURCE_CHECKPOINT_ONLY_NOT_CANONICALLY_ACCEPTED"
    assert photo["prior_accepted_historical_Lilly_records"] == 12803
    assert sha(SECONDARY) == "8155673a9922eeeeb4af9d11680d55b038b08f2621b38bc54fd9a9085445fac0"
    begins = [text.index(x) for x in PHRASES.values()]
    assert begins == sorted(begins)
    for planet in PLANETS:
        rr = [r for r in candidate["records"] if r["revolution_planet"] == planet]
        assert len(rr) == 7, planet
        assert {r["natal_radix_target"] for r in rr} == TARGETS, planet
    manifest = {
        edition: {row["printed_folio"]: row for row in photos}
        for edition, photos in photo["source_original_visual_evidence"].items()
    }
    for edition, pages in manifest.items():
        assert set(pages) == {738, 739, 740, 741}
        for folio, r in pages.items():
            f = ROOT / r["repo_relative_file"]
            assert f.is_file() and f.stat().st_size == r["bytes"]
            assert sha(f) == r["sha256"], (edition, folio)
    all_records = []
    locators = []
    for i, r in enumerate(candidate["records"]):
        planet = r["revolution_planet"]
        idx = PLANETS.index(planet)
        source = text[begins[idx] : begins[idx + 1] if idx + 1 < len(begins) else len(text)]
        original_anchor = r["modern_secondary_locator_not_primary_quote"]
        n = source.count(original_anchor)
        assert n == 1, (planet, r["natal_radix_target"], n, original_anchor)
        relative = source.index(original_anchor)
        at = begins[idx] + relative
        page = r["first_edition_1647_printed_folio"]
        assert page in (738, 739, 740, 741)
        assert r["second_edition_1659_printed_folio"] == page
        assert r["second_edition_1659_DjVu_frame"] == page + 29
        assert r["first_edition_1647_PDF_frame"] == page + 34
        physical_1647 = manifest["first_edition_1647"][page]
        physical_1659 = manifest["independently_typeset_1659"][page]
        historical = {
            "id": f"R{12804 + i}",
            "record_number": 12804 + i,
            "batch": "B07av",
            "original_printed_chapter": "CLXXIII",
            "returning_planet": planet,
            "natal_radix_target": r["natal_radix_target"],
            "original_pdf_frames": [page + 34],
            "original_printed_folio": page,
            "source_first_1647_photo_sha256": physical_1647["sha256"],
            "source_independently_typeset_1659_photo_sha256": physical_1659["sha256"],
            "source_first_edition_photo_relative_path": physical_1647["repo_relative_file"],
            "source_second_edition_photo_relative_path": physical_1659["repo_relative_file"],
            "modern_secondary_text_locator_non_diplomatic": original_anchor,
            "secondary_search_position_relative_CLXXIII": at,
            "secondary_locator_utf8_sha256": hashlib.sha256(original_anchor.encode()).hexdigest(),
            "source_historical_meaning_only": r["source_historical_claim_paraphrase"],
            "source_original_natal_and_return_conditions": r[
                "explicit_source_conditions_or_limits"
            ],
            "source_read_by_one_nonblinded_reader_only": True,
            "source_first_and_second_edition_full_diplomatic_expert_review": False,
            "genuine_revolution_natal_chart_time_parity_verified": False,
            "independent_person_life_outcome_prediction_validated": False,
            "medical_legal_crime_morality_gender_finance_inference_authorized": False,
            "runtime_model_promoted": False,
        }
        all_records.append(historical)
        locators.append(
            {
                "id": historical["id"],
                "planet": planet,
                "natal_target": r["natal_radix_target"],
                "original_pdf_frame": page + 34,
                "first_1647_photo_sha256": physical_1647["sha256"],
                "original_1659_photo_sha256": physical_1659["sha256"],
                "finding_aid_offset": at,
                "finding_aid_fragment": original_anchor,
                "finding_aid_fragment_sha256": historical["secondary_locator_utf8_sha256"],
                "is_not_original_source_diplomatic_quote": True,
            }
        )
    assert len(all_records) == 42
    assert [r["record_number"] for r in all_records] == list(range(12804, 12846))
    heading_witness = {
        "schema": "LILLY_TWO_ORIGINAL_EDITION_CLXXIV_ROMAN_NUMERAL_VARIANT_V1",
        "boundary_original_first_ed_pdf_frame": 775,
        "boundary_original_printed_page": 741,
        "original_1647_literal_chapter_heading": "CHAP. CLXXIIII.",
        "independently_typeset_1659_literal_chapter_heading": "CHAP. CLXXIV.",
        "editorial_normalized_chapter_numeral": "CLXXIV",
        "source_first_original_1647_photo_sha256": manifest["first_edition_1647"][741]["sha256"],
        "source_second_original_1659_photo_sha256": manifest["independently_typeset_1659"][741][
            "sha256"
        ],
        "physical_boundary_below_last_Moon_own_place_statement": True,
        "independently_typeset_second_book_not_independent_human_predictions": True,
        "modern_original_1647_natal_chart_verified": False,
        "real_person_outcome_predictive_validations": 0,
    }
    save(B / "SOURCE_CLXXIV_ORIGINAL_TWO_EDITION_NUMERAL_V1.json", heading_witness)
    boundary = {
        "id": "R12846",
        "record_number": 12846,
        "batch": "B07av",
        "original_printed_chapter": "CLXXIII",
        "role": "physical_heading_boundary_next_clxxiv_transits",
        "literal_next_1647_printed_numeral": "CLXXIIII",
        "literal_next_1659_printed_numeral": "CLXXIV",
        "next_editorial_numeral": "CLXXIV",
        "original_pdf_frames": [775],
        "original_printed_folio": 741,
        "source_first_1647_photo_sha256": manifest["first_edition_1647"][741]["sha256"],
        "source_independently_typeset_1659_photo_sha256": manifest["independently_typeset_1659"][
            741
        ]["sha256"],
        "source_historical_meaning_only": (
            "Original Moon-on-Moon final conditional passage is followed by "
            "a horizontal divider, then separate CHAP CLXXIV, Of the Transit of the Planets."
        ),
        "original_source_cross_chapter_rule_inference_prohibited": True,
        "historical_source_documented": True,
        "independently_validated_person_prediction": False,
        "runtime_model_promoted": False,
    }
    rules = {
        "batch": "B07av",
        "status": "ORIGINAL_1647_AND_1659_CLXXIII_PLANETARY_RETURNS_FULL_PHYSICAL_SPAN_DOCUMENTED",
        "original_printed_chapter": "CLXXIII",
        "source_groups": 4,
        "body_pdf_frames": [772, 773, 774, 775],
        "record_count": 43,
        "historical_return_to_natal_cases": 42,
        "original_source_heading_stars": list(PLANETS),
        "Sun_is_natal_target_not_separate_return_heading": True,
        "first_record": "R12804",
        "last_record": "R12846",
        "next_record": "R12847",
        "next_printed_chapter": "CLXXIIII",
        "next_second_edition_printed_chapter": "CLXXIV",
        "next_editorial_normalized_chapter": "CLXXIV",
        "next_original_pdf_frame": 775,
        "chapter_source_physically_covered": True,
        "complete_expert_original_edition_critical_collation": False,
        "verified_natal_solar_revolution_time_engine": False,
        "verified_actual_person_fate_claims": 0,
        "runtime_promotions": 0,
        "rules": all_records + [boundary],
    }
    for key in (
        "source_first_edition_photo_relative_path",
        "source_second_edition_photo_relative_path",
    ):
        assert all((ROOT / r[key]).is_file() for r in rules["rules"][:42])
    save(B / "RULES.json", rules)
    report = {
        "schema": "LILLY_CLXXIII_ALL_42_HISTORICAL_RETURN_TO_RADIX_SOURCE_CASES_V1",
        "batch": "B07av",
        "historical_source": "Lilly Christian Astrology 1647 original printed738–741 and separate 1659 printed738–741",
        "first_1647_original_full_pdf_sha256": photo["full_1647_first_edition_pdf_sha256"],
        "original_photo_checkpoint_sha256": sha(PREP),
        "secondary_navigator_file_sha256": sha(SECONDARY),
        "returning_planet_headings_six": list(PLANETS),
        "natal_radix_target_names_seven": sorted(TARGETS),
        "source_return_to_radix_readings": 42,
        "source_total_new_documentary_notes_including_next_boundary": 43,
        "source_source_printed_page_span": [738, 739, 740, 741],
        "first_edition_second_typeset_print_source_images": 8,
        "original_chapter_CLXXIII_physically_finished": True,
        "expert_independent_second_human_source_reading_completed": False,
        "independent_original_birth_epoch_solar_return_chart_parity_verified": False,
        "actual_real_human_forecasts_validated": 0,
        "runtime_model_promotions": 0,
        "records": all_records,
        "physical_boundary_note": boundary,
        "original_next_heading_two_edition_witness_sha256": sha(
            B / "SOURCE_CLXXIV_ORIGINAL_TWO_EDITION_NUMERAL_V1.json"
        ),
    }
    save(B / "ORIGINAL_CLXXIII_42_RETURN_SOURCE_CASES_V1.json", report)
    provenance = {
        "schema": "CLXXIII_ORIGINAL_PRINT_1647_1659_43_SOURCE_PROOFS_V1",
        "batch": "B07av",
        "physical_printed_span": [738, 739, 740, 741],
        "first_and_second_original_images": manifest,
        "modern_secondary_text_sha256": sha(SECONDARY),
        "modern_secondary_is_only_navigation": True,
        "new_interpretation_count": 42,
        "source_chapter_divider_notes": 1,
        "source_all_42_anchors_exactly_once_within_own_returning_planet_section": True,
        "expert_diplomatic_source_corpus_review_completed": False,
        "human_prediction_validations": 0,
        "runtime_model_promotions": 0,
        "source_rule_locators": locators,
        "source_heading_witness_sha256": sha(
            B / "SOURCE_CLXXIV_ORIGINAL_TWO_EDITION_NUMERAL_V1.json"
        ),
    }
    save(B / "SOURCE_RULE_PROVENANCE_V1.json", provenance)
    accept = {
        "batch": "B07av",
        "prior_Lilly_source_annotations": 12803,
        "prior_Ptolemy_source_annotations": 1066,
        "Chinese_V7_historical_annotations_retained": 355,
        "new_documentary_source_records": 43,
        "Lilly_if_accepted": 12846,
        "Western_if_accepted": 13912,
        "old_CLXXIII_physical_chapter_closed": True,
        "next_original_source_R": "R12847",
        "next_original_pdf_frame": 775,
        "next_original_printed_folio": 741,
        "next_original_printed_chapter": "CLXXIIII",
        "next_second_edition_printed_chapter": "CLXXIV",
        "next_editorial_normalized_chapter": "CLXXIV",
        "next_heading": "Of the TRANSIT of the Planets",
        "historical_return_rules_from_six_planets": 42,
        "full_critical_source_edition_collected": False,
        "old_epoch_natal_to_return_chart_calculations_verified": False,
        "human_predictions_validated": 0,
        "runtime_promotions": 0,
        "rules_sha256": sha(B / "RULES.json"),
        "source_matrix_sha256": sha(B / "ORIGINAL_CLXXIII_42_RETURN_SOURCE_CASES_V1.json"),
        "source_provenance_sha256": sha(B / "SOURCE_RULE_PROVENANCE_V1.json"),
        "original_next_heading_variant_witness_sha256": sha(
            B / "SOURCE_CLXXIV_ORIGINAL_TWO_EDITION_NUMERAL_V1.json"
        ),
    }
    save(B / "ACCEPTANCE.json", accept)
    print(
        json.dumps(
            {
                "source_planet_headings": 6,
                "historical_source_cases": 42,
                "new_record_count": 43,
                "first": rules["first_record"],
                "last": rules["last_record"],
                "next": accept["next_original_source_R"],
                "next_physical_chapter": "CLXXIV",
                "rules_sha256": accept["rules_sha256"],
                "source_matrix_sha256": accept["source_matrix_sha256"],
                "source_provenance_sha256": accept["source_provenance_sha256"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    freeze()
