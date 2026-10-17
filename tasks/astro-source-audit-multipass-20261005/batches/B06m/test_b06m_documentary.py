"""Original first edition Lilly marriage concord: source integrity not real couple validity."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class OriginalMaritalConcord(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.author = j("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.rules = j("RULES.json")
        cls.witness = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.map = j("SOURCE_TO_RECORD_MAP.json")
        cls.limits = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.accept = j("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.rules["rules"])
        cls.anchors = " ".join(x["anchor_not_diplomatic"] for x in cls.rules["rules"])

    def test_01_original_jpegs_sha_and_length(self):
        self.assertEqual(list(self.witness["photos"]), ["631", "632", "633", "634"])
        for item in self.witness["photos"].values():
            b = (B / item["file"]).read_bytes()
            self.assertEqual(b[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(b), item["bytes"])
            self.assertEqual(hashlib.sha256(b).hexdigest(), item["sha256"])

    def test_02_chapter_seam_at_upper_633(self):
        self.assertEqual(self.witness["body_pdf_frames"], [631, 632, 633])
        self.assertEqual(self.witness["following_printed_CXXXVI_heading_pdf"], 633)
        self.assertEqual(
            [x["printed_folio"] for x in self.witness["photos"].values()],
            ["597", "598", "599", "600"],
        )

    def test_03_append_only_71_historical_annotations(self):
        rows = self.rules["rules"]
        self.assertEqual([x["record_number"] for x in rows], list(range(8273, 8344)))
        self.assertEqual(len(set(x["id"] for x in rows)), 71)

    def test_04_seven_complete_source_groups_reversible(self):
        ids = []
        for a, m in zip(self.author["groups"], self.map["source_groups"], strict=True):
            self.assertEqual(a["source_span"], m["source_span"])
            self.assertEqual(a["original_pdf_frames"], m["original_pdf_frames"])
            mapped = [x["id"] for x in a["clauses"]]
            self.assertEqual(mapped, m["mapped_record_ids"])
            ids.extend(mapped)
        self.assertEqual(ids, [x["id"] for x in self.rules["rules"]])
        self.assertEqual(len(self.map["source_groups"]), 7)

    def test_05_source_scope_is_mutual_marital_concord_not_spouse_count(self):
        self.assertEqual(self.rules["printed_chapter"], "CXXXV")
        self.assertEqual(self.roles["chapter_heading"], 1)
        self.assertEqual(self.roles["source_indicator"], 1)

    def test_06_fortunate_friendly_and_malefic_hard(self):
        for role in (
            "benefic_planet",
            "friendly_to_moon",
            "love_outcome",
            "negative_nature",
            "hard_to_moon",
            "quarrel_outcome",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_07_benefic_hard_aspect_moderate_not_unity(self):
        for role in (
            "benign_ill_aspect",
            "moderate_agreement",
            "in_most_accord",
            "benefic_hostile_mitigated",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_08_malefic_beneficial_aspect_still_mostly_disagree(self):
        for role in (
            "malefic_friendly",
            "indifferent_agreement",
            "mostly_disagree",
            "malefic_good_limited",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_09_seventh_and_moon_exclusivity_original_limitation(self):
        self.assertEqual(self.roles["planet_scope_limit"], 1)
        self.assertEqual(self.roles["exclude_other_significators"], 1)

    def test_10_two_independent_birth_charts_not_single_natal_inferred(self):
        self.assertEqual(self.roles["both_genitures"], 1)
        self.assertEqual(self.roles["if_procured"], 1)
        self.assertEqual(self.roles["best_way"], 1)

    def test_11_wifes_sun_on_husbands_moon_same_sign_and_degree(self):
        for role in ("wife_sun_on_man_moon", "wife_moon_on_man_sun", "sun_moon_concord"):
            self.assertEqual(self.roles[role], 1)
        self.assertIn("Signe and degree Moon", self.anchors)

    def test_12_trine_sextile_vs_hostile_aspects(self):
        for role in ("marriage_sig_sextile", "marriage_sig_trine", "unity_af", "contrary_hard"):
            self.assertEqual(self.roles[role], 1)

    def test_13_venus_saturn_mars_glyph_no_false_conjunction(self):
        self.assertEqual(self.roles["venus_saturn_mars"], 1)
        r = next(x for x in self.rules["rules"] if x["role"] == "venus_saturn_mars")
        self.assertEqual(r["source_qualification"], "glyph-qualified")
        self.assertEqual(self.roles["jealousy_outcome"], 1)

    def test_14_venus_twelfth_and_jupiter_second_condition(self):
        for role in ("venus_twelfth", "jupiter_twelfth", "low_fortune"):
            self.assertEqual(self.roles[role], 1)

    def test_15_historical_jealousy_morality_not_real_partner_facts(self):
        self.assertEqual(self.roles["lasciviousness_blame"], 1)
        self.assertFalse(self.limits["intimate_or_moral_real_partner_claims_authorized"])

    def test_16_mutable_common_signs_distinct_context(self):
        for role in (
            "movable_marriage_indicators",
            "venus_movable",
            "venus_common",
            "asc_lord_common",
            "venus_unfortunate",
        ):
            self.assertEqual(self.roles[role], 1)
        self.assertEqual(self.roles["not_content_one"], 1)
        self.assertEqual(self.roles["discontent_one"], 1)

    def test_17_moon_sun_compound_same_page_crossing(self):
        for role in ("moon_beholds_sun", "both_humane_signs", "fortunate_aspects", "agree_well"):
            self.assertEqual(self.roles[role], 1)
        self.assertEqual(self.roles["bad_sun_moon_contact"], 1)
        self.assertEqual(self.roles["malefic_hard_one"], 1)

    def test_18_moon_mars_and_diminishing_dangerous_sex_claim_not_authorized(self):
        for role in ("moon_waning", "moon_mars_conj", "movable_sign", "wife_loves_other"):
            self.assertEqual(self.roles[role], 1)
        r = next(x for x in self.rules["rules"] if x["role"] == "wife_loves_other")
        self.assertFalse(r["real_partner_fidelity_morality_jealousy_claim_authorized"])

    def test_19_lunar_rulership_waning_eighth_must_be_joint(self):
        for role in ("moon_lady_seventh", "waning_again", "moon_eighth", "no_felicity"):
            self.assertEqual(self.roles[role], 1)

    def test_20_next_mortality_chapter_not_ingested(self):
        self.assertEqual(
            [x["id"] for x in self.rules["rules"] if x["role"] == "next_chapter_navigation"],
            ["R8342", "R8343"],
        )
        self.assertEqual(self.accept["next_printed_chapter"], "CXXXVI")
        self.assertEqual(self.rules["substantive"], 69)

    def test_21_no_real_couple_or_intimate_prediction_promoted(self):
        self.assertEqual(self.rules["empirical_validations"], 0)
        self.assertEqual(self.rules["actual_couple_predictive_validations"], 0)
        self.assertEqual(self.rules["runtime_promotions"], 0)
        for r in self.rules["rules"]:
            self.assertFalse(r["independent_human_marital_concord_validated"])
            self.assertFalse(r["independent_real_couple_pair_chart_accuracy_validated"])
            self.assertFalse(r["real_partner_fidelity_morality_jealousy_claim_authorized"])
            self.assertFalse(r["runtime_model_promoted"])

    def test_22_source_sha_and_cumulative_total(self):
        self.assertEqual(self.accept["previous_lilly"], 8272)
        self.assertEqual(self.accept["lilly_if_published"], 8343)
        self.assertEqual(self.accept["combined_if_published"], 9409)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.accept["rules_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
