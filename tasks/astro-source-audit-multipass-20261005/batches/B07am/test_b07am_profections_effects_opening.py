"""Original printed CLXVII p718–720 source-only photo/ID integrity."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class ProfectionsEffectsOpening(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notes = j(B / "CLXVII_OPENING_INTERPRETIVE_NOTES_V1.json")
        cls.rules = j(B / "RULES.json")
        cls.accept = j(B / "ACCEPTANCE.json")

    def test_original_pinned_source_pdf(self):
        self.assertEqual(
            self.notes["original_1647_pdf_SHA256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_three_original_photo_sha_members(self):
        self.assertEqual(self.notes["source_frames"], [752, 753, 754])
        for r in self.rules["photo_witnesses"].values():
            f = ROOT / r["path"]
            self.assertEqual(sha(f), r["sha256"])
            self.assertEqual(f.stat().st_size, r["bytes"])

    def test_14_sequential_historical_source_id_range(self):
        self.assertEqual(len(self.notes["records"]), 14)
        self.assertEqual(self.rules["record_count"], 14)
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(12612, 12626))
        )
        self.assertEqual(self.accept["next_R"], "R12626")

    def test_each_source_folio_kept_distinct(self):
        self.assertEqual(
            [r["printed_folio"] for r in self.rules["photo_witnesses"].values()], [718, 719, 720]
        )
        self.assertEqual(self.rules["body_pdf_frames"], [752, 753, 754])

    def test_chapter_not_marked_complete(self):
        self.assertFalse(self.rules["chapter_complete"])
        self.assertTrue(self.rules["next_1647_printed_conversion_tables_not_accepted"])
        self.assertFalse(self.accept["chapter_complete"])

    def test_next_source_table_PDF755(self):
        self.assertEqual(self.accept["next_PDF"], 755)
        self.assertEqual(self.accept["next_printed_folio"], 721)
        self.assertEqual(self.accept["Lilly_if_accepted"], 12625)

    def test_existing_lilly_and_chinese_not_changed(self):
        w = j(
            ROOT
            / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
        )
        c = j(
            ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"
        )
        self.assertEqual(w["records_count"], 12611)
        self.assertEqual(c["sum_source_annotations"], 262)

    def test_sha_matches_actual_released_source_records(self):
        self.assertEqual(self.accept["rules_SHA256"], sha(B / "RULES.json"))
        self.assertEqual(
            self.accept["notes_SHA256"], sha(B / "CLXVII_OPENING_INTERPRETIVE_NOTES_V1.json")
        )

    def test_conditional_source_not_empirical_result(self):
        self.assertEqual(self.rules["real_person_predictions_validated"], 0)
        self.assertEqual(self.rules["runtime_promotions"], 0)
        self.assertTrue(all(not r["runtime_model_promoted"] for r in self.rules["rules"]))

    def test_annual_profections_earlier_unit_not_reopened(self):
        w = j(
            ROOT
            / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
        )
        self.assertEqual(w["next"]["printed_chapter_numeral"], "CLXVII")
        self.assertEqual(w["next"]["editorial_source_sequence_ordinal"], 167)


def check_one(n):
    def test(self):
        note = self.notes["records"][n]
        row = self.rules["rules"][n]
        self.assertEqual(note["id"], f"R{12612 + n}")
        self.assertEqual(note["record_number"], 12612 + n)
        self.assertEqual(note["role"], row["role"])
        self.assertEqual(note["pdf_frame"], row["original_pdf_frames"][0])
        self.assertEqual(
            note["photo_sha256"], self.notes["original_source_photo_shas"][str(note["pdf_frame"])]
        )
        self.assertFalse(row["runtime_model_promoted"])

    return test


for n in range(14):
    setattr(ProfectionsEffectsOpening, f"test_photo_anchored_{n + 1:02d}", check_one(n))

if __name__ == "__main__":
    unittest.main()
