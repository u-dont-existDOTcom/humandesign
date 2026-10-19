#!/usr/bin/env python3
"""Pin original printed CLXVIII source conditions separately from predictions."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def save(file, x):
    Path(file).write_text(json.dumps(x, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build():
    notes = j(B / "CLXVIII_ORIGINAL_SOURCE_JUDGMENT_33_NOTES_V1.json")
    west = j(INDEX)
    china = j(CHINA)
    assert west["records_count"] == 12671
    assert west["batches"][-1]["id"] == "B07ao"
    assert west["next"]["chapter"] == "CLXVIII" and west["next"]["pdf_page"] == 760
    assert china["sum_source_annotations"] == 355
    assert notes["source_doc_record_count"] == 33
    assert len(notes["rows"]) == 33
    assert notes["source_next_CHAP_CLXIX_first_printed_PDF"] == 763
    assert notes["original_full_Wellcome_1647_PDF_SHA256"] == west["source_sha256"]
    assert notes["human_predictions_validated"] == notes["runtime_promotions"] == 0
    assert not notes["full_expert_diplomatic_comparison_completed"]
    image_proofs = {}
    for key, value in notes["image_sources"].items():
        file = B / value["source_relative_file"]
        assert file.is_file(), file
        assert sha(file) == value["sha256"], file
        assert file.stat().st_size > 160000
        image_proofs[key] = {
            "relative_file": value["source_relative_file"],
            "original_folio": value["printed_page"],
            "photo_sha256": sha(file),
            "source_exact_bytes": file.stat().st_size,
        }
    original = notes["source_example"]
    assert original["radical_pisces_degrees_minutes"] == [6, 37]
    assert original["full_sign_degrees_minutes"] == [30, 0]
    assert original["remainder_degrees_minutes"] == [23, 23]
    assert original["degree_table_23_d_h_m"] == [280, 0, 27]
    assert original["minute_table_23_d_h_m"] == [4, 16, 1]
    assert original["printed_combined_time_d_h_m"] == [284, 16, 28]
    assert original["first_lord_until_calendar_date"] == "June 29"
    assert original["second_lord_through_calendar_date"] == "September 19"
    assert (30 * 60 - (6 * 60 + 37)) == 23 * 60 + 23
    assert (280 * 1440 + 27) + (4 * 1440 + 16 * 60 + 1) == 284 * 1440 + 16 * 60 + 28

    ordered = []
    for k, source in enumerate(notes["rows"]):
        assert source["id"] == f"R{12672 + k}"
        assert source["source_original_pdf_frame"] in (760, 761, 762, 763)
        assert source["source_original_corresponding_second_1659_DjVu_frame"] == (
            source["source_original_pdf_frame"] - 5
        )
        assert source["source_one_reader_locator_not_diplomatic"]
        assert source["source_historical_interpretation_only"]
        assert source["real_human_predictive_success"] is False
        assert source["runtime_promoted"] is False
        ordered.append(
            {
                "id": source["id"],
                "record_number": 12672 + k,
                "batch": "B07ap",
                "source_span": f"B07ap-S{source['source_original_pdf_frame'] - 759:03d}",
                "original_pdf_frames": [source["source_original_pdf_frame"]],
                "source_original_printed_folio": source["source_original_printed_folio"],
                "role": source["role"],
                "source_anchor_not_diplomatic": source["source_one_reader_locator_not_diplomatic"],
                "historical_meaning_only": source["source_historical_interpretation_only"],
                "historical_one_reader_photo_documented": True,
                "original_full_birth_calendar_engine_validated": False,
                "original_1647_health_or_morality_prediction_validated": False,
                "independent_untouched_actual_human_validation": False,
                "runtime_model_promoted": False,
            }
        )
    rules = {
        "batch": "B07ap",
        "status": "LILLY_CLXVIII_1647_ORIGINAL_PROFECTION_YEAR_LORD_INTERPRETATION_SOURCE",
        "record_count": 33,
        "first_record": "R12672",
        "last_record": "R12704",
        "source_groups": 4,
        "body_pdf_frames": [760, 761, 762, 763],
        "original_printed_CLXVIII_source_physical_span_read": True,
        "full_independent_original_edition_philology_verified": False,
        "original_1647_full_natal_year_engine_validated": False,
        "human_predictions_validated": 0,
        "runtime_promotions": 0,
        "rules": ordered,
    }
    save(B / "RULES.json", rules)
    witness = {
        "batch": "B07ap",
        "original_1647_source_full_PDF_sha256": notes["original_full_Wellcome_1647_PDF_SHA256"],
        "original_first_and_second_printings_preserved": True,
        "full_image_sha_and_exact_bytes": image_proofs,
        "old_astrological_year_ruler_sample": original,
        "original_ancient_context_historical_not_real_life_validated": True,
        "source_exact_excerpt_philologist_double_checked": False,
        "independent_human_prediction_success": 0,
        "runtime_promotions": 0,
    }
    save(B / "ORIGINAL_PHOTOGRAPHIC_WITNESS_V1.json", witness)
    acc = {
        "batch": "B07ap",
        "Lilly_before": 12671,
        "Ptolemy_retained": 1066,
        "Chinese_V7_retained": 355,
        "new_historical_source_notes": 33,
        "Lilly_if_accepted": 12704,
        "Western_if_accepted": 13770,
        "next_R": "R12705",
        "next_source_PDF": 763,
        "next_source_printed_folio": 729,
        "next_source_printed_chapter": "CLXIX",
        "original_CLXVIII_physical_coverage_completed": True,
        "original_CLXVIII_philological_critical_edition_verified": False,
        "actual_astrology_calendar_model_verified": False,
        "records_sha256": sha(B / "CLXVIII_ORIGINAL_SOURCE_JUDGMENT_33_NOTES_V1.json"),
        "witness_sha256": sha(B / "ORIGINAL_PHOTOGRAPHIC_WITNESS_V1.json"),
        "rules_sha256": sha(B / "RULES.json"),
        "human_prediction_validations": 0,
        "runtime_promotions": 0,
    }
    save(B / "ACCEPTANCE.json", acc)
    print(
        json.dumps(
            {
                "historical_text_records": len(ordered),
                "original_first_and_second_print_images": len(image_proofs),
                "source_example_year_remainder": original["printed_combined_time_d_h_m"],
                "source_next_record": acc["next_R"],
                "next_chapter": acc["next_source_printed_chapter"],
                "records_SHA256": acc["records_sha256"],
                "rules_SHA256": acc["rules_sha256"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    build()
