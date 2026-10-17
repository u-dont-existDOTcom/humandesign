"""Integrity, source-coverage and non-promotion tests for original 1647 Lilly CXVI.

Success is documentary integrity only; it does not prove character or financial forecasts.
"""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class WealthConductHistoricalSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = j("RULES.json")
        cls.map = j("SOURCE_TO_RECORD_MAP.json")
        cls.images = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.limits = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.accept = j("ACCEPTANCE.json")
        cls.roles = Counter(r["role"] for r in cls.r["rules"])

    def text(self):
        return " ".join(r["original_anchor_not_diplomatic"] for r in self.r["rules"])

    def test_01_first_edition_images_sha256_bytes(self):
        for row in self.images["images"].values():
            p = B / row["path"]
            self.assertEqual(sha(p), row["sha256"])
            self.assertEqual(p.stat().st_size, row["bytes"])
            self.assertEqual(p.read_bytes()[:2], bytes.fromhex("ffd8"))

    def test_02_folios_with_duplicate_561_preserved(self):
        self.assertEqual(self.images["source_body_original_frames"], [594, 595, 596])
        self.assertEqual(
            [self.images["images"][str(n)]["printed_folio_verified"] for n in (594, 595, 596)],
            ["561", "561", "562"],
        )
        self.assertIn("duplicate", self.images["original_pagination_note"])

    def test_03_new_chapter_separate_same_page(self):
        self.assertEqual(self.images["next_numbered_heading_frame"], 596)
        self.assertEqual(self.accept["next_pdf_frame"], 596)
        self.assertEqual(self.a["printed_chapter"], "CXVI")

    def test_04_consecutive_57_source_records(self):
        self.assertEqual([r["record_number"] for r in self.r["rules"]], list(range(6995, 7052)))
        self.assertEqual(self.r["record_count"], 57)
        self.assertEqual(len({r["id"] for r in self.r["rules"]}), 57)

    def test_05_bidirectional_mapping_complete_and_unique(self):
        mapped = []
        for original, reverse in zip(self.a["groups"], self.map["groups"], strict=True):
            self.assertEqual(original["source_span"], reverse["source_span"])
            self.assertEqual(original["source_pdf_frames"], reverse["pdf_pages"])
            refs = [c["id"] for c in original["clauses"]]
            self.assertEqual(refs, reverse["mapped_record_ids"])
            mapped.extend(refs)
        self.assertEqual(mapped, [r["id"] for r in self.r["rules"]])
        self.assertEqual(len(self.map["groups"]), 10)
        self.assertEqual(len(mapped), len(set(mapped)))

    def test_06_good_planet_nature_and_alternative_dignity(self):
        self.assertEqual(self.roles["good_planet_definition"], 1)
        self.assertEqual(self.roles["good_planet_alternative"], 1)
        self.assertEqual(self.roles["good_planet_override"], 1)
        for x in (
            "benevolent by nature",
            "Dignities of a good Planet",
            "naturally he is maleficall",
        ):
            self.assertIn(x, self.text())

    def test_07_lawful_outcome_also_requires_no_bad_aspects(self):
        self.assertEqual(self.roles["lawful_condition"], 2)
        self.assertEqual(self.roles["lawful_result"], 1)
        self.assertIn("doe not partake in any evill aspect with the malevolent", self.text())

    def test_08_bad_planet_and_lack_of_benefic_correspondence(self):
        self.assertEqual(self.roles["indirect_condition"], 2)
        self.assertEqual(self.roles["indirect_result"], 1)
        self.assertIn("no correspondency", self.text())

    def test_09_different_weaknesses_retrograde_combust_peregrine(self):
        modified = [
            r["original_anchor_not_diplomatic"]
            for r in self.r["rules"]
            if r["role"] == "indirect_modifier"
        ]
        self.assertEqual(len(modified), 4)
        self.assertTrue(any(s == "Retrograde" for s in modified))
        self.assertTrue(any(s == "Combust" for s in modified))
        self.assertTrue(any(s == "Peregrine" for s in modified))

    def test_10_both_lawful_and_indirect_same_chart_possible(self):
        self.assertEqual(self.roles["mixed_result"], 1)
        self.assertIn("lawfull courses", self.text())
        self.assertIn("indirect", self.text())

    def test_11_natural_benefic_or_malefic_reversals(self):
        self.assertEqual(self.roles["indirect_reverse"], 2)
        self.assertEqual(self.roles["indirect_intensifier"], 2)
        self.assertEqual(self.roles["indirect_claim"], 2)

    def test_12_all_four_explicit_method_dimensions(self):
        self.assertEqual(self.roles["method_dimension"], 4)
        t = self.text()
        for condition in (
            "nature of the Significator",
            "nature of the Signe",
            "not being Combust",
            "not Retrograde",
        ):
            self.assertIn(condition, t)

    def test_13_mixing_and_majority_not_calibrated(self):
        self.assertEqual(self.roles["judgment_discretion"], 1)
        self.assertEqual(self.roles["corroboration_rule"], 2)
        self.assertIn("plurality of testimonies", self.text())

    def test_14_jupiter_saturn_worked_example_not_proof(self):
        self.assertEqual(self.roles["worked_case"], 3)
        self.assertEqual(self.roles["worked_outcome"], 1)
        self.assertEqual(self.roles["worked_exception"], 1)
        self.assertEqual(self.roles["worked_source"], 1)
        text = self.text()
        for keyword in ("Jupiter", "Saturn", "Square", "Servant"):
            self.assertIn(keyword, text)

    def test_15_timing_has_multiple_competing_routes(self):
        roles = Counter(x["role"] for x in self.r["rules"])
        self.assertGreaterEqual(roles["timing_direction"], 3)
        self.assertEqual(roles["revolution_alternative"], 2)
        self.assertEqual(roles["timing_method"], 2)
        self.assertEqual(roles["timing_scope"], 1)

    def test_16_timing_or_near_ambiguity(self):
        t = self.text()
        self.assertIn("neer that time", t)
        self.assertIn("Converse and Direct", t)

    def test_17_moderation_conditions_and_life_outcomes(self):
        self.assertEqual(self.roles["benefic_impairment"], 1)
        self.assertEqual(self.roles["malefic_mitigation"], 1)
        self.assertEqual(self.roles["moderation_rule"], 1)
        self.assertEqual(self.roles["moderation_timing"], 1)

    def test_18_new_durability_chapter_navigation_not_substantive(self):
        nav = [r["id"] for r in self.r["rules"] if r["role"] == "next_chapter_navigation"]
        self.assertEqual(nav, ["R7050", "R7051"])
        self.assertEqual(self.r["substantive_historical_annotations"], 55)

    def test_19_ethical_legal_claims_not_a_real_person_prediction(self):
        self.assertFalse(self.limits["person_level_moral_predictions_authorized"])
        self.assertEqual(self.accept["actual_ethical_or_criminal_outcomes_validated"], 0)
        self.assertEqual(self.r["verified_criminality_or_lawfulness_predictions"], 0)
        for row in self.r["rules"]:
            self.assertFalse(row["actual_criminal_or_ethical_classification_validated"])
            self.assertFalse(row["real_person_legal_allegation_authorized"])
            self.assertFalse(row["independent_human_financial_accuracy_validated"])

    def test_20_no_runtime_and_no_diplomatic_claim(self):
        self.assertFalse(self.r["full_diplomatic_transcription"])
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        self.assertGreaterEqual(len(self.limits["issues"]), 15)

    def test_21_sha_and_total_chapters_checkpoint(self):
        self.assertEqual(self.accept["prior_lilly"], 6994)
        self.assertEqual(self.accept["lilly_if_published"], 7051)
        self.assertEqual(self.accept["combined_if_published"], 8117)
        self.assertEqual(sha(B / "RULES.json"), self.accept["rules_sha256"])


if __name__ == "__main__":
    unittest.main()
