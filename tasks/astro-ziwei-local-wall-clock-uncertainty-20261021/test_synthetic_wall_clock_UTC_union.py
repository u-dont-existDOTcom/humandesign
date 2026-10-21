"""Exact original PEP495 fall folds and spring gaps with synthetic wall clocks.

Pinned source engine is mathematical/partially historical, not verified
human astrological behavioral evidence. No actual private birth information.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo

import run_source_pinned_local_wall_UTC_union as module

B = Path(__file__).resolve().parent
ROOT = B.parents[1]
FILE = B / "PINNED_SOURCE_SYNTHETIC_WALL_CLOCK_UTC_FOLD_UNION_V1.json"
WORKER = B / "worker_synthetic_local_wall_clock_to_UTC_set.py"


def read(p):
    return json.loads(p.read_text(encoding="utf-8"))


class SourcePinnedSyntheticLocalWallUncertaintyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = read(FILE)
        cls.data = cls.receipt["mock_local_wall_clock_set_results"]
        cls.cases = {c["case_id"]: c for c in cls.data["cases"]}
        # Exact original source modules, entirely temporary; never overwrite
        # the published natal engine or use real participant clock records.
        cls.temp = tempfile.TemporaryDirectory(prefix="ziwei_wall_clock_worker_under_test_")
        root = Path(cls.temp.name)
        module.verify_parent()
        sys.path.insert(0, str(module.PARENT))
        try:
            import run_source_pinned_utc_intervals as prior
        finally:
            sys.path.pop(0)
        _, source = prior.get_original_source()
        for name, raw in source.items():
            p = root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(raw)
        original_worker = (
            root
            / "tasks"
            / "astro-ziwei-finite-utc-uncertainty-20261020"
            / "worker_synthetic_utc_interval_states.py"
        )
        original_worker.parent.mkdir(parents=True, exist_ok=True)
        original_worker.write_bytes(module.PARENT_WORKER.read_bytes())
        cls.engine_dir = root / "tasks/astro-chinese-primary-sources-20261017/ziwei"
        cls.old_worker_dir = original_worker.parent
        sys.path.insert(0, str(cls.engine_dir))
        sys.path.insert(0, str(cls.old_worker_dir))
        spec = importlib.util.spec_from_file_location("synthetic_wall_clock_worker_test", WORKER)
        cls.worker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.worker)

    @classmethod
    def tearDownClass(cls):
        sys.path.remove(str(cls.old_worker_dir))
        sys.path.remove(str(cls.engine_dir))
        cls.temp.cleanup()

    def test_01_parent_SHA_and_original_natal_engine_pinned(self):
        module.verify_parent()
        self.assertEqual(
            self.receipt["original_accepted_UTC_interval_parent_commit"], module.PARENT_COMMIT
        )
        self.assertEqual(self.receipt["original_parent_runner_sha256"], module.PARENT_RUNNER_SHA)
        self.assertEqual(self.receipt["original_parent_worker_sha256"], module.PARENT_WORKER_SHA)
        self.assertEqual(self.receipt["original_parent_result_sha256"], module.PARENT_REPORT_SHA)
        self.assertEqual(
            self.receipt["original_Chinese_natal_source_engine_git_commit"],
            "fb6b30b1ca67ff62fecc0c4ea7f3e4d0553640d4",
        )
        self.assertEqual(len(self.receipt["pinned_chinese_engine_original_module_sha256"]), 22)

    def test_02_exact_two_external_original_lunar_software_versions_sha(self):
        self.assertEqual(
            self.receipt["pinned_external_package_versions"],
            {"lunar_python": "1.4.8", "sxtwl": "2.0.7"},
        )
        self.assertEqual(
            self.receipt["external_lunar_package_source_and_binary_tree_pinned_unbundled"],
            {
                "lunar_python": "7123d898cbe2e8afff663e57a7e25c9d4f080e383b98fcc33485d502772a2303",
                "sxtwl": "b4c1b25f0453489e10c6d25c5407e904a31e7fca1dc72615fda5db169f143d14",
            },
        )
        self.assertFalse(
            self.receipt["source_ASTRO_complete_real_birthplace_hour_uncertainty_covered"]
        )

    def test_03_six_fictional_local_clock_cases_and_total_counts(self):
        self.assertEqual(self.data["number_of_entirely_fictional_wall_clock_cases"], 6)
        self.assertEqual(
            self.data["sum_of_independent_artificial_local_wall_seconds_across_cases"], 1026
        )
        self.assertEqual(self.data["sum_of_UTC_candidates_including_two_fold_branches"], 995)
        self.assertEqual(len(self.cases), 6)
        self.assertEqual(
            [
                self.cases[x]["valid_UTC_candidate_instants_including_both_DST_folds"]
                for x in self.cases
            ],
            [362, 90, 0, 181, 181, 181],
        )

    def test_04_NY_fall_fold_both_independent_UTC_instants_preserved(self):
        case = self.cases["SYNTH_NY_FALL_FOLD_LOCAL_0130"]
        self.assertEqual(case["status"], "ALL_VALID_BOTH_DST_FOLDS_PRESERVED_SOURCE_ONLY")
        self.assertEqual(case["original_local_clock_interval_length_seconds"], 181)
        self.assertEqual(case["ambiguous_local_clock_second_count"], 181)
        self.assertEqual(case["valid_local_clock_second_count"], 181)
        self.assertEqual(case["valid_UTC_candidate_instants_including_both_DST_folds"], 362)
        self.assertEqual(case["number_of_separate_UTC_components"], 2)
        self.assertEqual(case["nonexistent_local_clock_second_count"], 0)
        self.assertEqual(
            case["disjoint_exact_contiguous_UTC_components"],
            [
                {
                    "start_UTC": "2026-11-01T05:28:30+00:00",
                    "end_UTC": "2026-11-01T05:31:30+00:00",
                    "whole_UTC_second_count": 181,
                },
                {
                    "start_UTC": "2026-11-01T06:28:30+00:00",
                    "end_UTC": "2026-11-01T06:31:30+00:00",
                    "whole_UTC_second_count": 181,
                },
            ],
        )

    def test_05_NY_fall_fold_source_UTC_candidates_include_fold0_and_fold1(self):
        case = self.cases["SYNTH_NY_FALL_FOLD_LOCAL_0130"]
        pair = [
            x
            for x in case["all_valid_local_wall_to_UTC_candidates"]
            if x["local_wall_second"] == "2026-11-01T01:30:00"
        ]
        self.assertEqual(len(pair), 2)
        self.assertEqual(
            {x["UTC_instant"] for x in pair},
            {"2026-11-01T05:30:00+00:00", "2026-11-01T06:30:00+00:00"},
        )
        self.assertEqual({x["recorded_wall_fold"] for x in pair}, {0, 1})
        self.assertEqual({x["historical_zone_UTC_offset_seconds"] for x in pair}, {-14400, -18000})

    def test_06_NY_fold_mechanical_chart_changes_due_to_local_mean_solar(self):
        case = self.cases["SYNTH_NY_FALL_FOLD_LOCAL_0130"]
        self.assertEqual(
            case["original_source_unique_chart_states_across_all_UTC_and_calendar_hour_policies"], 2
        )
        self.assertFalse(case["mechanical_full_source_chart_invariant_if_no_clock_gap"])
        self.assertEqual(
            case["all_source_star_status_categories"],
            ["ABSTAIN_NO_SELECTED_STAR_NOT_TRAIT_ABSENCE"],
        )
        components = case["source_chart_results_for_each_UTC_component"]
        self.assertEqual(len(components), 2)
        self.assertEqual(
            {
                tuple(s["life_palace_major_stars"])
                for component in components
                for policy in component["four_calendar_hour_policy_runs"]
                for s in policy["source_chart_segment_states"]
            },
            {(), ("TanLang",)},
        )

    def test_07_spring_gap_partial_fails_closed_despite_valid_source_diagnostic(self):
        case = self.cases["SYNTH_NY_SPRING_GAP_PARTIAL_LOCAL_0200"]
        self.assertEqual(case["status"], "ABSTAIN_PARTIAL_LOCAL_WALL_CLOCK_GAP")
        self.assertEqual(case["original_local_clock_interval_length_seconds"], 181)
        self.assertEqual(case["nonexistent_local_clock_second_count"], 91)
        self.assertEqual(case["valid_local_clock_second_count"], 90)
        self.assertEqual(case["valid_UTC_candidate_instants_including_both_DST_folds"], 90)
        self.assertEqual(case["number_of_separate_UTC_components"], 1)
        self.assertFalse(case["mechanical_full_source_chart_invariant_if_no_clock_gap"])
        self.assertEqual(
            case["disjoint_exact_contiguous_UTC_components"],
            [
                {
                    "start_UTC": "2026-03-08T06:58:30+00:00",
                    "end_UTC": "2026-03-08T06:59:59+00:00",
                    "whole_UTC_second_count": 90,
                }
            ],
        )

    def test_08_entire_nonexistent_spring_clock_returns_zero_UTC_candidates(self):
        case = self.cases["SYNTH_NY_SPRING_GAP_ALL_LOCAL_0230"]
        self.assertEqual(case["status"], "REJECT_ALL_LOCAL_WALL_TIMES_NONEXISTENT")
        self.assertEqual(case["nonexistent_local_clock_second_count"], 121)
        self.assertEqual(case["valid_local_clock_second_count"], 0)
        self.assertEqual(case["number_of_separate_UTC_components"], 0)
        self.assertEqual(case["source_chart_results_for_each_UTC_component"], [])
        self.assertEqual(
            case["original_source_unique_chart_states_across_all_UTC_and_calendar_hour_policies"], 0
        )

    def test_09_four_valid_date_day_hour_policies_propagated_across_fold_union(self):
        for case in self.cases.values():
            for component in case["source_chart_results_for_each_UTC_component"]:
                self.assertEqual(len(component["four_calendar_hour_policy_runs"]), 4)
                self.assertEqual(
                    component["source_lunar_leap_school_predeclared"],
                    "transmitted_quan_shu_as_next",
                )
                self.assertTrue(
                    all(
                        r["source_lunar_leap_policy"] == "transmitted_quan_shu_as_next"
                        for r in component["four_calendar_hour_policy_runs"]
                    )
                )

    def test_10_all_wall_clock_second_to_UTC_candidates_unique_and_range_exact(self):
        for case in self.cases.values():
            valid = case["all_valid_local_wall_to_UTC_candidates"]
            self.assertEqual(
                len(valid), case["valid_UTC_candidate_instants_including_both_DST_folds"]
            )
            self.assertEqual(len({x["UTC_instant"] for x in valid}), len(valid))
            count = sum(
                x["whole_UTC_second_count"]
                for x in case["disjoint_exact_contiguous_UTC_components"]
            )
            self.assertEqual(count, len(valid))
            self.assertEqual(
                case["valid_local_clock_second_count"]
                + case["nonexistent_local_clock_second_count"],
                case["original_local_clock_interval_length_seconds"],
            )
            self.assertEqual(
                len(case["source_chart_results_for_each_UTC_component"]),
                case["number_of_separate_UTC_components"],
            )

    def test_11_Dakar_LNY_source_calendar_and_hour_uncertainty_propagated(self):
        case = self.cases["SYNTH_DAKAR_LUNAR_NEW_YEAR_LOCAL_2100"]
        self.assertEqual(
            case["original_source_unique_chart_states_across_all_UTC_and_calendar_hour_policies"], 4
        )
        self.assertEqual(case["number_of_separate_UTC_components"], 1)
        self.assertEqual(case["nonexistent_local_clock_second_count"], 0)
        self.assertFalse(case["mechanical_full_source_chart_invariant_if_no_clock_gap"])
        self.assertEqual(
            set(case["all_source_star_status_categories"]),
            {
                "ABSTAIN_NO_SELECTED_STAR_NOT_TRAIT_ABSENCE",
                "ABSTAIN_OTHER_MAJOR_STAR_CONJUNCTION_UNRESOLVED",
            },
        )

    def test_12_HK_historic_DST_no_missing_local_clock_but_chart_varies(self):
        case = self.cases["SYNTH_HK_HISTORIC_DST_LOCAL_005930"]
        self.assertEqual(case["valid_local_clock_second_count"], 181)
        self.assertEqual(case["number_of_separate_UTC_components"], 1)
        self.assertEqual(
            case["original_source_unique_chart_states_across_all_UTC_and_calendar_hour_policies"], 3
        )
        self.assertIn(
            "SOURCE_ONLY_SINGLE_STAR_LAYOUT_NOT_PREDICTIVE_VALIDITY",
            case["all_source_star_status_categories"],
        )

    def test_13_HK_leap_hour_selected_four_absent_not_predicted_negative(self):
        case = self.cases["SYNTH_HK_2023_LEAP_LOCAL_125930"]
        self.assertEqual(case["valid_local_clock_second_count"], 181)
        self.assertEqual(
            case["original_source_unique_chart_states_across_all_UTC_and_calendar_hour_policies"], 2
        )
        self.assertEqual(
            case["all_source_star_status_categories"],
            ["ABSTAIN_NO_SELECTED_STAR_NOT_TRAIT_ABSENCE"],
        )
        self.assertTrue(
            case["mechanical_anchor_presence_status_invariant_without_trait_validation"]
        )
        self.assertFalse(case["source_summary_is_a_real_behavioral_prediction"])

    def test_14_entire_2057_original_calendar_disagreement_refused(self):
        record = self.data["entirely_rejected_2057_source_date"]
        self.assertTrue(record["refused"])
        self.assertEqual(record["failure_class"], "CalendarParityError")
        self.assertIn("disagree", record["reason"])
        self.assertEqual(record["synthetic_source_case"], "SYNTH_2057_DISPUTED_CALENDAR_LOCAL_1200")

    def test_15_direct_PE495_Fold_and_spring_gap_local_UTC_candidates(self):
        ny = ZoneInfo("America/New_York")
        fold = self.worker.utc_candidates_for_local_second(datetime(2026, 11, 1, 1, 30), ny)
        self.assertEqual(len(fold), 2)
        self.assertEqual({x["recorded_wall_fold"] for x in fold}, {0, 1})
        spring = self.worker.utc_candidates_for_local_second(datetime(2026, 3, 8, 2, 30), ny)
        self.assertEqual(spring, [])
        ordinary = self.worker.utc_candidates_for_local_second(datetime(2026, 3, 8, 1, 30), ny)
        self.assertEqual(len(ordinary), 1)
        self.assertEqual(ordinary[0]["recorded_wall_fold"], 0)

    def test_16_direct_UTC_contiguous_components_complete_and_fold_disjoint(self):
        cases = self.cases["SYNTH_NY_FALL_FOLD_LOCAL_0130"]
        instants = sorted(
            datetime.fromisoformat(s["UTC_instant"])
            for s in cases["all_valid_local_wall_to_UTC_candidates"]
        )
        self.assertEqual(
            self.worker.connected_UTC_groups(instants),
            [
                (
                    datetime.fromisoformat("2026-11-01T05:28:30+00:00"),
                    datetime.fromisoformat("2026-11-01T05:31:30+00:00"),
                ),
                (
                    datetime.fromisoformat("2026-11-01T06:28:30+00:00"),
                    datetime.fromisoformat("2026-11-01T06:31:30+00:00"),
                ),
            ],
        )

    def test_17_invalid_synthetic_wall_input_shape_DOB_and_long_margin_fail(self):
        simple = deepcopy(self.worker.MOCK_CASES[0])
        simple["personal_birth_id"] = "not allowed"
        with self.assertRaisesRegex(ValueError, "exact five approved fields"):
            self.worker.checked_wall_case(simple)
        for value in (151, 300, -1, True, 1.25):
            invalid = deepcopy(self.worker.MOCK_CASES[0])
            invalid["uncertainty_seconds"] = value
            with (
                self.subTest(value=str(value)),
                self.assertRaisesRegex(ValueError, "out of bounds"),
            ):
                self.worker.checked_wall_case(invalid)
        invalid = deepcopy(self.worker.MOCK_CASES[0])
        invalid["fictional_iana_zone"] = "Unsupported/UnknownZoneName"
        with self.assertRaisesRegex(ValueError, "IANA"):
            self.worker.checked_wall_case(invalid)

    def test_18_UTC_duplicate_or_bad_order_cannot_be_accepted_as_complete(self):
        cases = self.cases["SYNTH_NY_FALL_FOLD_LOCAL_0130"]
        instants = sorted(
            datetime.fromisoformat(s["UTC_instant"])
            for s in cases["all_valid_local_wall_to_UTC_candidates"]
        )
        bad = instants[:]
        bad[1] = bad[0]
        with self.assertRaisesRegex(ValueError, "sorted and unique"):
            self.worker.connected_UTC_groups(bad)
        bad = instants[::-1]
        with self.assertRaisesRegex(ValueError, "sorted and unique"):
            self.worker.connected_UTC_groups(bad)

    def test_19_parent_source_mutation_refused_before_running_binary(self):
        with (
            patch.object(module, "PARENT_WORKER_SHA", "0" * 64),
            self.assertRaisesRegex(ValueError, "checker/receipt changed"),
        ):
            module.verify_parent()

    def test_20_real_person_claims_unverified_and_invariant_not_predictive(self):
        self.assertFalse(self.receipt["astrological_source_a_real_person_trait_predictor"])
        self.assertFalse(
            self.receipt["source_ASTRO_complete_real_birthplace_hour_uncertainty_covered"]
        )
        self.assertTrue(self.receipt["source_traditional_23h_Zi_day_apparent_solar_unimplemented"])
        self.assertEqual(self.receipt["real_human_blind_chart_outcome_validations"], 0)
        self.assertEqual(self.receipt["astrological_runtime_rule_promotions"], 0)
        self.assertEqual(self.data["real_human_chart_outcomes_or_predictions_validated"], 0)
        self.assertEqual(self.data["real_person_birth_records"], 0)


if __name__ == "__main__":
    unittest.main()
