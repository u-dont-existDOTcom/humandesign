"""C23 source-only 14th-century commentary-manuscript photo audit.

Glyph normalization was not blind or independently checked; these tests
protect the limited transcription, not the authenticity of an original
4th-century authorial table and not astrological human predictive accuracy.
"""
import unittest

from paulus_c23_commentary_first_eight import (
    witness,source_slot,first_eight_source_comparison
)


class TestC23CommentaryManuscript(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.w=witness()
        cls.comp=first_eight_source_comparison()

    def test_exact_florence_14c_source_locator_and_hash(self):
        a=self.w["source"]
        self.assertEqual(a["shelfmark"],"Plut. 28.14")
        self.assertEqual(a["figure_folio"],"204v")
        self.assertEqual((a["figure_canvas_index"],a["manifest_canvas_count"]),(421,670))
        self.assertIn("plutei:565809",a["figure_iiif_photo"])
        self.assertEqual(a["figure_dimensions"],[2536,2572])
        self.assertEqual(a["figure_bytes"],741471)
        self.assertEqual(a["figure_sha256"],"52a1b8b4f8d67514c815a56178d54c1d45e03a991a09b48417f599ff3336128e")
        self.assertFalse(a["source_photographs_redistributed"])

    def test_pages_preceding_and_following_individually_observed(self):
        a=self.w["source"]
        self.assertIn("204r",a["preceding_folio"])
        self.assertIn("205r",a["following_folio"])
        self.assertEqual(a["preceding_sha256"],"c450625b85b0b655999b700b32c03ef590d33585c3f5b5789e4082f1dd8b78d0")
        self.assertEqual(a["following_sha256"],"3b92483a923a7dfa8754ea79d67caf8967ab75dc6e010dac8acc345857474bd5")
        self.assertIn("366–437",a["inspected_segment"])

    def test_ancient_caption_and_exact_structural_bounds(self):
        a=self.w["table_geometry"]
        self.assertEqual(a["ordinal_degrees_each"],30)
        self.assertEqual(a["paired_planet_assignments_per_degree"],2)
        self.assertEqual(a["double_line_bands_per_column"],15)
        self.assertEqual(len(a["four_columns"]),4)
        self.assertEqual(sum(len(s) for s in a["four_columns"].values()),12)
        self.assertFalse(a["greek_source_rubric_sect_certified"])
        self.assertFalse(a["entire_30x4x2_cells_read"])
        self.assertIn("κανόνιον",self.w["source"]["first_line_approx_greek"])

    def test_source_first_octets_frozen_as_handwritten_candidates(self):
        expected={
            "fire":["Sun","Jupiter","Venus","Moon","Saturn","Mercury","Mars","Sun"],
            "earth":["Venus","Moon","Saturn","Mercury","Mars","Sun","Jupiter","Venus"],
            "air":["Saturn","Mercury","Mars","Sun","Jupiter","Venus","Moon","Saturn"],
            "water":["Venus","Mars","Sun","Jupiter","Moon","Saturn","Mercury","Venus"],
        }
        self.assertEqual(self.w["first_slot_first_eight_observed_by_trigon"],expected)
        for trigon,values in expected.items():
            for ordinal,planet in enumerate(values,1):
                self.assertEqual(source_slot(trigon,ordinal),planet)

    def test_second_slot_only_first_degree_is_admitted(self):
        self.assertEqual(self.w["second_slot_degree_one_observed_by_trigon"],
                         {"fire":"Jupiter","earth":"Moon","air":"Mercury","water":"Mars"})
        self.assertEqual(self.comp["night_opening_pairs_match_C05_night"],4)
        self.assertFalse(self.comp["manuscript_day_night_abbreviations_independently_verified"])

    def test_reject_all_unread_degrees_and_slot_ranges(self):
        for trigon in ("fire","earth","air","water"):
            for d in (9,15,22,30):
                with self.assertRaises(ValueError):
                    source_slot(trigon,d)
            with self.assertRaises(ValueError):
                source_slot(trigon,2,"second")
        for invalid in (0,-1,31,True,2.0,"5"):
            with self.assertRaises(ValueError):
                source_slot("water",invalid)
        for invalid in ("north","day",""):
            with self.assertRaises(ValueError):
                source_slot(invalid,1)
        with self.assertRaises(ValueError):
            source_slot("water",1,"third")

    def test_only_32_first_slot_source_positions_measured(self):
        c=self.comp
        self.assertEqual(c["total_directly_sampled_positions"],32)
        self.assertTrue(c["remaining_22_degrees_x4_untranscribed"])
        self.assertEqual(len(c["rows"]),32)

    def test_direct_commentary_vs_three_prior_methods(self):
        c=self.comp
        self.assertEqual(c["agrees_C05_day_narrative"],28)
        self.assertEqual(c["agrees_C04_printed_day"],27)
        self.assertEqual(c["agrees_old_Paulus_ms_family"],16)

    def test_nine_preexisting_disputes_split_by_trigon(self):
        c=self.comp
        self.assertEqual(c["previously_disputed_subset"],9)
        self.assertEqual((c["disputed_align_C05_only"],c["disputed_align_C04_only"],
                          c["disputed_align_neither"]),(5,4,0))
        picks=[(x["trigon"],x["ordinal_degree"]) for x in c["rows"]
               if x["preexisting_C04_C05_disputed"]]
        self.assertEqual(picks,
            [("air",d) for d in (3,4,5,6)]+[("water",d) for d in (1,2,3,4,8)])

    def test_cancer_eighth_distinct_glyphs_preserved(self):
        case=next(x for x in self.comp["rows"]
                  if x["trigon"]=="water" and x["ordinal_degree"]==8)
        self.assertEqual((case["new_commentary_first_slot"],case["narrative_day"],
                          case["printed_Greenbaum_day"],case["old_Paulus_ms_candidate"]),
                         ("Venus","Venus","Mars","Mercury"))
        self.assertTrue(case["matches_narrative"])
        self.assertFalse(case["matches_printed"])
        self.assertFalse(case["matches_old_ms"])

    def test_daytime_scope_and_copy_genealogy_remain_uncertified(self):
        f=self.w["source_reading_flags"]
        self.assertFalse(f["independent_blind_palaeographer_checked"])
        self.assertTrue(f["source_reader_prior_model_prediction_patterns_known"])
        self.assertTrue(f["comparing_diurnal_sect_is_conditional_on_slot_order"])
        self.assertFalse(self.w["unresolved"]["nighttime_status_confirmed_in_own_rubric"])
        self.assertFalse(self.w["unresolved"]["commentary_ascribed_to_individual_Olympiodorus_certain"])

    def test_no_model_promotion_or_human_accuracy_claims(self):
        z=self.w["unresolved"]
        self.assertFalse(z["full_240_photo_glyphs_reindependently_read"])
        self.assertFalse(z["original_Boer_1958_chapter32_critical_apparatus_read"])
        self.assertFalse(z["Boer_1962_printed_commentary_ch34_apparatus_read"])
        self.assertFalse(z["production_scorer_changed"])
        self.assertEqual((z["previous_P_Oxy4277_monomoiria_C05_matches"],
                          z["previous_P_Oxy4277_monomoiria_C05_failures"]),(1,2))
        self.assertEqual(z["real_human_predictive_validations"],0)
        self.assertFalse(self.comp["promoted_production_rule"])


if __name__=="__main__":
    unittest.main()
