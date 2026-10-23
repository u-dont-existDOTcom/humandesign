"""Historical source exactness, not empirical predictive validation.
C08: the printed Epitome IV Saturn row and its proportional 7x
reconstruction are different; refuse to conflate 40 with derived 140.
"""
import json
import unittest
from pathlib import Path

SOURCE=Path(__file__).resolve().parent/"HEPHAISTIO_C08_LITERAL_VS_DERIVED_SUBPERIOD_WITNESS_V1.json"


class TestEpitomeIVSourceFidelityC08(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_literal_printed_vs_computed_expose_corrupt_numerals(self):
        s=self.data["saturn"]
        self.assertEqual(s["transmitted_printed_values"],[210,84,105,133,57,40,105])
        self.assertEqual(s["literal_printed_total"],734)
        self.assertEqual(s["derived_values"],[210,84,105,133,56,140,175])
        self.assertEqual(s["derived_total"],903)
        self.assertEqual(s["baseline_expected_30_day_months"],900)
        self.assertEqual(s["differences_literal_minus_derived"],[0,0,0,0,1,-100,-70])
        self.assertIn("NOT printed",s["source_specificity"])

    def test_corrupt_40_not_false_printed_140(self):
        s=self.data["saturn"]
        self.assertEqual(s["printed_mercury"],40)
        self.assertEqual(s["derived_mercury"],140)
        self.assertEqual(s["main_hephaistio_mercury"],150)
        self.assertEqual(s["later_valens_appendix_mercury"],140)
        self.assertEqual(s["printed_moon"],105)
        self.assertEqual(s["derived_moon"],175)
        self.assertTrue(self.data["source_boundaries"]["prior_C07_140_print_claim_corrected"])

    def test_365_day_finer_rows_still_fail_to_sum(self):
        t=self.data["finer_365"]
        self.assertEqual(sum(t["primary_annual_7"].values()),365)
        for row in t["verified_selected_finer_rows"]:
            self.assertEqual(sum(row["child_values"].values()),row["child_sum"])
            self.assertEqual(row["child_sum"]-row["source_parent_days"],row["offset"])
            self.assertEqual(row["offset"],1)
        venus=next(x for x in t["verified_selected_finer_rows"] if x["parent"]=="Venus")
        self.assertEqual(venus["finer_printed_heading"],23)
        self.assertEqual(venus["source_parent_days"],22)
        self.assertIn("legendum",venus["critical_apparatus"])
        self.assertIn("Do not",t["unused_unreviewed_full_rows"])

    def test_never_promote_source_integrity_to_predicted_human(self):
        s=self.data["source_boundaries"]
        self.assertFalse(s["model_promotion"])
        self.assertEqual(s["real_human_predictions"],0)
        self.assertEqual(s["independent_ancient_manuscripts_confirmed"],0)
        self.assertFalse(self.data["source"]["original_book_redistributed"])


if __name__=="__main__":
    unittest.main()
