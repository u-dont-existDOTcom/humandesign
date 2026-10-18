"""Lilly 1647 original unnumbered Directions: source integrity, not event accuracy."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class OriginalEffectsOfDirections(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = read("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.r = read("RULES.json")
        cls.w = read("ORIGINAL_SOURCE_WITNESS.json")
        cls.m = read("SOURCE_TO_RECORD_MAP.json")
        cls.limits = read("UNRESOLVED_SOURCE_LIMITS.json")
        cls.guard = read("DIRECTIONS_EMPIRICAL_FIREWALL_V1.json")
        cls.accept = read("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])

    def one(self, *roles):
        for name in roles:
            self.assertEqual(self.roles[name], 1, name)

    def test_01_original_jpeg_bytes_SHA256(self):
        self.assertEqual(list(self.w["images"]), [str(x) for x in range(685, 691)])
        for photo in self.w["images"].values():
            raw = (B / photo["file"]).read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), photo["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), photo["sha256"])

    def test_02_original_folio_651_to_656_seams(self):
        self.assertTrue(self.w["unnumbered"])
        self.assertEqual(self.w["body_original_pdf_frames"], [685, 686, 687, 688])
        self.assertEqual(self.w["following_printed_CLVII_heading_pdf"], 688)
        self.assertEqual(self.w["following_printed_CLVIII_heading_pdf"], 690)
        self.assertEqual(
            [x["printed_folio"] for x in self.w["images"].values()],
            ["651", "652", "653", "654", "655", "656"],
        )

    def test_03_exact_127_unique_contiguous_records(self):
        self.assertEqual(
            [r["record_number"] for r in self.r["rules"]],
            list(range(10469, 10596)),
        )
        self.assertEqual(len(set(x["id"] for x in self.r["rules"])), 127)

    def test_04_eight_photographed_groups_reversibly_mapped(self):
        ids = []
        for src, rev in zip(self.a["groups"], self.m["source_groups"], strict=True):
            self.assertEqual(src["source_span"], rev["source_span"])
            self.assertEqual(src["original_pdf_frames"], rev["original_pdf_frames"])
            original_ids = [x["id"] for x in src["claims"]]
            self.assertEqual(original_ids, rev["mapped_record_ids"])
            ids.extend(original_ids)
        self.assertEqual(ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(self.m["source_group_count"], 8)

    def test_05_source_125_substantive_2_navigation(self):
        self.assertEqual(self.r["substantive"], 125)
        self.assertEqual(
            [x["id"] for x in self.r["rules"] if x["role"] == "next_printed_navigation"],
            ["R10594", "R10595"],
        )

    def test_06_original_mathematical_author_names_kept(self):
        self.one(
            "regiomontanus_author",
            "maginus_author",
            "leovitius_author",
            "manginus_author",
            "zobolus_author",
            "argolus_best",
        )

    def test_07_original_historical_table_references_not_verified(self):
        self.one(
            "regio_tables",
            "old_house_tables",
            "old_diurnal_hours",
            "ptolemy_method",
            "origanus_crossref",
            "argolus_crossref",
        )

    def test_08_original_methods_Argolus_historical_opinion_only(self):
        self.one(
            "modern_author_preference", "most_rational", "circle_position", "house_cusp_offset"
        )
        self.assertFalse(self.limits["all_original_technical_sources_cross_collated"])

    def test_09_significator_and_promittor_two_distinct_objects(self):
        self.one(
            "definition_direct", "definition_significator", "definition_promittor", "encounter_when"
        )
        self.assertTrue(self.guard["historical_significator_and_promittor_as_separate_actors"])

    def test_10_separate_office_marriage_travel_wealth_target_ages(self):
        self.one(
            "preferment_year",
            "marriage_when",
            "travel_when",
            "estate_increase",
            "natal_general",
            "natal_life_scope",
        )

    def test_11_four_resolution_levels_unverified(self):
        self.one("directions_years", "directions_months", "directions_weeks", "directions_days")
        self.assertFalse(self.guard["original_timing_unit_mapping_verified"])

    def test_12_author_admits_timing_misses(self):
        self.one("author_timing_misses", "author_divine_excuse")

    def test_13_author_blames_operator_not_model(self):
        self.one("AUTHOR_BLAMES_ARTIST", "lack_rectification", "errant_natal_chart")
        self.assertTrue(
            any(
                "failure-explaining repair" in x["falsifiability"].lower()
                for x in self.guard["critical_original_claims"]
            )
        )
        self.assertFalse(self.guard["full_mathematical_calculator_parity_verified"])

    def test_14_rectification_exactly_two_or_three_degrees(self):
        self.one("two_three_degrees", "human_frailty", "several_years_shift", "mc_degrees_wrong")
        claim = [
            x
            for x in self.guard["critical_original_claims"]
            if x["source_pdf"] == 686 and "2 or 3" in x["claim"]
        ]
        self.assertEqual(len(claim), 1)

    def test_15_mathematical_directions_not_printed_here(self):
        self.one(
            "direction_math_elsewhere",
            "not_task_calculation",
            "give_effects_only",
            "good_bad_hylegiacal",
        )
        self.assertTrue(self.r["author_does_not_supply_complete_direction_math"])

    def test_16_no_rectification_events_in_holdout_tests(self):
        p = " ".join(self.guard["protocol_requirements_before_human_test"])
        self.assertIn("EXCLUDE all of them", p)
        self.assertIn("negative", p)
        self.assertIn("Freeze natal time input", p)

    def test_17_five_step_directive_aspect_initial(self):
        self.one(
            "step1_good_evil", "step1_good_aspects", "step2_good_direction", "step4_bad_direction"
        )

    def test_18_significator_natal_house_intrinsic_vs_accidental(self):
        self.one(
            "step2_significator_nature",
            "step2_accidental_house",
            "step2_persons_matter",
            "significator_vs_promittor",
        )

    def test_19_promittor_cause_vs_outcome_distinction(self):
        self.one("step3_promittor", "step3_intrinsic", "step3_accidental", "step3_meeting_house")

    def test_20_negative_promittor_branch_kept_distinct(self):
        self.one(
            "step4_source_topics",
            "step5_promittor_adverse",
            "step5_people_matter",
            "step5_house_meet",
        )

    def test_21_five_in_prose_ten_in_original_enumeration(self):
        self.one("ten_referents_intro", "five_hylegiacal_ambig")
        self.assertTrue(self.r["author_claims_five_but_enumerates_ten"])
        self.assertFalse(self.limits["authorial_five_vs_ten_number_ambiguity_resolved"])

    def test_22_ascendant_first_life_body_or_health_benefic_vs_malefic(self):
        self.one(
            "asc_first",
            "asc_life_body",
            "asc_complexion",
            "asc_benefic",
            "asc_cheer",
            "asc_malefic",
            "asc_6_12_8_lords",
        )

    def test_23_moon_second_travel_marriage_family_separately(self):
        self.one(
            "moon_second",
            "moon_body",
            "moon_journeys",
            "moon_marriage",
            "moon_wife_women",
            "moon_close_kin",
        )

    def test_24_sun_third_status_father_health_estimation(self):
        self.one(
            "sun_third",
            "sun_health",
            "sun_honour",
            "sun_great_people",
            "sun_father",
            "sun_estimation",
        )

    def test_25_MC_fourth_profession_mother_office(self):
        self.one("mc_fourth", "mc_offices", "mc_rulers", "mc_profession", "mc_mother")

    def test_26_fortuna_fifth_author_explicit_body_rejection(self):
        self.one(
            "fortuna_fifth",
            "fortuna_good_bad",
            "fortuna_body_some",
            "FORTUNA_DISAGREE",
            "fortuna_dispositor",
        )
        self.assertTrue(self.r["source_lilly_disputes_fortuna_body_effect"])

    def test_27_forward_backward_fortuna_but_forward_preferred(self):
        self.one("fortuna_direction_forward", "fortuna_backward", "fortuna_prefers_forward")

    def test_28_saturn_sixth_and_author_lesser_custom(self):
        self.one(
            "saturn_sixth",
            "saturn_ancestors",
            "saturn_inheritances",
            "saturn_buildings",
            "saturn_fruits",
            "saturn_fears",
            "saturn_source_strength",
            "saturn_not_usual",
        )

    def test_29_Jupiter_seventh_wealth_religion_children(self):
        self.one(
            "jupiter_seventh",
            "jupiter_glory",
            "jupiter_riches",
            "jupiter_children",
            "jupiter_religion",
        )

    def test_30_Mars_eighth_war_law_sibling_categories(self):
        self.one("mars_eighth", "mars_animosity", "mars_lawsuits", "mars_brethren")

    def test_31_Venus_ninth_matrimony_goods_women(self):
        self.one("venus_ninth", "venus_marriage", "venus_ornaments", "venus_maids_women")

    def test_32_Mercury_tenth_trade_journey_learning_siblings(self):
        self.one(
            "mercury_tenth",
            "mercury_wit",
            "mercury_trade",
            "mercury_journey",
            "mercury_younger_brother",
            "mercury_scholarship",
        )

    def test_33_original_natal_houses_change_planet_category(self):
        self.one("intrinsic_all", "accidental_all", "no_unique_event")
        self.assertFalse(self.r["source_life_event_prediction_engine_executable"])

    def test_34_printed_CLVII_lifetime_duration_separate(self):
        self.assertEqual(self.accept["next_printed_chapter"], "CLVII")
        self.assertEqual(self.accept["next_original_pdf"], 688)
        self.assertEqual(self.r["following_printed_chapter"], "CLVII")

    def test_35_no_actual_untouched_human_accuracy(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        self.assertEqual(self.guard["independently_tested_real_humans"], 0)
        for row in self.r["rules"]:
            for key in (
                "real_person_timed_event_accuracy_validated",
                "real_person_health_mortality_or_law_accuracy_validated",
                "first_edition_direction_geometry_verified",
                "rectification_and_holdout_independence_demonstrated",
                "correct_direction_promittor_significator_computation_verified",
                "real_person_prediction_or_decision_authorized",
                "runtime_model_promoted",
            ):
                self.assertFalse(row[key], (row["id"], key))

    def test_36_zero_numbered_chapter_delta_and_hashes(self):
        self.assertEqual(self.accept["prior_lilly"], 10468)
        self.assertEqual(self.accept["lilly_if_published"], 10595)
        self.assertEqual(self.accept["combined_if_published"], 11661)
        self.assertEqual(self.accept["numbered_chapters_added"], 0)
        for name, key in (
            ("RULES.json", "rules_sha256"),
            ("SOURCE_FIRST_AUTHORING_20261018.json", "authoring_sha256"),
            ("DIRECTIONS_EMPIRICAL_FIREWALL_V1.json", "firewall_sha256"),
        ):
            self.assertEqual(
                hashlib.sha256((B / name).read_bytes()).hexdigest(),
                self.accept[key],
            )


if __name__ == "__main__":
    unittest.main()
