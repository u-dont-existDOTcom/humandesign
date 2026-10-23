"""C10: separate edited Greek printed numerals, glyph candidates, and arithmetic.

Tests confirm internal fixture consistency ONLY; no independent autograph
or historical/empirical astrology prediction validation is claimed.
"""
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
NEW = HERE / "HEPHAISTIO_C10_EPITOME_IV37_SOURCE_QUESTION_REGISTER_V1.json"
C08 = HERE / "HEPHAISTIO_C08_LITERAL_VS_DERIVED_SUBPERIOD_WITNESS_V1.json"
C09 = HERE / "HEPHAISTIO_C09_FULL_FINE_PERIOD_AND_OPEN_GLYPHS_V1.json"


class TestEpitomeIV37C10(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads(NEW.read_text(encoding="utf-8"))
        cls.c08 = json.loads(C08.read_text(encoding="utf-8"))
        cls.c09 = json.loads(C09.read_text(encoding="utf-8"))

    def test_periods_and_recipient_order(self):
        self.assertEqual(self.source["recipient_order"],
                         ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"])
        self.assertEqual([v["parent_months"] for v in self.source["parent_periods"].values()],
                         [30, 12, 15, 19, 8, 20, 25])
        self.assertEqual(sum(x["parent_months"] for x in self.source["parent_periods"].values()), 129)

    def test_edited_printed_values_provisional_and_preserved(self):
        p = self.source["parent_periods"]
        self.assertEqual(p["Saturn"]["edited_printed_values_by_recipient"],
                         [210,84,105,133,57,40,105])
        self.assertEqual(p["Jupiter"]["edited_printed_values_by_recipient"],
                         [85,34,42,54,22,57,71])
        self.assertEqual(p["Mars"]["edited_printed_values_by_recipient"],
                         [105,52,52,66,28,70,87])
        self.assertEqual(p["Sun"]["edited_printed_values_by_recipient"],
                         [104,52,64,83,30,80,118])
        self.assertEqual(p["Venus"]["edited_printed_values_by_recipient"],
                         [57,22,28,36,15,38,17])
        self.assertEqual(p["Mercury"]["edited_printed_values_by_recipient"],
                         [141,57,70,90,36,96,117])
        self.assertEqual(p["Moon"]["edited_printed_values_by_recipient"],
                         [177,71,87,None,47,119,148])

    def test_unresolved_sum_sets_are_computed_not_silently_clamped(self):
        p = self.source["parent_periods"]
        for name, r in p.items():
            common = sum(v or 0 for v in r["edited_printed_values_by_recipient"])
            opts = r["possible_sum_days"]
            self.assertEqual(max(opts), common) if name == "Mars" else self.assertTrue(all(total >= common for total in opts), name)
            self.assertEqual(r["possible_delta_vs_30day_months"],
                             [total-r["nominal_30_day_baseline"] for total in opts])
        self.assertEqual({n: p[n]["possible_sum_days"] for n in p},
                         {"Saturn":[734],"Jupiter":[365],"Mars":[450,460],
                          "Sun":[531],"Venus":[213],"Mercury":[607],"Moon":[764,794]})

    def test_mars_52_high_res_is_not_arithmetic_fitted(self):
        m=self.source["high_resolution_reading_changes"]["mars_jupiter"]
        self.assertEqual((m["new_preferred_reading"],m["earlier_alternative_value"]), (52,42))
        self.assertEqual((m["reference_total_with_52"],m["other_possible_total_with_42"]), (460,450))
        self.assertTrue(m["do_not_select_by_arithmetic"])
        self.assertFalse(m["independent_manuscript_confirmation"])

    def test_sun_venus_mercury_nonclosing_rows_keep_failures(self):
        p=self.source["parent_periods"]
        self.assertEqual(p["Sun"]["possible_delta_vs_30day_months"],[-39])
        self.assertEqual(p["Venus"]["possible_delta_vs_30day_months"],[-27])
        self.assertEqual(p["Mercury"]["possible_delta_vs_30day_months"],[7])
        self.assertEqual(p["Jupiter"]["possible_delta_vs_30day_months"],[5])

    def test_moon_sun_not_given_one_invented_literal_value(self):
        m=self.source["high_resolution_reading_changes"]["moon_sun"]
        self.assertEqual({v["days"] for v in m["candidates"]},{115,145})
        self.assertIsNone(self.source["parent_periods"]["Moon"]["edited_printed_values_by_recipient"][3])
        self.assertEqual(m["source_total_candidates"],[764,794])
        self.assertIn("UNRESOLVED",m["status"])

    def test_c08_c09_not_rewritten_to_fit(self):
        old=self.c08["saturn"]
        self.assertEqual((old["printed_mercury"],old["derived_mercury"]),(40,140))
        previous=self.c09["section44"]
        self.assertEqual((previous["sum_seven_primary_days"],
                          previous["sum_seven_printed_finer_row_sums"]),(365,366))
        self.assertEqual(self.source["status_vs_prior"]["c08_printed_saturn_mercury"],40)

    def test_new_greek_corpus_is_bibliographic_lead_only(self):
        r=self.source["independent_references"]
        self.assertIn("CATALOGUE_ONLY",r["boer_greek_searchable_corpus"]["status"])
        self.assertIn("NOT_FACSIMILE_INSPECTED",r["boer_1958"]["status"])
        self.assertIn("NOT_FACSIMILE_INSPECTED",r["boer_1962"]["status"])
        self.assertIn("UNCHANGED",r["oxy_4277"]["status"])

    def test_source_only_never_human_model_promotion(self):
        src=self.source
        self.assertEqual(src["assurance"]["no_human_validation"],0)
        self.assertFalse(src["assurance"]["altered_production_scorer"])
        self.assertFalse(src["assurance"]["source_book_redistributed"])
        self.assertFalse(src["assurance"]["full_original_ms_image_evidence"])
        self.assertEqual(src["assurance"]["paulus_34_cell_dispute_remaining"],34)
        self.assertFalse(src["source"]["manuscript_collation_done"])


if __name__=="__main__":
    unittest.main()
