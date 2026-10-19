"""Final sign columns and 372/372 historical source photo attempt inventory."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V3.json"


def load(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


class AquariusPiscesPhoto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = load(B / "PHOTO_SOURCE_AQUARIUS_PISCES_1647_V1.json")
        cls.v6 = load(B / "ANNUAL_RATE_PHOTO_OVERLAY_V6.json")
        cls.v5 = load(B.parent / "B07ac/ANNUAL_RATE_PHOTO_OVERLAY_V5.json")
        cls.source_by = {(x["sign"], x["degree"]): x for x in cls.source["records"]}
        cls.rows = {(x["sign"], x["degree"]): x for x in cls.v6["rows"]}
        cls.old = {(x["sign"], x["degree"]): x for x in cls.v5["rows"]}

    def test_original_1647_pdf_full_source_sha(self):
        self.assertEqual(
            self.source["original_full_1647_scan_sha256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_primary_photo_1647_sha(self):
        path = B.parent / "B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg"
        self.assertEqual(sha(path), self.source["original_first_edition_table_photo_sha256"])

    def test_provenance_preserves_all_old_overlay_bytes(self):
        self.assertEqual(
            sha(B.parent / "B07ac/ANNUAL_RATE_PHOTO_OVERLAY_V5.json"),
            self.v6["parent_B07ac_overlay_sha256"],
        )

    def test_all_original_372_positions_accounted(self):
        self.assertEqual(self.v6["original_table_total_positions"], 372)
        self.assertEqual(len(self.rows), 372)
        self.assertEqual(self.v6["cumulative_one_reader_legible_original_1647"], 365)
        self.assertEqual(self.v6["cumulative_original_print_unresolved_positions"], 7)
        self.assertEqual(self.v6["cumulative_positions_without_any_original_photo_attempt"], 0)
        self.assertEqual(365 + 7, 372)

    def test_both_full_sign_columns(self):
        self.assertEqual(len(self.source_by), 62)
        for sign in ("Aquarius", "Pisces"):
            self.assertEqual(sorted(d for s, d in self.source_by if s == sign), list(range(31)))

    def test_prior_fifteen_B07y_photo_rows_not_recounted(self):
        overlap = {
            key for key, v in self.source_by.items() if v["prior_B07y_original_photo_status"]
        }
        self.assertEqual(len(overlap), 15)
        self.assertEqual(
            overlap,
            {
                ("Aquarius", 0),
                ("Aquarius", 1),
                ("Aquarius", 2),
                ("Aquarius", 3),
                ("Aquarius", 4),
                ("Pisces", 0),
                ("Pisces", 4),
                ("Pisces", 5),
                ("Pisces", 6),
                ("Pisces", 7),
                ("Pisces", 21),
                ("Pisces", 22),
                ("Pisces", 23),
                ("Pisces", 24),
                ("Pisces", 25),
            },
        )
        for k in overlap:
            self.assertEqual(self.rows[k]["source_read_batch"], "B07y")

    def test_new_45_photo_legible_and_two_unresolved(self):
        self.assertEqual(self.source["additionally_legible_original_photo"], 45)
        self.assertEqual(self.source["additional_ambiguous_print_glyphs"], 2)
        self.assertEqual(self.v6["new_B07ad_one_reader_legible_original"], 45)
        self.assertEqual(self.v6["new_B07ad_unresolved_original_glyphs"], 2)

    def test_new_original_glyph_unknown_not_interpolated(self):
        unresolved = {
            k
            for k, v in self.source_by.items()
            if v["unresolved_source_photo_alternatives"]
            and not v["prior_B07y_original_photo_status"]
        }
        self.assertEqual(unresolved, {("Aquarius", 5), ("Aquarius", 6)})
        self.assertEqual(
            self.rows["Aquarius", 5]["unresolved_original_source_glyph_options"],
            [[62, 33], [62, 35]],
        )
        self.assertEqual(
            self.rows["Aquarius", 6]["unresolved_original_source_glyph_options"],
            [[62, 22], [62, 24]],
        )
        for k in unresolved:
            self.assertIsNone(self.rows[k]["first_edition_1647_one_reader_photo_rate"])

    def test_three_new_source_transcription_conflicts(self):
        differences = self.v6["new_1647_print_vs_derivative_conflicts"]
        self.assertEqual(
            [(x["sign"], x["degree"]) for x in differences],
            [("Aquarius", 13), ("Aquarius", 15), ("Pisces", 30)],
        )
        self.assertEqual(
            [
                (x["previous_derivative_searchable_text"], x["original_1647_photo_reading"])
                for x in differences
            ],
            [([60, 50], [60, 56]), ([60, 21], [60, 31]), ([54, 16], [54, 26])],
        )

    def test_1647_Aquarius13_15_exact(self):
        self.assertEqual(
            self.rows["Aquarius", 13]["first_edition_1647_one_reader_photo_rate"], [60, 56]
        )
        self.assertEqual(
            self.rows["Aquarius", 15]["first_edition_1647_one_reader_photo_rate"], [60, 31]
        )

    def test_1647_Pisces30_exact(self):
        self.assertEqual(
            self.rows["Pisces", 30]["first_edition_1647_one_reader_photo_rate"], [54, 26]
        )
        self.assertEqual(
            self.rows["Pisces", 29]["first_edition_1647_one_reader_photo_rate"], [54, 28]
        )

    def test_previous_Pisces24_ambiguity_remains(self):
        k = ("Pisces", 24)
        self.assertEqual(self.rows[k]["source_read_batch"], "B07y")
        self.assertIsNone(self.rows[k]["first_edition_1647_one_reader_photo_rate"])
        self.assertEqual(
            self.rows[k]["unresolved_original_source_glyph_options"], [[53, 43], [54, 43]]
        )

    def test_preservation_of_prior_rows(self):
        for k, prev in self.old.items():
            if k not in self.source_by:
                self.assertEqual(self.rows[k], prev)
            else:
                self.assertEqual(
                    self.rows[k]["frozen_B07x_derivative_candidate"],
                    prev["frozen_B07x_derivative_candidate"],
                )

    def test_source_crops_are_first_edition_derivatives(self):
        for name in (
            "Aquarius_first_half.png",
            "Aquarius_second_half.png",
            "Pisces_first_half.png",
            "Pisces_second_half.png",
            "Aqua_4_8.png",
            "Aqua_11_17.png",
            "Aqua_14_20.png",
            "Pisces_22_30.png",
            "Pisces_0_12.png",
        ):
            f = B / "evidence" / name
            self.assertTrue(f.is_file(), name)
            self.assertGreater(f.stat().st_size, 10_000)

    def test_source_assignment_no_synthetic_source_from_ramp(self):
        for k, src in self.source_by.items():
            dest = self.rows[k]
            self.assertEqual(src["original_pdf_frame"], 745)
            self.assertEqual(
                src["first_edition_1647_printed_rate"],
                dest["first_edition_1647_one_reader_photo_rate"],
            )
            self.assertFalse(src["human_forecast_prediction_verified"])
            self.assertFalse(src["runtime_model_promoted"])

    def test_original_1647_is_not_authorized_chart_engine(self):
        self.assertFalse(self.v6["source_critical_second_reader_verified_for_all_positions"])
        self.assertFalse(self.v6["scientific_1647_ra_year_method_ascendant_calculations_validated"])
        self.assertFalse(self.v6["modern_ephemeris_and_birth_datetime_parity_validated"])
        self.assertEqual(self.v6["individual_human_outcome_predictions_validated"], 0)
        self.assertEqual(self.v6["runtime_model_promotions"], 0)

    def test_current_historic_registry_unchanged(self):
        self.assertEqual(load(WEST)["records_count"], 12472)
        self.assertEqual(load(CHINA)["sum_source_annotations"], 142)
        self.assertEqual(self.v6["Western_Lilly_accepted_history_unchanged"], 12472)
        self.assertEqual(self.v6["Chinese_V3_accepted_history_unchanged"], 142)


def check_one(sign, degree):
    def test(self):
        k = (sign, degree)
        src = self.source_by[k]
        row = self.rows[k]
        self.assertEqual(
            src["first_edition_1647_printed_rate"],
            row["first_edition_1647_one_reader_photo_rate"],
        )
        self.assertEqual(
            row["source_read_batch"], "B07y" if src["prior_B07y_original_photo_status"] else "B07ad"
        )
        self.assertFalse(row["runtime_promoted"])

    return test


for sign in ("Aquarius", "Pisces"):
    for degree in range(31):
        setattr(
            AquariusPiscesPhoto, f"test_{sign.lower()}_degree{degree:02d}", check_one(sign, degree)
        )


if __name__ == "__main__":
    unittest.main()
