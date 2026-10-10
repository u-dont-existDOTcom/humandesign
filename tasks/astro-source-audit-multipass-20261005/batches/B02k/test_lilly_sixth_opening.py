"""Focused source/data and bounded-logic tests; no predictive-accuracy claim."""

from fractions import Fraction
import json
from pathlib import Path
import unittest

import lilly_sixth_opening_reference as ref

ROOT = Path(__file__).parent


def all_unavailable():
    return {key: ref.TimeEvidence(False) for key in ref.TIME_KEYS}


class TimeSelection(unittest.TestCase):
    def test_enforced_rest_precedes_other_available_times(self):
        evidence = {key: ref.TimeEvidence(True, key) for key in ref.TIME_KEYS}
        self.assertEqual(ref.select_source_time(evidence)["candidates"],
                         [{"event": "enforced_bed_or_rest", "token": "enforced_bed_or_rest"}])

    def test_first_urine_inquiry_can_be_to_a_nonphysician(self):
        evidence = all_unavailable()
        evidence["first_urine_inquiry"] = ref.TimeEvidence(True, "nonphysician-enquiry")
        self.assertEqual(ref.select_source_time(evidence)["stage"], 2)

    def test_unknown_onset_availability_does_not_mean_unavailable(self):
        evidence = all_unavailable()
        evidence["enforced_bed_or_rest"] = ref.TimeEvidence(None)
        evidence["first_urine_inquiry"] = ref.TimeEvidence(True, "later-enquiry")
        self.assertEqual(ref.select_source_time(evidence)["status"], ref.UNKNOWN)

    def test_stage_three_distinct_times_remain_alternatives(self):
        evidence = all_unavailable()
        evidence["physician_first_speaking"] = ref.TimeEvidence(True, "contact-a")
        evidence["physician_first_urine_receipt"] = ref.TimeEvidence(True, "contact-b")
        self.assertEqual(ref.select_source_time(evidence)["status"], "CHOICE_UNRESOLVED")

    def test_stage_three_identical_times_can_share_selection(self):
        evidence = all_unavailable()
        for key in ref.TIME_KEYS[2:]:
            evidence[key] = ref.TimeEvidence(True, "same-observed-time")
        result = ref.select_source_time(evidence)
        self.assertEqual((result["status"], len(result["candidates"])), ("SELECTED", 3))

    def test_unknown_stage_three_alternative_is_retained(self):
        evidence = all_unavailable()
        evidence["physician_first_access"] = ref.TimeEvidence(None)
        evidence["physician_first_speaking"] = ref.TimeEvidence(True, "known-time")
        result = ref.select_source_time(evidence)
        self.assertEqual(result["status"], ref.UNKNOWN)
        self.assertEqual(len(result["candidates"]), 1)

    def test_first_slight_symptom_is_not_a_source_time_key(self):
        with self.assertRaises(ValueError):
            ref.select_source_time({"first_slight_symptom": ref.TimeEvidence(True, "early")})

    def test_missing_or_invalid_time_evidence_never_fabricates_time(self):
        self.assertEqual(ref.select_source_time({})["status"], ref.UNKNOWN)
        self.assertEqual(ref.select_source_time(all_unavailable())["status"], "UNAVAILABLE")
        with self.assertRaises(ValueError):
            ref.TimeEvidence(True)


