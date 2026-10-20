"""Source-specific 1647/1659 Brethren known-case leakage and sibling-count test."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class OriginalBrethren(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = j(B / "ORIGINAL_1647_1659_BRETHREN_22_SOURCE_NOTES_V1.json")
        cls.rules = j(B / "RULES.json")
        cls.accept = j(B / "ACCEPTANCE.json")
        cls.by = {r["role"]: r for r in cls.rules["rules"]}

    def test_pinned_original_Wellcome_book_sha(self):
        self.assertEqual(
            self.source["full_original_1647_Wellcome_pdf_SHA256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_four_first_second_photos_sha_and_bytes(self):
        photos = self.source["original_two_editions_four_source_page_images"]
        self.assertEqual(set(photos), {"751", "752"})
        for folio, parts in photos.items():
            for _, meta in parts.items():
                file = ROOT / meta["relative_original_source_image"]
                self.assertTrue(file.is_file())
                self.assertEqual(meta["sha256"], sha(file))
                self.assertEqual(meta["bytes"], file.stat().st_size)
                self.assertGreater(meta["bytes"], 200000)
                self.assertEqual(meta["original_printed_folio"], int(folio))

    def test_shared_prior_riches_page_not_edited(self):
        old = j(B.parent / "B07az/ORIGINAL_1647_1659_RICHES_29_SOURCE_NOTES_V1.json")
        witness = old["original_1647_and_1659_six_source_photo_witnesses"]["751"]
        now = self.source["original_two_editions_four_source_page_images"]["751"]
        self.assertEqual(witness["first_original_1647"]["sha256"], now["first_1647"]["sha256"])
        self.assertEqual(
            witness["independently_typeset_1659"]["sha256"], now["typeset_1659"]["sha256"]
        )

    def test_original_brethren_source_spans_and_boundary(self):
        self.assertEqual(self.source["original_physical_first_edition_printed_folios"], [751, 752])
        self.assertEqual(self.source["original_first_PDF_frames"], [785, 786])
        self.assertEqual(self.rules["rules"][0]["role"], "CHAPTER_HEAD")
        self.assertEqual(self.rules["rules"][-1]["role"], "CLXXIX_PARENTS_BOUNDARY")
        self.assertEqual(self.accept["next_original_physically_distinct_chapter"], "CLXXIX")
        self.assertEqual(self.accept["next_original_pdf"], 786)

    def test_source_Ptolemy_few_siblings_vs_author_report_seven(self):
        self.assertTrue(self.source["source_strict_ptolemy_interpretation_predicts_few_siblings"])
        self.assertEqual(self.source["source_author_reports_sibling_count_brothers"], 7)
        self.assertEqual(self.source["source_author_reports_sibling_count_sisters"], 1)
        self.assertTrue(
            self.source["source_known_seven_brothers_context_posthoc_reconciled_with_extra_factors"]
        )
        self.assertIn(
            "not many",
            self.by["PTOLEMY_FEW_BRETHREN_IF_STRICT"]["source_historical_interpretation"],
        )

    def test_historical_count_report_not_genealogically_validated(self):
        self.assertEqual(self.source["reported_sibling_count_independent_validation_count"], 0)
        self.assertTrue(
            self.rules[
                "author_retrospective_seven_brother_one_sister_report_not_external_validation"
            ]
        )
        self.assertTrue(self.source["source_explicitly_warns_exact_sibling_counts_difficult"])
        self.assertEqual(self.rules["real_human_blind_prediction_successes"], 0)

    def test_sister_health_longevity_not_predictions_of_known_people(self):
        x = self.by["SISTER_SICKLY_SHORTER_LIFE"]
        self.assertFalse(x["historical_person_biography_verified_independently"])
        self.assertFalse(x["high_stakes_health_lifespan_or_relationship_risk_advice_authorized"])
        self.assertEqual(self.source["sister_health_mortality_claims_independently_verified"], 0)

    def test_uncle_estate_dispute_not_verified(self):
        self.assertIn("UNCLES_ESTATE_FUTURE_CONTROVERSY", self.by)
        self.assertFalse(
            self.by["UNCLES_ESTATE_FUTURE_CONTROVERSY"][
                "this_is_heldout_real_person_prediction_accuracy"
            ]
        )
        self.assertEqual(self.source["sibling_estate_disputes_independently_verified"], 0)

    def test_22_exactly_consecutive_documentary_notes(self):
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(12970, 12992))
        )
        self.assertEqual(self.accept["historical_source_note_count"], 22)
        self.assertEqual(self.accept["next_R"], "R12992")

    def test_previous_historical_index_not_advanced_during_draft(self):
        self.assertEqual(j(WEST)["records_count"], 12969)
        self.assertEqual(j(WEST)["batches"][-1]["id"], "B07az")
        self.assertEqual(j(WEST)["next"]["chapter"], "CLXXVIII")
        self.assertEqual(j(CHINA)["sum_source_annotations"], 355)

    def test_original_source_meanings_not_modern_validated_chart_engine(self):
        self.assertFalse(self.source["historical_natal_chart_engine_verified"])
        self.assertFalse(self.source["independent_expert_original_text_collation_complete"])
        self.assertEqual(self.source["independent_prospective_real_human_prediction_successes"], 0)
        self.assertEqual(self.source["runtime_promotions"], 0)
        self.assertTrue(all(not x["runtime_model_promoted"] for x in self.rules["rules"]))

    def test_exact_record_sha_receipts(self):
        self.assertEqual(
            self.accept["source_notes_sha256"],
            sha(B / "ORIGINAL_1647_1659_BRETHREN_22_SOURCE_NOTES_V1.json"),
        )
        self.assertEqual(self.accept["rules_sha256"], sha(B / "RULES.json"))


def one_source_note(i):
    def test(self):
        item = self.rules["rules"][i]
        self.assertEqual(item["id"], f"R{12970 + i}")
        self.assertEqual(item["original_pdf_frames"], [item["original_printed_folio"] + 34])
        self.assertTrue(item["natal_case_was_known_to_Lilly"])
        self.assertFalse(item["source_prospective_prediction_frozen_before_human_outcomes"])
        self.assertFalse(item["runtime_model_promoted"])

    return test


for i in range(22):
    setattr(OriginalBrethren, f"test_brethren_note_{i + 1:02d}", one_source_note(i))


if __name__ == "__main__":
    unittest.main()
