#!/usr/bin/env python3
"""Build source-only Lilly CLXXIII 1647/1659 return-to-radix matrix.

This consolidates the 42 PHOTO-ATTESTED historical claims into contiguous
source-note identifiers. Original early printed source is not a validated
natal ephemeris or an independently evaluated real-life prediction system.
"""

import hashlib
import json
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = (
    ROOT / "tasks/astro-source-audit-multipass-20261005" / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
)
CHINESE = (
    ROOT / "tasks/astro-chinese-primary-sources-20261017" / "CHINESE_SOURCE_AUDIT_INDEX_V7.json"
)
MATRIX = B / "RADIX_RETURN_42_SOURCE_CLAIMS_PROVISIONAL_V1.json"
PHOTO = B / "PHOTO_CHECKPOINT_1647_1659_ORIGINAL_V1.json"
EDITION = B / "ORIGINAL_TRANSIT_NUMERAL_VARIANT_1647_VS_1659_V1.json"
SOURCE = B / "CLXXIII_42_ORIGINAL_1647_1659_SOURCE_WITNESS_V1.json"
RULES = B / "RULES.json"
ACCEPT = B / "ACCEPTANCE.json"

PLANETS = ("Saturn", "Jupiter", "Mars", "Venus", "Mercury", "Moon")
TARGETS = ("Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon")
EXPECTED_FOLIO_COUNTS = {738: 13, 739: 13, 740: 15, 741: 1}


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def build():
    original = j(MATRIX)
    photos = j(PHOTO)
    variant = j(EDITION)
    west = j(INDEX)
    chinese = j(CHINESE)

    assert west["records_count"] == 12803
    assert west["batches"][-1]["id"] == "B07au"
    assert west["next"]["pdf_page"] == 772
    assert west["next"]["chapter"] == "CLXXIII"
    assert west["read_numbered_chapters"] == list(range(1, 173))
    assert west["read_headed_units_count"] == 88
    assert west["partial_numbered_chapters"] == []
    assert chinese["sum_source_annotations"] == 355
    assert west["empirical_validations"] == west["runtime_promotions"] == 0
    assert original["source_matrix_cells"] == 42
    assert tuple(original["returning_planets"]) == PLANETS
    assert tuple(original["radix_target_planets"]) == TARGETS
    assert len(original["records"]) == 42
    assert variant["source_original_first_1647_literal_printed_heading"] == ("CHAP. CLXXIIII.")
    assert variant["source_second_1659_literal_printed_heading"] == ("CHAP. CLXXIV.")
    assert variant["editorial_chapter_ordinal"] == 174

    # All six first-edition source sections against seven natal targets.
    pairset = {(r["returning_planet"], r["radix_place_planet"]) for r in original["records"]}
    assert pairset == {(p, t) for p in PLANETS for t in TARGETS}
    assert len(pairset) == len(original["records"])
    assert (
        dict(Counter(r["original_1647_printed_folio"] for r in original["records"]))
        == EXPECTED_FOLIO_COUNTS
    )

    originals = photos["photo_witnesses"]
    assert len(originals) == 8
    for key, entry in originals.items():
        f = ROOT / entry["relative_repo_path"]
        assert f.is_file(), key
        assert f.stat().st_size == entry["bytes"]
        assert sha(f) == entry["sha256"]

    witness = []
    for printed in range(738, 742):
        first = originals[f"1647_{printed}"]
        second = originals[f"1659_{printed}"]
        assert first["original_printed_folio"] == printed
        assert second["original_printed_folio"] == printed
        assert first["original_scan_frame"] == printed + 34
        assert second["original_scan_frame"] == printed + 29
        witness.append(
            {
                "original_printed_folio": printed,
                "1647_original_pdf_frame": first["original_scan_frame"],
                "1647_source_file": first["relative_repo_path"],
                "1647_sha256": first["sha256"],
                "1659_original_djvu_frame": second["original_scan_frame"],
                "1659_source_file": second["relative_repo_path"],
                "1659_sha256": second["sha256"],
                "two_independently_typeset_editions_one_reader": True,
                "independently_blinded_second_human_reader": False,
            }
        )

    rules = []
    for i, claim in enumerate(original["records"]):
        planet = claim["returning_planet"]
        target = claim["radix_place_planet"]
        folio = claim["original_1647_printed_folio"]
        number = 12804 + i
        assert claim["provisional_original_source_annotation_id"] == f"R{number}"
        assert claim["original_relative_order_in_section"] == (
            sum(r["returning_planet"] == planet for r in original["records"][: i + 1])
        )
        first = originals[f"1647_{folio}"]
        second = originals[f"1659_{folio}"]
        assert not claim["runtime_model_promoted"]
        assert not claim["human_person_prediction_validation"]

        rules.append(
            {
                "id": f"R{number}",
                "record_number": number,
                "batch": "B07av",
                "source_span": f"B07av-S{folio - 737:03d}",
                "original_pdf_frames": [folio + 34],
                "original_printed_folio": folio,
                "printed_chapter_1647": "CLXXIII",
                "returning_revolution_planet": planet,
                "radix_natal_place_planet": target,
                "section_row_order": claim["original_relative_order_in_section"],
                "original_1647_source_photo_sha256": first["sha256"],
                "second_1659_source_photo_sha256": second["sha256"],
                "source_anchor_not_diplomatic": (
                    f"Of {planet}: returning to radix place {target}, "
                    f"source line {claim['original_relative_order_in_section']}"
                ),
                "historical_meaning_only": claim["source_historical_claim_paraphrase"],
                "source_conditional_qualifiers": claim["source_conditional_qualifiers"],
                "historical_domains_not_verified_event_outcomes": claim[
                    "source_interpretive_domains"
                ],
                "source_documented_one_reader": True,
                "independently_blinded_second_edition_text_expert_verified": False,
                "historical_personality_wealth_family_health_death_efficacy": False,
                "independent_real_event_prediction_validated": False,
                "natal_chart_ephemeris_true_solar_return_method_verified": False,
                "live_human_high_stakes_advice_authorized": False,
                "runtime_model_promoted": False,
            }
        )
    assert len(rules) == 42
    assert rules[0]["id"] == "R12804"
    assert rules[-1]["id"] == "R12845"
    assert rules[-1]["returning_revolution_planet"] == "Moon"
    assert rules[-1]["radix_natal_place_planet"] == "Moon"
    assert rules[-1]["original_printed_folio"] == 741

    doc = {
        "schema": "LILLY_CLXXIII_FIRST_SECOND_PRINT_42_RETURN_TO_RADIX_V1",
        "batch": "B07av",
        "original_full_1647_source_pdf_sha256": original["source_full_1647_book_sha256"],
        "historical_chapter": "CLXXIII",
        "1647_original_heading": original["first_printed_heading"],
        "original_1647_physical_span_printed_folios": [738, 739, 740, 741],
        "original_1647_physical_span_pdf_frames": [772, 773, 774, 775],
        "historical_returning_planets": list(PLANETS),
        "historical_radix_target_planets": list(TARGETS),
        "source_mapped_physical_positions": 42,
        "source_1647_1659_photo_page_witnesses": witness,
        "original_1647_to_1659_first_next_transit_chapter_heading_variant": j(EDITION),
        "original_1647_book_photo_text_reader_count": 1,
        "complete_expert_critical_edition_collation": False,
        "source_clause_matrix_sha256": sha(MATRIX),
        "original_photo_checkpoint_sha256": sha(PHOTO),
        "following_new_chapter_is_not_source_CLXXIII": True,
        "six_returning_planets_seven_radix_places_not_seven_returning": True,
        "source_old_1647_chart_mechanics_verified": False,
        "actual_real_human_prediction_validations": 0,
        "runtime_promotions": 0,
        "rows": original["records"],
    }
    save(SOURCE, doc)
    ledger = {
        "batch": "B07av",
        "status": "FIRST_PRINTED_CLXXIII_PHYSICAL_SOURCE_COVERAGE_ONLY",
        "record_count": len(rules),
        "first_record": "R12804",
        "last_record": "R12845",
        "source_groups": 4,
        "body_pdf_frames": [772, 773, 774, 775],
        "original_source_page_741_traverses_next_chapter_boundary": True,
        "source_next_1647_literal_heading": "CLXXIIII",
        "source_next_1659_literal_heading": "CLXXIV",
        "source_next_editorial_chapter_ordinal": 174,
        "physical_CLXXIII_text_covered": True,
        "complete_historical_source_expert_critical_edition": False,
        "historical_radix_return_chart_engine_verified": False,
        "independently_blinded_human_predicted_results": 0,
        "runtime_promotions": 0,
        "rules": rules,
    }
    save(RULES, ledger)
    accepted = {
        "batch": "B07av",
        "Lilly_before": 12803,
        "Ptolemy_retained": 1066,
        "Chinese_V7_retained": 355,
        "new_historical_annotations": 42,
        "Lilly_if_admitted": 12845,
        "Western_historical_if_admitted": 13911,
        "next_R": "R12846",
        "next_original_pdf_frame": 775,
        "next_original_printed_folio": 741,
        "next_1647_literal_chapter_numeral": "CLXXIIII",
        "next_1659_literal_chapter_numeral": "CLXXIV",
        "next_editorial_source_chapter_ordinal": 174,
        "next_chapter_heading": "Of the TRANSIT of the Planets.",
        "CLXXIII_physical_source_pages_completed": True,
        "expert_original_source_later_collation_needed": True,
        "radix_return_accurate_birth_engine_verified": False,
        "source_full_doc_sha256": sha(SOURCE),
        "source_original_candidate_matrix_sha256": sha(MATRIX),
        "source_photographic_manifest_sha256": sha(PHOTO),
        "rules_sha256": sha(RULES),
        "independent_human_predictive_results": 0,
        "runtime_astrology_model_promotions": 0,
    }
    save(ACCEPT, accepted)
    print(
        json.dumps(
            {
                "historical_rules": len(rules),
                "source_photo_pairs": len(witness),
                "original_1647_chapter": "CLXXIII",
                "separate_1647_next_roman": "CLXXIIII",
                "separate_1659_next_roman": "CLXXIV",
                "last": "R12845",
                "next": "R12846",
                "source_SHA256": sha(SOURCE),
                "rules_SHA256": sha(RULES),
                "human_predictions_validated": 0,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    build()
