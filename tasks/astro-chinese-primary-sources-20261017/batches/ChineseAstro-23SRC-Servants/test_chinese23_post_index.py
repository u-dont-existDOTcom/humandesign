#!/usr/bin/env python3
"""Independent post-index regression for original Zi Wei Servants documentation."""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
import unittest
from zipfile import ZipFile

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT / "tasks/astro-chinese-primary-sources-20261017"
OLD = T / "CHINESE_SOURCE_AUDIT_INDEX_V22.json"
NEW = T / "CHINESE_SOURCE_AUDIT_INDEX_V23.json"
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
NOTES = B / "ZIWEI_SERVANTS_26_SOURCE_NOTES_V1.json"
WITNESS = B / "SOURCE_SERVANTS_26_OFFSET_WITNESS_V1.json"
EXCERPT = B / "SOURCE_1963110_SERVANTS_EXACT_EXCERPT.txt"
V22_SHA = "3c3d74b9f53d10e7905f026733d902511bf19f2f0f64ae34bed9f4af894bba68"
V23_SHA = "0bc5836d92c332a458a7d4a74dbb25488705344aa38df256dc721c6c5a673a0e"
WEST_SHA = "c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8"

def sha(p:Path)->str:
    return sha256(p.read_bytes()).hexdigest()
def load(p:Path)->dict:
    return json.loads(p.read_text(encoding="utf-8"))

class SourceIndexV23(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = load(OLD)
        cls.new = load(NEW)
        cls.receipt = load(B/"CANONICAL_PREPARE_RECEIPT_20261021.json")
        cls.archive = load(B/"SOURCE_RELEASE_RECEIPT_20261021.json")

    def test_previous_and_new_canonical_source_hashes(self):
        self.assertEqual(sha(OLD),V22_SHA)
        self.assertEqual(sha(NEW),V23_SHA)
        self.assertEqual(self.new["prior_index_sha256"],V22_SHA)

    def test_prior_accepted_history_not_edited(self):
        self.assertEqual(self.new["systems"][0],self.old["systems"][0])
        self.assertEqual(self.new["accepted_batches"][:-1],self.old["accepted_batches"])
        self.assertEqual(self.new["systems"][1]["source_files"][:-1],
                         self.old["systems"][1]["source_files"])

    def test_new_source_only_total_and_frontier(self):
        self.assertEqual(self.new["sum_source_annotations"],1146)
        self.assertEqual(self.new["original_chinese_source_anchors_checked_against_revision"],1074)
        self.assertEqual([(s["accepted_source_annotations"],s["next_id"]) for s in self.new["systems"]],
                         [(210,"BZI-R0211"),(936,"ZWD-R0937")])
    def test_servants_exact_historical_source_count(self):
        batch = self.new["accepted_batches"][-1]
        self.assertEqual((batch["id"],batch["start"],batch["end"],batch["added_ziwei_source_annotations"]),
                         ("ChineseAstro-23SRC-Servants","ZWD-R0911","ZWD-R0936",26))
        self.assertEqual((batch["original_heading_lines"],batch["historical_star_or_combination_lines"],
                          batch["following_Career_navigation_only"]),(1,24,1))
        self.assertEqual(batch["source_original_codepoint_range"],[43499,44429])
        self.assertTrue(batch["historical_class_servitude_stereotypes_are_unverified"])

    def test_source_notes_witness_and_excerpt_hashes(self):
        batch = self.new["accepted_batches"][-1]
        self.assertEqual(batch["rules_sha256"],sha(NOTES))
        self.assertEqual(batch["witness_sha256"],sha(WITNESS))
        self.assertEqual(batch["original_excerpt_sha256"],sha(EXCERPT))
        self.assertEqual(len(load(NOTES)["records"]),26)

    def test_older_Western_source_not_mutated(self):
        self.assertEqual(sha(WEST),WEST_SHA)
        self.assertEqual((B/"recovery/WESTERN_B07bc_BEFORE_23.json").read_bytes(),WEST.read_bytes())

    def test_original_previous_state_recoverable(self):
        self.assertEqual(sha(B/"recovery/CHINESE_V22_BEFORE_23.json"),V22_SHA)
        original = (B/"recovery/CHINESE_CURRENT_BEFORE_23.md").read_text(encoding="utf-8")
        current = (ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md").read_text(encoding="utf-8")
        self.assertIn(original,current)
        self.assertIn("ZWD-R0937",current)

    def test_portable_cold_source_archive_integrity(self):
        self.assertEqual(self.archive["cold_extracted_source_tests_green"],7)
        self.assertTrue(self.archive["all_members_SHA256_bytes_verified"])
        p=Path(self.archive["local_archive_path"])
        self.assertTrue(p.is_file())
        self.assertEqual(sha(p),self.archive["archive_SHA256"])
        with ZipFile(p) as z:
            self.assertIsNone(z.testzip())
            manifest=json.loads(z.read("SOURCE_ARCHIVE_MANIFEST.json"))
            self.assertEqual(len(manifest["members"]),15)
            for name,witness in manifest["members"].items():
                raw=z.read(name)
                self.assertEqual((sha256(raw).hexdigest(),len(raw)),
                                 (witness["sha256"],witness["bytes"]))

    def test_no_original_ancient_authenticity_or_real_human_success(self):
        self.assertFalse(self.new["full_ziwei_original_text_collation_finished"])
        self.assertFalse(self.new["ziwei_complete_natal_calendar_engine_verified"])
        self.assertFalse(self.new["accepted_batches"][-1]["original_Ming_woodblock_printing_independently_authenticated"])
        self.assertEqual((self.new["independently_validated_real_human_claims"],
                          self.new["runtime_promotions"]),(0,0))
        self.assertEqual((self.receipt["human_blind_predictive_validations"],
                          self.receipt["runtime_astrology_promotions"]),(0,0))

if __name__=="__main__":
    unittest.main()
