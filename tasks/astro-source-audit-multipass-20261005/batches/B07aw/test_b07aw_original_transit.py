"""Original Lilly 1647/1659 chapter CLXXIIII/CLXXIV transit source tests."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = ROOT / "tasks/astro-source-audit-multipass-20261005"
WEST = TASK / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
PHOTOS = TASK / "batches/B07av/evidence"


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class OriginalTransitChapter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = read(B / "CLXXIIII_TRANSITS_ORIGINAL_1647_1659_25_SOURCE_NOTES_V1.json")
        cls.rules = read(B / "RULES.json")
        cls.accept = read(B / "ACCEPTANCE.json")
        cls.conflict = read(B / "ORIGINAL_1647_1659_MARS_TRANSIT_DURATION_SOURCE_CONFLICT_V1.json")
        cls.boundary = read(B / "ORIGINAL_NEXT_MERCHANT_NATIVITY_BOUNDARY_1647_1659_V1.json")
        cls.west = read(WEST)
        cls.china = read(CHINA)
        cls.rows = cls.rules["rules"]

    def test_photographic_1647_source_pdf_full_identity(self):
        self.assertEqual(
            self.west["source_sha256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )
        self.assertEqual(
            self.west["source_sha256"],
            self.boundary["original_full_Wellcome_1647_pdf_sha256"],
        )

    def test_both_exact_original_page_741_photographs_sha(self):
        self.assertEqual(
            sha(PHOTOS / "1647_original-775.jpg"),
            self.conflict["original_first_edition_full_page_sha256"],
        )
        self.assertEqual(
            sha(PHOTOS / "1659_original_djvu_770.jpg"),
            self.conflict["original_second_edition_full_page_sha256"],
        )

    def test_both_exact_original_page_742_photographs_sha(self):
        self.assertEqual(
            sha(B / "evidence/1647_original-776.jpg"),
            self.boundary["new_first_edition_page_sha256"],
        )
        self.assertEqual(
            sha(B / "evidence/1659_original_djvu_771.jpg"),
            self.boundary["new_second_typeset_edition_page_sha256"],
        )

    def test_original_duration_crop_sha_reproduced(self):
        self.assertEqual(
            sha(B / self.conflict["first_edition_source_crop"]),
            self.conflict["first_crop_sha256"],
        )
        self.assertEqual(
            sha(B / self.conflict["second_edition_source_crop"]),
            self.conflict["second_crop_sha256"],
        )

    def test_physical_editions_same_chapter_distinct_numerals(self):
        self.assertEqual(self.source["first_source_chapter_original_1647"], "CLXXIIII")
        self.assertEqual(self.source["second_source_chapter_original_1659"], "CLXXIV")
        self.assertEqual(
            self.source["original_editions_both_title"], "Of the TRANSIT of the Planets."
        )

    def test_transit_scope_exact_one_1647_page(self):
        self.assertEqual(self.source["first_source_pdf_frame"], 775)
        self.assertEqual(self.source["first_source_printed_folio"], 741)
        self.assertTrue(self.source["first_1647_source_physically_covered"])
        self.assertFalse(
            self.source["historical_source_first_1647_complete_expert_diplomatic_collation"]
        )

    def test_new_merchants_separate_physical_chapter(self):
        self.assertEqual(self.boundary["first_edition_original_chapter_numeral"], "CLXXV")
        self.assertEqual(self.boundary["second_edition_original_chapter_numeral"], "CLXXV")
        self.assertEqual(self.boundary["1647_original_pdf_frame"], 776)
        self.assertEqual(self.boundary["1659_original_djvu_frame"], 771)
        self.assertEqual(self.source["next_original_pdf_frame"], 776)
        self.assertEqual(self.accept["next_source_chapter"], "CLXXV")

    def test_original_mars_duration_variation_material(self):
        self.assertEqual(self.conflict["first_edition_quote_exact_span"], "for two or three dayes")
        self.assertEqual(self.conflict["second_edition_quote_exact_span"], "for two or three years")
        self.assertTrue(self.conflict["source_variation_material_for_historical_prediction_window"])
        r = next(r for r in self.rows if r["role"] == "mars_ascendant_duration_edition_conflict")
        self.assertEqual(r["first_printing_1647_literal_duration"], "two or three dayes")
        self.assertEqual(r["second_printing_1659_literal_duration"], "two or three years")
        self.assertTrue(r["source_duration_choice_prohibited_without_new_evidence"])

    def test_all_25_historical_ids_exact_unrepeated(self):
        self.assertEqual(self.source["new_source_documentary_rule_count"], 25)
        self.assertEqual(self.rules["record_count"], 25)
        self.assertEqual(len(self.rows), 25)
        self.assertEqual(
            [r["record_number"] for r in self.rows],
            list(range(12846, 12871)),
        )
        self.assertEqual(self.accept["next_record"], "R12871")

    def test_source_groups_one_transit_one_next_boundary(self):
        self.assertEqual(self.rules["source_groups"], 2)
        self.assertEqual(sum(r["original_pdf_frames"] == [775] for r in self.rows), 24)
        self.assertEqual(sum(r["original_pdf_frames"] == [776] for r in self.rows), 1)
        self.assertEqual(self.rows[-1]["role"], "next_chapter_merchant_separate")
        self.assertEqual(self.rows[-1]["original_printed_folio"], 742)

    def test_original_photo_references_are_pinned_in_each_record(self):
        for r in self.rows:
            self.assertEqual(len(r["first_1647_original_source_image_SHA256"]), 64)
            self.assertEqual(len(r["second_1659_original_source_image_SHA256"]), 64)
            self.assertTrue(r["source_short_photo_anchor_or_locator"])
            self.assertTrue(r["source_preconditions_and_uncertainty"])
            self.assertFalse(r["source_anchor_is_full_diplomatic_transcription"])

    def test_original_sources_not_modern_biomedical_financial_assertions(self):
        for r in self.rows:
            self.assertFalse(r["personal_mood_health_money_or_risk_predictions_validated"])
            self.assertFalse(r["independent_blinded_actual_human_predictive_accuracy_verified"])
            self.assertFalse(r["runtime_model_promoted"])

    def test_previous_registries_not_mutated_before_acceptance(self):
        self.assertEqual(self.west["records_count"], 12845)
        self.assertEqual(self.west["batches"][-1]["id"], "B07av")
        self.assertEqual(self.china["sum_source_annotations"], 355)
        self.assertEqual(self.source["parallel_Chinese_V7_historical_records"], 355)

    def test_original_1647_natal_ephemeris_not_mathematically_validated(self):
        self.assertFalse(self.source["modern_calendar_ephemeris_natal_house_parity_validated"])
        self.assertFalse(self.source["source_validated_against_actual_human_transit_outcomes"])
        self.assertEqual(self.source["independent_blinded_real_people_predictions_validated"], 0)
        self.assertEqual(self.source["runtime_astrological_rule_promotions"], 0)

    def test_rules_and_acceptance_original_SHA(self):
        self.assertEqual(self.accept["rules_SHA256"], sha(B / "RULES.json"))
        self.assertEqual(
            self.accept["source_full_document_SHA256"],
            sha(B / "CLXXIIII_TRANSITS_ORIGINAL_1647_1659_25_SOURCE_NOTES_V1.json"),
        )

    def test_source_154_vs_201_chinese_independent(self):
        self.assertEqual(
            [s["accepted_source_annotations"] for s in self.china["systems"]],
            [154, 201],
        )
        self.assertEqual(self.china["runtime_promotions"], 0)

    def test_forward_next_original_merchant_age_not_retuned(self):
        self.assertEqual(self.accept["next_editorial_chapter_ordinal"], 175)
        self.assertEqual(self.accept["Lilly_after_if_admitted"], 12870)
        self.assertEqual(self.accept["Western_after_if_admitted"], 13936)
        self.assertTrue(
            self.accept["next_source_title"].startswith("The NATIVITY of an English Merchant")
        )


def one_source_row(i: int):
    def test(self):
        row = self.rows[i]
        self.assertEqual(row["id"], f"R{12846 + i}")
        self.assertEqual(row["record_number"], 12846 + i)
        self.assertTrue(row["historical_source_documented_by_one_reader"])
        self.assertFalse(row["independent_source_expert_critical_edition_verified"])
        self.assertFalse(row["runtime_model_promoted"])

    return test


for i in range(25):
    setattr(OriginalTransitChapter, f"test_photo_reading_{i + 1:02d}", one_source_row(i))


if __name__ == "__main__":
    unittest.main()
