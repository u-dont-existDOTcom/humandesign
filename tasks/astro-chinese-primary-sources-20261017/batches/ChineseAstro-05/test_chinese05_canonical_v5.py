"""Chinese original BaZi V5 append-only historical-source admission tests."""
import hashlib
import json
import unittest
from pathlib import Path

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
P=B.parents[1]
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class OriginalChineseV5(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v={i:j(P/f"CHINESE_SOURCE_AUDIT_INDEX_V{i}.json") for i in range(1,6)}
        cls.notes=j(B/"BAZI_DITIAN_SUI_SIX_SECTIONS_55_SOURCE_NOTES_V1.json")
        cls.source=j(B/"DITIAN_SUI_PINNED_SOURCE_MANIFEST_V1.json")
        cls.witness=j(B/"SOURCE_REVISION_ANCHOR_WITNESS_V1.json")
        cls.release=j(B/"SOURCE_RELEASE_RECEIPT_20261019.json")
        cls.index_receipt=j(B/"CANONICAL_PREPARE_RECEIPT_20261019.json")

    def test_old_indexes_progression_untouched(self):
        self.assertEqual(
            [self.v[i]["sum_source_annotations"] for i in range(1,6)],
            [72,97,142,207,262],
        )

    def test_old_version_sha_and_recovery_file(self):
        old=P/"CHINESE_SOURCE_AUDIT_INDEX_V4.json"
        self.assertEqual(sha(old),self.v[5]["prior_index_sha256"])
        self.assertEqual(sha(old),self.release["prior_chinese_V4_index_sha256"])
        self.assertEqual(sha(old),self.index_receipt["prior_index_V4_sha256"])
        self.assertEqual(sha(old),sha(B/"recovery/CHINESE_V4_BEFORE_05.json"))

    def test_BaZi_total_next_ID(self):
        b=self.v[5]["systems"][0]
        self.assertEqual(b["accepted_source_annotations"],101)
        self.assertEqual(b["next_id"],"BZI-R0102")
        self.assertEqual(b["current_batch"],"ChineseAstro-05")
        self.assertEqual(b["current_ids"],"BZI-R0001–BZI-R0101")
        self.assertIn("ChineseAstro-05",b["source_files"][-1])

    def test_ZiWei_ledger_identical_to_V4(self):
        self.assertEqual(self.v[5]["systems"][1],self.v[4]["systems"][1])
        self.assertEqual(self.v[5]["systems"][1]["accepted_source_annotations"],161)
        self.assertEqual(self.v[5]["systems"][1]["next_id"],"ZWD-R0162")

    def test_one_new_source_only_batch(self):
        self.assertEqual(
            [x["id"] for x in self.v[5]["accepted_batches"]],
            [x["id"] for x in self.v[4]["accepted_batches"]]+["ChineseAstro-05"]
        )

    def test_new_batch_source_and_witness_sha(self):
        row=self.v[5]["accepted_batches"][-1]
        self.assertEqual(row["start"],"BZI-R0047")
        self.assertEqual(row["end"],"BZI-R0101")
        self.assertEqual(row["added_bazi_source_annotations"],55)
        self.assertEqual(row["added_ziwei_source_annotations"],0)
        self.assertEqual(row["rules_sha256"],
                         sha(B/"BAZI_DITIAN_SUI_SIX_SECTIONS_55_SOURCE_NOTES_V1.json"))
        self.assertEqual(row["witness_sha256"],
                         sha(B/"SOURCE_REVISION_ANCHOR_WITNESS_V1.json"))
        self.assertEqual(row["source_manifest_sha256"],
                         sha(B/"DITIAN_SUI_PINNED_SOURCE_MANIFEST_V1.json"))

    def test_six_frozen_oldids(self):
        self.assertEqual(
            self.v[5]["accepted_batches"][-1]["source_pinned_multiple_revision_ids"],
            {key:row["revision_id"] for key,row in self.source.items()},
        )

    def test_sequential_55_new_ids_no_reuse(self):
        self.assertEqual(
            [r["id"] for r in self.notes["records"]],
            [f"BZI-R{x:04d}" for x in range(47,102)],
        )

    def test_190_chinese_phrase_hashes_from_pinned_pages(self):
        self.assertEqual(self.v[4]["original_chinese_source_anchors_checked_against_revision"],135)
        self.assertEqual(self.v[5]["original_chinese_source_anchors_checked_against_revision"],190)
        self.assertEqual(self.witness["exact_chinese_source_anchor_matches"],55)

    def test_current_user_checkpoints_match_V5(self):
        text=(ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md").read_text()
        self.assertIn("262",text)
        self.assertIn("BZI-R0102",text)
        self.assertTrue(
            (ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261019_05.md").is_file()
        )

    def test_retained_Western_source_count_and_sha(self):
        self.assertEqual(j(WEST)["records_count"],12472)
        self.assertEqual(j(WEST)["batches"][-1]["id"],"B07w")
        self.assertEqual(self.v[5]["separate_lilly_source_count_at_this_revision"],12472)
        self.assertEqual(self.v[5]["separate_ptolemy_source_count_at_this_revision"],1066)
        self.assertEqual(sha(WEST),
                         sha(B/"recovery/WESTERN_LILLY_INDEX_BEFORE_CHINESE05.json"))

    def test_independently_extracted_archive_replay_321(self):
        self.assertTrue(self.release["CRC_passed"])
        self.assertTrue(self.release["member_sha256_and_exact_bytes_passed"])
        self.assertTrue(self.release["independent_archive_extract_passed"])
        self.assertEqual(self.release["total_portable_test_replays"],321)
        self.assertEqual(self.index_receipt["portable_tests"],321)

    def test_new_canonical_index_SHA_receipt(self):
        self.assertEqual(sha(P/"CHINESE_SOURCE_AUDIT_INDEX_V5.json"),
                         self.index_receipt["new_index_V5_sha256"])
        self.assertEqual(self.index_receipt["new_documented_source_notes"],55)

    def test_critical_interpretive_limits_not_promoted(self):
        self.assertFalse(self.v[5]["chinese_bazi_solar_term_engine_verified"])
        self.assertFalse(self.v[5]["ziwei_complete_natal_calendar_engine_verified"])
        self.assertFalse(self.v[5]["all_14_principal_stars_verified"])
        self.assertEqual(self.v[5]["independently_validated_real_human_claims"],0)
        self.assertEqual(self.v[5]["runtime_promotions"],0)

    def test_verses_not_same_as_later_commentary(self):
        self.assertEqual(self.notes["verse_quote_count"],44)
        self.assertEqual(self.notes["commentary_exact_quote_count"],11)
        self.assertFalse(self.notes["source_author_or_commentary_attribution_certified"])


if __name__=="__main__":
    unittest.main()
