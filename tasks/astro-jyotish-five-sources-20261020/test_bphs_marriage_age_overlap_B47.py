"""Isolated nonproduction arithmetic checks of BPHS 18.22/23 coactivation."""
import unittest
from dataclasses import replace
from bphs_marriage_age_overlap_B47 import (
    original_moshier_witness, zodiac_sign, distance, source_age_sets,
)


class TestB47(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.w = original_moshier_witness()

    def test_expected_signs(self):
        self.assertEqual(tuple(zodiac_sign(x) for x in (
            self.w.ascendant, self.w.sun, self.w.venus, self.w.saturn)),
            (3, 9, 11, 11))

    def test_ephemeris_returned_moshier_sidereal(self):
        self.assertTrue(all((flag & 7) == 4 and flag & 65536
                            for flag in (self.w.sun_flags, self.w.venus_flags,
                                         self.w.saturn_flags)))

    def test_independently_calculated_longitudes(self):
        for actual, expected in zip((self.w.ascendant, self.w.sun,
                                     self.w.venus, self.w.saturn),
                                    (106.8900453, 298.031932, 333.321638,
                                     332.912978)):
            self.assertAlmostEqual(actual, expected, delta=0.005)

    def test_seventh_lord_and_venus_conjunct(self):
        self.assertLess(distance(self.w.saturn, self.w.venus), 1.0)

    def test_disjoint_coactivation(self):
        a, b = source_age_sets(self.w)
        self.assertEqual(a, frozenset((5, 9)))
        self.assertEqual(b, frozenset((7, 11)))
        self.assertFalse(a & b)

    def test_mutate_venus_division(self):
        a, b = source_age_sets(replace(self.w, venus=310.0))
        self.assertFalse(a)
        self.assertFalse(b)

    def test_mutate_sun_seventh(self):
        a, b = source_age_sets(replace(self.w, sun=275.0))
        self.assertEqual(a, frozenset((5, 9)))
        # Capricorn is still 7th, so use Aries to actually change the sign.
        a, b = source_age_sets(replace(self.w, sun=10.0))
        self.assertEqual(a, frozenset((5, 9)))
        self.assertFalse(b)

    def test_other_ascendant_fails_closed(self):
        with self.assertRaises(ValueError):
            source_age_sets(replace(self.w, ascendant=145.0))


if __name__ == "__main__":
    unittest.main()
