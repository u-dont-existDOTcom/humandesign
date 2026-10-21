import unittest
from fractions import Fraction
from solar_graha_aspect_B36 import aspect_fraction,whole_sign_minimum_gap,solar_aspect_possible
class SaravaliSourceOnlyAspects(unittest.TestCase):
    def test_verse35_80_mercury_solar_aspect_empty(self):
        self.assertEqual(solar_aspect_possible('Mercury'), [])
    def test_venus_control(self):
        self.assertEqual(len(solar_aspect_possible('Venus')),12)
        self.assertEqual(aspect_fraction(0,2),Fraction(1,4))
    def test_source_aspect_strengths(self):
        self.assertEqual(aspect_fraction(0,6),Fraction(1))
        self.assertEqual(aspect_fraction(0,3),Fraction(1,2))
        self.assertEqual(aspect_fraction(0,1),Fraction(0))
    def test_verse35_169_mercury_sun_third(self):
        self.assertEqual(whole_sign_minimum_gap(0,2),30)
        self.assertGreater(whole_sign_minimum_gap(0,2),28)
    def test_failclosed(self):
        with self.assertRaises(ValueError):aspect_fraction(12,2)
        with self.assertRaises(ValueError):whole_sign_minimum_gap(0,2.0)
if __name__=='__main__':unittest.main()
