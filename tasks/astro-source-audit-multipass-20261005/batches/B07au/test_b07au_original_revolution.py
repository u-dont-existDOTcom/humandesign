"""Physical Lilly 1647/1659 CLXXII ending and independent CLXXIII boundary."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class RevolutionBoundary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = load(B / "ORIGINAL_CLXXII_CHART_COMPARISON_AND_NEXT_CLXXIII_V1.json")
        cls.rules = load(B / "RULES.json")
        cls.accept = load(B / "ACCEPTANCE.json")
        cls.prep = load(B / "SOURCE_EVIDENCE_PREP_ONLY_V1.json")

    def test_source_original_1647_wellcome_full_sha(self):
        self.assertEqual(
            self.doc["original_full_first_edition_PDF_SHA256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_original_first_second_editions_six_photo_hashes(self):
        items = self.doc["source_new_edition_photos"]
        self.assertEqual(len(items), 6)
        for k, v in items.items():
            path = ROOT / v["repository_path"]
            self.assertEqual(path.stat().st_size, v["bytes"], k)
            self.assertEqual(sha(path), v["sha256"], k)

    def test_first_four_prepared_images_not_mutated(self):
        self.assertEqual(len(self.prep["historical_first_edition_source_photographs"]), 4)
        for r in self.prep["historical_first_edition_source_photographs"]:
            path = B / r["relative_evidence_file"]
            self.assertEqual(sha(path), r["sha256"])
            self.assertEqual(path.stat().st_size, r["exact_bytes"])

    def test_exact_new_Historical_15_source_record_ids(self):
        self.assertEqual(self.rules["record_count"], 15)
        self.assertEqual(self.doc["new_documentary_historical_source_notes"], 15)
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(12789, 12804))
        )
        self.assertEqual(self.accept["next_original_R"], "R12804")

    def test_first_CLXXII_end_p737_next_CLXXIII_start_p738(self):
        self.assertTrue(self.doc["source_CLXXII_physically_covered_through_original_pdf_771"])
        self.assertTrue(self.doc["separate_source_next_CLXXIII_heading_starts_pdf_772"])
        self.assertEqual(self.doc["records"][-1]["original_pdf_frames"], [772])
        self.assertEqual(self.accept["next_original_pdf"], 772)
        self.assertEqual(self.accept["next_chapter"], "CLXXIII")

    def test_source_exact_labeled_chapter_no_duplicate_source_prediction(self):
        self.assertEqual(self.doc["records"][-1]["role"], "separate_next_CLXXIII_heading")
        self.assertFalse(self.doc["source_full_1647_solar_return_accurate_chart_engine_verified"])
        self.assertFalse(self.doc["critical_source_edition_expert_collation_complete"])

    def test_historical_source_health_moral_wealth_claims_not_person(self):
        for r in self.doc["records"]:
            self.assertFalse(r["historical_personal_health_wealth_marriage_crime_claim_validated"])
            self.assertFalse(r["independently_tested_actual_human_prediction"])
            self.assertFalse(r["runtime_promoted"])

    def test_source_contextual_natal_annual_comparison(self):
        roles = {r["role"] for r in self.doc["records"]}
        self.assertTrue(
            {
                "compare_birth_to_revolution",
                "house_cusps_and_lords",
                "return_natal_ascendant_matching",
                "annual_asc_lord_combust",
                "natal_moon_strength_qualified_exception",
            }.issubset(roles)
        )

    def test_previous_historical_source_registry_is_unchanged(self):
        x = load(WEST)
        c = load(CHINA)
        self.assertEqual(x["records_count"], 12788)
        self.assertEqual(x["batches"][-1]["id"], "B07at")
        self.assertEqual(x["next"]["pdf_page"], 770)
        self.assertEqual(c["sum_source_annotations"], 355)

    def test_risk_and_accepted_sha(self):
        self.assertEqual(
            self.accept["new_source_SHA256"],
            sha(B / "ORIGINAL_CLXXII_CHART_COMPARISON_AND_NEXT_CLXXIII_V1.json"),
        )
        self.assertEqual(self.accept["rules_SHA256"], sha(B / "RULES.json"))
        self.assertEqual(self.doc["independent_real_human_prediction_validations"], 0)
        self.assertEqual(self.doc["runtime_promotions"], 0)


def one_original_note(idx):
    def test(self):
        raw = self.doc["records"][idx]
        rule = self.rules["rules"][idx]
        self.assertEqual(raw["record_number"], 12789 + idx)
        self.assertEqual(raw["id"], rule["id"])
        self.assertEqual(raw["role"], rule["role"])
        self.assertEqual(raw["original_pdf_frames"], rule["original_pdf_frames"])
        self.assertFalse(rule["runtime_model_promoted"])

    return test


for i in range(15):
    setattr(RevolutionBoundary, f"test_original_note_{i + 1:02d}", one_original_note(i))

if __name__ == "__main__":
    unittest.main()
