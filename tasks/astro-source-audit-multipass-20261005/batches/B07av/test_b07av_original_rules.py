"""Original Lilly CLXXIII planet↔radix source notes and edition witnesses.

These assertions preserve documentary fidelity and editorial boundaries.
No one-reader source passage demonstrates actual-event predictive success.
"""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
WEST = (
    ROOT / "tasks/astro-source-audit-multipass-20261005" / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
)
CHINESE = (
    ROOT / "tasks/astro-chinese-primary-sources-20261017" / "CHINESE_SOURCE_AUDIT_INDEX_V7.json"
)
PLANETS = ("Saturn", "Jupiter", "Mars", "Venus", "Mercury", "Moon")
RADIX = ("Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon")


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class OriginalCLXXIII(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = j(B / "RADIX_RETURN_42_SOURCE_CLAIMS_PROVISIONAL_V1.json")
        cls.source = j(B / "CLXXIII_42_ORIGINAL_1647_1659_SOURCE_WITNESS_V1.json")
        cls.rules = j(B / "RULES.json")
        cls.accept = j(B / "ACCEPTANCE.json")
        cls.photo = j(B / "PHOTO_CHECKPOINT_1647_1659_ORIGINAL_V1.json")
        cls.edition = j(B / "ORIGINAL_TRANSIT_NUMERAL_VARIANT_1647_VS_1659_V1.json")
        cls.original_by_pair = {
            (a["returning_planet"], a["radix_place_planet"]): a for a in cls.matrix["records"]
        }
        cls.by_pair = {
            (a["returning_revolution_planet"], a["radix_natal_place_planet"]): a
            for a in cls.rules["rules"]
        }

    def test_42_unique_conditional_original_source_records(self):
        self.assertEqual(len(self.by_pair), 42)
        self.assertEqual(set(self.by_pair), {(p, r) for p in PLANETS for r in RADIX})
        self.assertEqual(self.rules["record_count"], 42)

    def test_correct_original_1647_first_edition_full_book_sha(self):
        self.assertEqual(
            self.source["original_full_1647_source_pdf_sha256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )

    def test_photo_pair_folio_to_exact_original_scan(self):
        witnesses = self.source["source_1647_1659_photo_page_witnesses"]
        self.assertEqual(len(witnesses), 4)
        self.assertEqual(
            [v["original_printed_folio"] for v in witnesses],
            [738, 739, 740, 741],
        )
        for x in witnesses:
            folio = x["original_printed_folio"]
            self.assertEqual(x["1647_original_pdf_frame"], folio + 34)
            self.assertEqual(x["1659_original_djvu_frame"], folio + 29)
            for prefix in ("1647", "1659"):
                path = ROOT / x[f"{prefix}_source_file"]
                self.assertEqual(sha(path), x[f"{prefix}_sha256"])
                self.assertTrue(path.is_file())
            self.assertFalse(x["independently_blinded_second_human_reader"])

    def test_exact_R_sequence_and_source_photo_frame(self):
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]],
            list(range(12804, 12846)),
        )
        self.assertEqual(
            [r["id"] for r in self.rules["rules"]],
            [f"R{i}" for i in range(12804, 12846)],
        )
        for rule in self.rules["rules"]:
            self.assertEqual(
                rule["original_pdf_frames"],
                [rule["original_printed_folio"] + 34],
            )
            self.assertEqual(
                rule["source_span"],
                f"B07av-S{rule['original_printed_folio'] - 737:03d}",
            )

    def test_source_1647_revolution_planet_is_distinct_from_radix(self):
        self.assertEqual(tuple(self.source["historical_returning_planets"]), PLANETS)
        self.assertEqual(tuple(self.source["historical_radix_target_planets"]), RADIX)
        self.assertTrue(self.source["six_returning_planets_seven_radix_places_not_seven_returning"])
        self.assertNotIn(("Sun", "Sun"), self.by_pair)

    def test_original_1647_next_chapter_numeral_not_1659_numeral(self):
        self.assertEqual(self.rules["source_next_1647_literal_heading"], "CLXXIIII")
        self.assertEqual(self.rules["source_next_1659_literal_heading"], "CLXXIV")
        self.assertEqual(self.rules["source_next_editorial_chapter_ordinal"], 174)
        self.assertEqual(self.accept["next_1647_literal_chapter_numeral"], "CLXXIIII")
        self.assertEqual(self.accept["next_1659_literal_chapter_numeral"], "CLXXIV")

    def test_four_printed_folios_and_asymmetric_conditional_claims(self):
        self.assertEqual(self.rules["body_pdf_frames"], [772, 773, 774, 775])
        self.assertEqual(self.by_pair["Venus", "Mercury"]["original_printed_folio"], 740)
        self.assertEqual(self.by_pair["Moon", "Moon"]["original_printed_folio"], 741)
        self.assertNotEqual(
            self.by_pair["Jupiter", "Saturn"]["historical_meaning_only"],
            self.by_pair["Saturn", "Jupiter"]["historical_meaning_only"],
        )

    def test_retain_natal_and_revolution_conditional_qualifiers(self):
        for r, n in (
            ("Saturn", "Saturn"),
            ("Jupiter", "Saturn"),
            ("Jupiter", "Moon"),
            ("Venus", "Saturn"),
            ("Venus", "Sun"),
            ("Venus", "Mercury"),
            ("Moon", "Jupiter"),
            ("Moon", "Moon"),
        ):
            self.assertTrue(self.by_pair[r, n]["source_conditional_qualifiers"])

    def test_risky_historical_moral_illness_death_claims_not_promoted(self):
        for pair in (
            ("Saturn", "Moon"),
            ("Mars", "Venus"),
            ("Mercury", "Mars"),
            ("Moon", "Mars"),
        ):
            claim = self.by_pair[pair]
            self.assertFalse(claim["historical_personality_wealth_family_health_death_efficacy"])
            self.assertFalse(claim["live_human_high_stakes_advice_authorized"])
            self.assertFalse(claim["independent_real_event_prediction_validated"])
        self.assertEqual(self.source["actual_real_human_prediction_validations"], 0)

    def test_previous_original_Western_and_Chinese_indexes_untouched(self):
        w = j(WEST)
        c = j(CHINESE)
        self.assertEqual(w["records_count"], 12803)
        self.assertEqual(w["batches"][-1]["id"], "B07au")
        self.assertEqual(w["next"]["chapter"], "CLXXIII")
        self.assertEqual(c["sum_source_annotations"], 355)

    def test_acceptance_hash_provenance_and_nonpromotion(self):
        self.assertEqual(
            self.accept["source_full_doc_sha256"],
            sha(B / "CLXXIII_42_ORIGINAL_1647_1659_SOURCE_WITNESS_V1.json"),
        )
        self.assertEqual(
            self.accept["source_original_candidate_matrix_sha256"],
            sha(B / "RADIX_RETURN_42_SOURCE_CLAIMS_PROVISIONAL_V1.json"),
        )
        self.assertEqual(
            self.accept["source_photographic_manifest_sha256"],
            sha(B / "PHOTO_CHECKPOINT_1647_1659_ORIGINAL_V1.json"),
        )
        self.assertEqual(self.accept["rules_sha256"], sha(B / "RULES.json"))
        self.assertFalse(self.rules["historical_radix_return_chart_engine_verified"])
        self.assertFalse(self.source["complete_expert_critical_edition_collation"])
        self.assertEqual(self.rules["runtime_promotions"], 0)

    def test_next_transit_chapter_same_physical_page(self):
        self.assertEqual(self.accept["next_R"], "R12846")
        self.assertEqual(self.accept["next_original_pdf_frame"], 775)
        self.assertEqual(self.accept["next_original_printed_folio"], 741)
        self.assertEqual(self.accept["next_chapter_heading"], "Of the TRANSIT of the Planets.")
        self.assertFalse(self.accept["radix_return_accurate_birth_engine_verified"])


def one_source_rule(i):
    def test(self):
        a = self.rules["rules"][i]
        b = self.matrix["records"][i]
        self.assertEqual(a["id"], f"R{12804 + i}")
        self.assertEqual(a["historical_meaning_only"], b["source_historical_claim_paraphrase"])
        self.assertEqual(a["returning_revolution_planet"], b["returning_planet"])
        self.assertEqual(a["radix_natal_place_planet"], b["radix_place_planet"])
        self.assertFalse(a["runtime_model_promoted"])
        self.assertFalse(a["independent_real_event_prediction_validated"])

    return test


for n in range(42):
    setattr(OriginalCLXXIII, f"test_source_return_{n + 1:02d}", one_source_rule(n))


if __name__ == "__main__":
    unittest.main()
