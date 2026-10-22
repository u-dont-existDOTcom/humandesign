import unittest
from marriage_witness_variants_B49 import (house, sign_of_house, bphs_18_33_candidate_antecedents,
                                            Witness, witness_disagreement, event_age_vs_duration)


class VariantsB49(unittest.TestCase):
    def _check(self, positions):
        return bphs_18_33_candidate_antecedents(lagna_sign=0, positions=positions, synthetic=True)

    def test_house_arithmetic(self):
        self.assertEqual(house(sign_of_house(0, 9), 0), 9)
        self.assertEqual(house(sign_of_house(8, 5), 8), 5)
        self.assertEqual(house(2, 0), 3)  # seventh from ninth, Aries ascendant

    def test_printed_house_option_only(self):
        r = self._check({"Venus": 4, "Rahu": 8, "Sun": 0, "Jupiter": 2})
        self.assertTrue(r["Rahu_in_one_of_houses"])
        self.assertFalse(r["Rahu_conjunct_both_house_lords"])

    def test_editorial_lord_conjunction_only(self):
        r = self._check({"Venus": 4, "Rahu": 9, "Sun": 9, "Jupiter": 9})
        self.assertFalse(r["Rahu_in_one_of_houses"])
        self.assertTrue(r["Rahu_conjunct_both_house_lords"])

    def test_both_possible(self):
        r = self._check({"Venus": 4, "Rahu": 8, "Sun": 8, "Jupiter": 8})
        self.assertTrue(r["Rahu_in_one_of_houses"])
        self.assertTrue(r["Rahu_conjunct_both_house_lords"])

    def test_neither_possible(self):
        r = self._check({"Venus": 0, "Rahu": 9, "Sun": 8, "Jupiter": 8})
        self.assertFalse(r["Rahu_in_one_of_houses"])
        self.assertFalse(r["Rahu_conjunct_both_house_lords"])

    def test_no_canonical_selection(self):
        r = self._check({"Venus": 4, "Rahu": 8, "Sun": 8, "Jupiter": 8})
        self.assertFalse(r["score_allowed"])
        self.assertIsNone(r["source_interpretation_canonical"])

    def test_synthetic_gate_and_missing_lord(self):
        with self.assertRaises(ValueError):
            bphs_18_33_candidate_antecedents(lagna_sign=0, positions={"Venus": 4, "Rahu": 8, "Sun": 8, "Jupiter": 8})
        with self.assertRaises(ValueError):
            self._check({"Venus": 4, "Rahu": 8, "Sun": 8})
        with self.assertRaises(ValueError):
            house(True, 0)

    def test_same_verse_only_and_duplicate_witness(self):
        a = Witness("18.34", "dyune", "house7", "a", "sanskritdocuments")
        b = Witness("18.34", "dvune", "unresolved", "b", "web-transcriptions")
        r = witness_disagreement((a, b))
        self.assertEqual(r["distinct_literal_readings"], 2)
        self.assertEqual(r["independent_manuscripts_verified"], 0)
        with self.assertRaises(ValueError):
            witness_disagreement((a, a))
        with self.assertRaises(ValueError):
            witness_disagreement((a, Witness("18.33", "x", "y", "c", "web")))

    def test_same_web_family_not_independent_manuscripts(self):
        a = Witness("18.38", "19", "19", "a", "shared-web")
        b = Witness("18.38", "19", "19", "b", "shared-web")
        self.assertEqual(witness_disagreement((a, b))["distinct_declared_transmission_families"], 1)

    def test_duration_and_age_remain_distinct(self):
        self.assertNotEqual(event_age_vs_duration(10, "EVENT_AGE"), event_age_vs_duration(10, "DURATION_YEARS"))
        self.assertFalse(event_age_vs_duration(10, "EVENT_AGE")["score_allowed"])


if __name__ == "__main__":
    unittest.main()
