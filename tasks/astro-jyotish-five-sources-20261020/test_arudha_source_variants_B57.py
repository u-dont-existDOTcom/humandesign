"""B57 source-calculation diagnostics, not human predictive validation."""
import unittest
import json
from pathlib import Path
from arudha_source_variants_B57 import (
    count_inclusive, nth_from, bhava_arudha, unresolved_two_lords,
    graha_arudha, arudha_degree)


def r(lord_house, mode='RATH_BPHS_CH29', bhava=0):
    return bhava_arudha(bhava_sign=bhava,lord_sign=(bhava+lord_house-1)%12,
                         version=mode,synthetic=True)


class B57ArudhaSourceTests(unittest.TestCase):
    def test_forward_inclusive_count(self):
        self.assertEqual(count_inclusive(0,0),1)
        self.assertEqual(count_inclusive(11,0),2)
        self.assertEqual(count_inclusive(0,11),12)
    def test_nth_from_one_and_twelve(self):
        self.assertEqual(nth_from(5,1),5)
        self.assertEqual(nth_from(5,12),4)
    def test_natural_raw_arudha_third(self):
        self.assertEqual(r(2)['raw_pada_sign'],2)
        self.assertEqual(r(2)['pada_sign'],2)
    def test_rider_first_house_tenth(self):
        self.assertEqual(r(1)['pada_sign'],9)
    def test_rider_seventh_house_tenth(self):
        self.assertEqual(r(7)['pada_sign'],9)
    def test_rider_fourth_house_fourth(self):
        self.assertEqual(r(4)['raw_pada_sign'],6)
        self.assertEqual(r(4)['pada_sign'],3)
    def test_rider_tenth_house_fourth(self):
        self.assertEqual(r(10)['pada_sign'],3)
    def test_rider_output_universe(self):
        self.assertEqual({r(n)['pada_sign']+1 for n in range(1,13)},{3,4,5,9,10,11})
    def test_rider_all_twelve_relative_pairs(self):
        self.assertEqual([r(n)['pada_sign']+1 for n in range(1,13)],
                         [10,3,5,4,9,11,10,3,5,4,9,11])
    def test_venk_fourth_seventh_does_not_equal_rath(self):
        v=r(4,'VENKATESHA_COMMENTARY_LOCAL')
        self.assertEqual(v['pada_sign'],6)
        self.assertNotEqual(v['pada_sign'],r(4)['pada_sign'])
    def test_venk_seventh_first_does_not_equal_rath(self):
        v=r(7,'VENKATESHA_COMMENTARY_LOCAL')
        self.assertEqual(v['pada_sign'],0)
        self.assertNotEqual(v['pada_sign'],r(7)['pada_sign'])
    def test_venk_first_cited_vriddha_first(self):
        self.assertEqual(r(1,'VENKATESHA_COMMENTARY_LOCAL')['pada_sign'],0)
    def test_venk_tenth_abstains(self):
        v=r(10,'VENKATESHA_COMMENTARY_LOCAL')
        self.assertIsNone(v['pada_sign'])
        self.assertEqual(v['raw_pada_sign'],6)
    def test_venk_other_unmodified(self):
        self.assertEqual(r(3,'VENKATESHA_COMMENTARY_LOCAL')['pada_sign'],4)
    def test_both_modes_are_source_only(self):
        self.assertFalse(r(7)['score_allowed'])
        self.assertIsNone(r(7)['canonical_choice'])
        self.assertFalse(r(7,'VENKATESHA_COMMENTARY_LOCAL')['score_allowed'])
    def test_non_aries_translation(self):
        for mode in ('RATH_BPHS_CH29','VENKATESHA_COMMENTARY_LOCAL'):
            expected = (8 + (3 if mode == 'RATH_BPHS_CH29' else 6)) % 12
            self.assertEqual(r(4,mode,bhava=8)['pada_sign'],expected)
    def test_require_synthetic(self):
        with self.assertRaises(ValueError):
            bhava_arudha(bhava_sign=0,lord_sign=4,version='RATH_BPHS_CH29')
    def test_reject_bad_signs_and_types(self):
        for v in (-1,12,1.5,True):
            with self.assertRaises(ValueError):count_inclusive(v,3)
    def test_reject_unknown_mode(self):
        with self.assertRaises(ValueError):
            bhava_arudha(bhava_sign=0,lord_sign=3,version='SINGLE_TRUE_SCHOOL',synthetic=True)
    def test_two_lords_preserves_both(self):
        d=unresolved_two_lords(bhava_sign=7,lord_signs={'Mars':2,'Ketu':11},
                               version='RATH_BPHS_CH29',synthetic=True)
        self.assertEqual(len(d['variants']),2)
        self.assertIsNone(d['dominant_lord'])
        self.assertFalse(d['score_allowed'])
    def test_two_lords_can_yield_same_candidate_without_strength(self):
        d=unresolved_two_lords(bhava_sign=7,lord_signs={'Mars':9,'Ketu':3},
                               version='RATH_BPHS_CH29',synthetic=True)
        self.assertFalse(d['strengths_verified'])
    def test_two_lords_wrong_count_rejected(self):
        with self.assertRaises(ValueError):
            unresolved_two_lords(bhava_sign=7,lord_signs={'Mars':2},
                                 version='RATH_BPHS_CH29',synthetic=True)
    def test_graha_from_own_sign(self):
        g=graha_arudha(planet_sign=0,owned_sign=4,base='OWNED_SIGN',synthetic=True)
        self.assertEqual(g['count'],5)
        self.assertEqual(g['pada_sign'],8)
    def test_graha_planet_self_gloss_collapses_to_owned_sign(self):
        g=graha_arudha(planet_sign=0,owned_sign=4,base='PLANET_SELF_GLOSS',synthetic=True)
        self.assertEqual(g['pada_sign'],4)
        self.assertFalse(g['exception_rider_applied'])
    def test_graha_version_difference(self):
        a=graha_arudha(planet_sign=0,owned_sign=4,base='OWNED_SIGN',synthetic=True)
        b=graha_arudha(planet_sign=0,owned_sign=4,base='PLANET_SELF_GLOSS',synthetic=True)
        self.assertNotEqual(a['pada_sign'],b['pada_sign'])
        self.assertFalse(a['score_allowed'] or b['score_allowed'])
    def test_degree_examples(self):
        a=arudha_degree(natal_sign_degree=9+50/60,mode='RETAIN_SIGN_DEGREE',synthetic=True)
        b=arudha_degree(natal_sign_degree=9+50/60,mode='RATH_COMPLEMENT',synthetic=True)
        self.assertAlmostEqual(a['arudha_degree'],9+50/60)
        self.assertAlmostEqual(b['arudha_degree'],20+10/60)
    def test_sign_only_has_no_degree(self):
        d=arudha_degree(natal_sign_degree=9.5,mode='SIGN_ONLY',synthetic=True)
        self.assertIsNone(d['arudha_degree'])
    def test_zero_degree_boundary_abstains_rather_than_wraps(self):
        r=arudha_degree(natal_sign_degree=0,mode='RATH_COMPLEMENT',synthetic=True)
        self.assertIsNone(r['arudha_degree'])
        self.assertIn('UNRESOLVED',r['status'])
    def test_invalid_degree_rejected(self):
        for v in (-0.1,30,31,True):
            with self.assertRaises(ValueError):
                arudha_degree(natal_sign_degree=v,mode='RATH_COMPLEMENT',synthetic=True)
    def test_unknown_graha_base_rejected(self):
        with self.assertRaises(ValueError):
            graha_arudha(planet_sign=0,owned_sign=4,base='RECONSTRUCTED',synthetic=True)
    def test_matrix_is_documentary_and_unscored(self):
        doc=json.loads((Path(__file__).parent/'ARUDHA_SOURCE_VARIANT_MATRIX_B57.json').read_text())
        self.assertEqual(doc['record_count'],8)
        self.assertTrue(all(row['score_allowed'] is False for row in doc['records']))
        self.assertEqual(doc['independent_human_predictive_successes'],0)
        self.assertEqual(doc['production_rules_promoted'],0)
        self.assertEqual(doc['cumulative_documentary_annotations'],432)
        self.assertEqual(len(doc['records'][-1]['enumeration']),12)


if __name__ == '__main__':unittest.main()
