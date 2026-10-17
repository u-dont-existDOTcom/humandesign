"""First-edition Lilly wealth durability documentary source verification.

Passing checks prove source-record integrity, not human predictive accuracy.
"""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class OriginalWealthDurability(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.author = j("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = j("RULES.json")
        cls.cross = j("SOURCE_TO_RECORD_MAP.json")
        cls.witness = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.limits = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.a = j("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])

    def anchor_text(self):
        return " ".join(x["original_anchor_not_diplomatic"] for x in self.r["rules"])

    def test_01_original_source_jpeg_bytes_and_hashes(self):
        self.assertEqual(list(self.witness["images"]), [str(x) for x in range(596, 601)])
        for image in self.witness["images"].values():
            path = B / image["file"]
            self.assertEqual(sha(path), image["sha256"])
            self.assertEqual(path.stat().st_size, image["bytes"])
            self.assertEqual(path.read_bytes()[:2], bytes.fromhex("ffd8"))

    def test_02_original_printed_folios_in_sequence(self):
        self.assertEqual(
            [x["original_printed_page"] for x in self.witness["images"].values()],
            ["562", "563", "564", "565", "566"],
        )
        self.assertEqual(self.witness["source_body_pages"], [596, 597, 598])

    def test_03_next_two_distinct_boundaries_on_frame_598(self):
        self.assertEqual(self.witness["first_following_unnumbered_heading_page"], 598)
        self.assertEqual(self.witness["next_printed_chapter_CXVIII_heading_page"], 598)

    def test_04_consecutive_ids_and_navigations(self):
        self.assertEqual(
            [r["record_number"] for r in self.r["rules"]],
            list(range(7052, 7127)),
        )
        self.assertEqual(
            [x["id"] for x in self.r["rules"] if x["role"] == "next_section_navigation"],
            ["R7124", "R7125", "R7126"],
        )

    def test_05_bidirectional_source_groups_complete(self):
        ids = []
        for original, cross in zip(
            self.author["source_groups"], self.cross["source_groups"], strict=True
        ):
            self.assertEqual(original["source_span"], cross["source_span"])
            self.assertEqual(original["original_pdf_frames"], cross["original_pdf_frames"])
            expected = [x["id"] for x in original["claims"]]
            self.assertEqual(expected, cross["mapped_record_ids"])
            ids.extend(expected)
        self.assertEqual(ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(len(set(ids)), len(ids))
        self.assertEqual(self.cross["source_group_count"], 13)

    def test_06_favorable_second_house_requires_three_conditions(self):
        self.assertEqual(self.roles["positive_condition"], 3)
        self.assertIn("powerfull", self.anchor_text())
        self.assertIn("essentially qualified", self.anchor_text())

    def test_07_weak_house_planet_allows_continued_wealth_and_loss(self):
        self.assertEqual(self.roles["weak_variability"], 2)
        self.assertIn("continue, but with great hazard", self.anchor_text())
        self.assertIn("lose somewhat equivalent", self.anchor_text())

    def test_08_malefic_second_strong_versus_unfortunate(self):
        self.assertEqual(self.roles["malefic_positive"], 3)
        self.assertEqual(self.roles["malefic_negative"], 2)
        self.assertEqual(self.roles["malefic_middle"], 1)

    def test_09_multiple_occupants_prioritize_strongest(self):
        self.assertEqual(self.roles["multi_occupancy"], 1)
        self.assertEqual(self.roles["strongest_priority"], 2)

    def test_10_empty_second_ruler_and_fortune_dispositor(self):
        self.assertEqual(self.roles["no_occupant"], 1)
        self.assertEqual(self.roles["fallback"], 2)
        self.assertIn("Lord of the second house", self.anchor_text())
        self.assertIn("Dispositor of Part of Fortune", self.anchor_text())

    def test_11_directed_part_of_fortune_and_other_targets(self):
        self.assertEqual(self.roles["timing_primary"], 2)
        self.assertEqual(self.roles["timing_targets"], 3)
        self.assertEqual(self.roles["timing_contacts"], 1)
        self.assertEqual(self.roles["timing_aspects"], 1)

    def test_12_aspect_glyph_uncertain_not_executable(self):
        row = next(x for x in self.r["rules"] if x["role"] == "timing_contacts")
        self.assertEqual(row["qualification"], "glyph-unresolved")
        self.assertIn("ambiguous", row["original_anchor_not_diplomatic"])

    def test_13_youth_adult_older_and_late_house_quadrants(self):
        self.assertEqual(self.roles["timing_youth"], 1)
        self.assertEqual(self.roles["timing_adulthood"], 2)
        self.assertEqual(self.roles["timing_older"], 2)
        self.assertEqual(self.roles["timing_late"], 1)

    def test_14_explicit_ages_overlap_and_lifespan_fudge(self):
        text = self.anchor_text()
        for token in (
            "twenty five to thirty five or forty",
            "after forty",
            "before fifty five",
            "live many or few yeers",
        ):
            self.assertIn(token, text)
        self.assertEqual(self.roles["timing_life_adjustment"], 2)

    def test_15_solar_orientation_motion_and_concurrence(self):
        self.assertEqual(self.roles["orientation"], 2)
        self.assertEqual(self.roles["movement"], 2)
        self.assertEqual(self.roles["timing_confirmation"], 2)

    def test_16_second_ruler_combust_fortune_afflicted_legal_stereotype(self):
        self.assertEqual(self.roles["adverse_configuration"], 2)
        self.assertEqual(self.roles["adverse_result"], 1)
        self.assertTrue(self.limits["clinical_or_financial_actions_authorized"] is False)

    def test_17_angular_vs_cadent_luminary_contrary_claims(self):
        self.assertEqual(self.roles["luminary_condition"], 1)
        self.assertEqual(self.roles["luminary_opposite"], 1)
        self.assertEqual(self.roles["luminary_result"], 2)
        self.assertIn("left by Ancestors", self.anchor_text())

    def test_18_fixed_stars_and_geometry_both_present(self):
        self.assertEqual(self.roles["stellar_condition"], 2)
        self.assertEqual(self.roles["stellar_result"], 1)
        text = self.anchor_text()
        for token in ("Oculus Tauri", "Caput Medusae", "Part of Fortune or joyned"):
            self.assertIn(token, text)

    def test_19_saturn_character_stereotype_and_luminary_exception(self):
        self.assertEqual(self.roles["stereotype"], 1)
        self.assertEqual(self.roles["stereotype_exception"], 1)
        self.assertIn("covetous", self.anchor_text())

    def test_20_compound_poverty_requires_multiple_conditions(self):
        self.assertEqual(self.roles["compound_condition"], 5)
        self.assertEqual(self.roles["compound_result"], 1)
        for token in ("Retrograde", "Cadent", "Peregrine", "contrary nature"):
            self.assertIn(token, self.anchor_text())

    def test_21_no_unreviewed_glyph_as_numeric_operator(self):
        self.assertGreaterEqual(
            sum(
                x["qualification"] in {"ambiguous", "glyph-unresolved", "glyph-qualified"}
                for x in self.r["rules"]
            ),
            3,
        )
        self.assertTrue(
            any("symbol" in issue or "glyph" in issue for issue in self.limits["issues"])
        )

    def test_22_source_requires_family_and_time_baseline(self):
        text = " ".join(self.limits["issues"])
        self.assertIn("Family inheritance", text)
        self.assertIn("overlapping numerical age", text)

    def test_23_zero_human_financial_validations_and_promotions(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["real_financial_outcomes_validated"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for x in self.r["rules"]:
            self.assertFalse(x["independent_human_financial_validation"])
            self.assertFalse(x["actual_wealth_timing_accuracy_verified"])
            self.assertFalse(x["real_person_moral_or_legal_inference_authorized"])
            self.assertFalse(x["runtime_model_promoted"])

    def test_24_source_history_not_full_diplomatic(self):
        self.assertFalse(self.r["full_diplomatic_transcription"])
        self.assertGreaterEqual(len(self.limits["issues"]), 16)

    def test_25_archive_count_and_hash(self):
        self.assertEqual(self.a["previous_lilly"], 7051)
        self.assertEqual(self.a["lilly_if_published"], 7126)
        self.assertEqual(self.a["combined_historical_if_published"], 8192)
        self.assertEqual(sha(B / "RULES.json"), self.a["rules_sha256"])

    def test_26_following_unnumbered_intro_not_absorbed(self):
        self.assertEqual(self.r["next_section_navigation_records"], 3)
        self.assertEqual(self.a["next_section"], "UNNUMBERED_THIRD_HOUSE_BRETHREN")
        self.assertEqual(self.a["next_section_pdf_frame"], 598)


if __name__ == "__main__":
    unittest.main()
