"""Original 1647 Lilly CLVI mortality chapter: document fidelity, NOT death predictions."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class HistoricalCLVIOriginal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.r = j("RULES.json")
        cls.w = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.map = j("SOURCE_TO_RECORD_MAP.json")
        cls.limit = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.guard = j("MORTALITY_HISTORICAL_NONPROMOTION_GUARD_V1.json")
        cls.stars = j("VIOLENT_FIXED_STARS_1647_SOURCE_TABLE_V1.json")
        cls.accept = j("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])
        cls.original_text_anchors = " ".join(
            x["original_anchor_not_diplomatic"] for x in cls.r["rules"]
        )

    def one(self, *roles):
        for role in roles:
            self.assertEqual(self.roles[role], 1, role)

    def test_01_photo_sha256_bytes_all_8_first_edition_witnesses(self):
        self.assertEqual(list(self.w["original_source_images"]), [str(n) for n in range(678, 686)])
        for info in self.w["original_source_images"].values():
            raw = (B / info["file"]).read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), info["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), info["sha256"])

    def test_02_original_printed_page_labels_and_separate_directions_heading(self):
        self.assertEqual(self.w["body_pdf_frames"], list(range(678, 685)))
        self.assertEqual(self.w["next_unnumbered_directions_starts_pdf"], 685)
        self.assertEqual(
            [x["printed_folio"] for x in self.w["original_source_images"].values()],
            [str(n) for n in range(644, 652)],
        )

    def test_03_all_222_records_contiguous_unique_ids(self):
        self.assertEqual(
            [r["record_number"] for r in self.r["rules"]],
            list(range(10247, 10469)),
        )
        self.assertEqual(len({r["id"] for r in self.r["rules"]}), 222)

    def test_04_eleven_reversible_original_page_source_groups(self):
        ids = []
        for group, reverse in zip(self.a["groups"], self.map["source_groups"], strict=True):
            self.assertEqual(group["source_span"], reverse["source_span"])
            self.assertEqual(group["original_pdf_frames"], reverse["original_pdf_frames"])
            src_ids = [x["id"] for x in group["claims"]]
            self.assertEqual(src_ids, reverse["mapped_record_ids"])
            ids.extend(src_ids)
        self.assertEqual(ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(self.map["source_group_count"], 11)

    def test_05_source_heading_and_luminaries_malefics_priority(self):
        self.one(
            "heading",
            "heading_violent",
            "first_sun_moon",
            "second_saturn_mars",
            "third_eighth",
            "fourth_asc_lord",
            "fifth_fixed_stars",
        )

    def test_06_saturn_death_vs_mars_mode_distinct(self):
        self.one("saturn_death_vs_mars_kind", "violent_signs")

    def test_07_historical_six_star_names_and_positions_not_modern_ephemeris(self):
        expected = [
            ("Caput Medusae", 21, "Taurus"),
            ("Oculus Tauri", 4, "Gemini"),
            ("Hercules", 18, "Cancer"),
            ("Right shoulder of Orion", 23, "Gemini"),
            ("Cor Scorpii", 4, "Sagittarius"),
            ("Chele", 9, "Scorpio"),
        ]
        self.assertEqual(
            [(x["original_name"], x["degree"], x["sign"]) for x in self.stars["table"]],
            expected,
        )
        self.assertFalse(self.stars["modern_star_identity_parity_verified"])

    def test_08_both_luminaries_violent_separate_without_mutual_aspect(self):
        self.one("two_luminaries_violent", "different_signs", "no_mutual_aspect")

    def test_09_fixed_star_five_degree_luminary_contact(self):
        self.one("both_fixed_stars", "within_five_degrees", "moon_cor_scorpio_sun_oculus")

    def test_10_one_violent_sign_one_star_requires_malefic_condition(self):
        self.one("one_light_sign_one_star", "infortune_infests")

    def test_11_two_malefics_afflict_both_lights_or_compound_alternative(self):
        self.one("both_lights_afflicted_two", "one_infortune_both", "other_infortune_eighth")

    def test_12_malefic_angular_aspect_and_eighth_house_qualifiers(self):
        self.one(
            "saturn_mars_conj_angle",
            "especially_midheaven",
            "malefic_hard_aspect",
            "one_eighth_power",
        )

    def test_13_eighth_ruler_ascendant_fall_detriment_or_fixed_star(self):
        self.one("lord_eighth_asc", "eighth_in_fall", "eighth_fixed_star", "asc_light_afflict")

    def test_14_first_ruler_and_sect_light_dispositor_compound(self):
        self.one(
            "lord_first_violent", "dispositor_time_light", "lord_first_in_eighth", "nonmalefic_fall"
        )

    def test_15_seventh_moon_star_hard_aspects_and_benefic_override(self):
        self.one("moon_seventh_star", "moon_hard_sun", "BENEFIC_OVERRIDE", "override_effect")
        self.assertIn("fear sudden violent death is taken away", self.original_text_anchors)

    def test_16_afflicting_significator_combined_with_sign_house_manner(self):
        self.one(
            "manner_heading",
            "strongest_afflicter",
            "death_significators",
            "combine_sign",
            "combine_house",
        )

    def test_17_saturn_and_mars_manner_many_alternatives_not_one(self):
        self.one(
            "saturn_water",
            "saturn_building",
            "saturn_poison",
            "mars_fire",
            "mars_guns",
            "mars_horses",
            "mars_fall",
            "mars_strangling",
        )

    def test_18_sign_elements_and_humane_poisonous_distinct(self):
        self.one(
            "fiery_signs",
            "airy_signs",
            "watery_signs",
            "earthy_signs",
            "humane_signs",
            "poisonous_signs",
        )

    def test_19_house_rank_sources_and_multiple_testimonies(self):
        self.one(
            "tenth_magistrate",
            "twelfth_beasts",
            "twelfth_murder",
            "sixth_servants",
            "two_three_concur",
        )

    def test_20_quality_separate_from_violent_death_with_social_class_bias(self):
        self.one(
            "quality_heading",
            "quality_first_violent",
            "quality_second_manners",
            "quality_thief_murder",
            "quality_public_punish",
            "quality_third_condition",
            "princes_common",
        )

    def test_21_original_later_authors_named_but_not_independently_collated(self):
        self.one(
            "ptolemy_quality",
            "ptolemy_sign",
            "ptolemy_house",
            "ptolemy_lights_lords",
            "schoner_cardanus",
            "albubater_haly",
            "origanus",
            "experiential_claim",
        )
        self.assertFalse(
            self.limit["original_Ptolemy_Haly_Albubater_Cardanus_Schoner_cited_sources_collated"]
        )

    def test_22_saturn_watery_moon_with_wine_drowning_distinct(self):
        self.one(
            "saturn_heading",
            "saturn_pisces_moon_virgo",
            "saturn_watery_moon_opposition",
            "saturn_drowning",
            "saturn_drinking",
        )

    def test_23_saturn_7th_12th_8th_source_examples_separate(self):
        self.one(
            "saturn_seventh_opposite_lights",
            "saturn_dungeon",
            "saturn_argos",
            "mercury_saturn_earth",
            "saturn_sun_fixed",
            "saturn_tenth_time_light",
            "saturn_mars_twelfth",
            "saturn_sag_eighth",
        )

    def test_24_saturn_explicit_benefic_mitigation_required(self):
        self.one("BENEFIC_MITIGATES")
        self.assertIn("Benevolent Planet mittigateth", self.original_text_anchors)

    def test_25_Mars_conditional_moon_venus_mercury_and_signs(self):
        self.one(
            "mars_heading",
            "mars_moon_humane",
            "mars_venus_aspects",
            "mars_mercury_humane",
            "mars_medusa_andromeda",
            "mars_scorpio_sag",
            "mars_7_fire",
            "mars_7_feral",
        )

    def test_26_Mars_luminary_configuration_is_absolute_prerequisite(self):
        self.one("MARS_LIGHTS_NECESSARY", "without_lights_invalid")
        self.assertIn("or else the judgement is invalid", self.original_text_anchors)

    def test_27_lord_ascendant_and_eighth_fire_smoke_contrasts(self):
        self.one(
            "asc_lord_heading",
            "lords_asc_eight_opposition",
            "lords_7_8_ninth_earth",
            "saturn_instead",
            "smoke",
            "mars_fixedstar",
        )

    def test_28_fixed_star_old_individual_modes_and_nonfatal_vision_case(self):
        self.one(
            "fixedstars_heading",
            "sun_algol",
            "mars_arcturus_moon_hercules",
            "malefic_oculus_moon_cor",
            "moon_lucida_hydra",
            "pegasus_lyra",
            "pegasus_orion",
            "pleiades_eye",
            "mars_pleiades_saturn_leonis",
        )

    def test_29_fixed_star_angle_and_broad_9th_11th_8th_dispute(self):
        self.one("near_angles", "other_houses_opinion", "drowned_vs_man", "moon_aquarius_star")

    def test_30_no_apparent_violent_rules_natural_death_fallback(self):
        self.one(
            "NATURAL_IF_NONE",
            "natural_death",
            "natural_eighth_planets",
            "multiple_eighth_pick_strong",
            "empty_eighth_lord",
            "diseases_sixth_crossref",
        )

    def test_31_source_principal_significators_precede_all_aphorisms(self):
        self.one(
            "PRINCIPAL_REQUIRED",
            "APHORISMS_ALONE_INVALID",
            "self_verified",
            "artist_interpretation",
        )

    def test_32_explicit_never_positive_about_persons_death_time(self):
        self.one("TIME_GOD", "DONT_BE_POSITIVE", "be_modest", "divine_providence")
        self.assertFalse(self.guard["nonpromotion"]["individual_death_timing_inference_allowed"])

    def test_33_hypothetical_apheta_directions_not_actual_times(self):
        self.one("apheta_hostile", "ill_directs", "climacterical")
        self.assertFalse(self.limit["mortality_scoring_engine_computable"])

    def test_34_directions_is_next_unnumbered_not_source_CLVI(self):
        self.assertEqual(
            [x["id"] for x in self.r["rules"] if x["role"] == "next_section_navigation"],
            ["R10467", "R10468"],
        )
        self.assertEqual(self.accept["next_original_pdf"], 685)
        self.assertEqual(self.accept["next_unnumbered_section"], "THE_EFFECTS_OF_DIRECTIONS")
        self.assertEqual(self.r["substantive"], 220)

    def test_35_real_person_medical_legal_criminality_mortality_accuracy_zero(self):
        self.assertEqual(self.guard["real_human_deaths_predicted_or_validated"], 0)
        self.assertFalse(
            self.limit["person_mortality_medical_crime_or_self_harm_inference_authorized"]
        )
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for x in self.r["rules"]:
            for key in (
                "independent_human_natural_vs_violent_death_validated",
                "independent_human_death_age_or_date_validated",
                "independent_human_cause_of_death_validated",
                "independent_human_injury_violence_or_morality_validated",
                "source_fixed_star_natal_parity_verified",
                "source_other_authors_independently_collated",
                "real_person_medical_criminality_or_mortality_inference_authorized",
                "runtime_model_promoted",
            ):
                self.assertFalse(x[key], (x["id"], key))

    def test_36_source_hashes_and_cumulative_historical_count(self):
        self.assertEqual(self.accept["prior_lilly"], 10246)
        self.assertEqual(self.accept["lilly_if_published"], 10468)
        self.assertEqual(self.accept["combined_if_published"], 11534)
        self.assertEqual(self.accept["new_numbered_chapters"], 1)
        for fname, key in [
            ("RULES.json", "rules_sha256"),
            ("SOURCE_FIRST_AUTHORING_20261018.json", "authoring_sha256"),
            ("VIOLENT_FIXED_STARS_1647_SOURCE_TABLE_V1.json", "star_source_table_sha256"),
            ("MORTALITY_HISTORICAL_NONPROMOTION_GUARD_V1.json", "nonpromotion_guard_sha256"),
        ]:
            self.assertEqual(
                hashlib.sha256((B / fname).read_bytes()).hexdigest(),
                self.accept[key],
            )


if __name__ == "__main__":
    unittest.main()
