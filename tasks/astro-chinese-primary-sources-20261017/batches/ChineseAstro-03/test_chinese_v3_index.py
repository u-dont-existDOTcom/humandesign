"""Post-acceptance appended Chinese V3 index, no source/Western replacement."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
P = B.parents[1]
V1 = P / "CHINESE_SOURCE_AUDIT_INDEX_V1.json"
V2 = P / "CHINESE_SOURCE_AUDIT_INDEX_V2.json"
V3 = P / "CHINESE_SOURCE_AUDIT_INDEX_V3.json"
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class AcceptedV3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v1 = j(V1)
        cls.v2 = j(V2)
        cls.v3 = j(V3)
        cls.notes = j(B / "ZIWEI_VOLUME2_AUXILIARY_45_SOURCE_NOTES_V1.json")
        cls.witness = j(B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json")
        cls.receipt = j(B / "CANONICAL_PREPARE_RECEIPT_20261018.json")

    def test_source_registry_grows_only_v3(self):
        self.assertEqual(self.v1["sum_source_annotations"], 72)
        self.assertEqual(self.v2["sum_source_annotations"], 97)
        self.assertEqual(self.v3["sum_source_annotations"], 142)

    def test_previous_index_preserved(self):
        self.assertEqual(sha(V2), self.v3["prior_index_sha256"])
        self.assertEqual(sha(V2), self.receipt["original_index_v2_sha256"])
        self.assertEqual(sha(B / "recovery" / "CHINESE_V2_BEFORE_03.json"), sha(V2))

    def test_batch_three_is_single_append(self):
        self.assertEqual(
            [b["id"] for b in self.v3["accepted_batches"]],
            [b["id"] for b in self.v2["accepted_batches"]] + ["ChineseAstro-03"],
        )

    def test_BaZi_source_count_not_conflated(self):
        self.assertEqual(self.v3["systems"][0]["accepted_source_annotations"], 46)
        self.assertEqual(self.v3["systems"][0]["next_id"], "BZI-R0047")
        self.assertEqual(self.v2["systems"][0], self.v3["systems"][0])

    def test_ziwei_count_and_next_id(self):
        z = self.v3["systems"][1]
        self.assertEqual(z["accepted_source_annotations"], 96)
        self.assertEqual(z["next_id"], "ZWD-R0097")
        self.assertEqual(z["current_ids"], "ZWD-R0001–ZWD-R0096")
        self.assertEqual(z["current_batch"], "ChineseAstro-03")

    def test_previous_ziwei_source_files_append_only(self):
        old = self.v2["systems"][1]["source_files"]
        new = self.v3["systems"][1]["source_files"]
        self.assertEqual(new[: len(old)], old)
        self.assertEqual(len(new), len(old) + 1)

    def test_original_quote_count_increased_exactly_by_45(self):
        self.assertEqual(self.v3["original_chinese_source_anchors_checked_against_revision"], 70)
        self.assertEqual(self.v2["original_chinese_source_anchors_checked_against_revision"], 25)
        self.assertEqual(self.witness["short_exact_chinese_anchor_matches"], 45)

    def test_source_sha_in_batch_index(self):
        b = self.v3["accepted_batches"][-1]
        self.assertEqual(
            b["rules_sha256"], sha(B / "ZIWEI_VOLUME2_AUXILIARY_45_SOURCE_NOTES_V1.json")
        )
        self.assertEqual(b["witness_sha256"], sha(B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json"))

    def test_sha_old_original_china_V1_kept(self):
        self.assertEqual(self.v1["sum_source_annotations"], 72)
        self.assertEqual(self.v3["prior_index"], "CHINESE_SOURCE_AUDIT_INDEX_V2.json")

    def test_western_lilly_not_modified(self):
        self.assertEqual(j(WEST)["records_count"], 12472)
        self.assertEqual(sha(WEST), sha(B / "recovery" / "WESTERN_INDEX_BEFORE_CHINESE_03.json"))
        self.assertEqual(self.v3["separate_lilly_source_count_at_this_revision"], 12472)
        self.assertEqual(self.v3["separate_ptolemy_source_count_at_this_revision"], 1066)

    def test_active_chinese_state_points_v3(self):
        p = ROOT / "state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
        self.assertIn("45 newly anchored", p.read_text(encoding="utf-8"))
        self.assertIn("142 Chinese", p.read_text(encoding="utf-8"))

    def test_full_calendar_and_predicted_outcomes_not_promoted(self):
        self.assertFalse(self.v3["ziwei_complete_natal_calendar_engine_verified"])
        self.assertFalse(self.v3["chinese_bazi_solar_term_engine_verified"])
        self.assertFalse(self.v3["all_14_principal_stars_verified"])
        self.assertFalse(self.v3["full_ziwei_original_text_collation_finished"])
        self.assertEqual(self.v3["independently_validated_real_human_claims"], 0)
        self.assertEqual(self.v3["runtime_promotions"], 0)

    def test_receipt_and_index_sha(self):
        self.assertEqual(self.receipt["new_index_v3_sha256"], sha(V3))
        self.assertEqual(self.receipt["new_historical_source_notes"], 45)
        self.assertEqual(self.receipt["portable_tests"], 160)

    def test_last_45_new_ids_sequential(self):
        self.assertEqual(
            [r["id"] for r in self.notes["records"]], [f"ZWD-R{n:04d}" for n in range(52, 97)]
        )

    def test_original_wikisource_revision_unchanged(self):
        self.assertEqual(
            self.notes["raw_source_sha256"], self.v3["accepted_batches"][-1]["original_raw_sha256"]
        )
        self.assertEqual(self.v3["accepted_batches"][-1]["wikisource_revision_id"], 1963110)


if __name__ == "__main__":
    unittest.main()
