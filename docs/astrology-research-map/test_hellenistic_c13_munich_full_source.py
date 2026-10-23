"""C13: source-only first full visual transcript of Munich Cod.graec.170 p65.

Tests protect the recorded source numbers, scope and negative results; they
do NOT establish ancient autograph correctness or human predictive validity.
"""
import json
import unittest
from pathlib import Path

from paulus_munich_full_c13 import (
    manuscript_source, manuscript_model_comparison, observed_glyph_assignment,
    naive_eight_step_hypothesis,
)

HERE=Path(__file__).resolve().parent
C12=json.loads((HERE/"PAULUS_C12_MUNICH_FIRST_OCTET_SOURCE_WITNESS_V1.json").read_text(encoding="utf-8"))


class TestPaulusMunichC13(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s=manuscript_source()
        cls.v=manuscript_model_comparison()

    def test_source_provenance_exact_image_sha_and_pixels(self):
        x=self.s["source"]
        self.assertEqual(x["shelfmark"],"Cod. graec. 170")
        self.assertEqual((x["handwritten_page"],x["bsb_digital_image"]),(65,81))
        self.assertEqual(x["image_sha256"],"371149ee4b769979977935a2c45496bb6065aef4229f2e1168dfac12a89d52fb")
        self.assertEqual(x["image_pixel_size"],[1831,2400])
        self.assertEqual(len(x["horizontal_row_boundaries_y"]),16)
        self.assertFalse(x["image_stored_in_repo"])

    def test_four_transcribed_columns_30_positions_each_not_algorithm_generated(self):
        o=self.s["observed_degrees_1_to_30"]
        self.assertEqual(set(o),{"fire","earth","air","water"})
        self.assertTrue(all(len(a)==30 for a in o.values()))
        self.assertEqual(self.v["total_source_positions"],120)
        self.assertEqual((self.v["read"],self.v["unread"]),(119,1))
        self.assertEqual((self.s["quality"]["definite_planet_labels"],self.s["quality"]["unresolved_planet_labels"]),(119,1))

    def test_first_eight_remain_C12_literal_compatibility(self):
        for t,prior in C12["eight_by_trigon"].items():
            self.assertEqual(self.s["observed_degrees_1_to_30"][t][:8],prior,t)

    def test_fire_and_air_eightfold_pattern_observed_all_30(self):
        v=self.v["by_trigon"]
        self.assertEqual(v["fire"]["eightfold_extrapolation_mismatch_degrees"],[])
        self.assertEqual(v["air"]["eightfold_extrapolation_mismatch_degrees"],[])
        for tri in ("fire","air"):
            self.assertEqual(v[tri]["read_positions"],30)

    def test_water_phase_shift_after_eight_without_uncritical_correction(self):
        obs=self.s["observed_degrees_1_to_30"]["water"]
        first=obs[:8]
        self.assertEqual(obs[8:16],["Mars","Sun","Jupiter","Venus","Moon","Saturn","Mercury","Venus"])
        self.assertEqual(self.v["by_trigon"]["water"]["eightfold_extrapolation_mismatch_degrees"],list(range(9,31)))
        self.assertTrue(all(obs[d-1]==first[(d-8)%8] for d in range(9,31)))
        self.assertEqual(obs[7],"Mercury")
        self.assertEqual(obs[8],"Mars")
        self.assertNotEqual(obs[8],naive_eight_step_hypothesis("water",9))

    def test_earth_late_unresolved_and_two_negative_deviations(self):
        o=self.s["observed_degrees_1_to_30"]["earth"]
        self.assertIsNone(o[27])
        self.assertEqual(o[28:30],["Mars","Jupiter"])
        self.assertEqual(self.v["by_trigon"]["earth"]["unresolved_positions"],[28])
        self.assertEqual(self.v["by_trigon"]["earth"]["eightfold_extrapolation_mismatch_degrees"],[29,30])
        self.assertEqual(self.s["transcription_policy"]["one_ambiguous_position"]["candidates"],["Mercury","Mars"])

    def test_disputed_34_now_compared_directly_all_but_not_adjudicated_canon(self):
        x=self.v["previous_34_disputed"]
        self.assertEqual(x["previous_narrative_greenbaum_dispute_universe"],34)
        self.assertEqual(x["disputed_source_observations_read"],34)
        self.assertEqual(x["disputed_with_unread_manuscript"],[])
        self.assertEqual((x["disputed_source_agrees_narrative_only"],x["disputed_source_agrees_corrected_only"],x["disputed_source_agrees_neither"]),(11,1,22))
        self.assertEqual(11+1+22,34)
        self.assertFalse(self.v["eightfold_hypothesis_is_admitted_canon"])

    def test_one_printed_only_air_27_is_not_overstated(self):
        selected=[r for r in self.v["rows"] if r["prior_day_canon_disputed"] and r["observed_corrected_agreement"]]
        self.assertEqual([(r["trigon"],r["degree"],r["observed"]) for r in selected],[("air",27,"Venus")])
        self.assertNotEqual(selected[0]["narrative_seven_unique_day"],"Venus")

    def test_water_8_and_water_22_preserve_neither_cases(self):
        x={(r["trigon"],r["degree"]):r for r in self.v["rows"]}
        self.assertEqual((x["water",8]["observed"],x["water",8]["narrative_seven_unique_day"],x["water",8]["greenbaum_printed_corrected_day"]),("Mercury","Venus","Mars"))
        self.assertEqual(x["water",22]["observed"],"Saturn")
        self.assertFalse(x["water",22]["observed_narrative_agreement"])
        self.assertFalse(x["water",22]["observed_corrected_agreement"])

    def test_strict_invalid_degree_type_and_trigon(self):
        for value in (0,31,-2,2.0,True):
            with self.assertRaises(ValueError):
                observed_glyph_assignment("air",value)
        with self.assertRaises(ValueError):
            observed_glyph_assignment("wrong",1)

    def test_no_human_prediction_or_source_glyph_certification(self):
        q=self.s["quality"]
        self.assertFalse(q["manuscript_family_collation_completed"])
        self.assertFalse(q["boer_1958_1962_full_apparatus_inspected"])
        self.assertFalse(q["original_oxy4277_image_inspected"])
        self.assertEqual(q["human_predictive_validations"],0)
        self.assertFalse(q["model_promoted"])
        self.assertEqual(self.v["human_predictive_validations"],0)
        self.assertFalse(self.v["production_scoring_changed"])

    def test_not_a_naively_repeated_8_slot_120_cell_fabrication(self):
        d=self.v
        mismatches=sum(len(v["eightfold_extrapolation_mismatch_degrees"]) for v in d["by_trigon"].values())
        self.assertEqual(mismatches,24)
        self.assertEqual(sum(1 for r in d["rows"] if r["observed_eightfold_agreement"] is True),95)
        self.assertEqual(sum(1 for r in d["rows"] if r["observed_eightfold_agreement"] is None),1)


if __name__=="__main__":
    unittest.main()
