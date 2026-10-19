#!/usr/bin/env python3
"""Build reversible source-only Merchant Nativity 1647/1659 CLXXV notes.

Original sources and second typeset editions are witness documents, NOT
actual-person out-of-sample prediction data. Keep printed historical values
and modern antiscion geometric arithmetic in distinct fields.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = ROOT / "tasks/astro-source-audit-multipass-20261005"
WEST = TASK / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
PROPOSED = B / "MERCHANT_NATIVITY_SOURCE_CANDIDATES_V1.json"
PHOTOS = B / "ORIGINAL_MERCHANT_1647_1659_PHOTO_CHECKPOINT_V1.json"
MERCURY = B / "MERCHANT_MERCURY_ANTISCION_ORIGINAL_EDITION_SOURCE_CONFLICT_V1.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    old = load(WEST)
    chinese = load(CHINA)
    proposed = load(PROPOSED)
    photos = load(PHOTOS)
    antiscion = load(MERCURY)
    assert old["records_count"] == 12870
    assert old["batches"][-1]["id"] == "B07aw"
    assert old["read_numbered_chapters"] == list(range(1, 175))
    assert old["read_headed_units_count"] == 90
    assert old["partial_numbered_chapters"] == []
    assert old["next"]["chapter"] == "CLXXV" and old["next"]["pdf_page"] == 776
    assert chinese["sum_source_annotations"] == 355
    assert proposed["entry_count"] == 30
    assert proposed["first_new_id"] == "R12871"
    assert proposed["last_new_id"] == "R12900"
    assert proposed["next_after"] == "R12901"
    assert photos["status"] == "PHOTO_CHECKPOINT_NOT_YET_CANONICAL_RULES"
    assert len(photos["original_source_photographic_witnesses"]) == 10
    assert photos["next_unaccepted_Lilly_R"] == "R12871"
    assert photos["original_1647_Wellcome_full_scan_sha256"] == old["source_sha256"]
    assert antiscion["analytic_7_body_reflection_matches"] == 6
    assert antiscion["analytic_7_body_reflection_mismatches"] == 1
    assert antiscion["original_minus_formula_arcminutes"] == -20
    assert antiscion["actual_person_outcomes_predicted_and_verified"] == 0
    for name, blob in photos["original_source_photographic_witnesses"].items():
        path = ROOT / blob["file"]
        assert path.is_file(), (name, path)
        assert sha(path) == blob["sha256"], name
        assert path.stat().st_size == blob["bytes"]
    hum = photos["temperament_source_table_and_author_qualifications"]
    assert hum["literal_first_edition_1647_folio743_counts"] == {
        "hot": 7,
        "moist": 6,
        "cold": 6,
        "drie": 7,
    }
    assert hum["author_already_knows_native_in_source_text"] is True
    scores = photos["original_1647_planetary_dignity_source_folio744_745"]
    assert len(scores) == 8
    assert [(r["body"], r["computed_source_net"]) for r in scores] == [
        ("Saturn", -4),
        ("Jupiter", 9),
        ("Mars", 12),
        ("Sun", -6),
        ("Venus", 16),
        ("Mercury", -3),
        ("Moon", 3),
        ("Part_of_Fortune", 0),
    ]
    for x in scores:
        assert (
            x["source_fortitude_points"] - x["source_debility_points"] == (x["computed_source_net"])
        )
    cases = []
    for i, r in enumerate(proposed["entries"]):
        folio = r["folio"]
        assert folio in (742, 743, 744, 745)
        assert r["proposed_id"] == f"R{12871 + i}"
        assert r["first_source_pdf_frame"] == folio + 34
        first = photos["original_source_photographic_witnesses"][f"1647_printed_{folio}"]
        second = photos["original_source_photographic_witnesses"][f"1659_printed_{folio}"]
        cases.append(
            {
                "id": r["proposed_id"],
                "record_number": 12871 + i,
                "batch": "B07ax",
                "source_span": f"B07ax-S{folio - 741:03d}",
                "original_pdf_frames": [folio + 34],
                "original_printed_folio": folio,
                "1659_independently_typeset_djvu_frame": folio + 29,
                "role": r["source_role"],
                "source_anchor_not_diplomatic": r["short_source_locator_not_diplomatic_quote"],
                "historical_meaning_only": r["historical_source_interpretation"],
                "source_original_1647_photo_SHA256": first["sha256"],
                "source_original_1659_photo_SHA256": second["sha256"],
                "original_1647_early_print_source_documented": True,
                "independent_classical_historian_critical_reading_verified": False,
                "historical_natal_chart_arithmetic_not_recomputed_from_ephemeris": True,
                "original_merchant_biography_independently_facts_checked": False,
                "known_person_retroactive_fit_is_not_blind_prediction": True,
                "high_stakes_mental_moral_health_fortune_personal_advice_permitted": False,
                "independent_real_human_prediction_accuracy_verified": False,
                "runtime_model_promoted": False,
            }
        )
    assert [r["record_number"] for r in cases] == list(range(12871, 12901))
    assert cases[-1]["role"] == "manner_chapter_divider"
    assert cases[-1]["original_printed_folio"] == 745
    rules = {
        "batch": "B07ax",
        "status": "ORIGINAL_FIRST_1647_CLXXV_MERCHANT_NATIVITY_30_HISTORICAL_SOURCE_CLAUSES",
        "record_count": len(cases),
        "first_record": "R12871",
        "last_record": "R12900",
        "source_groups": 4,
        "body_pdf_frames": [776, 777, 778, 779],
        "original_first_edition_merchant_section_source_physically_covered": True,
        "following_printed_CLXXVI_manners_separate_chapter": True,
        "merchant_case_known_to_Lilly_unblinded": True,
        "printed_humor_balance_not_same_as_later_manners": True,
        "printed_mercury_antiscia_20arcmin_discrepancy_kept_literal": True,
        "historical_epoch_birth_chart_ephemeris_verified": False,
        "original_source_critically_collated_by_independent_second_reader": False,
        "independent_actual_person_outcome_validations": 0,
        "runtime_promotions": 0,
        "rules": cases,
    }
    save(B / "RULES.json", rules)
    source = {
        "schema": "LILLY_B07ax_ORIGINAL_1647_1659_MERCHANT_NATIVITY_SOURCE_V1",
        "batch": "B07ax",
        "source_full_original_1647_pdf_sha256": old["source_sha256"],
        "original_first_ed_heading": (
            "CHAP. CLXXV. The NATIVITY of an English Merchant Astrologically handled."
        ),
        "original_second_ed_heading": (
            "CHAP. CLXXV. The NATIVITY of an English Merchant Astrologically handled."
        ),
        "original_first_ed_source_folios": [742, 743, 744, 745],
        "original_1647_photo_source_witness_sha256": sha(PHOTOS),
        "source_antiscion_arithmetic_conflict_SHA256": sha(MERCURY),
        "original_physical_source_photo_sha256s": {
            k: v["sha256"]
            for k, v in photos["original_source_photographic_witnesses"].items()
            if v["printed_folio"] <= 745
        },
        "historic_chart_input_source_only": photos["original_1647_chart_center_source_folio742"],
        "source_temperament_source_table_only": hum,
        "source_dignity_fortitude_debility_rows": scores,
        "source_7_planet_antiscia_values_as_printed_preserved": True,
        "source_6_antiscia_math_equal_one_mismatch_Mercury": True,
        "source_1647_Mercury_print_Pisces_26_06_not_silently_changed": True,
        "actual_known_person_case_not_independently_blinded": True,
        "hypothesized_personality_outcomes_not_experimentally_validated": True,
        "merchant_original_chart_accurately_computed_with_original_era_ephemeris": False,
        "manuscript_source_independently_critical_collated": False,
        "next_printed_chapter_after_this_source": "CLXXVI Of the Manners of the Native",
        "next_original_printed_chapter_on_same_folio": 745,
        "after_substantive_merchant_CLXXV_next_R": "R12901",
        "new_source_only_documentary_records": len(cases),
        "source_human_outcomes_validated": 0,
        "runtime_astrology_promotions": 0,
        "source_records": cases,
    }
    save(B / "ORIGINAL_1647_1659_MERCHANT_NATIVITY_30_SOURCE_NOTES_V1.json", source)
    accept = {
        "batch": "B07ax",
        "prior_Lilly": 12870,
        "Ptolemy_retained": 1066,
        "Chinese_V7_retained": 355,
        "source_historical_annotations_to_append": len(cases),
        "Lilly_after_if_admitted": 12900,
        "Western_after_if_admitted": 13966,
        "next_historical_R": "R12901",
        "next_original_PDF_frame": 779,
        "next_original_printed_folio": 745,
        "next_original_physically_distinct_chapter": "CLXXVI",
        "next_original_heading": "Of the Manners of the Native.",
        "source_printed_Mercury_antiscion_26_06_vs_arithmetic_26_26": True,
        "historical_original_merchant_excerpt_physically_covered": True,
        "independent_natal_human_chart_accuracy_verified": False,
        "actual_human_predictive_validations": 0,
        "runtime_promotions": 0,
        "rules_SHA256": sha(B / "RULES.json"),
        "source_notes_SHA256": sha(
            B / "ORIGINAL_1647_1659_MERCHANT_NATIVITY_30_SOURCE_NOTES_V1.json"
        ),
        "photo_witness_SHA256": sha(PHOTOS),
        "source_antiscion_critical_diagnostic_SHA256": sha(MERCURY),
    }
    save(B / "ACCEPTANCE.json", accept)
    print(
        json.dumps(
            {
                "new_source_records": len(cases),
                "first": rules["first_record"],
                "last": rules["last_record"],
                "next": accept["next_historical_R"],
                "source_photographs": len(photos["original_source_photographic_witnesses"]),
                "known_native_unblinded": True,
                "Mercury_20arcminute_diagnostic_unfixed": True,
                "source_document_sha256": accept["source_notes_SHA256"],
                "rules_sha256": accept["rules_SHA256"],
                "person_predictive_validations": 0,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
