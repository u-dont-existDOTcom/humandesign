"""Manners CLXXVI 1647/1659 first-edition source, exact photo provenance.

Validates 40 physical-page bound historical source observations, including
the explicitly unsuccessful throat blemish inference. No independent human
prospective study or Natal epoch chart validation.
"""

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


class MannersOriginalEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.photos = j(B / "ORIGINAL_PHOTO_WITNESS_V1.json")
        cls.correction = j(B / "CORRECTED_PHYSICAL_CHAPTER_BOUNDARY_V1.json")
        cls.proposed = j(B / "MANNERS_SOURCE_CANDIDATES_V1.json")
        cls.notes = j(B / "ORIGINAL_1647_1659_MANNERS_40_SOURCE_NOTES_V1.json")
        cls.rules = j(B / "RULES.json")
        cls.accept = j(B / "ACCEPTANCE.json")
        cls.by = {r["role"]: r for r in cls.rules["rules"]}
        cls.records = cls.rules["rules"]

    def test_full_original_1647_book_SHA(self):
        self.assertEqual(
            self.photos["source_full_Wellcome_1647_original_PDF_SHA256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_all_ten_first_and_second_original_edition_photo_SHA_bytes(self):
        self.assertEqual(len(self.photos["source_1647_1659_page_photos"]), 10)
        for key, meta in self.photos["source_1647_1659_page_photos"].items():
            file = ROOT / meta["image_path"]
            self.assertTrue(file.is_file(), key)
            self.assertEqual(file.stat().st_size, meta["bytes"], key)
            self.assertEqual(sha(file), meta["sha256"], key)
            self.assertEqual(int(key[-3:]), meta["original_printed_folio"])
            self.assertIn(meta["original_public_domain_print_source_year"], (1647, 1659))

    def test_corrected_five_physical_pages_source_witness(self):
        self.assertTrue(
            self.photos["original_1647_CLXXVI_ends_pdf783_printed749_before_next_divider"]
        )
        self.assertTrue(self.photos["source_next_printed_CLXXVII_Riches_starts_same_pdf783"])
        self.assertEqual(
            self.photos["first_1647_original_source_folios"], [745, 746, 747, 748, 749]
        )
        self.assertEqual(
            self.photos["separately_typeset_second_1659_original_source_folios"],
            [745, 746, 747, 748, 749],
        )

    def test_original_p748_end_false_provisional_boundary_rejected(self):
        self.assertIn("printed748", self.correction["error_in_prior_provisional_checkpoint"])
        self.assertIn("printed749", self.correction["source_photo_corrected_boundary"])
        self.assertTrue(self.accept["original_1647_first_CLXXVI_source_end_folio749"])
        self.assertEqual(self.accept["next_original_pdf_frame"], 783)
        self.assertEqual(self.accept["next_original_printed_folio"], 749)

    def test_40_contiguous_source_only_R(self):
        self.assertEqual(self.proposed["proposed_count"], 40)
        self.assertEqual(self.notes["historical_annotations_added_if_accepted"], 40)
        self.assertEqual(self.rules["record_count"], 40)
        self.assertEqual([r["id"] for r in self.records], [f"R{i}" for i in range(12901, 12941)])
        self.assertEqual(self.accept["next_original_R"], "R12941")

    def test_exact_original_source_negative_not_relabelled_as_success(self):
        negative = [
            r
            for r in self.records
            if r["historical_claim_category"] == "EXPLICIT_NEGATIVE_OBSERVATION"
        ]
        self.assertEqual(len(negative), 1)
        item = negative[0]
        self.assertEqual(item["role"], "THROAT_MARK_SATURN_NEGATIVE")
        self.assertEqual(item["original_printed_folio"], 748)
        self.assertEqual(item["literal_historical_author_observation"], "I can find none.")
        self.assertTrue(item["historical_author_observes_no_throat_mark"])
        self.assertTrue(item["negative_observation_must_not_be_recoded_as_success"])
        self.assertEqual(self.notes["source_negative_throat_mark_observation_count"], 1)
        self.assertEqual(self.notes["independent_actual_human_forecast_validations"], 0)

    def test_original_1647_is_retrospective_known_person_not_blind_prediction(self):
        self.assertTrue(self.notes["source_author_already_knows_subject_of_example"])
        self.assertTrue(self.rules["historical_subject_known_to_author_not_blinded"])
        self.assertTrue(
            self.notes["source_first_and_second_edition_same_text_not_independent_persons"]
        )
        self.assertFalse(
            self.notes["historical_original_first_printed_1616_chart_era_ephemeris_validated"]
        )

    def test_unumbered_sections_vs_distinct_CLXXVII(self):
        for role in (
            "WIT_UNDERSTANDING_HEADING",
            "FORM_STATURE_HEADING",
            "GENERAL_FORTUNE_HEADING",
        ):
            self.assertEqual(self.by[role]["historical_claim_category"], "SECTION_BOUNDARY")
        self.assertEqual(self.records[-1]["role"], "CLXXVII_RICHES_DIVIDER")
        self.assertEqual(self.records[-1]["historical_claim_category"], "NEXT_CHAPTER_BOUNDARY")
        self.assertEqual(self.records[-1]["original_printed_folio"], 749)
        self.assertEqual(self.accept["next_original_physically_distinct_chapter"], "CLXXVII")

    def test_first_new_record_starts_after_source_R12900(self):
        prior = j(WEST)
        self.assertEqual(prior["records_count"], 12900)
        self.assertEqual(prior["batches"][-1]["id"], "B07ax")
        self.assertEqual(prior["next"]["chapter"], "CLXXVI")
        self.assertEqual(prior["next"]["pdf_page"], 779)
        self.assertEqual(self.records[0]["id"], "R12901")

    def test_chinese_V7_not_mutated(self):
        chinese = j(CHINA)
        self.assertEqual(chinese["sum_source_annotations"], 355)
        self.assertEqual(chinese["systems"][0]["accepted_source_annotations"], 154)
        self.assertEqual(chinese["systems"][1]["accepted_source_annotations"], 201)
        self.assertEqual(self.accept["Chinese_V7_retained"], 355)

    def test_photo_witness_source_data_hash_and_note_fidelity(self):
        self.assertEqual(
            self.notes["photo_witness_SHA256"], sha(B / "ORIGINAL_PHOTO_WITNESS_V1.json")
        )
        self.assertEqual(
            self.notes["physical_chapter_boundary_correction_SHA256"],
            sha(B / "CORRECTED_PHYSICAL_CHAPTER_BOUNDARY_V1.json"),
        )
        self.assertEqual(
            self.accept["source_data_SHA256"],
            sha(B / "ORIGINAL_1647_1659_MANNERS_40_SOURCE_NOTES_V1.json"),
        )
        self.assertEqual(self.accept["rules_SHA256"], sha(B / "RULES.json"))

    def test_no_independent_person_outcomes_or_live_rules(self):
        self.assertEqual(self.notes["independent_actual_human_forecast_validations"], 0)
        self.assertEqual(self.notes["runtime_model_promotions"], 0)
        self.assertEqual(self.rules["empirical_real_human_outcomes_validated"], 0)
        for note in self.records:
            self.assertFalse(note["source_historical_character_claim_empirically_validated"])
            self.assertFalse(note["source_actual_behavior_medical_morality_wealth_verified"])
            self.assertFalse(note["independently_real_person_predictive_validation"])
            self.assertFalse(note["high_stakes_real_person_risk_classification_authorized"])
            self.assertFalse(note["runtime_model_promoted"])


def one_source_record(i):
    def test(self):
        r = self.records[i]
        old = self.proposed["records"][i]
        self.assertEqual(r["id"], old["id"])
        self.assertEqual(r["record_number"], 12901 + i)
        self.assertEqual(r["role"], old["role"])
        self.assertEqual(r["original_printed_folio"], old["source_printed_folio"])
        self.assertEqual(r["original_pdf_frames"], [old["original_1647_PDF_frame"]])
        self.assertEqual(r["second_edition_DjVu_frame"], old["original_1659_DjVu_frame"])
        self.assertEqual(
            r["source_original_1647_photo_SHA256"],
            self.photos["source_1647_1659_page_photos"][
                f"1647_printed_{r['original_printed_folio']}"
            ]["sha256"],
        )
        self.assertFalse(r["runtime_model_promoted"])

    return test


for n in range(40):
    setattr(MannersOriginalEvidence, f"test_original_source_{12901 + n}", one_source_record(n))


if __name__ == "__main__":
    unittest.main()
