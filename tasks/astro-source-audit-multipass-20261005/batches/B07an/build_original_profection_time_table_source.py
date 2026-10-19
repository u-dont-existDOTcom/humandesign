#!/usr/bin/env python3
"""Original 1647 and separately typeset 1659 profection-time tables and cases.

Single informed reader source claims; pins eight whole original printed
images and checks exact arithmetic without pretending a verified historical
calendar engine or independently blinded personal event predictions.
"""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
DATA = B / "ORIGINAL_1647_1659_PROFECTION_TIME_TABLES_AND_CASES_V1.json"
PROOF = B / "SELECTED_ORIGINAL_PHOTO_ARITHMETIC_WITNESS_V1.json"
KNOWN = {
    "first_edition_pdf755": "712fee2a65ffafdc92d44aca2b11f03927d3872b880d93ca3bcd3b5ddc6fbb1d",
    "first_edition_pdf756": "f73b8619f1febd5fa15c670b56b3be2733fb8c1ba00288c5acd934fdf6994703",
    "first_edition_pdf757": "884098fadfc2200d18df10d556ca7567c31c3949b687abfeaa905b50acc7fe5e",
    "first_edition_pdf758": "2fb4b587c2e1d8eb5ec132db97183492d0102a08c59bb4538c518388523aed64",
    "second_edition_djvu750": "52d3ca6e9b387d645ad9dea9a184caa9bb4cd98aaf0013b03d7f95352e33490e",
    "second_edition_djvu751": "8cce3ceaf513dc19b5e782b1cfe20a6893d48a5799e23c6592662bf8079c1d7c",
    "second_edition_djvu752": "4c5ced505599a8bd5add98281067d3a4e98ca181c9c326239fafce0077fa9d4b",
    "second_edition_djvu753": "ab983b9ec5e3efa433a3e019f7008aceaa9fd360bae982dbff69fdb03ed70dd1",
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, a):
    path.write_text(json.dumps(a, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def minutes(x):
    assert len(x) == 3 and all(type(y) is int and y >= 0 for y in x)
    assert 0 <= x[1] < 24 and 0 <= x[2] < 60
    return (x[0] * 24 + x[1]) * 60 + x[2]


def dhm(m):
    assert type(m) is int and m >= 0
    return [m // 1440, (m // 60) % 24, m % 60]


def freeze():
    a = j(DATA)
    west = j(WEST)
    china = j(CHINA)
    assert west["records_count"] == 12625 and west["batches"][-1]["id"] == "B07am"
    assert west["next"]["pdf_page"] == 755 and west["next"]["chapter"] == "CLXVII"
    assert china["sum_source_annotations"] == 355
    assert a["proposed_source_record_count"] == 24
    assert a["source_full_30_and_60_digit_columns_critically_collated"] is False
    assert a["source_365day_month_table_all_cells_critically_collated"] is False
    assert a["independent_real_person_predictions_validated"] == 0
    photos = {}
    for label, entry in a["source_images"].items():
        path = B / entry["file"]
        assert path.is_file()
        assert sha(path) == KNOWN[label], (label, sha(path))
        assert path.stat().st_size > 200000
        entry["source_image_SHA256"] = KNOWN[label]
        entry["source_image_exact_bytes"] = path.stat().st_size
        photos[label] = {
            "file": entry["file"],
            "sha256": KNOWN[label],
            "bytes": path.stat().st_size,
        }
    select = {
        (r["table"], r["printed_label"]): r["first_edition_1647_time_dhm"]
        for r in a["source_sample_one_reader_table_rows"]
    }
    assert len(select) == 9
    assert select["degree", 1] == [12, 4, 12]
    assert select["minute", 60] == [12, 4, 13]
    assert minutes(select["minute", 60]) - minutes(select["degree", 1]) == 1
    assert select["minute", 23] == [4, 16, 1]
    assert select["minute", 37] == [7, 12, 11]
    outcomes = []
    for c in a["original_printed_1647_date_table_and_examples"]:
        assert (
            c["original_target"][0] * 60
            + c["original_target"][1]
            - c["original_ascendant"][0] * 60
            - c["original_ascendant"][1]
        ) == (c["printed_arc"][0] * 60 + c["printed_arc"][1])
        d = select["degree", c["printed_arc"][0]]
        assert d == c["source_degree_row_dhm"]
        if "source_minute_row" in c:
            assert c["source_minute_row"][0] == c["printed_arc"][1]
            m = select["minute", c["printed_arc"][1]]
            assert m == c["source_minute_row"][1:]
            assert dhm(minutes(d) + minutes(m)) == c["printed_total_dhm"]
        else:
            printed = c["printed_minute_row_actually_used"]
            correct = c["mathematically_corresponding_minute_row"]
            assert printed[0] == 37 and correct[0] == 23
            assert select["minute", 37] == printed[1:]
            assert select["minute", 23] == correct[1:]
            assert dhm(minutes(d) + minutes(printed[1:])) == c["printed_total_dhm"]
            assert (
                dhm(minutes(d) + minutes(correct[1:])) == (c["recalculated_total_using_23_row_dhm"])
            )
            assert (
                dhm(minutes(printed[1:]) - minutes(correct[1:]))
                == (c["difference_using_37_vs_23_row_dhm"])
            )
        outcomes.append(
            {
                "name": c["case"],
                "original_arc": c["printed_arc"],
                "original_total": c["printed_total_dhm"],
                "textual_date": c["printed_month_day"],
                "historical_first_second_prints_witnessed_by_one_reader": True,
                "event_occurred_in_real_life_verified": False,
            }
        )
    assert [x["original_total"] for x in outcomes] == [[17, 20, 34], [29, 10, 8], [80, 13, 21]]
    assert dhm(minutes([73, 1, 10]) + minutes([4, 16, 1])) == [77, 17, 11]
    assert a["next_source_id"] == "R12650"
    assert [r["planned_id"] for r in a["source_notes"]] == [f"R{i}" for i in range(12626, 12650)]
    records = []
    for i, r in enumerate(a["source_notes"]):
        assert r["original_first_edition_pdf_frame"] in (755, 756, 757, 758)
        frame = r["original_first_edition_pdf_frame"]
        source_hash = KNOWN[f"first_edition_pdf{frame}"]
        second_hash = KNOWN[f"second_edition_djvu{frame - 5}"]
        records.append(
            {
                "id": f"R{12626 + i}",
                "record_number": 12626 + i,
                "batch": "B07an",
                "source_span": f"B07an-S{frame - 754:03d}",
                "original_pdf_frames": [frame],
                "original_printed_folio": frame - 34,
                "original_1647_source_photo_SHA256": source_hash,
                "separately_typeset_1659_source_photo_SHA256": second_hash,
                "role": r["role"],
                "source_anchor_not_diplomatic": r["source_photo_locator_only"],
                "historical_meaning_only": r["source_historical_meaning"],
                "historical_source_documented_by_one_reader": True,
                "source_complete_original_tabular_cell_corpus_verified": False,
                "original_birth_time_and_profection_calendar_engine_verified": False,
                "independently_validated_actual_human_predicted_outcomes": False,
                "high_stakes_life_outcome_inference_authorized": False,
                "runtime_model_promoted": False,
            }
        )
    assert len(records) == 24
    out = {
        "batch": "B07an",
        "status": "ORIGINAL_1647_CLXVII_PROFECTION_TABLES_THREE_WORKED_CASES_PARTIAL",
        "source_only": True,
        "record_count": 24,
        "first_record": "R12626",
        "last_record": "R12649",
        "source_groups": 4,
        "body_pdf_frames": [755, 756, 757, 758],
        "source_full_degree_minute_table_critical_collation_finished": False,
        "source_all_365_day_year_month_cells_critically_collated": False,
        "third_original_example_prints_37_minute_lookup_instead_of_23": True,
        "source_first_CLXVII_chapter_physically_complete": False,
        "source_actual_chart_time_engine_verified": False,
        "empirical_human_prediction_validations": 0,
        "runtime_promotions": 0,
        "rules": records,
    }
    save(B / "RULES.json", out)
    a["source_images"] = a["source_images"]
    save(DATA, a)
    witness = {
        "batch": "B07an",
        "first_1647_original_full_pdf_SHA256": a["original_full_1647_PDF_sha256"],
        "independently_typeset_source_edition_1659_photographs": True,
        "primary_photographic_binary_witnesses": photos,
        "source_original_1647_readings_by_a_single_nonblinded_reader": True,
        "sampled_literal_table_cells": a["source_sample_one_reader_table_rows"],
        "actual_1647_and_1659_original_worked_case_arithmetic": outcomes,
        "original_rounding_rule_nearest_whole_source_days_not_extensively_validated": True,
        "first_1647_and_second_1659_original_exemplar_37_vs_23_discrepancy": True,
        "reconstructed_third_case_from_correct_arc_6_23": [77, 17, 11],
        "printed_third_case_using_37_minutes": [80, 13, 21],
        "original_date_table_full_source_collation_done": False,
        "separate_original_philologist_critical_expert_second_reader": False,
        "independent_real_human_outcome_validations": 0,
        "runtime_promotions": 0,
    }
    save(PROOF, witness)
    accept = {
        "batch": "B07an",
        "prior_Lilly": 12625,
        "Ptolemy_retained": 1066,
        "Chinese_V7_retained": 355,
        "new_documentary_source_annotations": 24,
        "Lilly_if_accepted": 12649,
        "Western_if_accepted": 13715,
        "next_R": "R12650",
        "next_original_PDF": 759,
        "next_original_printed_folio": 725,
        "next_source": "Midheaven profection examples continued under first CLXVII",
        "full_original_first_CLXVII_chapter_finished": False,
        "all_original_time_table_values_critically_verified": False,
        "third_case_37_min_vs_23_min_printing_discrepancy_preserved": True,
        "rules_SHA256": sha(B / "RULES.json"),
        "source_photo_and_arithmetic_witness_SHA256": sha(PROOF),
        "historical_photographic_data_SHA256": sha(DATA),
        "independent_real_person_predictions_validated": 0,
        "runtime_promotions": 0,
    }
    save(B / "ACCEPTANCE.json", accept)
    print(
        json.dumps(
            {
                "photos": len(photos),
                "source_sampled_cells": len(select),
                "historical_source_records": len(records),
                "printed_three_cases": [c["original_total"] for c in outcomes],
                "third_case_alternative": [77, 17, 11],
                "next_record": accept["next_R"],
                "source_SHA256": sha(DATA),
                "rules_SHA256": sha(B / "RULES.json"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    freeze()
