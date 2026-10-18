"""Lilly original CLVIII Ascendant/Saturn documentary checks only."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class OriginalSaturnDirections(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.r = j("RULES.json")
        cls.w = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.mapping = j("SOURCE_TO_RECORD_MAP.json")
        cls.lim = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.guard = j("CLVIII_SATURN_HISTORICAL_NONPROMOTION_GUARD_V1.json")
        cls.accept = j("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])

    def one(self, *roles):
        for role in roles:
            self.assertEqual(self.roles[role], 1, role)

    def test_01_original_source_images_sha_and_bytes(self):
        self.assertEqual(list(self.w["images"]), ["690", "691", "692"])
        for v in self.w["images"].values():
            raw = (B / v["file"]).read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), v["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), v["sha256"])

    def test_02_original_pdf_and_folio_boundaries(self):
        self.assertEqual(self.w["body_original_pdf_frames"], [690, 691])
        self.assertEqual(self.w["following_printed_CLIX_heading_pdf"], 691)
        self.assertEqual(
            [x["printed_folio"] for x in self.w["images"].values()],
            ["656", "657", "658"],
        )

    def test_03_75_qualified_historical_records_consecutive(self):
        self.assertEqual(
            [x["record_number"] for x in self.r["rules"]],
            list(range(10658, 10733)),
        )
        self.assertEqual(len({x["id"] for x in self.r["rules"]}), 75)

    def test_04_six_groups_inverse_source_map(self):
        ids = []
        for src, reverse in zip(self.a["groups"], self.mapping["source_groups"], strict=True):
            self.assertEqual(src["source_span"], reverse["source_span"])
            self.assertEqual(src["original_pdf_frames"], reverse["original_pdf_frames"])
            children = [x["id"] for x in src["claims"]]
            self.assertEqual(children, reverse["mapped_record_ids"])
            ids.extend(children)
        self.assertEqual(ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(self.mapping["source_group_count"], 6)

    def test_05_separate_73_substantive_and_two_next_nav(self):
        self.assertEqual(self.r["substantive"], 73)
        self.assertEqual(
            [x["id"] for x in self.r["rules"] if x["role"] == "next_navigation"],
            ["R10731", "R10732"],
        )

    def test_06_five_hylegiacal_heading_not_every_planet_in_CLVIII(self):
        self.one("heading", "five_places", "promittors", "asc_body_saturn")

    def test_07_Saturn_body_bodily_humoral_outcomes_are_historical(self):
        self.one(
            "saturn_body_unhealthy",
            "cold_dry",
            "phlegm",
            "coughs",
            "quartan_agues",
            "double_tertian",
        )

    def test_08_no_real_neurology_psychology_from_original_claims(self):
        self.one(
            "brain_involution",
            "giddiness",
            "mind_perturbation",
            "chimeras",
            "stupidity",
            "lazy_careless",
        )

    def test_09_old_gender_and_youth_diseases_separate(self):
        self.one(
            "long_sickness", "wasting", "girls_green_sickness", "youth_consumption", "lethargy"
        )

    def test_10_water_danger_requires_two_specific_qualifiers(self):
        self.one("watery_sign", "near_violent_stars", "water_danger")
        self.assertFalse(self.guard["mathematical_aspects_or_stellar_parity_verified"])

    def test_11_Saturn_sextile_or_trine_not_same_as_body(self):
        self.one("saturn_sextile", "saturn_trine", "grave_sober", "aged_men")

    def test_12_social_reputation_not_same_as_financial_wealth(self):
        self.one("reputation_not_profit", "stable_goods")

    def test_13_farm_building_gardening_rural_trade_are_alternatives(self):
        self.one("husbandry", "buildings", "orchards", "country_affairs", "land_lease")

    def test_14_aged_patron_vs_rent_mines_conditional(self):
        self.one(
            "farmers_laborers",
            "aged_legacy",
            "gentleman_leases",
            "renew_advantage",
            "mine_discovery",
        )

    def test_15_decision_making_child_parent_are_separate(self):
        self.one("settled_discretion", "children_obey")

    def test_16_three_adverse_Saturn_aspects_exclusive_source_branches(self):
        self.one("saturn_square", "saturn_opposition", "terms_saturn")

    def test_17_high_stakes_mortality_claim_has_extra_prerequisites(self):
        self.one("other_malefics_agree", "saturn_anareta", "death_danger")
        self.assertFalse(self.guard["original_anareta_selection_verified"])

    def test_18_old_chronic_medical_claims_not_diagnosis(self):
        self.one(
            "cold_dry_diseases",
            "former_griefs",
            "spleen_pain",
            "wind_cholic",
            "rupture_guts",
            "gonorrhoea",
            "gouts",
        )

    def test_19_body_parts_and_disease_named_separately(self):
        self.one("nose_polyps", "fistula", "tumours", "genital_hurt")

    def test_20_negative_year_delay_status_vs_character_different(self):
        self.one(
            "sorrow_year",
            "elders_vexation",
            "actions_delayed",
            "lose_office",
            "slow_dull",
            "speech_little",
            "reserved",
            "envy_malice",
            "washpish",
        )

    def test_21_four_elements_modify_humors_distinctly(self):
        self.one("sign_modifier", "fiery_dry", "watery_moist", "airy_blood", "earthly_melancholy")

    def test_22_next_CLIX_is_Jupiter_and_not_Saturn(self):
        self.assertEqual(self.accept["next_printed"], "CLIX")
        self.assertEqual(self.accept["next_pdf"], 691)
        self.assertFalse(self.r["full_primary_direction_geometry"])

    def test_23_real_person_health_mortality_accuracy_is_zero(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        self.assertFalse(self.lim["individual_mortality_or_clinical_claim_authorized"])
        for row in self.r["rules"]:
            for key in (
                "real_person_health_or_clinical_accuracy_validated",
                "real_person_mortality_or_danger_accuracy_validated",
                "real_person_cognition_character_or_morality_validated",
                "real_person_property_or_business_success_validated",
                "historical_direction_anareta_orb_geometry_verified",
                "individual_diagnostic_or_mortality_prediction_authorized",
                "runtime_model_promoted",
            ):
                self.assertFalse(row[key], (row["id"], key))

    def test_24_guard_and_competing_historical_source_no_computation(self):
        self.assertFalse(self.lim["source_directions_and_fixed_stars_computationally_verified"])
        self.assertEqual(self.guard["real_human_medical_accuracy_validated"], 0)
        self.assertEqual(self.guard["real_human_mortality_predictions_validated"], 0)

    def test_25_acceptance_hashes_and_corpus_math(self):
        self.assertEqual(self.accept["prior_lilly"], 10657)
        self.assertEqual(self.accept["lilly_if_published"], 10732)
        self.assertEqual(self.accept["combined_if_published"], 11798)
        self.assertEqual(self.accept["new_numbered_chapters"], 1)
        for file, key in (
            ("RULES.json", "rules_sha256"),
            ("SOURCE_FIRST_AUTHORING_20261018.json", "authoring_sha256"),
            ("CLVIII_SATURN_HISTORICAL_NONPROMOTION_GUARD_V1.json", "guard_sha256"),
        ):
            self.assertEqual(
                hashlib.sha256((B / file).read_bytes()).hexdigest(),
                self.accept[key],
            )


if __name__ == "__main__":
    unittest.main()
