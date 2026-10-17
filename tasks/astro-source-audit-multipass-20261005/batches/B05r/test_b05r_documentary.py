"""Integrity/coverage tests for original Lilly unnumbered third-house introduction."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text())


class OriginalSiblingIntro(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = j("RULES.json")
        cls.m = j("SOURCE_TO_RECORD_MAP.json")
        cls.w = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.l = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.rec = j("ACCEPTANCE.json")

    def test_01_primary_image_sha256_and_size(self):
        for f in self.w["source_images"].values():
            path = B / f["file"]
            data = path.read_bytes()
            self.assertEqual(len(data), f["bytes"])
            self.assertEqual(data[:2], bytes.fromhex("ffd8"))
            self.assertEqual(hashlib.sha256(data).hexdigest(), f["sha256"])

    def test_02_original_source_folio_and_next_chapter(self):
        self.assertEqual(list(self.w["source_images"]), ["598", "599", "600"])
        self.assertEqual(
            [x["printed_folio"] for x in self.w["source_images"].values()],
            ["564", "565", "566"],
        )
        self.assertEqual(self.w["intro_pdf_frame"], 598)
        self.assertEqual(self.w["numbered_CXVIII_heading_pdf_frame"], 598)

    def test_03_unique_consecutive_records(self):
        self.assertEqual(
            [r["record_number"] for r in self.r["rules"]],
            list(range(7127, 7139)),
        )
        self.assertEqual(len({r["id"] for r in self.r["rules"]}), 12)

    def test_04_reversible_five_source_groups(self):
        all_ids = []
        for authored, mapped in zip(self.a["groups"], self.m["source_groups"], strict=True):
            self.assertEqual(authored["source_span"], mapped["source_span"])
            self.assertEqual(authored["original_pdf_frames"], mapped["original_pdf_frames"])
            ids = [x["id"] for x in authored["claims"]]
            self.assertEqual(ids, mapped["mapped_record_ids"])
            all_ids.extend(ids)
        self.assertEqual(all_ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(len(self.m["source_groups"]), 5)

    def test_05_firstborn_nativity_and_after_birth_scoping(self):
        anchors = " ".join(x["anchor_not_diplomatic"] for x in self.r["rules"])
        self.assertIn("first borne", anchors)
        self.assertIn("after the Birth", anchors)
        self.assertTrue(any("subsequent siblings" in s for s in self.l["issues"]))

    def test_06_firstborn_unavailable_fallback(self):
        anchors = " ".join(x["anchor_not_diplomatic"] for x in self.r["rules"])
        self.assertIn("cannot be had", anchors)
        self.assertEqual(sum(x["role"] == "fallback" for x in self.r["rules"]), 1)

    def test_07_three_distinct_sibling_questions(self):
        agenda = [x["anchor_not_diplomatic"] for x in self.r["rules"] if x["role"] == "agenda"]
        self.assertEqual(len(agenda), 3)
        self.assertTrue(any("Whether" in x for x in agenda))
        self.assertTrue(any("condition" in x for x in agenda))
        self.assertTrue(any("amity" in x for x in agenda))

    def test_08_intro_does_not_swallow_printed_CXVIII(self):
        nav = [x["id"] for x in self.r["rules"] if x["role"] == "next_chapter_navigation"]
        self.assertEqual(nav, ["R7137", "R7138"])
        self.assertEqual(self.r["following_CXVIII_pdf_frame"], 598)
        self.assertEqual(self.rec["numbered_chapters_added"], 0)

    def test_09_zero_real_family_outcomes_or_runtime(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        self.assertFalse(self.r["complete_diplomatic_transcription"])
        for x in self.r["rules"]:
            self.assertFalse(x["validated_actual_sibling_number"])
            self.assertFalse(x["validated_sibling_relationship_quality"])
            self.assertFalse(x["promoted_to_runtime_model"])

    def test_10_source_hash_and_total_arithmetic(self):
        p = B / "RULES.json"
        self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), self.rec["source_sha256"])
        self.assertEqual(self.rec["previous_lilly"], 7126)
        self.assertEqual(self.rec["lilly_if_published"], 7138)
        self.assertEqual(self.rec["combined_if_published"], 8204)


if __name__ == "__main__":
    unittest.main()
