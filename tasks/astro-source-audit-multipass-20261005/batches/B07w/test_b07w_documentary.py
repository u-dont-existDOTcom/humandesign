"""Original 1647 Part Fortune photo, source-bijection and safety checks."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V2.json"
COUNTS = [
    3,
    8,
    9,
    9,
    7,
    8,
    8,
    8,
    6,
    7,
    8,
    9,
    14,
    12,
    8,
    9,
    3,
    6,
    4,
    6,
    5,
    2,
    2,
    3,
    3,
    3,
    4,
    5,
    3,
    3,
    4,
    4,
    3,
    5,
    3,
]
PAGES = [
    [737],
    [737],
    [737, 738],
    [738],
    [738],
    [738],
    [738],
    [738, 739],
    [739],
    [739],
    [739],
    [739],
    [739, 740],
    [740],
    [740],
    [740],
    [740],
    [740],
    [741],
    [741],
    [741],
    [741],
    [741],
    [741],
    [741],
    [741],
    [741],
    [741],
    [741],
    [741],
    [741],
    [741],
    [741],
    [742],
    [742],
]
FIRST = [
    "clxv_heading",
    "saturn_group",
    "saturn_benefic",
    "jupiter_good_group",
    "jupiter_adverse_group",
    "mars_good_group",
    "mars_bad_group",
    "sun_body",
    "sun_benefic",
    "sun_adverse",
    "venus_good",
    "venus_adverse",
    "mercury_good",
    "mercury_adverse",
    "moon_good",
    "moon_adverse",
    "north_node",
    "south_node",
    "spica_star",
    "lion_star",
    "south_balance_star",
    "houses_heading",
    "cusp1",
    "cusp2",
    "cusp3",
    "cusp4",
    "cusp5",
    "cusp6",
    "cusp7",
    "cusp8",
    "cusp9",
    "cusp10",
    "cusp11",
    "cusp12",
    "next_clxvi",
]
PART_COUNTS = [10, 8, 17]


def load(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class CLXVSourceDocumentary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.win = load("ORIGINAL_SOURCE_WINDOW_V1.json")
        cls.rules = load("RULES.json")
        cls.author = load("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.map = load("SOURCE_TO_RECORD_MAP.json")
        cls.photo = load("ORIGINAL_SOURCE_WITNESS.json")
        cls.acc = load("ACCEPTANCE.json")
        cls.stars = load("FORTUNE_THREE_STAR_HEADINGS_NO_LONGITUDES_V1.json")
        cls.guard = load("HISTORICAL_NONPROMOTION_GUARD_V1.json")
        cls.limits = load("UNRESOLVED_SOURCE_LIMITS.json")
        prev = B / "recovery" / "INDEX_BEFORE_B07w.json"
        cls.pre = prev if prev.exists() else INDEX
        cls.idx = json.loads(cls.pre.read_text(encoding="utf-8"))

    def test_original_index_boundary(self):
        self.assertEqual(self.idx["records_count"], 12268)
        self.assertEqual(self.idx["batches"][-1]["id"], "B07v")
        self.assertEqual(self.idx["next"]["chapter"], "CLXV")
        self.assertEqual(sha(self.pre), self.win["parent_index_sha256"])

    def test_chapter_source_202(self):
        self.assertEqual(self.rules["record_count"], 204)
        self.assertEqual(self.acc["new_historical_annotations"], 204)
        self.assertEqual(self.acc["substantive"], 201)
        self.assertEqual(self.acc["following_navigation"], 3)

    def test_last_and_next_no_overlaps(self):
        self.assertEqual(
            [x["record_number"] for x in self.rules["rules"]], list(range(12269, 12473))
        )
        self.assertEqual(self.rules["last_record"], "R12472")
        self.assertEqual(self.acc["next_id"], "R12473")

    def test_source_groups_are_photo_anchored(self):
        self.assertEqual([len(g["claims"]) for g in self.author["groups"]], COUNTS)
        self.assertEqual([g["original_pdf_frames"] for g in self.author["groups"]], PAGES)
        self.assertEqual([g["claims"][0]["role"] for g in self.author["groups"]], FIRST)

    def test_bidirectional_map(self):
        expected = [x["id"] for x in self.rules["rules"]]
        from_author = [x["id"] for g in self.author["groups"] for x in g["claims"]]
        from_map = [x for g in self.map["source_groups"] for x in g["mapped_record_ids"]]
        self.assertEqual(expected, from_author)
        self.assertEqual(expected, from_map)

    def test_roles_unique_and_qualified(self):
        roles = [r["role"] for r in self.rules["rules"]]
        self.assertEqual(len(roles), len(set(roles)))
        for r in self.rules["rules"]:
            self.assertGreaterEqual(len(r["source_anchor_not_diplomatic"]), 5)
            self.assertGreaterEqual(len(r["historical_meaning_only"]), 15)
            self.assertTrue(r["qualification"])

    def test_only_1647_body(self):
        self.assertEqual(self.win["body_pdf_frames"], list(range(737, 743)))
        self.assertEqual(self.win["following_heading_pdf"], 742)
        self.assertEqual(self.rules["following_printed"], "CLXVI")
        for r in self.rules["rules"]:
            self.assertTrue(set(r["original_pdf_frames"]) <= set(range(737, 743)))

    def test_next_numerical_chapter_separate(self):
        self.assertEqual(
            [r["role"] for r in self.rules["rules"][-3:]],
            ["next_clxvi", "next_age_relevance", "next_ptolemy_methods"],
        )
        self.assertTrue(self.guard["original_direction_numerical_math_verified"] is False)
        self.assertTrue(self.limits["following_CLXVI_is_independent_numerical_method"])

    def test_planet_groups_not_artificially_split(self):
        roles = {r["role"] for r in self.rules["rules"]}
        for key in (
            "saturn_group",
            "jupiter_good_group",
            "jupiter_adverse_group",
            "mars_good_group",
            "mars_bad_group",
            "venus_good",
            "venus_adverse",
            "mercury_good",
            "mercury_adverse",
            "moon_good",
            "moon_adverse",
        ):
            self.assertIn(key, roles)

    def test_lilly_author_counterexamples(self):
        roles = {r["role"] for r in self.rules["rules"]}
        for role in (
            "sun_author_negative",
            "sun_small_saving",
            "jupiter_reduced_gains",
            "venus_generosity",
            "lion_duration",
            "lion_depose",
            "moon_good_sea",
            "mercury_credit",
        ):
            self.assertIn(role, roles)

    def test_three_fixed_star_headings_not_modern(self):
        self.assertEqual(self.stars["historical_headings"], 3)
        self.assertEqual(len(self.stars["entries"]), 3)
        for row in self.stars["entries"]:
            self.assertIsNone(row["original_printed_longitude_degree"])
            self.assertIsNone(row["original_printed_longitude_minute"])
            self.assertIsNone(row["original_printed_sign"])
            self.assertFalse(row["star_catalog_id_validated"])

    def test_twelve_house_cells_and_animal_twelve(self):
        roles = {r["role"] for r in self.rules["rules"]}
        for i in range(1, 13):
            self.assertIn(f"cusp{i}", roles)
        self.assertIn("cusp12_races", roles)

    def test_ptolemy_chinese_not_conflated(self):
        self.assertEqual(self.acc["prior_ptolemy"], 1066)
        self.assertEqual(self.acc["parallel_chinese"], 97)
        self.assertEqual(self.acc["western_if_accepted"], 13538)
        self.assertEqual(json.loads(CHINA.read_text())["sum_source_annotations"], 97)

    def test_no_human_outcome_from_document(self):
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
        self.assertFalse(self.guard["independent_real_person_predictive_accuracy_validated"])
        self.assertFalse(
            self.guard["real_person_crime_sex_gender_class_health_safety_money_inference_permitted"]
        )

    def test_photo_witness(self):
        self.assertEqual(self.photo["body_pdf_frames"], list(range(737, 743)))
        self.assertEqual(list(self.photo["photos"]), [str(x) for x in range(737, 744)])
        self.assertEqual(
            self.photo["full_original_pdf_sha256"], self.win["full_pdf_original_sha256"]
        )

    def test_rule_and_star_hash(self):
        self.assertEqual(sha(B / "RULES.json"), self.acc["rules_sha256"])
        self.assertEqual(
            sha(B / "FORTUNE_THREE_STAR_HEADINGS_NO_LONGITUDES_V1.json"),
            self.acc["star_table_sha256"],
        )

    def test_no_human_or_runtime_promotion(self):
        self.assertEqual(self.rules["empirical_human_validations"], 0)
        self.assertEqual(self.rules["runtime_promotions"], 0)
        self.assertEqual(self.acc["human_predictions_validated"], 0)
        self.assertEqual(self.acc["runtime_promotions"], 0)


def group_case(i, n, pg, first):
    def test(self):
        g = self.author["groups"][i]
        row = self.map["source_groups"][i]
        self.assertEqual(g["source_span"], f"B07w-S{i + 1:03d}")
        self.assertEqual(g["original_pdf_frames"], pg)
        self.assertEqual(g["claims"][0]["role"], first)
        self.assertEqual(len(g["claims"]), n)
        self.assertEqual(row["mapped_record_ids"], [x["id"] for x in g["claims"]])

    return test


for i, (n, pg, first) in enumerate(zip(COUNTS, PAGES, FIRST, strict=True)):
    setattr(CLXVSourceDocumentary, f"test_group_{i + 1:02d}", group_case(i, n, pg, first))


def photo_case(page):
    def test(self):
        w = self.photo["photos"][str(page)]
        file = B / w["file"]
        raw = file.read_bytes()
        self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
        self.assertEqual(len(raw), w["bytes"])
        self.assertEqual(sha(file), w["sha256"])

    return test


for page in range(737, 744):
    setattr(CLXVSourceDocumentary, f"test_photo_{page}", photo_case(page))


def part_case(i, n):
    def test(self):
        d = load(self.map["source_parts"][i])
        self.assertEqual(d["part"], i + 1)
        self.assertEqual(len(d["groups"]), n)
        self.assertTrue(d["source_only"])

    return test


for i, n in enumerate(PART_COUNTS):
    setattr(CLXVSourceDocumentary, f"test_part_{i + 1}", part_case(i, n))


if __name__ == "__main__":
    unittest.main()
