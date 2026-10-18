"""Unambiguous, portable CLXII original photographic source record replay."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
COUNTS = [
    4,
    14,
    9,
    13,
    7,
    10,
    10,
    10,
    7,
    15,
    10,
    11,
    5,
    11,
    10,
    7,
    9,
    11,
    8,
    8,
    5,
    12,
    8,
    10,
    6,
    7,
    4,
    5,
    4,
    3,
    9,
    6,
    5,
    5,
    5,
    7,
    5,
    4,
    5,
    2,
]
FRAMES = [
    [713],
    [713, 714],
    [714],
    [714, 715],
    [715],
    [715],
    [715, 716],
    [715, 716],
    [716],
    [716],
    [716, 717],
    [717],
    [717],
    [717, 718],
    [718],
    [718],
    [718, 719],
    [719],
    [719],
    [719, 720],
    [720],
    [720],
    [720],
    [720, 721],
    [721],
    [721],
    [721],
    [721],
    [721],
    [721],
    [722],
    [722],
    [722],
    [722],
    [722],
    [722],
    [722, 723],
    [723],
    [723],
    [723],
]
FIRST = [
    "chapter_clxii",
    "saturn_body",
    "saturn_benefic",
    "saturn_adverse",
    "saturn_terms",
    "jupiter_body",
    "jupiter_benefic",
    "jupiter_adverse",
    "jupiter_terms",
    "mars_body",
    "mars_benefic",
    "mars_adverse",
    "mars_terms",
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
    "north_node",
    "south_node",
    "fortune",
    "cusp_1",
    "cusp_2",
    "cusp_3",
    "cusp_4",
    "cusp_5",
    "cusp_6",
    "cusp_7",
    "cusp_8",
    "cusp_9",
    "cusp_10",
    "cusp_11",
    "cusp_12",
    "next_clxiii",
]
PART_GROUPS = [7, 6, 8, 6, 13]


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


class OriginalSolarDocumentary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.win = j("ORIGINAL_SOURCE_WINDOW_V1.json")
        cls.source = j("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.rules = j("RULES.json")
        cls.inv = j("SOURCE_TO_RECORD_MAP.json")
        cls.witness = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.accept = j("ACCEPTANCE.json")
        cls.guard = j("SUN_DIRECTION_HISTORICAL_NONPROMOTION_GUARD_V1.json")
        cls.limits = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.repair = j("PRE_FREEZE_ROLE_REPAIR_RECEIPT_V1.json")

    def test_photo_source_authentic(self):
        self.assertEqual(self.witness["full_original_pdf_sha256"], self.win["original_pdf_sha256"])
        self.assertEqual(self.witness["full_original_pdf_bytes"], 141842963)

    def test_exact_counts(self):
        self.assertEqual(self.rules["record_count"], 306)
        self.assertEqual(self.rules["substantive"], 304)
        self.assertEqual(self.rules["following_navigation"], 2)
        self.assertEqual(self.inv["source_group_count"], 40)

    def test_prior_source_id(self):
        self.assertEqual(self.win["new_source_record_starts"], "R11416")
        self.assertEqual(self.accept["prior_lilly"], 11415)
        self.assertEqual(self.accept["new_historical_annotations"], 306)

    def test_consecutive_record_numbers(self):
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(11416, 11722))
        )
        self.assertEqual(self.rules["last_record"], "R11721")
        self.assertEqual(self.accept["next_record"], "R11722")

    def test_no_conflated_chinese_or_ptolemy(self):
        self.assertEqual(self.win["independent_chinese_v2_count"], 97)
        self.assertEqual(self.accept["parallel_chinese_source_notes"], 97)
        self.assertEqual(self.accept["prior_ptolemy"], 1066)
        self.assertEqual(self.accept["western_if_accepted"], 12787)

    def test_source_records_inverse_bijection(self):
        rows = [r["id"] for r in self.rules["rules"]]
        from_source = [r["id"] for g in self.source["groups"] for r in g["claims"]]
        from_inverse = [rid for g in self.inv["source_groups"] for rid in g["mapped_record_ids"]]
        self.assertEqual(rows, from_source)
        self.assertEqual(rows, from_inverse)
        self.assertEqual(len(set(rows)), 306)

    def test_unique_historical_roles(self):
        roles = [r["role"] for r in self.rules["rules"]]
        self.assertEqual(len(set(roles)), 306)
        self.assertTrue(self.repair["after_unique"])
        self.assertEqual(self.repair["repaired_roles"], 17)

    def test_semantic_qualifications(self):
        for r in self.rules["rules"]:
            self.assertGreaterEqual(len(r["source_anchor_not_diplomatic"]), 5)
            self.assertGreaterEqual(len(r["historical_meaning_only"]), 18)
            self.assertTrue(r["qualification"])

    def test_all_40_groups_manual_photo_bounds(self):
        self.assertEqual([len(g["claims"]) for g in self.source["groups"]], COUNTS)
        self.assertEqual([g["original_pdf_frames"] for g in self.source["groups"]], FRAMES)
        self.assertEqual([g["claims"][0]["role"] for g in self.source["groups"]], FIRST)

    def test_only_original_clxii_body_or_navigation(self):
        for r in self.rules["rules"]:
            self.assertTrue(set(r["original_pdf_frames"]) <= set(range(713, 724)))
        self.assertEqual(self.rules["body_pdf_frames"], list(range(713, 724)))
        self.assertEqual(self.rules["following_heading_original_pdf"], 723)

    def test_verified_neighbor_chapter_divider(self):
        self.assertEqual(self.win["printed_clxii"]["starts_frame"], 713)
        self.assertEqual(self.win["printed_clxii"]["ends_frame"], 723)
        self.assertEqual(self.win["following_printed_clxiii"]["starts_frame"], 723)
        self.assertEqual(
            [r["role"] for r in self.rules["rules"][-2:]], ["next_clxiii", "next_rigel"]
        )

    def test_every_planet_has_body_benefic_adverse(self):
        roles = {r["role"] for r in self.rules["rules"]}
        for planet in ("saturn", "jupiter", "mars", "venus", "mercury", "moon"):
            for key in ("body", "benefic", "adverse"):
                self.assertIn(f"{planet}_{key}", roles)

    def test_planetary_terms_where_printed(self):
        roles = {r["role"] for r in self.rules["rules"]}
        for planet in ("saturn", "jupiter", "mars", "venus", "mercury"):
            self.assertIn(f"{planet}_terms", roles)

    def test_nodes_partfortune_present(self):
        roles = {r["role"] for r in self.rules["rules"]}
        for role in ("north_node", "south_node", "fortune"):
            self.assertIn(role, roles)

    def test_twelve_house_cusps(self):
        roles = {r["role"] for r in self.rules["rules"]}
        for n in range(1, 13):
            self.assertIn(f"cusp_{n}", roles)

    def test_venus_mercury_impossible_aspect_exception(self):
        roles = {r["role"] for r in self.rules["rules"]}
        for role in (
            "venus_sun_elong",
            "venus_square_not_opposition",
            "venus_80",
            "mercury_opp_refusal",
            "mercury_century",
        ):
            self.assertIn(role, roles)
        self.assertTrue(self.guard["source_venus_opposition_reinterpreted_as_square"])
        self.assertTrue(self.guard["original_sun_mercury_opposition_doubted_by_lilly"])

    def test_extreme_claims_quarantined(self):
        high = [r for r in self.rules["rules"] if "high-stakes" in r["qualification"]]
        self.assertGreaterEqual(len(high), 25)
        self.assertFalse(
            self.guard["clinical_mortality_injury_crime_moral_gender_social_rank_claims_authorized"]
        )
        self.assertFalse(self.guard["natal_forecasting_at_the_person_level_authorized"])

    def test_complex_natal_provisos_preserved(self):
        roles = {r["role"] for r in self.rules["rules"]}
        for role in (
            "mars_violent_prior",
            "mars_anareta",
            "jupiter_radix",
            "venus_radix_wife",
            "venus_profection",
            "venus_revolution",
            "south_other_ill",
            "cusp9_malefic",
            "cusp10_unfortunate",
        ):
            self.assertIn(role, roles)
        self.assertFalse(self.guard["exact_lilly_hyleg_anareta_and_climacteric_year_verified"])

    def test_all_predictions_and_models_unverified(self):
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
        self.assertFalse(self.guard["predictive_method_scientifically_validated"])

    def test_source_parts_safe(self):
        self.assertEqual(len(self.inv["source_parts"]), 5)
        self.assertEqual(self.source["printed_chapter"], "CLXII")
        self.assertEqual(self.source["individual_human_predictions_validated"], 0)

    def test_witness_exact_image_set(self):
        self.assertEqual(self.witness["body_original_pdf_frames"], list(range(713, 724)))
        self.assertEqual(list(self.witness["photos"]), [str(i) for i in range(713, 726)])

    def test_rule_hash_attested(self):
        self.assertEqual(sha(B / "RULES.json"), self.accept["rules_sha256"])

    def test_no_western_model_promotions(self):
        self.assertEqual(self.guard["independent_human_outcomes_validated"], 0)
        self.assertEqual(self.guard["runtime_rules_promoted"], 0)
        self.assertTrue(self.limits["no_real_person_health_safety_legal_interpretation_permitted"])


def group_check(i, expected, frames, first):
    def test(self):
        group = self.source["groups"][i]
        mapping = self.inv["source_groups"][i]
        self.assertEqual(group["source_span"], f"B07s-S{i + 1:03d}")
        self.assertEqual(group["original_pdf_frames"], frames)
        self.assertEqual(group["claims"][0]["role"], first)
        self.assertEqual(len(group["claims"]), expected)
        self.assertEqual([c["id"] for c in group["claims"]], mapping["mapped_record_ids"])
        self.assertEqual(mapping["source_span"], group["source_span"])

    return test


for i, (count, frame, role) in enumerate(zip(COUNTS, FRAMES, FIRST, strict=True)):
    setattr(
        OriginalSolarDocumentary, f"test_passage_{i + 1:03d}", group_check(i, count, frame, role)
    )


def image_check(n):
    def test(self):
        image = self.witness["photos"][str(n)]
        raw = (B / image["file"]).read_bytes()
        self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
        self.assertEqual(len(raw), image["bytes"])
        self.assertEqual(hashlib.sha256(raw).hexdigest(), image["sha256"])
        self.assertEqual(image["original_pdf_frame"], n)

    return test


for n in range(713, 726):
    setattr(OriginalSolarDocumentary, f"test_photo_{n}", image_check(n))


def part_check(i, expected):
    def test(self):
        part = j(self.inv["source_parts"][i])
        self.assertEqual(part["batch"], "B07s")
        self.assertEqual(part["part"], i + 1)
        self.assertEqual(len(part["groups"]), expected)
        self.assertTrue(part["source_only"])
        self.assertEqual(part["human_predictive_validations"], 0)

    return test


for i, count in enumerate(PART_GROUPS):
    setattr(OriginalSolarDocumentary, f"test_source_part_{i + 1}", part_check(i, count))


if __name__ == "__main__":
    unittest.main()
