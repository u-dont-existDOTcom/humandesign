#!/usr/bin/env python3
"""Portable documentary source/branch-boundary regression tests, not empirical validation."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
COUNTS = [
    5,
    12,
    9,
    11,
    5,
    12,
    6,
    11,
    11,
    9,
    11,
    6,
    11,
    8,
    10,
    9,
    12,
    12,
    4,
    12,
    12,
    13,
    11,
    10,
    12,
    6,
    8,
]
FRAMES = [
    [702],
    [702, 703],
    [703],
    [703],
    [703],
    [703, 704],
    [704],
    [704],
    [705],
    [705],
    [705],
    [705, 706],
    [706],
    [706],
    [706, 707],
    [707],
    [707],
    [707, 708],
    [708],
    [708],
    [708, 709],
    [709],
    [709, 710],
    [710],
    [710],
    [710],
    [710, 711],
]
PART_GROUPS = [8, 7, 7, 5]
EXPECTED_FIRST_ROLES = [
    "chapter_heading",
    "saturn_body",
    "saturn_benefic_aspect",
    "saturn_adverse_aspect",
    "saturn_terms",
    "jupiter_body",
    "jupiter_benefic_aspect",
    "jupiter_adverse_aspect",
    "mars_body",
    "mars_benefic_aspect",
    "mars_adverse",
    "mars_terms",
    "sun_body",
    "sun_benefic",
    "sun_adverse",
    "venus_body",
    "venus_benefic",
    "venus_adverse",
    "venus_terms",
    "mercury_body",
    "mercury_benefic",
    "mercury_adverse",
    "moon_body",
    "moon_benefic",
    "moon_adverse",
    "cusp_11",
    "cusp_12",
]


def load(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class SourceIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = load("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.rules = load("RULES.json")
        cls.map = load("SOURCE_TO_RECORD_MAP.json")
        cls.witness = load("ORIGINAL_SOURCE_WITNESS.json")
        cls.window = load("ORIGINAL_SOURCE_WINDOW_V1.json")
        cls.guard = load("CLX_HISTORICAL_DIRECTIONS_VALIDATION_GUARD_V1.json")
        cls.limits = load("UNRESOLVED_SOURCE_LIMITS.json")
        cls.accept = load("ACCEPTANCE.json")

    def test_accepted_parent_boundary(self):
        self.assertEqual(self.window["current_accepted_lilly"], 11067)
        self.assertEqual(self.window["next_historical_record"], "R11068")

    def test_exact_record_sequence(self):
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(11068, 11326))
        )

    def test_end_count(self):
        self.assertEqual((self.rules["record_count"], self.rules["last_record"]), (258, "R11325"))
        self.assertEqual(
            (self.accept["prior_lilly"], self.accept["lilly_if_published"]), (11067, 11325)
        )
        self.assertEqual(self.accept["combined_if_published"], 12391)

    def test_source_group_counts(self):
        self.assertEqual(self.map["source_group_count"], 27)
        self.assertEqual([len(g["claims"]) for g in self.source["groups"]], COUNTS)
        self.assertEqual([g["original_pdf_frames"] for g in self.source["groups"]], FRAMES)

    def test_mapping_bijection(self):
        rule_ids = [r["id"] for r in self.rules["rules"]]
        map_ids = [rid for g in self.map["source_groups"] for rid in g["mapped_record_ids"]]
        author_ids = [c["id"] for g in self.source["groups"] for c in g["claims"]]
        self.assertEqual(rule_ids, map_ids)
        self.assertEqual(rule_ids, author_ids)
        self.assertEqual(len(set(map_ids)), 258)

    def test_qualifications_retained(self):
        for r in self.rules["rules"]:
            self.assertGreater(len(r["source_anchor_not_diplomatic"]), 4)
            self.assertGreater(len(r["historical_meaning_only"]), 17)
            self.assertGreater(len(r["qualification"]), 2)

    def test_roles_unique(self):
        roles = [r["role"] for r in self.rules["rules"]]
        self.assertEqual(len(roles), len(set(roles)))

    def test_seam_exact(self):
        self.assertEqual(self.window["printed_CLX"]["starts_original_pdf"], 702)
        self.assertEqual(self.window["printed_CLX"]["ends_original_pdf"], 711)
        self.assertEqual(self.window["following_printed_CLXI"]["heading_original_pdf"], 711)
        self.assertEqual(self.rules["following_printed"], "CLXI")
        self.assertEqual(
            [r["role"] for r in self.rules["rules"][-2:]], ["next_CLXI_divider", "next_fixedstars"]
        )
        self.assertNotIn("next_CLXII", [r["role"] for r in self.rules["rules"]])

    def test_no_source_after_clx(self):
        self.assertEqual(self.rules["body_pdf_frames"], list(range(702, 712)))
        for r in self.rules["rules"]:
            self.assertTrue(set(r["original_pdf_frames"]) <= set(range(702, 712)))

    def test_no_human_promotion(self):
        for r in self.rules["rules"]:
            for field in (
                "independent_real_event_timing_accuracy_validated",
                "independent_health_or_death_prediction_validated",
                "independent_relationship_or_financial_prediction_validated",
                "independent_faith_personality_or_crime_label_validated",
                "original_directions_angle_date_conversion_verified",
                "original_1647_fixed_star_modern_epoch_parity_verified",
                "real_person_health_safety_social_status_advice_authorized",
                "runtime_model_promoted",
            ):
                self.assertIs(r[field], False)
        self.assertFalse(self.guard["real_human_predictive_accuracy_demonstrated"])
        self.assertEqual(self.rules["runtime_promotions"], 0)
        self.assertEqual(self.rules["empirical_validations"], 0)

    def test_historical_high_stakes_no_promotion(self):
        high = [r for r in self.rules["rules"] if "high-stakes" in r["qualification"]]
        self.assertGreaterEqual(len(high), 9)
        self.assertFalse(
            self.guard[
                "owner_person_specific_health_harm_mortality_finance_relationship_inference_authorized"
            ]
        )

    def test_accepted_source_only(self):
        self.assertTrue(self.source["source_only"])
        self.assertEqual(self.source["real_person_directions_validated"], 0)
        self.assertFalse(self.limits["original_primary_directions_time_engine_verified"])
        self.assertFalse(
            self.limits["real_person_medical_criminal_religious_or_safety_advice_authorized"]
        )

    def test_aspect_conditional_completeness(self):
        roles = set(r["role"] for r in self.rules["rules"])
        for key in (
            "saturn_body",
            "saturn_benefic_aspect",
            "saturn_adverse_aspect",
            "saturn_terms",
            "jupiter_body",
            "jupiter_benefic_aspect",
            "jupiter_adverse_aspect",
            "jupiter_terms",
            "mars_body",
            "mars_benefic_aspect",
            "mars_adverse",
            "mars_terms",
            "sun_body",
            "sun_benefic",
            "sun_adverse",
            "venus_body",
            "venus_benefic",
            "venus_adverse",
            "venus_terms",
            "mercury_body",
            "mercury_benefic",
            "mercury_adverse",
            "mercury_terms",
            "moon_body",
            "moon_benefic",
            "moon_adverse",
            "cusp_11",
            "cusp_12",
            "horoscope_rare",
        ):
            self.assertIn(key, roles)

    def test_class_and_radix_modifiers(self):
        classes = [r for r in self.rules["rules"] if "birth-class" in r["qualification"]]
        radix = [r for r in self.rules["rules"] if "radix-condition" in r["qualification"]]
        self.assertGreaterEqual(len(classes), 32)
        self.assertGreaterEqual(len(radix), 9)

    def test_explicit_qualifying_counterexamples(self):
        roles = set(x["role"] for x in self.rules["rules"])
        for role in (
            "jupiter_attack_fails",
            "mars_soldier",
            "sun_pride",
            "mercury_scandal",
            "moon_alternates",
            "moon_if_living",
            "moon_capability",
            "venus_hasty_marriage",
        ):
            self.assertIn(role, roles)

    def test_no_chinese_count_mixing(self):
        self.assertEqual(self.window["parallel_chinese_source_annotations"], 72)
        self.assertEqual(self.accept["new_historical_annotations"], 258)
        self.assertEqual(self.accept["prior_ptolemy"], 1066)

    def test_rule_hash_matches_acceptance(self):
        self.assertEqual(sha(B / "RULES.json"), self.accept["rules_sha256"])

    def test_window_witness_consistency(self):
        self.assertEqual(
            self.witness["full_original_1647_pdf_sha256"],
            self.window["original_pdf_894_frames_sha256"],
        )
        self.assertEqual(self.witness["body_original_pdf_frames"], list(range(702, 712)))

    def test_no_additional_chapter_claims(self):
        self.assertEqual(self.accept["numbered_chapters_added"], 1)
        self.assertEqual(self.rules["printed_chapter"], "CLX")
        self.assertEqual(self.accept["next_navigation"], 2)
        self.assertEqual(self.accept["substantive"], 256)


def make_group_check(index, expected_n, expected_pages, first_role):
    def test(self):
        original = self.source["groups"][index]
        lookup = self.map["source_groups"][index]
        self.assertEqual(original["source_span"], f"B07q-S{index + 1:03d}")
        self.assertEqual(original["original_pdf_frames"], expected_pages)
        self.assertEqual(len(original["claims"]), expected_n)
        self.assertEqual(original["claims"][0]["role"], first_role)
        self.assertEqual([c["id"] for c in original["claims"]], lookup["mapped_record_ids"])
        self.assertTrue(all(not c["runtime_promoted"] for c in original["claims"]))

    return test


for n, (count, pages, role) in enumerate(zip(COUNTS, FRAMES, EXPECTED_FIRST_ROLES, strict=True), 1):
    setattr(SourceIntegrity, f"test_group_{n:03d}", make_group_check(n - 1, count, pages, role))


def make_photo_check(number):
    def test(self):
        name = str(number)
        manifest = self.window["photos"][name]
        saved = self.witness["photos"][name]
        file = B / manifest["file"]
        self.assertEqual(file.stat().st_size, manifest["bytes"])
        self.assertEqual(sha(file), manifest["sha256"])
        self.assertEqual(saved["sha256"], manifest["sha256"])
        self.assertTrue(
            saved["role"] == ("CLX_BODY_OR_BOUNDARY" if number <= 711 else "CLXI_CONTEXT_NOT_CLX")
        )

    return test


for n in range(702, 714):
    setattr(SourceIntegrity, f"test_photo_{n}", make_photo_check(n))


def make_part_check(index, n):
    def test(self):
        part = load(self.map["source_parts"][index])
        self.assertEqual((part["batch"], part["part"]), ("B07q", index + 1))
        self.assertEqual(len(part["groups"]), n)
        self.assertTrue(part["source_only"])
        self.assertEqual(part["verified_human_predictions"], 0)

    return test


for i, n in enumerate(PART_GROUPS):
    setattr(SourceIntegrity, f"test_part_{i + 1}", make_part_check(i, n))


if __name__ == "__main__":
    unittest.main()