class LunarMotion(unittest.TestCase):
    def test_below_both_thresholds(self):
        self.assertEqual(ref.moon_speed_comparisons(47399),
                         {"below_stated_mean": True, "under_retrograde_analogy_threshold": True})

    def test_exact_analogy_boundary_is_not_below_analogy_threshold(self):
        self.assertEqual(ref.moon_speed_comparisons(47400),
                         {"below_stated_mean": True, "under_retrograde_analogy_threshold": False})

    def test_thirty_six_second_interval_keeps_distinct_source_tests(self):
        self.assertEqual(ref.moon_speed_comparisons(47418),
                         {"below_stated_mean": True, "under_retrograde_analogy_threshold": False})

    def test_exact_mean_is_not_below_mean(self):
        self.assertEqual(ref.moon_speed_comparisons(47436),
                         {"below_stated_mean": False, "under_retrograde_analogy_threshold": False})

    def test_unknown_motion_and_invalid_units(self):
        self.assertEqual(ref.moon_speed_comparisons(None)["below_stated_mean"], None)
        for value in [True, 13.17, "47400"]:
            with self.assertRaises(TypeError):
                ref.moon_speed_comparisons(value)
        with self.assertRaises(ValueError):
            ref.moon_speed_comparisons(-1)


class SourcePredicateQualifications(unittest.TestCase):
    def test_benefic_must_not_be_author_of_disease(self):
        inputs = dict(benevolent=True, well_fortified=True, in_sixth=True)
        self.assertEqual(ref.benevolent_sixth_predicate(**inputs, author_of_disease=False), ref.SATISFIED)
        self.assertEqual(ref.benevolent_sixth_predicate(**inputs, author_of_disease=True), ref.CONTRADICTED)

    def test_unknown_authorship_does_not_satisfy_exclusion(self):
        self.assertEqual(ref.benevolent_sixth_predicate(benevolent=True, well_fortified=True,
                                                      in_sixth=True, author_of_disease=None), ref.UNKNOWN)

    def test_already_declining_exception_blocks_adverse_moon_clause(self):
        inputs = dict(light_decreasing=True, motion_decreasing=True,
                      moon_applying_conjunction_square_or_opposition_to_saturn=True)
        self.assertEqual(ref.declining_moon_saturn_predicate(**inputs, disease_decreasing_and_leaving=False), ref.SATISFIED)
        self.assertEqual(ref.declining_moon_saturn_predicate(**inputs, disease_decreasing_and_leaving=True), ref.CONTRADICTED)
        self.assertEqual(ref.declining_moon_saturn_predicate(**inputs, disease_decreasing_and_leaving=None), ref.UNKNOWN)

    def test_three_valued_predicates_preserve_unknown_and_negative(self):
        self.assertEqual(ref.all_facts(True, None), ref.UNKNOWN)
        self.assertEqual(ref.all_facts(False, None), ref.CONTRADICTED)
        with self.assertRaises(TypeError):
            ref.all_facts("unknown")


class RemainingArc(unittest.TestCase):
    def test_half_degree_remaining_does_not_select_a_time_unit(self):
        self.assertEqual(ref.remaining_degrees_in_sign(29, 30, 0),
                         {"remaining_degrees": Fraction(1, 2), "time_unit": None})

    def test_known_zero_start_has_thirty_degrees_remaining(self):
        self.assertEqual(ref.remaining_degrees_in_sign(0, 0, 0)["remaining_degrees"], 30)

    def test_omitted_minutes_or_seconds_stay_unknown(self):
        self.assertIsNone(ref.remaining_degrees_in_sign(29)["remaining_degrees"])
        self.assertIsNone(ref.remaining_degrees_in_sign(29, 0)["remaining_degrees"])

    def test_invalid_within_sign_coordinate_is_rejected(self):
        for coordinates in [(30, 0, 0), (29, 60, 0), (29, 0, 60), (-1, 0, 0)]:
            with self.assertRaises(ValueError):
                ref.remaining_degrees_in_sign(*coordinates)

    def test_individually_valid_fractional_components_must_not_reach_next_sign(self):
        for coordinates in [(Fraction(59, 2), 59, 0), (Fraction(59, 2), 30, 0)]:
            with self.assertRaises(ValueError):
                ref.remaining_degrees_in_sign(*coordinates)


