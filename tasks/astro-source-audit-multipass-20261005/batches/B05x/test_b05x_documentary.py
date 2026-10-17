"""Original 1647 Lilly printed mother chapter documentary tests: NOT medicine."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text())


class FirstEditionMotherHistory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = j("RULES.json")
        cls.m = j("SOURCE_TO_RECORD_MAP.json")
        cls.w = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.u = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.accept = j("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])
        cls.text = " ".join(x["anchor_not_diplomatic"] for x in cls.r["rules"])

    def test_01_all_primary_images_cryptographic_hash(self):
        for p in self.w["images"].values():
            f = B / p["file"]
            data = f.read_bytes()
            self.assertEqual(data[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(data), p["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), p["sha256"])

    def test_02_physical_page_order_and_next_chapter(self):
        self.assertEqual(list(self.w["images"]), ["604", "605", "606"])
        self.assertEqual(
            [p["printed_folio"] for p in self.w["images"].values()],
            ["570", "571", "572"],
        )
        self.assertEqual(self.w["body_frames"], [604, 605])
        self.assertEqual(self.w["next_printed_CXXIII_heading_frame"], 606)

    def test_03_contiguous_source_ids(self):
        self.assertEqual(
            [row["record_number"] for row in self.r["rules"]],
            list(range(7358, 7411)),
        )
        self.assertEqual(len({x["id"] for x in self.r["rules"]}), 53)

    def test_04_all_source_groups_bidirectionally_mapped(self):
        ids = []
        for s, m in zip(self.a["groups"], self.m["source_groups"], strict=True):
            self.assertEqual(s["source_span"], m["source_span"])
            self.assertEqual(s["original_pdf_frames"], m["original_pdf_frames"])
            original_ids = [x["id"] for x in s["claims"]]
            self.assertEqual(m["mapped_record_ids"], original_ids)
            ids.extend(original_ids)
        self.assertEqual(ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(len(self.m["source_groups"]), 11)

    def test_05_mother_four_sources_and_day_night_separate(self):
        self.assertEqual(self.roles["maternal_indicator"], 3)
        self.assertEqual(self.roles["maternal_indicator_day"], 1)
        self.assertEqual(self.roles["maternal_indicator_night"], 1)
        self.assertIn("tenth house", self.text)
        self.assertIn("Venus in a diurnall", self.text)
        self.assertIn("Moon in a nocturnall", self.text)

    def test_06_majority_favorable_and_family_background(self):
        self.assertEqual(self.roles["favorable_condition"], 2)
        self.assertEqual(self.roles["favorable_baseline"], 1)
        self.assertEqual(self.roles["favorable_time"], 1)
        self.assertIn("quality of the Family", self.text)

    def test_07_negative_moon_and_relative_mother_father(self):
        self.assertEqual(self.roles["unfavorable_condition"], 1)
        self.assertEqual(self.roles["unfavorable_result"], 2)
        self.assertEqual(self.roles["comparative_method"], 1)
        self.assertEqual(self.roles["comparative_target"], 1)

    def test_08_benefics_and_malefics_distinct(self):
        self.assertEqual(self.roles["benefic_source"], 1)
        self.assertEqual(self.roles["malefic_source"], 1)
        self.assertEqual(self.roles["malefic_detail"], 2)

    def test_09_orientation_harm_life_vs_estate_kept(self):
        self.assertEqual(self.roles["orientation_method"], 1)
        self.assertEqual(self.roles["orientation_harm"], 1)
        self.assertEqual(self.roles["orientation_estate"], 1)
        self.assertTrue(any("grammatical" in q for q in self.u["issues"]))

    def test_10_negative_maternal_lifespan_combination(self):
        self.assertEqual(self.roles["longevity_condition"], 2)
        self.assertEqual(self.roles["longevity_result"], 1)
        self.assertIn("tenth or fourth", self.text)

    def test_11_favorable_moon_requires_multiple_criteria(self):
        self.assertEqual(self.roles["long_life"], 4)
        self.assertEqual(self.roles["long_life_result"], 1)
        self.assertIn("Venus Sextile or Trine", self.text)
        self.assertIn("Jupiter doe aspect", self.text)

    def test_12_low_status_mother_servant_stereotype(self):
        self.assertEqual(self.roles["status_condition"], 2)
        self.assertEqual(self.roles["status_result"], 1)
        self.assertIn("one in the twelfth the other in the sixth", self.text)

    def test_13_multiple_malefic_maternal_health_claims(self):
        self.assertEqual(self.roles["malefic_harm"], 1)
        self.assertEqual(self.roles["motion_qualifier"], 1)
        self.assertEqual(self.roles["short_life_result"], 1)
        self.assertEqual(self.roles["oriental_diseases"], 1)
        self.assertEqual(self.roles["occidental_diseases"], 1)
        self.assertEqual(self.roles["chronic_disease"], 1)

    def test_14_original_pre_modern_organs_not_diagnoses(self):
        self.assertIn("imposthumation in Matrix Reines", self.text)
        self.assertIn("Chollick", self.text)
        self.assertFalse(self.u["original_diplomatic_transcription_complete"])

    def test_15_next_printed_childbirth_chapter_not_swallowed(self):
        self.assertEqual(
            [r["id"] for r in self.r["rules"] if r["role"] == "next_chapter_navigation"],
            ["R7409", "R7410"],
        )
        self.assertEqual(self.r["substantive_historical_clauses"], 51)
        self.assertEqual(self.accept["next_printed_chapter"], "CXXIII")

    def test_16_zero_human_health_mortality_accuracy(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["medical_outcomes_validated"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for row in self.r["rules"]:
            self.assertFalse(row["independent_human_maternal_health_validated"])
            self.assertFalse(row["validated_maternal_wealth_or_ancestry"])
            self.assertFalse(row["reliable_human_birth_death_prediction"])
            self.assertFalse(row["clinical_or_moral_actions_authorized"])
            self.assertFalse(row["runtime_model_promoted"])

    def test_17_record_count_and_sha256(self):
        self.assertEqual(self.accept["previous_lilly"], 7357)
        self.assertEqual(self.accept["lilly_if_published"], 7410)
        self.assertEqual(self.accept["combined_if_published"], 8476)
        h = hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest()
        self.assertEqual(h, self.accept["rules_sha256"])


if __name__ == "__main__":
    unittest.main()
