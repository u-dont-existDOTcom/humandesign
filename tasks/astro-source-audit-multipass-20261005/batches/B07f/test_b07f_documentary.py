"""Original 1647 Lilly CLI: two-chart mutual concord documentary tests only."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class OriginalTwoNatalCharts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = read("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.r = read("RULES.json")
        cls.w = read("ORIGINAL_SOURCE_WITNESS.json")
        cls.m = read("SOURCE_TO_RECORD_MAP.json")
        cls.guard = read("DYAD_HISTORICAL_VALIDATION_GUARD_V1.json")
        cls.limits = read("UNRESOLVED_SOURCE_LIMITS.json")
        cls.acc = read("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])

    def one(self, *roles):
        for role in roles:
            self.assertEqual(self.roles[role], 1, role)

    def test_01_original_first_edition_photo_SHA_bytes(self):
        self.assertEqual(list(self.w["images"]), [str(n) for n in range(671, 676)])
        for info in self.w["images"].values():
            raw = (B / info["file"]).read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), info["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), info["sha256"])

    def test_02_physical_page_seams_twelfth_and_CLIII(self):
        self.assertEqual(self.w["original_body_pdf_frames"], [671, 672, 673])
        self.assertEqual(self.w["next_unnumbered_twelfth_house_pdf"], 673)
        self.assertEqual(self.w["following_printed_CLIII_pdf"], 674)
        self.assertFalse(self.w["original_intervening_CLII_heading_found"])
        self.assertEqual(
            [x["printed_folio"] for x in self.w["images"].values()],
            ["637", "638", "639", "640", "641"],
        )

    def test_03_exact_unique_93_historic_records(self):
        self.assertEqual(
            [x["record_number"] for x in self.r["rules"]],
            list(range(9927, 10020)),
        )
        self.assertEqual(len({x["id"] for x in self.r["rules"]}), 93)

    def test_04_reversible_eight_source_groups(self):
        ids = []
        for a, m in zip(self.a["groups"], self.m["source_groups"], strict=True):
            self.assertEqual(a["source_span"], m["source_span"])
            self.assertEqual(a["original_pdf_frames"], m["original_pdf_frames"])
            subset = [x["id"] for x in a["claims"]]
            self.assertEqual(subset, m["mapped_record_ids"])
            ids.extend(subset)
        self.assertEqual(ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(self.m["source_group_count"], 8)

    def test_05_both_independent_natals_mandatory_not_one_chart(self):
        self.one(
            "heading",
            "two_nativities",
            "compare_asc1",
            "compare_asc_occupants",
            "compare_asc_lords",
        )
        self.assertEqual(len(self.guard["input_requirements"]), 4)

    def test_06_concord_discord_temperament_vs_unobserved_manners(self):
        self.one(
            "agreement_dissent", "temperament_concord", "temperament_strife", "asc_gov_temperament"
        )

    def test_07_same_asc_sign_and_ruler_vs_dignity_receptions(self):
        self.one("two_horoscope_signs", "same_ruler", "receptions_dignity", "good_aspects")

    def test_08_same_rising_planet_affinity_vs_different_asc_planets(self):
        self.one(
            "same_planet_asc",
            "same_manners",
            "different_asc_planets",
            "natural_planet_friends",
            "natural_friendship",
            "natural_hatred",
        )

    def test_09_Saturn_friend_enemy_lists_asymmetric(self):
        self.one("natural_table", "saturn_enemies", "saturn_venus_vs_mars", "saturn_venus_nature")

    def test_10_Jupiter_Mars_Venus_friendship_can_be_one_way(self):
        self.one(
            "jupiter_enemy_mars",
            "mars_only_venus_friend",
            "venus_not_reciprocate",
            "hot_dry_moist",
            "venus_softens",
        )
        self.assertTrue(any("Mars calls Venus" in x for x in self.guard["asymmetry_to_preserve"]))

    def test_11_Sun_Venus_Mercury_Moon_independent_friend_lists(self):
        self.one("sun_friends", "venus_saturn_enemy", "mercury_friends", "moon_friends")

    def test_12_nodes_treatment_not_fully_legible(self):
        self.one("nodes_friends", "nodes_enemies")
        self.assertFalse(self.limits["original_planet_friendship_glyphs_fully_verified"])

    def test_13_four_lord_ascendant_concord_routes_not_universal(self):
        self.one(
            "four_modes_heading",
            "mode1_same_lord",
            "mode2_reception",
            "mode3_conjunction",
            "mode4_sextile",
            "mode4_trine",
            "four_modes_no_match",
            "friendship_not_last",
        )

    def test_14_fortunes_lights_planet_swaps_different_confidence(self):
        self.one(
            "fortunes_swap", "venus_moon_swap", "sure_friends", "sun_moon_mercury_swap", "less_firm"
        )

    def test_15_planet_swaps_cannot_infer_wicked_or_greedy_motive(self):
        self.one(
            "saturn_jupiter_venus_mars_swap",
            "dissent_mixed_friendship",
            "jupiter_saturn_swap",
            "for_covetousness",
            "mars_venus_swap",
            "for_wickedness",
        )

    def test_16_oppositions_infortune_strength_not_real_physical_harm(self):
        self.one(
            "sun_mars_opposition",
            "injury_conflict",
            "infortune_dominion",
            "saturn_mars_opposite",
            "perpetual_enmity",
        )

    def test_17_opposing_malefics_money_rivalry_vs_infortune_friend(self):
        self.one(
            "infortunes_opposition",
            "mutual_lucre",
            "advocates_merchants",
            "infortunes_agree",
            "friends_ill_action",
            "not_faithful",
        )

    def test_18_Sun_Jupiter_Venus_Moon_ascribed_distinct_motives(self):
        self.one(
            "sun_place_other", "sun_friend_honesty", "jupiter_place", "venus_place", "moon_place"
        )

    def test_19_best_friendship_several_same_sign_paths(self):
        self.one(
            "best_heading",
            "sun_one_same_sign",
            "moon_one_same_sign",
            "fortune_one_same_sign",
            "asc_lord_one_same_sign",
            "best_friendship_claim",
        )

    def test_20_asymmetrical_most_sincere_friend_source(self):
        self.one(
            "sincerity_heading",
            "benign_lord",
            "benign_asc_occupant",
            "sinister_sextile",
            "sinister_trine",
            "hate_malefic_lord",
            "hate_malefic_asc",
        )

    def test_21_negative_ascendant_house_hard_cases_all_distinct(self):
        self.one(
            "never_agree_heading", "asc_in_12th", "asc_in_6th", "asc_in_8th", "never_agree_result"
        )

    def test_22_next_unnumbered_enemies_not_in_relationship_source(self):
        self.assertEqual(
            [
                r["id"]
                for r in self.r["rules"]
                if r["role"] in ("next_unnumbered_navigation", "later_numbered_navigation")
            ],
            ["R10016", "R10017", "R10018", "R10019"],
        )
        self.assertEqual(self.acc["next_source"], "UNNUMBERED_TWELFTH_HOUSE_ENEMIES")
        self.assertEqual(self.acc["next_original_pdf"], 673)

    def test_23_printed_CLI_to_CLIII_skip_preserved_no_fake_CLII(self):
        self.assertFalse(self.a["printed_CLII_heading_observed"])
        self.assertFalse(self.limits["original_CLII_printed_heading_found"])
        self.assertEqual(self.acc["later_printed_chapter"], "CLIII")
        self.assertEqual(self.acc["later_printed_pdf"], 674)

    def test_24_targets_affinity_conflict_duration_direction_separate(self):
        self.assertEqual(len(self.guard["independent_future_targets"]), 7)
        self.assertTrue(any(x["directional"] for x in self.guard["independent_future_targets"]))
        self.assertTrue(all(not x["measured"] for x in self.guard["independent_future_targets"]))

    def test_25_zero_validated_real_dyad_safety_morality(self):
        self.assertFalse(
            self.limits["real_person_relationship_risk_or_moral_inferences_authorized"]
        )
        self.assertFalse(self.limits["pairwise_affinity_scoring_engine_executable"])
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for row in self.r["rules"]:
            for key in (
                "independent_real_mutual_affinity_validated",
                "independent_real_relationship_duration_validated",
                "independent_real_conflict_or_aggression_validated",
                "independent_real_asymmetric_affection_validated",
                "original_pairwise_chart_geometry_verified",
                "real_person_relationship_ethics_or_safety_claim_authorized",
                "runtime_model_promoted",
            ):
                self.assertFalse(row[key], (row["id"], key))

    def test_26_hashes_and_corpus_total(self):
        self.assertEqual(self.r["substantive"], 89)
        self.assertEqual(self.acc["previous_lilly"], 9926)
        self.assertEqual(self.acc["lilly_if_published"], 10019)
        self.assertEqual(self.acc["combined_if_published"], 11085)
        self.assertEqual(self.acc["numbered_chapters_added"], 1)
        for name, key in [
            ("RULES.json", "rules_sha256"),
            ("SOURCE_FIRST_AUTHORING_20261018.json", "authoring_sha256"),
            ("DYAD_HISTORICAL_VALIDATION_GUARD_V1.json", "dyad_guard_sha256"),
        ]:
            self.assertEqual(
                hashlib.sha256((B / name).read_bytes()).hexdigest(),
                self.acc[key],
            )


if __name__ == "__main__":
    unittest.main()
