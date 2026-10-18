"""Original Lilly 1647 CLVII direction effects: documentary conditions only."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class OriginalDurationOfDirections(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.r = j("RULES.json")
        cls.w = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.m = j("SOURCE_TO_RECORD_MAP.json")
        cls.limits = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.guard = j("DURATION_HISTORICAL_NONPROMOTION_GUARD_V1.json")
        cls.acc = j("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])

    def one(self, *roles):
        for role in roles:
            self.assertEqual(self.roles[role], 1, role)

    def test_01_original_photo_sha_and_bytes(self):
        self.assertEqual(list(self.w["images"]), ["688", "689", "690"])
        for item in self.w["images"].values():
            raw = (B / item["file"]).read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), item["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), item["sha256"])

    def test_02_first_edition_printed_folios_and_next_header(self):
        self.assertEqual(self.w["body_original_pdf_frames"], [688, 689, 690])
        self.assertEqual(self.w["next_printed_CLVIII_heading_frame"], 690)
        self.assertEqual(
            [x["printed_folio"] for x in self.w["images"].values()],
            ["654", "655", "656"],
        )

    def test_03_exact_unique_62_historical_records(self):
        self.assertEqual(
            [r["record_number"] for r in self.r["rules"]],
            list(range(10596, 10658)),
        )
        self.assertEqual(len({r["id"] for r in self.r["rules"]}), 62)

    def test_04_reversible_six_source_groups(self):
        ids = []
        for authored, reverse in zip(self.a["groups"], self.m["source_groups"], strict=True):
            self.assertEqual(authored["source_span"], reverse["source_span"])
            self.assertEqual(authored["original_pdf_frames"], reverse["original_pdf_frames"])
            source_ids = [x["id"] for x in authored["claims"]]
            self.assertEqual(source_ids, reverse["mapped_record_ids"])
            ids.extend(source_ids)
        self.assertEqual(ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(self.m["source_group_count"], 6)

    def test_05_separate_duration_vs_magnitude_not_mislabel(self):
        self.one("heading", "direction_effects_title", "vehemency")
        self.assertFalse(self.guard["numeric_effect_duration_rule_present"])

    def test_06_both_natal_source_actors_required(self):
        self.one("significator_strength", "promittor_strength", "root_radix")

    def test_07_both_essential_dignity_and_angular_for_full_effect(self):
        self.one("both_dignified", "both_angular", "manifest", "perform_full")

    def test_08_sun_sextile_moon_both_dignified_example(self):
        self.one("sun_sextile_moon", "sun_moon_essentials", "felicity")

    def test_09_one_strong_other_weak_gives_moderate(self):
        self.one("one_strong_other_weak", "effects_mean", "which_stronger")

    def test_10_significator_more_powerful_small_cause_success(self):
        self.one("significator_stronger", "happiness_without_cause")

    def test_11_promittor_more_powerful_alternate_cause(self):
        self.one("promittor_stronger", "felicity_appear", "not_magnitude_cause")

    def test_12_both_weak_graded_and_small_cause(self):
        self.one(
            "both_weak", "effects_according", "poor_cause", "degree_weakness", "less_answerable"
        )

    def test_13_wholly_weak_may_mean_zero_event(self):
        self.one("both_wholly_weak", "come_to_nothing", "shadow_only")
        self.assertTrue(self.r["author_allows_nonoccurrence"])

    def test_14_strong_malefic_promittor_own_house_is_mitigation(self):
        self.one(
            "malefic_promittor",
            "sad_event",
            "radix_strong",
            "own_house",
            "evil_tolerable",
            "not_hurt_own",
            "weak_more_bad",
        )

    def test_15_same_year_good_bad_directions_both_may_operate(self):
        self.one(
            "same_year_dual",
            "different_significators",
            "doubtful_astrologer",
            "both_effects",
            "no_mutual_disturbance",
        )
        self.assertTrue(self.r["author_good_bad_simultaneous"])

    def test_16_same_natal_domain_requires_special_arbitration(self):
        self.one("agreement_conveniency", "moon_asc_health")

    def test_17_mars_square_fiery_fevers_unsupported_medical_claim(self):
        self.one("asc_square_mars", "fiery_sign", "fever_claim")

    def test_18_venus_sextile_or_trine_watery_opposite_claim(self):
        self.one("moon_sextile_venus", "moon_trine_venus", "watery_sign", "sick_or_evade")

    def test_19_profection_or_annual_revolution_competing_methods(self):
        self.one("profection_chart", "annual_revolution")
        self.assertFalse(self.limits["annual_profection_revolution_parity_verified"])

    def test_20_annual_mars_alignment_bad_vs_venus_good(self):
        self.one("agree_mars", "ill_branch", "agree_venus", "escape_illness")

    def test_21_remaining_uncertainty_fallback_original_radix(self):
        self.one("still_uncertain", "compare_root_strength", "give_preeminence", "both_partake")

    def test_22_no_directional_event_math_verified(self):
        self.assertFalse(
            self.guard["original_direction_and_annual_methods_mathematically_verified"]
        )
        self.assertFalse(self.limits["numeric_event_duration_equation_present"])

    def test_23_next_CLVIII_is_five_hylegiacal_not_same_source(self):
        self.assertEqual(
            [r["id"] for r in self.r["rules"] if r["role"] == "next_navigation"],
            ["R10656", "R10657"],
        )
        self.assertEqual(self.acc["next_printed"], "CLVIII")
        self.assertEqual(self.acc["next_pdf"], 690)

    def test_24_zero_real_person_clinical_event_validation(self):
        self.assertFalse(self.limits["source_high_stakes_person_level_predictions_authorized"])
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for item in self.r["rules"]:
            for name in (
                "independent_real_direction_magnitude_validated",
                "independent_real_direction_duration_validated",
                "actual_real_person_medical_or_legal_accuracy_validated",
                "original_primary_direction_geometry_verified",
                "original_profection_revolution_parity_verified",
                "real_person_birth_rectification_validation_independent",
                "real_person_danger_or_illness_prediction_authorized",
                "runtime_model_promoted",
            ):
                self.assertFalse(item[name], (item["id"], name))

    def test_25_acceptance_hashes_and_numbered_chapter(self):
        self.assertEqual(self.acc["prior_lilly"], 10595)
        self.assertEqual(self.acc["lilly_if_published"], 10657)
        self.assertEqual(self.acc["combined_if_published"], 11723)
        self.assertEqual(self.acc["new_numbered_chapters"], 1)
        for file, key in (
            ("RULES.json", "rules_sha256"),
            ("SOURCE_FIRST_AUTHORING_20261018.json", "authoring_sha256"),
            ("DURATION_HISTORICAL_NONPROMOTION_GUARD_V1.json", "guard_sha256"),
        ):
            self.assertEqual(
                hashlib.sha256((B / file).read_bytes()).hexdigest(),
                self.acc[key],
            )


if __name__ == "__main__":
    unittest.main()
