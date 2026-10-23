"""C09 source-critical Greek child-period regression, not a human validation.

Positive tests are *internal checks* on human-rechecked printed Greek; they
do not establish autograph accuracy or the predictive merit of astrology.
"""
import json
import unittest
from pathlib import Path

DATA = Path(__file__).with_name("HEPHAISTIO_C09_FULL_FINE_PERIOD_AND_OPEN_GLYPHS_V1.json")


class C09EpitomeIVGreekSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = json.loads(DATA.read_text(encoding="utf-8"))

    def test_original_source_provenance_and_no_prediction(self):
        x = self.s
        self.assertEqual(x["provenance"]["local_sha256"], "6ee168a3a39d414620b7c820145c1ffe06dd437617bf79fdc6c9842f51c47f8a")
        self.assertFalse(x["provenance"]["original_pdf_redistributed"])
        self.assertFalse(x["release"]["production_scorer_modified"])
        self.assertFalse(x["release"]["model_promoted"])
        self.assertEqual(x["release"]["predictive_human_tests"], 0)

    def test_seven_fine_rows_exact_literal_transcription_fixtures(self):
        expected = {
            "Saturn": [20, 8, 10, 13, 5, 14, 16],
            "Jupiter": [8, 3, 4, 5, 2, 5, 7],
            "Mars": [10, 4, 5, 5, 3, 7, 8],
            "Sun": [12, 5, 7, 8, 4, 8, 11],
            "Venus": [5, 2, 3, 3, 1, 4, 5],
            "Mercury": [13, 5, 9, 8, 3, 9, 11],
            "Moon": [16, 7, 8, 11, 4, 11, 11],
        }
        x = self.s["section44"]
        self.assertEqual(set(x["finer_rows"]), set(expected))
        for parent, literal in expected.items():
            row = x["finer_rows"][parent]
            self.assertEqual(row["child_values_by_normalized_planet_order"], literal)
            self.assertEqual(row["printed_child_sum"], sum(literal))
            self.assertEqual(row["delta_vs_primary_days"], sum(literal) - row["parent_days"])

    def test_extra_mercury_and_moon_discrepancies_survive(self):
        rows = self.s["section44"]["finer_rows"]
        self.assertEqual(rows["Mercury"]["parent_days"], 57)
        self.assertEqual(rows["Mercury"]["printed_child_sum"], 58)
        self.assertEqual(rows["Moon"]["parent_days"], 71)
        self.assertEqual(rows["Moon"]["printed_child_sum"], 68)
        self.assertEqual(
            {name: row["delta_vs_primary_days"] for name, row in rows.items()},
            {"Saturn": 1, "Jupiter": 0, "Mars": 0, "Sun": 1, "Venus": 1, "Mercury": 1, "Moon": -3},
        )

    def test_primary_365_and_child_total_366_are_distinct(self):
        x = self.s["section44"]
        self.assertEqual(sum(x["printed_primary_by_planet"].values()), 365)
        self.assertEqual(sum(row["printed_child_sum"] for row in x["finer_rows"].values()), 366)
        self.assertEqual(x["net_finer_minus_primary"], 1)
        self.assertEqual(x["exact_parents"], ["Jupiter", "Mars"])
        self.assertEqual(len(x["mismatched_parents"]), 5)

    def test_editorial_22_does_not_rewrite_venus_23(self):
        v = self.s["section44"]["venus"]
        self.assertEqual((v["upper_primary_heading"], v["printed_finer_heading"], v["editorial_suggested_heading"]), (22, 23, 22))
        self.assertEqual(v["printed_finer_children_sum"], 23)
        self.assertIn("legendum", v["editorial_apparatus"])

    def test_section37_jupiter_literal_five_day_extra(self):
        j = self.s["section37"]["jupiter"]
        self.assertEqual(sum(j["transmitted_printed_values_by_normalized_order"]), 365)
        self.assertEqual(j["printed_sum"] - j["thirty_day_month_period"], 5)
        self.assertIn("+5 matches", j["note"])

    def test_section37_venus_is_only_preliminary(self):
        v = self.s["section37"]["venus_preliminary"]
        self.assertEqual(sum(v["transcription_values"]), 213)
        self.assertEqual(v["sum_transcription"] - v["thirty_day_month_period"], -27)
        self.assertIn("PRELIMINARY", v["status"])

    def test_uncertain_mars_letter_cannot_be_autocorrected(self):
        m = self.s["section37"]["mars_uncertainty"]
        fixed = sum(m["non_disputed_values_by_recipient"].values())
        self.assertEqual(sorted(fixed + c for c in m["jupiter_numeric_candidates"]), [450, 460])
        self.assertIn("AMBIGUOUS", m["status"])
        self.assertIn("do not", m["caution"].lower())

    def test_critical_gates_open_for_paulus_and_papyrus(self):
        f = self.s["other_frontiers"]
        self.assertEqual(f["paulus_monomoiria_day_vs_narrative"]["disputed_cells"], 34)
        self.assertFalse(f["paulus_monomoiria_day_vs_narrative"]["editorial_manuscript_diagram_examined"])
        self.assertFalse(f["oxy_4277"]["original_papyrus_image_verified_this_batch"])


if __name__ == "__main__":
    unittest.main()
