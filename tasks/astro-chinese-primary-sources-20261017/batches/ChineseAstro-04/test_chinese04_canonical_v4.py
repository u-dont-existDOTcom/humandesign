"""Chinese V4 source ledger append-only gate; earlier V1–V3 immutable."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
P = B.parents[1]
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


class AcceptedChineseHistoricalV4(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = {
            version: j(P / f"CHINESE_SOURCE_AUDIT_INDEX_V{version}.json")
            for version in (1, 2, 3, 4)
        }
        cls.pre = j(B / "SOURCE_RELEASE_RECEIPT_20261019.json")
        cls.commit = j(B / "CANONICAL_PREPARE_RECEIPT_20261019.json")
        cls.source = j(B / "ZIWEI_VOLUME2_LIFE_BODY_TAXONOMY_SOURCE_NOTES_V1.json")
        cls.witness = j(B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json")

    def test_source_progression_not_synthetic_forecasts(self):
        self.assertEqual(
            [self.a[k]["sum_source_annotations"] for k in (1, 2, 3, 4)], [72, 97, 142, 207]
        )

    def test_previous_v3_sha_exact(self):
        path = P / "CHINESE_SOURCE_AUDIT_INDEX_V3.json"
        self.assertEqual(self.a[4]["prior_index_sha256"], sha(path))
        self.assertEqual(self.pre["old_Chinese_V3_index_SHA256"], sha(path))
        self.assertEqual(self.commit["prior_chinese_V3_sha256"], sha(path))
        self.assertEqual(sha(B / "recovery/CHINESE_V3_BEFORE_04.json"), sha(path))

    def test_only_one_new_batch(self):
        older = [row["id"] for row in self.a[3]["accepted_batches"]]
        new = [row["id"] for row in self.a[4]["accepted_batches"]]
        self.assertEqual(new, older + ["ChineseAstro-04"])

    def test_twelve_byte_arrays_not_mutated(self):
        old = self.a[3]["systems"][0]
        new = self.a[4]["systems"][0]
        self.assertEqual(old, new)
        self.assertEqual(new["accepted_source_annotations"], 46)
        self.assertEqual(new["next_id"], "BZI-R0047")

    def test_source_life_body_65(self):
        self.assertEqual(self.source["count"], 65)
        self.assertEqual(self.source["short_chinese_quote_direct_match_count"], 65)
        self.assertEqual(self.witness["original_quote_count"], 65)
        self.assertEqual(
            self.a[4]["original_chinese_source_anchors_checked_against_revision"],
            self.a[3]["original_chinese_source_anchors_checked_against_revision"] + 65,
        )

    def test_exact_zero_gap_new_ID_range(self):
        self.assertEqual(
            [r["id"] for r in self.source["records"]], [f"ZWD-R{x:04d}" for x in range(97, 162)]
        )

    def test_ZiWei_next_cursor(self):
        cur = self.a[4]["systems"][1]
        self.assertEqual(cur["accepted_source_annotations"], 161)
        self.assertEqual(cur["next_id"], "ZWD-R0162")
        self.assertEqual(cur["current_batch"], "ChineseAstro-04")

    def test_source_files_append_exactly_one(self):
        before = self.a[3]["systems"][1]["source_files"]
        after = self.a[4]["systems"][1]["source_files"]
        self.assertEqual(after[:-1], before)
        self.assertEqual(
            after[-1],
            "batches/ChineseAstro-04/ZIWEI_VOLUME2_LIFE_BODY_TAXONOMY_SOURCE_NOTES_V1.json",
        )

    def test_new_batch_SHA_and_traceability(self):
        record = self.a[4]["accepted_batches"][-1]
        self.assertEqual(record["start"], "ZWD-R0097")
        self.assertEqual(record["end"], "ZWD-R0161")
        self.assertEqual(
            record["rules_sha256"], sha(B / "ZIWEI_VOLUME2_LIFE_BODY_TAXONOMY_SOURCE_NOTES_V1.json")
        )
        self.assertEqual(
            record["witness_sha256"], sha(B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json")
        )
        self.assertEqual(record["wikisource_revision_id"], 1963110)

    def test_pinned_raw_hash_same_as_prior(self):
        record = self.a[4]["accepted_batches"][-1]
        self.assertEqual(record["original_raw_sha256"], self.source["raw_source_sha256"])
        self.assertEqual(
            record["original_raw_sha256"], self.witness["original_full_raw_source_sha256"]
        )
        self.assertEqual(
            record["original_raw_sha256"], self.a[3]["accepted_batches"][-1]["original_raw_sha256"]
        )

    def test_compressed_archive_249_tests(self):
        self.assertEqual(self.pre["total_replayed_tests"], 249)
        self.assertTrue(self.pre["crc_passed"])
        self.assertTrue(self.pre["member_SHA256_and_bytes_passed"])
        self.assertTrue(self.pre["independent_ZIP_extract_passed"])
        self.assertEqual(self.commit["portable_test_replays"], 249)

    def test_exact_index_v4_sha(self):
        self.assertEqual(
            self.commit["new_chinese_V4_sha256"], sha(P / "CHINESE_SOURCE_AUDIT_INDEX_V4.json")
        )
        self.assertEqual(self.commit["new_documented_source_notes"], 65)

    def test_source_v3_snapshot_and_western_history_protection(self):
        self.assertEqual(j(WEST)["records_count"], 12472)
        self.assertEqual(self.a[4]["separate_lilly_source_count_at_this_revision"], 12472)
        self.assertEqual(self.a[4]["separate_ptolemy_source_count_at_this_revision"], 1066)
        self.assertEqual(sha(WEST), sha(B / "recovery/WESTERN_LILLY_INDEX_BEFORE_CHINESE04.json"))

    def test_zero_human_predictions_or_runtime_promotions(self):
        self.assertFalse(self.a[4]["ziwei_complete_natal_calendar_engine_verified"])
        self.assertFalse(self.a[4]["chinese_bazi_solar_term_engine_verified"])
        self.assertFalse(self.a[4]["all_14_principal_stars_verified"])
        self.assertFalse(self.a[4]["full_ziwei_original_text_collation_finished"])
        self.assertEqual(self.a[4]["independently_validated_real_human_claims"], 0)
        self.assertEqual(self.a[4]["runtime_promotions"], 0)

    def test_original_english_summary_and_canonical_status(self):
        text = (ROOT / "state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md").read_text()
        self.assertIn("207 historical notes", text)
        self.assertIn("Zi Wei", text)
        self.assertIn("ZWD-R0162", text)


if __name__ == "__main__":
    unittest.main()
