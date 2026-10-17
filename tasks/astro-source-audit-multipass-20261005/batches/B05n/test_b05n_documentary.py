"""First-edition wealth chapter: historical source mapping and integrity tests.

These are not tests of real-world wealth forecasts or causality.
"""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class FirstEditionWhetherRich(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.authored = j("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.rules = j("RULES.json")
        cls.mapping = j("SOURCE_TO_RECORD_MAP.json")
        cls.images = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.limits = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.accept = j("ACCEPTANCE.json")
        cls.claims = cls.rules["rules"]
        cls.roles = Counter(x["role"] for x in cls.claims)

    def test_01_jpeg_source_frames_sha_and_bytes(self):
        for info in self.images["images"].values():
            p = B / info["path"]
            raw = p.read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), info["bytes"])
            self.assertEqual(sha(p), info["sha256"])

    def test_02_source_frame_order_and_next_chapter_seam(self):
        self.assertEqual(list(self.images["images"]), ["587", "588", "589", "590", "591"])
        self.assertEqual(self.images["body_pages"], [587, 588])
        self.assertEqual(self.images["next_heading_pdf_frame"], 588)
        self.assertEqual(self.images["printed_folio_sequence"], ["553", "554", "555", "556", "557"])
        self.assertEqual(self.images["first_following_chapter"], "CXV")

    def test_03_record_ids_are_contiguous_and_unique(self):
        self.assertEqual([x["record_number"] for x in self.claims], list(range(6854, 6911)))
        self.assertEqual(len(set(x["id"] for x in self.claims)), 57)

    def test_04_full_bidirectional_source_claim_coverage(self):
        ids = []
        for authored, mapped in zip(
            self.authored["source_groups"],
            self.mapping["source_groups"],
            strict=True,
        ):
            self.assertEqual(authored["source_span"], mapped["source_span"])
            self.assertEqual(authored["pdf_pages"], mapped["original_pdf_frames"])
            expected = [c["id"] for c in authored["claims"]]
            self.assertEqual(mapped["mapped_record_ids"], expected)
            ids.extend(expected)
        self.assertEqual(ids, [r["id"] for r in self.claims])
        self.assertEqual(len(self.mapping["source_groups"]), 12)

    def test_05_independent_previous_unnumbered_source_not_recopied(self):
        self.assertEqual(self.roles["source_dependency"], 1)
        self.assertTrue(
            any(
                "above" in r["historical_source_interpretation"]
                or "immediately" in r["historical_source_interpretation"]
                for r in self.claims
                if r["role"] == "source_dependency"
            )
        )

    def test_06_all_or_majority_angular_plus_dignity(self):
        self.assertEqual(self.roles["angle_condition"], 1)
        self.assertEqual(self.roles["angle_alternative"], 1)
        self.assertEqual(self.roles["essential_dignity_condition"], 1)

    def test_07_wealth_degree_depends_on_for_and_against_testimony(self):
        self.assertEqual(self.roles["grading_rule"], 1)
        self.assertEqual(self.roles["grading_result"], 1)
        r = [x for x in self.claims if x["role"] == "grading_rule"][0]
        self.assertIn("fortitudes or debilities", r["original_anchor_not_diplomatic"])

    def test_08_explicit_poverty_and_moderate_alternatives(self):
        s = " ".join(x["original_anchor_not_diplomatic"] for x in self.claims)
        self.assertIn("all the Significators weak", s)
        self.assertIn("moderately fortified", s)
        self.assertEqual(self.roles["middle_result"], 2)

    def test_09_regulus_spica_operator_uncertainty_retained(self):
        text = " ".join(x["original_anchor_not_diplomatic"] for x in self.claims)
        self.assertIn("Regulus", text)
        self.assertIn("Spica", text)
        self.assertEqual(self.roles["stellar_ambiguity"], 2)
        self.assertTrue(any("Regulus/Spica" in x for x in self.limits["issues"]))

    def test_10_benefics_not_mandatory_for_wealth_significator(self):
        x = next(r for r in self.claims if r["role"] == "planet_role_exception")
        self.assertIn("Fortunes or Infortunes", x["original_anchor_not_diplomatic"])

    def test_11_two_luminaries_favourable_alt_crosses_page_break(self):
        self.assertEqual(self.roles["luminary_stellar_wealth"], 1)
        self.assertEqual(self.roles["luminary_stellar_alternative"], 1)
        self.assertEqual(self.roles["luminary_benefic_alternative"], 1)
        for r in self.claims:
            if r["role"].startswith("luminary_"):
                self.assertEqual(r["original_pdf_frames"], [587, 588])

    def test_12_moon_ascendant_requires_favourable_condition(self):
        x = next(
            r
            for r in self.claims
            if r["role"] == "wealth_configuration"
            and "Moon in the ascendant" in r["original_anchor_not_diplomatic"]
        )
        self.assertIn("fortunate", x["original_anchor_not_diplomatic"])

    def test_13_sun_moon_trine_requires_exaltation_and_unafflicted(self):
        text = " ".join(x["original_anchor_not_diplomatic"] for x in self.claims)
        for marker in (
            "Sun and Moon in Trine",
            "Sun then in his Exaltation",
            "neither of them unfortunated by Saturn or Mars",
        ):
            self.assertIn(marker, text)

    def test_14_jupiter_moon_swap_has_two_distinct_cases(self):
        text = " ".join(x["original_anchor_not_diplomatic"] for x in self.claims)
        for marker in (
            "Jupiter in the second and Moon in the first",
            "Jupiter in the ascendant in his owne dignities",
            "Moon in the second in her dignities",
        ):
            self.assertIn(marker, text)

    def test_15_three_eighth_house_inheritance_outcomes(self):
        self.assertEqual(self.roles["inheritance_configuration"], 6)
        self.assertEqual(self.roles["inheritance_result"], 3)
        text = " ".join(x["original_anchor_not_diplomatic"] for x in self.claims)
        for marker in ("diurnall Geniture", "Lord of the eighth", "Lord of Part of Fortune"):
            self.assertIn(marker, text)

    def test_16_saturn_land_claim_has_all_qualifiers(self):
        self.assertEqual(self.roles["land_configuration"], 3)
        self.assertEqual(self.roles["land_result"], 1)
        text = " ".join(
            x["original_anchor_not_diplomatic"]
            for x in self.claims
            if x["role"] == "land_configuration"
        )
        for marker in ("well posited", "essentially strong", "Trine"):
            self.assertIn(marker, text)

    def test_17_moon_mars_saturn_poverty_preserves_ambiguity(self):
        x = next(
            r
            for r in self.claims
            if "Moon in conjunction with Mars" in r["original_anchor_not_diplomatic"]
        )
        self.assertEqual(x["source_qualification"], "ambiguous")
        self.assertIn("Saturn", x["original_anchor_not_diplomatic"])

    def test_18_saturn_moon_square_or_opposition_separate(self):
        text = " ".join(x["original_anchor_not_diplomatic"] for x in self.claims)
        self.assertIn("Square of Saturn and Moon", text)
        self.assertIn("Opposition of Saturn and Moon", text)

    def test_19_complex_poverty_cluster_not_simplified(self):
        text = " ".join(
            x["original_anchor_not_diplomatic"]
            for x in self.claims
            if x["role"] == "poverty_configuration"
        )
        for marker in (
            "Fortunes in succedant",
            "Moon combust",
            "uncertain glyphs",
            "Jupiter cadent",
        ):
            self.assertIn(marker, text)
        self.assertEqual(self.roles["poverty_configuration"], 9)

    def test_20_inverse_clause_explicitly_unresolved(self):
        x = next(r for r in self.claims if r["role"] == "poverty_scope")
        self.assertIn("the contrary", x["original_anchor_not_diplomatic"])
        self.assertEqual(x["source_qualification"], "ambiguous")

    def test_21_following_chapter_is_navigation_only(self):
        nav = [x for x in self.claims if x["role"] == "next_chapter_navigation"]
        self.assertEqual([r["id"] for r in nav], ["R6909", "R6910"])
        self.assertEqual(self.rules["substantive_historical_units"], 55)
        self.assertEqual(self.accept["following_heading_pdf_frame"], 588)

    def test_22_no_empirical_wealth_or_inheritance_success(self):
        self.assertEqual(self.rules["empirical_validations"], 0)
        self.assertEqual(self.rules["independently_successful_economic_predictions"], 0)
        self.assertEqual(self.rules["runtime_promotions"], 0)
        for r in self.claims:
            self.assertTrue(r["historical_documentary_accepted"])
            self.assertFalse(r["independent_economic_outcome_validated"])
            self.assertFalse(r["tested_wealth_prediction_success"])
            self.assertFalse(r["financial_advice_authorized"])
            self.assertFalse(r["runtime_model_promoted"])

    def test_23_source_uncertainties_and_no_diplomatic_completion(self):
        self.assertFalse(self.rules["full_diplomatic_transcription"])
        self.assertFalse(self.limits["diplomatic_transcription_complete"])
        self.assertGreaterEqual(len(self.limits["issues"]), 15)
        self.assertTrue(self.limits["source_documentary_only"])

    def test_24_record_number_and_rules_hash_total(self):
        self.assertEqual(self.accept["previous_lilly"], 6853)
        self.assertEqual(self.accept["lilly_if_published"], 6910)
        self.assertEqual(self.accept["combined_if_published"], 7976)
        self.assertEqual(sha(B / "RULES.json"), self.accept["rules_sha256"])


if __name__ == "__main__":
    unittest.main()
