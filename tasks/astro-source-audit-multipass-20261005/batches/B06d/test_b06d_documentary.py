"""Original 1647 sixth-house medical taxonomy DOCUMENTARY integrity, not clinical tests."""

import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class SixthHouseFirstEditionDocumentation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = j("SOURCE_FIRST_AUTHORING_20261017.json")
        cls.tables = j("ORIGINAL_1647_PLANET_SIGN_MEDICAL_TABLES_20261017.json")
        cls.r = j("RULES.json")
        cls.m = j("SOURCE_TO_RECORD_MAP.json")
        cls.w = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.limits = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.acc = j("ACCEPTANCE.json")
        cls.roles = Counter(row["role"] for row in cls.r["rules"])
        cls.anchors = " ".join(
            row.get("original_anchor_not_diplomatic", "") for row in cls.r["rules"]
        )

    def test_01_sha256_and_file_bytes_all_original_image_witnesses(self):
        self.assertEqual(list(self.w["images"]), [str(n) for n in range(610, 617)])
        for row in self.w["images"].values():
            path = B / row["file"]
            self.assertEqual(sha(path), row["sha256"])
            self.assertEqual(path.stat().st_size, row["bytes"])
            self.assertEqual(path.read_bytes()[:2], bytes.fromhex("ffd8"))

    def test_02_original_printed_folios_and_new_chapter_boundary(self):
        self.assertEqual(
            [x["printed_folio"] for x in self.w["images"].values()],
            ["576", "577", "578", "579", "580", "581", "582"],
        )
        self.assertEqual(self.w["source_body_original_frames"], [610, 611, 612, 613, 614, 615])
        self.assertEqual(self.w["next_printed_CHAP_CXXVIII_begin_frame"], 615)

    def test_03_exact_append_only_112_record_ids(self):
        self.assertEqual(
            [r["record_number"] for r in self.r["rules"]],
            list(range(7584, 7696)),
        )
        self.assertEqual(self.r["record_count"], 112)
        self.assertEqual(len({r["id"] for r in self.r["rules"]}), 112)

    def test_04_all_reversible_source_groups_and_unique_records(self):
        refs = []
        for group in self.m["source_groups"]:
            self.assertTrue(group["source_span"])
            self.assertTrue(group["original_pdf_frames"])
            refs.extend(group["mapped_record_ids"])
        self.assertEqual(refs, [r["id"] for r in self.r["rules"]])
        self.assertEqual(len(refs), len(set(refs)))
        self.assertEqual(self.m["source_group_count"], 27)

    def test_05_eight_prose_groups_and_last_nav_after_tables(self):
        self.assertEqual(len(self.a["prose_groups"]), 8)
        self.assertEqual(self.m["original_prose_passage_groups"], 8)
        self.assertEqual(
            [r["id"] for r in self.r["rules"] if r["role"] == "next_chapter_navigation"],
            ["R7694", "R7695"],
        )
        self.assertEqual(self.r["substantive_source_annotations"], 110)

    def test_06_five_health_significator_classes(self):
        self.assertEqual(self.roles["significator"], 6)
        for t in (
            "Signe ascending",
            "Sun and Moon",
            "sixt house",
            "Planets in the sixt",
            "seventh house",
        ):
            self.assertIn(t, self.anchors)

    def test_07_three_source_criteria_not_single_test(self):
        self.assertEqual(self.roles["three_considerations"], 1)
        self.assertGreaterEqual(self.roles["criterion"], 5)
        for t in (
            "strong or weak",
            "fixed Stars of ill influence",
            "Saturn and Mars",
            "Temperament equall",
        ):
            self.assertIn(t, self.anchors)

    def test_08_majority_strong_with_fixed_star_malefic_exceptions(self):
        self.assertEqual(self.roles["strong_majority"], 1)
        self.assertEqual(self.roles["strong_exception"], 2)
        self.assertEqual(self.roles["strong_result"], 1)
        self.assertEqual(self.roles["weak_majority"], 1)
        self.assertEqual(self.roles["weak_result"], 1)

    def test_09_luminary_humoral_language_not_anatomy(self):
        self.assertEqual(self.roles["humoral"], 2)
        self.assertEqual(self.roles["fortune_rising"], 1)
        self.assertEqual(self.roles["moon_strong"], 1)
        self.assertIn("humours", self.anchors)

    def test_10_all_four_elemental_humor_aphorisms(self):
        for role in (
            "triplicity_water",
            "triplicity_earth",
            "triplicity_fire",
            "triplicity_air",
        ):
            self.assertEqual(self.roles[role], 1)
        for term in ("Flegme", "Melancholly", "Choller", "Blood"):
            self.assertIn(term, self.anchors)

    def test_11_historical_health_negligence_stereotype_separate(self):
        self.assertEqual(self.roles["lord_application"], 1)
        self.assertEqual(self.roles["behavior_result"], 1)

    def test_12_sun_longevity_favorable_and_contrary(self):
        for role in (
            "sun_angle",
            "sun_cancer",
            "sun_long_result",
            "sun_other_houses",
            "sun_short_result",
        ):
            self.assertEqual(self.roles[role], 1)
        self.assertIn("sixt eighth seventh or twelfth", self.anchors)

    def test_13_sun_moon_aspect_glyph_unresolved(self):
        row = next(r for r in self.r["rules"] if r["role"] == "luminary_aspect")
        self.assertEqual(row["qualification"], "glyph-unresolved")

    def test_14_mars_saturn_specific_house_temperament_branches(self):
        for role in (
            "mars_sixth",
            "mars_twelfth",
            "mars_asc",
            "saturn_midheaven",
            "saturn_promotion",
        ):
            self.assertEqual(self.roles[role], 1)
        self.assertEqual(self.roles["malefic_phase"], 2)

    def test_15_author_vs_significator_medical_causation_kept_distinct(self):
        self.assertEqual(self.roles["author_vs_significator"], 1)
        self.assertEqual(self.roles["both_roles"], 2)
        self.assertEqual(self.roles["only_significator"], 2)
        self.assertEqual(self.roles["author_alone"], 1)
        self.assertEqual(self.roles["other_planets"], 1)

    def test_16_compounded_versus_single_affliction_and_exact_aspect(self):
        for role in (
            "doubly_afflicted",
            "double_stronger",
            "single_less",
            "partile_aspect",
            "planet_angular",
        ):
            self.assertEqual(self.roles[role], 1)

    def test_17_four_way_disease_type_horizon_and_house_cross_reference(self):
        self.assertEqual(self.roles["medical_axes"], 2)
        for role in (
            "disease_nature",
            "sign_of_significator",
            "nature_malefic",
            "sign_malefic",
            "above_horizon",
            "below_horizon",
            "every_house",
            "crossref_house",
            "combined_lookup",
        ):
            self.assertEqual(self.roles[role], 1)
        self.assertIn("pag. 245", self.anchors)

    def test_18_both_table_types_completely_separate_from_prose(self):
        self.assertEqual(self.roles["planet_body_region_cell"], 7)
        self.assertEqual(self.roles["planet_historic_ailment_cell"], 7)
        self.assertEqual(self.roles["zodiac_body_region_cell"], 12)
        self.assertEqual(sum(r["source_item_count"] > 0 for r in self.r["rules"]), 26)

    def test_19_all_seven_planets_in_original_source_order(self):
        rows = self.tables["planetary_rows"]
        self.assertEqual(
            [r["planet"] for r in rows],
            ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"],
        )
        self.assertEqual(self.m["planet_table_source_groups"], 7)

    def test_20_planet_anatomical_and_ailments_two_addressable_cells(self):
        for row in self.tables["planetary_rows"]:
            records = [x for x in self.r["rules"] if x.get("planet") == row["planet"]]
            self.assertEqual(len(records), 2)
            self.assertEqual(records[0]["source_list_items"], row["body"])
            self.assertEqual(records[1]["source_list_items"], row["ailments"])
            self.assertEqual(
                {x["role"] for x in records},
                {"planet_body_region_cell", "planet_historic_ailment_cell"},
            )

    def test_21_no_mercury_glyph_invented_and_jupiter_margin_uncertain(self):
        mercury = next(x for x in self.tables["planetary_rows"] if x["planet"] == "Mercury")
        jupiter = next(x for x in self.tables["planetary_rows"] if x["planet"] == "Jupiter")
        self.assertIn("uncertain", mercury["extra"].lower())
        self.assertIn("verification", jupiter["extra"].lower())

    def test_22_moon_eye_laterality_is_historical_and_explicit(self):
        row = next(x for x in self.tables["planetary_rows"] if x["planet"] == "Moon")
        self.assertIn("right eye of woman", row["body"])
        self.assertIn("left eye of man", row["body"])

    def test_23_all_twelve_zodiac_signs_exactly_once(self):
        signs = [
            "Aries",
            "Taurus",
            "Gemini",
            "Cancer",
            "Leo",
            "Virgo",
            "Libra",
            "Scorpio",
            "Sagittarius",
            "Capricorn",
            "Aquarius",
            "Pisces",
        ]
        self.assertEqual([r["name"] for r in self.tables["zodiac_rows"]], signs)
        self.assertEqual(
            [r["sign"] for r in self.r["rules"] if r["role"] == "zodiac_body_region_cell"],
            signs,
        )
        self.assertEqual(self.m["zodiac_sign_source_groups"], 12)

    def test_24_aries_mixes_specific_conditions_with_body_parts(self):
        aries = next(r for r in self.tables["zodiac_rows"] if r["name"] == "Aries")
        self.assertIn("head", aries["body"])
        self.assertIn("toothache", aries["conditions"])
        for row in self.tables["zodiac_rows"][1:]:
            self.assertFalse(row["conditions"])

    def test_25_anatomical_and_illness_terms_exact_total(self):
        self.assertEqual(
            sum(len(x["body"]) + len(x["ailments"]) for x in self.tables["planetary_rows"]),
            99,
        )
        self.assertEqual(
            sum(len(x["body"]) + len(x["conditions"]) for x in self.tables["zodiac_rows"]),
            51,
        )
        self.assertEqual(
            sum(x["source_item_count"] for x in self.r["rules"]),
            150,
        )

    def test_26_medical_claims_not_person_diagnoses(self):
        self.assertFalse(self.tables["medical_evidence"])
        self.assertFalse(self.tables["clinical_use_authorized"])
        self.assertEqual(self.r["empirical_validations"], 0)
        self.assertEqual(self.r["independent_human_health_forecasts_validated"], 0)
        self.assertEqual(self.r["runtime_promotions"], 0)
        self.assertFalse(self.limits["medical_or_treatment_inference_authorized"])
        for r in self.r["rules"]:
            self.assertFalse(r["independent_human_health_accuracy_validated"])
            self.assertFalse(r["actual_disease_cause_verified"])
            self.assertFalse(r["clinical_diagnosis_or_treatment_authorized"])
            self.assertFalse(r["runtime_model_promoted"])

    def test_27_next_eye_chapter_not_ingested(self):
        self.assertEqual(self.acc["next_printed_chapter"], "CXXVIII")
        self.assertEqual(self.acc["next_original_pdf_frame"], 615)
        self.assertEqual(self.acc["numbered_chapters_added"], 0)

    def test_28_source_matrix_and_authoring_hashes(self):
        self.assertEqual(sha(B / "RULES.json"), self.acc["rules_sha256"])
        self.assertEqual(
            sha(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
            self.acc["authoring_sha256"],
        )
        self.assertEqual(
            sha(B / "ORIGINAL_1647_PLANET_SIGN_MEDICAL_TABLES_20261017.json"),
            self.acc["source_matrix_sha256"],
        )

    def test_29_canonical_count_and_source_not_diplomatic(self):
        self.assertEqual(self.acc["previous_lilly"], 7583)
        self.assertEqual(self.acc["lilly_if_published"], 7695)
        self.assertEqual(self.acc["combined_if_published"], 8761)
        self.assertFalse(self.r["full_diplomatic_transcription"])
        self.assertGreaterEqual(len(self.limits["issues"]), 19)


if __name__ == "__main__":
    unittest.main()
