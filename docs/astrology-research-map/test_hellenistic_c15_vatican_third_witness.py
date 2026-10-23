"""C15: directly photographed Vatican table comparison with Florence and Munich.

Green source arithmetic is NOT palaeographic peer review, an ancient autograph,
an independently descended textual family, or any human predictive validation.
"""
import unittest
from paulus_c15_three_manuscript_comparison import (
    vatican_source, three_manuscript_comparison
)
from paulus_florence_munich_comparison_c14 import florence_source
from paulus_munich_full_c13 import manuscript_source


class C15VaticanManuscript(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vat=vatican_source()
        cls.flo=florence_source()
        cls.mun=manuscript_source()
        cls.comp=three_manuscript_comparison()
        cls.v=cls.vat["independent_source_observed_planetary_degree_1_to_30"]

    def test_original_bav_photo_image_id_and_sha(self):
        x=self.vat["original"]
        self.assertEqual(x["shelfmark"],"Vat. gr. 1444")
        self.assertEqual(x["catalogue_date"],"1542")
        self.assertEqual(x["inspected_digital_opening_number"],202)
        self.assertIn("Vat.gr.1444_0202.jp2",x["source_image"])
        self.assertEqual(x["source_sha256"],"de6fc8f48e57b4b339037805618743e151945e505e162fd3b2168a4a6f9c9f1e")
        self.assertEqual((x["source_dimensions"],x["source_image_size_bytes"]),([2368,1814],609948))
        self.assertFalse(x["manuscript_images_reproduced_in_repo"])
        self.assertIn("not independently identified",x["table_position"])

    def test_four_source_columns_exactly_thirty_handwritten_degrees(self):
        self.assertEqual(set(self.v),{"fire","earth","air","water"})
        self.assertTrue(all(len(arr)==30 for arr in self.v.values()))
        self.assertTrue(all(v is not None for arr in self.v.values() for v in arr))
        self.assertEqual(self.comp["counts"]["vatican_glyphs_read"],120)

    def test_source_glyphs_frozen_first_eight_by_trigon(self):
        expected={
            "fire":["Sun","Jupiter","Venus","Moon","Saturn","Mercury","Venus","Mars"],
            "earth":["Venus","Moon","Saturn","Mercury","Venus","Mars","Sun","Jupiter"],
            "air":["Saturn","Mercury","Venus","Mars","Sun","Jupiter","Venus","Moon"],
            "water":["Venus","Mars","Sun","Jupiter","Venus","Moon","Saturn","Mercury"],
        }
        for tri,first in expected.items():
            self.assertEqual(self.v[tri][:8],first)
            self.assertEqual(first.count("Venus"),2)

    def test_source_only_120_florence_pairs_agree(self):
        x=self.comp["counts"]
        self.assertEqual(x["vatican_florence_agree"],120)
        self.assertEqual(x["florence_glyphs_read"],120)
        self.assertTrue(all(self.v[t]==self.flo["observed_degrees_1_to_30"][t] for t in self.v))

    def test_source_only_119_munich_pairs_agree(self):
        x=self.comp["counts"]
        self.assertEqual(x["munich_readable_glyphs"],119)
        self.assertEqual(x["vatican_munich_agree"],119)
        self.assertEqual(x["vatican_munich_disagree"],[])

    def test_unread_munich_earth_28_never_rewritten(self):
        x=self.comp["counts"]
        self.assertIsNone(self.mun["observed_degrees_1_to_30"]["earth"][27])
        self.assertEqual(self.v["earth"][27:30],["Mars","Mars","Jupiter"])
        self.assertEqual(x["munich_unread_but_vatican_fl_fully_agree"],[("earth",28,"Mars")])

    def test_water_degrees_8_through_10_preserve_source_break(self):
        self.assertEqual(self.v["water"][7:10],["Mercury","Mars","Sun"])
        self.assertEqual(self.comp["counts"]["octet_repetition_failure_by_trigon"]["water"],list(range(9,31)))

    def test_nonclosing_8_slot_exact_negative_by_trigon(self):
        x=self.comp["counts"]
        self.assertEqual(x["octet_repetition_failure_by_trigon"]["fire"],[])
        self.assertEqual(x["octet_repetition_failure_by_trigon"]["air"],[])
        self.assertEqual(x["octet_repetition_failure_by_trigon"]["earth"],[28,29,30])
        self.assertEqual(x["octet_repetition_failure_total"],25)

    def test_disputed_34_source_outcome_preserved(self):
        x=self.comp["counts"]
        self.assertEqual(x["preexisting_source_disagreements"],34)
        self.assertEqual((x["vatican_on_c05_narrative_only"],x["vatican_on_c04_greenbaum_only"],x["vatican_matches_neither"]),(11,1,22))

    def test_one_canon_match_air_27_and_water_negative(self):
        rows={(r["trigon"],r["ordinal_degree"]):r for r in self.comp["rows"]}
        self.assertEqual(rows["air",27]["vatican_observed"],"Venus")
        self.assertEqual(rows["air",27]["c04_greenbaum_sevenfold_day"],"Venus")
        self.assertNotEqual(rows["air",27]["c05_narrative_sevenfold_day"],"Venus")
        r=rows["water",8]
        self.assertEqual((r["vatican_observed"],r["c05_narrative_sevenfold_day"],r["c04_greenbaum_sevenfold_day"]),("Mercury","Venus","Mars"))

    def test_no_false_three_independent_ancient_lineages(self):
        x=self.comp
        self.assertEqual(x["counts"]["three_physical_manuscripts_consulted"],3)
        self.assertEqual(x["counts"]["independent_manuscript_text_families_proved"],0)
        self.assertFalse(x["genetically_independent_witnesses_established"])
        self.assertFalse(x["unique_ancient_authorial_canon_determined"])

    def test_release_and_papyrology_gates_remain_closed(self):
        x=self.vat["negative_uncertainties"]
        self.assertTrue(x["Boer_1958_original_pages_not_read"])
        self.assertTrue(x["Boer_1962_original_pages_not_read"])
        self.assertTrue(x["P_Oxy_LXI_4277_full_original_photo_not_verified"])
        self.assertEqual(x["human_predictive_validations"],0)
        self.assertFalse(x["production_model_modified"])
        self.assertEqual(self.comp["blinded_human_predictive_validations"],0)
        self.assertFalse(self.comp["promoted_production_rule"])


if __name__=="__main__":
    unittest.main()
