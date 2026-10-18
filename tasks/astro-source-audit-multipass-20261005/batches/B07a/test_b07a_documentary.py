"""Lilly CXLVII honors persistence: original-document tests, not personal predictions."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class OriginalHonoursDuration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.r = j("RULES.json")
        cls.w = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.m = j("SOURCE_TO_RECORD_MAP.json")
        cls.limits = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.acc = j("ACCEPTANCE.json")
        cls.roles = Counter(row["role"] for row in cls.r["rules"])
        cls.text = " ".join(row["original_anchor_not_diplomatic"] for row in cls.r["rules"])

    def one(self, *roles):
        for role in roles:
            self.assertEqual(self.roles[role], 1, role)

    def test_01_source_photos_sha256_member_bytes(self):
        self.assertEqual(list(self.w["images"]), [str(x) for x in range(656, 661)])
        for v in self.w["images"].values():
            raw = (B / v["file"]).read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), v["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), v["sha256"])

    def test_02_page_folios_and_original_next_seam(self):
        self.assertEqual(self.w["body_original_pdf_frames"], [656, 657, 658])
        self.assertEqual(self.w["following_printed_CXLVIII_heading_pdf"], 658)
        self.assertEqual(
            [x["printed_folio"] for x in self.w["images"].values()],
            ["622", "623", "624", "625", "626"],
        )

    def test_03_source_seventy_seven_unique_historical_records(self):
        self.assertEqual(
            [x["record_number"] for x in self.r["rules"]],
            list(range(9368, 9445)),
        )
        self.assertEqual(len(set(x["id"] for x in self.r["rules"])), 77)

    def test_04_six_photo_groups_bidirectionally_mapped(self):
        ids = []
        for source, reverse in zip(self.a["groups"], self.m["source_groups"], strict=True):
            self.assertEqual(source["source_span"], reverse["source_span"])
            self.assertEqual(source["original_pdf_frames"], reverse["original_pdf_frames"])
            refs = [c["id"] for c in source["claims"]]
            self.assertEqual(refs, reverse["mapped_record_ids"])
            ids.extend(refs)
        self.assertEqual(ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(self.m["source_group_count"], 6)

    def test_05_honor_duration_not_exist_or_kind_of_honor(self):
        self.one("heading", "status_duration_target")
        self.assertEqual(self.r["substantive"], 75)

    def test_06_planet_contact_partile_most_powerful_required(self):
        self.one("planets_in_contact", "planets_partile_aspects", "most_powerful")
        self.assertEqual(
            next(r for r in self.r["rules"] if r["role"] == "planets_in_contact")["qualification"],
            "glyph-unresolved",
        )

    def test_07_strong_jupiter_or_venus_easy_increasing_source(self):
        self.one(
            "benefic_jupiter", "benefic_venus", "benefic_strong", "benefic_increase", "benefic_easy"
        )

    def test_08_moderate_benefics_obstruction_not_total_failure(self):
        self.one("benefics_moderately_afflicted", "gradual_rise", "continue_obstructions")

    def test_09_weak_benefics_temporary_decrease_not_absolute_loss(self):
        self.one("benefics_weak", "honor_temporary", "decrease_not_vanish")

    def test_10_saturn_and_mars_strong_can_preserve_with_interruptions(self):
        self.one(
            "malefic_saturn",
            "malefic_mars",
            "malefic_happy_position",
            "malefic_continue",
            "malefic_interruption",
        )

    def test_11_malefic_mean_decline_vs_extreme_vanish(self):
        self.one(
            "malefic_mean", "honor_wears", "glimpse_remains", "malefic_unlucky", "honors_vanish"
        )

    def test_12_mercury_fast_rise_but_later_maintenance_difficulty(self):
        self.one(
            "mercury_selected",
            "mercury_fast_rise",
            "mercury_some_duration",
            "mercury_instability",
            "mercury_unstable",
        )

    def test_13_mercury_intellect_can_modify_bad_outcome(self):
        self.one("mercury_moderately_fortified", "mercury_risk_ruin", "mercury_understanding")

    def test_14_weak_mercury_rise_then_strong_decline(self):
        self.one("mercury_debilitated", "mercury_rise_then_bad")

    def test_15_absent_aspects_tenth_occupant_first_fallback(self):
        self.one(
            "no_light_contact",
            "tenth_occupants",
            "tenth_nature",
            "tenth_fortitude",
            "tenth_essential_dignity",
        )

    def test_16_empty_tenth_ruler_fallback_only_if_empty(self):
        self.one("tenth_empty", "tenth_lord")

    def test_17_composite_fixed_sign_and_benefic_aspect(self):
        self.one("fixed_lord", "fixed_tenth_sign", "support_contact", "continued_status")

    def test_18_sun_moon_jupiter_venus_are_distinct_supports(self):
        self.one("support_sun", "support_moon", "support_jupiter", "support_venus")

    def test_19_special_fixed_star_aphorisms_inside_same_chapter(self):
        self.one(
            "special_heading",
            "bright_stars_angles",
            "hyades",
            "hercules",
            "cor_scorpii",
            "lanx_australis",
        )

    def test_20_stellar_rise_can_end_in_collapse(self):
        self.one("malefic_hard", "raised_from_poverty", "later_collapse")

    def test_21_bad_solar_direction_and_revolution_vs_temporary_fall(self):
        self.one(
            "sun_sign_uncertain",
            "sun_star_company",
            "ill_direction",
            "ill_revolution",
            "permanent_fall",
            "one_trigger",
            "temporary_fall_recover",
        )
        self.assertFalse(self.limits["original_solar_and_lunar_glyphs_fully_deciphered"])

    def test_22_king_and_people_method_requires_two_nativities(self):
        self.one("king_justice", "nation_nativity")
        self.assertIn("Nativity concurre with people Kingdom", self.text)

    def test_23_lunar_infamy_compound_is_not_morality_measure(self):
        self.one(
            "moon_mc_sign",
            "malefics_fourth",
            "infamy_claim",
            "moon_scorpio",
            "mars_taurus",
            "infamous_forever",
        )
        self.assertFalse(
            self.limits["actual_person_moral_status_or_travel_safety_claim_authorized"]
        )

    def test_24_profession_chapter_is_new_source_not_honor_duration(self):
        self.assertEqual(
            [x["id"] for x in self.r["rules"] if x["role"] == "next_chapter_navigation"],
            ["R9443", "R9444"],
        )
        self.assertEqual(self.acc["following_printed_chapter"], "CXLVIII")
        self.assertEqual(self.acc["following_heading_pdf"], 658)

    def test_25_zero_real_person_mortality_rank_or_infamy_accuracy(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for x in self.r["rules"]:
            for key in (
                "real_person_honor_persistence_validated",
                "real_person_promotion_or_loss_age_validated",
                "actual_reputation_or_moral_trait_validated",
                "fixed_star_natal_parity_verified",
                "joint_nation_individual_chart_method_verified",
                "real_person_social_danger_or_prognosis_authorized",
                "runtime_model_promoted",
            ):
                self.assertFalse(x[key], (x["id"], key))

    def test_26_source_hash_and_cumulative_count(self):
        self.assertEqual(self.acc["previous_lilly"], 9367)
        self.assertEqual(self.acc["lilly_if_published"], 9444)
        self.assertEqual(self.acc["combined_if_published"], 10510)
        self.assertEqual(self.acc["new_numbered_chapters"], 1)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.acc["rules_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
