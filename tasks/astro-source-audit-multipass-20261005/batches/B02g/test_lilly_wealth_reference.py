"""Tests of explicit source contracts and input boundaries, not prediction."""

import unittest

import lilly_wealth_reference as reference


class QueryFrameTests(unittest.TestCase):
    def test_general_wealth_has_no_invented_counterparty(self):
        result = reference.query_frame("general_wealth")
        self.assertEqual((result["querent_house"], result["querent_money_house"]), (1, 2))
        self.assertIsNone(result["counterparty_house"])
        self.assertIsNone(result["counterparty_money_house"])
        self.assertEqual(result["pages"], [201])
        self.assertEqual(result["profile"], "general_wealth")
        self.assertIs(result["is_forecast"], False)

    def test_superior_and_ordinary_payment_are_distinct(self):
        ordinary = reference.query_frame("ordinary_specific_counterparty")
        superior = reference.query_frame("powerful_superior_payment")
        self.assertEqual((ordinary["counterparty_house"], ordinary["counterparty_money_house"]), (7, 8))
        self.assertEqual((superior["counterparty_house"], superior["counterparty_money_house"]), (10, 11))
        self.assertEqual(ordinary["pages"], [207, 208])
        self.assertEqual(superior["pages"], [208, 209])
        self.assertEqual(ordinary["precondition"], "comparable ordinary parties")
        self.assertEqual(superior["precondition"], "querent much inferior to payment source")
        for result in (ordinary, superior):
            self.assertEqual((result["querent_house"], result["querent_money_house"]), (1, 2))
            self.assertIs(result["is_forecast"], False)

    def test_no_automatic_or_unknown_frame(self):
        for name in ("auto", "seventh_house", "", "General_Wealth"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                reference.query_frame(name)
        with self.assertRaises(TypeError):
            reference.query_frame(None)

    def test_returned_data_cannot_change_later_reference(self):
        result = reference.query_frame("ordinary_specific_counterparty")
        result["counterparty_house"] = 10
        result["pages"].append(999)
        fresh = reference.query_frame("ordinary_specific_counterparty")
        self.assertEqual(fresh["counterparty_house"], 7)
        self.assertEqual(fresh["pages"], [207, 208])


class WealthIntervalTests(unittest.TestCase):
    def interval(self, distance, first, second):
        return reference.wealth_symbolic_interval(
            distance, first, second, profile=reference.WEALTH_TIMING_PROFILE
        )

    def test_all_source_pairs_and_their_reversed_order(self):
        cases = (
            ("cadent", "cadent", "days"),
            ("succedent", "succedent", "weeks"),
            ("angular", "angular", "months"),
            ("angular", "succedent", "months"),
            ("angular", "cadent", "months"),
            ("succedent", "cadent", "weeks"),
        )
        for first, second, unit in cases:
            with self.subTest(first=first, second=second):
                self.assertEqual(self.interval(90, first, second)["unit"], unit)
                self.assertEqual(self.interval(90, second, first)["unit"], unit)

    def test_exact_fraction_and_zero(self):
        self.assertEqual(self.interval(1, "cadent", "cadent")["interval"], "1/60")
        self.assertEqual(self.interval(90, "angular", "cadent")["interval"], "3/2")
        self.assertEqual(self.interval(0, "succedent", "cadent")["interval"], "0")

    def test_profile_is_required_and_not_inferred(self):
        with self.assertRaises(TypeError):
            reference.wealth_symbolic_interval(60, "angular", "cadent")
        for profile in (None, "auto", "LILLY_II_XXIII", ""):
            with self.subTest(profile=profile), self.assertRaises(ValueError):
                reference.wealth_symbolic_interval(60, "angular", "cadent", profile=profile)

    def test_long_interval_stays_months_without_undefined_override(self):
        result = self.interval(21600, "angular", "cadent")
        self.assertEqual((result["interval"], result["unit"]), ("360", "months"))
        self.assertEqual(result["source_note"], "long business may warrant years, threshold undefined, not chosen here")
        self.assertEqual(result["pages"], [209, 210])
        self.assertIs(result["civil_dates_computed"], False)
        self.assertIs(result["is_forecast"], False)
        with self.assertRaises(TypeError):
            reference.wealth_symbolic_interval(60, "angular", "cadent", profile=reference.WEALTH_TIMING_PROFILE, long_business=True)

    def test_invalid_distance_and_house_categories(self):
        for value in (True, False, 1.5, "60", None):
            with self.subTest(value=value), self.assertRaises(TypeError):
                self.interval(value, "angular", "cadent")
        with self.assertRaises(ValueError):
            self.interval(-1, "angular", "cadent")
        for first, second in (("fixed", "angular"), ("angular", "movable")):
            with self.subTest(first=first, second=second), self.assertRaises(ValueError):
                self.interval(60, first, second)
        for first, second in ((True, "angular"), ("angular", None)):
            with self.subTest(first=first, second=second), self.assertRaises(TypeError):
                self.interval(60, first, second)


class DegreeTests(unittest.TestCase):
    def test_zodiac_order_and_exact_sign_boundaries(self):
        self.assertIsInstance(reference.ZODIAC, tuple)
        self.assertEqual(reference.degree("Aries", 0, 0), 0)
        self.assertEqual(reference.degree("Gemini", 19, 26), 4766)
        self.assertEqual(reference.degree("Cancer", 0, 0), 5400)
        self.assertEqual(reference.degree("Pisces", 29, 59), 21599)

    def test_no_silent_sign_or_coordinate_normalization(self):
        for sign in ("aries", "Aries ", "Ophiuchus"):
            with self.subTest(sign=sign), self.assertRaises(ValueError):
                reference.degree(sign, 0, 0)
        for degrees, minutes in ((-1, 0), (30, 0), (0, -1), (0, 60)):
            with self.subTest(degrees=degrees, minutes=minutes), self.assertRaises(ValueError):
                reference.degree("Aries", degrees, minutes)

    def test_boolean_float_and_missing_minute_are_rejected(self):
        for degrees, minutes in ((True, 0), (0, False), (1.0, 0), (0, 1.0), (1, None)):
            with self.subTest(degrees=degrees, minutes=minutes), self.assertRaises(TypeError):
                reference.degree("Aries", degrees, minutes)
        with self.assertRaises(TypeError):
            reference.degree(None, 0, 0)


if __name__ == "__main__":
    unittest.main()