class SourceLookups(unittest.TestCase):
    def test_three_catalogues_have_separate_complete_key_sets(self):
        tables = json.loads((ROOT / "REFERENCE_TABLES.json").read_text())["namespaces"]
        self.assertEqual(set(tables["house"]), {str(i) for i in range(1, 13)})
        self.assertEqual(len(tables["sign"]), 12)
        self.assertEqual(set(tables["planet"]), {"Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"})

    def test_saturn_in_cancer_callback_is_not_generic_cancer_catalogue(self):
        callback = ref.source_lookup("retained_planet_sign", "Saturn|Cancer")
        self.assertEqual(callback["source_items"], ["Reins", "Belly", "Secrets"])
        self.assertNotEqual(callback["source_items"], ref.source_lookup("sign", "Cancer")["source_items"])

    def test_historical_star_labels_have_no_invented_minutes(self):
        star = ref.source_lookup("historical_fixed_star", "Pleiades")
        self.assertEqual((star["sign"], star["source_degree_number"]), ("Taurus", 24))
        self.assertIsNone(star["minutes"])
        self.assertIsNone(star["modern_epoch_longitude"])

    def test_unrecorded_lookup_does_not_fall_back_to_another_table(self):
        with self.assertRaises(KeyError):
            ref.source_lookup("house", "Cancer")
        with self.assertRaises(KeyError):
            ref.source_lookup("retained_planet_sign", "Mars|Cancer")

    def test_lookup_result_does_not_mutate_retained_evidence(self):
        item = ref.source_lookup("retained_planet_sign", "Saturn|Cancer")
        item["source_items"].clear()
        self.assertEqual(len(ref.source_lookup("retained_planet_sign", "Saturn|Cancer")["source_items"]), 3)


class SourceRecordIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = json.loads((ROOT / "RULES.json").read_text())
        cls.rules = cls.document["rules"]

    def test_contiguous_new_ids_begin_at_1358(self):
        numbers = [int(row["id"].rsplit("R", 1)[1]) for row in self.rules]
        self.assertEqual(numbers, list(range(1358, 1358 + len(numbers))))
        self.assertEqual(self.document["records_count"], len(numbers))

    def test_all_records_have_checked_source_anchors_and_conditions(self):
        for row in self.rules:
            self.assertTrue(row["source_locator"]["passage_anchor"].strip())
            self.assertTrue(row["source_statement"].strip())
            self.assertIn("condition_logic", row["source_fields"])
            self.assertTrue(set(row["source_locator"]["pdf_pages"]) <= set(range(277, 293)))

    def test_source_records_do_not_claim_runtime_or_independent_validation(self):
        for row in self.rules:
            self.assertEqual(row["runtime_status"], "REFERENCE_ONLY_NOT_PROMOTED")
            self.assertFalse(row["independent_evidence_unit"])
            self.assertIsNone(row["case_id"])

    def test_visible_repeated_page_number_is_retained(self):
        rows = [row for row in self.rules if 280 in row["source_locator"]["pdf_pages"]]
        self.assertTrue(rows)
        for row in rows:
            locator = row["source_locator"]
            index = locator["pdf_pages"].index(280)
            self.assertEqual(locator["visible_printed_labels"][index], "244")
            self.assertEqual(locator["printed_sequence_expected"][index], 246)

    def test_every_record_has_section_coverage(self):
        coverage = json.loads((ROOT / "SECTION_COVERAGE.json").read_text())
        covered = {rid for section in coverage["sections"] for rid in section["record_ids"]}
        self.assertEqual(covered, {row["id"] for row in self.rules})

    def test_continuation_keeps_dariot_heading_and_opening_together(self):
        coverage = json.loads((ROOT / "SECTION_COVERAGE.json").read_text())
        self.assertEqual(coverage["next"]["pdf_page"], 292)
        self.assertEqual(coverage["next"]["heading"], "DARIOT Abridged.")
        self.assertTrue(coverage["next"]["include_opening_paragraph"])
        self.assertFalse(coverage["whole_chapter_complete"])


if __name__ == "__main__":
    unittest.main()
