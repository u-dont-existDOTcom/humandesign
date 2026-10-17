"""Original Lilly first-edition alternate sibling-count and attributed Ptolemy source tests.

Structural historical-source verification only; no demographic or clinical inference.
"""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text())


class HistoricalSiblingMethodContrast(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.author = read("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = read("RULES.json")
        cls.mapping = read("SOURCE_TO_RECORD_MAP.json")
        cls.w = read("ORIGINAL_SOURCE_WITNESS.json")
        cls.limits = read("UNRESOLVED_SOURCE_LIMITS.json")
        cls.a = read("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])
        cls.text = " ".join(r["anchor_not_diplomatic"] for r in cls.r["rules"])

    def test_01_all_image_sha256_and_bytes(self):
        for img in self.w["images"].values():
            p = B / img["path"]
            data = p.read_bytes()
            self.assertEqual(data[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(data), img["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), img["sha256"])

    def test_02_source_and_next_unnumbered_folio(self):
        self.assertEqual(list(self.w["images"]), ["602", "603", "604", "605"])
        self.assertEqual(
            [i["original_printed_page"] for i in self.w["images"].values()],
            ["568", "569", "570", "571"],
        )
        self.assertEqual(self.w["body_pdf_page"], 602)
        self.assertEqual(self.w["following_unnumbered_fourth_house_pdf_page"], 603)

    def test_03_consecutive_source_records(self):
        self.assertEqual([r["record_number"] for r in self.r["rules"]], list(range(7253, 7296)))
        self.assertEqual(len({r["id"] for r in self.r["rules"]}), 43)

    def test_04_reversible_eight_group_coverage(self):
        all_refs = []
        for group, reverse in zip(
            self.author["groups"], self.mapping["source_groups"], strict=True
        ):
            self.assertEqual(group["source_span"], reverse["source_span"])
            self.assertEqual(group["original_pdf_frames"], reverse["original_pdf_frames"])
            refs = [c["id"] for c in group["clauses"]]
            self.assertEqual(refs, reverse["mapped_record_ids"])
            all_refs.extend(refs)
        self.assertEqual(all_refs, [r["id"] for r in self.r["rules"]])
        self.assertEqual(len(self.mapping["source_groups"]), 8)

    def test_05_third_house_and_lord_both_required(self):
        self.assertEqual(self.roles["sign_premise"], 1)
        self.assertEqual(self.roles["lord_premise"], 1)
        self.assertEqual(self.roles["positive_result"], 1)
        self.assertEqual(self.roles["negative_alternative"], 1)

    def test_06_brothers_sisters_by_count_and_sign_separated(self):
        for role in ("count_rule", "count_masculine", "count_feminine"):
            self.assertEqual(self.roles[role], 1)
        for text in ("Masculine Signes", "feminine Signes"):
            self.assertIn(text, self.text)

    def test_07_aspect_based_survival_opposites(self):
        self.assertEqual(self.roles["survival_condition"], 1)
        self.assertEqual(self.roles["survival_favour"], 1)
        self.assertEqual(self.roles["survival_adverse"], 1)

    def test_08_mars_combust_and_younger_sibling_conditional(self):
        for role in ("mars_combust", "mars_few", "mars_younger"):
            self.assertEqual(self.roles[role], 1)
        self.assertIn("if any be", self.text)

    def test_09_third_ruler_combust_and_sun_jupiter_ambiguous(self):
        for role in ("third_ruler_combust", "sun_third", "sun_jupiter_opposition", "few_deaths"):
            self.assertEqual(self.roles[role], 1)
        row = next(r for r in self.r["rules"] if r["role"] == "sun_jupiter_opposition")
        self.assertEqual(row["source_qualification"], "ambiguous")

    def test_10_firstborn_or_best_life_alternative(self):
        for role in (
            "first_house_planet",
            "birth_order_result",
            "better_life_alternative",
            "birth_welfare_result",
        ):
            self.assertEqual(self.roles[role], 1)
        self.assertIn("either first borne", self.text)

    def test_11_angular_and_superior_inferior_conjunctions(self):
        for role in (
            "angle_condition",
            "angle_dignity",
            "superior_ruler",
            "superior_third",
            "inferior_ruler",
            "inferior_first",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_12_ptolemy_all_attributed_factors_preserved(self):
        for role in (
            "attribution",
            "ptolemy_mid",
            "ptolemy_day",
            "ptolemy_night",
            "ptolemy_house",
            "ptolemy_benefic",
            "ptolemy_many",
        ):
            self.assertEqual(self.roles[role], 1)
        for text in ("mid-heaven", "diurnally from Venus", "nocturnally from Moon", "eleventh"):
            self.assertIn(text, self.text)

    def test_13_lilly_same_mother_scope_and_retort_preserved(self):
        self.assertEqual(self.roles["ptolemy_scope"], 2)
        for role in ("own_method", "method_popularity", "opponent_isolation", "latin_maxim"):
            self.assertEqual(self.roles[role], 1)
        self.assertIn("same Mother", self.text)

    def test_14_next_unumbered_fourth_house_separate(self):
        self.assertEqual(
            [r["id"] for r in self.r["rules"] if r["role"] == "next_section_navigation"],
            ["R7294", "R7295"],
        )
        self.assertEqual(self.r["substantive_historical_claims"], 41)

    def test_15_no_birth_sex_longevity_or_ptolemy_validation(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["actual_sibling_births_or_deaths_validated"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        self.assertFalse(self.r["full_diplomatic_transcription"])
        for row in self.r["rules"]:
            self.assertFalse(row["independent_sibling_birth_count_validated"])
            self.assertFalse(row["human_fertility_or_sex_prediction_validated"])
            self.assertFalse(row["human_longevity_or_death_prediction_validated"])
            self.assertFalse(row["original_ptolemy_text_independently_verified"])
            self.assertFalse(row["runtime_model_promoted"])

    def test_16_conservation_records_and_sha(self):
        self.assertEqual(self.a["previous_lilly"], 7252)
        self.assertEqual(self.a["lilly_if_published"], 7295)
        self.assertEqual(self.a["combined_if_published"], 8361)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.a["rules_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
