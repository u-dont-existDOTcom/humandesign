import unittest
from career_income_scope_B50 import (bhasin_11_malefic_collision,
                                      movement_hunting_8_1_29,
                                      wealth_exchange_2_11, source_selection)


class SourceScopeB50(unittest.TestCase):
    def test_identical_malefic_eleventh_antecedents_opposite_results(self):
        r = bhasin_11_malefic_collision(has_malefic_in_eleventh=True, synthetic=True)
        self.assertTrue(r["v2_gain"] and r["v10_loss"] and r["outcome_collision"])
        self.assertFalse(r["score_allowed"])
        self.assertIsNone(r["canonical_precedence"])

    def test_without_malefic_no_collision(self):
        self.assertFalse(bhasin_11_malefic_collision(has_malefic_in_eleventh=False,
                                                      eleventh_lord_kendra_trine=True,
                                                      synthetic=True)["outcome_collision"])

    def test_synthetic_gate_and_bool(self):
        with self.assertRaises(ValueError):
            bhasin_11_malefic_collision(has_malefic_in_eleventh=True)
        with self.assertRaises(TypeError):
            bhasin_11_malefic_collision(has_malefic_in_eleventh=1, synthetic=True)

    def test_dual_navamsa_hunting_translation_opposition(self):
        r = movement_hunting_8_1_29(navamsa_mode="DUAL", rasi_mode="DUAL", synthetic=True)
        self.assertTrue(r["sanskrit_hunting"] and r["printed_explicit_no_hunting"])
        self.assertTrue(r["hunting_opposition"])

    def test_movable_navamsa_movement_is_not_identical_to_hunting(self):
        r = movement_hunting_8_1_29(navamsa_mode="MOVABLE", rasi_mode="FIXED", synthetic=True)
        self.assertTrue(r["sanskrit_movement"])
        self.assertFalse(r["sanskrit_hunting"] or r["printed_hunting"])

    def test_2_11_exchange_distinct_timing_targets(self):
        r = wealth_exchange_2_11(second_lord_house=11, eleventh_lord_house=2, synthetic=True)
        self.assertTrue(r["shared_antecedent"])
        self.assertNotEqual(r["bhasin_outcome"], r["portuguese_bphs_outcome"])
        self.assertFalse(r["observational_targets_equal"] or r["score_allowed"])

    def test_strongest_only_and_all_scenarios_differ(self):
        r = source_selection({"Sun": 1, "Moon": 5, "Saturn": 2}, synthetic=True)
        self.assertEqual(r["strongest_planets"], ["Moon"])
        self.assertEqual(r["all_contributing_planets"], ["Moon", "Saturn", "Sun"])
        self.assertIsNone(r["source_selection_canonical"])

    def test_ties_and_bad_strengths(self):
        r = source_selection({"Moon": 5, "Sun": 5}, synthetic=True)
        self.assertEqual(r["strongest_planets"], ["Moon", "Sun"])
        with self.assertRaises(ValueError):
            source_selection({"Moon": -1}, synthetic=True)
        with self.assertRaises(ValueError):
            source_selection({"Moon": 5})


if __name__ == "__main__":
    unittest.main()
