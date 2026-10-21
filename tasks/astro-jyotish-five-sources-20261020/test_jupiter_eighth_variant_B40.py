import unittest
from jupiter_eighth_variant_B40 import jupiter_aspect_virupas as aspect
from bphs_special_aspect_B39 import bphs_sphuta_special as original

class JupiterCommentarialVariants(unittest.TestCase):
    def test_historical_literal_preserved(self):
        for d in (0, 90, 105, 120, 135, 180, 225, 240, 245, 255, 269.999, 270, 359):
            self.assertEqual(aspect(d, version='sanskrit_literal'), original(d, planet='Jupiter'))
    def test_ernst_example_and_difference(self):
        self.assertEqual(aspect(245, version='wilhelm_editorial_repair'), 52.5)
        self.assertEqual(aspect(245, version='sanskrit_literal'), 50)
        self.assertEqual(aspect(255, version='wilhelm_editorial_repair'), 37.5)
        self.assertEqual(aspect(255, version='sanskrit_literal'), 30)
    def test_junction_at_270(self):
        self.assertAlmostEqual(aspect(269.999999, version='sanskrit_literal'), 0, places=4)
        self.assertEqual(aspect(270, version='sanskrit_literal'), 15)
        self.assertAlmostEqual(aspect(269.999999, version='wilhelm_editorial_repair'), 15, places=4)
        self.assertEqual(aspect(270, version='wilhelm_editorial_repair'), 15)
    def test_outside_changed_sector_remains_same(self):
        for i in range(0, 3600):
            d = i / 10
            mod = aspect(d, version='wilhelm_editorial_repair')
            assert 0 <= mod <= 60
            if not 240 <= d < 270:
                self.assertEqual(mod, original(d, planet='Jupiter'))
    def test_requires_version_and_valid_angle(self):
        with self.assertRaises(TypeError):aspect(245)
        with self.assertRaises(ValueError):aspect(245, version='auto')
        with self.assertRaises(ValueError):aspect(-1, version='sanskrit_literal')
        with self.assertRaises(ValueError):aspect(360, version='wilhelm_editorial_repair')

if __name__ == '__main__':
    unittest.main(verbosity=2)
