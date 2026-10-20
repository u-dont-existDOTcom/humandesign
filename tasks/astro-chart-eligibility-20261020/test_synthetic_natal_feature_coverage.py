"""Mechanical Zi Wei source-only chart-feature availability, not human testing."""

from __future__ import annotations

import json
import tempfile
import unittest
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch

import audit_synthetic_natal_feature_coverage as audit

B = Path(__file__).resolve().parent
ROOT = B.parents[1]
REPORT = B / "SYNTHETIC_CHART_FOUR_ANCHOR_ELIGIBILITY_AUDIT_V1.json"
SNAPSHOT = B / "ORIGINAL_312_SOURCE_ORACLE_SNAPSHOT.json"


class OriginalSourceChartEligibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = audit.load_pinned_parity_data(SNAPSHOT if SNAPSHOT.is_file() else None)
        cls.report = json.loads(REPORT.read_text(encoding="utf-8"))

    def test_01_pinned_312_original_oracle_SHA_and_commit(self):
        self.assertEqual(audit.PARITY_COMMIT, "6f4a75febc1624e44b54d724422804a05f31fd12")
        self.assertEqual(
            audit.PARITY_SHA, "01efe5181d7c9d07a6c9f780df9d03b557b356baa4ca3770464f38e8552feaa5"
        )
        self.assertEqual(self.fixture["synthetic_cases"], 312)
        self.assertEqual(self.fixture["original_official_HKO_dates"], 10)
        self.assertEqual(self.fixture["preregistered_blinded_real_person_tests"], 0)
        self.assertFalse(self.fixture["birthplace_local_to_calendar_date_verified"])

    def test_02_original_four_behavior_candidates_same_source_SHA(self):
        anchors = audit.verify_candidates()
        self.assertEqual(anchors, ("LianZhen", "PoJun", "TianLiang", "WuQu"))
        self.assertEqual(
            self.report["pin_unvalidated_four_question_source_map_sha256"], audit.SOURCE_MAPPING_SHA
        )
        self.assertEqual(sha256(audit.MAP.read_bytes()).hexdigest(), audit.SOURCE_MAPPING_SHA)

    def test_03_312_raw_gender_leap_options_are_not_312_persons(self):
        raw = self.report["raw_comparison_counts_not_independent_source_chart_cases"]
        self.assertEqual(
            raw,
            {
                "cases": 312,
                "matched": 192,
                "mismatched": 120,
                "leap_comparisons": 144,
                "nonleap_comparisons": 168,
            },
        )
        self.assertTrue(self.report["all_312_records_are_synthetic_comparison_not_real_subjects"])
        self.assertEqual(self.report["empirical_human_chart_predictions_validated"], 0)

    def test_04_de_dup_date_and_hour_correctly_120_states(self):
        self.assertEqual(self.report["number_of_selected_reference_dates"], 10)
        self.assertEqual(self.report["number_of_synthetic_hour_branches_per_date"], 12)
        v = self.report["unique_source_chart_coverage_counts"]
        self.assertEqual(v["unique_source_chart_states"], 120)
        self.assertEqual(v["nonleap_unique_states"], 84)
        self.assertEqual(v["leap_unique_states"], 36)
        self.assertEqual(
            len(self.report["ten_selected_reference_dates_each_twelve_synthetic_branch_outcomes"]),
            10,
        )

    def test_05_life_house_zero_one_two_star_configurations(self):
        v = self.report["unique_source_chart_coverage_counts"]
        self.assertEqual([v[f"life_palace_star_count_{i}"] for i in range(3)], [23, 59, 38])
        self.assertEqual(v["no_selected_star_states"], 86)
        self.assertEqual(v["any_selected_star_states"], 34)
        self.assertEqual(v["selected_stars_with_any_conjunction"], 22)
        self.assertEqual(v["two_selected_stars_states"], 3)
        self.assertEqual(v["exactly_one_selected_star_states"], 31)

    def test_06_strict_only_12_eligible_and_WuQu_zero(self):
        self.assertEqual(self.report["strict_sole_model_eligible_cases"], 12)
        self.assertEqual(self.report["strict_sole_model_abstentions"], 108)
        self.assertEqual(self.report["strict_sole_model_eligibility_fraction_toy_dataset"], 0.1)
        self.assertEqual(
            self.report["strict_sole_star_counts"],
            {"LianZhen": 2, "PoJun": 6, "TianLiang": 4, "WuQu": 0},
        )
        self.assertEqual(len(self.report["all_12_sole_selected_synthetic_cases"]), 12)

    def test_07_sole_selected_10_cases_with_all_raw_vendor_parity(self):
        v = self.report["unique_source_chart_coverage_counts"]
        self.assertEqual(v["sole_selected_any_vendor_match"], 10)
        self.assertEqual(v["sole_selected_all_vendor_match"], 10)
        self.assertEqual(
            sum(
                not c["source_original_leap_month"]
                for c in self.report["all_12_sole_selected_synthetic_cases"]
            ),
            10,
        )
        self.assertEqual(
            sum(
                c["source_original_leap_month"]
                for c in self.report["all_12_sole_selected_synthetic_cases"]
            ),
            2,
        )

    def test_08_vendor_parity_aggregated_without_selecting_best_leap_policy(self):
        v = self.report["grouped_independent_vendor_raw_parity"]
        self.assertEqual(
            (v["all_vendor_match"], v["any_vendor_match"], v["none_vendor_match"]), (84, 96, 24)
        )
        self.assertEqual(
            self.report["source_leap_month_school_rule"],
            "transmitted Quan Shu leap month always counts as following month",
        )
        self.assertTrue(self.report["source_original_leap_policy_not_overwritten"])

    def test_09_no_claim_of_population_prevalence_or_representative_cohort(self):
        self.assertTrue(self.report["selected_dates_not_statistical_representative_population"])
        self.assertTrue(
            self.report["no_birthplace_historical_iana_or_apparent_solar_time_verification"]
        )
        self.assertTrue(self.report["other_major_stars_and_all_source_modifiers_not_resolved"])
        self.assertEqual(self.report["real_person_birth_records_included"], 0)

    def test_10_results_recompute_exact_without_duplicate_input_changes(self):
        expected = audit.evaluate(self.fixture)
        self.assertEqual(expected, self.report)

    def test_11_reject_changed_original_pinned_fixture_sha(self):
        with tempfile.TemporaryDirectory() as d:
            fp = Path(d) / "tampered.json"
            data = self.fixture.copy()
            data["synthetic_cases"] = 313
            fp.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "byte count/SHA"):
                audit.load_pinned_parity_data(fp)

    def test_12_missing_vendor_row_is_detected(self):
        data = deepcopy(self.fixture)
        data["all_312_case_records"].pop()
        with self.assertRaisesRegex(ValueError, "source fixture totals"):
            audit.evaluate(data)

    def test_13_duplicate_pseudocase_id_fails(self):
        data = deepcopy(self.fixture)
        data["all_312_case_records"][0]["id"] = data["all_312_case_records"][1]["id"]
        with self.assertRaisesRegex(ValueError, "ID duplicated"):
            audit.evaluate(data)

    def test_14_non_synthetic_private_chart_fields_not_accepted(self):
        data = deepcopy(self.fixture)
        data["all_312_case_records"][0]["source_case"]["birth_record_id"] = "person-identifying"
        with self.assertRaisesRegex(ValueError, "chart fields changed"):
            audit.evaluate(data)

    def test_15_original_source_year_school_policies_cannot_change(self):
        data = deepcopy(self.fixture)
        data["chosen_original_leap_rule"] = "vendor convention picked for nice results"
        with self.assertRaisesRegex(ValueError, "leap month policy"):
            audit.evaluate(data)

    def test_16_original_engine_match_flags_must_be_true_to_raw_outputs(self):
        data = deepcopy(self.fixture)
        data["all_312_case_records"][0]["match"] = not data["all_312_case_records"][0]["match"]
        with self.assertRaisesRegex(ValueError, "match flag"):
            audit.evaluate(data)

    def test_17_original_engine_source_status_not_promoted(self):
        data = deepcopy(self.fixture)
        data["all_312_case_records"][0]["source_case"]["source_status"] = (
            "psychological_accuracy_validated"
        )
        with self.assertRaisesRegex(ValueError, "status unexpectedly promoted"):
            audit.evaluate(data)

    def test_18_gender_or_vendor_duplicate_changes_chart_source_geometry_fails(self):
        data = deepcopy(self.fixture)
        data["all_312_case_records"][1]["source_case"]["life_palace"] = (
            "AnIllegalDifferentLifePalace"
        )
        with self.assertRaises(ValueError):
            audit.evaluate(data)

    def test_19_four_source_question_map_sha_tampering_fails(self):
        path = audit.MAP
        with (
            patch.object(audit, "SOURCE_MAPPING_SHA", "0" * 64),
            self.assertRaisesRegex(ValueError, "candidate mapping SHA drift"),
        ):
            audit.verify_candidates()
        self.assertTrue(path.exists())

    def test_20_ancient_source_and_mechanics_not_empirical_predictor(self):
        self.assertFalse(self.fixture["independent_ancient_imprint_authenticated"])
        self.assertEqual(self.fixture["runtime_astrological_forecast_promotions"], 0)
        self.assertEqual(self.report["astrological_production_rules_promoted"], 0)
        self.assertEqual(self.report["participant_questionnaire_data_included"], 0)
        self.assertEqual(self.report["empirical_human_chart_predictions_validated"], 0)


if __name__ == "__main__":
    unittest.main()
