"""Integrity tests: original first-edition sibling harmony historical rules.

These tests do not establish real-family predictions or astrological effectiveness.
"""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def load(name):
    return json.loads((B / name).read_text())


class OriginalSiblingHarmony(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = load("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.rules = load("RULES.json")
        cls.mapping = load("SOURCE_TO_RECORD_MAP.json")
        cls.images = load("ORIGINAL_SOURCE_WITNESS.json")
        cls.limits = load("UNRESOLVED_SOURCE_LIMITS.json")
        cls.accept = load("ACCEPTANCE.json")
        cls.roles = Counter(r["role"] for r in cls.rules["rules"])
        cls.anchors = " ".join(r["source_anchor_not_diplomatic"] for r in cls.rules["rules"])

    def test_01_original_images_sha256(self):
        for info in self.images["images"].values():
            p = B / info["file"]
            raw = p.read_bytes()
            self.assertEqual(len(raw), info["bytes"])
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(hashlib.sha256(raw).hexdigest(), info["sha256"])

    def test_02_source_pagination_and_next_chapter(self):
        self.assertEqual(list(self.images["images"]), ["601", "602"])
        self.assertEqual(
            [v["printed_folio"] for v in self.images["images"].values()],
            ["567", "568"],
        )
        self.assertEqual(self.images["source_body_frame"], 601)
        self.assertEqual(self.images["next_chapter_heading_frame"], 602)

    def test_03_consecutive_record_ids(self):
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]],
            list(range(7209, 7253)),
        )
        self.assertEqual(len({r["id"] for r in self.rules["rules"]}), 44)

    def test_04_every_source_claim_reversibly_mapped(self):
        refs = []
        for source, m in zip(self.source["groups"], self.mapping["source_groups"], strict=True):
            self.assertEqual(source["source_span"], m["source_span"])
            self.assertEqual(source["original_pdf_frames"], m["pdf_pages"])
            each = [c["id"] for c in source["claims"]]
            self.assertEqual(each, m["mapped_ids"])
            refs.extend(each)
        self.assertEqual(refs, [r["id"] for r in self.rules["rules"]])
        self.assertEqual(self.mapping["source_group_count"], 8)

    def test_05_good_bad_and_no_aspect_compete(self):
        for role in (
            "benevolent_aspect",
            "hard_aspect",
            "absent_aspect",
            "hard_result",
            "absent_result",
        ):
            self.assertEqual(self.roles[role], 1)
        self.assertIn("Square or Opposition", self.anchors)
        self.assertIn("no aspect at all", self.anchors)

    def test_06_author_claim_of_no_failures_not_evidence(self):
        self.assertEqual(self.roles["self_report"], 1)
        line = next(r for r in self.rules["rules"] if r["role"] == "self_report")
        self.assertIn("I usually doe find", line["source_anchor_not_diplomatic"])
        self.assertIn("without presenting independent", line["historical_only_meaning"])

    def test_07_three_malefic_alternatives_source_separate(self):
        for role in ("saturn_third", "mars_third", "south_node_third"):
            self.assertEqual(self.roles[role], 1)
        self.assertEqual(self.roles["conflict_result"], 1)

    def test_08_mars_as_third_ruler_requires_trine_and_reception(self):
        for role in (
            "mars_third_ruler",
            "mars_trine",
            "mars_reception",
            "mars_result",
            "mars_contrast",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_09_concord_four_other_conditions(self):
        self.assertEqual(self.roles["concord_condition"], 2)
        self.assertEqual(self.roles["concord_alternative"], 2)
        self.assertEqual(self.roles["concord_result"], 2)

    def test_10_kin_profit_and_losses_are_compound(self):
        self.assertEqual(self.roles["benefit_condition"], 2)
        self.assertEqual(self.roles["benefit_result"], 1)
        self.assertEqual(self.roles["harm_condition"], 2)
        self.assertEqual(self.roles["harm_result"], 1)

    def test_11_three_ascending_sign_groups_preserved(self):
        self.assertEqual(self.roles["asc_sign"], 3)
        self.assertEqual(self.roles["asc_sign_exception"], 1)
        for x in ("Aries or Libra", "Cancer or Scorpio", "Leo or Aquarius"):
            self.assertIn(x, self.anchors)

    def test_12_mercury_mars_and_neighbors_preserved(self):
        self.assertEqual(self.roles["mercury_mars"], 1)
        self.assertEqual(self.roles["mercury_result"], 1)
        self.assertEqual(self.roles["generalization"], 2)

    def test_13_following_sibling_number_section_is_navigation(self):
        self.assertEqual(
            [r["id"] for r in self.rules["rules"] if r["role"] == "next_chapter_navigation"],
            ["R7251", "R7252"],
        )
        self.assertEqual(self.rules["substantive_historical_records"], 42)

    def test_14_zero_independent_validation_and_diplomatic_status(self):
        self.assertFalse(self.rules["full_diplomatic_transcription"])
        self.assertEqual(self.rules["empirical_validations"], 0)
        self.assertEqual(self.rules["runtime_promotions"], 0)
        self.assertGreaterEqual(len(self.limits["issues"]), 12)
        for r in self.rules["rules"]:
            self.assertFalse(r["verified_family_relationship_prediction"])
            self.assertFalse(r["clinical_or_personal_accusation_authorized"])
            self.assertFalse(r["runtime_rule_promoted"])

    def test_15_corpus_total_rules_hash(self):
        self.assertEqual(self.accept["previous_lilly"], 7208)
        self.assertEqual(self.accept["lilly_if_published"], 7252)
        self.assertEqual(self.accept["combined_if_published"], 8318)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.accept["rules_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
