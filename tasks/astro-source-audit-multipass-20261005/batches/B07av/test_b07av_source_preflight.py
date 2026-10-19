"""Preflight integrity for original Lilly 1647/1659 CLXXIII source inventory.

Source was read once against original printed page photos by one informed
investigator; these tests verify reversible historical data, not human fate.
"""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
PLANETS = ("Saturn", "Jupiter", "Mars", "Venus", "Mercury", "Moon")
TARGETS = ("Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon")


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class RadixSourcePreflight(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = load(B / "RADIX_RETURN_42_SOURCE_CLAIMS_PROVISIONAL_V1.json")
        cls.witness = load(B / "PHOTO_CHECKPOINT_1647_1659_ORIGINAL_V1.json")
        cls.roman = load(B / "ORIGINAL_TRANSIT_NUMERAL_VARIANT_1647_VS_1659_V1.json")
        cls.rows = cls.source["records"]
        cls.by = {(r["returning_planet"], r["radix_place_planet"]): r for r in cls.rows}

    def test_original_Wellcome_1647_complete_book_sha_is_pinned(self):
        self.assertEqual(
            self.source["source_full_1647_book_sha256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )
        self.assertEqual(
            self.witness["source_original_1647_complete_Wellcome_pdf_sha256"],
            self.source["source_full_1647_book_sha256"],
        )

    def test_8_original_historical_source_page_photos_checksum(self):
        self.assertEqual(len(self.witness["photo_witnesses"]), 8)
        for key, meta in self.witness["photo_witnesses"].items():
            p = ROOT / meta["relative_repo_path"]
            self.assertTrue(p.is_file(), key)
            self.assertGreater(meta["bytes"], 200000, key)
            self.assertEqual(p.stat().st_size, meta["bytes"])
            self.assertEqual(sha(p), meta["sha256"])

    def test_full_six_by_seven_unique_source_matrix(self):
        self.assertEqual(len(self.rows), 42)
        self.assertEqual(len(self.by), 42)
        self.assertEqual(set(self.by), {(p, t) for p in PLANETS for t in TARGETS})

    def test_first_edition_pages_and_original_sequence(self):
        self.assertEqual(self.source["printed_original_folios"], [738, 739, 740, 741])
        count = Counter(r["original_1647_printed_folio"] for r in self.rows)
        self.assertEqual(dict(count), {738: 13, 739: 13, 740: 15, 741: 1})
        self.assertEqual([r["returning_planet"] for r in self.rows[0:7]], ["Saturn"] * 7)
        self.assertEqual([r["returning_planet"] for r in self.rows[-7:]], ["Moon"] * 7)

    def test_seven_target_place_classes_are_not_seven_returning_planets(self):
        self.assertEqual(tuple(self.source["returning_planets"]), PLANETS)
        self.assertEqual(tuple(self.source["radix_target_planets"]), TARGETS)
        self.assertTrue(
            self.source["source_section_excludes_solar_return_as_a_seventh_returning_planet"]
        )

    def test_provisional_contiguous_Rs_after_B07au(self):
        self.assertEqual(
            [r["provisional_original_source_annotation_id"] for r in self.rows],
            [f"R{i}" for i in range(12804, 12846)],
        )
        self.assertEqual(
            load(
                ROOT
                / "tasks/astro-source-audit-multipass-20261005"
                / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
            )["records_count"],
            12803,
        )
        self.assertEqual(
            load(
                ROOT
                / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
            )["sum_source_annotations"],
            355,
        )

    def test_source_condition_variants_not_collapsed(self):
        for planet, radix in (
            ("Saturn", "Saturn"),
            ("Jupiter", "Saturn"),
            ("Jupiter", "Moon"),
            ("Venus", "Saturn"),
            ("Venus", "Sun"),
            ("Venus", "Mercury"),
            ("Moon", "Jupiter"),
            ("Moon", "Moon"),
        ):
            self.assertGreater(len(self.by[planet, radix]["source_conditional_qualifiers"]), 0)
        self.assertNotEqual(
            self.by["Saturn", "Jupiter"]["source_historical_claim_paraphrase"],
            self.by["Jupiter", "Saturn"]["source_historical_claim_paraphrase"],
        )

    def test_every_claim_stays_historical_not_person_level_prediction(self):
        for r in self.rows:
            self.assertTrue(r["historical_claim_rather_than_observed_human_outcome"])
            self.assertFalse(r["human_person_prediction_validation"])
            self.assertFalse(r["original_era_natal_radix_location_engine_verified"])
            self.assertFalse(r["source_critical_edition_independent_reader_verified"])
            self.assertFalse(r["runtime_model_promoted"])
            self.assertTrue(r["source_historical_claim_paraphrase"])
            self.assertTrue(r["source_interpretive_domains"])

    def test_first_1647_printed_heading_different_from_1659(self):
        self.assertEqual(
            self.roman["source_original_first_1647_literal_printed_heading"], "CHAP. CLXXIIII."
        )
        self.assertEqual(self.roman["source_second_1659_literal_printed_heading"], "CHAP. CLXXIV.")
        self.assertEqual(self.roman["editorial_chapter_ordinal"], 174)
        self.assertEqual(self.roman["next_source_record_not_yet_accepted"], "R12846")

    def test_heading_photo_crop_binary_identity(self):
        for stem in ("1647", "1659"):
            p = B / self.roman[f"{stem}_heading_crop"]
            self.assertTrue(p.is_file())
            self.assertEqual(sha(p), self.roman[f"{stem}_heading_crop_sha256"])


def one_row(index):
    def test(self):
        r = self.rows[index]
        expected_index = (index % 7) + 1
        self.assertEqual(r["original_relative_order_in_section"], expected_index)
        self.assertEqual(r["provisional_original_source_annotation_id"], f"R{12804 + index}")
        self.assertFalse(r["human_person_prediction_validation"])
        self.assertFalse(r["runtime_model_promoted"])

    return test


for i in range(42):
    setattr(RadixSourcePreflight, f"test_original_cell_{i + 1:02d}", one_row(i))


if __name__ == "__main__":
    unittest.main()
