import unittest
from whole_sign_geometry_B35 import minimum_whole_sign_gap_deg as gap, sun_pair_empty, six_exaltation_exclusions

class WholeSignTests(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(gap(1, 6), 120)  # Mercury in second, Sun seventh
        self.assertEqual(gap(0, 3), 60)   # Venus rising, Sun fourth
        self.assertEqual(gap(1, 3), 30)   # Mercury second, Sun fourth
    def test_source_empty(self):
        self.assertTrue(sun_pair_empty('Mercury', 1, 6))
        self.assertTrue(sun_pair_empty('Venus', 0, 3))
        self.assertTrue(sun_pair_empty('Mercury', 1, 3))
    def test_ordinary_near_sun_not_falsely_excluded(self):
        self.assertFalse(sun_pair_empty('Venus', 11, 0))
        self.assertFalse(sun_pair_empty('Mercury', 0, 0))
    def test_six_exaltation_only_unexcluded_case(self):
        out = six_exaltation_exclusions()
        self.assertEqual([missing for missing, why in out.items() if not why], ['Mercury'])
        self.assertIn('Mercury/Venus', out['Sun'])
        self.assertIn('Sun/Mercury', out['Venus'])
    def test_symmetry_and_bounds(self):
        for a in range(12):
            for b in range(12):
                self.assertEqual(gap(a, b), gap(b, a))
                self.assertGreaterEqual(gap(a, b), 0)
                self.assertLessEqual(gap(a, b), 150)
    def test_fail_closed(self):
        for a, b in [(-1,2), (12,3), (4,False), (3,2.1)]:
            with self.assertRaises(ValueError):gap(a,b)
        with self.assertRaises(ValueError):sun_pair_empty('Jupiter',1,2)

if __name__ == '__main__':
    unittest.main()
