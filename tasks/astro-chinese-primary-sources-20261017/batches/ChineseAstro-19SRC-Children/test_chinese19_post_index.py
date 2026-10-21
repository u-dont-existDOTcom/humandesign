#!/usr/bin/env python3
"""Independent post-index regression for historical Chinese V19 source append."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import unittest
from zipfile import ZipFile

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V18.json"
NEW=T/"CHINESE_SOURCE_AUDIT_INDEX_V19.json"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
NOTES=B/"ZIWEI_CHILDREN_34_SOURCE_NOTES_V1.json"
WIT=B/"SOURCE_CHILDREN_34_EXACT_OFFSET_WITNESS_V1.json"
EXCERPT=B/"SOURCE_1963110_CHILDREN_EXACT_EXCERPT.txt"
OLD_SHA="d3bdefc69a441140b9b16ef82bd10aad786a3d31e9919e5baec821fbe009e9eb"
NEW_SHA="52c5d51a281d5e641d2e029af81929e7a327d04eb5e1b510534d45b78c27fcb2"
WEST_SHA="c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8"


def sha(p:Path)->str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p:Path)->dict:
    return json.loads(p.read_text(encoding="utf-8"))


class OriginalChineseV19Canonical(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old=load(OLD);cls.new=load(NEW)
        cls.receipt=load(B/"CANONICAL_PREPARE_RECEIPT_20261021.json")
        cls.archive=load(B/"SOURCE_RELEASE_RECEIPT_20261021.json")
        cls.source=load(NOTES)

    def test_old_and_new_index_SHA_anchored(self):
        self.assertEqual(sha(OLD),OLD_SHA)
        self.assertEqual(sha(NEW),NEW_SHA)
        self.assertEqual(self.new["prior_index_sha256"],OLD_SHA)
        self.assertEqual(self.new["prior_index"],"CHINESE_SOURCE_AUDIT_INDEX_V18.json")

    def test_new_total_and_system_counts(self):
        self.assertEqual(self.new["sum_source_annotations"],1038)
        self.assertEqual(self.new["original_chinese_source_anchors_checked_against_revision"],966)
        self.assertEqual([(i["accepted_source_annotations"],i["next_id"]) for i in self.new["systems"]],
                         [(210,"BZI-R0211"),(828,"ZWD-R0829")])

    def test_previous_BaZi_unchanged(self):
        self.assertEqual(self.new["systems"][0],self.old["systems"][0])
        self.assertEqual(self.new["systems"][0]["current_ids"],"BZI-R0001–BZI-R0210")

    def test_previous_source_batches_unchanged(self):
        self.assertEqual(self.new["accepted_batches"][:-1],self.old["accepted_batches"])
        self.assertEqual(self.new["systems"][1]["source_files"][:-1],
                         self.old["systems"][1]["source_files"])
        self.assertEqual(self.new["accepted_batches"][-1]["id"],"ChineseAstro-19SRC-Children")

    def test_new_source_provenance_counts_and_ids(self):
        row=self.new["accepted_batches"][-1]
        self.assertEqual((row["start"],row["end"],row["added_ziwei_source_annotations"]),
                         ("ZWD-R0795","ZWD-R0828",34))
        self.assertEqual((row["source_method_preamble_lines"],row["source_wrapped_continuation_lines"],
                          row["source_historical_star_or_combination_lines"],
                          row["next_wealth_navigation_only"]),(4,4,24,1))
        self.assertEqual(row["source_original_codepoint_range"],[39218,40563])
        self.assertEqual(row["next_original_source_heading"],"===五财帛===")

    def test_source_note_and_witness_SHA_match_append(self):
        row=self.new["accepted_batches"][-1]
        self.assertEqual(row["rules_sha256"],sha(NOTES))
        self.assertEqual(row["witness_sha256"],sha(WIT))
        self.assertEqual(row["original_excerpt_sha256"],sha(EXCERPT))
        self.assertEqual(len(self.source["records"]),34)

    def test_exact_old_Western_source_still_unchanged(self):
        self.assertEqual(sha(WEST),WEST_SHA)
        self.assertEqual((B/"recovery/WESTERN_B07bc_BEFORE_19.json").read_bytes(),
                         WEST.read_bytes())

    def test_recovery_of_original_V18_and_current_state(self):
        self.assertEqual(sha(B/"recovery/CHINESE_V18_BEFORE_19.json"),OLD_SHA)
        earlier=(B/"recovery/CHINESE_CURRENT_BEFORE_19.md").read_text(encoding="utf-8")
        current=(ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md").read_text(encoding="utf-8")
        self.assertIn(earlier,current)
        self.assertIn("Zi Wei828 =1038",current)
        self.assertIn("ZWD-R0829",current)

    def test_archive_CRC_SHA_and_independent_tests(self):
        self.assertTrue(self.archive["ZIP_CRC_verified"])
        self.assertTrue(self.archive["all_members_SHA256_and_bytes_verified"])
        self.assertTrue(self.archive["cold_extracted_member_checks_complete"])
        self.assertEqual(self.archive["independent_cold_source_tests_green"],13)
        p=Path(self.archive["local_archive_path"])
        self.assertTrue(p.is_file())
        self.assertEqual(sha(p),self.archive["archive_sha256"])
        with ZipFile(p) as z:
            self.assertIsNone(z.testzip())
            manifest=json.loads(z.read("SOURCE_ARCHIVE_MANIFEST.json"))
            self.assertEqual(len(manifest["members"]),14)
            for rel,proof in manifest["members"].items():
                self.assertEqual(len(z.read(rel)),proof["size_bytes"])
                self.assertEqual(hashlib.sha256(z.read(rel)).hexdigest(),proof["sha256"])

    def test_no_empirical_or_runtime_promotion(self):
        self.assertEqual((self.new["independently_validated_real_human_claims"],
                          self.new["runtime_promotions"]),(0,0))
        self.assertFalse(self.new["ziwei_complete_natal_calendar_engine_verified"])
        self.assertFalse(self.new["full_ziwei_original_text_collation_finished"])
        self.assertFalse(self.new["accepted_batches"][-1]["ancient_Ming_imprint_critical_text_authenticated"])
        self.assertEqual((self.receipt["real_human_blind_predictions"],
                          self.receipt["runtime_astrology_promotions"]),(0,0))


if __name__=="__main__":
    unittest.main()
