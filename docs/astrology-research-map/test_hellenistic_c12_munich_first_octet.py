"""C12: historical manuscrip­t first-octet transcription and no-skip diagnostic.

Positive arithmetic tests are NOT independent palaeography certification or
evidence astrology predicts human traits. Manuscript pages 9..30 unresolved.
"""
import unittest

from paulus_munich_first_octet_c12 import (
    direct_octet_comparison,
    eight_slots_without_skipping,
    manuscript_first_octet,
    witness,
)


class TestC12MunichManuscript(unittest.TestCase):
    def setUp(self):
        self.w=witness()
        self.s=direct_octet_comparison()

    def test_original_manuscript_locator_exact(self):
        p=self.w["source"]
        self.assertEqual(p["shelfmark"],"Cod. graec. 170")
        self.assertEqual((p["ms_page"],p["digital_image"]),(65,81))
        self.assertIn("bsb00131007_00081",p["photo"])
        self.assertIn("presentation/v3/bsb00131007",p["iiif_manifest"])

    def test_four_triplicities_cover_exactly_twelve_signs(self):
        signs=self.w["trigon_signs"]
        self.assertEqual(set(signs),{"fire","earth","air","water"})
        self.assertEqual([len(v) for v in signs.values()],[3]*4)
        self.assertEqual(len(set(n for vs in signs.values() for n in vs)),12)

    def test_first_eight_literal_source_matrix_frozen(self):
        expected={
            "fire":["Sun","Jupiter","Venus","Moon","Saturn","Mercury","Venus","Mars"],
            "earth":["Venus","Moon","Saturn","Mercury","Venus","Mars","Sun","Jupiter"],
            "air":["Saturn","Mercury","Venus","Mars","Sun","Jupiter","Venus","Moon"],
            "water":["Venus","Mars","Sun","Jupiter","Venus","Moon","Saturn","Mercury"],
        }
        self.assertEqual(self.w["eight_by_trigon"],expected)
        for tri,vals in expected.items():
            for deg,planet in enumerate(vals,1):
                self.assertEqual(manuscript_first_octet(tri,deg),planet)

    def test_all_four_octets_contain_duplicate_venus_and_seven_unique_planets(self):
        for tri,values in self.w["eight_by_trigon"].items():
            self.assertEqual(values.count("Venus"),2,tri)
            self.assertEqual(len(set(values)),7,tri)
            self.assertEqual(tuple(values),eight_slots_without_skipping(tri),tri)

    def test_missing_9_through_30_are_explicitly_not_transcribed(self):
        with self.assertRaises(ValueError):
            manuscript_first_octet("air",9)
        with self.assertRaises(ValueError):
            manuscript_first_octet("water",30)
        for out_of_range in (0,-1,1.5,True):
            with self.assertRaises(ValueError):
                manuscript_first_octet("fire",out_of_range)
        with self.assertRaises(ValueError):
            manuscript_first_octet("imaginary",1)
        self.assertFalse(self.s["original_ms_120_decoded"])

    def test_source_only_nine_of_34_relevant_first_octet_positions(self):
        s=self.s
        self.assertEqual(s["inspected_cells"],32)
        self.assertEqual(s["formerly_disputed_visible_cells"],9)
        self.assertEqual(s["uninspected_of_previous_34"],25)
        self.assertEqual(s["visible_disputed_match_narrative"],8)
        self.assertEqual(s["visible_disputed_match_corrected_day"],0)
        self.assertEqual(s["visible_disputed_match_neither"],1)
        subset={(r["trigon"],r["ordinal_degree"]) for r in s["rows"] if r["previous_34_disputed_subset"]}
        self.assertEqual(subset,{("air",d) for d in (3,4,5,6)}|{("water",d) for d in (1,2,3,4,8)})

    def test_water_degree_eight_matches_neither_seven_cycle(self):
        r=next(x for x in self.s["rows"] if (x["trigon"],x["ordinal_degree"])==("water",8))
        self.assertEqual((r["direct_manuscript_read"],r["seven_unique_narrative"],r["greenbaum_corrected_day"]),
                         ("Mercury","Venus","Mars"))
        self.assertFalse(r["agrees_narrative"])
        self.assertFalse(r["agrees_corrected_day"])

    def test_day_scope_inferred_not_rubric_proved(self):
        self.assertIn("INFERRED_DAY",self.w["day_night"])
        self.assertEqual(self.w["eight_by_trigon"]["fire"][:2],["Sun","Jupiter"])
        self.assertEqual(self.w["eight_by_trigon"]["earth"][:2],["Venus","Moon"])
        self.assertIn("FIRST_EIGHT_ONLY",self.w["scope"])

    def test_no_astrology_predictive_claim_or_production_promotion(self):
        self.assertEqual(self.s["human_predictive_validations"],0)
        self.assertFalse(self.s["accepted_as_canonical_day_rule"])
        self.assertFalse(self.w["open"]["production_scored"])
        self.assertFalse(self.w["open"]["poxy_4277_image_verified"])
        self.assertFalse(self.w["open"]["boer_greek_collated"])


if __name__=="__main__":
    unittest.main()
