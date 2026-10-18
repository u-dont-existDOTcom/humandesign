"""B07z 1647 original annual-rate full four columns: integrity and scope tests."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
PARENT_Y = B.parent / "B07y"
PARENT_X = B.parent / "B07x"
ROOT = B.parents[3]
WESTERN = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V3.json"
SIGN_NAMES = ("Aries", "Taurus", "Gemini", "Cancer")


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


class FourSourceColumns(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = j(B / "FULL_COLUMNS_ARIES_TAURUS_GEMINI_CANCER_1647_V1.json")
        cls.new = j(B / "ANNUAL_372_SOURCE_PHOTO_OVERLAY_V2.json")
        cls.old = j(PARENT_Y / "ANNUAL_RATE_372_PHOTO_ADJUDICATION_OVERLAY_V1.json")
        cls.b07x = j(PARENT_X / "ANNUAL_DIRECTION_MEASURE_372_CANDIDATES_V1.json")
        cls.index = j(WESTERN)
        cls.chinese = j(CHINESE)
        cls.sourcerows = {(r["sign"], r["degree"]): r for r in cls.source["records"]}
        cls.current = {(r["sign"], r["degree"]): r for r in cls.new["cells"]}
        cls.original = {(r["sign"], r["degree"]): r for r in cls.old["rows"]}

    def test_original_source_pdf_sha_locked(self):
        self.assertEqual(
            self.source["source_pdf_full_sha256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_source_image_byte_sha(self):
        f = PARENT_Y / "evidence" / "original_1647_annual_measure_pdf745_3500.jpg"
        self.assertEqual(sha(f), self.source["original_source_photo_sha256"])
        self.assertEqual(self.new["direct_first_edition_photo_sha256"], sha(f))

    def test_derivative_crops_not_primary_evidence(self):
        folder = B / "evidence" / "contrast_crops"
        self.assertTrue(folder.is_dir())
        self.assertEqual(len(list(folder.glob("*.png"))), 8)
        for f in folder.glob("*.png"):
            self.assertGreater(f.stat().st_size, 10_000)
            self.assertEqual(len(sha(f)), 64)
        self.assertEqual(
            self.source["contrast_crops_derivative_not_independent_source"],
            "evidence/contrast_crops",
        )

    def test_complete_four_columns(self):
        self.assertEqual(self.source["source_signs"], list(SIGN_NAMES))
        self.assertEqual(self.source["four_sign_source_rows"], 124)
        self.assertEqual(len(self.sourcerows), 124)
        self.assertEqual(self.source["original_rows_per_sign"], 31)
        for sign in SIGN_NAMES:
            self.assertEqual(sorted(d for s, d in self.sourcerows if s == sign), list(range(31)))

    def test_first_1647_photo_rows_no_clipped_seconds(self):
        for (_sign, d), r in self.sourcerows.items():
            self.assertEqual(r["original_source"], "1647_original_pdf745_printed711")
            self.assertEqual(r["source_photo_half"], "first_half" if d < 16 else "second_half")
            self.assertTrue(0 <= r["original_1647_rate_arcseconds"] < 60)
            self.assertTrue(50 <= r["original_1647_rate_arcminutes"] <= 68)

    def test_124_direct_one_reader_source_photographic_positions(self):
        self.assertEqual(
            sum(
                r["first_edition_source_photo_verified_by_one_reader"]
                for k, r in self.current.items()
                if k in self.sourcerows
            ),
            124,
        )
        self.assertEqual(self.new["new_full_column_photo_positions"], 124)
        self.assertFalse(self.source["one_read_of_old_text_is_not_an_empirical_test"] is False)

    def test_no_overlap_with_prior_B07y_24_source_positions(self):
        prev = {
            (r["sign"], r["degree"])
            for r in j(PARENT_Y / "PHOTO_ADJUDICATION_1647_V1.json")["photo_readings"]
        }
        self.assertEqual(len(prev), 24)
        self.assertFalse(set(self.sourcerows) & prev)

    def test_b07x_original_derivative_candidates_byte_preserved(self):
        self.assertEqual(self.b07x["source_cells_expected"], 372)
        self.assertEqual(len(self.original), 372)
        for key, r in self.current.items():
            self.assertEqual(
                r["frozen_B07x_derivative_candidate"],
                self.original[key]["B07x_derivative_candidate_as_originally_retained"],
            )
        self.assertEqual(
            self.new["parent_B07y_overlay_sha256"],
            sha(PARENT_Y / "ANNUAL_RATE_372_PHOTO_ADJUDICATION_OVERLAY_V1.json"),
        )

    def test_372_rows_and_counts(self):
        self.assertEqual(len(self.current), 372)
        self.assertEqual(len(self.new["cells"]), 372)
        self.assertEqual(self.new["full_annual_table_positions"], 372)
        self.assertEqual(self.new["one_reader_photo_read_positions_cumulative_B07y_B07z"], 146)
        self.assertEqual(self.new["unresolved_original_photo_glyph_positions_cumulative"], 2)
        self.assertEqual(self.new["not_yet_first_edition_photo_read_positions_cumulative"], 224)
        self.assertEqual(146 + 2 + 224, 372)

    def test_only_one_new_transcription_discrepancy(self):
        self.assertEqual(self.new["source_1647_values_differing_from_derivative_in_new_column"], 1)
        self.assertEqual(
            self.new["new_source_conflicts"],
            [
                {
                    "sign": "Taurus",
                    "degree": 28,
                    "derivative_rate": [59, 56],
                    "1647_first_edition_photo_rate": [59, 36],
                    "source_fidelity_status": "UNBLINDED_SINGLE_READER_PHOTOGRAPHIC_REVISION",
                }
            ],
        )

    def test_taurus_28_literal_1647_photo_vs_derivative(self):
        current = self.current["Taurus", 28]
        self.assertEqual(current["frozen_B07x_derivative_candidate"], [59, 56])
        self.assertEqual(current["first_edition_1647_one_reader_photo_rate"], [59, 36])
        self.assertEqual(current["source_read_batch"], "B07z")

    def test_taurus_27_printed_nonmonotonic_not_fixed(self):
        r = self.sourcerows["Taurus", 27]
        self.assertEqual(
            (r["original_1647_rate_arcminutes"], r["original_1647_rate_arcseconds"]), (59, 48)
        )
        self.assertEqual(
            r["source_uncertainty_or_exception"],
            "ORIGINAL_1647_PRINTED_NONMONOTONE_RATE_PRESERVE_SOURCE",
        )
        self.assertEqual(
            self.current["Taurus", 27]["first_edition_1647_one_reader_photo_rate"], [59, 48]
        )
        self.assertEqual(
            self.current["Taurus", 29]["first_edition_1647_one_reader_photo_rate"], [59, 44]
        )
        self.assertEqual(
            self.current["Taurus", 26]["first_edition_1647_one_reader_photo_rate"], [59, 19]
        )

    def test_Aries_end_and_initial_preserved(self):
        self.assertEqual(
            self.current["Aries", 0]["first_edition_1647_one_reader_photo_rate"], [54, 26]
        )
        self.assertEqual(
            self.current["Aries", 30]["first_edition_1647_one_reader_photo_rate"], [55, 40]
        )

    def test_Gemini_rate_full_degree_over_60_valid(self):
        self.assertEqual(
            self.current["Gemini", 1]["first_edition_1647_one_reader_photo_rate"], [60, 0]
        )
        self.assertEqual(
            self.current["Gemini", 30]["first_edition_1647_one_reader_photo_rate"], [62, 18]
        )
        self.assertEqual(
            self.current["Gemini", 28]["first_edition_1647_one_reader_photo_rate"], [62, 18]
        )

    def test_Cancer_return_rate(self):
        self.assertEqual(
            self.current["Cancer", 0]["first_edition_1647_one_reader_photo_rate"], [62, 18]
        )
        self.assertEqual(
            self.current["Cancer", 30]["first_edition_1647_one_reader_photo_rate"], [59, 34]
        )

    def test_every_new_source_row_read_is_pair_equal(self):
        for key, r in self.sourcerows.items():
            self.assertEqual(
                self.current[key]["first_edition_1647_one_reader_photo_rate"],
                [r["original_1647_rate_arcminutes"], r["original_1647_rate_arcseconds"]],
            )
            self.assertEqual(self.current[key]["source_read_batch"], "B07z")

    def test_original_two_glyph_ambiguities_not_lost(self):
        old_ambiguous = {
            key for key, r in self.original.items() if r["B07y_manual_original_glyph_alternatives"]
        }
        self.assertEqual(old_ambiguous, {("Pisces", 24), ("Capricorn", 15)})
        for key in old_ambiguous:
            self.assertIsNone(self.current[key]["first_edition_1647_one_reader_photo_rate"])
            self.assertTrue(self.current[key]["unresolved_original_source_glyph_options"])

    def test_b07y_previous_five_photo_conflicts_retained(self):
        for sign, degree, value in (
            ("Leo", 0, [59, 34]),
            ("Capricorn", 13, [66, 10]),
            ("Aquarius", 0, [63, 33]),
            ("Aquarius", 3, [62, 57]),
            ("Pisces", 6, [56, 37]),
        ):
            self.assertEqual(
                self.current[sign, degree]["first_edition_1647_one_reader_photo_rate"], value
            )
            self.assertEqual(self.current[sign, degree]["source_read_batch"], "B07y")

    def test_without_new_evidence_remaining_224_are_not_source_proven(self):
        remaining = [r for r in self.current.values() if r["source_read_batch"] is None]
        self.assertEqual(len(remaining), 224)
        self.assertTrue(
            all(r["first_edition_1647_one_reader_photo_rate"] is None for r in remaining)
        )
        self.assertTrue(
            all(not r["first_edition_source_photo_verified_by_one_reader"] for r in remaining)
        )

    def test_historical_western_lilly_index_unchanged(self):
        self.assertEqual(self.index["records_count"], 12472)
        self.assertEqual(self.index["batches"][-1]["id"], "B07w")
        self.assertEqual(self.new["history_source_registry_lilly_retained"], 12472)

    def test_chinese_V3_source_index_unchanged(self):
        self.assertEqual(self.chinese["sum_source_annotations"], 142)
        self.assertEqual(self.new["independent_chinese_source_V3_retained"], 142)

    def test_no_independent_photographic_second_reader(self):
        self.assertEqual(self.new["independent_photo_reader_reviews"], 0)
        self.assertTrue(
            all(not r["independently_second_reader_validated"] for r in self.source["records"])
        )

    def test_do_not_confuse_documentary_source_with_event_validations(self):
        self.assertFalse(self.new["source_complete_original_photo_table"])
        self.assertFalse(self.new["historical_math_or_birth_chart_engine_verified"])
        self.assertEqual(self.new["human_predictive_accuracy_validations"], 0)
        self.assertEqual(self.new["runtime_promotions"], 0)

    def test_never_promote_any_cell_to_personal_prediction(self):
        for row in self.new["cells"]:
            self.assertFalse(row["naibod_maginus_ptolemy_calendar_engine_verified"])
            self.assertFalse(row["real_life_event_predictive_accuracy_verified"])
            self.assertFalse(row["runtime_promoted"])


def photo_cell_test(sign, degree):
    def test(self):
        src = self.sourcerows[sign, degree]
        eff = self.current[sign, degree]
        self.assertEqual(
            [src["original_1647_rate_arcminutes"], src["original_1647_rate_arcseconds"]],
            eff["first_edition_1647_one_reader_photo_rate"],
        )
        self.assertTrue(eff["first_edition_source_photo_verified_by_one_reader"])
        self.assertFalse(eff["runtime_promoted"])

    return test


for sign in SIGN_NAMES:
    for degree in range(31):
        setattr(
            FourSourceColumns,
            f"test_first_edition_{sign.lower()}_degree_{degree:02d}",
            photo_cell_test(sign, degree),
        )


if __name__ == "__main__":
    unittest.main()
