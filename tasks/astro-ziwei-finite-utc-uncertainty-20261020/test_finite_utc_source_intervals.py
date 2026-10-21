"""Zi Wei finite explicitly synthetic UTC instants, original engine source.

These are mathematical source-layout tests, not human birth-time probabilities,
calibrated astrology traits or an original Ming-print verification.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from copy import deepcopy
from datetime import timedelta
from pathlib import Path
from unittest.mock import patch

import run_source_pinned_utc_intervals as parent

B = Path(__file__).resolve().parent
ROOT = B.parents[1]
RESULT = B / "FINITE_UTC_SECOND_SYNTHETIC_ORIGINAL_SOURCE_CHART_SETS_V1.json"
WORKER = B / "worker_synthetic_utc_interval_states.py"
ORIGINAL_COMMIT = "fb6b30b1ca67ff62fecc0c4ea7f3e4d0553640d4"


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


class OriginalSourceFiniteUTCIntervalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.outer = load(RESULT)
        cls.d = cls.outer["synthetic_UTC_integer_second_interval_output"]
        cls.cases = {x["case_id"]: x for x in cls.d["case_results"]}

    def test_01_original_engines_and_22_HKO_source_sha_pinned(self):
        self.assertEqual(self.outer["source_engine_git_commit"], ORIGINAL_COMMIT)
        self.assertEqual(self.outer["source_original_manifest_SHA256"], parent.PARENT_MANIFEST_SHA)
        self.assertEqual(
            self.outer["source_original_calculation_runner_SHA256"], parent.PARENT_ENGINE_RUNNER_SHA
        )
        self.assertEqual(
            self.outer["source_previous_policy_oracle_report_SHA256"], parent.PARENT_REPORT_SHA
        )
        self.assertEqual(len(self.outer["source_22_original_engine_files_sha256"]), 22)
        self.assertEqual(
            parent.sha(parent.PARENT_MANIFEST.read_bytes()), parent.PARENT_MANIFEST_SHA
        )
        self.assertEqual(parent.sha(parent.PARENT_REPORT.read_bytes()), parent.PARENT_REPORT_SHA)
        self.assertEqual(
            parent.sha(parent.PARENT_RUNNER.read_bytes()), parent.PARENT_ENGINE_RUNNER_SHA
        )

    def test_02_external_two_pinned_versions_and_binary_tree_SHA(self):
        self.assertEqual(
            self.outer["pinned_external_calendar_package_versions"],
            {"lunar_python": "1.4.8", "sxtwl": "2.0.7"},
        )
        self.assertEqual(
            self.outer["pinned_external_calendar_binary_source_tree_sha256"],
            {
                "lunar_python": "7123d898cbe2e8afff663e57a7e25c9d4f080e383b98fcc33485d502772a2303",
                "sxtwl": "b4c1b25f0453489e10c6d25c5407e904a31e7fca1dc72615fda5db169f143d14",
            },
        )
        self.assertFalse(self.outer["external_calendar_package_binaries_included_in_repository"])

    def test_03_exact_6_fake_intervals_and_1206_integer_UTC_instants(self):
        self.assertEqual(self.d["fictional_UTC_intervals"], 6)
        self.assertEqual(len(self.d["case_results"]), 6)
        self.assertEqual(
            self.d["fake_integer_UTC_seconds_by_case"],
            {
                "SYNTH_DAKAR_CIVIL_HOUR_BOUNDARY": 121,
                "SYNTH_DAKAR_LUNAR_NEW_YEAR_UTC8_MIDNIGHT": 121,
                "SYNTH_NY_LOCAL_MEAN_SOLAR_HOUR_BOUNDARY": 601,
                "SYNTH_HK_1965_DST_UTC8_MIDNIGHT": 121,
                "SYNTH_NY_2026_DST_FOLD_UTC_INSTANT": 121,
                "SYNTH_HK_2023_LEAP_HOUR_BOUNDARY": 121,
            },
        )
        self.assertEqual(self.d["total_fake_integer_second_instants_unique_by_case"], 1206)
        self.assertEqual(self.d["number_of_declared_calendar_hour_policies_per_case"], 4)

    def test_04_each_policy_covers_every_second_without_gaps(self):
        from datetime import datetime

        total = 0
        for case in self.d["case_results"]:
            start = datetime.fromisoformat(case["start_UTC"])
            end = datetime.fromisoformat(case["end_UTC"])
            n = case["total_original_UTC_integer_second_inclusive_samples"]
            self.assertEqual(int((end - start).total_seconds()) + 1, n)
            self.assertTrue(case["interval_exact_only_at_declared_integer_second_resolution"])
            self.assertTrue(case["all_birth_instants_fictitious"])
            self.assertEqual(len(case["four_calendar_hour_policy_runs"]), 4)
            for policy in case["four_calendar_hour_policy_runs"]:
                self.assertEqual(
                    sum(
                        row["integer_second_samples"]
                        for row in policy["source_chart_segment_states"]
                    ),
                    n,
                )
                self.assertEqual(policy["interval_integer_second_samples"], n)
                fragments = policy["source_chart_segment_states"]
                self.assertEqual(datetime.fromisoformat(fragments[0]["start_UTC_inclusive"]), start)
                self.assertEqual(datetime.fromisoformat(fragments[-1]["end_UTC_inclusive"]), end)
                for i, row in enumerate(fragments):
                    a = datetime.fromisoformat(row["start_UTC_inclusive"])
                    b = datetime.fromisoformat(row["end_UTC_inclusive"])
                    self.assertEqual(
                        int((b - a).total_seconds()) + 1, row["integer_second_samples"]
                    )
                    if i:
                        previous = datetime.fromisoformat(fragments[i - 1]["end_UTC_inclusive"])
                        self.assertEqual(previous + timedelta(seconds=1), a)
            total += n
        self.assertEqual(total, 1206)

    def test_05_source_lunar_and_hour_policies_named_not_chosen_after_answers(self):
        self.assertEqual(
            self.d["source_acceptance"],
            (
                "Pinned original source engine as-next lunar leap, "
                "HKO raw and two external calendars"
            ),
        )
        self.assertTrue(
            self.d[
                "only_exact_integer_second_UTC_interval_no_real_unknown_clock_to_instant_conversion"
            ]
        )
        for case in self.d["case_results"]:
            self.assertEqual(
                {
                    (r["calendar_reference_day_policy"], r["hour_Earthly_branch_policy"])
                    for r in case["four_calendar_hour_policy_runs"]
                },
                {
                    ("same_instant_fixed_utc_plus_8_calendar_day", "recorded_local_civil_clock"),
                    ("same_instant_fixed_utc_plus_8_calendar_day", "local_mean_solar_longitude"),
                    ("birth_site_civil_date_hko_lookup", "recorded_local_civil_clock"),
                    ("birth_site_civil_date_hko_lookup", "local_mean_solar_longitude"),
                },
            )
            self.assertTrue(
                all(
                    r["source_lunar_leap_policy"] == "transmitted_quan_shu_as_next"
                    for r in case["four_calendar_hour_policy_runs"]
                )
            )

    def test_06_result_distinct_full_source_states_and_invariance(self):
        self.assertEqual(
            {
                k: r["distinct_source_calendar_hour_life_full14_states_across_all_seconds_policies"]
                for k, r in self.cases.items()
            },
            {
                "SYNTH_DAKAR_CIVIL_HOUR_BOUNDARY": 4,
                "SYNTH_DAKAR_LUNAR_NEW_YEAR_UTC8_MIDNIGHT": 4,
                "SYNTH_NY_LOCAL_MEAN_SOLAR_HOUR_BOUNDARY": 4,
                "SYNTH_HK_1965_DST_UTC8_MIDNIGHT": 3,
                "SYNTH_NY_2026_DST_FOLD_UTC_INSTANT": 1,
                "SYNTH_HK_2023_LEAP_HOUR_BOUNDARY": 2,
            },
        )
        self.assertEqual(
            sum(c["source_all_policy_invariant_14star_state"] for c in self.cases.values()), 1
        )
        self.assertEqual(
            {
                k
                for k, c in self.cases.items()
                if c["source_all_policy_invariant_four_anchor_status_only"]
            },
            {
                "SYNTH_NY_2026_DST_FOLD_UTC_INSTANT",
                "SYNTH_HK_2023_LEAP_HOUR_BOUNDARY",
            },
        )

    def test_07_Dakar_civil_Earthly_hour_boundary_switch_exactly_21_UTC(self):
        case = self.cases["SYNTH_DAKAR_CIVIL_HOUR_BOUNDARY"]
        policies = {
            (r["calendar_reference_day_policy"], r["hour_Earthly_branch_policy"]): r
            for r in case["four_calendar_hour_policy_runs"]
        }
        for cal in (
            "same_instant_fixed_utc_plus_8_calendar_day",
            "birth_site_civil_date_hko_lookup",
        ):
            fragments = policies[(cal, "recorded_local_civil_clock")]["source_chart_segment_states"]
            self.assertEqual([f["integer_second_samples"] for f in fragments], [60, 61])
            self.assertEqual([f["selected_hour_branch"] for f in fragments], ["Xu", "Hai"])
            self.assertEqual(fragments[0]["end_UTC_inclusive"], "2026-02-16T20:59:59+00:00")
            self.assertEqual(fragments[1]["start_UTC_inclusive"], "2026-02-16T21:00:00+00:00")
            solar = policies[(cal, "local_mean_solar_longitude")]
            self.assertEqual(len(solar["source_chart_segment_states"]), 1)

    def test_08_Dakar_new_year_fixed_utc8_midnight_is_not_local_civil_day(self):
        case = self.cases["SYNTH_DAKAR_LUNAR_NEW_YEAR_UTC8_MIDNIGHT"]
        p = {r["calendar_reference_day_policy"]: [] for r in case["four_calendar_hour_policy_runs"]}
        for r in case["four_calendar_hour_policy_runs"]:
            p[r["calendar_reference_day_policy"]].append(r)
        fixed = p["same_instant_fixed_utc_plus_8_calendar_day"]
        local = p["birth_site_civil_date_hko_lookup"]
        self.assertTrue(all(len(x["source_chart_segment_states"]) == 2 for x in fixed))
        self.assertTrue(all(len(x["source_chart_segment_states"]) == 1 for x in local))
        self.assertEqual(
            [x["integer_second_samples"] for x in fixed[0]["source_chart_segment_states"]], [60, 61]
        )
        self.assertEqual(
            {x["source_calendar_day"] for y in fixed for x in y["source_chart_segment_states"]},
            {"2026-02-16", "2026-02-17"},
        )

    def test_09_NY_mean_solar_UTC_minus_4_56_hour_crosses_1756_UTC(self):
        case = self.cases["SYNTH_NY_LOCAL_MEAN_SOLAR_HOUR_BOUNDARY"]
        for r in case["four_calendar_hour_policy_runs"]:
            segments = r["source_chart_segment_states"]
            if r["hour_Earthly_branch_policy"] == "local_mean_solar_longitude":
                self.assertEqual([x["integer_second_samples"] for x in segments], [60, 541])
                self.assertEqual([x["selected_hour_branch"] for x in segments], ["Wu", "Wei"])
                self.assertEqual(segments[1]["start_UTC_inclusive"], "2026-07-01T17:56:00+00:00")
            else:
                self.assertEqual(len(segments), 1)
                self.assertEqual(segments[0]["selected_hour_branch"], "Wei")

    def test_10_HK_1965_DST_calendrical_day_policy_and_civil_hour_boundary(self):
        case = self.cases["SYNTH_HK_1965_DST_UTC8_MIDNIGHT"]
        self.assertEqual(
            case["distinct_source_calendar_hour_life_full14_states_across_all_seconds_policies"], 3
        )
        self.assertEqual(
            {
                v
                for r in case["four_calendar_hour_policy_runs"]
                for s in r["source_chart_segment_states"]
                for v in s["zone_UTC_offset_seconds_values"]
            },
            {32400},
        )
        self.assertEqual(
            {
                s["selected_hour_branch"]
                for r in case["four_calendar_hour_policy_runs"]
                for s in r["source_chart_segment_states"]
            },
            {"Zi", "Chou"},
        )

    def test_11_NY_fold_treated_as_two_distinct_civil_wall_offset_records(self):
        case = self.cases["SYNTH_NY_2026_DST_FOLD_UTC_INSTANT"]
        self.assertTrue(case["source_all_policy_invariant_14star_state"])
        for r in case["four_calendar_hour_policy_runs"]:
            self.assertEqual(len(r["source_chart_segment_states"]), 1)
            state = r["source_chart_segment_states"][0]
            self.assertEqual(state["zone_fold_values"], [0, 1])
            self.assertEqual(state["zone_UTC_offset_seconds_values"], [-14400, -18000])
            self.assertEqual(state["life_palace_major_stars"], [])
        self.assertFalse(case["robust_behavioral_prediction_from_source"])

    def test_12_HK_2023_leap_mock_hour_variants_no_selected_anchor(self):
        case = self.cases["SYNTH_HK_2023_LEAP_HOUR_BOUNDARY"]
        self.assertFalse(case["source_all_policy_invariant_14star_state"])
        self.assertTrue(case["source_all_policy_invariant_four_anchor_status_only"])
        self.assertEqual(case["distinct_four_candidate_anchor_sets_across_all_seconds_policies"], 1)
        for s in case["all_original_unique_source_state_details"].values():
            self.assertEqual(s["selected_four_provisional_behavior_anchor_stars"], [])
            self.assertFalse(s["human_behavior_p_value_or_probability_available"])

    def test_13_2057_disagreement_fails_entire_interval(self):
        fail = self.d["disputed_original_calendar_interval_rejection"]
        self.assertEqual(fail["case_id"], "SYNTH_2057_DISPUTED_DUAL_LUNAR_CALENDAR")
        self.assertTrue(fail["entire_uncertain_interval_rejected"])
        self.assertEqual(fail["reason_class"], "CalendarParityError")
        self.assertIn("disagree", fail["reason"])
        self.assertTrue(fail["rejected_instead_of_voting_on_calendar_school"])

    def test_14_invalid_UTC_timezone_fractional_second_and_interval_bound_rejected(self):
        # Use the actual *pinned source worker* in an isolated imported module,
        # without starting any natal calculation. The old natal engine is
        # source-SHA verified and never altered or imported as a free chart.
        import importlib.util
        import sys

        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _, files = parent.get_original_source()
            for name, raw in files.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
            source_dir = root / "tasks/astro-chinese-primary-sources-20261017/ziwei"
            sys.path.insert(0, str(source_dir))
            try:
                spec = importlib.util.spec_from_file_location(
                    "source_locked_interval_worker_under_test", WORKER
                )
                self.assertIsNotNone(spec)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.assertEqual(
                    module.datetime_from_UTC("2026-02-16T21:00:00+00:00").isoformat(),
                    "2026-02-16T21:00:00+00:00",
                )
                for bad in (
                    "2026-02-16T21:00:00+01:00",
                    "2026-02-16T21:00:00",
                    "2026-02-16T21:00:00.500000+00:00",
                ):
                    with self.subTest(clock=bad), self.assertRaises(ValueError):
                        module.datetime_from_UTC(bad)
                example = deepcopy(module.CASES[0])
                example["end_UTC"] = "2026-02-16T20:58:59+00:00"
                with self.assertRaisesRegex(ValueError, "outside bounded"):
                    module.summarize_interval(example)
                example = deepcopy(module.CASES[0])
                example["end_UTC"] = "2026-02-16T22:59:01+00:00"
                with self.assertRaisesRegex(ValueError, "outside bounded"):
                    module.summarize_interval(example)
            finally:
                sys.path.pop(0)

    def test_15_original_source_three_calendrical_input_negatives_explicit(self):
        self.assertTrue(self.d["source_true_apparent_solar_and_23h_Zi_day_not_supported"])
        self.assertFalse(self.d["human_birth_zone_from_approximate_location_inferred"])
        self.assertFalse(
            self.outer["real_birth_clock_uncertainty_to_possible_UTC_instants_implemented"]
        )
        self.assertFalse(self.outer["validated_full_ZiWei_natal_chart"])

    def test_16_any_source_predicate_still_ambiguous_not_scholarly_truth(self):
        for case in self.d["case_results"]:
            for row in case["all_original_unique_source_state_details"].values():
                self.assertFalse(row["is_independent_birth_chart_empirical_truth"])
                self.assertFalse(row["human_behavior_p_value_or_probability_available"])
                self.assertEqual(len(row["full_14_major_star_layout_sha256"]), 64)
                self.assertIn(
                    row["original_source_status"],
                    ("original_transcription_only", "qualified_source_variant"),
                )

    def test_17_tampered_prior_engine_manifest_or_hash_throws(self):
        with (
            patch.object(parent, "PARENT_MANIFEST_SHA", "0" * 64),
            self.assertRaisesRegex(ValueError, "parent source"),
        ):
            parent.assert_pinned_original_parent()

    def test_18_tampered_parent_response_counts_cannot_promote_forecast(self):
        d = deepcopy(self.outer)
        d["real_blind_predictive_outcomes"] = 1
        self.assertNotEqual(d, self.outer)
        self.assertEqual(self.outer["real_blind_predictive_outcomes"], 0)
        self.assertEqual(self.d["real_human_predictive_validations"], 0)

    def test_19_parent_sensitivity_helper_undeclared_exceptions_never_silent(self):
        self.assertEqual(self.outer["source_engine_git_commit"], parent.ENGINE_COMMIT)
        self.assertEqual(
            self.outer["pinned_external_calendar_package_versions"],
            {"lunar_python": "1.4.8", "sxtwl": "2.0.7"},
        )
        self.assertFalse(self.outer["original_Ming_printed_source_verified"])

    def test_20_shipped_file_does_not_include_personal_DOB_or_answers(self):
        self.assertEqual(self.outer["actual_human_chart_subjects"], 0)
        self.assertEqual(self.outer["astrological_runtime_rule_promotions"], 0)
        self.assertEqual(self.d["human_personal_birth_records_or_survey_responses"], 0)
        self.assertEqual(self.d["unique_source_calendar_hour_key_count"], 18)
        self.assertEqual(len(self.outer["source_22_original_engine_files_sha256"]), 22)


if __name__ == "__main__":
    unittest.main()
