"""Original 1647/1659 photo source and opening partial CLXVI rule acceptance tests."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"
ORIGINAL = B.parent / "B07x"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class CLXVIPartialOriginalSources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notes = j(B / "CLXVI_OPENING_SOURCE_PHOTO_29_NOTES_V1.json")
        cls.witness = j(B / "FIRST_SECOND_ORIGINAL_708_710_SOURCE_WITNESS_V1.json")
        cls.rules = j(B / "RULES.json")
        cls.accept = j(B / "ACCEPTANCE.json")
        cls.index = j(WEST)
        cls.china = j(CHINA)
        cls.by = {x["id"]: x for x in cls.rules["rules"]}

    def test_1647_original_first_print_full_source_SHA(self):
        self.assertEqual(
            self.witness["full_1647_original_pdf_sha256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )
        self.assertEqual(
            self.notes["whole_original_pdf_sha256"], self.witness["full_1647_original_pdf_sha256"]
        )

    def test_exact_three_original_source_photo_hashes(self):
        photos = self.witness["first_edition_source_photographs"]
        self.assertEqual(list(photos), ["742", "743", "744"])
        for key, item in photos.items():
            path = ROOT / item["file"]
            self.assertEqual(sha(path), item["sha256"])
            self.assertEqual(path.stat().st_size, item["bytes"])
            self.assertEqual(item["original_pdf_frame"], int(key))
            self.assertEqual(item["original_printed_folio"], int(key) - 34)

    def test_distinct_second_1659_printed_710_image_sha(self):
        photo = self.witness["independent_1659_typeset_photo"]
        self.assertEqual(photo["djvu_page"], 739)
        self.assertEqual(photo["printed_folio"], 710)
        file = ROOT / photo["file"]
        self.assertEqual(sha(file), photo["sha256"])
        self.assertGreater(file.stat().st_size, 200000)

    def test_physical_print_vs_searchable_transcription_conflict(self):
        self.assertEqual(self.witness["original_printing_1647_next_day_sun_longitude"], [7, 36])
        self.assertEqual(self.witness["second_printing_1659_next_day_sun_longitude"], [7, 36])
        self.assertEqual(
            self.witness["modern_derivative_transcription_next_day_sun_longitude"], [7, 37]
        )
        self.assertEqual(
            self.witness["source_edition_comparison_status"],
            "FIRST_AND_SECOND_PHYSICAL_PRINT_CONFIRM_7_36",
        )
        last = self.rules["rules"][-1]
        self.assertEqual(last["original_printed_next_day_sun_longitude_degrees_minutes"], [7, 36])
        self.assertEqual(last["modern_derivative_mistranscribed_next_day_sun_longitude"], [7, 37])

    def test_29_reversible_1647_partial_historical_rules(self):
        self.assertEqual(self.rules["record_count"], 29)
        self.assertEqual(len(self.rules["rules"]), 29)
        self.assertEqual(self.notes["historical_source_claim_count"], 29)
        self.assertEqual(len(self.witness["photographic_source_note_receipts"]), 29)
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(12473, 12502))
        )
        self.assertEqual(self.rules["first_record"], "R12473")
        self.assertEqual(self.rules["last_record"], "R12501")

    def test_first_heading_is_distinct_from_prior_fortuna(self):
        self.assertEqual(self.rules["rules"][0]["role"], "boundary")
        self.assertEqual(self.rules["rules"][0]["original_pdf_frames"], [742])
        self.assertEqual(self.index["batches"][-1]["id"], "B07w")
        self.assertEqual(self.index["next"]["chapter"], "CLXVI")
        self.assertEqual(self.index["next"]["pdf_page"], 742)

    def test_printed_year_rate_basic_original_math(self):
        roles = {r["role"]: r for r in self.rules["rules"]}
        for role in (
            "one_degree_year",
            "one_min_six_days",
            "natal_asc",
            "mars_diff",
            "mars_opp",
            "sun_rate",
            "sun_birth",
            "sun_ra_birth",
            "sun_ra_next",
        ):
            self.assertIn(role, roles)
        self.assertIn("54", roles["sun_rate"]["source_anchor_not_diplomatic"])
        self.assertEqual(186 * 60 + 58 - (186 * 60 + 4), 54)

    def test_historical_age_caveats_included_not_prediction_success(self):
        roles = {r["role"] for r in self.rules["rules"]}
        self.assertTrue(
            {"age", "infant_marriage", "old_parenthood", "birth_region", "collective"}.issubset(
                roles
            )
        )
        self.assertEqual(self.rules["empirical_real_person_predictions_validated"], 0)

    def test_index_and_parallel_chinese_pre_acceptance_untouched(self):
        self.assertEqual(self.index["records_count"], 12472)
        self.assertEqual(self.china["sum_source_annotations"], 262)
        self.assertEqual(self.accept["prior_Lilly"], 12472)
        self.assertEqual(self.accept["parallel_Chinese_V5"], 262)
        self.assertEqual(self.rules["runtime_promotions"], 0)

    def test_witness_has_all_29_anchor_position_proofs(self):
        for note, proof, rule in zip(
            self.notes["records"],
            self.witness["photographic_source_note_receipts"],
            self.rules["rules"],
            strict=True,
        ):
            self.assertEqual(note["id"], proof["record_id"])
            self.assertEqual(note["id"], rule["candidate_source_note_id"])
            self.assertEqual(note["original_1647_pdf_frame"], proof["source_photo_pdf_frame"])
            self.assertEqual(
                note["derivative_search_text_anchor"], proof["modern_derivative_anchor"]
            )
            self.assertEqual(
                hashlib.sha256(note["derivative_search_text_anchor"].encode()).hexdigest(),
                proof["derivative_phrase_utf8_sha256"],
            )

    def test_true_epoch_direction_algorithm_not_claimed(self):
        self.assertFalse(self.rules["original_full_chapter_CLXVI_completed"])
        self.assertFalse(
            self.rules["all_372_1647_original_annual_rate_glyphs_independently_verified"]
        )
        self.assertFalse(self.rules["historical_arc_to_age_engine_verified"])
        self.assertTrue(self.rules["no_read_numbered_chapter_165_added_yet"])
        self.assertEqual(self.notes["new_canonical_source_R_records_accepted"], 0)

    def test_next_after_partial_still_same_numbered_chapter(self):
        self.assertEqual(self.accept["next_original_source_id"], "R12502")
        self.assertEqual(self.accept["next_original_source_pdf_frame"], 745)
        self.assertEqual(self.accept["next_heading_printed_numeral"], "CLXVI")
        self.assertFalse(self.accept["diplomatic_1647_CLXVI_full_chapter_complete"])

    def test_ALL_high_stakes_prognoses_not_authorized(self):
        for r in self.rules["rules"]:
            self.assertTrue(r["historical_source_documented"])
            self.assertFalse(r["independent_real_event_timing_accuracy_validated"])
            self.assertFalse(r["independent_health_or_death_prediction_validated"])
            self.assertFalse(r["independent_relationship_or_financial_prediction_validated"])
            self.assertFalse(r["independent_faith_personality_or_crime_label_validated"])
            self.assertFalse(r["real_person_health_safety_social_status_advice_authorized"])
            self.assertFalse(r["runtime_model_promoted"])

    def test_record_SHA_preflight(self):
        self.assertEqual(self.accept["rules_sha256"], sha(B / "RULES.json"))
        self.assertEqual(
            self.accept["source_witness_sha256"],
            sha(B / "FIRST_SECOND_ORIGINAL_708_710_SOURCE_WITNESS_V1.json"),
        )


def single_note_test(i):
    def test(self):
        source = self.notes["records"][i]
        rule = self.rules["rules"][i]
        self.assertEqual(rule["id"], f"R{12473 + i}")
        self.assertEqual(rule["record_number"], 12473 + i)
        self.assertEqual(rule["role"], source["role"])
        self.assertEqual(rule["original_pdf_frames"], [source["original_1647_pdf_frame"]])
        self.assertTrue(rule["historical_source_documented"])
        self.assertFalse(rule["runtime_model_promoted"])

    return test


for number in range(29):
    setattr(
        CLXVIPartialOriginalSources,
        f"test_partial_source_{number + 1:03d}",
        single_note_test(number),
    )


if __name__ == "__main__":
    unittest.main()
