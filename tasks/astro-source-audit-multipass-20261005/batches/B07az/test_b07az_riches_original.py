"""Original 1647 and 1659 Riches known-merchant history; no human forecast claims."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class LillyOriginalRiches(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = j(B / "ORIGINAL_1647_1659_RICHES_29_SOURCE_NOTES_V1.json")
        cls.rules = j(B / "RULES.json")
        cls.accept = j(B / "ACCEPTANCE.json")
        cls.records = cls.rules["rules"]
        cls.by = {r["role"]: r for r in cls.records}

    def test_full_original_book_binary_identity(self):
        self.assertEqual(
            self.data["original_full_1647_PDF_sha256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_six_source_photo_binaries_first_and_second(self):
        photos = self.data["original_1647_and_1659_six_source_photo_witnesses"]
        self.assertEqual(set(photos), {"749", "750", "751"})
        for folio, records in photos.items():
            for category, p in records.items():
                file = ROOT / p["relative_path"]
                self.assertEqual(sha(file), p["sha256"], (folio, category))
                self.assertEqual(file.stat().st_size, p["bytes"], folio)
                self.assertGreater(file.stat().st_size, 150000)
                self.assertEqual(
                    p.get("original_pdf_frame", p.get("original_djvu_page")),
                    int(folio) + (34 if category == "first_original_1647" else 29),
                )

    def test_1647_source_prev_page_photo_reused_without_modification(self):
        prior = j(B.parent / "B07ay/ORIGINAL_PHOTO_WITNESS_V1.json")
        curr = self.data["original_1647_and_1659_six_source_photo_witnesses"]["749"]
        self.assertEqual(
            prior["source_1647_1659_page_photos"]["1647_printed_749"]["sha256"],
            curr["first_original_1647"]["sha256"],
        )
        self.assertEqual(
            prior["source_1647_1659_page_photos"]["1659_printed_749"]["sha256"],
            curr["independently_typeset_1659"]["sha256"],
        )

    def test_bounded_new_canonical_id_range_without_recount(self):
        self.assertEqual(len(self.records), 29)
        self.assertEqual(self.data["historical_documentary_annotation_count"], 29)
        self.assertEqual([r["id"] for r in self.records], [f"R{n}" for n in range(12941, 12970)])
        self.assertEqual(self.accept["new_source_only_historical_annotations"], 29)
        self.assertEqual(self.accept["next_R"], "R12970")

    def test_physical_original_boundaries_not_adjacent_chapters(self):
        self.assertEqual(self.data["actual_chapter_folios"], [749, 750, 751])
        self.assertEqual(self.data["actual_1647_PDF_frames"], [783, 784, 785])
        self.assertEqual(self.records[0]["role"], "CHAPTER_HEAD")
        self.assertEqual(self.records[-1]["role"], "CLXXVIII_BRETHREN_BOUNDARY")
        self.assertEqual(self.records[-1]["original_pdf_frames"], [785])
        self.assertEqual(self.accept["next_chapter"], "CLXXVIII")
        self.assertTrue(self.data["next_original_CLXXVIII_starts_shared_folio751"])

    def test_original_1647_cusp_print_not_modern_derivative(self):
        self.assertEqual(
            self.data["original_fixed_second_cusp_print_Aquarius_degree_minute"], [23, 30]
        )
        self.assertEqual(
            self.data["secondary_searchable_derivative_truncates_minutes"], "Aquarius 23.3"
        )
        self.assertFalse(self.by["AQUARIUS_23_30"]["source_era_1616_natal_ephemeris_verified"])

    def test_riches_and_kin_legal_allegations_untested(self):
        for role in (
            "FORGED_WILL_LAWSUIT",
            "LEGACY_LAWSUIT_SOUTH_NODE",
            "PATRIMONY_DEPLETION_SISTER_KIN",
            "LATER_INCREASE_SATURN_NORTH_NODE",
        ):
            self.assertTrue(self.by[role]["this_is_not_observed_independently_verified_outcome"])
            self.assertFalse(self.by[role]["source_merchant_biography_independently_verified"])

    def test_single_known_merchant_not_29_validated_subjects(self):
        self.assertTrue(self.data["subject_was_already_known_to_original_author"])
        self.assertTrue(self.data["source_is_retrospective_unblinded_individual_reading"])
        self.assertEqual(
            self.data["independent_biographical_wealth_predicted_outcomes_validated"], 0
        )
        self.assertEqual(self.rules["empirical_actual_person_outcomes_validated"], 0)

    def test_source_critical_and_astrological_model_not_validated(self):
        self.assertFalse(self.data["complete_independent_critical_edition_expert_review"])
        self.assertFalse(self.data["original_17th_century_natal_chart_engine_verified"])
        self.assertFalse(self.rules["natal_1616_chart_engine_verified"])
        self.assertEqual(self.data["runtime_promotions"], 0)

    def test_previous_published_indexes_unchanged(self):
        western = j(WEST)
        china = j(CHINA)
        self.assertEqual(western["records_count"], 12940)
        self.assertEqual(western["batches"][-1]["id"], "B07ay")
        self.assertEqual(western["next"]["chapter"], "CLXXVII")
        self.assertEqual(western["next"]["pdf_page"], 783)
        self.assertEqual(china["sum_source_annotations"], 355)
        self.assertEqual(self.accept["Chinese_V7_retained"], 355)

    def test_source_and_rules_frozen_sha(self):
        self.assertEqual(
            self.accept["source_photo_witness_SHA256"],
            sha(B / "ORIGINAL_1647_1659_RICHES_29_SOURCE_NOTES_V1.json"),
        )
        self.assertEqual(self.accept["rules_SHA256"], sha(B / "RULES.json"))

    def test_no_person_level_high_stakes_claim_authorized(self):
        for rec in self.records:
            self.assertTrue(rec["historic_subject_already_known_to_Lilly"])
            self.assertFalse(rec["source_merchant_biography_independently_verified"])
            self.assertFalse(rec["traditional_chart_to_wealth_claim_falsification_evaluated"])
            self.assertFalse(rec["independent_real_human_prediction_validated"])
            self.assertFalse(rec["runtime_model_promoted"])


def check_row(i):
    def test(self):
        row = self.records[i]
        self.assertEqual(row["record_number"], 12941 + i)
        self.assertEqual(row["id"], f"R{12941 + i}")
        self.assertEqual(row["original_pdf_frames"], [row["original_printed_folio"] + 34])
        self.assertTrue(row["this_is_not_observed_independently_verified_outcome"])
        self.assertFalse(row["runtime_model_promoted"])

    return test


for i in range(29):
    setattr(LillyOriginalRiches, f"test_source_{i + 1:02d}", check_row(i))


if __name__ == "__main__":
    unittest.main()
