"""Original 1647 unnumbered fifth-house source, NOT medical or natal truth."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class OriginalChildrenIntroduction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = j("RULES.json")
        cls.w = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.m = j("SOURCE_TO_RECORD_MAP.json")
        cls.limits = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.accept = j("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])
        cls.text = " ".join(x["source_anchor_not_diplomatic"] for x in cls.r["rules"])

    def one(self, *names):
        for name in names:
            self.assertEqual(self.roles[name], 1, name)

    def test_01_original_photographs_bytes_sha256(self):
        self.assertEqual(list(self.w["images"]), ["636", "637", "638", "639"])
        for v in self.w["images"].values():
            data = (B / v["path"]).read_bytes()
            self.assertEqual(data[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(data), v["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), v["sha256"])

    def test_02_original_unnumbered_bounds_and_later_numbered_source(self):
        self.assertTrue(self.w["unnumbered"])
        self.assertEqual(self.w["body_pdf_frames"], [636, 637, 638])
        self.assertEqual(self.w["following_printed_CXXXVIII_heading_frame"], 638)
        self.assertEqual(
            [v["printed_folio"] for v in self.w["images"].values()],
            ["602", "603", "604", "605"],
        )

    def test_03_no_numbered_chapter_increment(self):
        self.assertIsNone(self.a["printed_chapter"])
        self.assertEqual(self.accept["new_numbered_chapters"], 0)
        self.assertEqual(self.r["section"], "UNNUMBERED_FIFTH_HOUSE_CHILDREN")

    def test_04_106_append_only_source_ids(self):
        self.assertEqual([r["record_number"] for r in self.r["rules"]], list(range(8497, 8603)))
        self.assertEqual(len(set(r["id"] for r in self.r["rules"])), 106)

    def test_05_all_eight_passages_reversible(self):
        ids = []
        for g, m in zip(self.a["groups"], self.m["source_groups"], strict=True):
            self.assertEqual(g["source_span"], m["source_span"])
            self.assertEqual(g["original_pdf_frames"], m["original_pdf_frames"])
            refs = [c["id"] for c in g["clauses"]]
            self.assertEqual(m["mapped_record_ids"], refs)
            ids.extend(refs)
        self.assertEqual(ids, [r["id"] for r in self.r["rules"]])
        self.assertEqual(self.m["source_groups_count"], 8)

    def test_06_fifth_eleventh_first_priority(self):
        self.one(
            "primary_fifth",
            "secondary_eleventh",
            "third_first",
            "none_planets",
            "fifth_lord",
            "majority_testimonies",
        )

    def test_07_fruitful_cusp_and_planet_conjunction(self):
        self.one(
            "fruitful_planets",
            "prolific_signs",
            "children_promised",
            "barren_cusps",
            "barren_planets",
            "children_absent",
        )

    def test_08_four_source_fecund_indicators_distinct(self):
        self.one("fruitful_jupiter", "fruitful_venus", "fruitful_moon", "fruitful_north_node")

    def test_09_four_source_barren_indicators_distinct(self):
        self.one("barren_saturn", "barren_mars", "barren_sun", "barren_south_node")

    def test_10_mercury_not_fixed_fertile_barren(self):
        self.one(
            "mercury_convertible",
            "mercury_conjunction",
            "mercury_aspect",
            "mercury_dignity",
            "mercury_not_fixed",
        )

    def test_11_positive_fifth_overrules_negative_eleventh(self):
        self.one("fifth_fruitful_eleventh_barren", "fifth_wins_positive")

    def test_12_negative_fifth_overrules_positive_eleventh(self):
        self.one("fifth_barren_eleventh_fruitful", "fifth_wins_negative")

    def test_13_no_planet_fifth_lord_branch_no_issue_vs_few(self):
        self.one(
            "both_houses_empty",
            "fifth_lord_fecund",
            "fifth_lord_child_result",
            "fifth_lord_barren",
            "fewer_or_none",
            "will_they_live_unclear",
        )

    def test_14_sign_category_ternary_and_mixed_indeterminate(self):
        self.one(
            "signs_planets_mix",
            "three_sign_categories",
            "fecund_barren",
            "mediocre_result",
            "barren_fertile",
            "other_signifiers",
            "weight_majority",
        )

    def test_15_same_fecund_fertile_sign_and_fifth(self):
        self.one(
            "fecund_planet_fertile_sign", "especially_fifth", "positive_claim", "barren_barren"
        )

    def test_16_attributed_aphorisms_are_not_independent_validation(self):
        self.one("authors_attribution", "origanus_page")
        self.assertFalse(self.limits["original_named_author_attributions_verified"])

    def test_17_moon_mercury_fifth_ruler_dignity(self):
        self.one("moon_mercury_fifth", "lords_free", "many_children")

    def test_18_mercury_oriental_vs_occidental_aspect(self):
        self.one(
            "mercury_oriental",
            "mercury_good_aspect",
            "mercury_many",
            "mercury_occidental",
            "mercury_infortunes",
            "mercury_barren",
        )

    def test_19_lunar_fifth_with_saturn_modifier_not_character_diagnosis(self):
        self.one("moon_fifth", "saturn_same_fifth", "child_ill_disposition")

    def test_20_fifth_lord_ascendant_all_fruitful(self):
        self.one(
            "fifth_sign_fruitful",
            "fifth_ruler_sign_fruitful",
            "ascending_sign_fruitful",
            "triple_children",
        )

    def test_21_venus_asc_jupiter_seventh_and_trine_moon(self):
        self.one(
            "venus_asc",
            "jupiter_seventh",
            "good_from_children",
            "jupiter_trine_moon",
            "humane_moist_signs",
            "children_by_trine",
        )

    def test_22_angular_lunar_benefics_and_merc_lunar_fifth(self):
        self.one(
            "moon_venus_jupiter_angle",
            "angular_aspect",
            "many_by_angles",
            "mercury_moon_fifth",
            "fruitful_signs_again",
            "well_children",
        )

    def test_23_all_fruitful_signs_all_planets_broad_claim(self):
        self.one("all_planets_fruitful_signs", "abundance")

    def test_24_malefics_fifth_weak_exception_and_child_survival_distinct(self):
        self.one(
            "malefics_children_house",
            "malefics_weak",
            "children_possible",
            "malefics_afflicted",
            "survival_allegation",
            "sterility_allegation",
        )

    def test_25_saturn_venus_original_glpyh_and_mortality_not_medical(self):
        self.one(
            "venus_first_seventh",
            "venus_saturn_hard",
            "mutual_terms",
            "venus_saturn_specific_signs",
            "abortion_claim",
            "early_death_claim",
        )
        self.assertFalse(self.limits["original_glyphs_fully_resolved"])
        self.assertFalse(self.limits["medical_or_child_death_predictions_authorized"])

    def test_26_later_negative_rulership_and_benefic_exemption(self):
        self.one(
            "saturn_fifth_sun_jupiter",
            "denies_issue",
            "three_rulers",
            "unless_benefics",
            "no_planet_house_children",
            "denies_children",
        )

    def test_27_later_child_death_not_count(self):
        self.one("sun_saturn_mercury", "no_children_or_death")

    def test_28_retrograde_combust_fifth_lord_and_author_anecdote(self):
        self.one(
            "fifth_lord_retrograde",
            "fifth_lord_combust",
            "infortune_fifth",
            "author_jupiter_anecdote",
            "healthy_couple_not_enough",
        )

    def test_29_next_numbered_children_count_not_ingested(self):
        self.assertEqual(
            [r["id"] for r in self.r["rules"] if r["role"] == "next_chapter_navigation"],
            ["R8601", "R8602"],
        )
        self.assertEqual(self.r["substantive"], 104)
        self.assertEqual(self.accept["next_printed_chapter"], "CXXXVIII")
        self.assertEqual(self.accept["next_source_pdf"], 638)

    def test_30_all_actual_medical_parent_child_morality_validation_zero(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        self.assertEqual(self.r["real_human_fertility_or_child_outcomes_validated"], 0)
        for r in self.r["rules"]:
            for key in (
                "independent_human_fertility_accuracy_validated",
                "independent_human_child_count_validated",
                "independent_real_child_health_or_death_validated",
                "human_parent_child_morality_claim_authorized",
                "person_level_medical_fertility_advice_authorized",
                "runtime_model_promoted",
            ):
                self.assertFalse(r[key], r["id"])

    def test_31_source_sha_and_cumulative_count(self):
        self.assertEqual(self.accept["prior_lilly"], 8496)
        self.assertEqual(self.accept["lilly_if_published"], 8602)
        self.assertEqual(self.accept["combined_if_published"], 9668)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.accept["rules_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
