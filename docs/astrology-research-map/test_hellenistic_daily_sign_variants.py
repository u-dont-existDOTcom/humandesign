"""Regression tests for *source-rate* arithmetic, not astrology validation."""
import unittest

from hellenistic_daily_sign_variants import (
    RATES,
    discrepancy_counts,
    relative_sign,
)


class TestDailySignVariants(unittest.TestCase):
    def test_four_distinct_source_modes_preserved(self):
        self.assertEqual(len(RATES), 4)
        self.assertEqual(RATES["PAULUS_1D"].days_per_sign.numerator, 1)
        self.assertEqual(RATES["HEPH_5_OVER_2"].days_per_sign.denominator, 2)
        self.assertEqual(RATES["PTOLEMY_ROBBINS_7_OVER_3"].days_per_sign.denominator, 3)
        self.assertEqual(
            RATES["HEPH_5_OVER_2"].days_per_sign,
            RATES["PTOLEMY_MSS_5_OVER_2"].days_per_sign,
        )
        self.assertNotEqual(
            RATES["HEPH_5_OVER_2"].locator,
            RATES["PTOLEMY_MSS_5_OVER_2"].locator,
        )

    def test_days_cross_mathematically_distinct_boundaries(self):
        self.assertEqual(relative_sign(0, "PAULUS_1D"), 0)
        self.assertEqual(relative_sign(7, "PAULUS_1D"), 7)
        self.assertEqual(relative_sign(7, "HEPH_5_OVER_2"), 2)
        self.assertEqual(relative_sign(7, "PTOLEMY_ROBBINS_7_OVER_3"), 3)
        self.assertEqual(relative_sign(12, "PAULUS_1D"), 0)
        self.assertEqual(relative_sign(12, "HEPH_5_OVER_2"), 4)
        self.assertEqual(relative_sign(12, "PTOLEMY_ROBBINS_7_OVER_3"), 5)

    def test_28_day_synthetic_contrast(self):
        self.assertEqual(discrepancy_counts(28), {
            "toy_days": 28,
            "paulus_vs_hephaistio_different": 25,
            "paulus_vs_ptolemy_different": 25,
            "hephaistio_vs_ptolemy_different": 10,
            "all_three_identical": 2,
        })

    def test_rotating_origin_does_not_change_pairwise_differences(self):
        for k in range(28):
            a = relative_sign(k, "HEPH_5_OVER_2")
            b = relative_sign(k, "PTOLEMY_ROBBINS_7_OVER_3")
            self.assertEqual(a == b,
                relative_sign(k, "HEPH_5_OVER_2", 7) ==
                relative_sign(k, "PTOLEMY_ROBBINS_7_OVER_3", 7))

    def test_no_implicit_calendar_or_unknown_variant(self):
        for val in (-1, 0.5, "7"):
            with self.assertRaises(ValueError):
                relative_sign(val, "PAULUS_1D")
        for val in (-1, 12, "0"):
            with self.assertRaises(ValueError):
                relative_sign(0, "PAULUS_1D", val)
        with self.assertRaises(ValueError):
            relative_sign(0, "MIXED_UNSOURCED_RULE")
        with self.assertRaises(ValueError):
            discrepancy_counts(0)


if __name__ == "__main__":
    unittest.main()
