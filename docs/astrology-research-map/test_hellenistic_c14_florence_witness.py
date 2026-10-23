"""C14 source-critical Florence Plut.28.7 against Munich Cod.graec.170.

A second physical historical manuscript is not an independent predictive
human validation, nor proof the two codices descend from independent exemplars.
All 120 Florence labels and source-image SHA are a manual photographic witness,
not generated from any of the period hypotheses under comparison.
"""
import unittest
from paulus_florence_munich_comparison_c14 import florence_source, cross_codex_matrix

EXPECTED_FIRE=["Sun","Jupiter","Venus","Moon","Saturn","Mercury","Venus","Mars",
               "Sun","Jupiter","Venus","Moon","Saturn","Mercury","Venus","Mars",
               "Sun","Jupiter","Venus","Moon","Saturn","Mercury","Venus","Mars",
               "Sun","Jupiter","Venus","Moon","Saturn","Mercury"]
EXPECTED_EARTH=["Venus","Moon","Saturn","Mercury","Venus","Mars","Sun","Jupiter",
                "Venus","Moon","Saturn","Mercury","Venus","Mars","Sun","Jupiter",
                "Venus","Moon","Saturn","Mercury","Venus","Mars","Sun","Jupiter",
                "Venus","Moon","Saturn","Mars","Mars","Jupiter"]
EXPECTED_AIR=["Saturn","Mercury","Venus","Mars","Sun","Jupiter","Venus","Moon",
              "Saturn","Mercury","Venus","Mars","Sun","Jupiter","Venus","Moon",
              "Saturn","Mercury","Venus","Mars","Sun","Jupiter","Venus","Moon",
              "Saturn","Mercury","Venus","Mars","Sun","Jupiter"]
EXPECTED_WATER=["Venus","Mars","Sun","Jupiter","Venus","Moon","Saturn","Mercury",
                "Mars","Sun","Jupiter","Venus","Moon","Saturn","Mercury","Venus",
                "Mars","Sun","Jupiter","Venus","Moon","Saturn","Mercury","Venus",
                "Mars","Sun","Jupiter","Venus","Moon","Saturn"]


class TestC14FlorenceSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src=florence_source()
        cls.summary=cross_codex_matrix()
        cls.vals=cls.src["observed_degrees_1_to_30"]

    def test_actual_14th_century_source_and_provenance(self):
        s=self.src["source"]
        self.assertEqual(s["shelfmark"],"Plut. 28.7")
        self.assertEqual(s["catalogue_century"],"fourteenth century / 1301–1400")
        self.assertEqual((s["folio"],s["image_index_in_iiif"]),("168v",343))
        self.assertIn("plutei:667740",s["image"])
        self.assertEqual(s["original_image_dimensions"],[2910,3779])
        self.assertEqual(s["original_image_size_bytes"],1177330)
        self.assertEqual(s["image_sha256"],"fa84f5499c1131cd148ba5c1461a85d7700d0b793e41b0e23c1fbadc678e2d75")
        self.assertFalse(s["image_stored_in_repo"])

    def test_exact_four_columns_complete_and_all_planets_known(self):
        self.assertEqual(set(self.vals),{"fire","earth","air","water"})
        self.assertEqual(len([x for a in self.vals.values() for x in a]),120)
        self.assertTrue(all(len(v)==30 for v in self.vals.values()))
        self.assertTrue(all(v is not None for a in self.vals.values() for v in a))

    def test_fire_full_literal_source_fixture(self):
        self.assertEqual(self.vals["fire"],EXPECTED_FIRE)

    def test_earth_full_literal_exception_fixture(self):
        self.assertEqual(self.vals["earth"],EXPECTED_EARTH)

    def test_air_full_literal_source_fixture(self):
        self.assertEqual(self.vals["air"],EXPECTED_AIR)

    def test_water_full_literal_phase_shift_fixture(self):
        self.assertEqual(self.vals["water"],EXPECTED_WATER)

    def test_bounded_witness_agreement_not_120_of_120_claim(self):
        s=self.summary
        self.assertEqual(s["florence_total_read"],120)
        self.assertEqual(s["munich_read"],119)
        self.assertEqual(s["cross_codex_cell_agreements"],119)
        self.assertEqual(s["cross_codex_cell_disagreements"],[])

    def test_munich_unknown_still_unknown_florence_mars(self):
        self.assertEqual(self.summary["munich_unresolved_even_after_other_witness"],[("earth",28,"Mars")])
        r=next(x for x in self.summary["rows"] if (x["trigon"],x["degree"])==("earth",28))
        self.assertIsNone(r["munich"])
        self.assertEqual(r["florence"],"Mars")
        self.assertFalse(r["two_codices_comparable"])
        self.assertIsNone(r["matches_munich"])

    def test_two_mars_at_earth_28_and_29_are_not_repaired(self):
        self.assertEqual(self.vals["earth"][27:30],["Mars","Mars","Jupiter"])
        marks=self.src["confidence_notes"]
        self.assertEqual([x["degree"] for x in marks if x["trigon"]=="earth"],[28,29,30])
        self.assertFalse(self.summary["manuscript_genealogy_independence_confirmed"])

    def test_two_codices_share_water_phase_break(self):
        x=self.summary["florence_not_naive_eightfold"]
        self.assertEqual(x["water"],list(range(9,31)))
        self.assertEqual(x["fire"],[])
        self.assertEqual(x["air"],[])
        self.assertEqual(x["earth"],[28,29,30])
        self.assertEqual(self.summary["eightfold_difference_count"],25)

    def test_original_34_dispute_outcome_from_florence(self):
        x=self.summary
        self.assertEqual(x["preexisting_disputed_cells"],34)
        self.assertEqual((x["florence_matches_narrative_only"],x["florence_matches_corrected_only"],x["florence_matches_neither"]),(11,1,22))
        self.assertEqual(sum((x["florence_matches_narrative_only"],x["florence_matches_corrected_only"],x["florence_matches_neither"])),34)

    def test_source_not_authoritative_ancient_or_human_model(self):
        s=self.summary;c=self.src["caveats"]
        self.assertFalse(s["ancient_author_preferred_algorithm_confirmed"])
        self.assertFalse(s["manuscript_genealogy_independence_confirmed"])
        self.assertFalse(s["production_model_promoted"])
        self.assertEqual(s["human_predictive_validations"],0)
        self.assertTrue(c["glyphs_not_independently_blind_double_coded"])
        self.assertTrue(c["manuscript_copies_may_share_ancestor"])
        self.assertEqual(c["human_predictive_validations"],0)


if __name__=="__main__":
    unittest.main()
