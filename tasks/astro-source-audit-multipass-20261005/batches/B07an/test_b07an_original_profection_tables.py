"""Original Lilly 1647/1659 profection table and three examples: source-only tests."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def time_minutes(v):
    return (v[0] * 24 + v[1]) * 60 + v[2]


def from_minutes(x):
    return [x // 1440, (x // 60) % 24, x % 60]


class ProfectionOriginalPrintedTimeTables(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = j(B / "ORIGINAL_1647_1659_PROFECTION_TIME_TABLES_AND_CASES_V1.json")
        cls.proof = j(B / "SELECTED_ORIGINAL_PHOTO_ARITHMETIC_WITNESS_V1.json")
        cls.rules = j(B / "RULES.json")
        cls.accept = j(B / "ACCEPTANCE.json")
        cls.rows = {
            (r["table"], r["printed_label"]): r["first_edition_1647_time_dhm"]
            for r in cls.raw["source_sample_one_reader_table_rows"]
        }
        cls.cases = cls.raw["original_printed_1647_date_table_and_examples"]

    def test_1647_first_edition_source_pdf_full_identity(self):
        self.assertEqual(
            self.raw["original_full_1647_PDF_sha256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )
        self.assertEqual(
            self.proof["first_1647_original_full_pdf_SHA256"],
            self.raw["original_full_1647_PDF_sha256"],
        )

    def test_eight_edition_photographs_sha_byte_integrity(self):
        self.assertEqual(len(self.raw["source_images"]), 8)
        self.assertEqual(len(self.proof["primary_photographic_binary_witnesses"]), 8)
        for key, row in self.raw["source_images"].items():
            file = B / row["file"]
            self.assertTrue(file.is_file(), key)
            self.assertGreater(file.stat().st_size, 200000)
            self.assertEqual(file.stat().st_size, row["source_image_exact_bytes"])
            self.assertEqual(sha(file), row["source_image_SHA256"])
            self.assertEqual(
                sha(file), self.proof["primary_photographic_binary_witnesses"][key]["sha256"]
            )

    def test_original_physical_printed_pages_aligned(self):
        self.assertEqual(self.raw["source_original_printed_pages"], [721, 722, 723, 724])
        for n in range(755, 759):
            row = self.raw["source_images"][f"first_edition_pdf{n}"]
            self.assertEqual(row["printed_folio"], n - 34)
        for n in range(750, 754):
            row = self.raw["source_images"][f"second_edition_djvu{n}"]
            self.assertEqual(row["printed_folio"], n - 29)

    def test_literal_only_nine_verified_sampled_rows(self):
        self.assertEqual(len(self.raw["source_sample_one_reader_table_rows"]), 9)
        self.assertEqual(self.rows["degree", 1], [12, 4, 12])
        self.assertEqual(self.rows["degree", 2], [24, 8, 23])
        self.assertEqual(self.rows["degree", 6], [73, 1, 10])
        self.assertEqual(self.rows["degree", 30], [365, 5, 49])
        self.assertEqual(self.rows["minute", 23], [4, 16, 1])
        self.assertEqual(self.rows["minute", 25], [5, 1, 45])
        self.assertEqual(self.rows["minute", 28], [5, 16, 22])
        self.assertEqual(self.rows["minute", 37], [7, 12, 11])
        self.assertEqual(self.rows["minute", 60], [12, 4, 13])

    def test_minutes_60_vs_one_degree_one_minute_difference(self):
        delta = time_minutes(self.rows["minute", 60]) - time_minutes(self.rows["degree", 1])
        self.assertEqual(delta, 1)
        self.assertFalse(self.raw["source_full_30_and_60_digit_columns_critically_collated"])

    def test_calendar_table_physical_scope_not_all_days_critically_read(self):
        self.assertEqual(self.raw["source_expected_table_degree_rows"], 30)
        self.assertEqual(self.raw["source_expected_table_minute_rows"], 60)
        self.assertFalse(self.raw["source_365day_month_table_all_cells_critically_collated"])
        self.assertFalse(self.proof["original_date_table_full_source_collation_done"])

    def test_first_1647_example_exact_1degree28_and_rounding(self):
        x = self.cases[0]
        self.assertEqual(x["printed_arc"], [1, 28])
        self.assertEqual(x["source_degree_row_dhm"], [12, 4, 12])
        self.assertEqual(x["source_minute_row"], [28, 5, 16, 22])
        self.assertEqual(
            from_minutes(time_minutes([12, 4, 12]) + time_minutes([5, 16, 22])), [17, 20, 34]
        )
        self.assertEqual(x["printed_rounded_day"], 18)
        self.assertEqual(x["printed_month_day"], "October 6")

    def test_second_original_example_2degree25_calendar(self):
        x = self.cases[1]
        self.assertEqual(x["printed_arc"], [2, 25])
        self.assertEqual(
            from_minutes(time_minutes([24, 8, 23]) + time_minutes([5, 1, 45])), [29, 10, 8]
        )
        self.assertEqual(x["printed_month_day"], "October 17")

    def test_third_example_printed_subtraction_6degrees23(self):
        x = self.cases[2]
        self.assertEqual(x["original_target"], [13, 0])
        self.assertEqual(x["original_ascendant"], [6, 37])
        self.assertEqual(x["printed_arc"], [6, 23])
        self.assertEqual(x["printed_minute_row_actually_used"][0], 37)
        self.assertEqual(x["mathematically_corresponding_minute_row"][0], 23)

    def test_third_example_printed_37minute_is_not_target_remainder(self):
        x = self.cases[2]
        self.assertEqual(
            from_minutes(time_minutes([73, 1, 10]) + time_minutes([7, 12, 11])), [80, 13, 21]
        )
        self.assertEqual(
            from_minutes(time_minutes([73, 1, 10]) + time_minutes([4, 16, 1])), [77, 17, 11]
        )
        self.assertEqual(x["printed_total_dhm"], [80, 13, 21])
        self.assertEqual(x["recalculated_total_using_23_row_dhm"], [77, 17, 11])
        self.assertEqual(x["difference_using_37_vs_23_row_dhm"], [2, 20, 10])
        self.assertEqual(x["printed_month_day"], "December 7")

    def test_no_automatic_falsely_corrected_original(self):
        self.assertTrue(
            self.proof["first_1647_and_second_1659_original_exemplar_37_vs_23_discrepancy"]
        )
        self.assertTrue(self.raw["third_worked_case_discrepancy_retained_not_repaired"])
        self.assertTrue(self.proof["source_original_1647_readings_by_a_single_nonblinded_reader"])
        self.assertFalse(self.proof["separate_original_philologist_critical_expert_second_reader"])

    def test_original_calendar_and_astrological_person_accuracy_unknown(self):
        self.assertFalse(self.raw["original_1647_natal_chart_ephemeris_conversion_verified"])
        self.assertEqual(self.raw["independent_real_person_predictions_validated"], 0)
        self.assertEqual(self.raw["runtime_promotions"], 0)
        self.assertFalse(self.rules["source_first_CLXVII_chapter_physically_complete"])

    def test_source_note_ids_24_nonoverlapping(self):
        self.assertEqual(self.raw["proposed_source_record_count"], 24)
        self.assertEqual(self.rules["record_count"], 24)
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(12626, 12650))
        )
        self.assertEqual(self.accept["next_R"], "R12650")
        self.assertEqual(self.accept["next_original_PDF"], 759)

    def test_pinned_Western_and_chinese_source_counts_untouched(self):
        self.assertEqual(j(WEST)["records_count"], 12625)
        self.assertEqual(j(WEST)["batches"][-1]["id"], "B07am")
        self.assertEqual(j(CHINA)["sum_source_annotations"], 355)
        self.assertEqual(self.accept["Chinese_V7_retained"], 355)

    def test_scope_original_pages_timing_not_full_chart_engine(self):
        self.assertEqual(self.rules["body_pdf_frames"], [755, 756, 757, 758])
        self.assertFalse(self.accept["all_original_time_table_values_critically_verified"])
        self.assertFalse(self.accept["full_original_first_CLXVII_chapter_finished"])
        self.assertEqual(self.accept["Western_if_accepted"], 13715)

    def test_record_and_witness_SHAs_recompute(self):
        self.assertEqual(self.accept["rules_SHA256"], sha(B / "RULES.json"))
        self.assertEqual(
            self.accept["historical_photographic_data_SHA256"],
            sha(B / "ORIGINAL_1647_1659_PROFECTION_TIME_TABLES_AND_CASES_V1.json"),
        )
        self.assertEqual(
            self.accept["source_photo_and_arithmetic_witness_SHA256"],
            sha(B / "SELECTED_ORIGINAL_PHOTO_ARITHMETIC_WITNESS_V1.json"),
        )


def check_record(n):
    def test(self):
        note = self.raw["source_notes"][n]
        rule = self.rules["rules"][n]
        self.assertEqual(note["planned_id"], f"R{12626 + n}")
        self.assertEqual(rule["id"], note["planned_id"])
        self.assertEqual(rule["role"], note["role"])
        self.assertEqual(rule["original_printed_folio"], note["original_1647_printed_folio"])
        self.assertFalse(rule["runtime_model_promoted"])

    return test


for i in range(24):
    setattr(
        ProfectionOriginalPrintedTimeTables,
        f"test_original_1647_1659_source_note_{i + 1:02d}",
        check_record(i),
    )


if __name__ == "__main__":
    unittest.main()
