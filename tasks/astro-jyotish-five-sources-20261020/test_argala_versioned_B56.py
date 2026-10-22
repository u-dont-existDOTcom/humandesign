import unittest
from argala_versioned_B56 import (PRIMARY, SECONDARY_TEXTUALLY_SHARED,
    EpistemicGate, sign_at_house, primary_pairs, third_house_special_versions,
    node_reference_versions, obstruction_by_count, caturthamsa_quarter,
    opposing_quarter_pair)

class ArgalaVariantsB56(unittest.TestCase):
    def test_primary_pairs_exact(self):
        self.assertEqual(PRIMARY,((2,12),(4,10),(11,3)))
        self.assertEqual(SECONDARY_TEXTUALLY_SHARED,((5,9),))
    def test_sign_count_identity(self):
        self.assertEqual(sign_at_house(0,1),0)
        self.assertEqual(sign_at_house(0,12),11)
        self.assertEqual(sign_at_house(0,12,True),1)
    def test_invalid_sign_count(self):
        for x in (-1,12,True):
            with self.assertRaises(ValueError):sign_at_house(x,3)
    def test_invalid_house(self):
        for x in (0,13,True):
            with self.assertRaises(ValueError):sign_at_house(0,x)
    def test_zero_third(self):
        r=third_house_special_versions(0,2)
        self.assertFalse(r['RATH_third_argala_exists'] or r['BPHS_TRANSLATED_viparita_argala_3plus'])
    def test_one_third_one_eleventh_conflict(self):
        r=third_house_special_versions(1,1)
        self.assertTrue(r['RATH_third_argala_unobstructed'])
        self.assertTrue(r['VENKATESHA_obstruction_admissible_for_one_or_two'])
        self.assertTrue(r['RATH_VENKATESHA_conflict'])
    def test_two_third_three_eleventh_conflict(self):
        r=third_house_special_versions(2,3)
        self.assertTrue(r['RATH_VENKATESHA_conflict'])
        self.assertFalse(r['VENKATESHA_many_malefics_unobstructed_proxy_3plus'])
    def test_three_third_proxy_not_source_fact(self):
        r=third_house_special_versions(3,2)
        self.assertTrue(r['VENKATESHA_many_malefics_unobstructed_proxy_3plus'])
        self.assertTrue(r['BPHS_TRANSLATED_viparita_argala_3plus'])
        self.assertFalse(r['BPHS_SANSKRIT_exact_three_threshold_verified'])
    def test_no_eleventh_obstruction_detected(self):
        r=third_house_special_versions(1,0)
        self.assertFalse(r['VENKATESHA_obstruction_admissible_for_one_or_two'])
    def test_invalid_occupancies(self):
        for a,b in ((-1,0),(0,-1),(10,0),(0,True)):
            with self.assertRaises(ValueError):third_house_special_versions(a,b)
    def test_rahu_reverse_scope_differs(self):
        r=node_reference_versions(0,'RAHU')
        self.assertTrue(r['variants_disagree'])
        self.assertNotEqual(r['RATH_JAIMINI_SUTRA'],r['BPHS_PORTUGUESE_INTERPRETATION'])
    def test_ketu_reverse_scope_agrees_not_validation(self):
        r=node_reference_versions(0,'KETU')
        self.assertFalse(r['variants_disagree'])
        self.assertEqual(r['RATH_JAIMINI_SUTRA'],r['BPHS_PORTUGUESE_INTERPRETATION'])
        self.assertFalse(r['score_allowed'])
    def test_node_invalid(self):
        with self.assertRaises(ValueError):node_reference_versions(0,'SUN')
    def test_equally_many_is_not_resolved_by_sanskrit(self):
        r=obstruction_by_count(2,2)
        self.assertTrue(r['RATH_equal_bandhana_if_nonempty'])
        self.assertIsNone(r['equal_outcome_canonical'])
    def test_count_less_obstructor_ineffective(self):
        self.assertTrue(obstruction_by_count(2,1)['VYAKHYA_and_BPHS_fewer_obstructors_ineffective'])
    def test_zero_zero_not_bandhana(self):
        self.assertFalse(obstruction_by_count(0,0)['RATH_equal_bandhana_if_nonempty'])
    def test_invalid_count(self):
        with self.assertRaises(ValueError):obstruction_by_count(True,2)
    def test_four_quarters(self):
        self.assertEqual([caturthamsa_quarter(x) for x in (0,7.5,15,22.5,29.999)],[1,2,3,4,4])
    def test_quarter_cross_pairs(self):
        self.assertTrue(opposing_quarter_pair(0,29))
        self.assertTrue(opposing_quarter_pair(8,20))
        self.assertFalse(opposing_quarter_pair(0,8))
    def test_invalid_quarter(self):
        with self.assertRaises(ValueError):caturthamsa_quarter(30)
    def test_scoring_always_blocked(self):
        self.assertFalse(EpistemicGate().score_allowed)
        self.assertFalse(third_house_special_versions(3,0)['score_allowed'])

if __name__=='__main__':unittest.main()
