"""Lilly 1647 CXV original documentary source and classification coverage.

A green test means faithful structural source preservation, not economic validity.
"""

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


class OriginalCausesOfEstate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = j("RULES.json")
        cls.logic = j("SOURCE_FIRST_LOGIC_AUTHORING_20261017.json")
        cls.matrix = j("SOURCE_FIRST_CLASSIFICATION_MATRIX_20261017.json")
        cls.mapping = j("SOURCE_TO_RECORD_MAP.json")
        cls.images = j("ORIGINAL_SOURCE_WITNESS.json")
        cls.issues = j("UNRESOLVED_SOURCE_LIMITS.json")
        cls.accept = j("ACCEPTANCE.json")
        cls.rows = cls.rules["rules"]
        cls.roles = Counter(x["role"] for x in cls.rows)

    def test_01_all_original_first_edition_page_hashes(self):
        self.assertEqual(list(self.images["images"]), [str(n) for n in range(588, 597)])
        for image in self.images["images"].values():
            file = B / image["file"]
            data = file.read_bytes()
            self.assertEqual(data[:2], bytes.fromhex("ffd8"))
            self.assertEqual(len(data), image["bytes"])
            self.assertEqual(sha(file), image["sha256"])

    def test_02_pagination_original_duplicate_561_no_reordering(self):
        actual = [x["original_printed_folio"] for x in self.images["images"].values()]
        self.assertEqual(actual, ["554", "555", "556", "557", "558", "559", "561", "561", "562"])
        self.assertIn("duplicated folio", self.images["folio_note"])

    def test_03_original_body_and_following_numbered_heading(self):
        self.assertEqual(self.images["original_chapter_pdf_frames"], list(range(588, 595)))
        self.assertEqual(self.images["following_printed_chapter_CXVI_heading_pdf"], 594)
        self.assertEqual(self.rules["next_heading_frame"], 594)

    def test_04_records_contiguous_order(self):
        self.assertEqual([r["record_number"] for r in self.rows], list(range(6911, 6995)))
        self.assertEqual(len(set(r["id"] for r in self.rows)), 84)

    def test_05_reverse_source_map_one_to_one_coverage(self):
        self.assertEqual(self.mapping["record_count"], 84)
        self.assertEqual(
            [r["id"] for r in self.rows],
            [r["record_id"] for r in self.mapping["source_groups"]],
        )
        self.assertEqual(len(set(r["source_span"] for r in self.rows)), 84)

    def test_06_logic_claims_all_map_to_own_records(self):
        authored = {c["id"] for g in self.logic["groups"] for c in g["claims"]}
        actual = {
            r["source_metadata"]["authoring_claim_id"]
            for r in self.rows
            if r["source_metadata"].get("authoring_claim_id")
        }
        self.assertEqual(authored, actual)
        self.assertEqual(len(authored), 48)

    def test_07_all_seven_planets_have_two_separate_cells(self):
        self.assertEqual(
            [p["name"] for p in self.matrix["planets"]],
            ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"],
        )
        self.assertEqual(self.roles["planet_matters_cell"], 7)
        self.assertEqual(self.roles["planet_persons_cell"], 7)
        for planet in self.matrix["planets"]:
            rows = [x for x in self.rows if x["source_metadata"].get("planet") == planet["name"]]
            self.assertEqual(len(rows), 2)
            self.assertEqual(
                {x["source_metadata"]["cell_type"] for x in rows},
                {"matters", "persons"},
            )

    def test_08_source_items_all_316_accounted_for(self):
        self.assertEqual(sum(r["source_item_count"] for r in self.rows), 316)
        self.assertEqual(self.rules["source_normalized_items"], 316)
        self.assertEqual(self.mapping["normalized_item_count"], 316)
        self.assertEqual(self.accept["normalized_cell_items"], 316)

    def test_09_planet_matters_and_persons_185_items(self):
        rows = [
            r for r in self.rows if r["role"].startswith("planet_") and r["role"].endswith("_cell")
        ]
        self.assertEqual(len(rows), 14)
        self.assertEqual(sum(x["source_item_count"] for x in rows), 185)

    def test_10_each_cell_has_no_internal_duplicate_term(self):
        for row in self.rows:
            entries = row["source_items_normalized_not_diplomatic"]
            self.assertEqual(len(entries), len(set(entries)))
            self.assertEqual(len(entries), row["source_item_count"])

    def test_11_source_matters_persons_sensitive_claims_not_predictive(self):
        for row in self.rows:
            self.assertFalse(row["validated_person_occupational_or_moral_inference"])
            self.assertFalse(row["clinical_or_economic_action_authorized"])

    def test_12_four_elemental_sign_source_groups(self):
        self.assertEqual(self.roles["zodiac_element_cell"], 4)
        self.assertEqual(
            [row["name"] for row in self.matrix["elements"]],
            ["fiery", "earthly", "airy", "watery"],
        )
        self.assertEqual(
            sum(x["source_item_count"] for x in self.rows if x["role"] == "zodiac_element_cell"), 9
        )

    def test_13_six_planetary_sign_nature_categories_not_seven(self):
        self.assertEqual(self.roles["planetary_sign_nature_cell"], 6)
        self.assertEqual(
            [r["name"] for r in self.matrix["planetary_natures"]],
            ["saturnine", "jovial", "martial", "solar", "venereal", "mercurial"],
        )
        self.assertEqual(
            sum(
                x["source_item_count"]
                for x in self.rows
                if x["role"] == "planetary_sign_nature_cell"
            ),
            17,
        )

    def test_14_all_twelve_houses_in_original_sequence(self):
        self.assertEqual(self.roles["house_classification_cell"], 12)
        houses = [
            row["source_metadata"]["house"]
            for row in self.rows
            if row["role"] == "house_classification_cell"
        ]
        self.assertEqual(houses, list(range(1, 13)))

    def test_15_house_matrix_105_normalized_terms(self):
        self.assertEqual(
            sum(
                r["source_item_count"]
                for r in self.rows
                if r["role"] == "house_classification_cell"
            ),
            105,
        )

    def test_16_own_industry_not_identical_to_all_second_house_sources(self):
        houses = {x["no"]: x["items"] for x in self.matrix["houses"]}
        self.assertIn("wealth acquired through the native's own industry", houses[1])
        self.assertIn("gain from the native's own labor", houses[2])
        self.assertIn("household goods", houses[2])

    def test_17_third_fourth_eighth_specific_sources(self):
        houses = {x["no"]: x["items"] for x in self.matrix["houses"]}
        self.assertIn("brothers", houses[3])
        self.assertIn("concealed treasure", houses[4])
        self.assertIn("unexpected inheritances", houses[8])

    def test_18_tenth_eleventh_twelfth_sources_preserved(self):
        houses = {x["no"]: x["items"] for x in self.matrix["houses"]}
        self.assertIn("native's vocation", houses[10])
        self.assertIn("promotion through commendation of friends", houses[11])
        self.assertIn("private enemies", houses[12])

    def test_19_four_method_dimensions_and_matrix_headings(self):
        self.assertEqual(self.roles["method_dimension"], 4)
        self.assertEqual(self.roles["matrix_heading"], 3)
        text = " ".join(r["original_anchor_not_diplomatic"] or "" for r in self.rows)
        for word in ("First", "Secondly", "Thirdly", "Fourthly"):
            self.assertIn(word, text)

    def test_20_fortitude_comparison_precedes_source_assignment(self):
        self.assertEqual(self.roles["first_evidence_check"], 1)
        self.assertEqual(self.roles["testimony_count"], 1)
        self.assertEqual(self.roles["testimony_comparison"], 1)

    def test_21_all_strong_case_explicitly_rare(self):
        self.assertEqual(self.roles["all_strong_case"], 1)
        self.assertEqual(self.roles["all_strong_exception"], 1)
        text = " ".join(x["original_anchor_not_diplomatic"] or "" for x in self.rows)
        self.assertIn("seldome", text)

    def test_22_mostly_strong_still_has_specific_loss(self):
        self.assertEqual(self.roles["majority_strong_case"], 1)
        self.assertEqual(self.roles["mixed_loss_method"], 2)
        self.assertEqual(self.roles["mixed_outcome_exception"], 1)
        self.assertEqual(self.roles["illustrative_example"], 1)
        self.assertEqual(self.roles["illustrative_interpretation"], 1)

    def test_23_mostly_weak_still_has_temporary_gain(self):
        self.assertEqual(self.roles["majority_weak_case"], 1)
        self.assertEqual(self.roles["majority_weak_exception"], 1)
        self.assertEqual(self.roles["majority_weak_outcome"], 1)

    def test_24_equal_strong_weak_has_fluctuations_and_origin_baseline(self):
        self.assertEqual(self.roles["equal_strength_case"], 1)
        self.assertEqual(self.roles["equal_strength_dynamic"], 1)
        self.assertEqual(self.roles["ancestor_condition"], 1)
        self.assertEqual(self.roles["individual_behavior"], 1)

    def test_25_do_not_count_CXVI_as_CXV_historic_body(self):
        nav = [r for r in self.rows if r["role"] == "next_chapter_navigation"]
        self.assertEqual([r["id"] for r in nav], ["R6993", "R6994"])
        self.assertEqual(self.rules["next_chapter_navigation_units"], 2)

    def test_26_not_diplomatic_and_historical_only(self):
        self.assertFalse(self.rules["original_diplomatic_transcription"])
        self.assertTrue(self.issues["historical_only"])
        self.assertGreaterEqual(len(self.issues["issues"]), 13)

    def test_27_no_independent_financial_validations_or_runtime(self):
        self.assertEqual(self.rules["empirical_validations"], 0)
        self.assertEqual(self.rules["independently_verified_wealth_outcomes"], 0)
        self.assertEqual(self.rules["runtime_promotions"], 0)
        for row in self.rows:
            self.assertFalse(row["independently_validated_human_financial_result"])
            self.assertFalse(row["promoted_as_executable_runtime_rule"])

    def test_28_exact_rules_sha_and_corpus_arithmetic(self):
        self.assertEqual(sha(B / "RULES.json"), self.accept["rules_sha256"])
        self.assertEqual(self.accept["previous_lilly"], 6910)
        self.assertEqual(self.accept["lilly_if_published"], 6994)
        self.assertEqual(self.accept["combined_if_published"], 8060)
        self.assertEqual(self.accept["structured_source_cells"], 36)


if __name__ == "__main__":
    unittest.main()
