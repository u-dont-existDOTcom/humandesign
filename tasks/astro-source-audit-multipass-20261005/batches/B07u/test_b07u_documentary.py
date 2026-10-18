"""Original 1647 Moon to Promittors documentary tests (no human predictions)."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
COUNTS = [
    3,
    16,
    11,
    14,
    7,
    11,
    8,
    10,
    5,
    19,
    16,
    18,
    6,
    13,
    13,
    16,
    15,
    11,
    13,
    5,
    11,
    11,
    12,
    4,
    5,
    8,
    5,
    2,
    4,
    5,
    3,
    7,
    4,
    5,
    5,
    3,
    5,
    4,
    3,
    5,
    2,
]
FRAMES = [
    [725],
    [725, 726],
    [726],
    [726, 727],
    [727],
    [727],
    [727],
    [727, 728],
    [728],
    [728],
    [728, 729],
    [729],
    [729, 730],
    [730],
    [730],
    [731],
    [731, 732],
    [732],
    [732],
    [732],
    [732, 733],
    [733],
    [733],
    [733],
    [733],
    [734],
    [734],
    [734],
    [734],
    [734],
    [734],
    [734],
    [734],
    [734],
    [734, 735],
    [735],
    [735],
    [735],
    [735],
    [735],
    [735],
]
FIRST = [
    "clxiiii_heading",
    "saturn_body",
    "saturn_benefic",
    "saturn_adverse",
    "saturn_terms",
    "jupiter_body",
    "jupiter_benefic",
    "jupiter_adverse",
    "jupiter_terms",
    "mars_body_direction",
    "mars_benefic_aspect",
    "mars_adverse_aspect",
    "mars_terms_direction",
    "sun_body_direction",
    "sun_benefic_aspect",
    "sun_adverse_aspect",
    "venus_body_direction",
    "venus_benefic_aspect",
    "venus_adverse_aspect",
    "venus_terms_direction",
    "mercury_body_direction",
    "mercury_benefic_aspect",
    "mercury_adverse_aspect",
    "mercury_terms_direction",
    "north_node_direction",
    "south_node_direction",
    "fortune_direction",
    "twelve_house_heading",
    "cusp1_direction",
    "cusp2_direction",
    "cusp3_direction",
    "cusp4_direction",
    "cusp5_direction",
    "cusp6_direction",
    "cusp7_direction",
    "cusp8_direction",
    "cusp9_direction",
    "cusp10_direction",
    "cusp11_direction",
    "cusp12_direction",
    "next_unnumbered_moon_stars",
]
PART_COUNTS = [9, 7, 8, 17]


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class SourceFirst(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.win = j("ORIGINAL_SOURCE_WINDOW_V1.json")
        cls.author = j("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.rules = j("RULES.json")
        cls.mapping = j("SOURCE_TO_RECORD_MAP.json")
        cls.witness = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.accept = j("ACCEPTANCE.json")
        cls.guard = j("HISTORICAL_NONPROMOTION_GUARD_V1.json")
        cls.limits = j("UNRESOLVED_SOURCE_LIMITS.json")

    def test_parent_exact(self):
        self.assertEqual(self.win["accepted_lilly_before"], 11825)
        self.assertEqual(self.win["first_unaccepted_source_record"], "R11826")
        self.assertEqual(self.accept["prior_lilly"], 11825)

    def test_record_count_end(self):
        self.assertEqual(self.rules["record_count"], 343)
        self.assertEqual(self.rules["substantive"], 341)
        self.assertEqual(self.rules["following_navigation"], 2)
        self.assertEqual(self.accept["lilly_if_accepted"], 12168)
        self.assertEqual(self.accept["western_if_accepted"], 13234)
        self.assertEqual(self.accept["next_historical_record"], "R12169")

    def test_all_ids_consecutive(self):
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(11826, 12169))
        )
        self.assertEqual(self.rules["first_record"], "R11826")
        self.assertEqual(self.rules["last_record"], "R12168")

    def test_source_inverse_bijection(self):
        rows = [r["id"] for r in self.rules["rules"]]
        by_source = [r["id"] for g in self.author["groups"] for r in g["claims"]]
        by_map = [rid for g in self.mapping["source_groups"] for rid in g["mapped_record_ids"]]
        self.assertEqual(rows, by_source)
        self.assertEqual(rows, by_map)
        self.assertEqual(len(set(rows)), 343)

    def test_roles_unique(self):
        self.assertEqual(len(set(r["role"] for r in self.rules["rules"])), 343)

    def test_41_passage_expected_counts_pages_and_roles(self):
        self.assertEqual([len(g["claims"]) for g in self.author["groups"]], COUNTS)
        self.assertEqual([g["original_pdf_frames"] for g in self.author["groups"]], FRAMES)
        self.assertEqual([g["claims"][0]["role"] for g in self.author["groups"]], FIRST)

    def test_source_group_count_and_order(self):
        self.assertEqual(self.mapping["source_group_count"], 41)
        self.assertEqual(
            [g["source_span"] for g in self.author["groups"]],
            [f"B07u-S{i:03d}" for i in range(1, 42)],
        )

    def test_original_boundaries(self):
        self.assertEqual(self.win["starts_original_pdf"], 725)
        self.assertEqual(self.win["ends_original_pdf"], 735)
        self.assertEqual(self.win["following_heading_original_pdf"], 735)
        self.assertFalse(self.win["following_heading_numbered"])
        self.assertEqual(self.rules["body_pdf_frames"], list(range(725, 736)))

    def test_no_unnumbered_fixed_stars_leak(self):
        self.assertEqual(self.rules["printed_chapter"], "CLXIIII")
        self.assertEqual(
            [r["role"] for r in self.rules["rules"][-2:]],
            ["next_unnumbered_moon_stars", "next_moon_rigel"],
        )
        for r in self.rules["rules"]:
            self.assertTrue(set(r["original_pdf_frames"]) <= set(range(725, 736)))

    def test_short_anchor_qualification_and_meaning(self):
        for r in self.rules["rules"]:
            self.assertGreaterEqual(len(r["source_anchor_not_diplomatic"]), 5)
            self.assertGreaterEqual(len(r["historical_meaning_only"]), 20)
            self.assertTrue(r["qualification"])

    def test_no_doublecount_chinese_ptolemy(self):
        self.assertEqual(self.win["accepted_chinese_v2"], 97)
        self.assertEqual(self.accept["parallel_chinese_history"], 97)
        self.assertEqual(self.accept["prior_ptolemy"], 1066)

    def test_severe_illness_crime_death_source_only(self):
        high = [r for r in self.rules["rules"] if "high-stakes" in r["qualification"]]
        self.assertGreaterEqual(len(high), 20)
        self.assertTrue(
            self.guard["class_gender_morality_crime_mortality_claims_not_real_person_labels"]
        )
        self.assertTrue(self.guard["old_four_humors_disease_claims_not_modern_diagnoses"])

    def test_all_predictions_and_promotions_false(self):
        for r in self.rules["rules"]:
            for k in (
                "independent_real_event_timing_accuracy_validated",
                "independent_health_or_death_prediction_validated",
                "independent_relationship_or_financial_prediction_validated",
                "independent_faith_personality_or_crime_label_validated",
                "original_directions_angle_date_conversion_verified",
                "original_1647_fixed_star_modern_epoch_parity_verified",
                "real_person_health_safety_social_status_advice_authorized",
                "runtime_model_promoted",
            ):
                self.assertIs(r[k], False)
        self.assertEqual(self.rules["independent_human_outcomes_validated"], 0)
        self.assertEqual(self.rules["runtime_promotions"], 0)
        self.assertEqual(self.guard["individual_human_predictions_validated"], 0)

    def test_planetary_condition_coverage(self):
        roles = {r["role"] for r in self.rules["rules"]}
        for p in ("saturn", "jupiter"):
            for suffix in ("body", "benefic", "adverse", "terms"):
                self.assertIn(f"{p}_{suffix}", roles)
        for p in ("mars", "sun", "venus", "mercury"):
            self.assertIn(f"{p}_body_direction", roles)
            self.assertIn(f"{p}_benefic_aspect", roles)
            self.assertIn(f"{p}_adverse_aspect", roles)

    def test_important_natal_prerequisites(self):
        roles = {r["role"] for r in self.rules["rules"]}
        for role in (
            "mars_body_anareta",
            "mars_body_fixedstars",
            "sun_adverse_depose",
            "sun_adverse_death",
            "venus_adverse_years",
            "cusp4_aph",
            "cusp4_malefic",
            "cusp7_saturn",
            "fortune_both_strength",
        ):
            self.assertIn(role, roles)

    def test_favorable_negative_mixed(self):
        roles = {r["role"] for r in self.rules["rules"]}
        for role in (
            "saturn_benefic_cattle_stock",
            "saturn_body_cattle_loss",
            "jupiter_adverse_friendship_restored",
            "sun_body_trade",
            "sun_body_merchant",
            "venus_benefic_goodwoman",
            "mercury_body_student",
            "mercury_adverse_death",
            "cusp12_good",
        ):
            self.assertIn(role, roles)

    def test_all_twelve_house_cusps(self):
        roles = {r["role"] for r in self.rules["rules"]}
        for i in range(1, 13):
            self.assertIn(f"cusp{i}_direction", roles)

    def test_following_is_unnumbered_not_CLXV(self):
        self.assertTrue(
            self.guard["printed_numbered_chapter_separated_from_unnumbered_star_section"]
        )
        self.assertTrue(self.limits["later_unnumbered_moon_fixed_star_heading_separate"])
        self.assertEqual(self.author["following_unnumbered_heading_pdf"], 735)

    def test_annual_measure_math_still_separate(self):
        self.assertTrue(self.limits["original_annual_measure_table_followup_separate"])
        self.assertFalse(self.limits["full_natal_ephemeris_calendar_or_arctoage_parity"])

    def test_rule_sha_matches_acceptance(self):
        self.assertEqual(sha(B / "RULES.json"), self.accept["rules_sha256"])

    def test_photo_witness_boundary(self):
        self.assertEqual(self.witness["body_original_pdf_frames"], list(range(725, 736)))
        self.assertEqual(list(self.witness["photos"]), [str(i) for i in range(725, 737)])

    def test_unambiguous_body_to_stars_seam(self):
        roles = [r["role"] for r in self.rules["rules"]]
        self.assertIn("cusp12_good", roles[-10:])
        self.assertEqual(roles[-2:], ["next_unnumbered_moon_stars", "next_moon_rigel"])

    def test_four_authoring_parts(self):
        self.assertEqual(len(self.mapping["source_parts"]), 4)
        self.assertEqual(self.author["source_only"], True)
        self.assertEqual(self.author["runtime_promotions"], 0)


def group_check(i, count, frames, first):
    def test(self):
        g = self.author["groups"][i]
        m = self.mapping["source_groups"][i]
        self.assertEqual(g["source_span"], f"B07u-S{i + 1:03d}")
        self.assertEqual(len(g["claims"]), count)
        self.assertEqual(g["original_pdf_frames"], frames)
        self.assertEqual(g["claims"][0]["role"], first)
        self.assertEqual([r["id"] for r in g["claims"]], m["mapped_record_ids"])
        self.assertEqual(g["source_span"], m["source_span"])

    return test


for i, (count, pages, role) in enumerate(zip(COUNTS, FRAMES, FIRST, strict=True)):
    setattr(SourceFirst, f"test_original_passage_{i + 1:03d}", group_check(i, count, pages, role))


def photo_check(n):
    def test(self):
        photo = self.witness["photos"][str(n)]
        raw = (B / photo["file"]).read_bytes()
        self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
        self.assertEqual(len(raw), photo["bytes"])
        self.assertEqual(hashlib.sha256(raw).hexdigest(), photo["sha256"])
        self.assertEqual(photo["original_pdf_frame"], n)

    return test


for n in range(725, 737):
    setattr(SourceFirst, f"test_page_{n}", photo_check(n))


def part_check(i, count):
    def test(self):
        part = j(self.mapping["source_parts"][i])
        self.assertEqual((part["batch"], part["part"]), ("B07u", i + 1))
        self.assertEqual(len(part["groups"]), count)
        self.assertTrue(part["source_only"])
        self.assertEqual(part["independent_human_predictions_validated"], 0)

    return test


for i, count in enumerate(PART_COUNTS):
    setattr(SourceFirst, f"test_original_authoring_part_{i + 1}", part_check(i, count))


if __name__ == "__main__":
    unittest.main()
