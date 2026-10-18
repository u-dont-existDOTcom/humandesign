"""Photographic CLXI source-first verification, no human astrology forecasts."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
EXPECTED_COUNTS = [3, 11, 7, 6, 9, 8, 7, 12, 7, 9, 9, 2]
EXPECTED_FRAMES = [
    [711],
    [711],
    [711],
    [711],
    [711, 712],
    [712],
    [712],
    [712],
    [712, 713],
    [713],
    [713],
    [713],
]
EXPECTED_FIRST = [
    "heading_clxi",
    "goat_star",
    "orion_right_shoulder",
    "bull_eye",
    "orion_left_shoulder",
    "rigel_heading",
    "canopus",
    "lion_heart",
    "spica_heading",
    "pleiades_heading",
    "algol_heading",
    "next_clxii",
]


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


class B07rOriginalSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.win = j("ORIGINAL_SOURCE_WINDOW_V1.json")
        cls.writer = j("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.rules = j("RULES.json")
        cls.map = j("SOURCE_TO_RECORD_MAP.json")
        cls.stars = j("FIXED_STARS_1647_CLXI_ORIGINAL_TABLE_V1.json")
        cls.photo = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.accept = j("ACCEPTANCE.json")
        cls.guard = j("HIGH_STAKES_NONPROMOTION_GUARD_V1.json")
        cls.limits = j("UNRESOLVED_SOURCE_LIMITS.json")

    def test_record_sequence(self):
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(11326, 11416))
        )
        self.assertEqual(
            (self.rules["first_record"], self.rules["last_record"]), ("R11326", "R11415")
        )

    def test_chapter_count_and_prior(self):
        self.assertEqual(self.win["accepted_before_clxi"], 11325)
        self.assertEqual(self.accept["new_historical_annotations"], 90)
        self.assertEqual(self.accept["lilly_if_accepted"], 11415)
        self.assertEqual(self.accept["western_if_accepted"], 12481)

    def test_china_independent(self):
        self.assertEqual(self.win["chinese_v2_records"], 97)
        self.assertEqual(self.accept["parallel_chinese"], 97)
        self.assertEqual(self.accept["prior_ptolemy"], 1066)

    def test_source_seam(self):
        self.assertEqual(self.win["chapter_starts_frame"], 711)
        self.assertEqual(self.win["chapter_ends_frame"], 713)
        self.assertEqual(self.win["next_chapter_starts_frame"], 713)
        self.assertEqual(self.writer["following_printed"], "CLXII")
        self.assertEqual(
            [x["role"] for x in self.rules["rules"][-2:]], ["next_clxii", "next_sun_intro"]
        )

    def test_source_exclusion(self):
        self.assertEqual(self.win["body_original_pdf_frames"], [711, 712, 713])
        self.assertEqual(self.writer["body_pdf_frames"], [711, 712, 713])
        for r in self.rules["rules"]:
            self.assertTrue(set(r["original_pdf_frames"]) <= set((711, 712, 713)))

    def test_source_part_counts(self):
        self.assertEqual([len(g["claims"]) for g in self.writer["groups"]], EXPECTED_COUNTS)
        self.assertEqual([g["original_pdf_frames"] for g in self.writer["groups"]], EXPECTED_FRAMES)
        self.assertEqual([g["claims"][0]["role"] for g in self.writer["groups"]], EXPECTED_FIRST)

    def test_source_to_record_inverse(self):
        listed = [r["id"] for r in self.rules["rules"]]
        mapped = [r for group in self.map["source_groups"] for r in group["mapped_record_ids"]]
        original = [r["id"] for group in self.writer["groups"] for r in group["claims"]]
        self.assertEqual(listed, mapped)
        self.assertEqual(listed, original)
        self.assertEqual(len(set(listed)), 90)

    def test_roles_unique(self):
        roles = [r["role"] for r in self.rules["rules"]]
        self.assertEqual(len(roles), len(set(roles)))

    def test_ordered_source_groups(self):
        self.assertEqual(
            [g["source_span"] for g in self.writer["groups"]],
            [f"B07r-S{i:03d}" for i in range(1, 13)],
        )
        self.assertEqual(self.map["source_group_count"], 12)

    def test_source_high_stakes_not_facts(self):
        high = [r for r in self.rules["rules"] if "high-stakes" in r["qualification"]]
        self.assertGreaterEqual(len(high), 12)
        self.assertFalse(
            self.guard["violence_crime_capital_punishment_health_safety_predictions_allowed"]
        )
        self.assertFalse(
            self.guard["class_gender_religion_morality_interpretation_for_actual_people_allowed"]
        )

    def test_all_promotions_false(self):
        for r in self.rules["rules"]:
            for key in (
                "independent_real_event_timing_accuracy_validated",
                "independent_health_or_death_prediction_validated",
                "independent_relationship_or_financial_prediction_validated",
                "independent_faith_personality_or_crime_label_validated",
                "original_directions_angle_date_conversion_verified",
                "original_1647_fixed_star_modern_epoch_parity_verified",
                "real_person_health_safety_social_status_advice_authorized",
                "runtime_model_promoted",
            ):
                self.assertIs(r[key], False)
        self.assertEqual(self.rules["empirical_human_validations"], 0)
        self.assertEqual(self.rules["runtime_promotions"], 0)

    def test_original_coordinate_table(self):
        self.assertEqual(self.stars["entries_count"], 14)
        self.assertEqual([s["source_table_row"] for s in self.stars["entries"]], list(range(1, 15)))
        self.assertEqual(sum(s["historical_degree"] is None for s in self.stars["entries"]), 1)
        self.assertFalse(self.stars["original_1647_precession_parity_verified"])

    def test_star_ambiguities_recorded(self):
        rows = {s["period_star_designation"]: s for s in self.stars["entries"]}
        self.assertIsNone(rows["right shoulder Orion"]["historical_degree"])
        self.assertIsNone(rows["right shoulder Orion"]["historical_minute_if_printed"])
        self.assertIsNone(rows["Arcturus"]["historical_minute_if_printed"])
        self.assertIsNone(rows["Virgins Spike"]["historical_minute_if_printed"])
        self.assertEqual(
            rows["Arcturus"]["historical_degree"], rows["Virgins Spike"]["historical_degree"]
        )
        self.assertEqual(rows["Arcturus"]["source_sign"], rows["Virgins Spike"]["source_sign"])

    def test_star_coordinates_key_cases(self):
        rows = {s["period_star_designation"]: s for s in self.stars["entries"]}
        self.assertEqual(
            (
                rows["Goat"]["historical_degree"],
                rows["Goat"]["historical_minute_if_printed"],
                rows["Goat"]["source_sign"],
            ),
            (16, 33, "Aries"),
        )
        self.assertEqual(
            (
                rows["Pleiades"]["historical_degree"],
                rows["Pleiades"]["historical_minute_if_printed"],
                rows["Pleiades"]["source_sign"],
            ),
            (24, 20, "Taurus"),
        )
        self.assertEqual(
            (rows["head of Algol"]["historical_degree"], rows["head of Algol"]["source_sign"]),
            (20, "Taurus"),
        )

    def test_no_guess_star_names(self):
        for row in self.stars["entries"]:
            self.assertFalse(row["modern_star_identity_validated"])
            self.assertFalse(row["modern_epoch_longitude_validated"])

    def test_star_table_exact_hash(self):
        self.assertEqual(
            sha(B / "FIXED_STARS_1647_CLXI_ORIGINAL_TABLE_V1.json"), self.accept["table_sha256"]
        )

    def test_rule_hash_exact(self):
        self.assertEqual(sha(B / "RULES.json"), self.accept["rules_sha256"])

    def test_photo_hashes(self):
        for n in range(711, 715):
            entry = self.photo["photos"][str(n)]
            self.assertEqual(
                (sha(B / entry["file"]), (B / entry["file"]).stat().st_size),
                (entry["sha256"], entry["bytes"]),
            )

    def test_critical_conditions(self):
        roles = {r["role"] for r in self.rules["rules"]}
        for role in (
            "goat_low_profit",
            "goat_unstable",
            "orion_left_if_wise",
            "rigel_capacity",
            "rigel_overwork",
            "spica_birth",
            "pleiades_radix",
            "algol_benefic",
            "algol_ever_ill",
        ):
            self.assertIn(role, roles)

    def test_no_unverified_calculation(self):
        self.assertTrue(self.limits["right_shoulder_orion_coordinate_missing_here"])
        self.assertFalse(self.guard["original_1647_zodiac_epoch_and_precession_verified"])
        self.assertFalse(self.guard["natal_direction_arc_to_date_calculation_verified"])


def group_check(i, expected, first):
    def test(self):
        group = self.writer["groups"][i]
        self.assertEqual(group["source_span"], f"B07r-S{i + 1:03d}")
        self.assertEqual(len(group["claims"]), expected)
        self.assertEqual(group["claims"][0]["role"], first)
        self.assertEqual(
            [r["id"] for r in group["claims"]], self.map["source_groups"][i]["mapped_record_ids"]
        )

    return test


for i, (length, first) in enumerate(zip(EXPECTED_COUNTS, EXPECTED_FIRST, strict=True)):
    setattr(B07rOriginalSource, f"test_source_group_{i + 1:02d}", group_check(i, length, first))


def single_star_check(i):
    def test(self):
        star = self.stars["entries"][i]
        self.assertEqual(star["source_table_row"], i + 1)
        self.assertIn(star["original_pdf_frame"], [711, 712, 713])
        self.assertIn(star["source_span"], [f"B07r-S{x:03d}" for x in range(1, 13)])
        self.assertTrue(star["source_description_not_person_prediction"])
        if star["historical_degree"] is not None:
            self.assertTrue(0 <= star["historical_degree"] < 30)
            if star["historical_minute_if_printed"] is not None:
                self.assertTrue(0 <= star["historical_minute_if_printed"] < 60)

    return test


for i in range(14):
    setattr(B07rOriginalSource, f"test_period_star_{i + 1:02d}", single_star_check(i))


def photo_check(frame):
    def test(self):
        entry = self.win["photos"][str(frame)]
        self.assertEqual(sha(B / entry["file"]), entry["sha256"])
        self.assertEqual((B / entry["file"]).stat().st_size, entry["bytes"])
        if frame == 714:
            self.assertEqual(entry["chapter_role"], "CLXII_NEXT_SOURCE_CONTEXT_ONLY")

    return test


for frame in range(711, 715):
    setattr(B07rOriginalSource, f"test_original_photo_{frame}", photo_check(frame))


if __name__ == "__main__":
    unittest.main()
