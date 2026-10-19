"""B07ab Libra and Scorpio first-edition photographic source fidelity checks.

Mechanical checks verify the historical data packet, not independent reading
of image glyphs or the empirical validity of astrological event timing.
"""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V3.json"


def read(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


class LibraScorpioOriginalPhoto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = read(B / "PHOTO_SOURCE_LIBRA_SCORPIO_V1.json")
        cls.current = read(B / "ANNUAL_RATE_PHOTO_OVERLAY_V4.json")
        cls.parent = read(B.parent / "B07aa/ANNUAL_RATE_PHOTO_OVERLAY_V3.json")
        cls.records = {(r["sign"], r["degree"]): r for r in cls.document["records"]}
        cls.rows = {(r["sign"], r["degree"]): r for r in cls.current["rows"]}
        cls.old = {(r["sign"], r["degree"]): r for r in cls.parent["rows"]}

    def test_original_full_pdf_witness(self):
        self.assertEqual(
            self.document["full_original_pdf_sha256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_original_first_edition_full_page_image(self):
        f = B.parent / "B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg"
        self.assertEqual(sha(f), self.document["photo_parent_sha256"])
        self.assertEqual(self.current["original_photo_pdf745_sha256"], sha(f))

    def test_parent_overlay_immutable(self):
        self.assertEqual(
            self.current["parent_B07aa_sha256"],
            sha(B.parent / "B07aa/ANNUAL_RATE_PHOTO_OVERLAY_V3.json"),
        )

    def test_full_31_rows_each(self):
        self.assertEqual(len(self.records), 62)
        self.assertEqual(self.document["source_positions_total"], 62)
        for sign in ("Libra", "Scorpio"):
            self.assertEqual(sorted(deg for s, deg in self.records if s == sign), list(range(31)))

    def test_one_reader_photo_provenance(self):
        self.assertTrue(self.document["original_source_single_reader_only"])
        self.assertTrue(self.document["anomaly_not_silently_repaired"])
        self.assertEqual(self.current["new_source_reviewer_count"], 1)
        self.assertFalse(self.current["independent_two_reader_agreement_verified"])

    def test_exact_prior_four_positions_not_recounted(self):
        prev = {(s, d) for (s, d), r in self.records.items() if r["previous_B07y_photo_reading"]}
        self.assertEqual(prev, {("Libra", 7), ("Libra", 21), ("Libra", 22), ("Libra", 23)})
        for k in prev:
            self.assertEqual(self.rows[k]["source_read_batch"], "B07y")
            self.assertEqual(
                self.rows[k]["first_edition_1647_one_reader_photo_rate"],
                self.old[k]["first_edition_1647_one_reader_photo_rate"],
            )

    def test_remaining_positions_new_not_overwriting(self):
        for key in self.records:
            if key not in {("Libra", 7), ("Libra", 21), ("Libra", 22), ("Libra", 23)}:
                self.assertEqual(self.old[key]["source_read_batch"], None)
                self.assertEqual(self.rows[key]["source_read_batch"], "B07ab")

    def test_2_new_source_vs_derivative_corrections(self):
        x = self.current["new_derivative_source_conflicts"]
        self.assertEqual(len(x), 2)
        self.assertEqual([(r["sign"], r["degree"]) for r in x], [("Scorpio", 6), ("Scorpio", 21)])
        self.assertEqual(
            [(r["B07x_derivative"], r["original_1647"]) for r in x],
            [([58, 22], [58, 32]), ([61, 29], [61, 39])],
        )

    def test_printed_Libra_22_23_24_irregularity_retained(self):
        self.assertEqual(
            self.rows["Libra", 22]["first_edition_1647_one_reader_photo_rate"], [56, 32]
        )
        self.assertEqual(
            self.rows["Libra", 23]["first_edition_1647_one_reader_photo_rate"], [56, 11]
        )
        self.assertEqual(
            self.rows["Libra", 24]["first_edition_1647_one_reader_photo_rate"], [56, 2]
        )
        self.assertEqual(
            self.records["Libra", 22]["first_edition_print_anomaly"],
            "SEQUENCE_IRREGULAR_PRINTED_LITERAL_UNCHANGED",
        )

    def test_overlap_Libra7_Maginus_historical_rate(self):
        self.assertEqual(
            self.rows["Libra", 7]["first_edition_1647_one_reader_photo_rate"], [54, 25]
        )

    def test_372_all_counts(self):
        self.assertEqual(len(self.rows), 372)
        self.assertEqual(self.current["source_372_positions"], 372)
        self.assertEqual(self.current["added_Libra_Scorpio_source_readings"], 58)
        self.assertEqual(self.current["old_source_photo_overlaps_unmodified"], 4)
        self.assertEqual(self.current["cumulative_one_reader_original_photo_legible"], 263)
        self.assertEqual(self.current["cumulative_original_glyphs_unresolved"], 4)
        self.assertEqual(self.current["not_read_original_table_remaining"], 105)
        self.assertEqual(263 + 4 + 105, 372)

    def test_all_b07aa_values_retained(self):
        for key, r in self.old.items():
            if key not in self.records:
                self.assertEqual(
                    self.rows[key]["first_edition_1647_one_reader_photo_rate"],
                    r["first_edition_1647_one_reader_photo_rate"],
                )
                self.assertEqual(
                    self.rows[key]["unresolved_original_source_glyph_options"],
                    r["unresolved_original_source_glyph_options"],
                )
                self.assertEqual(self.rows[key]["source_read_batch"], r["source_read_batch"])

    def test_no_hidden_corrected_math_or_real_human_scoring(self):
        self.assertFalse(self.current["full_table_original_photo_complete"])
        self.assertFalse(self.current["genuine_17th_century_astronomical_method_parity_verified"])
        self.assertEqual(self.current["empirical_real_person_predictions_validated"], 0)
        self.assertEqual(self.current["runtime_promotions"], 0)
        for r in self.current["rows"]:
            self.assertFalse(r["runtime_promoted"])

    def test_source_derived_crops_are_not_independent_editions(self):
        self.assertEqual(len(list((B / "evidence").glob("*_half.png"))), 4)
        for r in self.records.values():
            self.assertTrue((B / "evidence" / r["evidence_crop"]).is_file())
            self.assertEqual(r["original_pdf_frame"], 745)
            self.assertEqual(r["original_printed_page"], 711)
            self.assertFalse(r["independently_confirmed_original_glyph"])

    def test_original_historical_indices_unchanged(self):
        self.assertEqual(read(WEST)["records_count"], 12472)
        self.assertEqual(read(CHINA)["sum_source_annotations"], 142)
        self.assertEqual(self.current["Lilly_canonical_source_index_retained"], 12472)
        self.assertEqual(self.current["Chinese_V3_canonical_source_index_retained"], 142)


def source_position_test(sign, degree):
    def test(self):
        key = (sign, degree)
        r = self.records[key]
        s = self.rows[key]
        self.assertEqual(
            s["first_edition_1647_one_reader_photo_rate"],
            [r["original_1647_rate_arcminutes"], r["original_1647_rate_arcseconds"]],
        )
        self.assertTrue(s["first_edition_source_photo_verified_by_one_reader"])
        self.assertFalse(s["runtime_promoted"])

    return test


for name in ("Libra", "Scorpio"):
    for i in range(31):
        setattr(
            LibraScorpioOriginalPhoto, f"test_{name.lower()}_{i:02d}", source_position_test(name, i)
        )


if __name__ == "__main__":
    unittest.main()
