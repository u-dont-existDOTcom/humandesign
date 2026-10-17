"""Source coverage and integrity for original Lilly CXIX sibling condition.

This test does not assess actual sibling health, wealth or social outcomes.
"""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text())


class SiblingConditionSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = read("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = read("RULES.json")
        cls.map = read("SOURCE_TO_RECORD_MAP.json")
        cls.w = read("ORIGINAL_SOURCE_WITNESS.json")
        cls.limits = read("UNRESOLVED_SOURCE_LIMITS.json")
        cls.receipt = read("ACCEPTANCE.json")
        cls.roles = Counter(row["role"] for row in cls.r["rules"])

    def anchors(self):
        return " ".join(row["source_anchor_not_diplomatic"] for row in self.r["rules"])

    def test_01_original_image_sha(self):
        for image in self.w["images"].values():
            path = B / image["file"]
            contents = path.read_bytes()
            self.assertEqual(contents[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(contents), image["bytes"])
            self.assertEqual(hashlib.sha256(contents).hexdigest(), image["sha256"])

    def test_02_edition_folio_sequence(self):
        self.assertEqual(list(self.w["images"]), ["600", "601", "602"])
        self.assertEqual(
            [x["printed_folio"] for x in self.w["images"].values()],
            ["566", "567", "568"],
        )

    def test_03_original_body_and_boundary(self):
        self.assertEqual(self.w["body_pdf_frame"], 600)
        self.assertEqual(self.w["next_printed_chapter_CXX_frame"], 601)
        self.assertEqual(self.w["next_next_printed_CXXI_frame"], 602)

    def test_04_consecutive_record_ids(self):
        self.assertEqual([x["record_number"] for x in self.r["rules"]], list(range(7187, 7209)))
        self.assertEqual(len({x["id"] for x in self.r["rules"]}), 22)

    def test_05_reverse_map_exact_coverage(self):
        refs = []
        for authored, mapped in zip(self.source["groups"], self.map["source_groups"], strict=True):
            self.assertEqual(authored["source_span"], mapped["source_span"])
            self.assertEqual(authored["original_pdf_pages"], mapped["pdf_frames"])
            these = [x["id"] for x in authored["claims"]]
            self.assertEqual(these, mapped["record_ids"])
            refs.extend(these)
        self.assertEqual(refs, [x["id"] for x in self.r["rules"]])
        self.assertEqual(len(self.map["source_groups"]), 6)

    def test_06_majority_strong_plus_multiple_claim_types(self):
        self.assertEqual(self.roles["positive_condition"], 1)
        self.assertEqual(self.roles["positive_result"], 4)
        for phrase in ("greater part", "long life", "honour and Wealth"):
            self.assertIn(phrase, self.anchors())

    def test_07_weak_and_mixed_result_separate(self):
        self.assertEqual(self.roles["negative_condition"], 1)
        self.assertEqual(self.roles["negative_result"], 1)
        self.assertEqual(self.roles["mixed_condition"], 1)
        self.assertEqual(self.roles["mixed_result"], 2)

    def test_08_favorable_sister_comparison_compound(self):
        self.assertEqual(self.roles["comparison_context"], 1)
        self.assertEqual(self.roles["sister_configuration"], 2)
        self.assertEqual(self.roles["sister_result"], 1)
        self.assertIn("Moon well fortified", self.anchors())
        self.assertIn("Mars prove weak", self.anchors())

    def test_09_favorable_brother_comparison_compound(self):
        self.assertEqual(self.roles["brother_configuration"], 2)
        self.assertEqual(self.roles["brother_result"], 2)
        self.assertIn("Mars be strong", self.anchors())
        self.assertIn("Moon weak and afflicted", self.anchors())

    def test_10_next_chapter_navigation_only(self):
        nav = [r["id"] for r in self.r["rules"] if r["role"] == "next_chapter_navigation"]
        self.assertEqual(nav, ["R7207", "R7208"])
        self.assertEqual(self.r["substantive_historical_records"], 20)

    def test_11_no_validated_social_or_longevity_predictions(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        self.assertEqual(self.r["independent_sibling_fortune_validations"], 0)
        for r in self.r["rules"]:
            self.assertFalse(r["actual_human_sibling_outcome_validated"])
            self.assertFalse(r["sibling_longevity_validated"])
            self.assertFalse(r["clinical_or_social_advice_authorized"])
            self.assertFalse(r["runtime_model_promoted"])

    def test_12_source_not_diplomatic(self):
        self.assertFalse(self.r["full_diplomatic_transcription"])
        self.assertGreaterEqual(len(self.limits["issues"]), 9)

    def test_13_corpus_and_rules_checksum(self):
        self.assertEqual(self.receipt["previous_lilly"], 7186)
        self.assertEqual(self.receipt["lilly_if_published"], 7208)
        self.assertEqual(self.receipt["combined_if_published"], 8274)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.receipt["rules_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
