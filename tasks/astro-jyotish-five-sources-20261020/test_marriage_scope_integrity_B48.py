"""Nonproduction source-integrity unit tests with no human or chart outcome inputs."""
import unittest
from marriage_scope_integrity_B48 import (
    AgeClaim, B47_22, B47_23, EXPLICIT_40, EXPLICIT_41_SECOND, EXPLICIT_41_THIRD,
    age_claim_collision, age_interpretation_difference, inclusive_relative_house,
    verse_21_partial,
)


class SourceIntegrityTests(unittest.TestCase):
    def test_ninth_from_ninth_is_fifth(self):
        self.assertEqual(inclusive_relative_house(9, 9), 5)

    def test_seventh_from_ninth_is_third(self):
        self.assertEqual(inclusive_relative_house(9, 7), 3)

    def test_seventh_from_eighth_is_second(self):
        self.assertEqual(inclusive_relative_house(8, 7), 2)

    def test_house_identity_and_validation(self):
        for n in range(1, 13):
            self.assertEqual(inclusive_relative_house(n, 1), n)
        with self.assertRaises(ValueError):
            inclusive_relative_house(0, 9)

    def test_disjunction_is_not_broad_interval(self):
        result = age_interpretation_difference(frozenset({22, 27}))
        self.assertEqual(result["new_age_values_mistakenly_admitted"], [23, 24, 25, 26])

    def test_childhood_alternatives_are_not_broad_interval(self):
        self.assertEqual(age_interpretation_difference(frozenset({5, 9}))["new_age_values_mistakenly_admitted"], [6, 7, 8])

    def test_b47_collision_but_no_implicit_first_marriage(self):
        result = age_claim_collision((B47_22, B47_23))
        self.assertEqual(result["status"], "UNRESOLVED_EVENT_INDEX_AND_DISJOINT_AGES")
        self.assertEqual(result["single_event_age_intersection_if_assumed"], [])
        self.assertFalse(result["score_allowed"])
        self.assertIsNone(result["canonical_selection"])

    def test_explicit_ordinals_distinct(self):
        result = age_claim_collision((EXPLICIT_40, EXPLICIT_41_SECOND, EXPLICIT_41_THIRD))
        self.assertEqual(len(result["explicitly_indexed_claims"]), 3)
        self.assertEqual(result["status"], "ORDINAL_EXPLICIT_REQUIRES_SOURCE_CONDITION_AND_EMPIRICAL_FREEZE")

    def test_no_rule_cannot_be_rescued(self):
        self.assertEqual(age_claim_collision(())['status'], "NO_SOURCE_CONDITION")

    def test_duplicate_source_rejected(self):
        with self.assertRaises(ValueError):
            age_claim_collision((B47_22, B47_22))

    def test_non_numeric_probability_qualifier(self):
        self.assertFalse(age_claim_collision((B47_22, B47_23))["probabilities_calibrated"])

    def test_multispouse_partial_unknown_strength(self):
        self.assertEqual(verse_21_partial(11, 3, None), "UNRESOLVED_SEVENTH_LORD_STRENGTH")
        self.assertEqual(verse_21_partial(11, 3, False), "SEVENTH_LORD_STRENGTH_CONDITION_FAILS")

    def test_multispouse_requires_full_conditions(self):
        self.assertEqual(verse_21_partial(11, 3, True), "FULL_CONDITION_SATISFIED")
        self.assertNotEqual(verse_21_partial(11, 2, True), "FULL_CONDITION_SATISFIED")

    def test_rule_age_guards(self):
        with self.assertRaises(ValueError):
            AgeClaim("X", frozenset(), "UNSPECIFIED_MARRIAGE")
        with self.assertRaises(ValueError):
            AgeClaim("X", frozenset({0}), "UNSPECIFIED_MARRIAGE")


if __name__ == "__main__":
    unittest.main()
