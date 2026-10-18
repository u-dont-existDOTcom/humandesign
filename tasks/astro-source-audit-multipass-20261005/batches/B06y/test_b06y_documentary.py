"""First edition Lilly CXLIIII source integrity: rank, stars and original numbering."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class OriginalDignityStatusSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.r = j("RULES.json")
        cls.stars = j("REGAL_FIXED_STARS_1647_TABLE_V1.json")
        cls.w = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.m = j("SOURCE_TO_RECORD_MAP.json")
        cls.l = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.accept = j("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])
        cls.text = " ".join(x["anchor_not_diplomatic"] for x in cls.r["rules"])

    def one(self, *roles):
        for name in roles:
            self.assertEqual(self.roles[name], 1, name)

    def test_01_original_jpeg_sha256_byte_count_all_pages(self):
        self.assertEqual(list(self.w["images"]), [str(n) for n in range(649, 661)])
        for item in self.w["images"].values():
            data = (B / item["file"]).read_bytes()
            self.assertEqual(data[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(data), item["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), item["sha256"])

    def test_02_original_printed_cxliiii_through_pdf655(self):
        self.assertEqual(self.w["body_original_pdf_frames"], list(range(649, 656)))
        self.assertEqual(self.w["following_printed_CXLVI_heading_frame"], 655)
        self.assertEqual(
            [s["printed_folio"] for s in self.w["images"].values()],
            [str(n) for n in range(615, 627)],
        )

    def test_03_original_printed_CXLV_missing_not_synthetic(self):
        self.assertFalse(self.a["intervening_printed_CXLV_observed"])
        self.assertFalse(self.w["intervening_printed_CXLV_heading_found"])
        self.assertFalse(self.r["original_CXLV_intervening_heading_present"])
        self.assertEqual(self.r["following_printed_chapter"], "CXLVI")
        self.one("skipped_CXLV")

    def test_04_exact_append_only_188_records(self):
        self.assertEqual(
            [row["record_number"] for row in self.r["rules"]],
            list(range(9125, 9313)),
        )
        self.assertEqual(len(set(row["id"] for row in self.r["rules"])), 188)

    def test_05_all_twelve_passages_source_mapped(self):
        ids = []
        for authored, inv in zip(self.a["groups"], self.m["source_groups"], strict=True):
            self.assertEqual(authored["source_span"], inv["source_span"])
            self.assertEqual(authored["original_pdf_frames"], inv["original_pdf_frames"])
            source_ids = [x["id"] for x in authored["clauses"]]
            self.assertEqual(source_ids, inv["mapped_record_ids"])
            ids.extend(source_ids)
        self.assertEqual(ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(self.m["source_group_count"], 12)

    def test_06_186_substantive_plus_two_navigation(self):
        self.assertEqual(self.r["substantive"], 186)
        self.assertEqual(
            [r["id"] for r in self.r["rules"] if r["role"] == "next_navigation"], ["R9310", "R9311"]
        )

    def test_07_domicile_exaltation_reception_alternatives(self):
        self.one(
            "significator_own_house",
            "significator_exaltation",
            "mutual_reception",
            "high_honour",
            "qualified_by_birth",
        )

    def test_08_triplicity_terms_faces_moderate_only(self):
        self.one("triplicity", "terms", "faces", "mediocrity")

    def test_09_peregrine_detriment_fall_and_no_reception(self):
        self.one("peregrine", "detriment", "fall", "without_reception", "little_dignity")

    def test_10_angles_succedent_eighth_or_cadent_interpretations(self):
        self.one(
            "angular",
            "succedent",
            "eighth_exception",
            "angular_promotion",
            "succedent_honor",
            "little_reputation",
        )

    def test_11_first_and_tenth_ruler_alternatives(self):
        self.one("lord_first_tenth")
        self.assertEqual(self.roles["lord_tenth_first"], 2)
        self.one("fame", "relative_capability", "low_birth_estimation")

    def test_12_fixed_stars_within_five_degrees_with_magnitude(self):
        self.one(
            "fixed_star_conjunction",
            "royal_stars",
            "first_second_magnitude",
            "near_ecliptic",
            "great_preferment",
        )

    def test_13_six_fixed_star_entries_verified_source_not_modern(self):
        self.assertEqual(len(self.stars["entries"]), 6)
        self.assertFalse(self.stars["source_conditions"]["source_era_coordinate_epoch_known"])
        self.assertFalse(self.l["historical_fixed_star_table_modern_parity_passed"])
        self.assertTrue(all(not s["modern_identification_verified"] for s in self.stars["entries"]))

    def test_14_named_six_original_fixed_star_positions(self):
        expected = [
            ("Oculus Tauri", 4, 30, "Gemini"),
            ("Hercules", 18, 0, "Cancer"),
            ("Cor Leonis", 24, 30, "Leo"),
            ("Spica Virgo", 18, 30, "Libra"),
            ("Lucida Lancis", 9, 45, "Scorpio"),
            ("Cor Scorpii", 4, 30, "Sagittarius"),
        ]
        self.assertEqual(
            [
                (x["printed_name"], x["degree"], x["minute"], x["zodiac_sign"])
                for x in self.stars["entries"]
            ],
            expected,
        )

    def test_15_benefics_vs_malefics_moderate_tenth(self):
        self.one("benefics_tenth", "malefics_tenth", "moderate_planets", "benefic_honors")

    def test_16_author_warning_single_aphorism_and_identical_birthcharts(self):
        self.one("warn_single_aphorism", "identical_charts", "different_birth_class")
        self.assertIn("Beggars Child Nativity equal Kings", self.text)

    def test_17_beggar_king_social_outcomes_not_equivalent(self):
        self.one(
            "king_direction",
            "beggar_direction",
            "beggar_alms",
            "king_royal_exploit",
            "beggar_respect",
            "happiness_analogy",
        )

    def test_18_luminary_day_night_and_royal_birth_limitation(self):
        self.one(
            "sun_moon_exaltation_degree",
            "diurnal_sun",
            "nocturnal_moon",
            "regal_asc_sign",
            "royal_progeny",
            "authority_nonroyal",
        )

    def test_19_luminary_benefic_support_vs_no_office(self):
        self.one(
            "luminary_culmination",
            "benefics_surround",
            "great_command",
            "without_assistance",
            "royal_favour_no_office",
        )

    def test_20_lights_cadent_and_ancestral_class_cases(self):
        self.one(
            "angle_no_surround",
            "ancestral_status",
            "lights_cadent",
            "common_low_status",
            "neither_light_angle",
            "high_oriental_lords",
        )

    def test_21_five_competing_kingly_configurations_glyph_unresolved(self):
        self.one(
            "kingly_heading",
            "kingly_mc_sun",
            "kingly_second_sun_venus",
            "kingly_third_fire",
            "kingly_fourth_sun",
            "kingly_fifth_planets",
            "kingly_orb_uncertain",
        )
        self.assertFalse(self.l["original_royal_configuration_glyphs_fully_resolved"])

    def test_22_square_can_be_positive_in_royal_composite(self):
        self.one("kingly_third_square")
        self.assertIn("Venus square Jupiter", self.text)

    def test_23_sun_solar_aries_noon_without_support_exception(self):
        self.one("sun_aries_noon", "great_without_others", "sun_fire_mc", "moon_trine_sun")
        self.assertIn("single Aphorisme", self.text)

    def test_24_moon_nocturnal_phase_and_angularity(self):
        self.one(
            "moon_nocturnal_asc",
            "moon_full",
            "moon_taurus_asc",
            "moon_cor_leonis",
            "moon_many_aspects",
        )

    def test_25_moon_spouse_status_social_class_and_sudden_fall(self):
        self.one("even_clown_born", "moon_jupiter_cancer", "sudden_rise", "sudden_fall")

    def test_26_midheaven_jupiter_malefic_reversal_and_sun_inheritance(self):
        self.one(
            "mc_heading",
            "jupiter_tenth_day",
            "saturn_mars_hard",
            "lose_preferment",
            "sun_tenth_exalt",
            "inherit_throne",
        )

    def test_27_ascendant_mars_merit_vs_less_succedent(self):
        self.one(
            "asc_heading",
            "mars_asc_lord_mc",
            "power_cruel",
            "self_exalt",
            "succedent_less",
            "honor_virtue",
        )

    def test_28_stars_have_glory_and_reverse_bad_outcome(self):
        self.one(
            "fixedstars_heading",
            "pleiades_hyades",
            "spica_ecclesiastical",
            "angular_fixed_unsupported",
            "calamity_later",
            "sirius_procyon",
        )

    def test_29_source_mortality_violence_person_moral_labels_off(self):
        self.assertFalse(self.l["personal_morality_crime_or_lifespan_inference_authorized"])
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for row in self.r["rules"]:
            for key in (
                "independent_real_social_rank_accuracy_validated",
                "independent_real_official_career_validated",
                "independent_income_or_peer_reputation_validated",
                "independent_real_life_span_or_person_violence_validated",
                "source_fixed_star_coordinates_independently_verified",
                "real_person_social_class_or_moral_inference_authorized",
                "runtime_model_promoted",
            ):
                self.assertFalse(row[key], (row["id"], key))

    def test_30_expected_count_and_star_table_sha(self):
        self.assertEqual(self.accept["previous_lilly"], 9124)
        self.assertEqual(self.accept["lilly_if_published"], 9312)
        self.assertEqual(self.accept["combined_if_published"], 10378)
        self.assertEqual(self.accept["new_numbered_chapters"], 1)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.accept["rules_sha256"],
        )
        self.assertEqual(
            hashlib.sha256((B / "REGAL_FIXED_STARS_1647_TABLE_V1.json").read_bytes()).hexdigest(),
            self.accept["star_table_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
