"""Source-exact mathematical diagnostics for two calendars and two editorial witnesses.

Hephaistio II.29 and II.36, Pingree 1973 (Greek critical edition)
and Schmidt 1998 (English). This is a *source* test; it neither
establishes an authentic manuscript arithmetic correction nor tests a
human astrological forecast.
"""
import json
import unittest
from pathlib import Path
from fractions import Fraction

HERE=Path(__file__).resolve().parent
SOURCE=HERE/"HEPHAISTIO_C07_FIVEDAY_MANUSCRIPT_AND_CALENDAR_V1.json"

class TestHephaistioFiveDayWitnessC07(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc=json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_primary_and_secondary_manuscript_layers_separate(self):
        d=self.doc
        self.assertIn("τὴν πενθήμερον",d["chapter29"]["source_phrase"])
        self.assertIn("marginal",d["chapter29"]["P2_apparatus_note"])
        self.assertTrue(d["chapter29"]["not_independent_ancient_authorial_P2"])
        self.assertIn("Parisinus",d["source"]["primary_manuscript_P"])
        self.assertFalse(d["model_promoted"])
        self.assertEqual(d["human_validation"],"NONE")

    def test_365_year_improves_total_but_no_final_text_repair(self):
        c=self.doc["chapter29"]["checks"]
        self.assertEqual(c["printed"],3910)
        self.assertEqual(c["expected360"],3870)
        self.assertEqual(c["expected365twelfths"],47085)
        self.assertEqual(c["absoluteDelta360"],42)
        self.assertEqual(Fraction(c["absoluteDelta365twelfths"],12),Fraction(263,12))
        self.assertLess(Fraction(c["absoluteDelta365twelfths"],12),c["absoluteDelta360"])
        self.assertNotEqual(Fraction(c["expected365twelfths"],12),c["printed"])

    def test_anomalies_persist_under_either_calendar(self):
        rows={r["planet"]:r for r in self.doc["chapter29"]["monthly_comparison"]}
        self.assertEqual(len(rows),7)
        self.assertEqual(rows["Mars"]["delta_360"],0)
        self.assertEqual(rows["Mars"]["delta_365_twelfths"],-75)
        self.assertEqual(rows["Sun"]["delta_365_twelfths"],-107)
        self.assertEqual(rows["Moon"]["delta_365_twelfths"],43)
        self.assertEqual(rows["Saturn"]["delta_365_twelfths"],6)

    def test_separate_ii36_readings(self):
        d=self.doc["chapter36"]
        self.assertEqual((d["Greek_primary"],d["Greek_fine_headers"],
                          d["Greek_fine_child_sums"],d["Schmidt_fine_headers"]),
                         (360,365,365,375))
        self.assertIn("τξε",d["P_apparatus_note"])
        self.assertEqual(d["editorial_expected_Mercury"],52)
        self.assertEqual(d["Greek_printed_fine_Mercury"],57)
        self.assertIn("νβ desid.",d["apparatus_note"])

    def test_do_not_rewrite_saturn_to_mercury(self):
        self.assertEqual(self.doc["chapter29"]["Saturn_Mercury_edited"],150)
        self.assertEqual(self.doc["chapter29"]["Saturn_Mercury_later_Valens"],140)
        self.assertNotEqual(self.doc["chapter29"]["Saturn_Mercury_edited"],
                            self.doc["chapter29"]["Saturn_Mercury_later_Valens"])

if __name__=="__main__":
    unittest.main()
