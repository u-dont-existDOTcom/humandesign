"""Documentary integrity tests for Lilly child-number section, never child prognosis."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class OriginalCountChildrenSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = read("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = read("RULES.json")
        cls.w = read("ORIGINAL_SOURCE_WITNESS.json")
        cls.m = read("SOURCE_TO_RECORD_MAP.json")
        cls.limits = read("UNRESOLVED_SOURCE_LIMITS.json")
        cls.accept = read("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])
        cls.anchors = " ".join(x["original_anchor_not_diplomatic"] for x in cls.r["rules"])

    def one(self, *names):
        for name in names:
            self.assertEqual(self.roles[name], 1, name)

    def test_01_original_jpeg_sha256_and_member_bytes(self):
        self.assertEqual(list(self.w["images"]), [str(n) for n in range(638, 644)])
        for info in self.w["images"].values():
            raw = (B / info["file"]).read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), info["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), info["sha256"])

    def test_02_page_numbers_and_true_next_source_boundary(self):
        self.assertEqual(self.w["body_pdf_frames"], [638, 639, 640])
        self.assertEqual(self.w["following_unnumbered_ninth_house_start_pdf"], 640)
        self.assertEqual(self.w["following_printed_CXXXIX_heading_pdf"], 640)
        self.assertEqual(
            [x["printed_folio"] for x in self.w["images"].values()],
            [str(n) for n in range(604, 610)],
        )

    def test_03_seventy_eight_records_contiguous_and_unique(self):
        self.assertEqual(
            [r["record_number"] for r in self.r["rules"]],
            list(range(8603, 8681)),
        )
        self.assertEqual(len({r["id"] for r in self.r["rules"]}), 78)

    def test_04_every_source_passage_reversibly_mapped(self):
        ids = []
        for authored, mapped in zip(self.a["source_groups"], self.m["source_groups"], strict=True):
            self.assertEqual(authored["source_span"], mapped["source_span"])
            self.assertEqual(authored["original_pdf_frames"], mapped["original_pdf_frames"])
            these = [r["id"] for r in authored["claims"]]
            self.assertEqual(mapped["mapped_record_ids"], these)
            ids.extend(these)
        self.assertEqual(ids, [r["id"] for r in self.r["rules"]])
        self.assertEqual(len(self.m["source_groups"]), 6)

    def test_05_exact_count_76_substantive_plus_two_navigation(self):
        self.assertEqual(self.r["substantive"], 76)
        self.assertEqual(self.r["following_unnumbered_navigation"], 2)
        self.assertEqual(len(self.r["rules"]), 78)

    def test_06_child_count_requires_planets_houses_and_signs(self):
        self.one(
            "collection",
            "count_planets",
            "planet_fruitful",
            "fifth_or_eleventh",
            "sign_fruitful",
            "greater_number",
        )

    def test_07_fewer_planets_and_barren_sign_negative_branch(self):
        self.one("few_planets", "barren_signs", "less_issue")

    def test_08_bicorporeal_double_and_fruitful_triple_distinct(self):
        self.one("bicorporeal", "double_child_count", "fruitful_multiplier", "triple_child_count")
        self.assertIn("double number", self.anchors)
        self.assertIn("treble the number", self.anchors)

    def test_09_two_count_multipliers_have_unresolved_overlap(self):
        issue = " ".join(self.limits["issues"]).lower()
        self.assertIn("double-count", issue)
        self.assertIn("triple-count", issue)
        self.assertIn("no disambiguating precedence", issue)

    def test_10_male_child_sex_source_not_just_masculine_planet(self):
        self.one(
            "masculine_planet_four",
            "masculine_houses",
            "masculine_signs",
            "masculine_degrees",
            "male_result",
        )

    def test_11_female_child_sex_require_orientation_and_degree(self):
        self.one(
            "feminine_planets",
            "feminine_occidental",
            "feminine_houses",
            "feminine_signs",
            "feminine_degrees",
            "female_result",
        )

    def test_12_weak_vs_strong_survival_fame_obedience_different(self):
        self.one(
            "all_significators",
            "potent",
            "essential_fortified",
            "long_life_result",
            "fame_result",
            "obedience",
            "financial_benefit",
            "weak_children",
            "short_lived",
            "disobedience",
        )

    def test_13_parent_child_affection_qualified_two_house_lords(self):
        self.one(
            "love_heading",
            "fifth_lord",
            "first_lord",
            "friendly_aspect",
            "mutual_love",
            "hateful_aspect",
            "mutual_hate",
        )

    def test_14_attributed_albubater_phrases_not_source_validity(self):
        self.one("aphorism_heading", "saturn_mars_fifth", "saturn_mars_eleventh", "not_livelong")
        self.assertIn("ALBUBATER", self.anchors)

    def test_15_sun_ruler_fifth_conj_malefic_separate_case(self):
        self.one("sun_fifth_dominion", "sun_conj_malefic", "no_child_alive")

    def test_16_taurus_mc_glyph_uncertain_and_moon_hard_aspect(self):
        self.one("sun_saturn_mercury_taurus", "moon_square_opposition", "alleged_children_die")
        row = next(r for r in self.r["rules"] if r["role"] == "sun_saturn_mercury_taurus")
        self.assertEqual(row["qualification"], "glyph-qualified")

    def test_17_two_different_malefic_oppositions_and_many_not_all(self):
        self.one("mars_op_jupiter", "mars_children", "jupiter_op_saturn", "jupiter_most")
        self.assertIn("greater part", self.anchors)

    def test_18_mercury_rising_saturn_west_child_short_life(self):
        self.one("mercury_asc", "saturn_west", "little_children_life")

    def test_19_fifth_house_lord_eighth_death_order_not_child_count(self):
        self.one("fifth_ruler_eighth", "children_first")

    def test_20_fifth_lord_taurus_and_alternative_eighth_malefic_contacts(self):
        self.one(
            "fifth_ruler_taurus",
            "fifth_ruler_malefic",
            "fifth_ruler_eighth_lord",
            "fifth_ruler_bad_aspect",
            "kills_children",
        )

    def test_21_ptolemy_method_explicit_disagreement_not_agreement(self):
        self.one("ptolemy_contrast", "not_corroborated")
        self.assertIn("all men declined opinion of Ptolomey", self.anchors)
        self.assertFalse(self.limits["original_ptolemy_disagreement_collated"])

    def test_22_ptolemy_attributed_four_houses_separately_preserved(self):
        self.one(
            "ptolemy_tenth",
            "ptolemy_eleventh",
            "ptolemy_fourth",
            "ptolemy_fifth",
            "ptolemy_signs",
            "ptolemy_occupants",
        )

    def test_23_travel_intro_not_child_count_and_next_chap_same_page(self):
        self.assertEqual(
            [r["id"] for r in self.r["rules"] if r["role"] == "next_section_navigation"],
            ["R8679", "R8680"],
        )
        self.assertEqual(
            self.accept["next_source"],
            "UNNUMBERED_NINTH_HOUSE_JOURNEYS_RELIGIONS",
        )
        self.assertEqual(self.accept["next_original_pdf"], 640)
        self.assertEqual(self.accept["following_printed_chapter"], "CXXXIX")

    def test_24_never_authorize_medical_or_child_mortality_forecast(self):
        self.assertFalse(self.limits["medical_or_child_mortality_advice_authorized"])
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for r in self.r["rules"]:
            for k in (
                "independent_actual_live_birth_count_validated",
                "independent_child_sex_accuracy_validated",
                "independent_child_survival_age_validated",
                "independent_parent_child_emotional_accuracy_validated",
                "clinical_health_or_child_mortality_forecast_authorized",
                "person_level_moral_or_gender_label_authorized",
                "ptolemy_source_attribution_independently_verified",
                "runtime_model_promoted",
            ):
                self.assertFalse(r[k], (r["id"], k))

    def test_25_expected_canonical_count_and_record_digest(self):
        self.assertEqual(self.accept["previous_lilly"], 8602)
        self.assertEqual(self.accept["lilly_if_published"], 8680)
        self.assertEqual(self.accept["combined_if_published"], 9746)
        self.assertEqual(self.accept["numbered_chapters_added"], 1)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.accept["rules_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
