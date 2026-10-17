"""Original Lilly multiple-wives historic methods, not human validation."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class NumberOfWivesSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = read("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = read("RULES.json")
        cls.map = read("SOURCE_TO_RECORD_MAP.json")
        cls.w = read("ORIGINAL_SOURCE_WITNESS.json")
        cls.methods = read("COMPETING_WIFE_COUNT_HISTORICAL_METHODS_V1.json")
        cls.limits = read("UNRESOLVED_SOURCE_LIMITS.json")
        cls.accept = read("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])
        cls.text = " ".join(x["original_anchor_not_diplomatic"] for x in cls.r["rules"])

    def test_01_original_jpegs_bytes_and_sha256(self):
        self.assertEqual(list(self.w["images"]), ["624", "625", "626", "627"])
        for photo in self.w["images"].values():
            p = B / photo["file"]
            raw = p.read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), photo["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), photo["sha256"])

    def test_02_pages_and_separate_geographic_next_chapter(self):
        self.assertEqual(self.w["body_pdf_frames"], [624, 625, 626])
        self.assertEqual(self.w["following_printed_CXXXIII_heading_frame"], 626)
        self.assertEqual(
            [x["printed_folio"] for x in self.w["images"].values()],
            ["590", "591", "592", "593"],
        )

    def test_03_consecutive_80_historical_ids(self):
        self.assertEqual(
            [r["record_number"] for r in self.r["rules"]],
            list(range(8027, 8107)),
        )
        self.assertEqual(len({r["id"] for r in self.r["rules"]}), 80)

    def test_04_all_eleven_source_groups_reversible(self):
        all_ids = []
        for group, mapped in zip(self.a["groups"], self.map["source_groups"], strict=True):
            self.assertEqual(group["source_span"], mapped["source_span"])
            self.assertEqual(group["original_pdf_frames"], mapped["original_pdf_frames"])
            refs = [c["id"] for c in group["clauses"]]
            self.assertEqual(refs, mapped["mapped_record_ids"])
            all_ids.extend(refs)
        self.assertEqual(all_ids, [r["id"] for r in self.r["rules"]])
        self.assertEqual(self.map["source_group_count"], 11)

    def test_05_ten_competing_methods_no_posthoc_priority(self):
        self.assertEqual(len(self.methods["methods"]), 10)
        self.assertEqual(
            [m["id"] for m in self.methods["methods"]],
            ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10"],
        )
        self.assertIn("conflicting", self.methods["incompatibility_warning"])

    def test_06_watery_plural_and_virgo_leo_gemini_inverse(self):
        for role in (
            "watery_condition",
            "water_fruitful",
            "water_many",
            "water_more_than_one",
            "barren_inverse",
        ):
            self.assertEqual(self.roles[role], 1)
        self.assertIn("Virgo Leo Gemini", self.text)

    def test_07_moon_venus_priority_and_seventh_exceptions(self):
        for role in (
            "moon_venus_priority",
            "moon_seventh",
            "moon_seventh_many",
            "moon_saturn_exception",
            "moon_sun_exception",
            "potent_moon",
            "potent_many",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_08_lilly_never_failed_anecdote_not_a_validated_human_cohort(self):
        self.assertEqual(self.roles["moon_personal_confidence"], 1)
        row = next(r for r in self.r["rules"] if r["role"] == "moon_personal_confidence")
        self.assertEqual(row["source_qualification"], "unverified-author-claim")
        self.assertFalse(row["independent_legal_spouse_count_validated"])

    def test_09_explicit_concubine_escape_and_no_legal_wife_result(self):
        self.assertEqual(self.roles["concubine_escape"], 1)
        self.assertEqual(self.roles["not_always_two_wives"], 1)
        self.assertIn("not alwayes two Wives", self.text)

    def test_10_moon_exactly_one_companion_only_one_wife(self):
        for role in ("moon_one_planet", "moon_conjunction_type", "one_wife"):
            self.assertEqual(self.roles[role], 1)
        self.assertIn("platick or partill", self.text)

    def test_11_death_order_relative_planetary_strength_high_stakes(self):
        for role in ("moon_stronger", "husband_outlives", "planet_stronger", "husband_dies_first"):
            self.assertEqual(self.roles[role], 1)
        rows = [
            x for x in self.r["rules"] if x["role"] in {"husband_outlives", "husband_dies_first"}
        ]
        self.assertTrue(all(not x["marital_survival_order_validated"] for x in rows))

    def test_12_moon_partile_aspects_application_direction_and_sun_exclusion(self):
        for role in (
            "no_conjunction",
            "count_planets",
            "require_direct",
            "exclude_combust",
            "exclude_fall",
            "exclude_detriment",
            "moon_applies",
            "exclude_sun",
        ):
            self.assertEqual(self.roles[role], 1)
        self.assertIn("not they unto her", self.text)

    def test_13_fruitful_signs_doubling_not_independent_replication(self):
        self.assertEqual(self.roles["fruitful_doubles"], 1)

    def test_14_ptolemy_attributed_one_form_and_bicorporeal_uncorroborated(self):
        for role in (
            "ptolemy_attribution",
            "one_form_sign",
            "one_form_application",
            "ptolemy_one",
            "bicorporeal_sign",
            "bicorporeal_many_aspects",
            "ptolemy_many",
        ):
            self.assertEqual(self.roles[role], 1)
        m = self.methods["methods"][4]
        self.assertFalse(m["original_ptolemy_independently_collated"])
        self.assertFalse(self.limits["verified_ptolemy_original_comparison"])

    def test_15_mid_heaven_venus_arc_count_direction_and_conditions(self):
        for role in (
            "fallback_no_other",
            "count_direct",
            "count_not_combust",
            "count_sun_beams",
            "between_mc_venus",
            "progress_mc_to_asc",
            "planet_count_wives",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_16_retrograde_combust_dignity_exception(self):
        for role in (
            "retrograde_count",
            "combust_count",
            "domicile_exception",
            "exaltation_exception",
            "mutual_reception_exception",
            "count_after_rescue",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_17_fallback_partile_seventh_lord_includes_retro_combust(self):
        for role in (
            "fallback_all_fail",
            "seventh_ruler_target",
            "partile_only",
            "retrograde_allowed",
            "combust_allowed",
            "count_seventh",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_18_lilly_best_personal_experience_applying_not_separating(self):
        for role in (
            "author_prefers",
            "moon_sign_count",
            "moon_applying",
            "moon_not_separating",
            "same_sign_count",
        ):
            self.assertEqual(self.roles[role], 1)
        p = next(x for x in self.r["rules"] if x["role"] == "author_prefers")
        self.assertEqual(p["source_qualification"], "unverified-author-claim")

    def test_19_lilly_fallback_dignity_in_moon_sign_partile(self):
        for role in (
            "if_no_bodily",
            "planet_dignities_moon_sign",
            "partile_aspect_to_moon",
            "wives_from_dignity",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_20_weak_significators_concubine_or_wooing_not_wives(self):
        for role in ("weak_indicator_caveat", "nonmarital_switch", "wooing_not_marriage"):
            self.assertEqual(self.roles[role], 1)

    def test_21_exact_two_or_three_wife_compound_conditions(self):
        for role in (
            "moon_common_sign",
            "two_wives",
            "moon_fruitful",
            "planet_fruitful",
            "three_wives",
            "seventh_prolific",
            "lord_seventh_fruitful",
            "three_wives_strong",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_22_next_cxxxiii_origin_not_counted(self):
        self.assertEqual(
            [x["id"] for x in self.r["rules"] if x["role"] == "next_chapter_navigation"],
            ["R8105", "R8106"],
        )
        self.assertEqual(self.r["substantive_historical"], 78)
        self.assertEqual(self.accept["next_printed_chapter"], "CXXXIII")

    def test_23_zero_verified_marriages_partner_counts_or_life_death(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["legal_marriage_or_partner_counts_validated"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        self.assertFalse(self.methods["actual_person_partner_claims_authorized"])
        for r in self.r["rules"]:
            self.assertFalse(r["independent_legal_spouse_count_validated"])
            self.assertFalse(r["independent_nonmarital_partner_count_validated"])
            self.assertFalse(r["marital_survival_order_validated"])
            self.assertFalse(r["private_partner_or_sexual_claim_authorized"])
            self.assertFalse(r["runtime_model_promoted"])

    def test_24_all_methods_are_source_author_not_independent_validations(self):
        for m in self.methods["methods"]:
            self.assertFalse(m["source_independent_replication"])
        self.assertEqual(self.methods["empirical_validations"], 0)
        self.assertFalse(self.r["full_diplomatic_transcription"])

    def test_25_counts_and_sha_digests(self):
        self.assertEqual(self.accept["previous_lilly"], 8026)
        self.assertEqual(self.accept["lilly_if_published"], 8106)
        self.assertEqual(self.accept["combined_if_published"], 9172)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.accept["rules_sha256"],
        )
        self.assertEqual(
            hashlib.sha256(
                (B / "COMPETING_WIFE_COUNT_HISTORICAL_METHODS_V1.json").read_bytes()
            ).hexdigest(),
            self.accept["competing_methods_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
