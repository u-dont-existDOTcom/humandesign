"""Original Lilly 1647/1659 Parents printed-text provenance, never forecast validation."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
BASE = B.parent
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"


def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class OriginalParentsSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = read(B / "ORIGINAL_1647_1659_PARENTS_26_SOURCE_NOTES_V1.json")
        cls.rules = read(B / "RULES.json")
        cls.accept = read(B / "ACCEPTANCE.json")
        cls.prior = read(BASE / "B07ba/ORIGINAL_1647_1659_BRETHREN_22_SOURCE_NOTES_V1.json")
        cls.west = read(WEST)
        cls.china = read(CHINA)
        cls.records = cls.source["records"]

    def test_1647_original_full_Wellcome_source(self):
        self.assertEqual(
            self.source["source_full_original_Wellcome_1647_PDF_sha256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )
        self.assertEqual(
            self.west["source_sha256"], self.source["source_full_original_Wellcome_1647_PDF_sha256"]
        )

    def test_original_1647_and_distinct_1659_prints_photographed(self):
        photos = self.source["two_original_printings_four_page_photo_witnesses"]
        self.assertEqual(set(photos), {"752", "753"})
        self.assertEqual(
            {k: set(v) for k, v in photos.items()},
            {"752": {"1647", "1659"}, "753": {"1647", "1659"}},
        )
        for printed_folio, editions in photos.items():
            for printed_year, meta in editions.items():
                path = ROOT / meta["original_source_repo_relative_file"]
                self.assertTrue(path.is_file(), path)
                self.assertGreater(path.stat().st_size, 180000)
                self.assertEqual(path.stat().st_size, meta["bytes"])
                self.assertEqual(sha(path), meta["sha256"])
                self.assertEqual(meta["source_ed"], int(printed_year))
                self.assertEqual(meta["original_folio"], int(printed_folio))

    def test_prior_photographed_brethren_parent_boundary_not_reextracted(self):
        old = self.prior["original_two_editions_four_source_page_images"]["752"]
        new = self.source["two_original_printings_four_page_photo_witnesses"]["752"]
        self.assertEqual(new["1647"]["sha256"], old["first_1647"]["sha256"])
        self.assertEqual(new["1659"]["sha256"], old["typeset_1659"]["sha256"])

    def test_original_printed_CLXXIX_spans_two_physical_pages(self):
        self.assertEqual(self.source["original_first_1647_printed_folios"], [752, 753])
        self.assertEqual(self.source["original_first_1647_pdf_frames"], [786, 787])
        self.assertEqual(self.source["original_separate_1659_typeset_djvu_frames"], [781, 782])
        self.assertEqual([r["original_printed_folio"] for r in self.records[:15]], [752] * 15)
        self.assertEqual([r["original_printed_folio"] for r in self.records[15:]], [753] * 11)

    def test_26_consecutive_ids_no_overlap(self):
        self.assertEqual(len(self.records), 26)
        self.assertEqual(len(self.rules["rules"]), 26)
        self.assertEqual(self.rules["record_count"], 26)
        self.assertEqual([r["record_number"] for r in self.records], list(range(12992, 13018)))
        self.assertEqual(self.source["first_record"], "R12992")
        self.assertEqual(self.source["last_record"], "R13017")

    def test_original_next_chapter_begins_after_divider_same_folio(self):
        self.assertEqual(self.records[0]["role"], "CLXXIX_PARENTS_HEAD")
        self.assertEqual(self.records[-1]["role"], "CLXXX_SICKNESS_SERVANTS_BOUNDARY")
        self.assertEqual(self.accept["next_printed_chapter"], "CLXXX")
        self.assertEqual(self.accept["next_original_PDF_frame"], 787)
        self.assertEqual(self.accept["next_printed_folio"], 753)
        self.assertEqual(self.accept["next_historical_R"], "R13018")

    def test_lilly_known_merchant_report_not_blind_prediction(self):
        self.assertTrue(self.source["source_author_knew_merchants_history"])
        self.assertTrue(all(r["merchant_known_to_Lilly_before_description"] for r in self.records))
        self.assertEqual(self.source["independently_validated_real_human_outcomes"], 0)
        self.assertEqual(self.source["independently_validated_mother_outlived_father_history"], 0)

    def test_family_character_health_and_lifespan_unverified(self):
        fields = [r["evidence_layer"] for r in self.records]
        for required in (
            "UNVERIFIED_PARENTAL_MORTALITY_CLAIM",
            "UNVERIFIED_FAMILY_PSYCHOLOGY_CLAIM",
            "UNVERIFIED_FINANCIAL_FAMILY_CLAIM",
            "UNVERIFIED_FAMILY_RELATIONSHIP_CLAIM",
        ):
            self.assertIn(required, fields)
        for r in self.records:
            self.assertFalse(r["independent_actual_person_prediction_result_validated"])
            self.assertFalse(r["historical_mother_outliving_father_observed_result_verified"])

    def test_day_night_parent_conventions_are_conditional_source_only(self):
        roles = {r["role"] for r in self.records}
        self.assertIn("PTOLEMY_FIRSTBORN_DERIVED_PARENT_CHART", roles)
        self.assertIn("PTOLEMY_DAY_NIGHT_FATHER_SIGNIFICATOR", roles)
        self.assertIn("PTOLEMY_DAY_NIGHT_MOTHER_SIGNIFICATOR", roles)
        self.assertTrue(
            self.source["source_has_parent_chart_derived_from_first_born_not_real_parent_birth"]
        )

    def test_derived_father_example_parameters_preserved(self):
        self.assertEqual(self.source["source_father_example_6deg37_Libra_pole40"], [6, 37, 40])
        self.assertIn("SOURCE_ADD_THIRTY_OBLIQUE_ASC", {r["role"] for r in self.records})
        self.assertTrue(self.source["original_solar_oblique_asc_plus_30_degree_method_unverified"])
        self.assertEqual(self.source["independently_reconstructed_parent_natal_charts"], 0)

    def test_full_historical_chart_and_era_engine_unverified(self):
        for r in self.records:
            self.assertFalse(r["source_1616_natal_full_chart_ephemeris_verified"])
            self.assertFalse(r["source_parent_actual_birth_data_independently_verified"])
            self.assertFalse(r["source_derived_parent_chart_algorithm_expert_verified"])
            self.assertFalse(r["medicine_or_high_stakes_family_advice_authorized"])
        self.assertFalse(self.accept["parent_chart_historical_algorithm_math_engine_verified"])
        self.assertFalse(self.accept["source_expert_diplomatic_collation_complete"])

    def test_source_original_vs_researcher_gloss_separated(self):
        for r in self.records:
            self.assertTrue(r["historical_gloss_not_author_quotation"])
            self.assertTrue(r["non_diplomatic_locator"])
            self.assertNotIn("\n", r["role"])
            self.assertFalse(r["runtime_model_promoted"])

    def test_before_lilly_and_chinese_index_unchanged(self):
        self.assertEqual(self.west["records_count"], 12991)
        self.assertEqual(self.west["batches"][-1]["id"], "B07ba")
        self.assertEqual(self.west["next"]["chapter"], "CLXXIX")
        self.assertEqual(self.china["sum_source_annotations"], 355)
        self.assertEqual(self.accept["Chinese_V7_retained"], 355)

    def test_acceptance_counts_and_source_hashes(self):
        self.assertEqual(self.accept["new_historical_source_only_notes"], 26)
        self.assertEqual(self.accept["Lilly_after_if_accepted"], 13017)
        self.assertEqual(self.accept["Western_after_if_accepted"], 14083)
        self.assertEqual(self.accept["rules_sha256"], sha(B / "RULES.json"))
        self.assertEqual(
            self.accept["source_notes_sha256"],
            sha(B / "ORIGINAL_1647_1659_PARENTS_26_SOURCE_NOTES_V1.json"),
        )

    def test_historical_records_no_live_morality_or_wealth_predictions(self):
        self.assertTrue(all(not r["runtime_model_promoted"] for r in self.records))
        self.assertEqual(self.rules["runtime_promotions"], 0)
        self.assertEqual(self.rules["independent_prospective_human_predictions_validated"], 0)

    def test_four_provenance_paths_source_ed_frames(self):
        for page in ("752", "753"):
            for ed, meta in self.source["two_original_printings_four_page_photo_witnesses"][
                page
            ].items():
                self.assertEqual(
                    meta["original_photo_pdf_or_djvu_frame"],
                    int(page) + (34 if ed == "1647" else 29),
                )


def single_historical_note(n):
    def test(self):
        note = self.records[n]
        rule = self.rules["rules"][n]
        self.assertEqual(note["id"], f"R{12992 + n}")
        self.assertEqual(rule["id"], note["id"])
        self.assertEqual(note["record_number"], 12992 + n)
        self.assertEqual(rule["record_number"], 12992 + n)
        self.assertFalse(note["runtime_model_promoted"])

    return test


for n in range(26):
    setattr(OriginalParentsSource, f"test_source_note_{n + 1:02d}", single_historical_note(n))


if __name__ == "__main__":
    unittest.main()
