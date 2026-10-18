"""Original Lilly 1647 travel-success source documents, NOT safety predictions."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


class OriginalTravelSuccessSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = read("SOURCE_FIRST_AUTHORING_20261018.json")
        cls.r = read("RULES.json")
        cls.w = read("ORIGINAL_SOURCE_WITNESS.json")
        cls.m = read("SOURCE_TO_RECORD_MAP.json")
        cls.limits = read("UNRESOLVED_SOURCE_LIMITS.json")
        cls.acc = read("ACCEPTANCE.json")
        cls.roles = Counter(row["role"] for row in cls.r["rules"])
        cls.text = " ".join(row["source_anchor_not_diplomatic"] for row in cls.r["rules"])

    def one(self, *names):
        for name in names:
            self.assertEqual(self.roles[name], 1, name)

    def test_01_original_photo_bytes_and_sha256(self):
        self.assertEqual(list(self.w["original_source_images"]), [str(n) for n in range(644, 649)])
        for info in self.w["original_source_images"].values():
            data = (B / info["file"]).read_bytes()
            self.assertEqual(data[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(data), info["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), info["sha256"])

    def test_02_original_boundaries_printed_CXLI_then_CXLII(self):
        self.assertEqual(self.w["body_pdf_frames"], [644, 645])
        self.assertEqual(self.w["following_printed_CXLII_heading_frame"], 645)
        self.assertEqual(
            [x["printed_folio"] for x in self.w["original_source_images"].values()],
            ["610", "611", "612", "613", "614"],
        )

    def test_03_original_76_records_ordering(self):
        self.assertEqual(
            [x["record_number"] for x in self.r["rules"]],
            list(range(8860, 8936)),
        )
        self.assertEqual(len({x["id"] for x in self.r["rules"]}), 76)

    def test_04_six_source_passages_bidirectional_mapping(self):
        ids = []
        for a, inv in zip(self.a["groups"], self.m["source_groups"], strict=True):
            self.assertEqual(a["source_span"], inv["source_span"])
            self.assertEqual(a["original_pdf_frames"], inv["original_pdf_frames"])
            refs = [c["id"] for c in a["clauses"]]
            self.assertEqual(refs, inv["mapped_record_ids"])
            ids.extend(refs)
        self.assertEqual(ids, [x["id"] for x in self.r["rules"]])
        self.assertEqual(self.m["source_group_count"], 6)

    def test_05_positive_signifier_power_or_benefic_or_domicile(self):
        self.one("eligible_significators", "benefic_aspect", "domicile")

    def test_06_safe_travel_vs_profit_friendships_honors_distinct(self):
        self.one("safe_travel", "prosperity", "friendships", "honors", "class_relative")

    def test_07_negative_signifier_weak_or_malefic_and_house(self):
        self.one("weak_significators", "malefic_aspect", "malefic_domicile", "difficult_journey")

    def test_08_house_sign_mars_saturn_all_qualified(self):
        self.one(
            "saturn_mars",
            "malefic_sign",
            "afflict_traveler",
            "elevated",
            "lords_signifier_house",
            "house_sign_matters",
        )

    def test_09_twelfth_imprisonment_third_thieves_and_treachery(self):
        self.one("twelfth_prison", "third_family_betrayal", "third_thieves")

    def test_10_saturn_poverty_distinct_from_mars_harm(self):
        self.one("saturn_poverty", "mars_thieves_soldiers")

    def test_11_moist_sign_weather_water_isolation_differ(self):
        self.one("moist_signs", "moist_showers", "moist_water", "moist_solitary")

    def test_12_fixed_Saturn_has_scoprio_explicit_exception(self):
        self.one("saturn_fixed", "scorpio_except", "fixed_falls", "fixed_winds")
        self.assertIn("except Scorpio", self.text)

    def test_13_movable_thunder_lightning_air_conditions(self):
        self.one("movable_signs", "movable_lightning", "movable_air")

    def test_14_humane_sign_theft_not_actual_crime(self):
        self.one("humane_signs", "humane_thieves")

    def test_15_bestial_sign_animal_earthquake_building(self):
        self.one("bestial_signs", "bestial_beasts", "bestial_falls", "bestial_buildings")

    def test_16_separate_Scorpio_flux_or_poison_conditions(self):
        self.one("scorpio_flux", "scorpio_poison")

    def test_17_drowning_requires_compound_water_malefics_fixed_stars(self):
        self.one("water_signs", "watery_malefics", "fixed_stars_violent", "drowning")

    def test_18_slain_when_Saturn_with_ninth_lord_twelve_vs_robbed(self):
        self.one("saturn_ninth_lord_twelve", "slain_travel", "lord_ninth_saturn_house", "robbery")

    def test_19_beneficial_regions_four_separate_houses(self):
        self.one(
            "subheading",
            "geography_basis",
            "first_house",
            "tenth_house",
            "eleventh_house",
            "second_house",
        )

    def test_20_Jupiter_Venus_plus_unresolved_positive_glyph(self):
        self.one("jupiter_sign", "venus_sign", "positive_glyph", "positive_regions")
        self.assertFalse(self.limits["original_node_heraldic_glyphs_fully_verified"])

    def test_21_bad_regions_all_four_houses_and_malefic_modifier(self):
        self.one(
            "malefic_place",
            "malefic_afflict",
            "seventh_sign",
            "sixth_sign",
            "eighth_sign",
            "fourth_sign",
            "infortune_possesses",
            "no_benefic_aspect",
        )

    def test_22_further_adverse_ruler_list_not_neutral_claim(self):
        self.one("node_malefic_ambig", "bad_house_lords", "avoid_countries")

    def test_23_printed_part_one_geography_table_not_imported(self):
        self.one("part1_crossref", "printed_p93")
        self.assertFalse(self.limits["geographical_zodiac_country_table_p93_verified"])
        self.assertIn("page 93", self.text)

    def test_24_following_religion_chapter_separate(self):
        self.assertEqual(
            [r["id"] for r in self.r["rules"] if r["role"] == "next_chapter_navigation"],
            ["R8934", "R8935"],
        )
        self.assertEqual(self.acc["next_printed_chapter"], "CXLII")
        self.assertEqual(self.acc["next_original_pdf"], 645)
        self.assertEqual(self.r["substantive"], 74)

    def test_25_zero_real_person_hazard_health_geography_validation(self):
        self.assertFalse(self.limits["person_travel_safety_or_criminality_forecasts_authorized"])
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        for x in self.r["rules"]:
            for key in (
                "real_travel_success_or_profit_validated",
                "real_travel_hazard_crime_or_death_validated",
                "real_favorable_country_location_validated",
                "historical_p93_country_table_verified",
                "person_level_travel_medical_or_safety_advice_authorized",
                "real_person_criminality_or_religion_inference_authorized",
                "runtime_model_promoted",
            ):
                self.assertFalse(x[key], (x["id"], key))

    def test_26_source_hash_and_new_corpus_total(self):
        self.assertEqual(self.acc["prior_lilly"], 8859)
        self.assertEqual(self.acc["lilly_if_published"], 8935)
        self.assertEqual(self.acc["combined_if_published"], 10001)
        self.assertEqual(self.acc["numbered_chapters_added"], 1)
        self.assertEqual(
            hashlib.sha256((B / "RULES.json").read_bytes()).hexdigest(),
            self.acc["rules_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
