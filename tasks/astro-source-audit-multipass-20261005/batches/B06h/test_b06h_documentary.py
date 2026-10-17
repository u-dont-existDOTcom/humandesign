"""Original Lilly marriage source structure: not real marriage/sexual validity."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class UnnumberedSeventhHouseMarriage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = read("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = read("RULES.json")
        cls.m = read("SOURCE_TO_RECORD_MAP.json")
        cls.w = read("ORIGINAL_SOURCE_WITNESS.json")
        cls.l = read("UNRESOLVED_SOURCE_LIMITS.json")
        cls.accept = read("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])
        cls.anchors = " ".join(x["original_anchor_not_diplomatic"] for x in cls.r["rules"])

    def test_01_image_hash_and_bytes(self):
        self.assertEqual(list(self.w["images"]), ["621", "622", "623", "624", "625"])
        for value in self.w["images"].values():
            p = B / value["file"]
            data = p.read_bytes()
            self.assertEqual(data[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(data), value["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), value["sha256"])

    def test_02_original_folio_and_numbered_seam(self):
        self.assertEqual(
            [r["printed_folio"] for r in self.w["images"].values()],
            ["587", "588", "589", "590", "591"],
        )
        self.assertTrue(self.w["seventh_house_intro_is_unnumbered"])
        self.assertEqual(self.w["body_pdf_frames"], [621, 622, 623])
        self.assertEqual(self.w["following_printed_CXXXI_heading_frame"], 623)

    def test_03_records_append_only(self):
        self.assertEqual(
            [x["record_number"] for x in self.r["rules"]],
            list(range(7878, 7944)),
        )
        self.assertEqual(len(set(x["id"] for x in self.r["rules"])), 66)

    def test_04_original_eight_groups_reversibly_mapped(self):
        ids = []
        for src, mapped in zip(self.a["source_groups"], self.m["source_groups"], strict=True):
            self.assertEqual(src["source_span"], mapped["source_span"])
            self.assertEqual(src["original_pdf_frames"], mapped["original_pdf_frames"])
            refs = [r["id"] for r in src["clauses"]]
            self.assertEqual(refs, mapped["mapped_record_ids"])
            ids.extend(refs)
        self.assertEqual(ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(len(self.m["source_groups"]), 8)

    def test_05_indicators_for_men_kept_separate(self):
        self.assertEqual(self.roles["marriage_indicators"], 3)
        self.assertIn("Venus and Moon", self.anchors)
        self.assertIn("seventh House and Lord", self.anchors)
        self.assertIn("Planets posited in seventh", self.anchors)

    def test_06_original_marriage_vs_dowry_not_merged(self):
        self.assertEqual(self.roles["wife_quality"], 1)
        self.assertEqual(self.roles["wife_dowry"], 1)
        self.assertEqual(self.roles["significator_context"], 1)
        self.assertEqual(self.roles["subheading"], 2)

    def test_07_barren_signs_two_planets(self):
        self.assertEqual(self.roles["barren_both"], 1)
        self.assertEqual(self.roles["barren_list"], 1)
        for term in ("Virgo", "Gemini", "Leo"):
            self.assertIn(term, self.anchors)

    def test_08_eighth_house_not_cadent_original_exception(self):
        self.assertEqual(self.roles["negative_houses"], 1)
        self.assertEqual(self.roles["eighth_exception"], 1)
        self.assertIn("eighth though not cadent", self.anchors)

    def test_09_negative_requires_corresponding_other_significators(self):
        self.assertEqual(self.roles["reinforcement"], 1)
        self.assertEqual(self.roles["single_or_aversion"], 1)
        self.assertEqual(self.roles["negative_primary"], 1)

    def test_10_saturn_weak_primary_compound_not_simple(self):
        for role in (
            "weak_luminaries",
            "saturn_conjunction",
            "venus_isolation",
            "moon_barren",
            "moon_cadent",
            "moon_afflicted",
            "no_desire",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_11_explicit_favorable_venus_moon_overrides_saturn(self):
        self.assertEqual(self.roles["saturn_strong_required"], 1)
        self.assertEqual(self.roles["luminaries_overrule"], 1)
        self.assertIn("judgement holds not true", self.anchors)

    def test_12_elevated_saturn_needs_unassisted_luminaries(self):
        for role in (
            "saturn_elevated",
            "no_aspect_assist",
            "elevation_as_hard",
            "saturn_impedes",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_13_no_private_sexual_behaviors_become_facts(self):
        for role in ("concubines", "weak_all", "no_lights_support", "chastity_combo", "lust_combo"):
            self.assertEqual(self.roles[role], 1)

    def test_14_compound_alternate_never_marriage_conditions(self):
        for role in (
            "others_review",
            "barren_or_cadent",
            "weak_afflicted",
            "saturn_hard",
            "never_marry_result",
            "moon_scorpio",
            "saturn_leo_taurus",
            "moon_combust",
            "moon_square_opposition",
            "saturn_cap_aqua_libra",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_15_moon_square_saturn_alone_explicitly_insufficient(self):
        for role in ("moon_saturn_not_sufficient", "need_many_testimonies", "venus_barren_alone"):
            self.assertEqual(self.roles[role], 1)
        self.assertIn("without many other testimonies", self.anchors)

    def test_16_positive_fecundity_and_seventh_benefic(self):
        for role in (
            "seventh_prolific",
            "seventh_ruler_fortunate",
            "benefic_seventh",
            "venus_moon_fecund",
            "marriage_houses",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_17_reception_application_and_outcome_separate(self):
        for role in (
            "asc_lord_applying",
            "equal_reception",
            "desire_marriage",
            "majority_concurring",
            "marry_result",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_18_potency_unsupported_and_not_a_marriage_certificate(self):
        self.assertEqual(self.roles["potency"], 1)
        self.assertFalse(self.l["sex_life_character_or_partner_claim_authorized"])

    def test_19_next_marriage_difficulty_chapter_not_ingested(self):
        self.assertEqual(
            [r["id"] for r in self.r["rules"] if r["role"] == "next_chapter_navigation"],
            ["R7942", "R7943"],
        )
        self.assertEqual(self.accept["next_printed_chapter"], "CXXXI")
        self.assertEqual(self.accept["new_numbered_chapters"], 0)
        self.assertEqual(self.r["substantive_historical_clauses"], 64)

    def test_20_no_real_relationship_or_intimate_validity(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        self.assertEqual(self.r["independent_human_marriage_predictions"], 0)
        for r in self.r["rules"]:
            self.assertFalse(r["independent_human_marriage_outcome_validated"])
            self.assertFalse(r["real_partner_character_or_sexual_behavior_validated"])
            self.assertFalse(r["person_level_moral_or_intimate_claim_authorized"])
            self.assertFalse(r["runtime_model_promoted"])

    def test_21_corpus_count_and_source_sha(self):
        self.assertEqual(self.accept["previous_lilly"], 7877)
        self.assertEqual(self.accept["lilly_if_published"], 7943)
        self.assertEqual(self.accept["combined_if_published"], 9009)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.accept["rules_sha256"],
        )
        self.assertEqual(
            hashlib.sha256((B / "SOURCE_FIRST_AUTHORING_20261017.json").read_bytes()).hexdigest(),
            self.accept["source_authoring_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
