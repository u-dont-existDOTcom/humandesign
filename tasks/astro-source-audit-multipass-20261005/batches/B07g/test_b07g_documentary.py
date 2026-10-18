"""Original 1647 Lilly unnumbered twelfth-house source documentary checks."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class OriginalUnnumberedEnemies(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.r = j("RULES.json")
        cls.w = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.m = j("SOURCE_TO_RECORD_MAP.json")
        cls.limits = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.accept = j("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])

    def once(self, *names):
        for n in names:
            self.assertEqual(self.roles[n], 1, n)

    def test_01_original_photo_SHA256_and_bytes(self):
        self.assertEqual(list(self.w["images"]), [str(i) for i in range(673, 677)])
        for photo in self.w["images"].values():
            raw = (B / photo["file"]).read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), photo["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), photo["sha256"])

    def test_02_original_source_body_and_next_printed_frame(self):
        self.assertTrue(self.w["unnumbered"])
        self.assertEqual(self.w["body_original_pdf_frames"], [673, 674])
        self.assertEqual(self.w["following_printed_CLIII_heading_pdf"], 674)
        self.assertFalse(self.w["intervening_original_CLII_heading_present"])
        self.assertEqual(
            [x["printed_folio"] for x in self.w["images"].values()],
            ["639", "640", "641", "642"],
        )

    def test_03_unique_contiguous_23_historical_records(self):
        self.assertEqual([r["record_number"] for r in self.r["rules"]], list(range(10020, 10043)))
        self.assertEqual(len({x["id"] for x in self.r["rules"]}), 23)

    def test_04_three_reversible_photo_group_maps(self):
        ids = []
        for src, dest in zip(self.a["groups"], self.m["source_groups"], strict=True):
            self.assertEqual(src["source_span"], dest["source_span"])
            self.assertEqual(src["original_pdf_frames"], dest["original_pdf_frames"])
            sub = [x["id"] for x in src["claims"]]
            self.assertEqual(sub, dest["mapped_record_ids"])
            ids.extend(sub)
        self.assertEqual(ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(len(self.m["source_groups"]), 3)

    def test_05_first_original_source_enemies_count_not_character(self):
        self.once("heading", "enemies_heading")
        self.assertEqual(self.r["substantive"], 21)

    def test_06_seventh_twelfth_or_opposite_luminaries(self):
        self.once(
            "planets_seventh",
            "planets_twelfth",
            "opposing_lights",
            "many_seventh",
            "many_twelfth",
            "both_lights_opposition",
            "many_adversaries",
        )

    def test_07_empty_houses_negative_few_or_no_enemies(self):
        self.once("no_occupants", "few_or_none")

    def test_08_reciprocal_first_twelfth_seventh_rulers(self):
        self.once(
            "asc_lord_in_twelfth",
            "twelfth_lord_in_first",
            "lord_first_in_seventh",
            "seventh_lord_first",
            "numerous_lord_conditions",
        )

    def test_09_node_analogies_two_different_signifier_sets(self):
        self.once("north_node_analogy", "south_node_analogy")
        self.assertFalse(self.limits["original_node_glyphs_and_rules_fully_verified"])

    def test_10_twelfth_lord_not_aspecting_asc_is_negative_evidence(self):
        self.once("twelfth_lord_no_aspect", "not_many")

    def test_11_original_missing_CLII_no_synthetic_printed_chapter(self):
        self.once("numeral_gap")
        self.assertFalse(self.limits["printed_CLII_heading_observed"])
        self.assertEqual(self.accept["numbered_chapters_added"], 0)
        self.assertEqual(self.accept["next_printed_chapter"], "CLIII")
        self.assertEqual(self.accept["next_original_pdf"], 674)
        self.assertEqual(
            [x["id"] for x in self.r["rules"] if x["role"] == "next_numbered_navigation"],
            ["R10041", "R10042"],
        )

    def test_12_no_actual_person_crime_danger_or_human_accuracy(self):
        self.assertFalse(self.limits["person_level_crime_danger_or_legal_prediction_authorized"])
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for row in self.r["rules"]:
            for key in (
                "independent_real_enemy_count_accuracy_validated",
                "independent_real_relationship_conflict_validated",
                "source_nodal_analogies_mathematically_verified",
                "real_person_enemy_crime_or_danger_inference_authorized",
                "runtime_model_promoted",
            ):
                self.assertFalse(row[key], (row["id"], key))

    def test_13_acceptance_corpus_digest(self):
        self.assertEqual(self.accept["prior_lilly"], 10019)
        self.assertEqual(self.accept["lilly_if_published"], 10042)
        self.assertEqual(self.accept["combined_if_published"], 11108)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.accept["rules_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
