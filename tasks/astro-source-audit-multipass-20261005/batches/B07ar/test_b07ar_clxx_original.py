"""Original first/second edition CLXX physical Midheaven/Sun source checks."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


class LillyCLXXSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = j(B / "ORIGINAL_CLXX_MIDHEAVEN_SUN_17_SOURCE_NOTES_V1.json")
        cls.rules = j(B / "RULES.json")
        cls.accept = j(B / "ACCEPTANCE.json")
        cls.nav = (B / "SECONDARY_CLXX_SOURCE_NAVIGATOR.txt").read_text()
        cls.rows = cls.source["records"]

    def test_original_full_Wellcome_first_edition_identity(self):
        self.assertEqual(
            self.source["original_book_full_1647_pdf_sha256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_all_four_original_printed_photo_witnesses(self):
        self.assertEqual(
            len(self.source["all_four_original_first_second_printed_photo_sha256s"]), 4
        )
        for row in self.source["all_four_original_first_second_printed_photo_sha256s"].values():
            file = ROOT / row["source_relative_path"]
            self.assertEqual(sha(file), row["file_sha256"])
            self.assertEqual(file.stat().st_size, row["file_bytes"])
            self.assertGreater(row["file_bytes"], 250000)

    def test_original_two_source_printings_not_two_human_experiments(self):
        self.assertTrue(self.source["source_reliance_on_independently_typeset_original_printings"])
        self.assertFalse(
            self.source["source_original_1647_full_critical_diplomatic_second_reader_complete"]
        )
        self.assertEqual(self.source["actual_human_forecasts_validated"], 0)

    def test_original_pdf765_to766_printed731_732_and_next_CLXXI(self):
        self.assertEqual(self.source["original_CLXX_chapter_primary_physical_frames"], [765, 766])
        self.assertEqual(self.source["next_CLXXI_chapter_starts_on_pdf_frame"], 766)
        self.assertEqual(self.accept["next_printed_chapter"], "CLXXI")
        self.assertEqual(self.accept["next_printed_folio"], 732)

    def test_all_twelve_source_houses_and_no_invented_gaps(self):
        self.assertEqual([r["profection_house"] for r in self.rows[:12]], list(range(1, 13)))
        self.assertTrue(self.source["twelve_historical_house_positions_source_read"])

    def test_second_house_work_and_eleven_friends_explicit(self):
        self.assertIn("reward", self.rows[1]["historical_source_description_not_personal_fact"])
        self.assertIn(
            "friendships", self.rows[10]["historical_source_description_not_personal_fact"]
        )
        self.assertIn("When to the 11th", self.nav)

    def test_source_old_sixth_house_secondary_typo_is_not_first_printed_quote(self):
        row = self.rows[5]
        self.assertEqual(row["modern_secondary_anchor_nondiplomatic"], "When to the 6th hosue")
        self.assertIn("When to the 6th hosue", self.nav)
        self.assertFalse(row["source_independent_critical_edition_review_complete"])

    def test_ordinal_geometry_conditions_not_universal_predictions(self):
        roles = {r["role"] for r in self.rows}
        self.assertIn("third_house_geometry_6_from10", roles)
        self.assertIn("midheaven_sun_joint_trigger", roles)
        self.assertIn("fifth_conditional_children", roles)
        self.assertIn("seventh_capability_conditional", roles)

    def test_verified_derivative_navigational_offsets(self):
        self.assertEqual(
            self.source["modern_secondary_text_excerpt_sha256"],
            sha(B / "SECONDARY_CLXX_SOURCE_NAVIGATOR.txt"),
        )
        for r in self.rows:
            anchor = r["modern_secondary_anchor_nondiplomatic"]
            at = r["secondary_anchor_char_offset"]
            self.assertEqual(self.nav[at : at + len(anchor)], anchor)

    def test_notes_17_exact_nonoverlapping_IDs(self):
        self.assertEqual(len(self.rows), 17)
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(12726, 12743))
        )
        self.assertEqual(self.rules["first_record"], "R12726")
        self.assertEqual(self.rules["last_record"], "R12742")
        self.assertEqual(self.accept["next_historical_R"], "R12743")

    def test_prior_Western_Chinese_indexes_not_modified(self):
        self.assertEqual(j(WEST)["records_count"], 12725)
        self.assertEqual(j(WEST)["batches"][-1]["id"], "B07aq")
        self.assertEqual(j(CHINA)["sum_source_annotations"], 355)

    def test_historical_harmful_claims_not_actual_human_outcomes(self):
        self.assertFalse(self.source["personal_astrological_predictive_accuracy_verified"])
        self.assertFalse(self.source["full_1647_epoch_calendar_engine_verified"])
        self.assertEqual(self.source["runtime_promotions"], 0)
        self.assertTrue(
            all(
                not r["individual_health_character_finance_prediction_validated"] for r in self.rows
            )
        )
        self.assertTrue(all(not r["runtime_promoted"] for r in self.rows))

    def test_source_record_rules_SHA(self):
        self.assertEqual(
            self.accept["source_notes_SHA256"],
            sha(B / "ORIGINAL_CLXX_MIDHEAVEN_SUN_17_SOURCE_NOTES_V1.json"),
        )
        self.assertEqual(self.accept["rules_SHA256"], sha(B / "RULES.json"))


def row_case(i):
    def test(self):
        r = self.rows[i]
        rule = self.rules["rules"][i]
        self.assertEqual(r["id"], f"R{12726 + i}")
        self.assertEqual(rule["id"], r["id"])
        self.assertEqual(rule["role"], r["role"])
        self.assertFalse(rule["runtime_model_promoted"])

    return test


for n in range(17):
    setattr(LillyCLXXSource, f"test_original_house_source_{n + 1:02d}", row_case(n))


if __name__ == "__main__":
    unittest.main()
