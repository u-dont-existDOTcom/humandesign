"""First edition Lilly CLIX Ascendant directions: documentary, not human forecasts."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class OriginalAscendantDirections(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.r = j("RULES.json")
        cls.map = j("SOURCE_TO_RECORD_MAP.json")
        cls.witness = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.star = j("FIXED_STARS_1647_CLIX_ORIGINAL_TABLE_V1.json")
        cls.guard = j("CLIX_HISTORICAL_DIRECTIONS_VALIDATION_GUARD_V1.json")
        cls.limits = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.acc = j("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])

    def once(self, *roles):
        for role in roles:
            self.assertEqual(self.roles[role], 1, role)

    def test_01_all_original_source_photos_sha_bytes(self):
        self.assertEqual(
            list(self.witness["images"]),
            [str(i) for i in range(691, 704)],
        )
        for obj in self.witness["images"].values():
            file = B / obj["file"]
            raw = file.read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), obj["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), obj["sha256"])

    def test_02_source_folio_sequence_and_independent_CLX(self):
        self.assertEqual(
            self.witness["body_original_pdf_frames"],
            list(range(691, 703)),
        )
        self.assertEqual(self.witness["following_printed_CLX_heading_pdf"], 702)
        self.assertEqual(
            [e["printed_folio"] for e in self.witness["images"].values()],
            [str(i) for i in range(657, 670)],
        )

    def test_03_all_335_records_contiguous_unique(self):
        records = self.r["rules"]
        self.assertEqual(len(records), 335)
        self.assertEqual(
            [x["record_number"] for x in records],
            list(range(10733, 11068)),
        )
        self.assertEqual(len({r["id"] for r in records}), 335)
        self.assertEqual(len({r["role"] for r in records}), 335)

    def test_04_seventeen_original_source_groups_reversible(self):
        ids = []
        for authored, mapped in zip(self.a["groups"], self.map["source_groups"], strict=True):
            self.assertEqual(authored["source_span"], mapped["source_span"])
            self.assertEqual(
                authored["original_pdf_frames"],
                mapped["original_pdf_frames"],
            )
            these = [x["id"] for x in authored["claims"]]
            self.assertEqual(these, mapped["mapped_record_ids"])
            ids.extend(these)
        self.assertEqual(ids, [r["id"] for r in self.r["rules"]])
        self.assertEqual(len(self.map["source_groups"]), 17)

    def test_05_previous_Saturn_not_repeated_and_CLIX_opening_Jupiter(self):
        self.once("printed_C LIX", "jupiter_body")
        self.assertEqual(self.r["printed_chapter"], "CLIX")
        self.assertEqual(self.r["following_printed"], "CLX")

    def test_06_three_distinct_physical_Jupiter_aspect_families(self):
        self.once("jupiter_body", "jupiter_sextile_trine", "jupiter_square_oppo", "jupiter_terms")

    def test_07_Jupiter_body_class_and_conditional_health(self):
        self.once(
            "jupiter_marriage_age",
            "jupiter_clergy_benefice",
            "radix_jupiter",
            "jupiter_watery_peregrine",
            "jupiter_airy_measles",
        )

    def test_08_Jupiter_soft_birth_class_trade_vs_king(self):
        self.once("jupiter_king", "jupiter_tradesman", "jupiter_courtier", "class_capacity")

    def test_09_Jupiter_hard_not_all_bad_and_terms_distinct(self):
        self.once(
            "jupiter_square_oppo",
            "jupiter_limited_loss",
            "jupiter_house_causes",
            "jupiter_terms_health",
            "jupiter_terms_esteem",
        )

    def test_10_Mars_body_and_severe_mortality_condition(self):
        self.once("mars_body", "mars_death_cond", "mars_hurt_sign_part", "mars_cancer_scorpio")

    def test_11_Mars_soft_can_benefit_military_but_choler_remains(self):
        self.once("mars_soft", "mars_preferment_arms", "mars_more_spend", "mars_soft_choler")

    def test_12_Mars_hard_mitigating_benefics_and_term_conditions(self):
        self.once(
            "mars_hard",
            "mars_hard_death",
            "mars_benefic_mitigate",
            "mars_terms",
            "mars_terms_dignity",
        )

    def test_13_Mars_sign_taxonomies_fire_earth_air_water(self):
        self.once(
            "mars_fire_sign",
            "mars_earth_sign",
            "mars_air_sign",
            "mars_water_sign",
            "mars_scorpio_water",
        )

    def test_14_Sun_body_vs_soft_vs_hard_separate(self):
        self.once("sun_body", "sun_soft", "sun_hard", "sun_square_vs_oppo", "sun_oppo_imprisonment")

    def test_15_Sun_father_eyes_prince_economy_distinct(self):
        self.once(
            "sun_father_harm", "sun_eye", "sun_class_quality", "sun_hard_losses", "sun_soft_estate"
        )

    def test_16_Venus_body_vs_good_bad_and_terms(self):
        self.once("venus_body", "venus_soft", "venus_hard", "venus_terms")

    def test_17_Venus_marriage_requires_life_stage_and_family_context(self):
        self.once("venus_marriage_cond", "venus_old_suit", "venus_soft_marry", "venus_soft_child")

    def test_18_Venus_health_society_and_trade_different_targets(self):
        self.once(
            "venus_hard_infirm", "venus_hard_urethral", "venus_hard_scandal", "venus_terms_trade"
        )

    def test_19_Mercury_body_soft_hard_terms(self):
        self.once("mercury_body", "mercury_soft", "mercury_hard", "mercury_terms")

    def test_20_Mercury_school_age_occupation_vs_monetary_job(self):
        self.once(
            "mercury_study",
            "mercury_apprentice",
            "mercury_tradesmen",
            "mercury_king_servant",
            "mercury_soft_books",
            "mercury_soft_condition",
        )

    def test_21_Mercury_negative_law_defamation_and_positive_term(self):
        self.once(
            "mercury_lawsuit",
            "mercury_false_witness",
            "mercury_written_libels",
            "mercury_terms_wit",
        )

    def test_22_Moon_radix_weak_body_vs_strong_and_soft(self):
        self.once(
            "moon_body", "moon_weak_radix", "moon_fortunate_radix", "moon_soft", "moon_overseas"
        )

    def test_23_Moon_family_and_life_stage_not_conflated(self):
        self.once(
            "moon_mother_death", "moon_capable_marry", "moon_soft_marry", "moon_soft_daughter"
        )

    def test_24_Moon_hard_is_distinct_from_nodes_and_Fortune(self):
        self.once("moon_hard", "north_node", "south_node", "fortune_part", "fortune_dispositor")

    def test_25_part_Fortune_source_uses_different_planetary_contacts(self):
        self.once(
            "fortune_jup_aspect",
            "fortune_sun_aspect",
            "fortune_venus_aspect",
            "fortune_mercury_aspect",
        )

    def test_26_house_cusp_directions_2_3_4_not_Planet_contact(self):
        self.once("cusp_second", "cusp_third", "cusp_fourth", "cusp_fourth_death")

    def test_27_fixed_star_prediction_needs_other_testimony(self):
        self.once(
            "fixedstar_heading",
            "fixedstar_concurrence",
            "fixedstar_no_epoch",
            "fixedstar_authorities",
        )

    def test_28_sixteen_period_star_entries_not_current_coordinates(self):
        self.assertEqual(len(self.star["entries"]), 16)
        self.assertEqual(
            [x["source_table_row"] for x in self.star["entries"]],
            list(range(1, 17)),
        )
        self.assertFalse(self.star["calculational_parity_verified"])
        self.assertTrue(
            all(
                not s["modern_star_identity_validated"]
                and not s["modern_ephemeris_longitude_parity_validated"]
                for s in self.star["entries"]
            )
        )

    def test_29_source_star_glyphs_and_missing_minutes_not_fabricated(self):
        self.assertTrue(any(x["minute"] is None for x in self.star["entries"]))
        self.assertFalse(self.limits["original_fixed_star_modern_longitude_epoch_parity"])

    def test_30_fixed_star_Arcturus_Leo_ships_girdle_different(self):
        self.once("spear_staff", "arcturus", "tail_lion", "buckler_ship", "girdle_orion")

    def test_31_fixed_star_Lion_Lesser_Dog_contrary_outcomes(self):
        self.once("lion_heart", "lion_honours", "lesser_dog", "dog_rapine")

    def test_32_Crater_Spica_Lion_knee_neck_Hydra(self):
        self.once("crater", "spica", "knee_lion", "neck_lion", "hydra")

    def test_33_Pleiades_Crab_and_two_Aselli_not_one_star(self):
        self.once("cratch_crab", "pleiades", "two_asses")
        aselli = [s for s in self.star["entries"] if s["printed_name"] == "two Asses"]
        self.assertEqual(sorted(x["degree"] for x in aselli), [2, 3])

    def test_34_CLX_is_separate_and_not_merged(self):
        self.assertEqual(
            [r["id"] for r in self.r["rules"] if r["role"].startswith("next_CLX")],
            ["R11065", "R11066", "R11067"],
        )
        self.assertEqual(self.acc["next_printed_chapter"], "CLX")
        self.assertEqual(self.acc["next_original_pdf"], 702)
        self.assertEqual(self.r["substantive"], 332)

    def test_35_high_stakes_medical_danger_morality_never_promoted(self):
        self.assertFalse(
            self.limits["real_person_medical_criminal_religious_or_safety_advice_authorized"]
        )
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for row in self.r["rules"]:
            for key in (
                "independent_real_event_timing_accuracy_validated",
                "independent_health_or_death_prediction_validated",
                "independent_relationship_or_financial_prediction_validated",
                "independent_faith_personality_or_crime_label_validated",
                "original_directions_angle_date_conversion_verified",
                "original_1647_fixed_star_modern_epoch_parity_verified",
                "real_person_health_safety_social_status_advice_authorized",
                "runtime_model_promoted",
            ):
                self.assertFalse(row[key], (row["id"], key))

    def test_36_primary_direction_time_engine_unverified_guard(self):
        self.assertFalse(self.limits["original_primary_directions_time_engine_verified"])
        self.assertEqual(self.guard["runtime_rules_promoted"], 0)
        self.assertFalse(self.guard["primary_directions_arc_time_engine_verified"])
        self.assertEqual(self.guard["independent_human_outcomes_validated"], 0)

    def test_37_original_part_signifier_and_calculation_scope(self):
        self.assertEqual(len(self.guard["predeclared_separate_event_targets"]), 10)
        self.assertTrue(
            all(not x["measured"] for x in self.guard["predeclared_separate_event_targets"])
        )
        self.assertGreaterEqual(
            len(self.guard["requirements_before_any_calculational_application"]), 5
        )

    def test_38_rules_SHA_and_cumulative_source_totals(self):
        self.assertEqual(self.acc["prior_lilly"], 10732)
        self.assertEqual(self.acc["lilly_if_published"], 11067)
        self.assertEqual(self.acc["combined_if_published"], 12133)
        self.assertEqual(self.acc["numbered_chapters_added"], 1)
        for f, k in [
            ("RULES.json", "rules_sha256"),
            ("SOURCE_FIRST_AUTHORING_20261018.json", "authoring_sha256"),
            ("FIXED_STARS_1647_CLIX_ORIGINAL_TABLE_V1.json", "fixed_star_source_table_sha256"),
        ]:
            self.assertEqual(
                hashlib.sha256((B / f).read_bytes()).hexdigest(),
                self.acc[k],
            )


if __name__ == "__main__":
    unittest.main()
