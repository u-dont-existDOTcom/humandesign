"""Source fidelity and exact nominal Naibod time carry, no predictive claim."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
P = B.parent


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class PrintedNaibodFinal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j(B / "ORIGINAL_1647_CLXVI_NAIBOD_FINISH_AND_NEXT_BOUNDARY_V1.json")
        cls.rules = j(B / "RULES.json")
        cls.accept = j(B / "ACCEPTANCE.json")
        cls.old = j(P / "B07aj/ORIGINAL_1647_NAIBOD_149_PRINTED_TABLE_ROWS_V1.json")

    def test_two_historical_printed_715_photo_SHA_and_bytes(self):
        p = self.a["source_photographic_first_and_second_edition_witnesses"]
        self.assertEqual(set(p), {"original_1647", "separately_typeset_1659"})
        for item in p.values():
            file = ROOT / item["relative_source"]
            self.assertEqual(sha(file), item["photo_sha256"])
            self.assertEqual(file.stat().st_size, item["bytes"])
            self.assertEqual(item["source_printed_folio"], 715)

    def test_first_1647_full_original_pdf_SHA(self):
        self.assertEqual(
            self.a["source_photographic_first_and_second_edition_witnesses"]["original_1647"][
                "original_full_1647_pdf_sha256"
            ],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_previous_source_rows_byte_identical(self):
        self.assertEqual(
            self.a["prior_b07aj_149_table_rows_SHA256"],
            sha(P / "B07aj/ORIGINAL_1647_NAIBOD_149_PRINTED_TABLE_ROWS_V1.json"),
        )

    def test_Mars_terms_before_carry_and_hour_day_result(self):
        a = self.a["cases"][0]
        self.assertEqual(a["degree_lookup"], [11, 58, 21])
        self.assertEqual(a["minute_lookup"], [339, 17])
        self.assertEqual(a["before_hours_carry"], [11, 397, 38])
        self.assertEqual(a["after_hours_carry"], [11, 398, 14])
        self.assertEqual(a["after_365day_year_carry"], [12, 33, 14])

    def test_Mars_opposition_day_carry(self):
        a = self.a["cases"][1]
        self.assertEqual(a["degree_lookup"], [19, 101, 17])
        self.assertEqual(a["minute_lookup"], [321, 4])
        self.assertEqual(a["before_hours_carry"], [19, 422, 21])
        self.assertEqual(a["after_365day_year_carry"], [20, 57, 21])

    def test_two_printings_agree_on_examples(self):
        self.assertTrue(all(x["literal_1647_1659_witness_agreement"] for x in self.a["cases"]))

    def test_duplicate_printed_chap_CLXVI_is_physical_new_unit(self):
        self.assertTrue(
            self.a["source_first_printed_CLXVI_directions_time_text_physically_ends_PDF749"]
        )
        self.assertTrue(self.a["second_distinct_original_PRINTED_CLXVI_starts_same_PDF749"])
        self.assertEqual(self.accept["next_printed_chapter_label"], "CLXVI")
        self.assertEqual(self.accept["next_editorial_distinct_chapter_ordinal"], 166)

    def test_14_historical_documentary_records_exact(self):
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(12568, 12582))
        )
        self.assertEqual(self.accept["next_original_R"], "R12582")
        self.assertEqual(self.accept["next_original_pdf_frame"], 749)
        self.assertEqual(self.rules["record_count"], 14)

    def test_physical_cover_not_expert_critical_text(self):
        self.assertTrue(self.a["source_all_1647_numbered_chapter_physical_pages_attempted"])
        self.assertFalse(
            self.a["source_first_CLXVI_full_expert_diplomatic_critical_edition_complete"]
        )
        self.assertFalse(
            self.a["source_old_astrological_chart_time_engine_mathematically_verified"]
        )
        self.assertFalse(self.rules["independent_expert_edition_collation_finished"])

    def test_source_seven_rates_unknown_minute27_missing(self):
        self.assertTrue(self.a["source_1647_original_rate_table_seven_unresolved_glyphs_remain"])
        self.assertTrue(self.a["source_Naibod_original_minute27_label_missing"])

    def test_separate_original_source_registries_unchanged(self):
        w = j(
            ROOT
            / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
        )
        c = j(
            ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"
        )
        self.assertEqual(w["records_count"], 12567)
        self.assertEqual(c["sum_source_annotations"], 262)

    def test_no_empirical_human_validation_or_runtime(self):
        self.assertEqual(self.a["independently_blinded_actual_person_predictions"], 0)
        self.assertEqual(self.a["runtime_promotions"], 0)
        for r in self.rules["rules"]:
            self.assertFalse(r["runtime_model_promoted"])


def one_rule(i):
    def test(self):
        s = self.a["records"][i]
        r = self.rules["rules"][i]
        self.assertEqual(r["id"], f"R{12568 + i}")
        self.assertEqual(r["record_number"], 12568 + i)
        self.assertEqual(r["role"], s["role"])
        self.assertFalse(r["runtime_model_promoted"])

    return test


for n in range(14):
    setattr(PrintedNaibodFinal, f"test_source_rule_{n + 1:02d}", one_rule(n))


if __name__ == "__main__":
    unittest.main()
