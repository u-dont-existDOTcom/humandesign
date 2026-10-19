"""Original 1647/1659 single-page transit chapter source integrity.

Checks original printed-source binary provenance, repeatable transcription
locators, explicit edition disagreement and fail-closed human prediction flags.
The automated assertions do NOT constitute a second human paleographic read.
"""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
PARENT = B.parent / "B07av"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class OriginalTransitSources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = j(B / "ORIGINAL_CLXXIV_TRANSITS_TWO_EDITIONS_SOURCE_V1.json")
        cls.rules = j(B / "RULES.json")
        cls.accept = j(B / "ACCEPTANCE.json")
        cls.checkpoint = j(B / "RECOVERY_CHECKPOINT.json")
        cls.finder = (B / "SECONDARY_SEARCH_NAVIGATOR_TRANSITS.txt").read_text(encoding="utf-8")
        cls.rows = cls.source["records"]
        cls.by = {r["source_section_role"]: r for r in cls.rows}

    def test_first_original_full_book_fingerprint(self):
        self.assertEqual(
            self.source["source_original_1647_full_book_pdf_sha256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_actual_original_two_editions_photo_SHA_and_byte(self):
        photographs = self.source["original_photo_witnesses"]
        self.assertEqual(len(photographs), 4)
        for label, record in photographs.items():
            path = ROOT / record["path"]
            self.assertTrue(path.is_file(), label)
            self.assertGreater(path.stat().st_size, 200000)
            self.assertEqual(path.stat().st_size, record["exact_bytes"])
            self.assertEqual(sha(path), record["SHA256"])

    def test_original_1647_heading_is_CLXXIIII_and_1659_CLXXIV(self):
        self.assertEqual(self.source["physical_original_1647_chapter_printed"], "CLXXIIII")
        self.assertEqual(self.source["independently_typeset_1659_original_printed"], "CLXXIV")
        self.assertEqual(self.source["editorial_normalized_ordinal"], 174)
        parent = j(PARENT / "SOURCE_CLXXIV_ORIGINAL_TWO_EDITION_NUMERAL_V1.json")
        self.assertEqual(parent["original_1647_literal_chapter_heading"], "CHAP. CLXXIIII.")
        self.assertEqual(
            parent["independently_typeset_1659_literal_chapter_heading"], "CHAP. CLXXIV."
        )

    def test_transit_chapter_fits_one_original_1647_page(self):
        self.assertEqual(self.source["original_1647_transit_one_page_pdf_frame"], 775)
        self.assertEqual(self.source["original_1647_transit_one_page_printed_folio"], 741)
        self.assertTrue(self.source["source_all_original_chapter_physical_pages_examined"])
        self.assertEqual(self.rules["body_pdf_frames"], [775])
        self.assertTrue(self.rules["physical_chapter_CLXXIV_source_span_covered"])

    def test_next_distinct_CLXXV_merchants_chart_not_same_chapter(self):
        self.assertEqual(self.source["original_1647_next_distinct_CLXXV_pdf_frame"], 776)
        self.assertEqual(self.source["independent_1659_next_CLXXV_djvu_frame"], 771)
        last = self.by["boundary_CLXXV_nativity"]
        self.assertEqual(last["next_printed_chapter_numeral"], "CLXXV")
        self.assertTrue(last["source_next_chapter_first_substantive_record_NOT_yet_accepted"])

    def test_secondary_searchable_text_known_unauthoritative(self):
        self.assertEqual(
            sha(B / "SECONDARY_SEARCH_NAVIGATOR_TRANSITS.txt"),
            self.source["non_authoritative_searchable_text_sha256"],
        )
        self.assertIn("The Transit of Jupiter or Mars", self.finder)
        self.assertIn("for two or three dayes", self.finder)

    def test_jupiter_venus_original_vs_secondary_wrong_mars(self):
        row = self.by["Jupiter_Venus_on_ascendant"]
        self.assertEqual(row["original_1647_and_1659_first_source_planets"], ["Jupiter", "Venus"])
        self.assertEqual(row["secondary_searchable_text_wrong_planets"], ["Jupiter", "Mars"])
        self.assertFalse(row["literal_original_matches_secondary_text"])
        self.assertTrue(
            self.source[
                "original_1647_1659_Jupiter_or_Venus_ascendant_not_secondary_Jupiter_or_Mars"
            ]
        )

    def test_mars_duration_original_two_printing_distinction(self):
        row = self.by["Mars_duration_edition_variant"]
        self.assertEqual(row["duration_magnitude_in_both_original_editions"], [2, 3])
        self.assertEqual(row["original_first_1647_duration_unit"], "dayes")
        self.assertEqual(row["original_second_1659_duration_unit"], "yeares")
        self.assertEqual(self.source["1647_printed_Mars_ascendant_duration"], "2 or 3 days")
        self.assertEqual(self.source["1659_printed_Mars_ascendant_duration"], "2 or 3 years")
        self.assertTrue(row["edition_variation_does_not_demonstrate_actual_effect"])

    def test_planet_targets_node_fortune_and_aspects_kept(self):
        for key in ("natal_cusps", "natal_planets_nodes_fortune", "natal_aspects"):
            self.assertIn(key, self.by)
        self.assertIn(
            "North Node",
            self.by["natal_planets_nodes_fortune"]["derivative_locator_NOT_original_transcription"],
        )
        self.assertIn(
            "South Node",
            self.by["natal_planets_nodes_fortune"]["derivative_locator_NOT_original_transcription"],
        )
        self.assertIn(
            "Square", self.by["natal_aspects"]["derivative_locator_NOT_original_transcription"]
        )

    def test_historical_house_examples_not_12_invented_outcomes(self):
        self.assertIn("Jupiter_Venus_second_cusp", self.by)
        self.assertIn("Jupiter_Venus_third_cusp_kin", self.by)
        self.assertIn("other_houses_analogy", self.by)
        self.assertEqual(len(self.rows), 22)

    def test_historical_1647_completion_date_not_human_outcome(self):
        self.assertIn("14 August 1647", self.source["date_of_source_closing_signature"])
        self.assertIn("composition statement", self.source["date_of_source_closing_signature"])

    def test_photographic_source_glyph_critical_expert_review_pending(self):
        self.assertFalse(self.source["source_critical_professional_collation_complete"])
        self.assertFalse(self.source["original_epoch_solar_and_transit_ephemeris_validated"])
        self.assertFalse(self.rules["critical_edition_professional_corroboration_complete"])

    def test_exact_contiguous_historical_source_R_ids_and_next_cursor(self):
        self.assertEqual([r["id"] for r in self.rows], [f"R{x}" for x in range(12847, 12869)])
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(12847, 12869))
        )
        self.assertEqual(self.accept["next_original_R"], "R12869")
        self.assertEqual(self.accept["next_original_PDF"], 776)

    def test_prior_source_registry_not_mutated_by_extraction(self):
        self.assertEqual(j(WEST)["records_count"], 12846)
        self.assertEqual(j(WEST)["batches"][-1]["id"], "B07av")
        self.assertEqual(j(CHINA)["sum_source_annotations"], 355)
        self.assertEqual(self.accept["Lilly_before"], 12846)
        self.assertEqual(self.accept["Chinese_V7_retained"], 355)

    def test_no_independent_actual_human_success_claim(self):
        self.assertEqual(self.source["independent_real_human_predictions_validated"], 0)
        self.assertEqual(self.source["runtime_promotions"], 0)
        for r in self.rows:
            self.assertTrue(r["source_one_reader_original_printing_observation"])
            self.assertFalse(r["source_critical_two_independent_human_readers_verified"])
            self.assertFalse(r["full_ephemeris_calendar_natal_transits_engine_verified"])
            self.assertFalse(
                r["historical_health_mood_money_relationship_claims_empirically_validated"]
            )
            self.assertFalse(r["source_predictions_tested_on_independent_human_cohort"])
            self.assertFalse(r["runtime_model_promoted"])

    def test_all_original_source_photo_historical_notes_in_one_frame(self):
        p = self.source["original_photo_witnesses"]["first_edition_transit"]["SHA256"]
        q = self.source["original_photo_witnesses"]["second_edition_transit"]["SHA256"]
        for r in self.rows:
            self.assertEqual(r["first_edition_original_pdf_frame"], 775)
            self.assertEqual(r["source_first_edition_original_photo_SHA256"], p)
            self.assertEqual(r["source_second_edition_original_photo_SHA256"], q)

    def test_provenance_exact_shas_in_acceptance(self):
        self.assertEqual(
            self.accept["source_SHA256"],
            sha(B / "ORIGINAL_CLXXIV_TRANSITS_TWO_EDITIONS_SOURCE_V1.json"),
        )
        self.assertEqual(self.accept["rules_SHA256"], sha(B / "RULES.json"))

    def test_second_edition_is_not_independent_predictive_replication(self):
        self.assertFalse(self.accept["observed_human_prediction_accuracy_validated"])
        self.assertFalse(self.accept["actual_transit_ephemeris_timing_engine_verified"])
        self.assertFalse(self.accept["professional_two_reader_critical_print_collation_complete"])


def one_note(i):
    def run(self):
        r = self.rows[i]
        rule = self.rules["rules"][i]
        self.assertEqual(r["id"], f"R{12847 + i}")
        self.assertEqual(rule["id"], r["id"])
        needle = r["derivative_locator_NOT_original_transcription"]
        self.assertEqual(
            self.finder[
                r["secondary_text_absolute_within_excerpt_offset"] : r[
                    "secondary_text_absolute_within_excerpt_offset"
                ]
                + len(needle)
            ],
            needle,
        )
        self.assertEqual(
            hashlib.sha256(needle.encode()).hexdigest(), r["secondary_anchor_utf8_sha256"]
        )
        self.assertFalse(rule["runtime_model_promoted"])

    return run


for index in range(22):
    setattr(OriginalTransitSources, f"test_source_note_{index + 1:02d}", one_note(index))


if __name__ == "__main__":
    unittest.main()
