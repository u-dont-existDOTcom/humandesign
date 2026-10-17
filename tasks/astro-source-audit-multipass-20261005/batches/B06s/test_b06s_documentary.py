"""Original Lilly 1647 CXXXIX travel source documentary checks, not travel forecasting."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def read(n):
    return json.loads((B / n).read_text(encoding="utf-8"))


class TravelSource1647Original(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = read("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.r = read("RULES.json")
        cls.m = read("SOURCE_TO_RECORD_MAP.json")
        cls.w = read("ORIGINAL_SOURCE_WITNESS.json")
        cls.methods = read("TRAVEL_QUARTER_HISTORICAL_METHODS_V1.json")
        cls.limits = read("UNRESOLVED_SOURCE_LIMITS.json")
        cls.acc = read("ACCEPTANCE.json")
        cls.roles = Counter(x["role"] for x in cls.r["rules"])
        cls.text = " ".join(x["anchor_not_diplomatic"] for x in cls.r["rules"])

    def one(self, *roles):
        for role in roles:
            self.assertEqual(self.roles[role], 1, role)

    def test_01_original_source_photo_sha256_and_bytes(self):
        self.assertEqual(list(self.w["images"]), ["640", "641", "642", "643"])
        for v in self.w["images"].values():
            raw = (B / v["path"]).read_bytes()
            self.assertEqual(raw[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(raw), v["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), v["sha256"])

    def test_02_original_pdf_folio_next_chapter_boundary(self):
        self.assertEqual(self.w["body_original_pdf_frames"], [640, 641, 642])
        self.assertEqual(self.w["following_printed_CXL_heading_pdf"], 643)
        self.assertEqual(
            [x["printed_folio"] for x in self.w["images"].values()], ["606", "607", "608", "609"]
        )

    def test_03_exact_record_ids_and_unique(self):
        self.assertEqual([r["record_number"] for r in self.r["rules"]], list(range(8706, 8807)))
        self.assertEqual(len(set(r["id"] for r in self.r["rules"])), 101)

    def test_04_eleven_photo_group_source_to_record_inverse(self):
        ids = []
        for a, inv in zip(self.a["groups"], self.m["groups"], strict=True):
            self.assertEqual(a["source_span"], inv["source_span"])
            self.assertEqual(a["original_pdf_frames"], inv["original_pdf_frames"])
            these = [r["id"] for r in a["clauses"]]
            self.assertEqual(inv["mapped_record_ids"], these)
            ids.extend(these)
        self.assertEqual(ids, [r["id"] for r in self.r["rules"]])
        self.assertEqual(self.m["source_group_count"], 11)

    def test_05_records_99_substantive_two_heading_navigation(self):
        self.assertEqual(self.r["substantive"], 99)
        self.assertEqual(self.r["following_numbered_navigation"], 2)
        self.assertEqual(self.acc["numbered_chapters_added"], 1)

    def test_06_priority_moon_mercury_and_original_uncertain_glyph(self):
        self.one(
            "all_significators",
            "especially_moon",
            "especially_mercury",
            "mutual_reception",
            "uncertain_aspect",
        )
        row = next(r for r in self.r["rules"] if r["role"] == "uncertain_aspect")
        self.assertEqual(row["qualification"], "glyph-unresolved")

    def test_07_reception_or_conjunction_two_ruler_alternatives(self):
        self.one(
            "reception_lord_ninth", "reception_lord_first", "conj_lord_ninth", "conj_lord_first"
        )

    def test_08_house_occupancy_vs_house_dignity_and_rulers(self):
        self.one(
            "travel_house_ninth",
            "travel_house_third",
            "travel_house_first",
            "travel_dignities",
            "ninth_lord_first",
            "first_lord_ninth",
            "first_ninth_conjunction",
        )

    def test_09_sun_moon_mercury_contact_and_dignity(self):
        self.one(
            "sun_moon_house",
            "sun_mercury_house",
            "sun_reception_moon",
            "sun_reception_mercury",
            "essential_dignity",
            "sun_conj_mercury",
            "sun_conj_moon",
            "sun_conj_both",
            "sun_travel_result",
        )

    def test_10_movable_sources_vs_fixed_outcomes_and_propensity(self):
        self.one(
            "many_movable",
            "stir_mind",
            "movable_travel",
            "travel_profit_speed",
            "fixed_travel",
            "long_stay",
            "little_profit",
        )

    def test_11_moon_mercury_domicile_reciprocity(self):
        self.one("mercury_moon_house", "moon_mercury_house")

    def test_12_few_many_none_travel_and_western_moon_branch(self):
        self.one(
            "many_positive",
            "journeys_more",
            "few_positive",
            "journeys_few",
            "occidental_planets",
            "moon_occidental",
            "many_by_occidental",
            "absence_all",
            "no_desire_foreign",
            "stay_country",
        )

    def test_13_destination_requires_travel_first(self):
        self.one(
            "direction_heading",
            "travel_first",
            "destination_part",
            "planet_source",
            "sign_source",
            "native_country_reference",
        )

    def test_14_sun_saturn_east_venus_south_jupiter_north_mars_moon_west(self):
        self.one(
            "sun_east", "saturn_east", "venus_south", "jupiter_north", "mars_west", "moon_west"
        )
        m = self.methods["source_methods"][0]["directions"]
        self.assertEqual(
            {x: m[x] for x in ("Sun", "Saturn", "Venus", "Jupiter", "Mars", "Moon")},
            {
                "Sun": "East",
                "Saturn": "East",
                "Venus": "South",
                "Jupiter": "North",
                "Mars": "West",
                "Moon": "West",
            },
        )

    def test_15_mercury_direction_may_be_no_forecast(self):
        self.one("mercury_conditional", "mercury_solar_lunar_conj", "mercury_weak", "mercury_none")

    def test_16_fire_air_earth_water_compass_and_signs(self):
        self.one(
            "triplicity_heading",
            "fire_signs",
            "fire_east",
            "air_signs",
            "air_west",
            "earth_signs",
            "earth_south",
            "water_signs",
            "water_north",
        )
        m = self.methods["source_methods"][1]
        self.assertEqual(
            m["directions"], {"Fire": "East", "Air": "West", "Earth": "South", "Water": "North"}
        )

    def test_17_ptolemy_method_explicitly_non_equivalent(self):
        self.one("ptolemy_direction", "other_author_disagreement")
        self.assertFalse(self.limits["original_ptolemy_travel_source_collated"])

    def test_18_ptolemy_house_groups_oriental_east_vs_west(self):
        self.one(
            "ptolemy_oriental",
            "ptolemy_east_southeast",
            "ptolemy_occidental",
            "ptolemy_west_north",
            "east_house_group",
            "west_house_group",
        )
        m = self.methods["source_methods"][2]
        self.assertEqual(m["house_groups"]["Oriental"], [10, 11, 12, 1, 2, 3])
        self.assertEqual(m["house_groups"]["Occidental"], [9, 8, 7, 6, 5, 4])

    def test_19_mars_moon_north_south_latitude_strong_and_majority(self):
        self.one(
            "lat_planets",
            "lat_strong",
            "north_lat",
            "travel_north",
            "south_lat",
            "travel_south",
            "collect_in_order",
            "majority_final",
        )

    def test_20_mode_land_water_signs_not_unique(self):
        self.one(
            "mode_heading",
            "majority_mode",
            "fire_earth_land",
            "land_result",
            "water_air_mode",
            "water_result",
            "mixed_water_land",
        )

    def test_21_horse_coach_foot_are_17th_century_categories(self):
        self.one("four_footed_sign", "horse_coach", "humane_sign", "travel_foot")
        self.assertIn("Horse and Coach", self.text)

    def test_22_seven_historical_methods_are_distinct_from_human_evidence(self):
        self.assertEqual(len(self.methods["source_methods"]), 7)
        self.assertEqual(self.methods["human_travel_predictions_verified"], 0)
        self.assertFalse(
            self.methods["source_methods"][4]["class"] == "deterministic-calibrated-probability"
        )

    def test_23_unresolved_majority_and_null_after_conflicts(self):
        self.one("majority_testimonies", "majority_final")
        self.assertFalse(self.limits["complete_travel_direction_engine"])
        self.assertIn("ties", " ".join(self.limits["issues"]))

    def test_24_next_printed_cxl_causes_separate(self):
        self.assertEqual(
            [r["id"] for r in self.r["rules"] if r["role"] == "next_chapter_navigation"],
            ["R8805", "R8806"],
        )
        self.assertEqual(self.acc["next_printed_chapter"], "CXL")
        self.assertEqual(self.acc["next_original_pdf_frame"], 643)

    def test_25_no_real_travel_geo_income_life_risk_faith_predictions(self):
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        self.assertFalse(
            self.limits["person_geography_profit_faith_or_life_risk_predictions_authorized"]
        )
        for r in self.r["rules"]:
            for key in (
                "independent_travel_occurrence_frequency_validated",
                "independent_travel_destination_geography_validated",
                "independent_travel_duration_profit_or_mode_validated",
                "independent_travel_life_hazard_validated",
                "real_person_travel_wealth_or_religion_inference_authorized",
                "source_math_directed_compass_executable",
                "original_ptolemy_source_collated",
                "runtime_model_promoted",
            ):
                self.assertFalse(r[key], (r["id"], key))

    def test_26_corpus_and_method_sha256(self):
        self.assertEqual(self.acc["previous_lilly"], 8705)
        self.assertEqual(self.acc["lilly_if_published"], 8806)
        self.assertEqual(self.acc["combined_if_published"], 9872)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.acc["rules_sha256"],
        )
        self.assertEqual(
            hashlib.sha256(
                (B / "TRAVEL_QUARTER_HISTORICAL_METHODS_V1.json").read_bytes()
            ).hexdigest(),
            self.acc["direction_method_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
