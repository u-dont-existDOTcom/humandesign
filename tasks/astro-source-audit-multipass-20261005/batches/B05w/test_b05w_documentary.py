"""First-edition fourth-house parent/father evidence checks, not human validations."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text())


class OriginalFourthHouseParentHistory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = read("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = read("RULES.json")
        cls.m = read("SOURCE_TO_RECORD_MAP.json")
        cls.w = read("ORIGINAL_SOURCE_WITNESS.json")
        cls.q = read("UNRESOLVED_SOURCE_LIMITS.json")
        cls.accept = read("ACCEPTANCE.json")
        cls.roles = Counter(r["role"] for r in cls.r["rules"])
        cls.anchors = " ".join(x["original_anchor_not_diplomatic"] for x in cls.r["rules"])

    def test_01_all_original_1647_image_bytes_and_sha(self):
        self.assertEqual(list(self.w["images"]), ["603", "604", "605"])
        for img in self.w["images"].values():
            path = B / img["path"]
            raw = path.read_bytes()
            self.assertEqual(len(raw), img["bytes"])
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(hashlib.sha256(raw).hexdigest(), img["sha256"])

    def test_02_printed_folios_and_mother_boundary(self):
        self.assertEqual(
            [v["printed_folio"] for v in self.w["images"].values()],
            ["569", "570", "571"],
        )
        self.assertEqual(self.w["father_section_body_frames"], [603, 604])
        self.assertEqual(self.w["mother_printed_chapter_CXXII_start_frame"], 604)

    def test_03_all_ids_consecutive_and_two_navigation(self):
        self.assertEqual(
            [r["record_number"] for r in self.r["rules"]],
            list(range(7296, 7358)),
        )
        self.assertEqual(
            [r["id"] for r in self.r["rules"] if r["role"] == "next_chapter_navigation"],
            ["R7356", "R7357"],
        )

    def test_04_reversible_source_to_claim_map(self):
        all_refs = []
        for src, mapped in zip(self.a["groups"], self.m["source_groups"], strict=True):
            self.assertEqual(src["source_span"], mapped["source_span"])
            self.assertEqual(src["page_frames"], mapped["original_pdf_frames"])
            expect = [x["id"] for x in src["claims"]]
            self.assertEqual(expect, mapped["mapped_record_ids"])
            all_refs.extend(expect)
        self.assertEqual(all_refs, [r["id"] for r in self.r["rules"]])
        self.assertEqual(len(self.m["source_groups"]), 12)
        self.assertEqual(len(all_refs), len(set(all_refs)))

    def test_05_father_four_sources_and_day_night_contrast(self):
        self.assertEqual(self.roles["father_indicator"], 3)
        self.assertEqual(self.roles["father_indicator_day"], 1)
        self.assertEqual(self.roles["father_indicator_night"], 1)
        self.assertIn("diurnall Geniture", self.anchors)
        self.assertIn("nocturnall", self.anchors)

    def test_06_all_or_majority_and_benefic_good_aspect(self):
        self.assertIn("these Significators or the most of them", self.anchors)
        self.assertIn("good aspect of Jupiter or Venus", self.anchors)
        self.assertEqual(self.roles["good_result"], 2)

    def test_07_adverse_branch_and_moderacy_not_excluded(self):
        self.assertEqual(self.roles["bad_result"], 2)
        self.assertEqual(self.roles["mixed_condition"], 1)
        self.assertEqual(self.roles["mixed_result"], 1)
        self.assertIn("some be strong and others weak", self.anchors)

    def test_08_multiple_occupants_most_dignified_selection(self):
        self.assertEqual(self.roles["multi_occupant"], 1)
        self.assertEqual(self.roles["strongest_precedence"], 1)
        self.assertEqual(self.roles["mixed_source"], 1)

    def test_09_father_own_nativity_preference_retained(self):
        self.assertEqual(self.roles["external_data_preference"], 1)
        self.assertIn("Fathers own Nativity", self.anchors)

    def test_10_positive_angular_conditions_and_no_malefic(self):
        self.assertIn("their Lords in angles or succedants", self.anchors)
        self.assertIn("no aspect to the Infortunes", self.anchors)

    def test_11_reception_trine_and_sextile_separate(self):
        self.assertEqual(self.roles["fourth_lord"], 1)
        self.assertEqual(self.roles["fourth_lord_alternative"], 2)

    def test_12_ancestry_rank_vs_actual_paternal_survival(self):
        self.assertEqual(self.roles["relative_dignity"], 1)
        self.assertEqual(self.roles["relative_descent"], 1)
        self.assertEqual(self.roles["relative_descent_inverse"], 1)
        self.assertEqual(self.roles["father_longlife_result"], 1)
        self.assertEqual(self.roles["father_dignity_result"], 1)

    def test_13_bad_glyph_mortality_claims_not_encoded(self):
        self.assertEqual(self.roles["mortality_ambiguous"], 1)
        self.assertEqual(self.roles["male_sign_condition"], 1)
        self.assertEqual(self.roles["sun_saturn"], 1)
        for r in self.r["rules"]:
            if r["qualification"] == "glyph-unresolved":
                self.assertFalse(r["runtime_model_promoted"])

    def test_14_mother_longevity_not_father_and_not_prediction(self):
        self.assertEqual(self.roles["male_sign_mother"], 1)
        self.assertEqual(self.roles["child_longevity"], 1)
        self.assertEqual(self.roles["saturn_death_cause"], 1)
        self.assertFalse(self.q["original_diplomatic_transcription_complete"])

    def test_15_next_mother_chapter_navigation_only(self):
        self.assertEqual(self.r["next_printed_chapter_navigation"], 2)
        self.assertEqual(self.r["substantive_source_records"], 60)
        self.assertEqual(self.accept["numbered_chapters_added"], 0)
        self.assertEqual(self.accept["next_printed_chapter"], "CXXII")

    def test_16_no_human_birth_death_socioeconomic_validations(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["independent_parent_predictions"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for x in self.r["rules"]:
            self.assertFalse(x["independent_human_parent_status_validated"])
            self.assertFalse(x["human_lifespan_or_death_cause_validated"])
            self.assertFalse(x["human_socioeconomic_ancestry_validated"])
            self.assertFalse(x["modern_medical_legal_utility"])

    def test_17_record_tally_and_sha_integrity(self):
        self.assertEqual(self.accept["previous_lilly"], 7295)
        self.assertEqual(self.accept["lilly_if_published"], 7357)
        self.assertEqual(self.accept["combined_if_published"], 8423)
        h = hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest()
        self.assertEqual(h, self.accept["rules_sha256"])


if __name__ == "__main__":
    unittest.main()
