"""Original-source documentary integrity tests, NOT natal predictive verification."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text())


def h(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class GeneralFortuneOriginal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.input = j("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = j("RULES.json")
        cls.map = j("SOURCE_TO_RECORD_MAP.json")
        cls.e = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.limit = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.q = j("ACCEPTANCE.json")

    def test_01_original_image_authenticity_and_bytes(self):
        for record in self.e["images"].values():
            path = B / record["path"]
            raw = path.read_bytes()
            self.assertEqual(h(path), record["sha256"])
            self.assertEqual(len(raw), record["bytes"])
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))

    def test_02_original_physical_order_and_folios(self):
        self.assertEqual(
            [row["original_printed_folio"] for row in self.e["images"].values()],
            ["543", "552", "553", "554"],
        )
        self.assertEqual(self.e["source_body_frames"], [585, 586])
        self.assertEqual(self.e["unnumbered_wealth_heading_frame"], 586)

    def test_03_consecutive_identifiers(self):
        self.assertEqual(
            [r["record_number"] for r in self.r["rules"]],
            list(range(6765, 6809)),
        )
        self.assertEqual(self.r["record_count"], 44)

    def test_04_bidirectional_10_group_mapping(self):
        ids = []
        for s, reverse in zip(self.input["groups"], self.map["groups"], strict=True):
            self.assertEqual(s["source_span"], reverse["source_span"])
            self.assertEqual(s["original_pdf_pages"], reverse["pdf_pages"])
            this = [c["id"] for c in s["claims"]]
            self.assertEqual(this, reverse["record_ids"])
            ids.extend(this)
        self.assertEqual(len(self.map["groups"]), 10)
        self.assertEqual(ids, [r["id"] for r in self.r["rules"]])
        self.assertEqual(len(ids), len(set(ids)))

    def test_05_favorable_strength_threshold_and_reception_alternative(self):
        x = " ".join(r["anchor_not_diplomatic"] for r in self.r["rules"])
        self.assertIn("three or four", x)
        self.assertIn("receive one another", x)

    def test_06_outcomes_contain_relative_class_constraint(self):
        x = " ".join(r["anchor_not_diplomatic"] for r in self.r["rules"])
        self.assertIn("ordinary Vogue of his Birth", x)
        self.assertIn("greatest part", x)

    def test_07_distinct_bad_dignity_conditions(self):
        rows = [r for r in self.r["rules"] if r["role"] == "negative_condition"]
        self.assertGreaterEqual(len(rows), 10)
        text = " ".join(r["anchor_not_diplomatic"] for r in rows)
        for term in (
            "Falls or Detriments",
            "abject houses",
            "Peregrine",
            "two Lights peregrine",
            "Saturn and Mars",
            "slow in motion",
        ):
            self.assertIn(term.lower(), text.lower())

    def test_08_sun_and_moon_are_additional_witnesses(self):
        kind = Counter(r["role"] for r in self.r["rules"])
        self.assertEqual(kind["solar_lunar_testimony"], 1)
        self.assertEqual(kind["solar_lunar_condition"], 1)
        self.assertEqual(kind["solar_lunar_confirmation"], 1)

    def test_09_mixed_good_bad_conditions_not_dropped(self):
        kind = Counter(r["role"] for r in self.r["rules"])
        self.assertEqual(kind["mixed_condition"], 3)
        self.assertEqual(kind["mixed_result"], 2)

    def test_10_delayed_blessings_explicit_exception(self):
        text = " ".join(r["anchor_not_diplomatic"] for r in self.r["rules"])
        self.assertIn("yet the events may come slowly", text)
        self.assertIn("very promising Nativity", text)

    def test_11_five_hylegical_directions_and_promittors(self):
        text = " ".join(r["anchor_not_diplomatic"] for r in self.r["rules"])
        self.assertIn("five Hylegicall places", text)
        self.assertIn("Directions", text)
        self.assertIn("Promittors", text)
        self.assertIn("Radix", text)

    def test_12_calibration_and_clock_source_unresolved(self):
        notes = " ".join(self.limit["issues"])
        self.assertIn("untouched", notes)
        self.assertIn("no measured outcomes", notes)
        self.assertIn("precisely predeclared", notes)

    def test_13_cause_and_timing_not_one_claim(self):
        role = Counter(r["role"] for r in self.r["rules"])
        self.assertEqual(role["cause_method"], 1)
        self.assertGreaterEqual(role["timing_method"], 5)

    def test_14_following_wealth_section_not_swallowed(self):
        nav = [r for r in self.r["rules"] if r["role"] == "next_chapter_navigation"]
        self.assertEqual([r["id"] for r in nav], ["R6806", "R6807", "R6808"])
        self.assertEqual(self.e["unnumbered_wealth_heading_frame"], 586)
        self.assertEqual(self.e["next_printed_numbered_chapter_frame"], 587)
        self.assertEqual(self.r["substantive_history_records"], 41)

    def test_15_historical_ambiguous_glyphs_guarded(self):
        self.assertTrue(self.limit["no_independent_predictions"])
        self.assertTrue(self.limit["runtime_admission_forbidden"])
        self.assertIn("glyph", " ".join(self.limit["issues"]))

    def test_16_no_independent_human_predictive_validity(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["independently_correct_life_forecasts"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for row in self.r["rules"]:
            self.assertFalse(row["verified_human_life_outcome_prediction"])
            self.assertFalse(row["prospective_blind_validation"])
            self.assertFalse(row["validated_medical_or_financial_forecast"])
            self.assertFalse(row["runtime_rule_promoted"])

    def test_17_original_source_not_diplomatic(self):
        self.assertFalse(self.r["diplomatic_transcription_complete"])
        self.assertGreaterEqual(len(self.limit["issues"]), 12)

    def test_18_hash_and_count_acceptance(self):
        self.assertEqual(self.q["prior_lilly"], 6764)
        self.assertEqual(self.q["historical_records_added"], 44)
        self.assertEqual(self.q["lilly_if_published"], 6808)
        self.assertEqual(self.q["combined_historical_if_published"], 7874)
        self.assertEqual(h(B / "RULES.json"), self.q["rules_sha256"])


if __name__ == "__main__":
    unittest.main()
