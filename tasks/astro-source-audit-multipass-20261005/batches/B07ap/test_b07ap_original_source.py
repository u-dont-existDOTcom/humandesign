"""Original 1647 and independent 1659 CLXVIII source and year-ruler example."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
W = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
C = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


class FirstOriginalCLXVIII(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = j(B / "CLXVIII_ORIGINAL_SOURCE_JUDGMENT_33_NOTES_V1.json")
        cls.rules = j(B / "RULES.json")
        cls.witness = j(B / "ORIGINAL_PHOTOGRAPHIC_WITNESS_V1.json")
        cls.accept = j(B / "ACCEPTANCE.json")
        cls.notes = cls.source["rows"]

    def test_pinned_original_Wellcome_book_source(self):
        self.assertEqual(
            self.source["original_full_Wellcome_1647_PDF_SHA256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_original_both_printed_editions_all_eight_photos(self):
        imgs = self.source["image_sources"]
        self.assertEqual(len(imgs), 8)
        for key, meta in imgs.items():
            file = B / meta["source_relative_file"]
            self.assertEqual(sha(file), meta["sha256"], key)
            self.assertEqual(
                sha(file), self.witness["full_image_sha_and_exact_bytes"][key]["photo_sha256"]
            )
            self.assertEqual(
                file.stat().st_size,
                self.witness["full_image_sha_and_exact_bytes"][key]["source_exact_bytes"],
            )

    def test_first_original_1647_printed726_to729(self):
        self.assertEqual(self.source["source_full_physical_span_1647_PDF"], [760, 761, 762])
        self.assertEqual(self.source["source_next_CHAP_CLXIX_first_printed_PDF"], 763)
        self.assertEqual(self.accept["next_source_printed_chapter"], "CLXIX")

    def test_all_33_ids_contiguous_no_reuse(self):
        self.assertEqual([r["id"] for r in self.notes], [f"R{i}" for i in range(12672, 12705)])
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(12672, 12705))
        )
        self.assertEqual(self.accept["new_historical_source_notes"], 33)
        self.assertEqual(self.rules["record_count"], 33)

    def test_source_year_remainder_sexagesimal_exact_math(self):
        a = self.source["source_example"]
        self.assertEqual(a["radical_pisces_degrees_minutes"], [6, 37])
        self.assertEqual(a["remainder_degrees_minutes"], [23, 23])
        self.assertEqual((30 * 60) - (6 * 60 + 37), 23 * 60 + 23)

    def test_source_day_time_split_lookup_correctly_added(self):
        a = self.source["source_example"]
        self.assertEqual(a["degree_table_23_d_h_m"], [280, 0, 27])
        self.assertEqual(a["minute_table_23_d_h_m"], [4, 16, 1])
        self.assertEqual(a["printed_combined_time_d_h_m"], [284, 16, 28])
        self.assertEqual((280 * 1440 + 27) + (4 * 1440 + 16 * 60 + 1), 284 * 1440 + 16 * 60 + 28)
        self.assertFalse(a["nominal_calendar_independently_verified"])

    def test_multiple_lords_and_source_29June_boundary(self):
        roles = {r["role"] for r in self.notes}
        self.assertIn("two_lords_possible", roles)
        self.assertIn("two_rulers_until_june29", roles)
        self.assertEqual(self.source["source_example"]["first_lord_until_calendar_date"], "June 29")

    def test_contextual_natal_annual_exceptions(self):
        roles = {r["role"] for r in self.notes}
        self.assertIn("natal_vs_annual_lord_strength_reversal", roles)
        self.assertIn("weak_both_benefic_aspects_exception", roles)
        self.assertIn("lord_afflicted_in_both", roles)
        self.assertIn("other_houses_application", roles)
        self.assertIn("concealment_houses_2_6_8_12", roles)

    def test_next_distinct_original_CHAP_CLXIX(self):
        self.assertEqual(self.notes[-2]["role"], "clxix_next_chapter_heading")
        self.assertEqual(self.notes[-1]["role"], "clxix_ascendant_moon_profection_title")
        self.assertEqual(self.accept["next_R"], "R12705")
        self.assertEqual(self.accept["next_source_PDF"], 763)

    def test_priors_chinese_and_western_unmodified(self):
        self.assertEqual(j(W)["records_count"], 12671)
        self.assertEqual(j(W)["batches"][-1]["id"], "B07ao")
        self.assertEqual(j(C)["sum_source_annotations"], 355)

    def test_no_original_critical_or_actual_birth_calendar(self):
        self.assertFalse(self.source["full_expert_diplomatic_comparison_completed"])
        self.assertFalse(self.source["true_solar_time_epoch_lunisolar_engine_verified"])
        self.assertFalse(self.accept["actual_astrology_calendar_model_verified"])
        self.assertFalse(self.accept["original_CLXVIII_philological_critical_edition_verified"])

    def test_historical_health_and_morality_not_predicted(self):
        self.assertTrue(
            self.source["classical_health_and_character_predictions_not_clinically_validated"]
        )
        self.assertEqual(self.source["human_predictions_validated"], 0)
        self.assertEqual(self.source["runtime_promotions"], 0)
        for n in self.notes:
            self.assertFalse(n["real_human_predictive_success"])
            self.assertFalse(n["unsafe_medical_or_financial_inference_authorized"])

    def test_source_exact_hash_and_33_rules(self):
        self.assertEqual(
            self.accept["records_sha256"],
            sha(B / "CLXVIII_ORIGINAL_SOURCE_JUDGMENT_33_NOTES_V1.json"),
        )
        self.assertEqual(
            self.accept["witness_sha256"], sha(B / "ORIGINAL_PHOTOGRAPHIC_WITNESS_V1.json")
        )
        self.assertEqual(self.accept["rules_sha256"], sha(B / "RULES.json"))


def individual_source_note(i):
    def test(self):
        r = self.notes[i]
        rule = self.rules["rules"][i]
        self.assertEqual(r["id"], f"R{12672 + i}")
        self.assertEqual(r["id"], rule["id"])
        self.assertEqual(r["source_original_pdf_frame"], rule["original_pdf_frames"][0])
        self.assertFalse(r["runtime_promoted"])
        self.assertFalse(rule["runtime_model_promoted"])

    return test


for k in range(33):
    setattr(FirstOriginalCLXVIII, f"test_source_note_{12672 + k}", individual_source_note(k))


if __name__ == "__main__":
    unittest.main()
