"""Source-photo and inverse-map verification for first-edition Sun fixed-star chapter."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
GROUP_COUNTS = [3, 8, 7, 7, 8, 7, 9, 9, 9, 7, 11, 17, 2]
GROUP_PAGES = [
    [723],
    [723],
    [723],
    [723],
    [723, 724],
    [724],
    [724],
    [724],
    [724],
    [724],
    [724, 725],
    [725],
    [725],
]
GROUP_FIRST = [
    "clxiii_heading",
    "rigel_star",
    "scorpion_star",
    "lesser_dog_star",
    "lion_star",
    "hercules_star",
    "bull_eye_star",
    "cheles_pair",
    "spica_star",
    "bull_south_horn_star",
    "asses_pair",
    "cratch_star",
    "next_clxiiii_heading",
]
PART_GROUPS = [5, 8]


def load(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


class CLXIIISourceFirst(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.win = load("ORIGINAL_SOURCE_WINDOW_V1.json")
        cls.source = load("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.rules = load("RULES.json")
        cls.table = load("FIXED_STARS_1647_CLXIII_ORIGINAL_TABLE_V1.json")
        cls.map = load("SOURCE_TO_RECORD_MAP.json")
        cls.witness = load("ORIGINAL_SOURCE_WITNESS.json")
        cls.accept = load("ACCEPTANCE.json")
        cls.guard = load("HISTORICAL_NONPROMOTION_GUARD_V1.json")
        cls.limits = load("UNRESOLVED_SOURCE_LIMITS.json")

    def test_prior_accepted_boundary(self):
        self.assertEqual(self.win["parent_accepted_lilly"], 11721)
        self.assertEqual(self.win["next_historical_id"], "R11722")
        self.assertEqual(self.accept["prior_lilly"], 11721)

    def test_record_count(self):
        self.assertEqual(self.rules["record_count"], 104)
        self.assertEqual(self.accept["new_historical_annotations"], 104)
        self.assertEqual(self.accept["lilly_if_accepted"], 11825)
        self.assertEqual(self.accept["western_if_accepted"], 12891)

    def test_id_no_duplicates(self):
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]], list(range(11722, 11826))
        )
        self.assertEqual(self.rules["first_record"], "R11722")
        self.assertEqual(self.rules["last_record"], "R11825")
        self.assertEqual(self.accept["next_record"], "R11826")

    def test_104_roles_unique(self):
        roles = [r["role"] for r in self.rules["rules"]]
        self.assertEqual(len(roles), len(set(roles)))

    def test_group_physical_folios(self):
        self.assertEqual([g["original_pdf_frames"] for g in self.source["groups"]], GROUP_PAGES)
        self.assertEqual([len(g["claims"]) for g in self.source["groups"]], GROUP_COUNTS)
        self.assertEqual([g["claims"][0]["role"] for g in self.source["groups"]], GROUP_FIRST)

    def test_source_inverse_bijection(self):
        rules = [r["id"] for r in self.rules["rules"]]
        groups = [x["id"] for g in self.source["groups"] for x in g["claims"]]
        reverse = [x for g in self.map["source_groups"] for x in g["mapped_record_ids"]]
        self.assertEqual(rules, groups)
        self.assertEqual(rules, reverse)
        self.assertEqual(len(set(rules)), 104)

    def test_first_and_last_actual_printed_divider(self):
        self.assertEqual(self.win["first_original_pdf"], 723)
        self.assertEqual(self.win["last_original_pdf"], 725)
        self.assertEqual(self.win["next_chapter"], "CLXIIII")
        self.assertEqual(self.win["next_heading_pdf"], 725)
        self.assertEqual(
            [r["role"] for r in self.rules["rules"][-2:]],
            ["next_clxiiii_heading", "next_moon_saturn"],
        )

    def test_preserves_prior_chapter_exclusion(self):
        roles = {r["role"] for r in self.rules["rules"]}
        self.assertIn("excludes_previous_house", roles)
        self.assertNotIn("cusp_12", roles)
        for r in self.rules["rules"]:
            self.assertTrue(set(r["original_pdf_frames"]) <= {723, 724, 725})

    def test_stellar_count_and_not_invented_samples(self):
        self.assertEqual(self.table["source_distinct_heading_groups"], 11)
        self.assertEqual(self.table["source_distinct_named_stellar_coordinate_entries"], 13)
        self.assertEqual(len(self.table["entries"]), 13)
        self.assertTrue(
            self.guard["printed_star_pairs_separate_from_independent_prediction_samples"]
        )

    def test_declared_pairs_and_unresolved_assignment(self):
        rows = self.table["entries"]
        self.assertEqual(
            [r["degree_as_printed"] for r in rows if "Cheles" in r["source_name"]], [8, 9]
        )
        ass = [r for r in rows if r["source_name"] in ("Northern Ass", "Southern Ass")]
        self.assertEqual(len(ass), 2)
        self.assertTrue(all(r["degree_as_printed"] is None for r in ass))
        self.assertTrue(all(r["degree_options_if_pair_ambiguous"] == [2, 3] for r in ass))

    def test_minutes_null_when_absent(self):
        self.assertEqual(sum(r["minute_as_printed"] is None for r in self.table["entries"]), 12)
        self.assertEqual(sum(r["degree_as_printed"] is None for r in self.table["entries"]), 2)
        south_horn = next(
            e for e in self.table["entries"] if e["source_name"] == "South Bull's Horn"
        )
        self.assertEqual(
            (
                south_horn["degree_as_printed"],
                south_horn["minute_as_printed"],
                south_horn["zodiac_sign_as_printed"],
            ),
            (12, 30, "Gemini"),
        )

    def test_peculiar_crab_in_leo_not_corrected(self):
        cratch = next(e for e in self.table["entries"] if e["source_name"] == "Cratch or Praesepe")
        self.assertEqual(
            (cratch["degree_as_printed"], cratch["zodiac_sign_as_printed"]), (2, "Leo")
        )

    def test_mixed_beneficial_and_negative_examples(self):
        roles = {r["role"] for r in self.rules["rules"]}
        for required in (
            "lion_not_mortal",
            "bull_eye_start",
            "bull_eye_tragic",
            "cheles_martial_benefit",
            "spica_culminating",
            "asses_wisdom",
            "cratch_prudence",
            "cratch_ancients",
            "cratch_observed",
        ):
            self.assertIn(required, roles)

    def test_source_qualification_and_nonquotation(self):
        for r in self.rules["rules"]:
            self.assertGreaterEqual(len(r["source_anchor_not_diplomatic"]), 5)
            self.assertGreaterEqual(len(r["historical_meaning_only"]), 20)
            self.assertTrue(r["qualification"])

    def test_sensitive_source_claims_not_person_forecasts(self):
        threats = [r for r in self.rules["rules"] if "high-stakes" in r["qualification"]]
        self.assertGreaterEqual(len(threats), 17)
        self.assertFalse(
            self.guard[
                "crime_mortality_disease_religion_gender_morality_real_person_predictions_permitted"
            ]
        )

    def test_every_runtime_and_predictive_flag_false(self):
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

    def test_source_stars_all_unmatched_to_modern(self):
        for star in self.table["entries"]:
            self.assertFalse(star["modern_star_identity_verified"])
            self.assertFalse(star["epoch_and_precession_parity_verified"])
            self.assertFalse(star["individual_human_prediction_validated"])

    def test_not_confused_with_china_or_ptolemy(self):
        self.assertEqual(self.win["separate_chinese_v2"], 97)
        self.assertEqual(self.win["parent_ptolemy"], 1066)
        self.assertEqual(self.accept["parallel_chinese_source_notes"], 97)

    def test_original_photo_witness(self):
        self.assertEqual(self.witness["body_original_pdf_frames"], [723, 724, 725])
        self.assertEqual(
            self.witness["full_original_pdf_sha256"], self.win["full_source_894_frame_pdf_sha256"]
        )
        self.assertEqual(list(self.witness["photos"]), ["723", "724", "725"])

    def test_rule_hash_frozen(self):
        self.assertEqual(sha(B / "RULES.json"), self.accept["rules_sha256"])

    def test_star_hash_frozen(self):
        self.assertEqual(
            sha(B / "FIXED_STARS_1647_CLXIII_ORIGINAL_TABLE_V1.json"),
            self.accept["fixed_star_table_sha256"],
        )

    def test_complete_glyph_collation_not_claimed(self):
        self.assertFalse(self.rules["full_original_glyph_collation_completed"])
        self.assertTrue(self.limits["modern_star_names_not_verified"])
        self.assertTrue(
            self.limits["meaning_and_source_commentary_not_expert_independent_reviewed"]
        )


def group_test(i, count, pages, first):
    def test(self):
        group = self.source["groups"][i]
        inverse = self.map["source_groups"][i]
        self.assertEqual(group["source_span"], f"B07t-S{i + 1:03d}")
        self.assertEqual(group["original_pdf_frames"], pages)
        self.assertEqual(len(group["claims"]), count)
        self.assertEqual(group["claims"][0]["role"], first)
        self.assertEqual([r["id"] for r in group["claims"]], inverse["mapped_record_ids"])

    return test


for i, (count, pages, first) in enumerate(zip(GROUP_COUNTS, GROUP_PAGES, GROUP_FIRST, strict=True)):
    setattr(CLXIIISourceFirst, f"test_group_{i + 1:02d}", group_test(i, count, pages, first))


def star_test(i):
    def test(self):
        star = self.table["entries"][i]
        self.assertEqual(star["source_table_row"], i + 1)
        self.assertTrue(star["source_span"].startswith("B07t-S"))
        self.assertIn(star["original_pdf_frame"], (723, 724, 725))
        if star["degree_as_printed"] is not None:
            self.assertTrue(0 <= star["degree_as_printed"] < 30)

    return test


for i in range(13):
    setattr(CLXIIISourceFirst, f"test_star_{i + 1:02d}", star_test(i))


def photo_test(n):
    def test(self):
        photo = self.witness["photos"][str(n)]
        raw = (B / photo["file"]).read_bytes()
        self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
        self.assertEqual(len(raw), photo["bytes"])
        self.assertEqual(hashlib.sha256(raw).hexdigest(), photo["sha256"])
        self.assertGreater(len(raw), 150000)

    return test


for n in (723, 724, 725):
    setattr(CLXIIISourceFirst, f"test_photo_{n}", photo_test(n))


def part_test(i, expected):
    def test(self):
        part = json.loads((B / self.map["source_parts"][i]).read_text(encoding="utf-8"))
        self.assertEqual((part["batch"], part["part"]), ("B07t", i + 1))
        self.assertEqual(len(part["groups"]), expected)
        self.assertTrue(part["source_only"])

    return test


for i, count in enumerate(PART_GROUPS):
    setattr(CLXIIISourceFirst, f"test_source_part_{i + 1}", part_test(i, count))


if __name__ == "__main__":
    unittest.main()
