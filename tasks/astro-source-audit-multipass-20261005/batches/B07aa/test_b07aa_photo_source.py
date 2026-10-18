"""Photo-source Leo and Virgo, append-only, full coverage and no forecast promotion."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
PARENT = B.parent / "B07z"
ROOT = B.parents[3]
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V3.json"


def j(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


class LeoVirgoSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = j(B / "PHOTO_SOURCE_COLUMNS_LEO_VIRGO_1647_V1.json")
        cls.current = j(B / "ANNUAL_RATE_PHOTO_OVERLAY_V3.json")
        cls.parent = j(PARENT / "ANNUAL_372_SOURCE_PHOTO_OVERLAY_V2.json")
        cls.c = {(r["sign"], r["degree"]): r for r in cls.current["rows"]}
        cls.p = {(r["sign"], r["degree"]): r for r in cls.parent["cells"]}
        cls.s = {(r["sign"], r["zodiac_degree"]): r for r in cls.source["entries"]}

    def test_original_source_sha_1647(self):
        self.assertEqual(
            self.source["source_original_894frame_pdf_sha256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_original_photo_binary_integrity(self):
        p = B.parent / "B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg"
        self.assertEqual(self.source["original_photo_sha256"], sha(p))

    def test_existing_B07z_parent_not_mutated(self):
        self.assertEqual(
            self.current["prior_B07z_overlay_sha256"],
            sha(PARENT / "ANNUAL_372_SOURCE_PHOTO_OVERLAY_V2.json"),
        )
        self.assertTrue(self.current["source_parent_overlay_unchanged"])
        self.assertEqual(len(self.parent["cells"]), 372)

    def test_old_Leo0_not_recounted(self):
        self.assertEqual(self.s["Leo", 0]["original_photo_literal_rate_minutes_seconds"], [59, 34])
        self.assertTrue(self.s["Leo", 0]["previously_source_read_in_B07y"])
        self.assertEqual(self.c["Leo", 0]["source_read_batch"], "B07y")
        self.assertEqual(self.c["Leo", 0]["first_edition_1647_one_reader_photo_rate"], [59, 34])

    def test_two_complete_source_column_positions(self):
        self.assertEqual(len(self.s), 62)
        for sign in ("Leo", "Virgo"):
            self.assertEqual(sorted(d for s, d in self.s if s == sign), list(range(31)))

    def test_59_new_legible_and_two_new_ambiguous(self):
        self.assertEqual(self.source["new_direct_1647_photo_one_reader_entries"], 59)
        self.assertEqual(self.source["new_ambiguous_photo_positions"], 2)
        self.assertEqual(self.source["source_positions_already_audited_in_B07y"], 1)
        self.assertEqual(sum(r["new_one_reader_source_read"] for r in self.s.values()), 59)

    def test_two_new_glyph_ambiguities_not_auto_corrected(self):
        ambiguous = {
            key for key, r in self.s.items() if r["unresolved_original_photo_glyph_options"]
        }
        self.assertEqual(ambiguous, {("Virgo", 1), ("Virgo", 18)})
        self.assertEqual(
            self.s["Virgo", 1]["unresolved_original_photo_glyph_options"], [[55, 10], [55, 13]]
        )
        self.assertEqual(
            self.s["Virgo", 18]["unresolved_original_photo_glyph_options"], [[53, 58], [53, 59]]
        )
        for k in ambiguous:
            self.assertIsNone(self.c[k]["first_edition_1647_one_reader_photo_rate"])
            self.assertTrue(self.c[k]["unresolved_original_source_glyph_options"])

    def test_virgo4_printed_rate_differs_from_derivative(self):
        r = self.c["Virgo", 4]
        self.assertEqual(r["frozen_B07x_derivative_candidate"], [54, 53])
        self.assertEqual(r["first_edition_1647_one_reader_photo_rate"], [54, 52])
        self.assertEqual(r["source_read_batch"], "B07aa")

    def test_new_discrepancy_exact_one(self):
        self.assertEqual(
            self.current["B07aa_new_derivative_conflicts"],
            [
                {
                    "sign": "Virgo",
                    "degree": 4,
                    "derivative_originally_frozen": [54, 53],
                    "1647_photo_one_reader": [54, 52],
                    "independent_second_reader_checked": False,
                }
            ],
        )

    def test_original_year_rate_leo_starts_and_ends(self):
        self.assertEqual(self.c["Leo", 0]["first_edition_1647_one_reader_photo_rate"], [59, 34])
        self.assertEqual(self.c["Leo", 30]["first_edition_1647_one_reader_photo_rate"], [55, 16])

    def test_original_year_rate_virgo_start_end(self):
        self.assertEqual(self.c["Virgo", 0]["first_edition_1647_one_reader_photo_rate"], [55, 16])
        self.assertEqual(self.c["Virgo", 30]["first_edition_1647_one_reader_photo_rate"], [54, 4])

    def test_photo_derived_evidence_not_independent(self):
        for name in (
            "Leo_first_half.png",
            "Leo_second_half.png",
            "Virgo_first_half.png",
            "Virgo_second_half.png",
            "virgo_rows0_5.png",
            "virgo_rows15_22.png",
            "virgo_rows18_25.png",
            "leo_rows0_6.png",
        ):
            f = B / "evidence" / name
            self.assertTrue(f.is_file(), name)
            self.assertGreater(f.stat().st_size, 15_000)
            self.assertEqual(len(sha(f)), 64)

    def test_cumulative_372_coverage_sums(self):
        self.assertEqual(len(self.current["rows"]), 372)
        self.assertEqual(len(self.c), 372)
        self.assertEqual(self.current["cumulative_photo_one_reader_legible"], 205)
        self.assertEqual(self.current["cumulative_photo_glyphs_unresolved"], 4)
        self.assertEqual(self.current["cumulative_unexamined_original_positions"], 163)
        self.assertEqual(205 + 4 + 163, 372)

    def test_all_prior_B07y_and_B07z_observations_preserved(self):
        for key, old in self.p.items():
            if key not in self.s or key == ("Leo", 0):
                new = self.c[key]
                self.assertEqual(
                    new["first_edition_1647_one_reader_photo_rate"],
                    old["first_edition_1647_one_reader_photo_rate"],
                )
                self.assertEqual(
                    new["unresolved_original_source_glyph_options"],
                    old["unresolved_original_source_glyph_options"],
                )
                self.assertEqual(new["source_read_batch"], old["source_read_batch"])

    def test_first_edition_source_glyphs_still_two_reader_unverified(self):
        self.assertFalse(self.current["independent_primary_source_two_reader_review"])
        for r in self.current["rows"]:
            self.assertFalse(r["independent_second_reader_verified"])
            self.assertFalse(r["modern_astro_chart_year_conversion_verified"])

    def test_Western_Lilly_and_chinese_registry_counts_protected(self):
        self.assertEqual(j(WEST)["records_count"], 12472)
        self.assertEqual(j(CHINA)["sum_source_annotations"], 142)
        self.assertEqual(self.current["West_Lilly_canonical_index_remains"], 12472)
        self.assertEqual(self.current["Chinese_canonical_V3_remains"], 142)

    def test_no_real_people_predictions_from_text(self):
        self.assertFalse(self.current["all_first_edition_372_source_positions_audited"])
        self.assertEqual(self.current["real_people_independent_predictions_validated"], 0)
        self.assertEqual(self.current["runtime_model_promotions"], 0)
        for row in self.current["rows"]:
            self.assertFalse(row["real_human_predictive_validation"])
            self.assertFalse(row["runtime_promoted"])


def source_cell_test(sign, degree):
    def test(self):
        key = (sign, degree)
        src = self.s[key]
        record = self.c[key]
        self.assertEqual(
            src["evidence_crop"], sign + ("_first_half.png" if degree < 16 else "_second_half.png")
        )
        self.assertEqual(record["source_read_batch"], "B07y" if key == ("Leo", 0) else "B07aa")
        self.assertEqual(
            record["first_edition_1647_one_reader_photo_rate"],
            src["original_photo_literal_rate_minutes_seconds"],
        )
        self.assertFalse(record["runtime_promoted"])

    return test


for sign in ("Leo", "Virgo"):
    for degree in range(31):
        setattr(LeoVirgoSource, f"test_{sign.lower()}_{degree:02d}", source_cell_test(sign, degree))


if __name__ == "__main__":
    unittest.main()
