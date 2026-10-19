"""B07ax Merchant original 1647 and actual 1659 source fidelity and arithmetic.

Tests historical book-source witnesses, 30 disjoint R-records, prior corpus
immutability and seven planet antiscion arithmetic. The known merchant
is not an independent blinded human prediction cohort.
"""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
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


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def longitude(pos):
    name, d, m = pos
    if name not in SIGNS or type(d) is not int or type(m) is not int:
        raise ValueError("Source zodiac angle is required")
    if not (0 <= d < 30 and 0 <= m < 60):
        raise ValueError("Source sexagesimal position out of bounds")
    return (SIGNS.index(name) * 30 + d) * 60 + m


def reflect_antiscion(pos):
    arc_minutes = (180 * 60 - longitude(pos)) % (360 * 60)
    return [
        SIGNS[arc_minutes // (30 * 60)],
        arc_minutes % (30 * 60) // 60,
        arc_minutes % 60,
    ]


class FirstEditionMerchant(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.photos = j(B / "ORIGINAL_MERCHANT_1647_1659_PHOTO_CHECKPOINT_V1.json")
        cls.math = j(B / "MERCHANT_MERCURY_ANTISCION_ORIGINAL_EDITION_SOURCE_CONFLICT_V1.json")
        cls.notes = j(B / "ORIGINAL_1647_1659_MERCHANT_NATIVITY_30_SOURCE_NOTES_V1.json")
        cls.candidates = j(B / "MERCHANT_NATIVITY_SOURCE_CANDIDATES_V1.json")
        cls.rules = j(B / "RULES.json")
        cls.accept = j(B / "ACCEPTANCE.json")
        cls.earlier = j(WEST)
        cls.chinese = j(CHINA)
        cls.by_body = {r["source_body"]: r for r in cls.math["records"]}

    def test_frozen_original_1647_book_SHA(self):
        expected = "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        self.assertEqual(self.earlier["source_sha256"], expected)
        self.assertEqual(self.photos["original_1647_Wellcome_full_scan_sha256"], expected)
        self.assertEqual(self.notes["source_full_original_1647_pdf_sha256"], expected)

    def test_all_ten_source_pages_independently_sha_witnessed(self):
        originals = self.photos["original_source_photographic_witnesses"]
        self.assertEqual(len(originals), 10)
        for key, img in originals.items():
            file = ROOT / img["file"]
            self.assertTrue(file.is_file(), key)
            self.assertEqual(file.stat().st_size, img["bytes"], key)
            self.assertEqual(sha(file), img["sha256"], key)
            self.assertEqual(img["printed_folio"], int(key.split("_")[-1]))
            self.assertIn(img["printed_year"], (1647, 1659))

    def test_first_and_second_edition_original_heading(self):
        self.assertIn("CLXXV", self.notes["original_first_ed_heading"])
        self.assertEqual(
            self.notes["original_second_ed_heading"], self.notes["original_first_ed_heading"]
        )
        self.assertTrue(
            self.rules["original_first_edition_merchant_section_source_physically_covered"]
        )
        self.assertTrue(self.rules["following_printed_CLXXVI_manners_separate_chapter"])

    def test_source_printed_1616_datetime_not_modern_ephemeris_claim(self):
        birth = self.notes["historic_chart_input_source_only"]
        self.assertEqual(birth["source_printed_year"], 1616)
        self.assertEqual(birth["source_printed_day"], 19)
        self.assertEqual(birth["source_printed_clock_text"], "2 h. 24. 39 P.M.")
        self.assertEqual(birth["source_printed_Latitude"], 53)
        self.assertFalse(birth["original_calendar_style_resolved"])
        self.assertFalse(birth["original_chart_computed_against_modern_ephemeris"])
        self.assertFalse(birth["birth_time_independent_source_certificate"])

    def test_original_humors_four_table_columns_exact(self):
        t = self.notes["source_temperament_source_table_only"]
        self.assertEqual(
            t["literal_first_edition_1647_folio743_counts"],
            {"hot": 7, "moist": 6, "cold": 6, "drie": 7},
        )
        self.assertTrue(t["author_already_knows_native_in_source_text"])
        self.assertTrue(t["retrospective_case_not_blind_or_independent_cohort"])

    def test_eight_planet_dignity_fortitude_debility_net(self):
        expected = [
            ("Saturn", -4),
            ("Jupiter", 9),
            ("Mars", 12),
            ("Sun", -6),
            ("Venus", 16),
            ("Mercury", -3),
            ("Moon", 3),
            ("Part_of_Fortune", 0),
        ]
        actual = [
            (r["body"], r["computed_source_net"])
            for r in self.notes["source_dignity_fortitude_debility_rows"]
        ]
        self.assertEqual(actual, expected)
        for r in self.notes["source_dignity_fortitude_debility_rows"]:
            self.assertEqual(
                r["source_fortitude_points"] - r["source_debility_points"],
                r["computed_source_net"],
            )
            self.assertFalse(r["direct_source_claim_empirically_validated_on_person"])

    def test_antiscion_all_seven_origins_geometry_recomputed(self):
        self.assertEqual(len(self.by_body), 7)
        counts = {"matches": 0, "mismatch": 0}
        for body, r in self.by_body.items():
            expected = reflect_antiscion(
                r["original_first_1647_and_second_1659_printed_natal_longitude"]
            )
            self.assertEqual(expected, r["analytic_solar_axis_reflection_antiscion"])
            contra = expected.copy()
            contra_arc = (longitude(contra) + 180 * 60) % (360 * 60)
            contra = [
                SIGNS[contra_arc // (30 * 60)],
                contra_arc % (30 * 60) // 60,
                contra_arc % 60,
            ]
            self.assertEqual(contra, r["analytic_solar_axis_reflection_contra_antiscion"])
            observed = r["original_first_1647_and_second_1659_printed_antiscion"]
            if observed == expected:
                counts["matches"] += 1
            else:
                counts["mismatch"] += 1
                self.assertEqual(body, "Mercury")
            self.assertFalse(r["may_replace_literal_old_print_in_canonical_original"])
        self.assertEqual(counts, {"matches": 6, "mismatch": 1})

    def test_Mercury_print_vs_arithmetic_20arcminute_mismatch(self):
        r = self.by_body["Mercury"]
        self.assertEqual(
            r["original_first_1647_and_second_1659_printed_natal_longitude"], ["Libra", 3, 34]
        )
        self.assertEqual(
            r["original_first_1647_and_second_1659_printed_antiscion"], ["Pisces", 26, 6]
        )
        self.assertEqual(reflect_antiscion(["Libra", 3, 34]), ["Pisces", 26, 26])
        self.assertEqual(r["printed_antiscion_minus_computed_arcminutes"], -20)
        self.assertEqual(
            r["original_first_1647_and_second_1659_printed_contra_antiscion"], ["Virgo", 26, 6]
        )
        self.assertEqual(r["analytic_solar_axis_reflection_contra_antiscion"], ["Virgo", 26, 26])
        self.assertEqual(self.math["original_minus_formula_arcminutes"], -20)

    def test_cross_edition_source_conflict_is_not_automatically_repaired(self):
        self.assertTrue(self.math["source_original_tables_preserved_without_interpolation"])
        self.assertFalse(self.math["historical_author_or_compositor_causation_established"])
        self.assertFalse(
            self.math["source_not_prospective_independent_birth_chart_validation"] is False
        )
        self.assertEqual(self.math["actual_person_outcomes_predicted_and_verified"], 0)
        self.assertEqual(self.math["astrology_runtime_promotions"], 0)

    def test_mercury_source_photo_hashes_match_page_witnesses(self):
        first = self.photos["original_source_photographic_witnesses"]
        self.assertEqual(
            self.math["source_1647_antiscion_photo_sha256"], first["1647_printed_743"]["sha256"]
        )
        self.assertEqual(
            self.math["source_1659_antiscion_photo_sha256"], first["1659_printed_743"]["sha256"]
        )
        self.assertEqual(
            self.math["source_1647_natal_Mercury_photo_sha256"], first["1647_printed_745"]["sha256"]
        )
        self.assertEqual(
            self.math["source_1659_natal_Mercury_photo_sha256"], first["1659_printed_745"]["sha256"]
        )

    def test_same_source_text_ten_photos_not_ten_independent_humans(self):
        self.assertTrue(self.photos["source_case_is_known_to_author_no_blind_human_validation"])
        self.assertFalse(self.photos["historical_cases_proven_independently_predictive"])
        self.assertFalse(self.photos["original_chart_lunisolar_or_epoch_math_verified"])

    def test_candidate_count_and_exact_unaccepted_registry_boundary(self):
        self.assertEqual(self.earlier["records_count"], 12870)
        self.assertEqual(self.earlier["batches"][-1]["id"], "B07aw")
        self.assertEqual(self.earlier["next"]["chapter"], "CLXXV")
        self.assertEqual(self.earlier["next"]["pdf_page"], 776)
        self.assertEqual(self.chinese["sum_source_annotations"], 355)
        self.assertEqual(self.candidates["entry_count"], 30)
        self.assertEqual(self.rules["record_count"], 30)
        self.assertEqual(self.rules["first_record"], "R12871")
        self.assertEqual(self.rules["last_record"], "R12900")
        self.assertEqual(self.accept["next_historical_R"], "R12901")

    def test_index_checksum_old_b07aw_preserved(self):
        self.assertEqual(self.accept["prior_Lilly"], 12870)
        self.assertEqual(self.accept["Lilly_after_if_admitted"], 12900)
        self.assertEqual(self.accept["Western_after_if_admitted"], 13966)
        self.assertEqual(self.accept["Chinese_V7_retained"], 355)
        self.assertEqual(self.accept["rules_SHA256"], sha(B / "RULES.json"))
        self.assertEqual(
            self.accept["source_notes_SHA256"],
            sha(B / "ORIGINAL_1647_1659_MERCHANT_NATIVITY_30_SOURCE_NOTES_V1.json"),
        )
        self.assertEqual(
            self.accept["photo_witness_SHA256"],
            sha(B / "ORIGINAL_MERCHANT_1647_1659_PHOTO_CHECKPOINT_V1.json"),
        )
        self.assertEqual(
            self.accept["source_antiscion_critical_diagnostic_SHA256"],
            sha(B / "MERCHANT_MERCURY_ANTISCION_ORIGINAL_EDITION_SOURCE_CONFLICT_V1.json"),
        )

    def test_all_source_rules_fail_closed_for_individuals(self):
        self.assertEqual(self.rules["independent_actual_person_outcome_validations"], 0)
        self.assertEqual(self.notes["source_human_outcomes_validated"], 0)
        self.assertEqual(self.rules["runtime_promotions"], 0)
        for r in self.rules["rules"]:
            self.assertFalse(r["independent_real_human_prediction_accuracy_verified"])
            self.assertFalse(
                r["historical_natal_chart_arithmetic_not_recomputed_from_ephemeris"] is False
            )
            self.assertFalse(r["high_stakes_mental_moral_health_fortune_personal_advice_permitted"])
            self.assertFalse(r["runtime_model_promoted"])

    def test_boundaries_not_duplicates(self):
        self.assertEqual(self.rules["rules"][-1]["role"], "manner_chapter_divider")
        self.assertEqual(self.rules["rules"][-1]["original_printed_folio"], 745)
        self.assertEqual(self.accept["next_original_physically_distinct_chapter"], "CLXXVI")
        self.assertEqual(self.accept["next_original_PDF_frame"], 779)

    def test_prior_chinese_source_V7_history_never_replaced(self):
        self.assertEqual(self.chinese["sum_source_annotations"], 355)
        self.assertEqual(self.chinese["systems"][0]["accepted_source_annotations"], 154)
        self.assertEqual(self.chinese["systems"][1]["accepted_source_annotations"], 201)

    def test_reproducible_30_row_map_nonduplicated(self):
        self.assertEqual(len(self.rules["rules"]), 30)
        self.assertEqual(len(self.candidates["entries"]), 30)
        self.assertEqual(len(self.notes["source_records"]), 30)
        for i, (proposal, historical, source) in enumerate(
            zip(
                self.candidates["entries"],
                self.rules["rules"],
                self.notes["source_records"],
                strict=True,
            )
        ):
            self.assertEqual(proposal["proposed_id"], f"R{12871 + i}")
            self.assertEqual(historical["id"], proposal["proposed_id"])
            self.assertEqual(historical, source)
            self.assertEqual(proposal["source_role"], historical["role"])
            self.assertEqual(historical["original_printed_folio"], proposal["folio"])
            self.assertTrue(historical["original_1647_early_print_source_documented"])
            self.assertFalse(historical["runtime_model_promoted"])


def individual_source_test(i):
    def check(self):
        r = self.rules["rules"][i]
        p = self.candidates["entries"][i]
        self.assertEqual(r["id"], f"R{12871 + i}")
        self.assertEqual(r["role"], p["source_role"])
        self.assertEqual(r["original_pdf_frames"], [p["first_source_pdf_frame"]])
        self.assertEqual(r["1659_independently_typeset_djvu_frame"], p["folio"] + 29)
        self.assertFalse(r["runtime_model_promoted"])

    return check


for i in range(30):
    setattr(FirstEditionMerchant, f"test_original_source_R{12871 + i}", individual_source_test(i))


if __name__ == "__main__":
    unittest.main()
