"""C24 source image glyph registry + partial second-slot diagnostic.

A green unit test checks consistency with stored, nonblind candidate readings.
It is not independent manuscript palaeography or blinded human prediction.
"""
import unittest

from paulus_c24_commentary_120_first_80_second import (
    source,observed_slot,research_comparison
)
from paulus_trigon_narrative_c05 import narrative_degree_ruler


class TestC24FlorenceSourceScope(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.w=source()
        cls.a=research_comparison()
        cls.rows={(r["trigon"],r["degree"]):r for r in cls.a["rows"]}

    def test_primary_folio_photo_provenance(self):
        x=self.w["source"]
        self.assertEqual(x["shelfmark"],"Plut. 28.14")
        self.assertEqual((x["folio"],x["IIIF_canvas"]),("204v",421))
        self.assertEqual(x["source_image_dimensions"],[2536,2572])
        self.assertEqual(x["source_image_bytes"],741471)
        self.assertEqual(x["source_sha256"],"52a1b8b4f8d67514c815a56178d54c1d45e03a991a09b48417f599ff3336128e")
        self.assertFalse(x["image_files_stored_in_repo"])

    def test_four_distinct_triplicity_columns_all_30_first_slot_positions(self):
        a=self.w["source_first_slot_ordinals_1_to_30"]
        self.assertEqual(set(a),{"fire","earth","air","water"})
        self.assertEqual([len(a[t]) for t in ("fire","earth","air","water")],[30]*4)
        self.assertEqual(self.a["first_slot_source_cells_provisionally_read"],120)
        self.assertEqual(len(self.w["method"]["image_position_y_centers_approx"]),30)

    def test_c23_first_eight_preserved_source_first(self):
        vals=self.w["source_first_slot_ordinals_1_to_30"]
        self.assertEqual(vals["fire"][:8],["Sun","Jupiter","Venus","Moon","Saturn","Mercury","Mars","Sun"])
        self.assertEqual(vals["earth"][:8],["Venus","Moon","Saturn","Mercury","Mars","Sun","Jupiter","Venus"])
        self.assertEqual(vals["air"][:8],["Saturn","Mercury","Mars","Sun","Jupiter","Venus","Moon","Saturn"])
        self.assertEqual(vals["water"][:8],["Venus","Mars","Sun","Jupiter","Moon","Saturn","Mercury","Venus"])

    def test_late_rows_recorded_as_literal_source_array(self):
        vals=self.w["source_first_slot_ordinals_1_to_30"]
        self.assertEqual(vals["fire"][24:30],["Moon","Saturn","Mercury","Mars","Sun","Jupiter"])
        self.assertEqual(vals["earth"][24:30],["Mercury","Mars","Sun","Jupiter","Venus","Moon"])
        self.assertEqual(vals["air"][24:30],["Sun","Jupiter","Venus","Moon","Saturn","Mercury"])
        self.assertEqual(vals["water"][24:30],["Jupiter","Moon","Saturn","Mercury","Venus","Mars"])

    def test_sparse_second_slot_only_80_actual_values(self):
        a=self.w["source_second_slot_ordinals_1_to_30_sparse"]
        for tr in a:
            self.assertEqual(len(a[tr]),30)
            self.assertEqual([d for d,v in enumerate(a[tr],1) if v is None],
                             [9,10,17,18,19,20,21,22,23,24])
        self.assertEqual(self.a["second_slot_source_cells_provisionally_read"],80)
        self.assertEqual(self.a["second_slot_source_cells_still_unread"],40)
        self.assertTrue(self.w["method"]["second_slot_null_is_source_unknown_not_negative_result"])

    def test_unread_second_slot_explicitly_raises_not_inferred(self):
        for t in ("fire","earth","air","water"):
            for d in (9,10,17,18,19,20,21,22,23,24):
                with self.assertRaises(ValueError):
                    observed_slot(t,d,"second")

    def test_invalid_source_requests_fail_closed(self):
        for bad in (-1,0,31,True,3.5,"2"):
            with self.assertRaises(ValueError):
                observed_slot("water",bad)
        for bad in ("","north","day"):
            with self.assertRaises(ValueError):
                observed_slot(bad,2)
        with self.assertRaises(ValueError):
            observed_slot("water",2,"not_a_slot")

    def test_source_first_mixed_historical_daytime_results(self):
        s=self.a
        self.assertEqual((s["first_slot_day_C05_narrative_agreements"],
                          s["first_slot_day_C04_printed_agreements"],
                          s["first_slot_old_Paulus_ms_family_agreements"]),(104,102,20))
        self.assertEqual(s["first_slot_matching_neither_day_rule"],0)
        self.assertEqual(s["per_trigon"]["fire"]["first_C05"],30)
        self.assertEqual(s["per_trigon"]["earth"]["first_C04"],30)
        self.assertEqual(s["per_trigon"]["air"]["first_C04"],30)
        self.assertEqual(s["per_trigon"]["water"]["first_C05"],30)

    def test_34_original_Greenbaum_narrative_source_disputes_unchanged(self):
        s=self.a
        self.assertEqual(s["previous_C04_C05_day_disagreement_cells"],34)
        self.assertEqual((
            s["source_first_in_disputed_cells_align_narrative_only"],
            s["source_first_in_disputed_cells_align_C04_only"],
            s["source_first_in_disputed_cells_align_neither"]
        ),(18,16,0))

    def test_sparse_second_slot_pair_exchange_is_diagnostic(self):
        s=self.a
        self.assertEqual(s["second_slot_pair_exchange_matches"],80)
        self.assertEqual(s["second_slot_matches_independent_C05_night"],40)
        self.assertTrue(self.w["hypotheses_to_test_separately"]["global_second_slot_pair_exchange_not_yet_verified_across_all_120"])
        self.assertFalse(s["second_slot_night_sect_palaeographically_verified"])

    def test_example_night_scheme_non_equivalence_kept(self):
        r=self.rows["fire",7]
        self.assertEqual((r["source_first"],r["source_second"],r["night_narrative_diagnostic"]),("Mars","Sun","Mars"))
        self.assertTrue(r["source_second_pair_exchange_agrees"])
        self.assertFalse(r["source_second_matches_night_narrative"])
        self.assertEqual(self.rows["water",8]["source_first"],"Venus")
        self.assertEqual(self.rows["water",8]["day_Greenbaum_printed"],"Mars")
        self.assertEqual(self.rows["water",8]["older_Paulus_manuscript"],"Mercury")

    def test_provisional_source_glyphs_are_not_blind_or_authoritative(self):
        p=self.w["method"]
        self.assertTrue(p["possible_confirmation_bias"])
        self.assertFalse(p["independent_second_palaeographer"])
        self.assertTrue(p["no_authoritative_greek_sect_heading_deciphered"])
        self.assertTrue(p["all_first_slot_candidate_labels_not_ancient_authorial_autograph"])
        self.assertFalse(self.a["Boer_1958_1962_printed_critical_apparatus_examined"])

    def test_no_human_validity_or_scoring_promotion(self):
        g=self.w["closed_gates"]
        self.assertEqual(g["human_predictive_validations"],0)
        self.assertEqual((g["P_Oxy_4277_old_matches"],g["P_Oxy_4277_old_failures"]),(1,2))
        self.assertFalse(g["production_model_modified"])
        self.assertFalse(g["cross_tradition_model_modified"])
        self.assertFalse(g["gansten_Kindle_ebook_extracted"])
        self.assertFalse(self.a["production_model_modified"])
        self.assertEqual(self.a["human_predictive_validations"],0)


if __name__=="__main__":
    unittest.main()
