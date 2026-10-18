"""Original Lilly 1647 eleventh-house friendship source archival tests only."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class OriginalFriendshipIntro(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = read("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.r = read("RULES.json")
        cls.w = read("ORIGINAL_SOURCE_WITNESS.json")
        cls.map = read("SOURCE_TO_RECORD_MAP.json")
        cls.limits = read("UNRESOLVED_SOURCE_LIMITS.json")
        cls.guard = read("FRIENDSHIP_HISTORICAL_TARGET_GUARD_V1.json")
        cls.accept = read("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])
        cls.text = " ".join(x["original_anchor_not_diplomatic"] for x in cls.r["rules"])

    def one(self, *roles):
        for role in roles:
            self.assertEqual(self.roles[role], 1, role)

    def test_01_original_1647_photo_member_SHA_and_bytes(self):
        self.assertEqual(list(self.w["images"]), [str(i) for i in range(668, 673)])
        for v in self.w["images"].values():
            raw = (B / v["file"]).read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), v["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), v["sha256"])

    def test_02_physical_source_continues_top_pdf670_before_printed_CL(self):
        self.assertTrue(self.w["unnumbered"])
        self.assertEqual(self.w["body_original_pdf_frames"], [668, 669, 670])
        self.assertEqual(self.w["next_printed_CL_heading_frame"], 670)
        self.assertEqual(
            [v["printed_folio"] for v in self.w["images"].values()],
            ["634", "635", "636", "637", "638"],
        )

    def test_03_unique_85_source_notes_and_contiguous_ids(self):
        self.assertEqual(
            [x["record_number"] for x in self.r["rules"]],
            list(range(9778, 9863)),
        )
        self.assertEqual(len({x["id"] for x in self.r["rules"]}), 85)

    def test_04_seven_reversible_source_groups_map_every_record(self):
        ids = []
        for s, rev in zip(self.a["groups"], self.map["source_groups"], strict=True):
            self.assertEqual(s["source_span"], rev["source_span"])
            self.assertEqual(s["original_pdf_frames"], rev["original_pdf_frames"])
            source_ids = [x["id"] for x in s["claims"]]
            self.assertEqual(source_ids, rev["mapped_record_ids"])
            ids.extend(source_ids)
        self.assertEqual(ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(self.map["source_group_count"], 7)

    def test_05_friendship_83_substantive_two_CL_navigation(self):
        self.assertEqual(self.r["substantive"], 83)
        self.assertEqual(self.r["following_numbered_navigation"], 2)
        self.assertEqual(
            [x["id"] for x in self.r["rules"] if x["role"] == "next_numbered_navigation"],
            ["R9861", "R9862"],
        )

    def test_06_eleventh_occupants_or_aspects_are_primary(self):
        self.one("occupants_eleventh", "aspects_eleventh")

    def test_07_first_house_is_subsequent_fallback_with_three_natures(self):
        self.one("fallback_first_house", "first_benefic", "first_malefic", "first_indifferent")

    def test_08_lord_eleventh_is_last_not_equal_first_source(self):
        self.one("fallback_lord_eleventh", "aspects_to_lord")

    def test_09_jupiter_venus_good_if_strong_and_appropriately_placed(self):
        self.one(
            "jupiter_venus",
            "fortified",
            "appropriate_places",
            "abundant_friends",
            "profitable_friends",
            "sincere_love",
        )

    def test_10_node_positive_signs_and_opposite_signs_not_same(self):
        self.one("north_node", "north_node_positive_signs", "north_node_other_signs")
        self.assertFalse(self.limits["all_original_lunar_node_glyphs_verified"])

    def test_11_weak_benefics_allow_moderate_expectation_and_mixed_trust(self):
        self.one("benefics_weak", "moderate_friendship", "little_expectation", "partly_sincere")

    def test_12_well_dignified_malefics_can_yield_many_but_mixed_loyalty(self):
        self.one(
            "saturn_mars",
            "malefics_place",
            "malefics_dignified",
            "many_bad_friends",
            "dissemblers",
            "truth_not_cordial",
        )

    def test_13_weak_malefics_shift_to_few_and_unfaithful(self):
        self.one("malefics_weak", "few_friends", "unfaithful")

    def test_14_south_node_relative_to_mars_lilly_exception(self):
        self.one("south_node", "mars_worst")
        self.assertIn("not wholly so bad as Mars", self.text)

    def test_15_peregrine_movable_moral_claim_not_human_validation(self):
        self.one("worst_case", "peregrine_infortune", "mutable_sign", "personal_testimony")

    def test_16_sun_moon_mercury_neutral_qualified_well_bad(self):
        self.one(
            "indifferent_lights",
            "other_glyph_indifferent",
            "neutral_first_eleventh",
            "neutral_well_dignified",
            "neutral_many",
            "neutral_more_faithful",
            "neutral_ill",
            "scarcity",
            "false_mutable",
        )

    def test_17_mixed_planets_true_friend_priority_vs_house_empty(self):
        self.one(
            "many_different_planets",
            "mixture_friends",
            "most_fortified",
            "both_houses_empty",
            "lord_eleventh_strength",
            "friends_nature",
        )

    def test_18_special_six_benefic_houses_vs_malefic_twelfth_angles(self):
        self.one(
            "special_heading",
            "benefics_six_houses",
            "benefic_many",
            "malefic_twelfth",
            "malefic_angles",
            "enemies_many",
        )

    def test_19_cancer_asc_vs_moon_aquarius_pisces_two_outcomes(self):
        self.one("cancer_ascendant", "friends_hard", "moon_aquarius_pisces", "not_accepted_princes")

    def test_20_lord_eleventh_and_lord_tenth_separation_distinct(self):
        self.one(
            "lord_eleventh_separates_asc",
            "few_little_agreement",
            "lord_tenth_retro",
            "prince_dislikes_native",
            "lord_asc_retro",
            "native_dislikes_prince",
        )

    def test_21_saturn_mars_false_vs_sun_powerful_and_venus_gender(self):
        self.one(
            "saturn_eleventh",
            "saturn_false",
            "mars_eleventh",
            "mars_no_faithful",
            "sun_eleventh",
            "powerful_friends",
            "venus_eleventh",
            "women_cause_friends",
        )

    def test_22_mercury_many_vs_moon_known_many_but_few_close(self):
        self.one(
            "mercury_eleventh",
            "mercury_many",
            "moon_eleventh",
            "moon_known_many",
            "moon_few_friends",
        )

    def test_23_separate_eight_nonoperationalized_human_targets(self):
        self.assertEqual(len(self.guard["target_variables"]), 8)
        self.assertTrue(self.guard["no_runtime_model_promotions"])
        self.assertTrue(all(not x["predeclared"] for x in self.guard["target_variables"]))

    def test_24_no_people_moral_trustworthiness_enemies_predictions(self):
        self.assertFalse(
            self.limits["actual_person_trustworthiness_and_moral_classification_authorized"]
        )
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for row in self.r["rules"]:
            for key in (
                "independent_real_friendship_count_validated",
                "independent_real_relationship_reliability_validated",
                "independent_real_support_or_social_influence_validated",
                "independent_actual_enemy_count_validated",
                "actual_source_planet_glyphs_and_calculations_verified",
                "runtime_model_promoted",
            ):
                self.assertFalse(row[key], (row["id"], key))
            self.assertTrue(row["no_real_person_morality_or_faith_label_authorized"])

    def test_25_original_unumbered_no_chapter_increment_and_hashes(self):
        self.assertEqual(self.accept["prior_lilly"], 9777)
        self.assertEqual(self.accept["lilly_if_published"], 9862)
        self.assertEqual(self.accept["combined_if_published"], 10928)
        self.assertEqual(self.accept["numbered_chapters_added"], 0)
        for name, field in [
            ("RULES.json", "rules_sha256"),
            ("SOURCE_FIRST_AUTHORING_20261018.json", "authoring_sha256"),
            ("FRIENDSHIP_HISTORICAL_TARGET_GUARD_V1.json", "friendship_guard_sha256"),
        ]:
            self.assertEqual(
                hashlib.sha256((B / name).read_bytes()).hexdigest(),
                self.accept[field],
            )


if __name__ == "__main__":
    unittest.main()
