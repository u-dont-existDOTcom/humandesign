#!/usr/bin/env python3
"""Build bounded source-only first CLXXVI Manners documentary records.

Ten original first/second printed edition photographs are physical witnesses,
not independent observed persons. Preserve the author's explicitly NEGATIVE
blemish observation and the actual chapter divider at printed749, not 748.
"""

import hashlib
import json
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
SOURCE = B / "MANNERS_SOURCE_CANDIDATES_V1.json"
IMAGES = B / "ORIGINAL_PHOTO_WITNESS_V1.json"
CORRECTION = B / "CORRECTED_PHYSICAL_CHAPTER_BOUNDARY_V1.json"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def write(p, record):
    p.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def freeze():
    prior = j(WEST)
    parallel = j(CHINA)
    candidates = j(SOURCE)
    photographs = j(IMAGES)
    correction = j(CORRECTION)
    assert prior["records_count"] == 12900
    assert prior["batches"][-1]["id"] == "B07ax"
    assert prior["next"]["chapter"] == "CLXXVI" and prior["next"]["pdf_page"] == 779
    assert prior["read_numbered_chapters"] == list(range(1, 176))
    assert prior["read_headed_units_count"] == 91
    assert not prior["partial_numbered_chapters"]
    assert parallel["sum_source_annotations"] == 355
    assert candidates["proposed_count"] == len(candidates["records"]) == 40
    assert [r["id"] for r in candidates["records"]] == [f"R{x:05d}" for x in range(12901, 12941)]
    assert candidates["next_unaccepted_after_if_admitted"] == "R12941"
    assert photographs["original_1647_CLXXVI_ends_pdf783_printed749_before_next_divider"]
    assert photographs["source_next_printed_CLXXVII_Riches_starts_same_pdf783"]
    assert correction["source_photo_corrected_boundary"].startswith(
        "CLXXVI prose continues in first paragraph of printed749/PDF783"
    )
    assert len(photographs["source_1647_1659_page_photos"]) == 10
    witnesses = {}
    for key, photo in photographs["source_1647_1659_page_photos"].items():
        file = ROOT / photo["image_path"]
        assert file.is_file(), (key, file)
        assert sha(file) == photo["sha256"], key
        assert file.stat().st_size == photo["bytes"], key
        assert photo["single_reader_photo_inspected"]
        witnesses[key] = {
            "original_year": photo["original_public_domain_print_source_year"],
            "printed_folio": photo["original_printed_folio"],
            "source_file": photo["image_path"],
            "source_SHA256": photo["sha256"],
            "source_bytes": photo["bytes"],
        }
    classified = Counter(x["evidence_category"] for x in candidates["records"])
    assert classified["EXPLICIT_NEGATIVE_OBSERVATION"] == 1
    assert sum(r["source_printed_folio"] == 749 for r in candidates["records"]) == 2
    assert candidates["records"][-1]["evidence_category"] == "NEXT_CHAPTER_BOUNDARY"
    assert candidates["records"][-2]["evidence_category"] == "SOURCE_CHAPTER_END"
    assert candidates["records"][-2]["source_printed_folio"] == 749
    assert "I can find none." in candidates["records"][30]["historical_source_interpretation"]
    observations = []
    for i, proposal in enumerate(candidates["records"]):
        folio = proposal["source_printed_folio"]
        assert 745 <= folio <= 749
        assert proposal["id"] == f"R{12901 + i}"
        assert proposal["original_1647_PDF_frame"] == folio + 34
        assert proposal["original_1659_DjVu_frame"] == folio + 29
        first = witnesses[f"1647_printed_{folio}"]
        second = witnesses[f"1659_printed_{folio}"]
        row = {
            "id": proposal["id"],
            "record_number": 12901 + i,
            "batch": "B07ay",
            "source_span": f"B07ay-S{folio - 744:03d}",
            "original_pdf_frames": [folio + 34],
            "original_printed_folio": folio,
            "second_edition_printed_folio": folio,
            "second_edition_DjVu_frame": folio + 29,
            "historical_claim_category": proposal["evidence_category"],
            "role": proposal["role"],
            "source_anchor_not_diplomatic": proposal["source_anchor_not_diplomatic_quote"],
            "historical_source_paraphrase": proposal["historical_source_interpretation"],
            "source_and_interpretation_limits": proposal["limits"],
            "source_original_1647_photo_SHA256": first["source_SHA256"],
            "independently_typeset_1659_source_photo_SHA256": second["source_SHA256"],
            "source_one_informed_reader_not_blinded_human": True,
            "source_case_known_to_author": True,
            "source_historical_character_claim_empirically_validated": False,
            "source_actual_behavior_medical_morality_wealth_verified": False,
            "natal_1616_oldstyle_era_chart_engine_validated": False,
            "independently_real_person_predictive_validation": False,
            "high_stakes_real_person_risk_classification_authorized": False,
            "runtime_model_promoted": False,
        }
        if row["historical_claim_category"] == "EXPLICIT_NEGATIVE_OBSERVATION":
            row["literal_historical_author_observation"] = "I can find none."
            row["historical_author_observes_no_throat_mark"] = True
            row["negative_observation_must_not_be_recoded_as_success"] = True
        observations.append(row)
    assert len(observations) == 40
    assert observations[-1]["source_span"] == "B07ay-S005"
    historical = {
        "schema": "LILLY_1647_1659_CHAP_CLXXVI_MANNERS_40_ORIGINAL_SOURCE_NOTES_V1",
        "batch": "B07ay",
        "source_first_original_1647_full_Wellcome_PDF_SHA256": photographs[
            "source_full_Wellcome_1647_original_PDF_SHA256"
        ],
        "original_two_edition_photo_witness_file": "batches/B07ay/ORIGINAL_PHOTO_WITNESS_V1.json",
        "photo_witness_SHA256": sha(IMAGES),
        "physical_chapter_boundary_correction_SHA256": sha(CORRECTION),
        "source_original_first_printed_folios": [745, 746, 747, 748, 749],
        "source_original_first_PDF_frames": [779, 780, 781, 782, 783],
        "second_original_typeset_1659_DjVu_frames": [774, 775, 776, 777, 778],
        "source_first_and_second_edition_same_text_not_independent_persons": True,
        "source_author_already_knows_subject_of_example": True,
        "source_negative_throat_mark_observation_count": 1,
        "negative_observation_historical_literal": "I can find none.",
        "historical_claim_categories": dict(classified),
        "physically_distinct_CLXXVII_starts_same_final_folio749": True,
        "historical_annotations_added_if_accepted": len(observations),
        "first_historical_R": "R12901",
        "last_historical_R": "R12940",
        "next_historical_R": "R12941",
        "historical_original_first_printed_1616_chart_era_ephemeris_validated": False,
        "original_second_edition_full_independent_classical_expert_review": False,
        "independent_actual_human_forecast_validations": 0,
        "runtime_model_promotions": 0,
        "historical_source_records": observations,
    }
    doc = B / "ORIGINAL_1647_1659_MANNERS_40_SOURCE_NOTES_V1.json"
    write(doc, historical)
    rules = {
        "batch": "B07ay",
        "status": "ORIGINAL_1647_1659_MANNERS_CLXXVI_40_DOCUMENTARY_NOT_PREDICTIONS",
        "record_count": 40,
        "first_record": "R12901",
        "last_record": "R12940",
        "source_groups": 5,
        "body_pdf_frames": [779, 780, 781, 782, 783],
        "original_first_CLXXVI_physical_chapter_covered_through_folio749": True,
        "CLXXVII_Riches_begins_on_same_original_last_folio": True,
        "explicit_lilly_negative_throat_mark_observation_preserved": True,
        "historical_subject_known_to_author_not_blinded": True,
        "original_natal_era_ephemeris_and_biography_independently_verified": False,
        "empirical_real_human_outcomes_validated": 0,
        "runtime_promotions": 0,
        "rules": observations,
    }
    write(B / "RULES.json", rules)
    accept = {
        "batch": "B07ay",
        "prior_Lilly": 12900,
        "Ptolemy_retained": 1066,
        "Chinese_V7_retained": 355,
        "new_original_historical_annotations": 40,
        "Lilly_after_if_accepted": 12940,
        "Western_after_if_accepted": 14006,
        "next_original_R": "R12941",
        "next_original_pdf_frame": 783,
        "next_original_printed_folio": 749,
        "next_original_physically_distinct_chapter": "CLXXVII",
        "next_original_heading": "Of Riches",
        "original_1647_first_CLXXVI_source_end_folio749": True,
        "negative_lilly_observation_source_not_predictive_success": True,
        "source_critical_expert_collation_completed": False,
        "source_merchant_true_chart_independently_verified": False,
        "real_person_prediction_validations": 0,
        "runtime_promotions": 0,
        "photo_witness_SHA256": sha(IMAGES),
        "source_data_SHA256": sha(doc),
        "rules_SHA256": sha(B / "RULES.json"),
        "original_chapter_boundary_correction_SHA256": sha(CORRECTION),
    }
    write(B / "ACCEPTANCE.json", accept)
    print(
        json.dumps(
            {
                "proposed_original_historical_source_notes": 40,
                "first": "R12901",
                "last": "R12940",
                "next": "R12941",
                "1647_and_1659_original_photo_witnesses": 10,
                "last_CLXXVI_source_folio": 749,
                "explicit_source_negative_found": "I can find none.",
                "source_SHA256": accept["source_data_SHA256"],
                "rules_SHA256": accept["rules_SHA256"],
                "actual_human_outcome_predictive_successes": 0,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    freeze()
