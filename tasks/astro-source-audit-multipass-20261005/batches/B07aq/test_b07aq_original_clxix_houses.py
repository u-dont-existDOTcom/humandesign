"""Two original printed Lilly editions preserve CLXIX eleventh-house text."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT / "tasks/astro-source-audit-multipass-20261005"
WEST = T / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"


def j(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


class OriginalCLXIXHouseSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = j(B / "FIRST_SECOND_ORIGINAL_CLXIX_HOUSES_21_NOTES_V1.json")
        cls.proof = j(B / "PHOTO_ELEVENTH_1647_1659_SOURCE_WITNESS_V1.json")
        cls.rules = j(B / "RULES.json")
        cls.accept = j(B / "ACCEPTANCE.json")
        cls.notes = cls.source["source_rows"]
        cls.modern = (B / "SECONDARY_CLXIX_NAVIGATOR_OMITS_ELEVENTH.txt").read_text()

    def test_primary_1647_Wellcome_pdf_source_identity(self):
        self.assertEqual(
            self.source["original_1647_full_pdf_SHA256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )
        self.assertEqual(
            self.source["original_1647_full_pdf_SHA256"],
            self.proof["full_original_1647_pdf_SHA256"],
        )

    def test_six_original_physical_edition_photo_SHA_and_bytes(self):
        images = self.source["source_six_original_primary_images"]
        self.assertEqual(len(images), 6)
        self.assertEqual(
            set(images),
            {
                "1647_folio729",
                "1647_folio730",
                "1647_folio731",
                "1659_folio729",
                "1659_folio730",
                "1659_folio731",
            },
        )
        for key, item in images.items():
            f = ROOT / item["relative_file"]
            self.assertTrue(f.is_file(), key)
            self.assertEqual(sha(f), item["sha256"])
            self.assertEqual(f.stat().st_size, item["bytes"])
            self.assertGreater(f.stat().st_size, 250000)

    def test_original_1647_chapter_physical_scope(self):
        self.assertEqual(self.source["source_original_first_CLXIX_physical_frames"], [763, 764])
        self.assertEqual(self.source["source_next_distinct_CLXX_heading_frame"], 765)
        self.assertTrue(self.source["first_CLXIX_physical_text_span_covered"])

    def test_one_of_12_house_paragraphs_absent_in_derivative_not_primary(self):
        self.assertEqual(len([x for x in self.notes if x["profection_house_number"]]), 12)
        self.assertEqual(
            [x["profection_house_number"] for x in self.notes[:12]],
            list(range(1, 13)),
        )
        self.assertTrue(self.source["source_original_1647_and_1659_both_contain_11th"])
        self.assertTrue(self.source["secondary_modern_html_transcription_omits_house11"])
        self.assertEqual(
            [
                x["profection_house_number"]
                for x in self.notes
                if x["original_print_missing_in_modern_derivative"]
            ],
            [11],
        )

    def test_11th_house_original_specific_text_not_modern_excerpt(self):
        r = self.notes[10]
        self.assertIn(
            "When to the eleventh", r["first_edition_11th_manual_cleaned_transcription_if_relevant"]
        )
        self.assertIn(
            "Native's Friends", r["first_edition_11th_manual_cleaned_transcription_if_relevant"]
        )
        self.assertIn(
            "husband time well", r["first_edition_11th_manual_cleaned_transcription_if_relevant"]
        )
        self.assertIsNone(r["modern_derivative_navigator_anchor"])
        self.assertIsNone(r["modern_derivative_relative_offset"])
        self.assertNotIn("When to the eleventh", self.modern)
        self.assertNotIn("When to the 11th", self.modern)
        self.assertIn("When to the 10th", self.modern)
        self.assertIn("When to the 12th", self.modern)
        self.assertEqual(
            r["source_first_1647_photo_SHA256"],
            self.source["source_six_original_primary_images"]["1647_folio730"]["sha256"],
        )
        self.assertEqual(
            r["source_second_1659_photo_SHA256"],
            self.source["source_six_original_primary_images"]["1659_folio730"]["sha256"],
        )

    def test_derivative_excerpt_exact_hash_and_absence_reproducible(self):
        self.assertEqual(
            sha(B / "SECONDARY_CLXIX_NAVIGATOR_OMITS_ELEVENTH.txt"),
            "fa2f78a87c05bb1dee27ba400f6c5bd840364fd7c4962c8697373b5dec0f9bcc",
        )
        self.assertEqual(
            self.source["searchable_derivative_excerpt_sha256"], self.proof["modern_excerpt_SHA256"]
        )

    def test_other_11_houses_have_derivative_locator_positions(self):
        for row in self.notes[:12]:
            if row["profection_house_number"] == 11:
                continue
            phrase = row["modern_derivative_navigator_anchor"]
            start = row["modern_derivative_relative_offset"]
            self.assertIsNotNone(start)
            self.assertEqual(self.modern[start : start + len(phrase)], phrase)

    def test_fifth_seventh_eighth_tenth_twelfth_source_qualifiers(self):
        roles = {r["role"] for r in self.notes}
        self.assertIn("fifth_age_context", roles)
        self.assertIn("seventh_other_significators", roles)
        self.assertIn("eighth_Hyleg_mortal_direction", roles)
        self.assertIn("tenth_if_capable", roles)
        self.assertIn("twelfth_natal_house_qualifier", roles)

    def test_original_Arabic_translation_and_annual_lords_context(self):
        roles = {r["role"] for r in self.notes}
        self.assertIn("arabic_source_translation_warning", roles)
        self.assertIn("infortune_annual_revolution_house", roles)
        self.assertIn("year_lord_and_house_lords", roles)

    def test_exact_numbering_21_source_only_records(self):
        self.assertEqual(len(self.notes), 21)
        self.assertEqual([r["id"] for r in self.notes], [f"R{i}" for i in range(12705, 12726)])
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(12705, 12726))
        )
        self.assertEqual(self.accept["new_historical_source_notes"], 21)
        self.assertEqual(self.rules["record_count"], 21)

    def test_next_heading_not_counted_twice_in_subsequent_chapter(self):
        self.assertEqual(self.notes[-1]["role"], "next_CLXX_physical_heading")
        self.assertEqual(self.accept["next_R"], "R12726")
        self.assertEqual(self.accept["next_chapter"], "CLXX")
        self.assertEqual(self.accept["next_original_pdf_frame"], 765)
        self.assertEqual(self.accept["next_original_printed_folio"], 731)

    def test_prior_Western_and_Chinese_preserved(self):
        self.assertEqual(j(WEST)["records_count"], 12704)
        self.assertEqual(j(WEST)["batches"][-1]["id"], "B07ap")
        self.assertEqual(j(CHINA)["sum_source_annotations"], 355)
        self.assertEqual(self.source["Lilly_before"], 12704)

    def test_historic_fates_are_not_supported_personal_forecasts(self):
        self.assertFalse(self.source["full_independent_expert_critical_edition_verified"])
        self.assertFalse(self.source["full_verified_astro_birth_chart_era_engine"])
        self.assertEqual(self.source["actual_human_predictive_validations"], 0)
        self.assertEqual(self.source["runtime_promotions"], 0)
        for row in self.notes:
            self.assertFalse(
                row["source_actual_human_health_money_reputation_prediction_validated"]
            )
            self.assertFalse(row["runtime_promoted"])

    def test_hash_links_and_source_proof(self):
        self.assertEqual(
            self.accept["source_notes_sha256"],
            sha(B / "FIRST_SECOND_ORIGINAL_CLXIX_HOUSES_21_NOTES_V1.json"),
        )
        self.assertEqual(
            self.accept["source_witness_sha256"],
            sha(B / "PHOTO_ELEVENTH_1647_1659_SOURCE_WITNESS_V1.json"),
        )
        self.assertEqual(self.accept["rules_sha256"], sha(B / "RULES.json"))
        self.assertEqual(len(self.proof["source_row_proofs"]), 21)


def one_row_test(i):
    def test(self):
        row = self.notes[i]
        rule = self.rules["rules"][i]
        self.assertEqual(row["id"], f"R{12705 + i}")
        self.assertEqual(row["id"], rule["id"])
        self.assertTrue(row["physical_original_edition_read_by_one_reader"])
        self.assertFalse(row["runtime_promoted"])
        self.assertFalse(rule["runtime_model_promoted"])

    return test


for n in range(21):
    setattr(OriginalCLXIXHouseSource, f"test_original_source_row_{n + 1:02d}", one_row_test(n))


if __name__ == "__main__":
    unittest.main()
