"""Original Lilly maternal childbirth historical source checks; not medical accuracy."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text())


class HistoricChildbirthSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = read("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = read("RULES.json")
        cls.m = read("SOURCE_TO_RECORD_MAP.json")
        cls.w = read("ORIGINAL_SOURCE_WITNESS.json")
        cls.l = read("UNRESOLVED_SOURCE_LIMITS.json")
        cls.acc = read("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])
        cls.text = " ".join(x["anchor_not_diplomatic"] for x in cls.r["rules"])

    def test_01_original_images_sha_bytes(self):
        for info in self.w["images"].values():
            file = B / info["file"]
            data = file.read_bytes()
            self.assertEqual(data[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(data), info["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), info["sha256"])

    def test_02_folio_and_same_page_following_chapter(self):
        self.assertEqual(list(self.w["images"]), ["606", "607", "608"])
        self.assertEqual(
            [x["printed_folio"] for x in self.w["images"].values()],
            ["572", "573", "574"],
        )
        self.assertEqual(self.w["childbirth_body_frame"], 606)
        self.assertEqual(self.w["following_printed_CXXIIII_heading_frame"], 606)

    def test_03_record_numbers_no_gaps(self):
        self.assertEqual([x["record_number"] for x in self.r["rules"]], list(range(7411, 7441)))
        self.assertEqual(len({x["id"] for x in self.r["rules"]}), 30)

    def test_04_source_mapping_all_groups(self):
        ids = []
        for source, mapping in zip(self.a["groups"], self.m["source_groups"], strict=True):
            self.assertEqual(source["source_span"], mapping["source_span"])
            self.assertEqual(source["original_pdf_frames"], mapping["original_pdf_frames"])
            expected = [x["id"] for x in source["claims"]]
            self.assertEqual(expected, mapping["mapped_ids"])
            ids.extend(expected)
        self.assertEqual(ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(self.m["source_groups_count"], 7)

    def test_05_oblique_requires_bad_aspect_or_node(self):
        self.assertEqual(self.roles["oblique_signs"], 1)
        self.assertEqual(self.roles["oblique_location"], 1)
        self.assertEqual(self.roles["oblique_malefic_aspect"], 2)
        self.assertEqual(self.roles["oblique_node"], 1)

    def test_06_long_ascent_benefic_or_node_alternative(self):
        for x in ("long_signs", "long_benefic", "long_node", "easy_result"):
            self.assertEqual(self.roles[x], 1)

    def test_07_moon_assistance_and_sex_sign_diff(self):
        self.assertEqual(self.roles["moon_assistance"], 2)
        self.assertEqual(self.roles["sex_sign"], 1)
        self.assertEqual(self.roles["sex_male"], 1)
        self.assertEqual(self.roles["sex_female"], 1)
        self.assertIn("Leo Libra Sagittarius", self.text)
        self.assertIn("Cancer Virgo Scorpio", self.text)

    def test_08_twelfth_house_slow_birth_vs_danger(self):
        self.assertEqual(self.roles["twelfth_malefics"], 1)
        self.assertEqual(self.roles["slow_birth"], 1)
        self.assertEqual(self.roles["maternal_danger"], 1)

    def test_09_oblique_moon_three_movement_choices(self):
        self.assertEqual(self.roles["moon_oblique"], 1)
        self.assertEqual(self.roles["slow_planet"], 3)
        self.assertEqual(self.roles["slow_labour_result"], 1)

    def test_10_tenth_lord_eighth_mortality_hedged(self):
        self.assertEqual(self.roles["tenth_eighth"], 1)
        self.assertEqual(self.roles["maternal_mortality"], 1)
        self.assertIn("it may be doubted", self.text)

    def test_11_next_inheritance_separate_not_counted(self):
        self.assertEqual(
            [r["id"] for r in self.r["rules"] if r["role"] == "next_chapter_navigation"],
            ["R7439", "R7440"],
        )
        self.assertEqual(self.r["substantive"], 28)

    def test_12_zero_human_mortality_and_obstetric_accuracy(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["clinical_validation_successes"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        self.assertFalse(self.r["full_diplomatic_transcription"])
        self.assertFalse(self.l["medical_advice_authorized"])
        for item in self.r["rules"]:
            self.assertFalse(item["human_pregnancy_complication_validated"])
            self.assertFalse(item["human_maternal_mortality_predicted"])
            self.assertFalse(item["human_neonatal_outcome_predicted"])
            self.assertFalse(item["runtime_model_promoted"])

    def test_13_rules_sha_and_count(self):
        self.assertEqual(self.acc["previous_lilly"], 7410)
        self.assertEqual(self.acc["lilly_if_published"], 7440)
        self.assertEqual(self.acc["combined_if_published"], 8506)
        digest = hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest()
        self.assertEqual(digest, self.acc["rules_sha256"])


if __name__ == "__main__":
    unittest.main()
