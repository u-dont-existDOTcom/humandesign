"""Original-source-only Zi Wei mock star applicability and hour-neighbor audit.

Only synthetic cases from 10 selected modern reference dates, no actual people.
"""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch

import audit_conservative_feature_states as subject

B = Path(__file__).resolve().parent
ROOT = B.parents[1]
COLD_ORACLE_FIXTURE = (
    ROOT / "tasks/astro-chart-eligibility-20261020/ORIGINAL_312_SOURCE_ORACLE_SNAPSHOT.json"
)
RESULT = B / "FOUR_ANCHOR_SOURCE_FEATURE_HOUR_SENSITIVITY_V1.json"


class OriginalSyntheticSourceHourSensitivity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.input = subject.oracle.load_pinned_parity_data(
            COLD_ORACLE_FIXTURE if COLD_ORACLE_FIXTURE.is_file() else None
        )
        cls.report = json.loads(RESULT.read_text(encoding="utf-8"))

    def test_01_exact_pinned_prior_accepted_code_report_and_312_raw(self):
        old = subject.check_predecessor()
        self.assertEqual(old["strict_sole_model_eligible_cases"], 12)
        self.assertEqual(subject.sha(subject.UP_CODE.read_bytes()), subject.UP_CODE_SHA)
        self.assertEqual(subject.sha(subject.PREVIOUS.read_bytes()), subject.PREVIOUS_SHA)
        self.assertEqual(self.input["synthetic_cases"], 312)

    def test_02_120_exact_unique_source_configurations_and_schema(self):
        self.assertEqual(self.report["unique_synthetic_source_states"], 120)
        self.assertEqual(len(self.report["all_120_synthetic_states"]), 120)
        self.assertEqual(self.report["actual_people_charted"], 0)
        self.assertEqual(self.report["real_human_forward_or_reverse_predictions_validated"], 0)
        self.assertFalse(self.report["real_natal_chart_scoring_approved"])

    def test_03_mutually_exclusive_status_counts(self):
        self.assertEqual(
            self.report["synthetic_source_state_counts_by_exclusive_status"],
            {
                "ABSTAIN_NO_SELECTED_STAR": 86,
                "ABSTAIN_TWO_SELECTED_STARS": 3,
                "ABSTAIN_OTHER_PRINCIPAL_STAR_PRESENT": 19,
                "ABSTAIN_SELECTED_SOLE_BUT_VENDOR_SCHOOL_DISAGREES": 2,
                "CONDITIONAL_SOURCE_CALCULATION_AGREES_NOT_HUMAN_PREDICTION": 10,
            },
        )
        self.assertEqual(len(self.report["conditional_model_status_definition"]), 5)
        self.assertEqual(
            self.report["strict_methodological_abstentions_from_120_synthetic_states"], 110
        )

    def test_04_four_star_breakdown_restrains_WuQu_absence_claim(self):
        self.assertEqual(
            self.report["conditional_source_mechanics_only_candidate_star_count"],
            {"LianZhen": 1, "PoJun": 6, "TianLiang": 3, "WuQu": 0},
        )
        self.assertTrue(self.report["sampled_dates_not_population_prevalence"])
        self.assertTrue(self.report["no_selected_star_does_not_predict_trait_absence"])

    def test_05_leap_source_school_and_external_oracle_mismatch_not_promoted(self):
        self.assertEqual(self.report["source_only_non_vendor_corrob_leap_cases"], 2)
        self.assertEqual(
            self.report["original_source_school_precommitted_for_mechanics_only"],
            "transmitted Quan Shu leap month always counts as following month",
        )
        self.assertEqual(subject.oracle.PARITY_COMMIT, "6f4a75febc1624e44b54d724422804a05f31fd12")
        self.assertTrue(
            self.report["original_source_school_precommitted_for_mechanics_only"].startswith(
                "transmitted Quan Shu"
            )
        )

    def test_06_structural_conditions_explicit_and_not_default_true_for_co_stars(self):
        cases = self.report["all_120_synthetic_states"]
        for row in cases.values():
            st = row["toy_model_rule_status"]
            stars = row["major_stars_in_Life_palace"]
            selected = row["selected_candidate_stars_in_Life_palace"]
            self.assertTrue(set(selected).issubset(stars))
            if st == "ABSTAIN_NO_SELECTED_STAR":
                self.assertEqual(selected, [])
            elif st == "ABSTAIN_TWO_SELECTED_STARS":
                self.assertEqual(len(selected), 2)
            elif st == "ABSTAIN_OTHER_PRINCIPAL_STAR_PRESENT":
                self.assertEqual(len(selected), 1)
                self.assertGreater(len(stars), 1)
            elif st == "ABSTAIN_SELECTED_SOLE_BUT_VENDOR_SCHOOL_DISAGREES":
                self.assertEqual(len(stars), 1)
                self.assertFalse(row["all_vendor_variants_match_source"])
            else:
                self.assertEqual(st, "CONDITIONAL_SOURCE_CALCULATION_AGREES_NOT_HUMAN_PREDICTION")
                self.assertEqual(len(stars), 1)
                self.assertTrue(row["all_vendor_variants_match_source"])

    def test_07_adjacent_12_strict_cases_preserved_and_all_change_nearby(self):
        counts = self.report["neighbor_Earthly_hour_branch_stress_test_summary"]
        self.assertEqual(
            counts,
            {
                "strict_source_only_candidates": 12,
                "nonwrapping_2_neighbor_checks": 10,
                "cyclic_full_star_stable_with_both_neighbors": 0,
                "both_neighbor_source_oracle_eligible": 0,
                "at_least_one_calendar_wrap_neighbor": 2,
                "both_source_vendor_matched_at_chosen_branch": 10,
            },
        )
        self.assertEqual(
            len(self.report["all_12_strict_source_only_cases_neighboring_branch_checks"]), 12
        )
        for row in self.report["all_12_strict_source_only_cases_neighboring_branch_checks"]:
            self.assertFalse(row["same_full_one_selected_star_with_both_neighbors"])
            self.assertFalse(row["both_neighbor_source_calculation_conditional_eligible"])

    def test_08_zi_hai_midnight_wrap_not_called_true_adjacent_instant(self):
        rows = self.report["all_12_strict_source_only_cases_neighboring_branch_checks"]
        wrapped = [r for r in rows if not r["both_neighbors_nonwrapping"]]
        self.assertEqual(len(wrapped), 2)
        self.assertEqual({r["synthetic_selected_hour_branch"] for r in wrapped}, {"Zi", "Hai"})
        self.assertTrue(
            self.report["near_Zi_Hai_midnight_calendar_day_wrap_invalid_as_real_clock_adjacent"]
        )
        self.assertTrue(
            self.report[
                "neighboring_branch_difference_not_equal_real_clock_uncertainty_probability"
            ]
        )

    def test_09_new_audit_repeat_is_byte_identical_report(self):
        self.assertEqual(subject.audit(self.input), self.report)

    def test_10_reject_pinned_source_document_sha_change(self):
        with (
            patch.object(subject, "PREVIOUS_SHA", "0" * 64),
            self.assertRaisesRegex(ValueError, "changed"),
        ):
            subject.check_predecessor()

    def test_11_reject_empty_or_missing_original_source_vendor_case(self):
        corrupt = copy.deepcopy(self.input)
        corrupt["all_312_case_records"].pop()
        with self.assertRaises(ValueError):
            subject.audit(corrupt)

    def test_12_reject_source_vendor_duplicate_different_geometry(self):
        corrupt = copy.deepcopy(self.input)
        corrupt["all_312_case_records"][1]["source_case"]["life_palace"] = "Fake"
        with self.assertRaises(ValueError):
            subject.audit(corrupt)

    def test_13_wrong_original_traditional_leap_policy_fails(self):
        corrupt = copy.deepcopy(self.input)
        corrupt["chosen_original_leap_rule"] = "choose vendor after responses"
        with self.assertRaisesRegex(ValueError, "school"):
            subject.audit(corrupt)

    def test_14_false_human_predictive_results_fails(self):
        corrupt = copy.deepcopy(self.input)
        corrupt["preregistered_blinded_real_person_tests"] = 1
        with self.assertRaisesRegex(ValueError, "original accepted oracle"):
            subject.audit(corrupt)

    def test_15_overlaps_cannot_be_interpreted_as_single_star_without_source_rule(self):
        star_pairs = [
            ("LianZhen", "QiSha"),
            ("WuQu", "PoJun"),
            ("TianLiang", "TianTong"),
            ("LianZhen", "TianFu"),
        ]
        for selected, other in star_pairs:
            with self.subTest(pair=(selected, other)):
                self.assertEqual(
                    subject.classify(tuple(sorted((selected, other))), True),
                    "ABSTAIN_OTHER_PRINCIPAL_STAR_PRESENT"
                    if other not in subject.SELECTED
                    else "ABSTAIN_TWO_SELECTED_STARS",
                )

    def test_16_all_no_star_selected_abstain_not_negative_behavior(self):
        self.assertEqual(subject.classify(("ZiWei",), True), "ABSTAIN_NO_SELECTED_STAR")
        self.assertTrue(self.report["no_selected_star_does_not_predict_trait_absence"])

    def test_17_if_all_conventions_agree_one_selected_allowed_for_mechanics_only(self):
        self.assertEqual(
            subject.classify(("LianZhen",), True),
            "CONDITIONAL_SOURCE_CALCULATION_AGREES_NOT_HUMAN_PREDICTION",
        )
        self.assertEqual(
            subject.classify(("LianZhen",), False),
            "ABSTAIN_SELECTED_SOLE_BUT_VENDOR_SCHOOL_DISAGREES",
        )
        self.assertFalse(self.report["source_mutually_qualifying_star_rules_expert_collated"])

    def test_18_source_input_never_includes_birth_data_or_questionnaire(self):
        self.assertEqual(self.report["human_questionnaire_responses_collected"], 0)
        self.assertEqual(self.report["production_astro_rule_promotions"], 0)
        self.assertFalse(self.report["independent_natal_civil_to_lunar_time_pipeline_integrated"])
        self.assertFalse(self.report["source_original_chinese_astrology_historic_truth"])
        self.assertTrue(
            all(
                not c["is_actual_calculated_human_birth_chart"]
                for c in self.report["all_120_synthetic_states"].values()
            )
        )


if __name__ == "__main__":
    unittest.main()
