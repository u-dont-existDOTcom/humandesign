import math
import unittest
from fractions import Fraction
from comparative_aspect_methods_B38 import (
    bphs_general_exact_virupas as virupa, jaimini_rasi_aspect as rasi,
    saravali_discrete_fraction as saravali, bound_all_sun_mercury_aspects,
    minimum_sign_longitude_gap_deg as gap)

class SourceAspectArithmeticTests(unittest.TestCase):
    def test_bphs_exact_edges(self):
        known={0:0,29:0,30:0,45:7.5,60:15,75:30,90:45,105:37.5,
               120:30,135:15,150:0,165:30,180:60,210:45,240:30,
               270:15,300:0,330:0,359:0}
        for delta,value in known.items():
            with self.subTest(angle=delta):self.assertEqual(virupa(delta),value)
    def test_continuous_bounded(self):
        for step in range(0,36000):
            v=virupa(step/100)
            self.assertGreaterEqual(v,0)
            self.assertLessEqual(v,60)
        for border in (30,60,90,120,150,180,300):
            self.assertAlmostEqual(virupa(border-0.0001),virupa(border+0.0001),places=3)
    def test_rasi_sign_aspect_not_same_or_adjacent(self):
        for a in range(12):
            for offset in (0,1,11):self.assertFalse(rasi(a,(a+offset)%12))
        self.assertTrue(rasi(0,7)) # Aries -> Scorpio
        self.assertTrue(rasi(2,5)) # Gemini -> Virgo
        self.assertFalse(rasi(0,1)) # Aries -> Taurus adjacent excluded
    def test_saravali_fraction_support(self):
        self.assertEqual(saravali(0,2),Fraction(1,4))
        self.assertEqual(saravali(0,3),Fraction(3,4))
        self.assertEqual(saravali(0,4),Fraction(1,2))
        self.assertEqual(saravali(0,6),Fraction(1))
        self.assertEqual(saravali(0,1),Fraction(0))
    def test_mercury_conservative_cap_29(self):
        self.assertEqual(bound_all_sun_mercury_aspects()['jaimini_rasi_sun_mercury_possibilities'],[])
        self.assertEqual(bound_all_sun_mercury_aspects()['saravali_graha_sun_mercury_possibilities'],[])
        self.assertEqual(bound_all_sun_mercury_aspects()['bphs_exact_positive_boundary_counterexamples'],[])
    def test_different_aspect_concepts_can_disagree_other_bodies(self):
        self.assertTrue(rasi(0,7))
        self.assertEqual(saravali(0,7),Fraction(3,4)) # 8th from Aries
        self.assertTrue(rasi(2,5))
        self.assertEqual(saravali(2,5),Fraction(3,4))
        # A 20-degree ordinary exact aspect is absent while same-sign always has no Rasi Drsti.
        self.assertEqual(virupa(20),0)
    def test_fail_closed_inputs(self):
        for x in (float('nan'),float('inf'),-1,360,True):
            with self.assertRaises(ValueError):virupa(x)
        with self.assertRaises(ValueError):gap(0,12)
        with self.assertRaises(ValueError):rasi(1,1.0)
        with self.assertRaises(ValueError):bound_all_sun_mercury_aspects(30)

if __name__=='__main__':unittest.main(verbosity=2)
