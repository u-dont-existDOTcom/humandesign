"""C24 Stage B source-photo audit: 240 tentative first/second planet labels.

Includes negative controls against silently conflating a pairwise manuscript
exchange pattern with C05's nighttime narrative, or against rewriting Stage A
unknowns post hoc. Not a blinded palaeographic validation or human prediction.
"""
import unittest

from paulus_c24_complete_240_source_comparison import (
    complete_provisional_240,stage_b_source
)
from paulus_c24_commentary_120_first_80_second import (
    source as stage_a_source,observed_slot
)


class TestC24SecondStage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=stage_a_source()
        cls.b=stage_b_source()
        cls.s=complete_provisional_240()
        cls.rows={(r["trigon"],r["ordinal_degree"]):r for r in cls.s["rows"]}

    def test_same_exact_library_photo_and_manuscript_id(self):
        self.assertEqual(self.b["source"]["shelfmark"],"Plut. 28.14")
        self.assertEqual(self.b["source"]["folio"],"204v")
        self.assertEqual(self.b["source"]["original_sha256"],
                         self.a["source"]["source_sha256"])
        self.assertFalse(self.b["source"]["source_image_stored_in_Git"])

    def test_first_and_second_literal_arrays_are_complete_only_in_stage_b(self):
        self.assertEqual(self.s["provisional_first_slot_glyphs"],120)
        self.assertEqual(self.s["provisional_second_slot_glyphs"],120)
        for tr,v in self.b["source_second_slot_ordinals_1_to_30"].items():
            self.assertEqual(len(v),30)
            self.assertTrue(all(x is not None for x in v))

    def test_previous_partial_readings_preserved_not_filled_retroactively(self):
        self.assertEqual(self.s["earlier_stage_A_second_cells_preserved"],80)
        self.assertEqual(self.s["new_stage_B_second_cells_read"],40)
        for tr in ("fire","earth","air","water"):
            self.assertIsNone(self.a["source_second_slot_ordinals_1_to_30_sparse"][tr][8])
            with self.assertRaises(ValueError):
                observed_slot(tr,9,"second")
            self.assertIsNotNone(self.b["source_second_slot_ordinals_1_to_30"][tr][8])

    def test_source_first_eight_second_slot_preserves_C23_night_openings(self):
        x=self.b["source_second_slot_ordinals_1_to_30"]
        self.assertEqual(x["fire"][:8],
                         ["Jupiter","Sun","Moon","Venus","Mercury","Saturn","Sun","Mars"])
        self.assertEqual(x["earth"][:8],
                         ["Moon","Venus","Mercury","Saturn","Sun","Mars","Venus","Jupiter"])
        self.assertEqual(x["air"][:8],
                         ["Mercury","Saturn","Sun","Mars","Venus","Jupiter","Saturn","Moon"])
        self.assertEqual(x["water"][:8],
                         ["Mars","Venus","Jupiter","Sun","Saturn","Moon","Venus","Mercury"])

    def test_late_direct_source_pairs_are_kept_in_register(self):
        x=self.b["source_second_slot_ordinals_1_to_30"]
        self.assertEqual(x["fire"][24:30],["Saturn","Moon","Mars","Mercury","Jupiter","Sun"])
        self.assertEqual(x["earth"][24:30],["Mars","Mercury","Jupiter","Sun","Moon","Venus"])
        self.assertEqual(x["air"][24:30],["Jupiter","Sun","Moon","Venus","Mercury","Saturn"])
        self.assertEqual(x["water"][24:30],["Moon","Jupiter","Mercury","Saturn","Mars","Venus"])

    def test_visual_transcription_pair_exchange_diagnostic_matches_120(self):
        self.assertEqual(self.s["pairwise_exchange_matches"],120)
        self.assertTrue(all(x["pairwise_exchange_matches"]==30 for x in self.s["per_trigon"].values()))
        self.assertEqual(self.s["unread_second_source_cells_from_stage_B"],0)
        self.assertTrue(self.s["unblinded_glyph_names_not_independent_expert_certification"])

    def test_not_the_same_as_C05_nighttime_rule(self):
        self.assertEqual(self.s["C05_night_narrative_matches_second_slot"],48)
        self.assertEqual([self.s["per_trigon"][t]["C05_night_matches"] for t in ("fire","earth","air","water")],
                         [14,14,6,14])
        r=self.rows["fire",7]
        self.assertEqual((r["first_slot"],r["second_slot"],r["nighttime_C05_narrative"]),
                         ("Mars","Sun","Mars"))
        self.assertFalse(r["second_matches_C05_night"])

    def test_stage_b_new_middle_and_early_gap_source_examples(self):
        self.assertEqual((self.rows["fire",9]["second_slot"],self.rows["fire",10]["second_slot"]),
                         ("Venus","Jupiter"))
        self.assertEqual((self.rows["water",21]["second_slot"],self.rows["water",22]["second_slot"]),
                         ("Venus","Mercury"))
        self.assertTrue(self.rows["water",21]["stage_B_second_newly_read"])
        self.assertTrue(self.rows["fire",9]["stage_B_second_newly_read"])

    def test_no_authorial_night_rule_or_predictive_validity_admitted(self):
        self.assertTrue(self.s["day_night_rubric_not_verified"])
        self.assertTrue(self.s["cannot_use_pairwise_swap_as_production_night_rule"])
        self.assertFalse(self.b["methodological_limits"]["original_Boer_1962_printed_diagram_compared"])
        self.assertFalse(self.b["methodological_limits"]["production_scorer_changed"])
        self.assertEqual(self.s["human_predictive_validations"],0)
        self.assertFalse(self.s["production_model_changed"])


if __name__=="__main__":
    unittest.main()
