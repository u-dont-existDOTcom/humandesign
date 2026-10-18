"""Lilly 1647 original religion: document attribution, source noncausation, no person labels."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class ReligionSourceOriginalFirstEdition(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = read("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.r = read("RULES.json")
        cls.w = read("ORIGINAL_SOURCE_WITNESS.json")
        cls.map = read("SOURCE_TO_RECORD_MAP.json")
        cls.limits = read("UNRESOLVED_SOURCE_LIMITS.json")
        cls.scope = read("RELIGION_SOURCE_CAUSAL_SCOPE_V1.json")
        cls.accept = read("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])
        cls.anchors = " ".join(x["original_anchor_not_diplomatic"] for x in cls.r["rules"])

    def one(self, *roles):
        for role in roles:
            self.assertEqual(self.roles[role], 1, role)

    def test_01_original_1647_image_sha256_and_bytes(self):
        self.assertEqual(list(self.w["images"]), [str(n) for n in range(645, 650)])
        for src in self.w["images"].values():
            raw = (B / src["file"]).read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), src["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), src["sha256"])

    def test_02_source_folio_and_next_dream_chapter_separate(self):
        self.assertEqual(self.w["body_original_pdf_frames"], [645, 646, 647])
        self.assertEqual(self.w["next_printed_CXLIII_heading_frame"], 647)
        self.assertEqual(
            [s["printed_folio"] for s in self.w["images"].values()],
            ["611", "612", "613", "614", "615"],
        )

    def test_03_exact_104_source_records_unique_consecutive(self):
        self.assertEqual(
            [x["record_number"] for x in self.r["rules"]],
            list(range(8936, 9040)),
        )
        self.assertEqual(len({r["id"] for r in self.r["rules"]}), 104)

    def test_04_original_seven_source_groups_reversibly_mapped(self):
        ids = []
        for src, mapped in zip(self.a["groups"], self.map["source_groups"], strict=True):
            self.assertEqual(src["source_span"], mapped["source_span"])
            self.assertEqual(src["original_pdf_frames"], mapped["original_pdf_frames"])
            these = [r["id"] for r in src["claims"]]
            self.assertEqual(these, mapped["mapped_record_ids"])
            ids.extend(these)
        self.assertEqual(ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(self.map["source_group_count"], 7)

    def test_05_adverse_sources_and_jupiter_dignity_scope(self):
        self.one(
            "saturn_ninth",
            "mars_ninth",
            "south_node_ninth",
            "saturn_third",
            "mars_third",
            "movable_sign",
            "jupiter_weak",
            "jupiter_detriment",
            "jupiter_cadent",
            "jupiter_malefic",
        )
        self.assertEqual(self.roles["jupiter_peregrine"], 2)

    def test_06_negative_no_faith_change_sectary_are_distinct(self):
        self.one("religion_negative", "no_religion", "perverted_education", "sectary")

    def test_07_positive_jupiter_venus_node_third_or_ninth(self):
        self.one(
            "positive_jupiter",
            "positive_venus",
            "positive_node",
            "good_christian",
            "raised_religion",
        )

    def test_08_moderate_light_sources_and_benefic_vs_malefic(self):
        self.one(
            "luminaries_mercury",
            "fortune_part",
            "moderate_signs",
            "benefic_aspect",
            "malefic_aspect",
        )

    def test_09_empty_houses_jupiter_natural_fallback_requires_dignity(self):
        self.one(
            "no_planets_third_ninth",
            "jupiter_natural",
            "jupiter_own_sign",
            "jupiter_exaltation",
            "jupiter_angular",
            "jupiter_reception",
            "religious_man",
            "jupiter_debilitated",
        )

    def test_10_author_denies_celestial_enforcement_of_religion(self):
        self.one("noncompulsion_heading", "stars_not_enforce")
        self.assertTrue(self.scope["strict_source_scope"]["denies_stars_enforce_faith"])

    def test_11_author_denies_stars_cause_religion_or_irreligion(self):
        self.one("stars_not_cause")
        self.assertTrue(
            self.scope["strict_source_scope"]["denies_stars_cause_religion_or_irreligion"]
        )
        self.assertTrue(self.r["original_author_denies_stars_cause_religion"])

    def test_12_divine_grace_is_historical_theology_not_science(self):
        self.one("divine_grace")
        self.assertTrue(
            self.scope["strict_source_scope"]["author_theology_is_not_empirical_evidence"]
        )

    def test_13_source_claim_propensity_and_persistence_distinct_from_cause(self):
        self.one("natural_propensity", "permanence", "not_validate")
        self.assertTrue(
            self.scope["strict_source_scope"]["author_claims_stars_interpret_natural_propensity"]
        )
        self.assertTrue(
            self.scope["strict_source_scope"]["cannot_equate_causal_prediction_with_disposition"]
        )

    def test_14_piety_aphorisms_keep_cazimi_source_uncertainty(self):
        self.one("heading_piety", "jupiter_venus_node", "spica", "religious_party", "cazimi")
        self.assertFalse(self.limits["all_original_astrological_glyphs_collated"])

    def test_15_prophecy_and_divination_not_verified_supernatural_accuracy(self):
        self.one("prophecy", "divination")
        self.assertFalse(
            self.scope["targets_to_keep_distinct"][-1]["personal_classifier_authorized"]
        )

    def test_16_sun_piety_religious_profession_and_moderation(self):
        self.one(
            "sun_moon_mercury",
            "moderate",
            "sun_ninth",
            "sun_piety",
            "sun_preferment",
            "sun_preacher",
        )

    def test_17_saturn_ninth_own_dignity_positive_counterexample(self):
        self.one("saturn_ninth_dignified", "saturn_charity")
        self.assertIn("Saturn ninth own Dignities", self.anchors)

    def test_18_good_ninth_lord_ill_qualified_can_have_few_followers(self):
        self.one("ninth_lord_fortune", "lord_ill_disposed", "right_judgment", "few_credit")

    def test_19_saturn_or_mars_can_yield_qualified_positive_piety(self):
        self.one(
            "saturn_or_mars_direct",
            "good_aspect_fortunes",
            "fortunes_fixed",
            "approved_piety",
            "not_so_firm",
            "fortunes_in_place",
            "weak_counter",
        )

    def test_20_sun_jupiter_oracle_attribution_not_truth(self):
        self.one(
            "sun_jupiter_ninth", "dignity_other_planets", "aspect_mercury_moon", "oracle_words"
        )

    def test_21_many_planets_mixed_or_jupiter_empty_house_fallback(self):
        self.one(
            "many_planets_mixed",
            "empty_ninth_jupiter",
            "fallback_reception",
            "fallback_benefic_aspects",
            "fallback_angular",
            "fallback_religious",
        )

    def test_22_impiety_requires_source_qualifiers_not_one_saturn(self):
        self.one(
            "heading_impiety",
            "saturn_mars_node",
            "movable_signs",
            "unstable_religion",
            "lord_ninth_malefic_angular",
            "retrograde_strengthens",
        )

    def test_23_heresy_blasphemy_atheism_are_historical_sectarian_labels(self):
        self.one("saturn_heresy", "mars_blasphemy", "node_atheism", "contempt")
        self.assertTrue(
            self.scope["strict_source_scope"][
                "historical_categories_are_christian_sectarian_not_universal"
            ]
        )

    def test_24_saturn_mars_specific_source_faith_appearance_distinct(self):
        self.one("saturn_retro_ninth", "outward_no_faith", "mars_unfortunate", "wrangling_priests")

    def test_25_multiple_religion_change_or_variable_opinion_source_cases(self):
        self.one(
            "moon_symbol_lord_asc",
            "heritical_or_change",
            "venus_moon_ninth",
            "venus_moon_movable",
            "opinion_variable",
            "divinations_lover",
        )

    def test_26_mercury_and_moon_node_conversion_no_faith_source(self):
        self.one("mercury_ninth", "conversion", "moon_south_node", "no_care_religion")

    def test_27_following_dream_source_separate_and_not_ingested(self):
        self.assertEqual(
            [x["id"] for x in self.r["rules"] if x["role"] == "next_chapter_navigation"],
            ["R9038", "R9039"],
        )
        self.assertEqual(self.r["substantive"], 102)
        self.assertEqual(self.accept["next_printed_chapter"], "CXLIII")

    def test_28_zero_person_religion_morality_divination_predictions(self):
        self.assertFalse(self.limits["personal_religion_or_morality_inferences_authorized"])
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for x in self.r["rules"]:
            for key in (
                "independent_real_faith_affiliation_accuracy_validated",
                "independent_real_conversion_stability_validated",
                "independent_charity_or_moral_validity_established",
                "real_person_sectarian_label_authorized",
                "real_person_prophecy_or_divination_claim_authorized",
                "celestial_causal_religion_mechanism_verified",
                "runtime_model_promoted",
            ):
                self.assertFalse(x[key], (x["id"], key))

    def test_29_record_source_and_causal_guard_digest(self):
        self.assertEqual(self.accept["prior_lilly"], 8935)
        self.assertEqual(self.accept["lilly_if_published"], 9039)
        self.assertEqual(self.accept["combined_if_published"], 10105)
        self.assertEqual(self.accept["numbered_chapters_added"], 1)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.accept["rules_sha256"],
        )
        self.assertEqual(
            hashlib.sha256((B / "RELIGION_SOURCE_CAUSAL_SCOPE_V1.json").read_bytes()).hexdigest(),
            self.accept["causal_guard_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
