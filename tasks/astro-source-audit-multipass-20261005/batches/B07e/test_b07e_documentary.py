"""Original William Lilly 1647 printed CL: documentary tests not human friend character claims."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class OriginalQualityOfFriends(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = read("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.r = read("RULES.json")
        cls.w = read("ORIGINAL_SOURCE_WITNESS.json")
        cls.m = read("SOURCE_TO_RECORD_MAP.json")
        cls.limits = read("UNRESOLVED_SOURCE_LIMITS.json")
        cls.acc = read("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])

    def one(self, *roles):
        for role in roles:
            self.assertEqual(self.roles[role], 1, role)

    def test_01_original_photo_sha256_bytes(self):
        self.assertEqual(list(self.w["images"]), [str(n) for n in range(670, 674)])
        for photo in self.w["images"].values():
            raw = (B / photo["file"]).read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), photo["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), photo["sha256"])

    def test_02_printed_original_folios_and_next_chapter_seam(self):
        self.assertEqual(self.w["body_pdf_frames"], [670, 671])
        self.assertEqual(self.w["following_printed_CLI_heading_pdf"], 671)
        self.assertEqual(
            [x["printed_folio"] for x in self.w["images"].values()],
            ["636", "637", "638", "639"],
        )

    def test_03_64_consecutive_historical_records(self):
        self.assertEqual(
            [r["record_number"] for r in self.r["rules"]],
            list(range(9863, 9927)),
        )
        self.assertEqual(len({r["id"] for r in self.r["rules"]}), 64)

    def test_04_six_original_source_groups_bidirectional_map(self):
        ids = []
        for source, dest in zip(self.a["groups"], self.m["source_groups"], strict=True):
            self.assertEqual(source["source_span"], dest["source_span"])
            self.assertEqual(source["original_pdf_frames"], dest["original_pdf_frames"])
            row_ids = [x["id"] for x in source["claims"]]
            self.assertEqual(row_ids, dest["mapped_record_ids"])
            ids.extend(row_ids)
        self.assertEqual(ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(len(self.m["source_groups"]), 6)

    def test_05_distinguish_friend_type_from_number_and_trust(self):
        self.one("target_quality", "planet_nature")
        self.assertEqual(self.r["substantive"], 62)

    def test_06_occupied_first_and_eleventh_before_rulers(self):
        self.one("planets_first", "planets_eleventh", "if_any", "lords_eleventh", "lords_first")

    def test_07_intercepted_sign_conditional(self):
        self.one("intercepted_sign")

    def test_08_saturn_older_agriculture_metals_stone_usury(self):
        self.one(
            "saturn",
            "saturn_old",
            "saturn_husbandman",
            "saturn_metals",
            "saturn_stonecutters",
            "saturn_usurers",
            "saturn_covetous",
        )

    def test_09_jupiter_clergy_legal_nobles_and_moral_stereotypes(self):
        self.one(
            "jupiter",
            "jupiter_clergy",
            "jupiter_lawyers",
            "jupiter_nobles",
            "jupiter_rulers",
            "jupiter_honest",
        )

    def test_10_mars_soldiers_surgeons_redhair_trades(self):
        self.one(
            "mars",
            "mars_captains",
            "mars_chirurgions",
            "mars_bold",
            "mars_red_hair",
            "mars_tradesmen",
        )

    def test_11_sun_kings_authority_counsellors_magistrates(self):
        self.one("sun", "sun_royal", "sun_counsellors", "sun_authority", "sun_magistrates")

    def test_12_venus_cultural_trades_and_gender_stereotypes(self):
        self.one(
            "venus",
            "venus_musicians",
            "venus_apothecaries",
            "venus_gamesters",
            "venus_painters",
            "venus_women",
            "venus_uxorious",
        )

    def test_13_mercury_learned_crafts_merchants_character(self):
        self.one("mercury", "mercury_learned", "mercury_merchants", "mercury_subtle")

    def test_14_moon_social_gender_roles_sailors_inconstancy(self):
        self.one(
            "moon", "moon_widows", "moon_envoys", "moon_seafarers", "moon_common", "moon_inconstant"
        )

    def test_15_constancy_heading_not_occupational_source(self):
        self.one("constancy_heading", "constancy_eleventh_sign", "constancy_planet_signs")

    def test_16_fixed_cusp_contrasted_with_movable_and_common(self):
        self.one(
            "fixed_cusp",
            "fixed_friendship",
            "movable_cusp",
            "movable_mutable",
            "common_sign",
            "different_constancy",
        )

    def test_17_negative_ruler_aspect_venus_house_original_scope_unresolved(self):
        self.one("lord_eleventh_not_aspect", "venus_own_house", "small_comfort")
        self.assertFalse(self.limits["friendship_quality_original_operator_complete"])

    def test_18_next_CLI_requires_two_nativities_and_not_imported(self):
        self.assertEqual(
            [r["id"] for r in self.r["rules"] if r["role"] == "next_chapter_navigation"],
            ["R9925", "R9926"],
        )
        self.assertEqual(self.acc["next_printed_chapter"], "CLI")
        self.assertEqual(self.acc["next_original_pdf"], 671)

    def test_19_no_person_friend_social_class_moral_or_professional_validity(self):
        self.assertFalse(
            self.limits["real_person_trustworthiness_or_demographic_inference_authorized"]
        )
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for x in self.r["rules"]:
            for key in (
                "independent_real_friend_occupation_accuracy_validated",
                "independent_real_friend_status_or_appearance_validated",
                "independent_real_friend_constancy_validated",
                "real_person_loyalty_or_morality_inference_authorized",
                "separate_relationship_synastry_rule_validated",
                "runtime_model_promoted",
            ):
                self.assertFalse(x[key], (x["id"], key))

    def test_20_acceptance_and_source_sha(self):
        self.assertEqual(self.acc["prior_lilly"], 9862)
        self.assertEqual(self.acc["lilly_if_published"], 9926)
        self.assertEqual(self.acc["combined_if_published"], 10992)
        self.assertEqual(self.acc["numbered_chapters_added"], 1)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.acc["rules_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
