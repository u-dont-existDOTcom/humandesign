import unittest
from fractions import Fraction
from solar_graha_aspect_B36 import ASPECTS_BY_VERSION,aspect_fraction,whole_sign_minimum_gap,solar_aspect_possible
class SaravaliSourceOnlyAspects(unittest.TestCase):
 def test_solar_mercury_empty_both(self):
  for version in ASPECTS_BY_VERSION:self.assertEqual(solar_aspect_possible('Mercury',version=version),[])
 def test_venus_control_both(self):
  for version in ASPECTS_BY_VERSION:self.assertEqual(len(solar_aspect_possible('Venus',version=version)),12)
 def test_sanskrit_quarter_sequence(self):
  v='sanskrit_restored'
  for house,weight in [(3,Fraction(1,4)),(5,Fraction(1,2)),(4,Fraction(3,4)),(7,Fraction(1))]:
   self.assertEqual(aspect_fraction(0,house-1,version=v),weight)
 def test_translation_fraction_inversion(self):
  self.assertEqual(aspect_fraction(0,3,version='english_uploaded'),Fraction(1,2))
  self.assertEqual(aspect_fraction(0,3,version='sanskrit_restored'),Fraction(3,4))
  self.assertEqual(aspect_fraction(0,4,version='english_uploaded'),Fraction(3,4))
  self.assertEqual(aspect_fraction(0,4,version='sanskrit_restored'),Fraction(1,2))
 def test_gap_ch35_169(self):
  self.assertEqual(whole_sign_minimum_gap(0,2),30)
 def test_failclosed_version_and_bad_sign(self):
  with self.assertRaises(TypeError):aspect_fraction(0,2)
  with self.assertRaises(ValueError):aspect_fraction(0,2,version='unverified')
  with self.assertRaises(ValueError):aspect_fraction(12,2,version='sanskrit_restored')
if __name__=='__main__':unittest.main()
