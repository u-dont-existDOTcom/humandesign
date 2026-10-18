"""Lilly unnumbered tenth-house original source documentary checks only."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class TenthHouseOriginalSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.author = j("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.rules = j("RULES.json")
        cls.witness = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.map = j("SOURCE_TO_RECORD_MAP.json")
        cls.limits = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.accept = j("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.rules["rules"])

    def one(self, *roles):
        for name in roles:
            self.assertEqual(self.roles[name], 1, name)

    def test_01_original_images_sha_and_bytes(self):
        self.assertEqual(list(self.witness["images"]), ["649", "650", "651"])
        for info in self.witness["images"].values():
            raw = (B / info["file"]).read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), info["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), info["sha256"])

    def test_02_ninth_to_tenth_boundary_exact(self):
        self.assertTrue(self.witness["unnumbered"])
        self.assertEqual(self.witness["body_original_pdf_frames"], [649])
        self.assertEqual(self.witness["following_printed_CXLIIII_heading_pdf"], 649)
        self.assertEqual(
            [v["printed_folio"] for v in self.witness["images"].values()],
            ["615", "616", "617"],
        )

    def test_03_19_historical_records_unique_contiguous(self):
        self.assertEqual(
            [r["record_number"] for r in self.rules["rules"]],
            list(range(9106, 9125)),
        )
        self.assertEqual(len({r["id"] for r in self.rules["rules"]}), 19)

    def test_04_three_source_groups_reversibly_mapped(self):
        ids = []
        for a, m in zip(self.author["source_groups"], self.map["source_groups"], strict=True):
            self.assertEqual(a["source_span"], m["source_span"])
            self.assertEqual(a["original_pdf_frames"], m["original_pdf_frames"])
            x = [r["id"] for r in a["claims"]]
            self.assertEqual(x, m["mapped_record_ids"])
            ids.extend(x)
        self.assertEqual(ids, [r["id"] for r in self.rules["rules"]])

    def test_05_four_historical_target_names_not_conflated(self):
        self.one("honours", "preferment", "dignity", "estimation")

    def test_06_luminary_and_sun_priority_vs_planets(self):
        self.one(
            "luminaries_first",
            "sun_most_considerable",
            "planets_behold_lights",
            "sun_beheld_especially",
        )

    def test_07_planet_aspect_limited_half_orbs(self):
        self.one("mediety_of_orbs")
        self.assertFalse(self.limits["original_fixed_star_orb_table_complete"])

    def test_08_second_and_third_mid_heaven_distinct(self):
        self.one("second_midheaven_lord", "third_midheaven_planets")

    def test_09_fourth_regal_stars_magnitude_and_two_cusps(self):
        self.one("fourth_regal_stars", "star_magnitude", "near_tenth_cusp", "near_first_cusp")

    def test_10_numbered_chapter_next_same_page_not_merged(self):
        self.assertEqual(
            [r["id"] for r in self.rules["rules"] if r["role"] == "next_numbered_navigation"],
            ["R9123", "R9124"],
        )
        self.assertEqual(self.accept["numbered_chapters_added"], 0)
        self.assertEqual(self.accept["next_source"], "CXLIIII")
        self.assertEqual(self.accept["next_original_pdf"], 649)

    def test_11_actual_human_social_rank_or_promotion_validation_zero(self):
        self.assertEqual(self.rules["empirical_validations"], 0)
        self.assertEqual(self.rules["runtime_promotions"], 0)
        for r in self.rules["rules"]:
            for k in (
                "real_human_honour_status_accuracy_validated",
                "real_career_rank_or_esteem_accuracy_validated",
                "regal_star_natal_conjunction_calculated",
                "real_person_professional_advice_authorized",
                "runtime_model_promoted",
            ):
                self.assertFalse(r[k], (r["id"], k))

    def test_12_accepted_hash_and_cumulative_counts(self):
        self.assertEqual(self.accept["prior_lilly"], 9105)
        self.assertEqual(self.accept["lilly_if_published"], 9124)
        self.assertEqual(self.accept["combined_if_published"], 10190)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.accept["rules_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
