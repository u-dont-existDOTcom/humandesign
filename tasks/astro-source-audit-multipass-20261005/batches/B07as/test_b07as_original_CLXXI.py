"""First and second actual printed Lilly CLXXI source, 22 historical notes.

Tests document source photo/record correspondence; never treat these as
empirically verified illness, financial, ethical or life-event forecasts.
"""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class FirstOriginalCLXXISource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = load(B / "ORIGINAL_CLXXI_FORTUNE_12_HOUSES_AND_ALFRIDARY_22_SOURCE_NOTES_V1.json")
        cls.rules = load(B / "RULES.json")
        cls.accept = load(B / "ACCEPTANCE.json")
        cls.navigator = (B / "SECONDARY_CLXXI_NAVIGATOR.txt").read_text(encoding="utf-8")
        cls.original = cls.doc["records"]

    def test_original_1647_full_source_pinned(self):
        self.assertEqual(
            self.doc["source_original_book_Wellcome_1647_full_pdf_SHA256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_six_original_first_second_printed_pages_hash_verified(self):
        sources = self.doc["source_first_and_separate_second_original_printings"]
        self.assertEqual(len(sources), 6)
        for label, entry in sources.items():
            path = ROOT / entry["relative_original_photo"]
            self.assertEqual(sha(path), entry["source_image_sha256"], label)
            self.assertEqual(path.stat().st_size, entry["file_bytes"], label)
            self.assertEqual(entry["edition_year"], int(label[:4]))
            self.assertEqual(entry["printed_page"], int(label[-3:]))

    def test_exact_22_historical_original_notes(self):
        self.assertEqual(len(self.original), 22)
        self.assertEqual(self.doc["new_source_only_annotations"], 22)
        self.assertEqual(self.rules["record_count"], 22)
        self.assertEqual([row["record_number"] for row in self.original], list(range(12743, 12765)))
        self.assertEqual(
            [row["id"] for row in self.rules["rules"]], [f"R{x}" for x in range(12743, 12765)]
        )

    def test_twelve_distinct_source_houses(self):
        self.assertEqual([r["historical_house"] for r in self.original[:12]], list(range(1, 13)))
        self.assertTrue(all(r["historical_house"] is None for r in self.original[12:]))
        self.assertTrue(self.doc["source_twelve_house_cases_documented"])

    def test_first_life_septennial_Alfridary_no_total_life_claim(self):
        self.assertEqual(
            self.doc["historical_source_Alfridary_day_first_three_7year_lords"],
            ["Sun", "Venus", "Mercury"],
        )
        self.assertEqual(
            self.doc["historical_source_Alfridary_night_first_three_7year_lords"],
            ["Moon", "Saturn", "Jupiter"],
        )
        self.assertFalse(self.doc["source_full_life_cycle_sequence_in_this_chapter"])
        self.assertFalse(self.accept["source_Alfridary_more_than_first_three_planets_assumed"])

    def test_1647_1659_page_end_CLXXII_physical_boundary(self):
        self.assertEqual(self.original[-1]["role"], "next_CLXXII_original_chapter_boundary")
        self.assertEqual(self.original[-1]["original_1647_pdf_frame"], 768)
        self.assertEqual(self.accept["next_R"], "R12765")
        self.assertEqual(self.accept["next_original_PDF"], 768)
        self.assertEqual(self.accept["next_chapter"], "CLXXII")
        self.assertEqual(self.accept["next_original_printed_folio"], 734)

    def test_searchable_flat_text_navigation_separate_from_original(self):
        self.assertEqual(
            sha(B / "SECONDARY_CLXXI_NAVIGATOR.txt"),
            self.doc["source_secondary_searchable_excerpt_SHA256"],
        )
        for row in self.original:
            q = row["derivative_navigation_anchor_not_diplomatic"]
            self.assertIn(q, self.navigator)
            self.assertEqual(
                self.navigator[
                    row["derivative_excerpt_codepoint_position"] : row[
                        "derivative_excerpt_codepoint_position"
                    ]
                    + len(q)
                ],
                q,
            )

    def test_each_rule_original_1647_1659_image_correspondence(self):
        bysource = self.doc["source_first_and_separate_second_original_printings"]
        for doc, rule in zip(self.original, self.rules["rules"], strict=True):
            self.assertEqual(doc["id"], rule["id"])
            self.assertEqual(doc["role"], rule["role"])
            page = doc["original_printed_folio"]
            self.assertEqual(rule["original_pdf_frames"], [page + 34])
            self.assertEqual(
                doc["original_1647_first_ed_photo_sha256"],
                bysource[f"1647_printed{page}"]["source_image_sha256"],
            )
            self.assertEqual(
                doc["original_1659_separately_typeset_photo_sha256"],
                bysource[f"1659_printed{page}"]["source_image_sha256"],
            )
            self.assertFalse(rule["runtime_model_promoted"])

    def test_previous_accepted_index_unchanged(self):
        old = load(INDEX)
        china = load(CHINA)
        self.assertEqual(old["records_count"], 12742)
        self.assertEqual(old["batches"][-1]["id"], "B07ar")
        self.assertEqual(old["next"]["chapter"], "CLXXI")
        self.assertEqual(old["next"]["pdf_page"], 766)
        self.assertEqual(china["sum_source_annotations"], 355)
        self.assertEqual(self.accept["Lilly_before"], 12742)

    def test_documentary_only_with_explicit_human_claim_limits(self):
        self.assertFalse(self.doc["original_full_diplomatic_expert_critical_edition_verified"])
        self.assertTrue(self.doc["source_authority_is_not_actual_human_prediction_data"])
        self.assertEqual(self.doc["independent_actual_human_forecasts_validated"], 0)
        self.assertEqual(self.rules["real_person_predicted_life_events_validated"], 0)
        self.assertEqual(self.rules["runtime_promotions"], 0)
        for record in self.original:
            self.assertFalse(record["real_person_health_morality_wealth_forecast_validated"])
            self.assertFalse(record["original_birth_hour_calendar_chart_engine_verified"])

    def test_files_stable_SHA_receipt(self):
        self.assertEqual(
            self.accept["source_records_SHA256"],
            sha(B / "ORIGINAL_CLXXI_FORTUNE_12_HOUSES_AND_ALFRIDARY_22_SOURCE_NOTES_V1.json"),
        )
        self.assertEqual(self.accept["rules_SHA256"], sha(B / "RULES.json"))
        self.assertEqual(self.accept["Lilly_after_if_accepted"], 12764)
        self.assertEqual(self.accept["Western_after_if_accepted"], 13830)

    def test_source_not_conflated_with_predictions_or_engine(self):
        for row in self.original:
            self.assertTrue(row["historical_source_verification_one_informed_reader"])
            self.assertFalse(row["original_full_edition_expert_collation"])
            self.assertFalse(row["runtime_promoted"])


def test_row(index):
    def test(self):
        row = self.original[index]
        rule = self.rules["rules"][index]
        self.assertEqual(row["id"], f"R{12743 + index}")
        self.assertEqual(rule["record_number"], 12743 + index)
        self.assertEqual(
            row["derivative_navigation_anchor_not_diplomatic"], rule["source_anchor_not_diplomatic"]
        )
        self.assertFalse(row["real_person_health_morality_wealth_forecast_validated"])

    return test


for i in range(22):
    setattr(FirstOriginalCLXXISource, f"test_exact_source_row_{i + 1:02d}", test_row(i))

if __name__ == "__main__":
    unittest.main()
