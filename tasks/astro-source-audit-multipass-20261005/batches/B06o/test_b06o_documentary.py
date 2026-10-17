"""Historical women-marriage original Lilly source integrity, not prediction."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class FirstEditionWomensMarriageSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = j("RULES.json")
        cls.w = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.m = j("SOURCE_TO_RECORD_MAP.json")
        cls.l = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.accept = j("ACCEPTANCE.json")
        cls.roles = Counter(row["role"] for row in cls.r["rules"])
        cls.anchors = " ".join(row["original_anchor_not_diplomatic"] for row in cls.r["rules"])

    def check_unique(self, *roles):
        for role in roles:
            self.assertEqual(self.roles[role], 1, role)

    def test_01_original_1647_photograph_sha_and_bytes(self):
        self.assertEqual(list(self.w["images"]), [str(n) for n in range(634, 639)])
        for v in self.w["images"].values():
            raw = (B / v["file"]).read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), v["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), v["sha256"])

    def test_02_physical_source_boundaries(self):
        self.assertEqual(self.w["body_original_pdf_frames"], [634, 635, 636])
        self.assertEqual(self.w["following_unnumbered_fifth_house_start_frame"], 636)
        self.assertEqual(self.w["following_printed_CXXXVIII_heading_frame"], 638)
        self.assertEqual(
            [r["printed_folio"] for r in self.w["images"].values()],
            [str(x) for x in range(600, 605)],
        )

    def test_03_first_edition_printed_cxxxvii_not_children_cxxxviii(self):
        self.assertEqual(self.a["printed_chapter"], "CXXXVII")
        self.assertEqual(self.a["editorial_chapter"], "CXXXVIII")
        self.assertEqual(self.a["following_section"], "UNNUMBERED_FIFTH_HOUSE_CHILDREN")
        self.assertEqual(self.accept["new_numbered_chapters"], 1)

    def test_04_99_append_only_exact_ids(self):
        self.assertEqual(
            [r["record_number"] for r in self.r["rules"]],
            list(range(8398, 8497)),
        )
        self.assertEqual(len(set(r["id"] for r in self.r["rules"])), 99)

    def test_05_seven_groups_reverse_mapping(self):
        ids = []
        for a, b in zip(self.a["groups"], self.m["source_groups"], strict=True):
            self.assertEqual(a["source_span"], b["source_span"])
            self.assertEqual(a["original_pdf_frames"], b["original_pdf_frames"])
            refs = [v["id"] for v in a["clauses"]]
            self.assertEqual(refs, b["mapped_record_ids"])
            ids.extend(refs)
        self.assertEqual(ids, [r["id"] for r in self.r["rules"]])
        self.assertEqual(self.m["source_group_count"], 7)

    def test_06_female_primary_sun_mars_not_male_venus_moon(self):
        self.check_unique(
            "female_sun",
            "female_mars",
            "replace_moon_with_sun",
            "replace_venus_with_mars",
            "male_transfer",
        )

    def test_07_houses_lord_planets_separate(self):
        self.check_unique(
            "seventh_house",
            "seventh_lord",
            "seventh_occupants",
            "sign_fertile_barren",
            "fortunes_strength",
        )

    def test_08_positive_marriage_composite(self):
        self.check_unique(
            "fruitful_primary", "positive_strength", "positive_benefics", "marriage_result"
        )

    def test_09_negative_marriage_composite(self):
        self.check_unique(
            "negative_barren",
            "negative_houses",
            "negative_weak",
            "negative_malefics",
            "no_marriage",
        )

    def test_10_venus_seventh_and_saturn_fourth_not_global_substitution(self):
        self.check_unique("venus_seventh", "saturn_fourth", "low_desire", "sex_desire")

    def test_11_sun_moon_masculine_not_sun_mars(self):
        self.check_unique(
            "sun_moon_masculine",
            "same_masculine_quarter",
            "same_masculine_sign",
            "historical_virgo",
            "historical_refractory",
        )
        self.assertIn("Sun and Moon in masculine Signes", self.anchors)

    def test_12_ease_good_aspects_or_intrinsic_fortune(self):
        self.check_unique(
            "ease_heading", "applying_good", "fortune_self", "ease_outcome", "contrary_ease"
        )

    def test_13_timing_distinguishes_mid_heaven_sun_and_quarters(self):
        self.check_unique(
            "time_heading",
            "special_mc",
            "special_sun",
            "general_sun",
            "oriental_quarter",
            "occidental_quarter",
        )

    def test_14_timing_alternatives_wedding_age_vs_husband_age(self):
        self.check_unique(
            "young_marriage",
            "young_any_age_husband",
            "mature_young_man",
            "later_marriage",
            "later_older_husband",
        )

    def test_15_husband_number_form_or_matutine(self):
        self.check_unique(
            "husbands_heading",
            "sun_one_form",
            "one_matutine",
            "one_husband",
            "sun_many_shapes",
            "many_matutine",
            "many_husbands",
        )

    def test_16_common_signs_and_venus_in_women_counting(self):
        self.check_unique(
            "three_common",
            "two_husbands",
            "sun_mars_bicorporeal",
            "venus_common",
            "venus_dispositor",
            "more_husbands",
        )

    def test_17_sun_same_sign_corporal_and_partile_platick(self):
        self.check_unique("sun_corporal", "aspect_partile_platick", "corp_count")

    def test_18_sun_dignity_application_fallback_direction(self):
        self.check_unique(
            "sun_not_joined",
            "sign_dignity_planets",
            "sun_beholds",
            "sun_applying",
            "count_from_dignity",
        )
        self.assertIn("not they to him", self.anchors)

    def test_19_stranger_glyph_uncertain_not_repaired(self):
        self.check_unique("origin_heading", "peregrine_stranger", "fortune_third")
        self.assertFalse(self.l["original_source_glyphs_fully_resolved"])

    def test_20_husband_shape_vs_qualities_and_author_anecdote(self):
        self.check_unique(
            "husband_heading",
            "seventh_shape",
            "seventh_lord_conditions",
            "lord_sun_aspect",
            "author_certainty",
            "saturnian_husband",
            "jovial_husband",
        )

    def test_21_riches_author_disagrees_with_ancients(self):
        self.check_unique(
            "wealth_heading",
            "contrary_ancients",
            "eighth_house",
            "eighth_ruler",
            "eighth_occupants",
        )

    def test_22_husband_riches_strength_and_angular_lord(self):
        self.check_unique(
            "fortified_eighth",
            "rich_husband",
            "contrary_poor",
            "lord_eighth_own",
            "angular_eighth",
            "not_fear_estate",
        )

    def test_23_mutual_reception_sextile_trine_and_negative_houses(self):
        self.check_unique(
            "agree_heading",
            "mutual_reception",
            "sextile",
            "trine",
            "benefic_good",
            "unity_result",
            "contrary_aspects",
            "bad_houses",
            "discord_result",
        )

    def test_24_following_unnumbered_children_navigation_not_absorbed(self):
        self.assertEqual(
            [r["id"] for r in self.r["rules"] if r["role"] == "next_section_navigation"],
            ["R8495", "R8496"],
        )
        self.assertEqual(self.r["substantive"], 97)
        self.assertEqual(self.accept["next_source_section"], "UNNUMBERED_FIFTH_HOUSE_CHILDREN")
        self.assertEqual(self.accept["next_source_pdf"], 636)

    def test_25_zero_real_human_sex_marriage_wealth_accuracy(self):
        self.assertFalse(self.l["sex_gender_partner_morality_predictions_authorized"])
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for r in self.r["rules"]:
            for key in (
                "independent_legal_marriage_occurrence_validated",
                "independent_marriage_ages_or_number_validated",
                "independent_husband_origin_wealth_traits_validated",
                "independent_marital_concord_validated",
                "real_partner_identity_gender_sexual_conduct_claim_authorized",
                "runtime_model_promoted",
            ):
                self.assertFalse(r[key], r["id"])

    def test_26_source_corpus_sha_and_numbered_change(self):
        self.assertEqual(self.accept["prior_lilly"], 8397)
        self.assertEqual(self.accept["lilly_if_published"], 8496)
        self.assertEqual(self.accept["combined_if_published"], 9562)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.accept["rules_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
