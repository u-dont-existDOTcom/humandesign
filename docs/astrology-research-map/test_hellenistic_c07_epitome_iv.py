"""Hephaistio Epitome IV's *written* approximation, not human prediction.

Sourced from Pingree, Epitomae Quattuor Vol II (1974), printed
pp240-242 and 264-265. Tests source arithmetic and preserves the
distinct P-recension values without silently emending either one.
"""
import json
import unittest
from pathlib import Path

WITNESS=Path(__file__).resolve().parent/"HEPHAISTIO_C07_EPITOME_IV_INDEPENDENT_RECENSION_V1.json"


class TestEpitomeIVSourceC07(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s=json.loads(WITNESS.read_text(encoding="utf-8"))

    def test_129_month_source_and_seven_times_approximation(self):
        row=self.s["saturn_subdivision"]
        self.assertEqual(sum(row["core_129_months"]),129)
        self.assertEqual(row["seven_day_allocations"],
            [210,84,105,133,56,140,175])
        self.assertEqual(sum(row["seven_day_allocations"]),903)
        self.assertEqual(row["sum_of_allocations"],903)
        self.assertEqual(row["baseline_900_delta"],3)
        self.assertEqual(row["saturn_to_mercury_epitome_IV"],140)
        self.assertEqual(row["saturn_to_mercury_main_Hephaistio_1973"],150)

    def test_source_140_and_later_valens_140_still_not_manuscript_autograph(self):
        row=self.s["saturn_subdivision"]
        self.assertEqual(row["saturn_to_mercury_epitome_IV"],
                         row["saturn_to_mercury_later_Valens_5th_century_addition"])
        self.assertNotEqual(row["saturn_to_mercury_main_Hephaistio_1973"],
                            row["saturn_to_mercury_epitome_IV"])
        self.assertIn("corrupt",row["apparatus_warning"].lower())
        self.assertFalse(self.s["source"]["manuscript_sigla_collation_complete"])

    def test_year_five_days_and_365_explicit_not_inferred(self):
        self.assertTrue(self.s["year_five_days"]["self_source_not_conjecture"])
        source=self.s["year_365"]
        self.assertIn("expressly",source["direct_source"])
        self.assertEqual(sum(source["primary_allocation"].values()),365)
        self.assertEqual(sum(source["compared_to_main_hephaistio_greek_II36"].values()),360)
        self.assertEqual(source["primary_allocation"]["Mercury"],57)
        self.assertEqual(source["compared_to_main_hephaistio_greek_II36"]["Mercury"],52)

    def test_no_human_prediction_included(self):
        self.assertEqual(self.s["human_validation"],0)
        self.assertFalse(self.s["model_promoted"])
        self.assertFalse(self.s["source"]["copyrighted_volume_shared"])


if __name__=="__main__":
    unittest.main()
