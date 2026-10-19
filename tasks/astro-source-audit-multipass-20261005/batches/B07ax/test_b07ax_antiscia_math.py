"""Original Lilly merchant antiscion printed vs arithmetic mismatch regression."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
OUTPUT = B / "MERCHANT_MERCURY_ANTISCION_ORIGINAL_EDITION_SOURCE_CONFLICT_V1.json"
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
ZODIAC = (
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


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def to_arcminutes(v):
    assert len(v) == 3
    return ZODIAC.index(v[0]) * 1800 + v[1] * 60 + v[2]


def zodiac(v):
    s, r = divmod(v % (360 * 60), 1800)
    d, m = divmod(r, 60)
    return [ZODIAC[s], d, m]


class MerchantAntiscionOriginalSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src = j(OUTPUT)
        cls.rows = {r["source_body"]: r for r in cls.src["records"]}
        cls.meta = j(B / "ORIGINAL_MERCHANT_1647_1659_PHOTO_CHECKPOINT_V1.json")

    def test_both_1647_1659_original_table_folio743_photos_sha(self):
        for source_year in (1647, 1659):
            key = f"{source_year}_printed_743"
            witness = self.meta["original_source_photographic_witnesses"][key]
            self.assertEqual(sha(ROOT / witness["file"]), witness["sha256"])
            self.assertEqual(witness["printed_folio"], 743)

    def test_both_1647_1659_original_natal_folio745_photos_sha(self):
        for source_year in (1647, 1659):
            row = self.meta["original_source_photographic_witnesses"][f"{source_year}_printed_745"]
            self.assertEqual(sha(ROOT / row["file"]), row["sha256"])
            self.assertEqual(row["printed_folio"], 745)

    def test_four_derived_readability_crop_shas(self):
        for name, value in self.src["derived_reading_aid_crop_sha256"].items():
            self.assertEqual(sha(B / "evidence" / name), value)

    def test_all_seven_source_bodies_unique(self):
        self.assertEqual(len(self.rows), 7)
        self.assertEqual(
            set(self.rows), {"Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"}
        )

    def test_source_antiscia_six_match_one_transmitted_conflict(self):
        errors = [
            r for r in self.rows.values() if r["printed_antiscion_minus_computed_arcminutes"] != 0
        ]
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["source_body"], "Mercury")
        self.assertEqual(errors[0]["printed_antiscion_minus_computed_arcminutes"], -20)

    def test_Mercury_Libra3_34_vs_Pisces26_06_both_edition_readings(self):
        r = self.rows["Mercury"]
        self.assertEqual(
            r["original_first_1647_and_second_1659_printed_natal_longitude"], ["Libra", 3, 34]
        )
        self.assertEqual(
            r["original_first_1647_and_second_1659_printed_antiscion"], ["Pisces", 26, 6]
        )
        self.assertEqual(r["analytic_solar_axis_reflection_antiscion"], ["Pisces", 26, 26])

    def test_Mercury_contra_antiscion_also_twenty_minute_gap(self):
        r = self.rows["Mercury"]
        self.assertEqual(
            r["original_first_1647_and_second_1659_printed_contra_antiscion"], ["Virgo", 26, 6]
        )
        self.assertEqual(r["analytic_solar_axis_reflection_contra_antiscion"], ["Virgo", 26, 26])

    def test_original_prints_never_replaced_by_formulas(self):
        self.assertTrue(self.src["source_original_tables_preserved_without_interpolation"])
        for r in self.rows.values():
            self.assertFalse(r["may_replace_literal_old_print_in_canonical_original"])
            self.assertFalse(r["underlying_real_natal_chart_position_independently_verified"])

    def test_both_editions_same_source_conflict_not_expert_critical_cause(self):
        self.assertFalse(self.src["historical_author_or_compositor_causation_established"])
        self.assertFalse(self.src["historical_source_natal_longitude_chart_recomputed"])
        self.assertEqual(self.src["analytic_7_body_reflection_matches"], 6)
        self.assertEqual(self.src["analytic_7_body_reflection_mismatches"], 1)

    def test_western_and_chinese_indexes_unchanged(self):
        self.assertEqual(j(INDEX)["records_count"], 12870)
        self.assertEqual(j(CHINA)["sum_source_annotations"], 355)

    def test_no_verified_real_person_predictions(self):
        self.assertEqual(self.src["actual_person_outcomes_predicted_and_verified"], 0)
        self.assertEqual(self.src["astrology_runtime_promotions"], 0)


def one_body(name):
    def test(self):
        r = self.rows[name]
        natal = to_arcminutes(r["original_first_1647_and_second_1659_printed_natal_longitude"])
        expected = (180 * 60 - natal) % (360 * 60)
        self.assertEqual(zodiac(expected), r["analytic_solar_axis_reflection_antiscion"])
        self.assertEqual(
            zodiac(expected + 180 * 60), r["analytic_solar_axis_reflection_contra_antiscion"]
        )
        delta = to_arcminutes(r["original_first_1647_and_second_1659_printed_antiscion"]) - expected
        if delta > 180 * 60:
            delta -= 360 * 60
        if delta < -180 * 60:
            delta += 360 * 60
        self.assertEqual(delta, r["printed_antiscion_minus_computed_arcminutes"])

    return test


for name in ("Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"):
    setattr(
        MerchantAntiscionOriginalSource,
        f"test_original_{name.lower()}_antiscion_computation",
        one_body(name),
    )


if __name__ == "__main__":
    unittest.main()
