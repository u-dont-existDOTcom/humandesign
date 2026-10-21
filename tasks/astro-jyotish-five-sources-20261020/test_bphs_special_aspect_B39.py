import unittest
from bphs_special_aspect_B39 import bphs_sphuta_special as aspect
from comparative_aspect_methods_B38 import bphs_general_exact_virupas as general

class SpecialAspectTests(unittest.TestCase):
 def test_saturn_special_peaks(self):
  for d,value in ((30,0),(45,30),(60,60),(75,52.5),(90,45),
                  (240,30),(255,45),(270,60),(285,30),(300,0)):
   with self.subTest(d=d):self.assertEqual(aspect(d,planet='Saturn'),value)
 def test_mars_special_peaks(self):
  for d,value in ((60,15),(75,37.5),(90,60),(105,45),(120,30),
                  (180,60),(195,60),(210,60),(225,45),(240,30)):
   with self.subTest(d=d):self.assertEqual(aspect(d,planet='Mars'),value)
 def test_jupiter_special_peaks(self):
  for d,value in ((90,45),(105,52.5),(120,60),(135,30),(150,0),
                  (210,45),(225,52.5),(240,60),(255,30),(270,15)):
   with self.subTest(d=d):self.assertEqual(aspect(d,planet='Jupiter'),value)
 def test_outside_override_ordinary(self):
  for name in ('Saturn','Mars','Jupiter'):
   for d in (0,20,29,30,150,165,330):
    # Not all 150 are outside Jupiter's 120-150 interval: at 150 both zero.
    self.assertEqual(aspect(d,planet=name),general(d))
 def test_nonnegative_bounded_dense_grid(self):
  for planet in ('Mars','Jupiter','Saturn'):
   for i in range(3600):
    value=aspect(i/10,planet=planet)
    self.assertTrue(0<=value<=60,(planet,i/10,value))
 def test_continuity_and_explicit_version(self):
  for planet in ('Mars','Jupiter','Saturn'):
   for d in range(30,301,30):
    if planet=='Jupiter' and d==270:continue # source piecewise gap, not smoothed
    self.assertLess(abs(aspect(d+1e-5,planet=planet)-aspect(d-1e-5,planet=planet)),0.01,(planet,d))
  self.assertAlmostEqual(aspect(270-1e-5,planet='Jupiter'),0,places=3)
  self.assertAlmostEqual(aspect(270+1e-5,planet='Jupiter'),15,places=3)
  self.assertEqual(aspect(270,planet='Jupiter'),15)
  with self.assertRaises(TypeError):aspect(60)
  with self.assertRaises(ValueError):aspect(60,planet='Sun')
  with self.assertRaises(ValueError):aspect(360,planet='Saturn')
 def test_modern_derivative_not_reliable(self):
  # A 2017 software reference table, not Sanskrit, misprints Mars 90-120,
  # Jupiter 240-270 and Saturn above 300. Source-based values are >=0.
  self.assertEqual(aspect(105,planet='Mars'),45)
  self.assertEqual(aspect(255,planet='Jupiter'),30)
  self.assertEqual(aspect(315,planet='Saturn'),0)

if __name__=='__main__':unittest.main(verbosity=2)
