"""Source-only tests of 42 original CLXXIII planetary-return paragraphs and boundary."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT / "tasks/astro-source-audit-multipass-20261005"
WEST = T / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
PLANETS = ("Saturn", "Jupiter", "Mars", "Venus", "Mercury", "Moon")
TARGETS = {"Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"}
HEADINGS = {
    "Saturn": "Of SATURNE.",
    "Jupiter": "Of JUPITER.",
    "Mars": "Of MARS.",
    "Venus": "Of VENUS.",
    "Mercury": "Of MERCURY.",
    "Moon": "Of MOON.",
}


def j(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


class OriginalPlanetReturnSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = j(B / "RULES.json")
        cls.data = j(B / "ORIGINAL_CLXXIII_42_RETURN_SOURCE_CASES_V1.json")
        cls.proof = j(B / "SOURCE_RULE_PROVENANCE_V1.json")
        cls.photo = j(B / "SOURCE_PHOTO_CHECKPOINT_V1.json")
        cls.accept = j(B / "ACCEPTANCE.json")
        cls.originals = cls.rules["rules"][:42]
        cls.navigator = (B / "SECONDARY_FINDING_AID_CLXXIII.txt").read_text(encoding="utf-8")

    def test_one_1647_first_edition_pinned_book(self):
        self.assertEqual(
            self.data["first_1647_original_full_pdf_sha256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        )
        self.assertEqual(
            self.data["original_photo_checkpoint_sha256"],
            sha(B / "SOURCE_PHOTO_CHECKPOINT_V1.json"),
        )

    def test_eight_original_1647_1659_photo_exact_file_shas(self):
        for source, photos in self.photo["source_original_visual_evidence"].items():
            self.assertEqual(len(photos), 4, source)
            for row in photos:
                f = ROOT / row["repo_relative_file"]
                self.assertTrue(f.is_file())
                self.assertEqual(f.stat().st_size, row["bytes"])
                self.assertEqual(sha(f), row["sha256"])
                self.assertEqual(
                    row["PDF_or_DjVu_frame"],
                    row["printed_folio"] + (34 if source == "first_edition_1647" else 29),
                )

    def test_all_42_history_claims_six_times_seven(self):
        self.assertEqual(len(self.originals), 42)
        self.assertEqual(len(self.proof["source_rule_locators"]), 42)
        self.assertEqual(self.rules["historical_return_to_natal_cases"], 42)
        for name in PLANETS:
            group = [r for r in self.originals if r["returning_planet"] == name]
            self.assertEqual(len(group), 7)
            self.assertEqual({r["natal_radix_target"] for r in group}, TARGETS)

    def test_first_and_last_return_and_one_boundary(self):
        self.assertEqual(self.originals[0]["returning_planet"], "Saturn")
        self.assertEqual(self.originals[0]["natal_radix_target"], "Saturn")
        self.assertEqual(self.originals[-1]["returning_planet"], "Moon")
        self.assertEqual(self.originals[-1]["natal_radix_target"], "Moon")
        self.assertEqual(
            self.rules["rules"][-1]["role"], "physical_heading_boundary_next_clxxiv_transits"
        )
        self.assertEqual(self.rules["rules"][-1]["original_pdf_frames"], [775])

    def test_exact_contiguous_unaccepted_IDs_no_parent_reuse(self):
        self.assertEqual(self.rules["record_count"], 43)
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(12804, 12847))
        )
        self.assertEqual(self.accept["next_original_source_R"], "R12847")
        self.assertEqual(self.rules["first_record"], "R12804")
        self.assertEqual(self.rules["last_record"], "R12846")

    def test_original_location_of_six_headings(self):
        pos = [self.navigator.index(HEADINGS[name]) for name in PLANETS]
        self.assertEqual(pos, sorted(pos))
        self.assertEqual(len(pos), 6)
        self.assertTrue(self.rules["Sun_is_natal_target_not_separate_return_heading"])

    def test_original_folios_and_next_distinct_source_chapter(self):
        self.assertEqual(self.rules["body_pdf_frames"], [772, 773, 774, 775])
        self.assertEqual(self.data["source_source_printed_page_span"], [738, 739, 740, 741])
        self.assertEqual(self.accept["next_original_pdf_frame"], 775)
        self.assertEqual(self.accept["next_original_printed_chapter"], "CLXXIV")
        self.assertEqual(self.accept["next_heading"], "Of the TRANSIT of the Planets")

    def test_original_condition_not_silent_coarse_prediction(self):
        conditions = {
            (r["returning_planet"], r["natal_radix_target"]): r[
                "source_original_natal_and_return_conditions"
            ]
            for r in self.originals
        }
        self.assertIn("favorable", conditions["Saturn", "Saturn"].lower())
        self.assertIn("Natal-Saturn".lower(), conditions["Jupiter", "Saturn"].lower())
        self.assertIn("combustion", conditions["Venus", "Saturn"].lower())
        self.assertIn("dignified", conditions["Venus", "Sun"].lower())
        self.assertIn("if married", conditions["Jupiter", "Moon"].lower())
        self.assertIn("fortune/weakness", conditions["Moon", "Moon"].lower())

    def test_parent_accepted_History_not_modified(self):
        old = j(WEST)
        china = j(CHINA)
        self.assertEqual(old["records_count"], 12803)
        self.assertEqual(old["batches"][-1]["id"], "B07au")
        self.assertEqual(old["next"]["chapter"], "CLXXIII")
        self.assertEqual(china["sum_source_annotations"], 355)
        self.assertEqual(self.accept["prior_Lilly_source_annotations"], 12803)

    def test_modern_derivative_not_authoritative_original(self):
        self.assertTrue(self.proof["modern_secondary_is_only_navigation"])
        self.assertTrue(
            self.proof["source_all_42_anchors_exactly_once_within_own_returning_planet_section"]
        )
        self.assertEqual(
            sha(B / "SECONDARY_FINDING_AID_CLXXIII.txt"), self.proof["modern_secondary_text_sha256"]
        )
        for r in self.originals:
            self.assertTrue(r["modern_secondary_text_locator_non_diplomatic"])

    def test_no_critical_second_person_review_or_model(self):
        self.assertFalse(self.data["expert_independent_second_human_source_reading_completed"])
        self.assertFalse(
            self.data["independent_original_birth_epoch_solar_return_chart_parity_verified"]
        )
        self.assertEqual(self.data["actual_real_human_forecasts_validated"], 0)
        self.assertEqual(self.data["runtime_model_promotions"], 0)
        for r in self.originals:
            self.assertFalse(r["independent_person_life_outcome_prediction_validated"])
            self.assertFalse(r["runtime_model_promoted"])

    def test_explicit_source_edition_shas_no_mutation(self):
        self.assertEqual(self.accept["rules_sha256"], sha(B / "RULES.json"))
        self.assertEqual(
            self.accept["source_matrix_sha256"],
            sha(B / "ORIGINAL_CLXXIII_42_RETURN_SOURCE_CASES_V1.json"),
        )
        self.assertEqual(
            self.accept["source_provenance_sha256"], sha(B / "SOURCE_RULE_PROVENANCE_V1.json")
        )


def check_one_original_paragraph(n):
    def test(self):
        r = self.originals[n]
        p = self.proof["source_rule_locators"][n]
        self.assertEqual(r["id"], f"R{12804 + n}")
        self.assertEqual(p["id"], r["id"])
        self.assertEqual(p["first_1647_photo_sha256"], r["source_first_1647_photo_sha256"])
        self.assertEqual(
            p["original_1659_photo_sha256"], r["source_independently_typeset_1659_photo_sha256"]
        )
        self.assertEqual(r["secondary_search_position_relative_CLXXIII"], p["finding_aid_offset"])
        anchor = r["modern_secondary_text_locator_non_diplomatic"]
        self.assertEqual(
            self.navigator[p["finding_aid_offset"] : p["finding_aid_offset"] + len(anchor)], anchor
        )
        self.assertEqual(
            p["finding_aid_fragment_sha256"], hashlib.sha256(anchor.encode("utf-8")).hexdigest()
        )
        self.assertFalse(r["medical_legal_crime_morality_gender_finance_inference_authorized"])

    return test


for i in range(42):
    setattr(
        OriginalPlanetReturnSource,
        f"test_original_photo_source_return_to_radix_{i + 1:02d}",
        check_one_original_paragraph(i),
    )


if __name__ == "__main__":
    unittest.main()
