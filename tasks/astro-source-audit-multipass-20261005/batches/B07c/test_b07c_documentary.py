"""Lilly original 1647 CXLIX: provenance/qualification tests, not natal accuracy."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class OriginalProfessionAphorisms(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = read("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.r = read("RULES.json")
        cls.w = read("ORIGINAL_SOURCE_WITNESS.json")
        cls.mapping = read("SOURCE_TO_RECORD_MAP.json")
        cls.limits = read("UNRESOLVED_SOURCE_LIMITS.json")
        cls.guard = read("PROFESSION_VALIDATION_REQUIREMENTS_V1.json")
        cls.accepted = read("ACCEPTANCE.json")
        cls.roles = Counter(row["role"] for row in cls.r["rules"])
        cls.original_anchors = " ".join(
            row["original_anchor_not_diplomatic"] for row in cls.r["rules"]
        )

    def one(self, *roles):
        for role in roles:
            self.assertEqual(self.roles[role], 1, role)

    def test_01_first_edition_photo_sha256_and_exact_bytes(self):
        self.assertEqual(list(self.w["images"]), [str(n) for n in range(660, 671)])
        for item in self.w["images"].values():
            raw = (B / item["file"]).read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), item["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), item["sha256"])

    def test_02_source_printed_folios_and_next_unnumbered_seam(self):
        self.assertEqual(self.w["body_pdf_frames"], list(range(660, 669)))
        self.assertEqual(self.w["following_unnumbered_eleventh_heading_frame"], 668)
        self.assertEqual(self.w["following_numbered_CL_heading_frame"], 670)
        self.assertEqual(
            [r["printed_folio"] for r in self.w["images"].values()],
            [str(n) for n in range(626, 637)],
        )

    def test_03_exact_251_source_ids_unique_append_only(self):
        self.assertEqual(
            [r["record_number"] for r in self.r["rules"]],
            list(range(9527, 9778)),
        )
        self.assertEqual(len({r["id"] for r in self.r["rules"]}), 251)

    def test_04_fourteen_source_groups_bidirectional_mapping(self):
        ids = []
        for source, reverse in zip(self.a["groups"], self.mapping["source_groups"], strict=True):
            self.assertEqual(source["source_span"], reverse["source_span"])
            self.assertEqual(
                source["original_pdf_frames"],
                reverse["original_pdf_frames"],
            )
            refs = [x["id"] for x in source["claims"]]
            self.assertEqual(refs, reverse["mapped_record_ids"])
            ids.extend(refs)
        self.assertEqual(ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(self.mapping["source_group_count"], 14)

    def test_05_248_substantive_three_future_navigation(self):
        self.assertEqual(self.r["substantive"], 248)
        self.assertEqual(self.r["following_unnumbered_navigation"], 3)
        self.assertEqual(
            [x["id"] for x in self.r["rules"] if x["role"].startswith("navigation_")],
            ["R9775", "R9776", "R9777"],
        )

    def test_06_single_vs_multiple_occupational_planets(self):
        self.one(
            "single_signifier",
            "venus_single",
            "mercury_single",
            "mars_single",
            "multiple_signifiers",
            "mixed_natures",
        )

    def test_07_mercury_can_yield_to_strong_mars(self):
        self.one("mercury_mars_good", "mars_overrides_mercury", "mars_house_sign")

    def test_08_jupiter_saturn_sun_moon_modify_not_equivalent(self):
        self.one(
            "other_modifiers",
            "jupiter_modifier",
            "saturn_modifier",
            "sun_magistracy",
            "moon_people",
        )

    def test_09_mercury_letters_arithmetic_poetry_and_engineering(self):
        self.one(
            "mercury_heading",
            "mercury_mind",
            "letters",
            "numbers",
            "writing",
            "learning",
            "arithmetick",
            "poetry",
            "engines",
        )

    def test_10_mercury_trade_secretaries_geometry_alternatives(self):
        self.one(
            "eloquence", "philosophy", "merchandize", "grammarian", "secretaries", "geometricians"
        )

    def test_11_mercury_jupiter_good_aspect_affects_profit_distinct(self):
        self.one("jupiter_good_aspect", "mercury_no_profit")

    def test_12_mercury_saturn_good_vs_malefic_aspects_separate(self):
        self.one(
            "mercury_mixes",
            "mercury_saturn_good",
            "mercury_saturn_bad",
            "servile_offices",
            "church_work",
        )
        self.assertEqual(self.roles["mercury_saturn"], 2)

    def test_13_mercury_mars_crafts_vs_occult_stereotype(self):
        self.one("mercury_mars", "husbandmen", "tailor_carver", "dream_interpreter")

    def test_14_mercury_jupiter_law_and_solar_cazimi_exception(self):
        self.one(
            "mercury_jupiter",
            "jupiter_legal",
            "jupiter_occupation",
            "jupiter_banking",
            "mercury_sun",
            "not_retrograde",
            "cazimi_exception",
        )

    def test_15_mercury_moon_astrology_divination_by_signs(self):
        self.one(
            "mercury_moon",
            "futurities",
            "divination",
            "moon_applies_mercury",
            "moon_virgo_scorpio",
            "astrologers",
            "moon_sag_pisces",
            "no_art_divination",
        )

    def test_16_venus_alone_trade_lists_vs_asserted_anti_learning(self):
        self.one(
            "venus_heading",
            "venus_pleasure",
            "venus_learning",
            "venus_saturn_discipline",
            "venus_apothecary",
            "venus_perfume",
            "venus_paint",
            "venus_musicians",
        )

    def test_17_venus_with_saturn_jupiter_dignity_and_cazimi(self):
        self.one(
            "venus_mixed_heading",
            "venus_saturn",
            "venus_saturn_ill",
            "venus_jupiter",
            "venus_jup_divines",
            "venus_sun_combust",
            "venus_cazimi",
            "venus_cazimi_wealth",
        )

    def test_18_mars_alone_manual_fire_and_nocturnal_warfare(self):
        self.one(
            "mars_heading",
            "mars_hard",
            "mars_strength",
            "manual",
            "fire",
            "sun_mars",
            "mars_nocturnal",
        )

    def test_19_mars_alone_strong_moderate_weak_tiers_distinct(self):
        self.one(
            "mars_strong",
            "soldier_captain",
            "mars_mean",
            "metalwork",
            "surgeons",
            "mars_weak",
            "manual_lower",
            "mars_criminal",
        )

    def test_20_mars_saturn_jupiter_sun_moon_alternatives(self):
        self.one(
            "mars_mixes_heading",
            "mars_saturn",
            "saturn_square_opposition",
            "mars_retrograde",
            "mercury_venus_better",
            "mars_jupiter",
            "mars_jupiter_weak",
            "mars_sun",
            "mars_moon",
            "saturn_mars_moon",
        )

    def test_21_mercury_venus_performing_arts_vs_teaching_law(self):
        self.one(
            "mercury_venus_heading",
            "music_venus_mercury",
            "dance",
            "wax_writing",
            "saturn_contact",
            "jupiter_venus_mercury",
            "teaching",
            "ninth_twelv",
            "jupiter_moon_combo",
        )

    def test_22_mercury_mars_technical_vs_criminal_ill_configurations(self):
        self.one(
            "mercury_mars_heading",
            "mercury_mars_well",
            "medicine_mercury_mars",
            "notary",
            "mercury_mars_weak",
            "dice",
            "false_evidence",
            "saturn_mercury_mars",
            "poisons",
            "jupiter_adds_good",
            "jupiter_lawyers",
        )

    def test_23_mars_venus_alternatives_vs_stigmatizing_labels(self):
        self.one(
            "mars_venus_heading",
            "bold_pleasure",
            "cooks_mars_venus",
            "physicians_mars_venus",
            "weak_mars_venus",
            "bawd",
            "saturn_mars_venus",
            "gravemakers",
            "jupiter_mars_venus",
            "pious_teacher",
        )

    def test_24_profession_success_separate_from_profession_type(self):
        self.one(
            "success_heading",
            "significator_strength",
            "essential_dignity",
            "no_malefic_partile",
            "angular",
            "oriental",
            "famous_workman",
            "public_reputation",
        )

    def test_25_weak_occupation_lord_produces_disparaging_claims(self):
        self.one(
            "weak_source",
            "occidental",
            "cadent",
            "malefic_oppressed",
            "botcher",
            "less_prosperity",
            "saturn_affliction",
            "sluggard",
            "mars_affliction",
            "rashness",
            "both_malefics",
        )

    def test_26_signs_movable_fixed_scropio_humane_separate(self):
        self.one(
            "signs_heading",
            "movable_signs",
            "fixed_signs",
            "scorpio_exception",
            "humane_signs",
            "fourfooted",
        )

    def test_27_attributed_albubater_sign_trade_lists_not_correlated(self):
        self.one(
            "albubater_attribution",
            "fire_signs",
            "goldsmith_baking",
            "earth_signs",
            "potters_earth",
            "air_signs",
            "watery_signs",
        )
        self.assertFalse(self.limits["original_albubater_attribution_independently_collated"])

    def test_28_final_quality_source_competing_aspects_and_older_crossref(self):
        self.one(
            "quality_heading",
            "three_significators",
            "configurations_others",
            "prefer_powerful_aspect",
            "two_planets",
            "prior_part1",
        )

    def test_29_final_mars_saturn_jupiter_aspect_contradictions(self):
        self.one(
            "mars_saturn_negative",
            "mars_saturn_lower",
            "jupiter_mars_positive",
            "jupiter_captains",
            "venus_mars_quality",
            "jupiter_mercury_law",
        )

    def test_30_following_eleventh_house_not_in_current_profession(self):
        self.one("navigation_eleventh", "navigation_friend", "navigation_planets")
        self.assertEqual(self.accepted["next_source"], "UNNUMBERED_ELEVENTH_HOUSE_FRIENDS")
        self.assertEqual(self.accepted["next_original_pdf"], 668)
        self.assertEqual(self.accepted["following_printed_chapter"], "CL")

    def test_31_validation_guard_separate_eight_real_person_targets(self):
        self.assertEqual(len(self.guard["separate_targets"]), 8)
        self.assertTrue(self.guard["explicit_nonpromotion"])
        self.assertFalse(self.guard["calibrated_probabilistic_model"])
        self.assertTrue(
            all(not x["currently_operationalized"] for x in self.guard["separate_targets"])
        )

    def test_32_no_criminality_religion_ability_or_job_labels_on_people(self):
        self.assertFalse(
            self.limits["actual_person_crime_morality_religion_or_spiritual_inference_authorized"]
        )
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for r in self.r["rules"]:
            for key in (
                "independent_real_occupation_category_accuracy_validated",
                "independent_real_work_skill_or_income_validated",
                "independent_real_religion_or_occult_ability_validated",
                "independent_real_violence_crime_or_personality_validated",
                "modern_occupation_code_mapping_verified",
                "original_albubater_attribution_crosscollated",
                "person_level_employment_or_danger_prediction_authorized",
                "runtime_model_promoted",
            ):
                self.assertFalse(r[key], (r["id"], key))

    def test_33_expected_corpus_and_rules_provenance_hashes(self):
        self.assertEqual(self.accepted["prior_lilly"], 9526)
        self.assertEqual(self.accepted["lilly_if_published"], 9777)
        self.assertEqual(self.accepted["combined_if_published"], 10843)
        self.assertEqual(self.accepted["new_numbered_chapters"], 1)
        for fname, key in [
            ("RULES.json", "rules_sha256"),
            ("SOURCE_FIRST_AUTHORING_20261018.json", "authoring_sha256"),
            ("PROFESSION_VALIDATION_REQUIREMENTS_V1.json", "scope_guard_sha256"),
        ]:
            self.assertEqual(
                hashlib.sha256((B / fname).read_bytes()).hexdigest(),
                self.accepted[key],
            )


if __name__ == "__main__":
    unittest.main()
