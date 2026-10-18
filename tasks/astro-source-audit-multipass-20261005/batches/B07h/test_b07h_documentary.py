"""Original Lilly 1647 CLIII enemy quality: documentary integrity only."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class OriginalEnemyQuality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.r = j("RULES.json")
        cls.w = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.m = j("SOURCE_TO_RECORD_MAP.json")
        cls.lim = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.acc = j("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])

    def one(self, *names):
        for n in names:
            self.assertEqual(self.roles[n], 1, n)

    def test_01_original_photo_sha_bytes(self):
        self.assertEqual(list(self.w["images"]), [str(n) for n in range(674, 678)])
        for item in self.w["images"].values():
            raw = (B / item["file"]).read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), item["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), item["sha256"])

    def test_02_source_pdf_folios_and_next_seam(self):
        self.assertEqual(self.w["body_pdf_frames"], [674, 675])
        self.assertEqual(self.w["following_printed_CLIIII_heading_pdf"], 675)
        self.assertEqual(
            [x["printed_folio"] for x in self.w["images"].values()],
            ["640", "641", "642", "643"],
        )

    def test_03_all_40_records_consecutive(self):
        self.assertEqual([x["record_number"] for x in self.r["rules"]], list(range(10043, 10083)))
        self.assertEqual(len({x["id"] for x in self.r["rules"]}), 40)

    def test_04_four_inverse_source_groups(self):
        ids = []
        for src, dest in zip(self.a["groups"], self.m["source_groups"], strict=True):
            self.assertEqual(src["source_span"], dest["source_span"])
            self.assertEqual(src["original_pdf_frames"], dest["original_pdf_frames"])
            subset = [x["id"] for x in src["claims"]]
            self.assertEqual(subset, dest["mapped_record_ids"])
            ids.extend(subset)
        self.assertEqual(ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(len(self.m["source_groups"]), 4)

    def test_05_quality_not_enemy_count(self):
        self.one("heading", "quality_target")
        self.assertEqual(self.r["substantive"], 38)

    def test_06_planets_seventh_twelfth_lords_opposite_lights(self):
        self.one(
            "seventh_occupants",
            "twelfth_occupants",
            "twelfth_lord",
            "seventh_lord",
            "opposite_lights",
        )

    def test_07_open_seventh_or_opposing_lights_vs_hidden_twelfth(self):
        self.one("open_seventh", "open_opposition", "hidden_twelfth", "backbiters")

    def test_08_eleventh_lord_seventh_can_reverse_friendship(self):
        self.one("eleventh_lord_seventh", "friend_at_one_time", "good_direction", "bad_direction")

    def test_09_twelfth_lord_ascendant_paradox_friend(self):
        self.one("twelfth_lord_asc", "turns_friendly", "asc_lord_dispose")

    def test_10_power_hierarchy_planet_nature_house_strength(self):
        self.one("prevalency_heading", "first_nature", "second_houses", "third_fortitude")

    def test_11_benefics_can_mean_powerful_adversaries(self):
        self.one("benefics_powerful", "malefics_obscure")
        self.assertEqual(self.r["empirical_validations"], 0)

    def test_12_angular_strength_mid_succedent_low_cadent(self):
        self.one("angular_strong", "angular_powerful", "succedent", "cadent")

    def test_13_essential_dignity_high_vs_peregrine_detriment_fall_low(self):
        self.one(
            "essential_dignities",
            "dignified_powerful",
            "peregrine",
            "detriment",
            "fall",
            "obscure_enemies",
        )

    def test_14_triplicity_terms_faces_mid_social_class(self):
        self.one("triplicities", "terms", "faces", "low_fortune")

    def test_15_following_CLIIII_not_imported(self):
        self.assertEqual(
            [r["id"] for r in self.r["rules"] if r["role"] == "next_chapter_navigation"],
            ["R10081", "R10082"],
        )
        self.assertEqual(self.acc["next_printed_chapter"], "CLIIII")
        self.assertEqual(self.acc["next_original_pdf"], 675)

    def test_16_person_hidden_intent_danger_unverified(self):
        self.assertFalse(self.lim["real_person_enmity_danger_inference_authorized"])
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for x in self.r["rules"]:
            for key in (
                "independent_real_enemy_identity_or_quality_validated",
                "independent_real_open_vs_covert_hostility_validated",
                "independent_real_enemy_social_power_validated",
                "independent_real_person_morality_or_safety_validated",
                "person_enemy_danger_or_moral_classification_authorized",
                "runtime_model_promoted",
            ):
                self.assertFalse(x[key], (x["id"], key))

    def test_17_expected_digest_and_record_total(self):
        self.assertEqual(self.acc["prior_lilly"], 10042)
        self.assertEqual(self.acc["lilly_if_published"], 10082)
        self.assertEqual(self.acc["combined_if_published"], 11148)
        self.assertEqual(self.acc["numbered_chapters_added"], 1)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.acc["rules_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
