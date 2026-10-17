"""Original Lilly 1647 CXXXIIII: historical source integrity only."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class WifeAppearanceDispositionRichesOriginalSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = j("RULES.json")
        cls.w = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.mapping = j("SOURCE_TO_RECORD_MAP.json")
        cls.l = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.accept = j("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])
        cls.anchors = " ".join(x["source_anchor_not_diplomatic"] for x in cls.r["rules"])

    def test_01_all_original_first_edition_photo_hash_and_bytes(self):
        self.assertEqual(list(self.w["original_source_images"]), [str(n) for n in range(627, 635)])
        for v in self.w["original_source_images"].values():
            data = (B / v["file"]).read_bytes()
            self.assertEqual(data[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(data), v["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), v["sha256"])

    def test_02_physical_printed_folio_and_next_chapter_boundary(self):
        self.assertEqual(self.w["original_body_pdf_frames"], [627, 628, 629, 630, 631])
        self.assertEqual(self.w["next_printed_CXXXV_heading_frame"], 631)
        self.assertEqual(
            [v["printed_folio"] for v in self.w["original_source_images"].values()],
            [str(n) for n in range(593, 601)],
        )

    def test_03_131_append_only_source_ids(self):
        self.assertEqual([r["record_number"] for r in self.r["rules"]], list(range(8142, 8273)))
        self.assertEqual(len(set(r["id"] for r in self.r["rules"])), 131)

    def test_04_fourteen_passages_reversibly_grouped(self):
        ids = []
        for src, dest in zip(self.a["groups"], self.mapping["source_groups"], strict=True):
            self.assertEqual(src["source_span"], dest["source_span"])
            self.assertEqual(src["original_pdf_frames"], dest["original_pdf_frames"])
            rec = [x["id"] for x in src["clauses"]]
            self.assertEqual(dest["mapped_record_ids"], rec)
            ids.extend(rec)
        self.assertEqual(ids, [r["id"] for r in self.r["rules"]])
        self.assertEqual(len(self.mapping["source_groups"]), 14)

    def test_05_original_question_not_just_appearance(self):
        for role in ("heading", "wealth_heading", "heading_good_wife", "heading_ill_wife"):
            self.assertEqual(self.roles[role], 1)
        self.assertEqual(self.roles["subheading"], 2)

    def test_06_aesthetic_sign_categories_historic_and_glyph_uncertain(self):
        for role in (
            "source_fair_category",
            "source_mediocre_category",
            "source_deform_category",
            "glyph_uncertainty",
        ):
            self.assertEqual(self.roles[role], 1)
        self.assertFalse(self.l["original_glyph_categories_fully_resolved"])

    def test_07_majority_required_not_one_zodiac_sign(self):
        for role in (
            "seventh_sign",
            "wife_planet",
            "lunar_applicants",
            "partile_or_conjunction",
            "majority_signs",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_08_saturn_composite_requires_affliction_and_significators(self):
        for role in (
            "saturn_bad",
            "saturn_afflicts",
            "sun_combust",
            "venus_saturn_terms",
            "saturn_aspect_venus",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_09_older_spouse_and_widow_not_bodily_stigma(self):
        for role in ("older_spouse", "widow_not_maid", "jupiter_weak"):
            self.assertEqual(self.roles[role], 1)
        self.assertEqual(self.roles["saturn_mars_seventh"], 2)

    def test_10_jupiter_negative_qualifies_benefic_positive(self):
        for role in (
            "jupiter_venus_moon",
            "jupiter_seventh",
            "jupiter_moon_conj",
            "other_circumstances",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_11_unsupported_author_personal_success(self):
        r = next(x for x in self.r["rules"] if x["role"] == "author_claim")
        self.assertEqual(r["qualifier"], "unverified-author-anecdote")
        self.assertFalse(r["independent_human_appearance_accuracy_validated"])

    def test_12_ptolemy_attribution_separate_from_chinese_source(self):
        self.assertEqual(self.roles["ptolemy_attributed"], 1)
        self.assertEqual(self.roles["authors_list"], 1)
        self.assertTrue(
            all(
                not x["original_ptolemy_attribution_independently_verified"]
                for x in self.r["rules"]
            )
        )

    def test_13_temperament_planets_need_source_dignity(self):
        for role in (
            "saturn_moon_apply",
            "saturn_fortified",
            "saturn_debilitated",
            "jupiter_well",
            "jupiter_ill",
            "moon_mars_apply",
            "mars_well",
            "mars_bad",
            "moon_venus_apply",
            "venus_strong",
            "venus_weak",
            "moon_mercury_apply",
            "mercury_good",
            "mercury_bad",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_14_sun_moon_nonmeaning_limited_to_temperament(self):
        self.assertEqual(self.roles["sun_moon_nonmeaning"], 1)
        self.assertIn("Sun and Moon no manner of signification", self.anchors)

    def test_15_venus_position_aphorisms_keep_distinct_outcomes(self):
        for role in (
            "venus_second",
            "venus_sixth",
            "venus_fourth",
            "venus_cancer",
            "venus_seventh_delay",
            "venus_eleventh",
            "venus_tenth",
            "venus_jupiter",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_16_unverified_moral_criminality_magic_sex_labels_caged(self):
        for role in (
            "witchcraft_poison",
            "venus_saturn_mars_sixth",
            "venus_seventh_harlots",
            "mars_venus_individual",
        ):
            self.assertEqual(self.roles[role], 1)
        self.assertFalse(
            self.l["real_person_spouse_character_moral_or_disability_claim_authorized"]
        )

    def test_17_fertility_and_impotence_not_medical_prediction(self):
        for role in ("moon_fourth_venus_tenth_saturn", "age_or_nature", "venus_saturn_seventh"):
            self.assertEqual(self.roles[role], 1)
        self.assertFalse(self.l["person_health_or_mortality_forecasts_authorized"])

    def test_18_spouse_riches_is_distinct_from_appearance(self):
        self.assertEqual(self.roles["wealth_heading"], 1)
        for role in (
            "moon_aspect_good",
            "moon_conj_wealth",
            "benefic_well_fortified",
            "wife_rich_wealth",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_19_class_relative_rule_and_beggar_example(self):
        for role in (
            "native_class_first",
            "noble_absolute_error",
            "beggar_case",
            "relative_tradesman",
            "dowry_portion",
            "life_conditions",
            "quid_capax",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_20_good_wealth_with_powerful_malefic_counterexample(self):
        for role in (
            "malefics_seventh",
            "malefic_power_rich",
            "malefic_ill_wife",
            "strong_malefics_wealth",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_21_reciprocal_second_seventh_tenth_rulers(self):
        for role in (
            "seventh_lord_tenth",
            "tenth_lord_seventh",
            "second_lord_seventh",
            "seventh_lord_second",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_22_positive_inheritance_fixed_star_extra_conditions(self):
        for role in (
            "jupiter_good_venus_moon",
            "mutual_reception",
            "seventh_lord_eighth",
            "inheritance_ample",
            "royal_fixed_star",
            "cusp_fortunate",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_23_negative_sixth_twelfth_alternatives(self):
        for role in (
            "seventh_sixth_twelfth",
            "sixth_twelfth_seventh",
            "twelfth_lord_seventh",
            "seventh_lord_twelfth",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_24_saturn_mars_serious_marital_mortality_not_human_validation(self):
        for role in ("benefics_no_aspect", "not_cadent", "saturn_grief", "mars_death"):
            self.assertEqual(self.roles[role], 1)
        self.assertEqual(self.roles["saturn_mars_seventh"], 2)
        self.assertTrue(
            all(not x["independent_marital_medical_mortality_validated"] for x in self.r["rules"])
        )

    def test_25_lunar_ruler_eighth_requires_decreasing_light(self):
        for role in ("moon_seventh_ruler_eighth", "moon_waning", "no_felicity"):
            self.assertEqual(self.roles[role], 1)

    def test_26_following_marital_concord_not_ingested(self):
        self.assertEqual(
            [r["id"] for r in self.r["rules"] if r["role"] == "next_chapter_navigation"],
            ["R8271", "R8272"],
        )
        self.assertEqual(self.accept["next_printed_chapter"], "CXXXV")
        self.assertEqual(self.r["substantive"], 129)

    def test_27_no_human_appearance_wealth_behavior_life_prediction(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for row in self.r["rules"]:
            for key in (
                "independent_human_appearance_accuracy_validated",
                "independent_human_spouse_personality_validated",
                "independent_spouse_wealth_class_validated",
                "independent_marital_medical_mortality_validated",
                "real_person_moral_intimate_danger_label_authorized",
                "runtime_model_promoted",
            ):
                self.assertFalse(row[key], row["id"])

    def test_28_corpus_and_source_sha256(self):
        self.assertEqual(self.accept["prior_lilly"], 8141)
        self.assertEqual(self.accept["lilly_if_published"], 8272)
        self.assertEqual(self.accept["combined_if_published"], 9338)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.accept["rules_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
