"""Lilly 1647 and 1659 original merchant-friends photographic/source verification."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class OriginalMerchantFriendsSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = read("SOURCE_FIRST_AUTHORING_20261021.json")
        cls.w = read("ORIGINAL_SOURCE_WITNESS_20261021.json")
        cls.m = read("SOURCE_TO_RECORD_MAP.json")
        cls.rules = read("RULES.json")
        cls.limits = read("UNRESOLVED_SOURCE_LIMITS.json")
        cls.accept = read("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.rules["rules"])

    def once(self, *roles):
        for role in roles:
            self.assertEqual(self.roles[role], 1, role)

    def test_01_exact_original_image_sha_and_bytes(self):
        self.assertEqual(len(self.w["photos"]), 5)
        for photo in self.w["photos"].values():
            path = B / photo["path"]
            raw = path.read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertGreater(len(raw), 150000)
            self.assertEqual(len(raw), photo["bytes"])
            self.assertEqual(sha(path), photo["sha256"])

    def test_02_both_editions_762_and_763_distinct_photos(self):
        x = self.w["photos"]
        for f in (762, 763):
            first = x[f"1647-original-folio{f}-IIIF.jpg"]
            second = x[f"1659-original-folio{f}-DjVu.jpg"]
            self.assertNotEqual(first["sha256"], second["sha256"])
            self.assertEqual(first["printed_folio"], second["printed_folio"])
            self.assertEqual(first["edition"], "first_1647")
            self.assertEqual(second["edition"], "second_1659")
        self.assertFalse(self.w["second_1659_whole_original_file_sha256_authenticated"])

    def test_03_exact_new_35_nonduplicated_records(self):
        self.assertEqual(
            [x["record_number"] for x in self.rules["rules"]],
            list(range(13237, 13272)),
        )
        self.assertEqual(len({x["id"] for x in self.rules["rules"]}), 35)

    def test_04_source_to_record_inverse_six_groups(self):
        ids = []
        for group, rev in zip(self.a["source_groups"], self.m["source_groups"], strict=True):
            self.assertEqual(group["id"], rev["source_span"])
            self.assertEqual(group["original_printed_folio"], rev["original_printed_folio"])
            a_ids = [x["id"] for x in group["clauses"]]
            self.assertEqual(a_ids, rev["source_record_ids"])
            ids.extend(a_ids)
        self.assertEqual(ids, [x["id"] for x in self.rules["rules"]])
        self.assertEqual(self.m["source_group_count"], 6)

    def test_05_heading_printed_regression_preserved(self):
        self.assertEqual(self.a["previous_honours_heading_printed_literal"], "CLXXXIIII")
        self.assertEqual(self.a["source_heading_printed_literal"], "CLXXXIII")
        self.assertEqual(self.a["editorial_source_ordinal"], 185)
        self.once("ELEVENTH_HOUSE_START", "FRIENDS_PRINTED_CLXXXIII", "FRIENDS_HEADING")

    def test_06_sagittarius_cusp_is_source_claim_not_measured(self):
        self.once("SAGITTARIUS_BICORPOREAL", "MOON_OPPOSITE_ELEVENTH")
        self.assertFalse(self.limits["source_mercury_peregrine_combust_independent_astro_verified"])

    def test_07_moon_ruler_seventh_partner_money_is_distinct(self):
        self.once("MOON_LADY_SEVENTH", "PARTNER_TRADE_HARM")
        self.assertFalse(
            self.a["independent_real_merchant_friendship_or_business_records_obtained"]
        )

    def test_08_moon_people_exclusions_are_historical_stereotype(self):
        self.once(
            "SAILOR_FRIEND_EXCLUSION",
            "VULGAR_FRIEND_EXCLUSION",
            "MOON_PEOPLE_NOT_ADMITTED",
            "MOON_TYPES_CROSSREF",
        )

    def test_09_jupiter_and_sagittarius_positive_branch(self):
        self.once(
            "ELEVENTH_SIGN_OWN", "JUPITER_SAGITTARIUS", "JOVIAL_FRIENDS", "SUITABLE_ASSOCIATES"
        )

    def test_10_venus_people_venetians_text_not_nationality(self):
        self.once("VENUSIAN_FRIENDS")
        self.assertFalse(self.limits["fully_disambiguated_old_venus_term_Venetians"])

    def test_11_mercury_negative_needs_peregrine_and_combust(self):
        self.once("MERCURIAN_REJECTED", "MERCURY_PEREGRINE", "MERCURY_COMBUST")

    def test_12_mars_trine_11th_and_mars_leo_explicit(self):
        self.once("MARS_TRINE_ELEVENTH", "MARS_LEO_SOURCE", "MARS_SIGN_CROSSREF")

    def test_13_mars_military_and_political_friends_alternatives(self):
        self.once("MARS_COMMANDERS", "MARS_TOWNS", "MARS_GOVERNORS", "MARS_ASSISTANCE")

    def test_14_mars_medical_mint_and_iron_categories_not_unique(self):
        self.once(
            "MARS_SURGEONS",
            "MARS_PHYSICIANS",
            "MARS_DRUGGISTS",
            "MARS_APOTHECARIES",
            "MARS_MINT_MASTERS",
            "MARS_IRON_INSTRUMENTS",
        )

    def test_15_next_twelfth_and_imprisonment_separate(self):
        self.once("TWELFTH_HOUSE_DIVIDER", "NEXT_CLXXXIV_IMPRISONMENT")
        self.assertEqual(self.rules["next_printed_chapter"], "CLXXXIV")
        self.assertEqual(self.rules["next_original_folio"], 763)

    def test_16_death_next_is_navigation_only(self):
        self.once("NEXT_CLXXXV_DEATH")
        self.assertEqual(
            [
                x["id"]
                for x in self.rules["rules"]
                if x["historical_evidence_type"] == "NEXT_SOURCE_NAVIGATION"
            ],
            ["R13269", "R13270", "R13271"],
        )
        self.assertEqual(self.rules["substantive"], 32)

    def test_17_all_source_records_known_merchant_not_validated(self):
        self.assertTrue(self.a["known_merchant"])
        for x in self.rules["rules"]:
            self.assertTrue(x["merchant_already_known_to_author"])
            for field in (
                "independent_real_business_associate_outcome_verified",
                "independent_real_friendship_count_or_quality_verified",
                "original_known_merchant_birth_clock_and_chart_engine_verified",
                "independent_human_blind_forecast_tested",
                "actual_person_partner_reliability_danger_inference_authorized",
                "runtime_astrological_rule_promoted",
            ):
                self.assertFalse(x[field], (x["id"], field))

    def test_18_archive_acceptance_rule_sha_and_scope(self):
        self.assertEqual(self.accept["Lilly_before"], 13236)
        self.assertEqual(self.accept["Lilly_after_if_accepted"], 13271)
        self.assertEqual(self.accept["Western_after_if_accepted"], 14337)
        self.assertEqual(self.accept["source_editorial_ordinal"], 185)
        self.assertEqual(self.accept["source_photo_count"], 5)
        self.assertEqual(self.accept["real_human_blind_validations"], 0)
        self.assertEqual(self.accept["runtime_promotions"], 0)
        self.assertEqual(sha(B / "RULES.json"), self.accept["rules_sha256"])
        self.assertEqual(
            sha(B / "SOURCE_FIRST_AUTHORING_20261021.json"),
            self.accept["source_first_sha256"],
        )
        self.assertEqual(
            sha(B / "ORIGINAL_SOURCE_WITNESS_20261021.json"),
            self.accept["witness_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
