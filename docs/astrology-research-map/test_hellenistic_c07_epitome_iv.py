"""Source comparison for Pingree's Epitome IV, not a predictive test.

C08 correction: the printed Mercury Saturn subperiod is 40, NOT 140.
The author's sevenfold approximate method *calculates* 140 but the
printed numerals in Vol II p240 contain several corrupted readings.
"""
import json
import unittest
from pathlib import Path

WITNESS = Path(__file__).resolve().parent / "HEPHAISTIO_C07_EPITOME_IV_INDEPENDENT_RECENSION_V1.json"


class TestEpitomeIVSourceC07(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s=json.loads(WITNESS.read_text(encoding="utf-8"))

    def test_129_month_derived_approximation_not_literal_transcription(self):
        row=self.s["saturn_subdivision"]
        self.assertEqual(sum(row["core_129_months"]),129)
        self.assertEqual(row["seven_day_allocations"],[210,84,105,133,56,140,175])
        self.assertEqual(row["seven_day_allocations_kind"],
                         "DERIVED_FROM_THE_ANCIENT_APPROXIMATE_RULE_NOT_LITERAL_PRINTED_VALUES")
        self.assertEqual(row["formula_derived_sum"],903)
        self.assertEqual(row["formula_derived_delta_vs_900"],3)
        self.assertNotEqual(row["formula_derived_sum"],row["printed_epitome_IV_sum"])

    def test_badly_corrupted_row_preserved_not_silently_repaired(self):
        row=self.s["saturn_subdivision"]
        self.assertEqual(row["printed_epitome_IV_seven_numerals_visual"],
                         [210,84,105,133,57,40,105])
        self.assertEqual(row["printed_epitome_IV_sum"],734)
        self.assertEqual(row["printed_epitome_IV_delta_vs_900"],-166)
        self.assertEqual(row["saturn_to_mercury_epitome_IV"],40)
        self.assertEqual(row["formula_derived_saturn_to_mercury_epitome_IV"],140)
        self.assertEqual(row["saturn_to_mercury_main_Hephaistio_1973"],150)
        self.assertEqual(row["saturn_to_mercury_later_Valens_5th_century_addition"],140)
        self.assertIn("corrupt",row["apparatus_warning"].lower())
        self.assertFalse(self.s["source"]["manuscript_sigla_collation_complete"])

    def test_year_five_days_and_365_are_source_attested(self):
        self.assertTrue(self.s["year_five_days"]["self_source_not_conjecture"])
        data=self.s["year_365"]
        self.assertEqual(sum(data["primary_allocation"].values()),365)
        self.assertEqual(sum(data["compared_to_main_hephaistio_greek_II36"].values()),360)
        self.assertEqual(data["primary_allocation"]["Mercury"],57)
        self.assertEqual(data["compared_to_main_hephaistio_greek_II36"]["Mercury"],52)
        # Venus conflicts *within* Epitome IV's 365-day method as printed.
        self.assertEqual(data["fine_venus_heading_printed_epitome_IV"],23)
        self.assertEqual(data["fine_venus_child_sum_epitome_IV"],23)
        self.assertEqual(data["fine_venus_editorial_expected_epitome_IV"],22)

    def test_no_human_prediction_or_source_book_redistribution(self):
        self.assertEqual(self.s["human_validation"],0)
        self.assertFalse(self.s["model_promoted"])
        self.assertFalse(self.s["source"]["copyrighted_volume_shared"])


if __name__=="__main__":
    unittest.main()
