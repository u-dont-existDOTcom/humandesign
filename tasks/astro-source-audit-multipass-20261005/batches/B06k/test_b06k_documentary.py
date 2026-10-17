"""Lilly CXXXIII 1647 spouse-origin source integrity, not human location prediction."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text())


class HistoricSpouseOrigin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = read("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = read("RULES.json")
        cls.m = read("SOURCE_TO_RECORD_MAP.json")
        cls.w = read("ORIGINAL_SOURCE_WITNESS.json")
        cls.l = read("UNRESOLVED_SOURCE_LIMITS.json")
        cls.acc = read("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])
        cls.text = " ".join(x["anchor_not_diplomatic"] for x in cls.r["rules"])

    def test_01_original_photo_sha_bytes(self):
        self.assertEqual(list(self.w["images"]), ["626", "627"])
        for x in self.w["images"].values():
            p = B / x["file"]
            raw = p.read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), x["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), x["sha256"])

    def test_02_printed_folio_and_new_chapter(self):
        self.assertEqual(
            [x["printed_folio"] for x in self.w["images"].values()],
            ["592", "593"],
        )
        self.assertEqual(self.w["body_original_frames"], [626, 627])
        self.assertEqual(self.w["following_printed_CXXXIIII_heading_frame"], 627)

    def test_03_append_only_exact_ids(self):
        self.assertEqual(
            [r["record_number"] for r in self.r["rules"]],
            list(range(8107, 8142)),
        )
        self.assertEqual(len({r["id"] for r in self.r["rules"]}), 35)

    def test_04_all_six_source_passages_reversible(self):
        ids = []
        for a, m in zip(self.a["groups"], self.m["source_groups"], strict=True):
            self.assertEqual(a["source_span"], m["source_span"])
            self.assertEqual(a["original_pdf_frames"], m["original_pdf_frames"])
            these = [x["id"] for x in a["claims"]]
            self.assertEqual(these, m["mapped_record_ids"])
            ids.extend(these)
        self.assertEqual(ids, [r["id"] for r in self.r["rules"]])
        self.assertEqual(len(self.m["source_groups"]), 6)

    def test_05_ninth_third_house_and_peregrine_separate(self):
        for role in (
            "foreign_house_ninth",
            "foreign_house_third",
            "foreign_peregrine",
            "no_dignities",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_06_county_not_country_original_exact_distinction(self):
        self.assertEqual(self.roles["not_same_county"], 1)
        self.assertEqual(self.roles["not_country_explicit"], 1)
        self.assertEqual(self.roles["other_country_birth"], 1)
        self.assertIn("I say not Country", self.text)
        self.assertTrue(self.l["county_vs_country_ambiguity_preserved"])

    def test_07_seventh_ninth_rulers_mutual_alternatives(self):
        self.assertEqual(self.roles["seventh_lord_ninth"], 1)
        self.assertEqual(self.roles["ninth_lord_seventh"], 1)
        self.assertEqual(self.roles["far_from_birthplace"], 1)

    def test_08_spouse_character_rich_and_virtuous_are_unverified(self):
        for role in (
            "spouse_religious",
            "spouse_rich",
            "spouse_virtuous",
            "benefic_modifier",
            "fortified_modifier",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_09_venus_must_rule_ninth_then_first_or_tenth(self):
        self.assertEqual(self.roles["venus_lady_ninth"], 1)
        self.assertEqual(self.roles["venus_first"], 1)
        self.assertEqual(self.roles["venus_tenth"], 1)

    def test_10_sun_plus_uncertain_glyph_never_encoded(self):
        self.assertEqual(self.roles["sun_companion"], 1)
        row = next(x for x in self.r["rules"] if x["role"] == "sun_companion")
        self.assertEqual(row["source_qualification"], "glyph-unresolved")
        self.assertFalse(self.l["source_glyph_fully_resolved"])

    def test_11_sun_third_distinct_from_seventh_contact(self):
        self.assertEqual(self.roles["seventh_contact"], 1)
        self.assertEqual(self.roles["sun_third"], 1)
        self.assertEqual(self.roles["not_native_place"], 1)

    def test_12_multiple_sign_and_quarter_witnesses_not_distance(self):
        for role in (
            "sign_seventh",
            "sign_of_seventh_lord",
            "venus_sign",
            "moon_sign",
            "quarters_of_heaven",
            "majority",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_13_personal_spouse_origin_wealth_morality_not_validated(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["independent_spouse_geography_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        self.assertFalse(self.l["private_partner_character_or_origin_claims_authorized"])
        for x in self.r["rules"]:
            self.assertFalse(x["independent_spouse_birthplace_validated"])
            self.assertFalse(x["actual_spouse_character_religion_or_wealth_validated"])
            self.assertFalse(x["independent_geographical_distance_validated"])
            self.assertFalse(x["real_person_spouse_origin_prediction_authorized"])
            self.assertFalse(x["runtime_model_promoted"])

    def test_14_following_spouse_appearance_chapter_separate(self):
        self.assertEqual(
            [x["id"] for x in self.r["rules"] if x["role"] == "next_chapter_navigation"],
            ["R8140", "R8141"],
        )
        self.assertEqual(self.acc["next_printed_chapter"], "CXXXIIII")
        self.assertEqual(self.r["substantive_historical"], 33)

    def test_15_accepted_number_and_rules_hash(self):
        self.assertEqual(self.acc["prior_lilly"], 8106)
        self.assertEqual(self.acc["lilly_if_published"], 8141)
        self.assertEqual(self.acc["combined_if_published"], 9207)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.acc["rules_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
