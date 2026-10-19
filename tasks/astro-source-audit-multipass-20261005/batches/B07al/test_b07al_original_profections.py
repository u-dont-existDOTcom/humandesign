"""Original first-edition annual Profections documentary and bounded sign cycle."""

import hashlib
import json
import sys
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
sys.path.insert(0, str(B))
import source_annual_profections as p  # noqa: E402


def j(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


class ProfectionsDocumentary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = j(B / "ANNUAL_PROFECTIONS_ORIGINAL_PRINTED_CLXVI_SOURCE_V1.json")
        cls.rules = j(B / "RULES.json")
        cls.accept = j(B / "ACCEPTANCE.json")

    def test_first_original_1647_pdf_identity(self):
        self.assertEqual(
            self.data["original_Wellcome_first_edition_full_PDF_SHA256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_original_printed_715_718_four_frame_hashes(self):
        self.assertEqual(
            list(self.data["original_first_edition_photo_witnesses"]), ["749", "750", "751", "752"]
        )
        for key, r in self.data["original_first_edition_photo_witnesses"].items():
            file = ROOT / r["file"]
            self.assertTrue(file.is_file())
            self.assertEqual(file.stat().st_size, r["bytes"])
            self.assertEqual(sha(file), r["sha256"])
            self.assertEqual(r["printed_folio"], int(key) - 34)

    def test_printed_reused_CLXVI_is_separate_original_chapter(self):
        self.assertTrue(self.data["second_distinct_PRINTED_CLXVI_source_unit"])
        self.assertTrue(self.data["first_PRINTED_CLXVI_directions_time_not_reopened"])
        self.assertTrue(self.data["next_PRINTED_CLXVII_starts_on_same_original_PDF752"])

    def test_30_source_only_records_exact_IDS(self):
        self.assertEqual(len(self.data["records"]), 30)
        self.assertEqual(self.rules["record_count"], 30)
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(12582, 12612))
        )
        self.assertEqual(self.accept["next_source_R"], "R12612")
        self.assertEqual(self.accept["next_original_pdf_frame"], 752)

    def test_transmitted_year_month_day_rates_unaltered(self):
        self.assertEqual(self.data["annual_sign_cycle_length_years"], 12)
        self.assertEqual(self.data["printed_monthly_profection_parts"], 13)
        self.assertEqual(self.data["printed_diurnal_sign_days_hours_minutes"], [2, 3, 54])
        self.assertEqual(self.data["printed_one_degree_nominal_days_hours_minutes"], [12, 4, 12])

    def test_nominal_30_degree_year_365_days_6_hours(self):
        self.assertEqual(p.source_nominal_degree_time_minutes(), (12 * 24 + 4) * 60 + 12)
        self.assertEqual(p.source_nominal_degree_time_minutes() * 30, (365 * 24 + 6) * 60)

    def test_generic_6Gemini_1year_moves_to6Cancer(self):
        self.assertEqual(p.projected_sign_degree_minute("Gemini", 6, 0, 1)["sign"], "Cancer")
        self.assertEqual(p.projected_sign_degree_minute("Gemini", 6, 0, 2)["sign"], "Leo")
        self.assertEqual(p.projected_sign_degree_minute("Gemini", 6, 0, 3)["sign"], "Virgo")

    def test_twelve_solar_year_cycle_not_direct_Gregorian_dates(self):
        for sign in p.SIGNS:
            self.assertEqual(p.sign_after_completed_solar_return_years(sign, 12), sign)
            self.assertEqual(p.sign_after_completed_solar_return_years(sign, 24), sign)
        self.assertFalse(
            p.source_method_limits()["Gregorian_birthday_is_verified_exact_solar_return"]
        )

    def test_25th_ordinal_year_uses_24_completed(self):
        self.assertEqual(p.completed_years_to_enter_for_current_ordinal_year(25), 24)
        self.assertEqual(p.sign_after_completed_solar_return_years("Capricorn", 24), "Capricorn")
        self.assertEqual(p.sign_after_completed_solar_return_years("Capricorn", 25), "Aquarius")

    def test_example_merchant_table_not_cloned_72_rows_as_verified_chart(self):
        self.assertEqual(self.data["historic_merchant_natal_date_as_printed"], "1616-09-19")
        self.assertEqual(self.data["historic_merchant_table_years_inclusive"], [1616, 1687])
        self.assertEqual(self.data["original_merchant_table_physical_source_rows"], 72)
        self.assertFalse(self.data["all_merchant_table_zodiac_cells_expert_collated"])

    def test_original_chinese_and_Lilly_before_are_unchanged(self):
        w = j(
            ROOT
            / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
        )
        c = j(
            ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"
        )
        self.assertEqual(w["records_count"], 12581)
        self.assertEqual(w["next"]["editorial_source_sequence_ordinal"], 166)
        self.assertEqual(c["sum_source_annotations"], 262)

    def test_invalid_profection_inputs_fail_closed(self):
        for value in (-1, True, "24", 201):
            with self.assertRaises(ValueError):
                p.sign_after_completed_solar_return_years("Gemini", value)
        with self.assertRaises(ValueError):
            p.sign_after_completed_solar_return_years("Unknown", 1)
        with self.assertRaises(ValueError):
            p.projected_sign_degree_minute("Gemini", 30, 0, 1)

    def test_original_sources_do_not_validate_real_person_predictions(self):
        self.assertEqual(self.data["real_person_outcome_predictions_validated"], 0)
        self.assertEqual(self.data["runtime_model_promotions"], 0)
        self.assertFalse(
            p.source_method_limits()[
                "original_1647_chart_ascendant_mid_heaven_full_natal_engine_validated"
            ]
        )
        self.assertTrue(all(not r["runtime_model_promoted"] for r in self.rules["rules"]))


def one_source_rule(n):
    def test(self):
        x = self.data["records"][n]
        r = self.rules["rules"][n]
        self.assertEqual(x["id"], f"R{12582 + n}")
        self.assertEqual(r["id"], x["id"])
        self.assertEqual(r["role"], x["role"])
        self.assertFalse(r["runtime_model_promoted"])

    return test


for n in range(30):
    setattr(
        ProfectionsDocumentary, f"test_original_profection_note_{n + 1:02d}", one_source_rule(n)
    )


if __name__ == "__main__":
    unittest.main()
