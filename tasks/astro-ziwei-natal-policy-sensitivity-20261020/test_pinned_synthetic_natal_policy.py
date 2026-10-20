"""Independently pinned original Chinese source-to-clock policy sensitivity.

Synthetic timestamp/calendar engineering only; no real natal trait evidence.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

import run_pinned_natal_policy_sensitivity as subject

B = Path(__file__).resolve().parent
ROOT = B.parents[1]
FILE = B / "PINNED_ENGINE_SYNTHETIC_NATAL_POLICY_SENSITIVITY_V1.json"
MANIFEST = B / "PINNED_ENGINE_FILE_MANIFEST_V1.json"


class OriginalSourcePinnedNatalPolicy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(FILE.read_text(encoding="utf-8"))
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.worker = cls.data["synthetic_birth_clocks_and_assumption_variants"]
        cls.cases = {c["case_id"]: c for c in cls.worker["cases"]}

    def test_01_exact_accepted_engine_commit_and_22_SHA_files(self):
        self.assertEqual(
            self.manifest["source_engine_parent_commit"],
            "fb6b30b1ca67ff62fecc0c4ea7f3e4d0553640d4",
        )
        self.assertEqual(
            self.data["original_accepted_engine_git_commit"],
            self.manifest["source_engine_parent_commit"],
        )
        self.assertEqual(self.data["exact_original_engine_member_count"], 22)
        self.assertEqual(len(self.manifest["source_engine_original_files_sha_and_bytes"]), 22)
        self.assertEqual(
            self.data["exact_original_engine_file_manifest_sha256"],
            subject.digest(MANIFEST.read_bytes()),
        )
        self.assertTrue(
            all(
                x["sha256"] == self.data["source_engine_pinned_original_file_SHA256"][name]
                for name, x in self.manifest["source_engine_original_files_sha_and_bytes"].items()
            )
        )

    def test_02_calendrical_external_package_versions_and_code_hashes(self):
        self.assertEqual(
            self.data["calendar_optional_library_versions"],
            {"lunar_python": "1.4.8", "sxtwl": "2.0.7"},
        )
        self.assertEqual(
            self.data["calendar_optional_library_installed_tree_sha256"],
            subject.EXPECTED_LIBRARY_TREE_SHA,
        )
        self.assertEqual(
            subject.verify_calendar_packages(subject.DEFAULT_CALENDAR_PACKAGE_SITE),
            self.data["calendar_optional_library_versions"],
        )
        self.assertTrue(self.data["calendar_optional_libraries_external_and_unbundled"])

    def test_03_prior_source_hour_eligibility_and_score_not_reclassified(self):
        self.assertEqual(
            self.data["original_prior_source_hour_sensitivity_audit_SHA256"],
            subject.PREVIOUS_AUDIT_SHA,
        )
        self.assertEqual(subject.digest(subject.PREVIOUS.read_bytes()), subject.PREVIOUS_AUDIT_SHA)
        self.assertEqual(self.data["actual_human_consent_or_birth_data"], 0)
        self.assertEqual(self.data["real_human_forward_reverse_predictive_validations"], 0)

    def test_04_four_synthetic_clocks_twelve_policies_each(self):
        self.assertEqual(self.worker["fictitious_independent_test_clocks"], 4)
        self.assertEqual(len(self.worker["cases"]), 4)
        self.assertEqual(
            {case["case_id"] for case in self.worker["cases"]},
            {
                "SYNTH_WEST_AFRICA_LUNAR_NEW_YEAR",
                "SYNTH_HONG_KONG_LEAP_FIRST_DAY",
                "SYNTH_NEW_YORK_DATE_CROSSING",
                "SYNTH_HONG_KONG_HISTORICAL_DST",
            },
        )
        self.assertEqual(self.worker["distinct_test_policy_variants_per_clock"], 12)
        self.assertEqual(sum(len(c["policy_cases"]) for c in self.worker["cases"]), 48)

    def test_05_hko_historical_original_lunar_source_witness_not_all_claimed(self):
        self.assertEqual(
            self.data["original_HKO_calendar_witness_counts"],
            {"original_HKO_and_pinned_dual_calendar": 30, "dual_calendar_software_only": 18},
        )
        self.assertTrue(
            any(
                r["calendar_witness_quality"] == "DUAL_SOFTWARE_CALENDARS_ONLY_NO_PINNED_HKO_SOURCE"
                for c in self.worker["cases"]
                for r in c["policy_cases"]
            )
        )

    def test_06_dakar_synthetic_cny_four_different_original_major_configurations(self):
        case = self.cases["SYNTH_WEST_AFRICA_LUNAR_NEW_YEAR"]
        self.assertEqual(
            case["source_original_leap_grid_distinct_life_plus_clock_configurations"], 4
        )
        base = [
            p
            for p in case["policy_cases"]
            if p["leap_month_school_policy"] == "transmitted_quan_shu_as_next"
        ]
        self.assertEqual(
            [r["life_palace_major_stars"] for r in base],
            [["JuMen", "TianJi"], ["TaiYin"], ["TianXiang", "WuQu"], ["TaiYang", "TianLiang"]],
        )
        self.assertEqual(
            {r["selected_chinese_calendar_day"] for r in base}, {"2026-02-16", "2026-02-17"}
        )
        self.assertEqual({r["selected_hour_Earthly_Branch"] for r in base}, {"Hai", "Xu"})
        self.assertEqual(case["source_original_leap_grid_distinct_selected_anchor_sets"], 3)

    def test_07_ny_synthetic_civil_vs_UTC8_and_mean_hour(self):
        case = self.cases["SYNTH_NEW_YORK_DATE_CROSSING"]
        self.assertEqual(
            case["source_original_leap_grid_distinct_life_plus_clock_configurations"], 4
        )
        base = [
            r
            for r in case["policy_cases"]
            if r["leap_month_school_policy"] == "transmitted_quan_shu_as_next"
        ]
        self.assertEqual(
            {r["selected_chinese_calendar_day"] for r in base}, {"2026-10-20", "2026-10-21"}
        )
        self.assertEqual({r["selected_hour_Earthly_Branch"] for r in base}, {"Wei", "Wu"})
        self.assertEqual(case["source_original_leap_grid_distinct_selected_anchor_sets"], 1)

    def test_08_hk_2023_leap_alternative_changes_life_palace(self):
        case = self.cases["SYNTH_HONG_KONG_LEAP_FIRST_DAY"]
        self.assertEqual(
            case["source_original_leap_grid_distinct_life_plus_clock_configurations"], 1
        )
        self.assertEqual(case["all_twelve_policy_variants_distinct_major_star_charts"], 2)
        first = case["policy_cases"][:3]
        self.assertEqual(
            [r["leap_month_school_policy"] for r in first],
            [
                "transmitted_quan_shu_as_next",
                "modern_leap_same_month",
                "modern_leap_first_15_same_else_next",
            ],
        )
        self.assertEqual([r["source_principal_life_palace"] for r in first], ["Xu", "You", "You"])
        self.assertTrue(all(r["original_is_leap_month"] for r in first))

    def test_09_1965_hong_kong_DST_fixed_reference_day_differs(self):
        case = self.cases["SYNTH_HONG_KONG_HISTORICAL_DST"]
        self.assertEqual(
            case["source_original_leap_grid_distinct_life_plus_clock_configurations"], 2
        )
        main = [
            r
            for r in case["policy_cases"]
            if r["leap_month_school_policy"] == "transmitted_quan_shu_as_next"
        ]
        self.assertEqual(
            {r["selected_chinese_calendar_day"] for r in main}, {"1965-06-30", "1965-07-01"}
        )
        self.assertEqual(
            {tuple(r["life_palace_major_stars"]) for r in main}, {("TianXiang",), ("TianLiang",)}
        )
        self.assertTrue(all(r["source_principal_life_palace"] == "Wei" for r in main))

    def test_10_all_source_variants_are_partial_engine_not_person_forecast(self):
        for case in self.worker["cases"]:
            self.assertTrue(case["source_clock_is_entirely_fictitious"])
            for row in case["policy_cases"]:
                self.assertFalse(row["is_complete_Zi_Wei_chart"])
                self.assertFalse(row["is_actual_ordinary_human_behavioral_prediction"])
                self.assertEqual(len(row["all_14_principal_star_locations"]), 14)
                self.assertTrue(
                    row["zoneinfo_TZif_SHA256"] is None or len(row["zoneinfo_TZif_SHA256"]) == 64
                )
                self.assertEqual(row["source_14_major_stars_status"], "original_transcription_only")

    def test_11_seven_deliberate_fail_closed_conditions(self):
        failures = self.worker["unsupported_conditions_fail_closed"]
        self.assertEqual(len(failures), 7)
        self.assertTrue(all(r["actual_failed_closed"] for r in failures))
        self.assertEqual(
            {x["case_id"] for x in failures},
            {
                "2057_calendar_conflict",
                "new_york_dst_spring_gap",
                "new_york_dst_fall_fold_missing",
                "birth_time_uncertainty_unresolved",
                "unsupported_23h_Zi_day",
                "unsupported_apparent_solar",
                "unsupported_LiChun_year",
            },
        )
        self.assertTrue(all(not x["real_human_chart_resolved"] for x in failures))
        conflict = next(x for x in failures if x["case_id"] == "2057_calendar_conflict")
        self.assertEqual(conflict["failure_class"], "CalendarParityError")
        self.assertIn("disagree", conflict["failure_message"])

    def test_12_unsupported_clock_precisions_and_ancient_rules_explicit(self):
        self.assertFalse(self.worker["nonzero_clock_uncertainty_supported"])
        self.assertFalse(self.worker["true_apparent_solar_time_supported"])
        self.assertFalse(self.worker["original_11pm_Zi_day_start_supported"])
        self.assertTrue(self.data["source_lunar_calendar_BaZi_LiChun_year_policy_unimplemented"])
        self.assertFalse(self.data["ancient_original_Ming_woodblock_authenticated"])

    def test_13_engine_manifest_bad_commit_rejected(self):
        wrong = deepcopy(self.manifest)
        wrong["source_engine_parent_commit"] = "0" * 40
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "manifest.json"
            f.write_text(json.dumps(wrong, indent=2))
            with (
                patch.object(subject, "MANIFEST", f),
                self.assertRaisesRegex(ValueError, "Git commit/version changed"),
            ):
                subject.verified_sources()

    def test_14_missing_optional_calendar_packages_fails(self):
        with tempfile.TemporaryDirectory() as d, self.assertRaisesRegex(ValueError, "pinned path"):
            subject.verify_calendar_packages(Path(d) / "absent")

    def test_15_wrong_installed_package_binary_hash_rejected(self):
        with (
            patch.dict(subject.EXPECTED_LIBRARY_TREE_SHA, {"sxtwl": "0" * 64}),
            self.assertRaisesRegex(ValueError, "fingerprint changed"),
        ):
            subject.verify_calendar_packages(subject.DEFAULT_CALENDAR_PACKAGE_SITE)

    def test_16_previous_source_hour_audit_sha_tamper_fails(self):
        with (
            patch.object(subject, "PREVIOUS_AUDIT_SHA", "0" * 64),
            self.assertRaisesRegex(ValueError, "provenance SHA"),
        ):
            subject.build()

    def test_17_installed_versions_and_original_hko_calendar_count_not_evidence(self):
        self.assertFalse(self.worker["fourteen_principal_star_engine_complete_natal_horoscope"])
        self.assertEqual(self.worker["empirically_validated_astrology_traits"], 0)
        self.assertEqual(self.worker["actual_human_natal_test_count"], 0)
        self.assertEqual(self.data["production_astrological_rule_promotions"], 0)

    def test_18_synthetic_policy_variants_source_sha_provenance(self):
        engine_files = self.data["source_engine_pinned_original_file_SHA256"]
        self.assertEqual(
            set(engine_files), set(self.manifest["source_engine_original_files_sha_and_bytes"])
        )
        self.assertTrue(any("HKO_10_EXACT_RESPONSE" in p for p in engine_files))
        self.assertTrue(any("SOURCE_ORIGINAL_ZIWEI_VOL2" in p for p in engine_files))
        self.assertTrue(any("explicit_natal_time.py" in p for p in engine_files))


if __name__ == "__main__":
    unittest.main()
