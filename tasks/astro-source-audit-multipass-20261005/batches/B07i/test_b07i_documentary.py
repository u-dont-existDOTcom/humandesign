"""Original Lilly 1647 CLIIII documentary integrity and unverified high-stakes warning."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class OriginalConflictOutcomeSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.r = j("RULES.json")
        cls.w = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.mapping = j("SOURCE_TO_RECORD_MAP.json")
        cls.limits = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.acc = j("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])

    def one(self, *roles):
        for role in roles:
            self.assertEqual(self.roles[role], 1, role)

    def test_01_source_photo_SHA_byte_and_folio(self):
        self.assertEqual(list(self.w["images"]), ["675", "676", "677"])
        for x in self.w["images"].values():
            raw = (B / x["file"]).read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), x["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), x["sha256"])
        self.assertEqual(
            [x["printed_folio"] for x in self.w["images"].values()],
            ["641", "642", "643"],
        )

    def test_02_original_CLI_equivalence_and_next_CLV(self):
        self.assertEqual(self.a["printed_chapter"], "CLIIII")
        self.assertEqual(self.w["body_pdf_frames"], [675, 676])
        self.assertEqual(self.w["following_printed_CLV_heading_frame"], 676)

    def test_03_64_unique_contiguous_original_source_records(self):
        self.assertEqual(
            [x["record_number"] for x in self.r["rules"]],
            list(range(10083, 10147)),
        )
        self.assertEqual(len({x["id"] for x in self.r["rules"]}), 64)

    def test_04_six_source_groups_reversible(self):
        ids = []
        for src, m in zip(self.a["groups"], self.mapping["source_groups"], strict=True):
            self.assertEqual(src["source_span"], m["source_span"])
            self.assertEqual(src["original_pdf_frames"], m["original_pdf_frames"])
            row_ids = [x["id"] for x in src["claims"]]
            self.assertEqual(m["mapped_record_ids"], row_ids)
            ids.extend(row_ids)
        self.assertEqual(ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(len(self.mapping["source_groups"]), 6)

    def test_05_seventh_tenth_reciprocal_lord_sources(self):
        self.one("seventh_lord_tenth", "tenth_lord_seventh", "overcome_seventh_tenth")

    def test_06_twelfth_tenth_reciprocal_lord_sources(self):
        self.one("twelfth_lord_tenth", "tenth_lord_twelfth", "overcome_twelfth_tenth")

    def test_07_twelfth_lord_retrograde_fall_or_detriment_and_sixth(self):
        self.one(
            "twelfth_lord_retro",
            "twelfth_lord_fall",
            "twelfth_lord_detriment",
            "twelfth_lord_sixth",
            "overcome_weak_twelfth",
        )

    def test_08_luminary_time_sun_vs_moon_and_eighth_exclusion(self):
        self.one("luminaries", "diurnal_sun", "nocturnal_moon", "not_eighth")

    def test_09_mars_dignity_or_reception_and_mars_near_light(self):
        self.one(
            "light_mars_dignity",
            "reciprocal_reception",
            "manifest_victory",
            "mars_stronger",
            "mars_conjunction_light",
            "mars_near_light",
            "mars_victory",
        )

    def test_10_saturn_AND_mars_strong_twelfth_fatal_allegation(self):
        self.one("saturn_twelfth", "mars_twelfth", "both_potent", "enemies_die")

    def test_11_saturn_and_mars_debility_reverse_and_injury(self):
        self.one("both_debilitated", "contrary_outcome", "member_debility")

    def test_12_sixth_and_twelfth_malefics_three_outcomes(self):
        self.one(
            "one_malefic_twelfth",
            "other_malefic_sixth",
            "risk_killed_by_enemies",
            "alternative_perpetual_sickness",
            "alternative_imprisonment",
        )

    def test_13_jupiter_or_venus_twelfth_claim_no_harm(self):
        self.one("jupiter_lord_twelfth", "venus_lord_twelfth", "no_harm", "evades")

    def test_14_three_ascending_signs_conflict_allegations(self):
        self.one("gemini_ascendant", "sagittarius_ascendant", "aquarius_ascendant", "stir_enemies")

    def test_15_horse_fall_fatal_qualified_twelfth(self):
        self.one(
            "leo_twelfth",
            "sagittarius_twelfth",
            "malefic_twelfth",
            "horse_fall",
            "horse_fall_fatal",
        )

    def test_16_source_avoid_friendship_heading_not_actual_advice(self):
        self.one(
            "avoid_heading",
            "friend_lord_malefic",
            "south_node_friend",
            "ill_fixed_star",
            "nativities_disagree",
            "source_warn_avoid",
            "offend_without_mind",
        )

    def test_17_directional_cross_chart_negative_aspect(self):
        self.one(
            "one_light_bad_aspect_other",
            "square_other",
            "opposition_other",
            "perpetual_enemies",
            "more_victory_signifiers",
            "one_person_prevails",
        )

    def test_18_next_printed_CLV_is_separate_captivity_source(self):
        self.assertEqual(
            [x["id"] for x in self.r["rules"] if x["role"] == "next_navigation"],
            ["R10145", "R10146"],
        )
        self.assertEqual(self.acc["next_printed"], "CLV")
        self.assertEqual(self.acc["next_original_pdf"], 676)

    def test_19_zero_real_safety_mortality_crime_prognosis(self):
        self.assertFalse(self.limits["actual_person_risk_or_moral_inference_authorized"])
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for row in self.r["rules"]:
            for f in (
                "independently_validated_real_adversary_victory",
                "independently_validated_injury_mortality_or_illness",
                "independently_validated_imprisonment_or_horse_fall",
                "independently_validated_relationship_danger",
                "real_person_adversary_or_friend_risk_advice_authorized",
                "runtime_model_promoted",
            ):
                self.assertFalse(row[f], (row["id"], f))

    def test_20_archival_acceptance_and_rule_checksum(self):
        self.assertEqual(self.acc["prior_lilly"], 10082)
        self.assertEqual(self.acc["new_historical_annotations"], 64)
        self.assertEqual(self.acc["lilly_if_published"], 10146)
        self.assertEqual(self.acc["combined_if_published"], 11212)
        self.assertEqual(self.acc["numbered_chapters_added"], 1)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.acc["rules_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
