"""C33 source sign-branch and feasible synthetic date-only classification."""
from datetime import UTC,datetime,timedelta
from decimal import Decimal
import importlib.util
import json
from pathlib import Path
import unittest

from hellenistic_c33_ptolemy_marriage_count import (
    BICORPOREAL,SIGNS, SOURCE_BRANCH_BODY,
    sign_at,sign_only_source_subrule,continuous_sign_enclosure,
    synthetic_body_from_verified_provider,
)
from hellenistic_c33_feasibility_synthetic import (
    SCENARIOS,feasibility_scenarios,required_n_two_group_unadjusted
)

HERE=Path(__file__).resolve().parent
REG=HERE/"HELLENISTIC_C33_MARRIAGE_RULE_AND_FEASIBILITY_V1.json"
SAMPLE=HERE/"HELLENISTIC_C33_UTC_2020_SYNTHETIC_CLASSIFIER_V1.json"
POWER=HERE/"HELLENISTIC_C33_HYPOTHETICAL_POWER_V1.json"
HAS_SWISS=importlib.util.find_spec("swisseph") is not None


class TestC33HistoricalMarriageOutcome(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry=json.loads(REG.read_text(encoding="utf8"))
        cls.sample=json.loads(SAMPLE.read_text(encoding="utf8"))
        cls.power=json.loads(POWER.read_text(encoding="utf8"))

    def test_direct_Greek_passage_attribution_no_modern_ingress(self):
        x=self.registry["source"]
        self.assertIn("Boll",x["edition"])
        self.assertIn("4.5",x["original_greek_url"])
        self.assertEqual(x["greek_full_modern_Eulogikon_markdown_sha256"],
            "7d337a6314d3a68cca0bd310355e4737b393180e1b287415ee6eddfe34b9f630")
        self.assertTrue(x["unimplemented_source_families"])
        self.assertFalse(x["source_photo_critical_manuscript_checked"])

    def test_bicorporeal_set_exactly_Ptolemy_I_11(self):
        self.assertEqual(BICORPOREAL,{"Gemini","Virgo","Sagittarius","Pisces"})
        self.assertEqual(set(BICORPOREAL),set(self.registry["source"]["sign_set_from_Ptolemy_I_11"]))
        self.assertEqual(len(SIGNS),12)
        self.assertEqual(set(SOURCE_BRANCH_BODY),{"men_moon","women_sun"})

    def test_exact_zodiac_boundaries_and_finite_requirement(self):
        positions=[
            (0,"Aries"),(29.999,"Aries"),(30,"Taurus"),
            (59.999,"Taurus"),(60,"Gemini"),(89.999,"Gemini"),
            (90,"Cancer"),(150,"Virgo"),(240,"Sagittarius"),
            (330,"Pisces"),(359.99999,"Pisces"),
        ]
        for longitude,expected in positions:
            with self.subTest(longitude=longitude):
                self.assertEqual(sign_at(longitude),expected)
        for bad in (360,-0.01,True,None,"nan","inf",object()):
            with self.subTest(bad=repr(bad)),self.assertRaises(ValueError):
                sign_at(bad)

    def test_positive_subrule_is_one_way_never_negated(self):
        x=sign_only_source_subrule(historical_branch="men_moon",longitude=65)
        self.assertTrue(x["bicorporeal_positive_condition"])
        self.assertEqual(x["source_outcome_if_positive"],
                         "TWO_OR_MORE_LAWFUL_MARRIAGES")
        y=sign_only_source_subrule(historical_branch="men_moon",longitude=45)
        self.assertFalse(y["bicorporeal_positive_condition"])
        self.assertEqual(y["source_outcome_if_positive"],
                         "NO_CLAIM_FROM_BICORPOREAL_SUBRULE")
        self.assertTrue(y["negative_condition_does_not_predict_one_marriage"])
        self.assertTrue(x["other_source_clauses_may_conflict"])

    def test_genders_in_ancient_text_different_luminaries_not_inferred(self):
        m=sign_only_source_subrule(historical_branch="men_moon",longitude=150)
        f=sign_only_source_subrule(historical_branch="women_sun",longitude=150)
        self.assertEqual((m["natal_body"],f["natal_body"]),("moon","sun"))
        for branch in ("unknown","",None):
            with self.assertRaises(ValueError):
                sign_only_source_subrule(historical_branch=branch,longitude=60)

    def test_same_positive_sign_full_interval_conditional_only(self):
        r=continuous_sign_enclosure(center_longitude=75,max_absolute_motion_deg=14)
        self.assertEqual(r["possible_signs"],["Gemini"])
        self.assertEqual(r["possible_bicorporeal_values"],[True])
        self.assertTrue(r["condition_stable_if_envelope_is_valid"])
        self.assertFalse(r["eligible_for_untouched_human_predictions"])
        self.assertFalse(r["continuous_speed_bound_independently_certified"])

    def test_sign_crossing_must_abstain_even_if_center_positive(self):
        r=continuous_sign_enclosure(center_longitude=60.1,max_absolute_motion_deg=0.2)
        self.assertEqual(r["possible_signs"],["Gemini","Taurus"])
        self.assertEqual(r["possible_bicorporeal_values"],[False,True])
        self.assertFalse(r["condition_stable_if_envelope_is_valid"])
        c=continuous_sign_enclosure(center_longitude=359,max_absolute_motion_deg=2)
        self.assertEqual(c["possible_signs"],["Aries","Pisces"])
        self.assertEqual(c["possible_bicorporeal_values"],[False,True])

    def test_positive_at_boundary_remains_unresolved_if_interval_crosses(self):
        r=continuous_sign_enclosure(center_longitude=75,max_absolute_motion_deg=15)
        self.assertEqual(r["possible_signs"],["Cancer","Gemini"])
        self.assertEqual(r["possible_bicorporeal_values"],[False,True])
        self.assertFalse(r["strictly_same_sign_if_envelope_is_valid"])

    def test_too_wide_interval_all_signs_and_invalid_rejected(self):
        self.assertEqual(len(continuous_sign_enclosure(
            center_longitude=75,max_absolute_motion_deg=180)["possible_signs"]),12)
        for k in (
            {"center_longitude":-1,"max_absolute_motion_deg":0},
            {"center_longitude":360,"max_absolute_motion_deg":0},
            {"center_longitude":60,"max_absolute_motion_deg":-1},
            {"center_longitude":60,"max_absolute_motion_deg":"NaN"}
        ):
            with self.subTest(k=k),self.assertRaises(ValueError):
                continuous_sign_enclosure(**k)

    def test_mock_strict_provider_substitution_rejected(self):
        with self.assertRaises(ValueError):
            synthetic_body_from_verified_provider(
                object(),
                time_start=datetime(2020,1,1,tzinfo=UTC),
                time_end=datetime(2020,1,2,tzinfo=UTC),
                historical_branch="men_moon")

    def test_every_utc_day_2020_calendar_count_and_no_person_data(self):
        s=self.sample
        self.assertEqual(s["sampled_days"],366)
        self.assertEqual(len(s["rows"]),366)
        self.assertEqual(s["source_bicorporeal_positive_windows"],55)
        self.assertEqual(s["source_bicorporeal_negative_windows"],186)
        self.assertEqual(s["unresolved_sign_boundary_windows"],125)
        self.assertEqual(55+186+125,366)
        self.assertTrue(s["no_real_births_or_outcomes"])
        self.assertFalse(s["actual_speed_enclosure_for_full_historical_range_independently_proved"])
        self.assertTrue(s["no_legal_marriage_predictions_frozen"])

    def test_source_hashes_real_ephemeris_provenance_not_fabricated(self):
        for row in self.sample["rows"]:
            h=dict(row["ephemeris_file_hashes"])
            self.assertEqual(h, {
                "sepl_18.se1":"ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66",
                "semo_18.se1":"1ca07bd67c24374d77226180c20a4f9996cba013697894810518e7eb582ca4f7"})
            self.assertIn(row["source_class"],(
                "MANY_INDICATED_CONDITIONALLY",
                "NO_INDICATION_CONDITIONALLY",
                "TIME_INDETERMINATE"))

    def test_hypothetical_power_is_not_measured_achieved_effect(self):
        x=self.power
        self.assertEqual(x,feasibility_scenarios())
        self.assertTrue(x["not_a_real_study_sample_size_commitment"])
        self.assertEqual(x["human_predictions_tested"],0)
        self.assertTrue(x["ignores_ascertainment_bias_clustering_and_birth_data_exclusion"])
        self.assertEqual([r["estimated_total_N_unadjusted"] for r in x["scenario_rows"]],
                         [4975,5513,548,2435])

    def test_invalid_power_assumptions_fail_closed(self):
        for kwargs in [
            {"p0":.2,"p1":.2},
            {"p0":.25,"p1":.2},
            {"p0":.2,"p1":1},
            {"p0":.1,"p1":.2,"exposed_fraction":0},
        ]:
            with self.assertRaises(ValueError):
                required_n_two_group_unadjusted(**kwargs)

    def test_feasibility_preference_not_validation_or_production(self):
        x=self.registry
        self.assertEqual(x["owner_goal"]["status"],"OPEN")
        self.assertEqual(x["owner_goal"]["unvalidated_human_count"],0)
        self.assertEqual(x["owner_goal"]["production_scorer_changes"],0)
        self.assertFalse(x["outcome_human_study_DRAFT"]["enrollment_started"])
        self.assertFalse(x["outcome_human_study_DRAFT"]["consent_approvals_received"])
        self.assertTrue(x["practical_feasibility"]["veteran_deployment_not_inferred_from_discharge_file"])


class TestC33StudyDraft(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study=json.loads((HERE/"HELLENISTIC_C33_BLINDED_MARRIAGE_COUNT_STUDY_DRAFT_V1.json").read_text(encoding="utf8"))

    def test_unregistered_not_automatically_authorized_human_study(self):
        x=self.study
        self.assertEqual(x["state"],"DEVELOPMENT_DESIGN_ONLY_NOT_REGISTERED_NOT_STARTED")
        self.assertEqual(x["execution_status"]["current_parent_goal"],"OPEN")
        for key in ("actual_cohort_consented","questions_administered",
                    "predictions_frozen_for_real_people","response_records_loaded",
                    "blinded_human_performance_observed","source_rule_production_promoted"):
            self.assertFalse(x["execution_status"][key],key)

    def test_no_source_gender_extrapolation_or_seasonal_claim(self):
        x=self.study
        self.assertTrue(x["no_sun_month_natal_increment_claim"])
        self.assertTrue(x["source_uses_nonpositive_as_control_not_a_literal_one_marriage_prediction"])
        self.assertTrue(x["modern_primary_outcome"]["cutoff_is_analyst_choice_not_in_Greek"])
        self.assertTrue(x["modern_primary_outcome"]["include_never_married_in_denominator"])
        self.assertTrue(x["modern_primary_outcome"]["do_not_condition_enrollment_on_ever_married"])

    def test_post_dateonly_filter_can_change_exposure_fraction(self):
        p0=0.15;p1=0.25
        self.assertEqual(required_n_two_group_unadjusted(
            p0=p0,p1=p1,exposed_fraction=55/241),677)
        self.assertEqual(required_n_two_group_unadjusted(
            p0=0.2,p1=0.25,exposed_fraction=55/241),3049)
        self.assertEqual(self.study["sample_feasibility"]
                         ["synthetic_date_window_positive_among_resolved_fraction"],
                         "55/241 (not expected true-cohort exposure proportion)")


if __name__=="__main__":
    unittest.main()
