"""Original first-edition unnumbered Moon-star source and photo verification."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V2.json"
COUNTS = [3, 7, 7, 9, 6, 5, 7, 7, 8, 8, 9, 7, 8, 7, 2]
PAGES = [
    [735],
    [735],
    [735],
    [735, 736],
    [736],
    [736],
    [736],
    [736],
    [736],
    [736],
    [736, 737],
    [737],
    [737],
    [737],
    [737],
]
FIRST = [
    "moon_star_heading",
    "rigel_heading",
    "spica_heading",
    "hydra_heading",
    "swan_heading",
    "orion_left_heading",
    "serpent_neck_heading",
    "ophiuchus_heading",
    "bootes_heading",
    "vulture_heading",
    "dragon_eye_heading",
    "serpent_crown_heading",
    "scorpion_heart_heading",
    "hercules_heading",
    "next_clxv_heading",
]


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class MoonStarsDocumentary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.w = load(B / "ORIGINAL_SOURCE_WINDOW_V1.json")
        cls.rules = load(B / "RULES.json")
        cls.src = load(B / "SOURCE_FIRST_AUTHORING_20261018.json")
        cls.map = load(B / "SOURCE_TO_RECORD_MAP.json")
        cls.star = load(B / "FIXED_STARS_1647_UNNUMBERED_MOON_SOURCE_TABLE_V1.json")
        cls.phot = load(B / "ORIGINAL_SOURCE_WITNESS.json")
        cls.acc = load(B / "ACCEPTANCE.json")
        cls.guard = load(B / "HISTORICAL_NONPROMOTION_GUARD_V1.json")
        cls.limits = load(B / "UNRESOLVED_SOURCE_LIMITS.json")
        old = B / "recovery" / "INDEX_BEFORE_B07v.json"
        cls.idx_file = old if old.exists() else INDEX
        cls.idx = load(cls.idx_file)

    def test_exact_prior_index_sha_and_id(self):
        self.assertEqual(sha(self.idx_file), self.w["prior_canonical_index_sha256"])
        self.assertEqual(self.idx["records_count"], 12168)
        self.assertEqual(self.idx["batches"][-1]["id"], "B07u")

    def test_prior_source_next_is_unnumbered(self):
        self.assertEqual(self.idx["next"]["chapter"], "UNNUMBERED_MOON_FIXED_STARRES")
        self.assertIsNone(self.idx["next"]["printed_chapter_numeral"])
        self.assertEqual(self.idx["next"]["pdf_page"], 735)

    def test_record_sequence(self):
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(12169, 12269))
        )
        self.assertEqual(self.rules["last_record"], "R12268")
        self.assertEqual(self.acc["next_record"], "R12269")

    def test_count_and_unnumbered_unit(self):
        self.assertEqual(
            (
                self.rules["record_count"],
                self.rules["substantive"],
                self.rules["following_navigation"],
            ),
            (100, 98, 2),
        )
        self.assertEqual(self.acc["lilly_if_accepted"], 12268)
        self.assertEqual(self.acc["western_if_accepted"], 13334)
        self.assertEqual(self.acc["numbered_chapters_added"], 0)

    def test_source_to_record_inverse(self):
        a = [r["id"] for r in self.rules["rules"]]
        b = [r["id"] for g in self.src["groups"] for r in g["claims"]]
        c = [r for g in self.map["source_groups"] for r in g["mapped_record_ids"]]
        self.assertEqual(a, b)
        self.assertEqual(a, c)
        self.assertEqual(len(set(a)), 100)

    def test_all_15_exact_page_groups(self):
        self.assertEqual([g["original_pdf_frames"] for g in self.src["groups"]], PAGES)
        self.assertEqual([len(g["claims"]) for g in self.src["groups"]], COUNTS)
        self.assertEqual([g["claims"][0]["role"] for g in self.src["groups"]], FIRST)

    def test_unique_roles(self):
        roles = [r["role"] for r in self.rules["rules"]]
        self.assertEqual(len(roles), len(set(roles)))

    def test_historical_anchor_qualification(self):
        for r in self.rules["rules"]:
            self.assertGreaterEqual(len(r["source_anchor_not_diplomatic"]), 5)
            self.assertGreaterEqual(len(r["historical_meaning_only"]), 20)
            self.assertTrue(r["qualification"])

    def test_photo_boundary_and_new_heading(self):
        self.assertEqual(self.w["body_original_pdf_frames"], [735, 736, 737])
        self.assertEqual(self.w["following_printed_numbered_chapter"], "CLXV")
        self.assertEqual(self.w["following_printed_heading_original_pdf"], 737)
        self.assertEqual(self.phot["following_numbered_heading_pdf"], 737)

    def test_no_current_clxv_body_imported(self):
        roles = {r["role"] for r in self.rules["rules"]}
        self.assertIn("next_clxv_heading", roles)
        self.assertNotIn("part_fortune_saturn_body", roles)
        for r in self.rules["rules"]:
            self.assertTrue(set(r["original_pdf_frames"]) <= {735, 736, 737})

    def test_13_historical_star_entries(self):
        self.assertEqual(len(self.star["entries"]), self.star["source_star_entries"])
        self.assertEqual(self.star["source_heading_effects"], 13)
        self.assertEqual([r["source_table_row"] for r in self.star["entries"]], list(range(1, 14)))

    def test_minute_vs_null_precision(self):
        self.assertEqual(sum(r["arcminute_as_printed"] is None for r in self.star["entries"]), 9)
        swan = next(
            r for r in self.star["entries"] if r["period_designation"] == "Tail of the Swan"
        )
        self.assertEqual(
            (
                swan["degree_as_printed"],
                swan["arcminute_as_printed"],
                swan["zodiac_sign_as_printed"],
            ),
            (0, 10, "Pisces"),
        )
        orion = next(
            r for r in self.star["entries"] if r["period_designation"] == "Left Shoulder of Orion"
        )
        self.assertEqual((orion["degree_as_printed"], orion["arcminute_as_printed"]), (15, None))

    def test_original_photo_full_pdf_witness(self):
        self.assertEqual(self.w["original_full_pdf_sha256"], self.phot["full_original_pdf_sha256"])
        self.assertEqual(len(self.phot["photos"]), 4)

    def test_next_divider_not_numbered_this_batch(self):
        self.assertIsNone(self.rules["printed_numbered_chapter"])
        self.assertEqual(self.acc["numbered_chapters_added"], 0)
        self.assertEqual(
            [r["role"] for r in self.rules["rules"][-2:]],
            ["next_clxv_heading", "next_fortune_saturn"],
        )

    def test_parent_ptolemy_china_unmodified(self):
        self.assertEqual(self.acc["prior_ptolemy"], 1066)
        self.assertEqual(self.acc["parallel_chinese"], 97)
        self.assertEqual(load(CHINA)["sum_source_annotations"], 97)

    def test_no_human_predictions_or_model_promotion(self):
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
                self.assertFalse(r[key])
        self.assertFalse(
            self.guard["clinical_mortality_crime_gender_religion_morality_human_inference_allowed"]
        )
        self.assertEqual(self.guard["human_predictions_validated"], 0)
        self.assertEqual(self.guard["runtime_model_promotions"], 0)

    def test_source_context_and_dependency_retained(self):
        roles = {r["role"] for r in self.rules["rules"]}
        for role in (
            "swan_same",
            "hydra_continuation",
            "swan_petulant",
            "vulture_alternative",
            "bootes_inheritance",
            "scorpion_heart_sick",
            "dragon_eye_continued",
        ):
            self.assertIn(role, roles)

    def test_rule_hash_and_star_table_hash(self):
        self.assertEqual(sha(B / "RULES.json"), self.acc["rules_sha256"])
        self.assertEqual(
            sha(B / "FIXED_STARS_1647_UNNUMBERED_MOON_SOURCE_TABLE_V1.json"),
            self.acc["star_table_sha256"],
        )

    def test_no_scientific_parity_claims(self):
        self.assertFalse(self.star["modern_catalog_matching_verified"])
        self.assertFalse(self.star["original_1647_julian_star_epoch_established"])
        self.assertFalse(self.limits["original_star_coordinate_modern_parity_verified"])
        self.assertTrue(self.limits["annual_direction_time_table_a_later_separate_task"])


def group_check(i, count, pages, first):
    def test(self):
        g = self.src["groups"][i]
        m = self.map["source_groups"][i]
        self.assertEqual(g["source_span"], f"B07v-S{i + 1:03d}")
        self.assertEqual(len(g["claims"]), count)
        self.assertEqual(g["original_pdf_frames"], pages)
        self.assertEqual(g["claims"][0]["role"], first)
        self.assertEqual([r["id"] for r in g["claims"]], m["mapped_record_ids"])

    return test


for i, (count, pages, first) in enumerate(zip(COUNTS, PAGES, FIRST, strict=True)):
    setattr(MoonStarsDocumentary, f"test_group_{i + 1:02d}", group_check(i, count, pages, first))


def star_check(i):
    def test(self):
        row = self.star["entries"][i]
        self.assertEqual(row["source_table_row"], i + 1)
        self.assertFalse(row["modern_fixed_star_identity_verified"])
        self.assertFalse(row["epoch_precession_computation_verified"])
        self.assertFalse(row["actual_human_prediction_validated"])
        self.assertIn(row["original_pdf_frame"], (735, 736, 737))

    return test


for i in range(13):
    setattr(MoonStarsDocumentary, f"test_original_star_{i + 1:02d}", star_check(i))


def photo_check(n):
    def test(self):
        p = self.phot["photos"][str(n)]
        raw = (B / p["file"]).read_bytes()
        self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
        self.assertEqual(len(raw), p["bytes"])
        self.assertEqual(sha(B / p["file"]), p["sha256"])

    return test


for n in range(735, 739):
    setattr(MoonStarsDocumentary, f"test_photo_{n}", photo_check(n))


def part_check(i, n):
    def test(self):
        p = load(B / self.map["source_parts"][i])
        self.assertEqual((p["batch"], p["part"]), ("B07v", i + 1))
        self.assertEqual(len(p["groups"]), n)
        self.assertTrue(p["source_only"])

    return test


for i, n in enumerate([6, 9]):
    setattr(MoonStarsDocumentary, f"test_part_{i + 1}", part_check(i, n))


if __name__ == "__main__":
    unittest.main()
