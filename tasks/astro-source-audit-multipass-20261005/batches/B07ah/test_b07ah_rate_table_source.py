"""B07ah: all 372 original Lilly table cells trace to an earlier photo-only audit.

These tests prove reversible source data mapping and explicit null semantics,
NOT independent historical glyph interpretation or predictive astrology.
"""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
BASE = B.parent
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V5.json"

SIGNS = (
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
)
UNKNOWN = {
    ("Virgo", 1),
    ("Virgo", 18),
    ("Capricorn", 9),
    ("Capricorn", 15),
    ("Aquarius", 5),
    ("Aquarius", 6),
    ("Pisces", 24),
}
DIFFERENCES = {
    ("Taurus", 28),
    ("Leo", 0),
    ("Virgo", 4),
    ("Scorpio", 6),
    ("Scorpio", 21),
    ("Sagittarius", 6),
    ("Sagittarius", 22),
    ("Capricorn", 13),
    ("Aquarius", 0),
    ("Aquarius", 3),
    ("Aquarius", 13),
    ("Aquarius", 15),
    ("Pisces", 6),
    ("Pisces", 30),
}


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class FirstEditionRateTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = j(B / "ORIGINAL_1647_ANNUAL_372_RATE_CROSSWALK_V1.json")
        cls.rules = j(B / "RULES.json")
        cls.accept = j(B / "ACCEPTANCE.json")
        cls.previous = j(BASE / "B07ad/ANNUAL_RATE_PHOTO_OVERLAY_V6.json")
        cls.past = {(r["sign"], r["degree"]): r for r in cls.previous["rows"]}
        cls.current = {(r["sign"], r["original_zodiac_degree_row"]): r for r in cls.data["rows"]}

    def test_original_full_source_identity_not_computed(self):
        self.assertEqual(
            self.data["source_original_1647_full_pdf_sha256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )
        self.assertEqual(self.data["original_pdf_frame"], 745)
        self.assertEqual(self.data["original_rate_printed_folio"], 711)

    def test_source_original_first_edition_photo_binary_sha(self):
        photo = BASE / "B07y/evidence/original_1647_annual_measure_pdf745_3500.jpg"
        self.assertEqual(sha(photo), self.data["source_first_edition_original_photo_pdf745_SHA256"])
        self.assertGreater(photo.stat().st_size, 2000000)

    def test_prior_372_source_overlay_unmodified(self):
        old = BASE / "B07ad/ANNUAL_RATE_PHOTO_OVERLAY_V6.json"
        self.assertEqual(sha(old), self.data["origin_source_overlay_sha256"])
        self.assertEqual(len(self.past), 372)

    def test_all_372_original_sign_degree_keys_unique(self):
        self.assertEqual(len(self.current), 372)
        self.assertEqual(set(self.current), set(self.past))
        self.assertEqual(self.data["original_rate_table_sign_count"], 12)
        self.assertEqual(self.data["original_rate_degrees_per_sign"], 31)

    def test_365_legible_seven_glyph_ambiguous_without_interpolation(self):
        self.assertEqual(
            sum(
                r["literal_original_1647_single_reader_rate_arcminutes_arcseconds"] is not None
                for r in self.current.values()
            ),
            365,
        )
        self.assertEqual(
            {
                k
                for k, r in self.current.items()
                if r["literal_original_1647_single_reader_rate_arcminutes_arcseconds"] is None
            },
            UNKNOWN,
        )
        self.assertEqual(self.data["original_1647_one_reader_legible"], 365)
        self.assertEqual(self.data["original_1647_unresolved"], 7)

    def test_fourteen_literal_derivative_differences_only(self):
        found = {
            k
            for k, r in self.current.items()
            if r["literal_original_1647_single_reader_rate_arcminutes_arcseconds"] is not None
            and r["literal_original_1647_single_reader_rate_arcminutes_arcseconds"]
            != r["modern_derivative_candidate_not_authoritative"]
        }
        self.assertEqual(found, DIFFERENCES)
        self.assertEqual(self.data["original_vs_derived_searchable_text_disagreements"], 14)

    def test_maginus_libra_7_54_25_and_source_unknown_distinct(self):
        self.assertEqual(
            self.current["Libra", 7][
                "literal_original_1647_single_reader_rate_arcminutes_arcseconds"
            ],
            [54, 25],
        )
        self.assertEqual(
            self.current["Libra", 7]["modern_derivative_candidate_not_authoritative"], [54, 25]
        )
        self.assertTrue(self.data["original_second_edition_1659_ambiguous_hints_not_substituted"])

    def test_fourteen_bounded_source_note_ids_zero_gap(self):
        self.assertEqual(self.rules["record_count"], 14)
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(12502, 12516))
        )
        self.assertEqual(self.rules["first_record"], "R12502")
        self.assertEqual(self.rules["last_record"], "R12515")
        self.assertEqual(self.rules["source_groups"], 1)
        self.assertEqual(self.rules["body_pdf_frames"], [745])

    def test_twelve_sign_column_summary_hashes(self):
        self.assertEqual(len(self.data["sign_source_groups"]), 12)
        for i, group in enumerate(self.data["sign_source_groups"]):
            self.assertEqual(group["sign"], SIGNS[i])
            self.assertEqual(group["original_degree_count"], 31)
            rows = [r for r in self.data["rows"] if r["sign"] == group["sign"]]
            encoded = json.dumps(
                rows, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            ).encode()
            self.assertEqual(hashlib.sha256(encoded).hexdigest(), group["data_rows_SHA256_ordered"])
            self.assertEqual(group["one_reader_legible"] + group["original_glyph_unresolved"], 31)

    def test_new_14_records_not_fake_372_history_ids(self):
        self.assertEqual(self.accept["new_historical_source_note_records"], 14)
        self.assertTrue(self.rules["original_372_rate_cells_are_separate_reversible_source_data"])
        self.assertEqual(self.accept["next_original_R"], "R12516")
        self.assertEqual(self.accept["next_original_PDF"], 746)

    def test_earlier_Lilly_and_chinese_histories_untouched(self):
        self.assertEqual(j(WEST)["records_count"], 12501)
        self.assertEqual(j(CHINA)["sum_source_annotations"], 262)
        self.assertEqual(self.accept["prior_Lilly"], 12501)
        self.assertEqual(self.accept["Chinese_V5_parallel"], 262)

    def test_original_page_not_fully_expert_critically_collated(self):
        self.assertTrue(self.data["source_photo_claim_made_by_one_unblinded_reader_only"])
        self.assertFalse(
            self.data["original_1647_first_and_second_print_source_expert_collation_done"]
        )
        self.assertFalse(self.data["historical_annual_measure_arithmetic_validated"])
        self.assertFalse(self.rules["full_CLXVI_historical_source_chapter_complete"])
        self.assertFalse(self.rules["verified_true_historical_annual_direction_time_engine"])

    def test_no_1647_astrology_person_predictions(self):
        self.assertFalse(
            self.data["model_use_as_accurate_astro_calendar_or_event_prediction_authorized"]
        )
        self.assertEqual(self.data["empirical_real_human_validations"], 0)
        self.assertEqual(self.rules["independent_human_predictive_validations"], 0)
        self.assertEqual(self.rules["runtime_promotions"], 0)
        self.assertTrue(all(not r["runtime_promoted"] for r in self.data["rows"]))

    def test_acceptance_references_bytes_shas(self):
        self.assertEqual(
            self.accept["source_rate_crosswalk_SHA256"],
            sha(B / "ORIGINAL_1647_ANNUAL_372_RATE_CROSSWALK_V1.json"),
        )
        self.assertEqual(self.accept["rules_SHA256"], sha(B / "RULES.json"))
        self.assertEqual(
            self.accept["source_b07ad_overlay_sha256"],
            sha(BASE / "B07ad/ANNUAL_RATE_PHOTO_OVERLAY_V6.json"),
        )


def verify_1647_cell(k):
    def test(self):
        cur = self.current[k]
        prev = self.past[k]
        self.assertEqual(
            cur["literal_original_1647_single_reader_rate_arcminutes_arcseconds"],
            prev["first_edition_1647_one_reader_photo_rate"],
        )
        self.assertEqual(
            cur["original_1647_unresolved_print_glyph_options"],
            prev["unresolved_original_source_glyph_options"],
        )
        self.assertEqual(
            cur["modern_derivative_candidate_not_authoritative"],
            prev["frozen_B07x_derivative_candidate"],
        )
        self.assertFalse(cur["runtime_promoted"])

    return test


for sign in SIGNS:
    for degree in range(31):
        setattr(
            FirstEditionRateTable,
            f"test_cell_{sign.lower()}_{degree:02d}",
            verify_1647_cell((sign, degree)),
        )


if __name__ == "__main__":
    unittest.main()
