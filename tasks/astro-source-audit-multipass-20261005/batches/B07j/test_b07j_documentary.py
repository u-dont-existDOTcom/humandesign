"""Original Lilly 1647 captivity source integrity; legal/safety claims never validated."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class OriginalCaptivitySource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.r = j("RULES.json")
        cls.w = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.m = j("SOURCE_TO_RECORD_MAP.json")
        cls.lim = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.accept = j("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])

    def one(self, *roles):
        for role in roles:
            self.assertEqual(self.roles[role], 1, role)

    def test_01_original_page_photos_SHA256_and_bytes(self):
        self.assertEqual(list(self.w["images"]), ["676", "677", "678", "679"])
        for x in self.w["images"].values():
            raw = (B / x["file"]).read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), x["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), x["sha256"])

    def test_02_physical_boundary_CLV_to_CLVI(self):
        self.assertEqual(self.w["body_pdf_frames"], [676, 677])
        self.assertEqual(self.w["following_printed_CLVI_heading_frame"], 678)
        self.assertEqual(
            [x["printed_folio"] for x in self.w["images"].values()],
            ["642", "643", "644", "645"],
        )

    def test_03_100_unique_consecutive_historical_records(self):
        self.assertEqual(
            [x["record_number"] for x in self.r["rules"]],
            list(range(10147, 10247)),
        )
        self.assertEqual(len(set(x["id"] for x in self.r["rules"])), 100)

    def test_04_eight_source_groups_bidirectionally_mapped(self):
        ids = []
        for a, m in zip(self.a["groups"], self.m["source_groups"], strict=True):
            self.assertEqual(a["source_span"], m["source_span"])
            self.assertEqual(a["original_pdf_frames"], m["original_pdf_frames"])
            x = [c["id"] for c in a["claims"]]
            self.assertEqual(x, m["mapped_record_ids"])
            ids.extend(x)
        self.assertEqual(ids, [c["id"] for c in self.r["rules"]])
        self.assertEqual(self.m["source_group_count"], 8)

    def test_05_luminaries_before_malefics_before_houses(self):
        self.one(
            "luminaries_first",
            "saturn_second",
            "mars_second",
            "seventh_third",
            "twelfth_third",
            "occupants_third",
        )

    def test_06_saturn_secret_vs_mars_open_conflict_distinct(self):
        self.one("saturn_twelfth_prison", "saturn_secret_enemies", "mars_quarrels")

    def test_07_first_light_malefic_square_opposition_and_angles(self):
        self.one(
            "either_light",
            "malefic_square",
            "malefic_opposition",
            "malefics_angles",
            "malevolent_houses",
        )

    def test_08_original_signs_and_affliction_not_a_simple_rule(self):
        self.one(
            "source_signs",
            "infortune_opposes_light",
            "source_sun_moon_signs",
            "assert_imprisonment",
        )

    def test_09_luminary_twelfth_malefic_debilitated_conjunction(self):
        self.one(
            "one_light_twelfth",
            "light_conj_saturn",
            "light_conj_mars",
            "debilitated_malefics",
            "captivity",
        )

    def test_10_mars_seventh_twelfth_and_saturn_luminary_aspects(self):
        self.one(
            "mars_seventh_twelfth",
            "mars_sign_group",
            "mars_afflicts_light",
            "saturn_afflicts_light",
        )

    def test_11_saturn_mars_mutual_aspects_and_receipt_protections(self):
        self.one(
            "saturn_mars_mutual",
            "square_each_other",
            "conj_each_other",
            "no_exaltation",
            "no_own_house",
            "no_benefic_reception",
            "no_luminary_reception",
        )

    def test_12_malefics_extra_dignity_and_cusp_condition(self):
        self.one(
            "only_direct",
            "malefic_cusp_dignity",
            "capture_arrest_loss",
            "malefic_opposition_mutual",
            "one_first_second",
            "other_seventh_eighth",
            "either_lord_twelfth",
        )

    def test_13_fourth_planets_and_mars_venus_eighth_perpetual_claim(self):
        self.one(
            "saturn_moon_mars_fourth",
            "fourth_captivity",
            "mars_venus_eighth",
            "saturn_square_opposition",
            "saturn_sextile_sixth",
            "perpetual_imprisonment",
        )

    def test_14_twelfth_lord_mars_dignity_partile_affliction(self):
        self.one(
            "lord_twelfth_mars_dignity",
            "lord_twelfth_seventh",
            "malefic_partile",
            "lord_twelfth_captivity",
        )

    def test_15_asc_twelfth_conjunction_and_hard_aspects(self):
        self.one(
            "asc_twelfth_join",
            "conjunction_houses",
            "asc_lord_infortune",
            "asc_retrograde",
            "asc_combust_angular",
            "asc_hard_twelfth_lord",
            "source_confinement",
        )

    def test_16_twelfth_ruler_fall_or_detriment_and_platic_aspect(self):
        self.one(
            "lord_twelfth_fall", "malefic_afflict_lord", "partile_or_platick", "twelfth_lord_prison"
        )

    def test_17_multiple_conjunction_and_twelfth_occupant_alternatives(self):
        self.one(
            "planet_list_twelfth",
            "jupiter_saturn_mars",
            "sun_mars_mercury",
            "sun_mars_mercury_combust",
            "lord_seventh_twelfth",
            "lord_seventh_hard_aspect",
        )

    def test_18_luminaries_eighth_exception_and_benefic_prohibition(self):
        self.one(
            "sun_moon_eighth",
            "not_own_signs",
            "cancer_leo_taurus",
            "benefic_prohibition",
            "most_captivity",
            "sun_moon_own_signs",
            "malefic_partile_lights",
        )

    def test_19_sun_twelfth_vs_moon_ruling_asc_peregrine(self):
        self.one("sun_twelfth", "sun_sorrow", "moon_asc_lord", "moon_peregrine", "moon_same")

    def test_20_kings_service_exception_and_malefic_killing_claim(self):
        self.one(
            "lord_nat_under_beams",
            "not_leo_aries",
            "serve_kings",
            "royal_prison",
            "malefic_sun",
            "royal_death",
        )

    def test_21_long_vs_short_prison_distinct_source_and_protection(self):
        self.one(
            "duration_heading",
            "malefics_opposing_twelfth",
            "malefics_fortified",
            "unrestrained_malefic",
            "long_imprisonment",
            "benefic_aspects_twelfth",
            "short_imprisonment",
        )

    def test_22_printed_CLVI_death_is_separate(self):
        self.assertEqual(
            [x["id"] for x in self.r["rules"] if x["role"] == "next_navigation"],
            ["R10245", "R10246"],
        )
        self.assertEqual(self.accept["following_printed"], "CLVI")
        self.assertEqual(self.accept["following_heading_pdf"], 678)

    def test_23_no_actual_criminality_legal_duration_health_or_mortality(self):
        self.assertFalse(
            self.lim[
                "actual_person_criminality_captivity_medical_or_mortality_inference_authorized"
            ]
        )
        self.assertFalse(self.lim["fully_executable_captivity_risk_method"])
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for row in self.r["rules"]:
            for k in (
                "real_person_captivity_or_detention_accuracy_validated",
                "real_person_sentence_or_detention_duration_validated",
                "real_person_legal_risk_criminality_validated",
                "real_person_harm_mortality_or_health_validated",
                "original_astro_calculations_or_glyphs_fully_verified",
                "person_level_legal_medical_safety_forecast_authorized",
                "runtime_model_promoted",
            ):
                self.assertFalse(row[k], (row["id"], k))

    def test_24_cumulative_count_and_source_checksum(self):
        self.assertEqual(self.accept["prior_lilly"], 10146)
        self.assertEqual(self.accept["lilly_if_published"], 10246)
        self.assertEqual(self.accept["combined_if_published"], 11312)
        self.assertEqual(self.accept["numbered_chapters_added"], 1)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.accept["rules_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
