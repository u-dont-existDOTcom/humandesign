"""Original Lilly parent affection / Regiomontanus historical source integrity.

A green test is documentary and limited arithmetic coherence, not father birth recovery.
"""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class OriginalParentNativeRegiomontanus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = read("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = read("RULES.json")
        cls.map = read("SOURCE_TO_RECORD_MAP.json")
        cls.w = read("ORIGINAL_SOURCE_WITNESS.json")
        cls.p = read("REGIOMONTANUS_HISTORICAL_PROCEDURE_V1.json")
        cls.limits = read("UNRESOLVED_SOURCE_LIMITS.json")
        cls.accept = read("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])
        cls.anchors = " ".join(x["original_anchor_not_diplomatic"] for x in cls.r["rules"])

    def test_01_original_scans_sha_bytes(self):
        self.assertEqual(list(self.w["images"]), ["608", "609", "610", "611"])
        for image in self.w["images"].values():
            path = B / image["file"]
            data = path.read_bytes()
            self.assertEqual(data[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(data), image["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), image["sha256"])

    def test_02_printed_folios_and_numbered_mines_boundary(self):
        self.assertEqual(
            [v["printed_folio"] for v in self.w["images"].values()],
            ["574", "575", "576", "577"],
        )
        self.assertEqual(self.w["body_pdf_frames"], [608, 609])
        self.assertEqual(self.w["following_mines_chapter_CXXVII_frame"], 609)
        self.assertEqual(self.w["following_unnumbered_sixth_house_frame"], 610)

    def test_03_consecutive_ids_two_navigation(self):
        self.assertEqual(
            [x["record_number"] for x in self.r["rules"]],
            list(range(7503, 7549)),
        )
        self.assertEqual(
            [x["id"] for x in self.r["rules"] if x["role"] == "next_chapter_navigation"],
            ["R7547", "R7548"],
        )

    def test_04_bidirectional_claim_source_coverage(self):
        refs = []
        for group, inverse in zip(
            self.a["source_groups"],
            self.map["source_groups"],
            strict=True,
        ):
            self.assertEqual(group["source_span"], inverse["source_span"])
            self.assertEqual(group["original_pdf_frames"], inverse["original_pdf_frames"])
            these = [c["id"] for c in group["clauses"]]
            self.assertEqual(these, inverse["mapped_record_ids"])
            refs.extend(these)
        self.assertEqual(refs, [r["id"] for r in self.r["rules"]])
        self.assertEqual(self.map["source_group_count"], 10)

    def test_05_correct_day_and_night_parent_signifiers(self):
        for role in (
            "day_sect",
            "day_father",
            "day_mother",
            "night_sect",
            "night_father",
            "night_mother",
        ):
            self.assertEqual(self.roles[role], 1)
        self.assertIn("for Mother Moon", self.anchors)
        self.assertIn("for the Father Saturn", self.anchors)

    def test_06_friendly_parent_aspect_targets_and_contrast(self):
        self.assertEqual(self.roles["friendly_target"], 2)
        self.assertEqual(self.roles["friendly_sextile"], 1)
        self.assertEqual(self.roles["friendly_trine"], 1)
        self.assertEqual(self.roles["friendly_result"], 1)
        self.assertEqual(self.roles["harsh_square"], 1)
        self.assertEqual(self.roles["harsh_opposition"], 1)

    def test_07_mother_asymmetric_aspect_excludes_father_support(self):
        self.assertEqual(self.roles["relative_mother_condition"], 1)
        self.assertEqual(self.roles["relative_mother_alternative"], 1)
        self.assertEqual(self.roles["relative_exclusion"], 1)
        self.assertIn("and not Saturn or Sun", self.anchors)

    def test_08_mutual_reception_as_distinct_method(self):
        self.assertEqual(self.roles["reception_condition"], 1)
        self.assertEqual(self.roles["reception_attribution"], 1)
        self.assertEqual(self.roles["reception_result"], 1)

    def test_09_attribution_and_incomplete_original_crosscheck(self):
        self.assertEqual(self.roles["source_attribution"], 1)
        self.assertEqual(self.roles["bibliographic_attribution"], 1)
        self.assertEqual(self.roles["usage_claim"], 1)
        self.assertIn("Problem 24", self.anchors)
        self.assertFalse(self.p["attributions_verified_against_original_regiomontanus"])

    def test_10_algorithm_day_and_sun_angle_exclusion(self):
        self.assertTrue(self.p["source_preconditions"]["day_geniture_required"])
        self.assertTrue(self.p["source_preconditions"]["sun_not_on_tenth_or_fourth_cusp"])
        self.assertEqual(
            self.p["source_preconditions"]["nighttime_alternative_in_this_passage"],
            "NOT_SPECIFIED",
        )
        self.assertEqual(self.roles["algorithm_sect"], 1)
        self.assertEqual(self.roles["algorithm_cusp_exclusion"], 1)

    def test_11_sun_position_and_oblique_ascension_distinct(self):
        self.assertEqual(self.roles["positional_circle"], 1)
        self.assertEqual(self.roles["positional_pole"], 1)
        self.assertEqual(self.roles["ascendant_assignment"], 1)
        self.assertEqual(self.roles["oblique_input"], 1)

    def test_12_declared_ninety_degree_transform_not_real_chart(self):
        self.assertEqual(self.roles["subtraction"], 1)
        self.assertEqual(self.roles["midheaven_ra"], 1)
        expression = self.p["arithmetic_template"]["displayed_expression"]
        self.assertIn("- 90°", expression)
        # Synthetic toy angles only; this does not recover any person's chart.
        self.assertEqual((55.0 - 90.0) % 360.0, 325.0)

    def test_13_house_poles_and_ra_increment_are_separate(self):
        self.assertEqual(self.roles["house_poles"], 1)
        self.assertEqual(self.roles["house_reference"], 1)
        self.assertEqual(self.roles["ra_increment"], 1)
        self.assertEqual(self.p["arithmetic_template"]["house_increment_deg"], 30)
        self.assertEqual(
            self.p["arithmetic_template"]["complete_house_pole_inverse_ascension_algorithm"],
            "MISSING",
        )

    def test_14_ecliptic_inversion_and_named_house_outputs(self):
        self.assertEqual(self.roles["ecliptic_inverse"], 1)
        self.assertEqual(self.roles["target_cusps"], 1)
        self.assertEqual(
            self.p["arithmetic_template"]["intermediate_houses_named"], ["11", "12", "2", "3"]
        )
        self.assertTrue(any("pole" in x.lower() for x in self.limits["issues"]))

    def test_15_regiomontanus_chart_not_independent_birth_recovery(self):
        for role in ("chart_claim", "native_chart_comparison", "planet_positions"):
            self.assertEqual(self.roles[role], 1)
        self.assertEqual(self.p["procedure_status"], "SOURCE_RECONSTRUCTION_ONLY_NON_EXECUTABLE")
        self.assertFalse(self.p["arithmetic_template"]["predicts_real_father_datetime"])
        self.assertEqual(
            self.p["tests_and_limits"]["independent_father_birth_time_predictions_validated"], 0
        )

    def test_16_next_mines_and_sixth_house_separated(self):
        self.assertEqual(self.r["substantive_source_annotations"], 44)
        self.assertEqual(self.r["following_navigation"], 2)
        self.assertEqual(self.accept["next_printed"], "CXXVII")

    def test_17_no_human_life_validation_or_runtime_promotion(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["independent_father_birth_time_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        self.assertFalse(self.r["regiomontanus_procedure_executable"])
        for x in self.r["rules"]:
            self.assertFalse(x["independent_human_parental_affection_validated"])
            self.assertFalse(x["independent_father_birth_time_recovery_validated"])
            self.assertFalse(x["runtime_algorithm_promoted"])

    def test_18_procedure_hash_and_canonical_count(self):
        self.assertEqual(self.accept["previous_lilly"], 7502)
        self.assertEqual(self.accept["lilly_if_published"], 7548)
        self.assertEqual(self.accept["combined_if_published"], 8614)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.accept["rules_sha256"],
        )
        self.assertEqual(
            hashlib.sha256(
                (B / "REGIOMONTANUS_HISTORICAL_PROCEDURE_V1.json").read_bytes()
            ).hexdigest(),
            self.accept["regiomontanus_source_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
