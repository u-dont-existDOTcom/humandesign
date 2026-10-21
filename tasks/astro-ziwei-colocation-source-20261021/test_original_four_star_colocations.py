"""Exact old Chinese source natal co-star grade text, not human trait testing."""

from __future__ import annotations

import json
import tempfile
import unittest
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch

import audit_original_four_star_colocations as subject

B = Path(__file__).resolve().parent
ROOT = B.parents[1]
DATA = B / "ORIGINAL_FOUR_BEHAVIOR_STAR_COLOCATION_SOURCE_AUDIT_V1.json"


def read(p):
    return json.loads(p.read_text(encoding="utf-8"))


def h(b):
    return sha256(b).hexdigest()


class SourceFourStarColocationTextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.output = read(DATA)
        cls.grade = cls.output["original_15_explicit_pair_grade_source_lines"]
        cls.clusters = cls.output["original_7_other_multistar_cluster_and_mitigation_source_lines"]
        cls.comparison = cls.output[
            "source_matching_against_120_synthetic_original_chart_positions"
        ]

    def test_01_immutable_full_original_Chinese_raw_index_and_source_map_SHA(self):
        self.assertEqual(h(subject.RAW.read_bytes()), subject.SOURCE_SHA)
        self.assertEqual(h(subject.INDEX.read_bytes()), subject.INDEX_SHA)
        self.assertEqual(h(subject.MAP.read_bytes()), subject.MAP_SHA)
        self.assertEqual(
            self.output["original_transmitted_SimplifiedChinese_revision_oldid"], 1963110
        )
        self.assertFalse(self.output["original_scholarly_critical_early_Ming_printing_verified"])
        self.assertEqual(
            [s["accepted_source_annotations"] for s in read(subject.INDEX)["systems"]], [210, 586]
        )

    def test_02_original_four_provisional_human_construct_fragments_not_validated(self):
        source = read(subject.MAP)
        self.assertEqual(
            {r["source_note_id"] for r in source["candidates"]},
            {"ZWD-R0287", "ZWD-R0330", "ZWD-R0464", "ZWD-R0505"},
        )
        self.assertTrue(
            all(not x["source_phrase_expert_translation_verified"] for x in source["candidates"])
        )
        self.assertFalse(source["score_probabilities_calibrated"])
        self.assertEqual(self.output["actual_consented_real_humans_tested"], 0)

    def test_03_fifteen_exact_original_natal_grade_line_notes_and_positions(self):
        self.assertEqual(len(self.grade), 15)
        self.assertEqual(
            [x["accepted_source_id"] for x in self.grade], [x[0] for x in subject.PAIR_RULES]
        )
        raw = subject.RAW.read_bytes()
        full = raw.decode("utf-8")
        for item in self.grade:
            original = item["verbatim_old_Chinese_line"]
            cp = item["source_original_line_codepoint_offset"]
            bytepos = item["source_original_line_UTF8_byte_offset"]
            b = original.encode("utf-8")
            self.assertEqual(full[cp : cp + len(original)], original)
            self.assertEqual(raw[bytepos : bytepos + len(b)], b)
            self.assertEqual(h(b), item["source_original_line_sha256"])
            self.assertEqual(
                h((ROOT / item["source_file_path"]).read_bytes()), item["source_file_sha256"]
            )
            self.assertEqual(item["source_full_original_Wikitext_sha256"], subject.SOURCE_SHA)

    def test_04_all_fifteen_grade_source_texts_explicit_same_palace(self):
        self.assertEqual(len(self.grade), 15)
        self.assertEqual(
            len({tuple(x["mechanical_unordered_principal_star_pair"]) for x in self.grade}), 13
        )
        for x in self.grade:
            self.assertIn(
                x["literal_old_chinese_co_location_fragment"], x["verbatim_old_Chinese_line"]
            )
            self.assertEqual(len(x["source_allowed_palaces_Earthly_roman"]), 2)
            self.assertTrue(
                all(
                    c in subject.CN_TO_ROMAN.values()
                    for c in x["source_allowed_palaces_Earthly_roman"]
                )
            )
            self.assertFalse(x["numerical_behavioral_trait_modifier_justified"])
            self.assertFalse(x["source_line_contains_exact_one_of_four_behavior_phrases"])

    def test_05_recipient_other_original_star_source_pair_symmetry(self):
        pairs = {}
        for x in self.grade:
            p = tuple(x["mechanical_unordered_principal_star_pair"])
            pairs.setdefault(p, []).append(x["accepted_source_id"])
        self.assertEqual(pairs[("PoJun", "WuQu")], ["ZWD-R0296", "ZWD-R0515"])
        self.assertEqual(pairs[("LianZhen", "PoJun")], ["ZWD-R0341", "ZWD-R0511"])
        self.assertTrue(
            all(
                len(ids) == 1
                for k, ids in pairs.items()
                if k not in (("PoJun", "WuQu"), ("LianZhen", "PoJun"))
            )
        )

    def test_06_first_reciprocal_grade_condition_uses_birth_stems_not_behavior(self):
        source = {x["accepted_source_id"]: x for x in self.grade}
        self.assertIn("壬戊生人财官格", source["ZWD-R0296"]["verbatim_old_Chinese_line"])
        self.assertIn("戊生人福厚", source["ZWD-R0515"]["verbatim_old_Chinese_line"])
        self.assertEqual(source["ZWD-R0296"]["source_allowed_palaces_Earthly_roman"], ["Si", "Hai"])
        self.assertEqual(source["ZWD-R0515"]["source_allowed_palaces_Earthly_roman"], ["Si", "Hai"])

    def test_07_second_reciprocal_has_favorable_and_adverse_year_stem_subsets(self):
        data = {x["accepted_source_id"]: x for x in self.grade}
        self.assertIn("乙辛癸生人吉", data["ZWD-R0341"]["verbatim_old_Chinese_line"])
        self.assertIn("乙辛癸生人利", data["ZWD-R0511"]["verbatim_old_Chinese_line"])
        self.assertIn("甲庚丙生人不耐久", data["ZWD-R0511"]["verbatim_old_Chinese_line"])
        self.assertEqual(data["ZWD-R0511"]["source_allowed_palaces_Earthly_roman"], ["Mao", "You"])
        self.assertFalse(
            data["ZWD-R0511"]["fully_interpreted_year_stem_benefic_malefic_source_policy"]
        )

    def test_08_original_TianLiang_grade_places_have_distinct_dignities(self):
        rules = {x["accepted_source_id"]: x for x in self.grade}
        a = rules["ZWD-R0469"]["verbatim_old_Chinese_line"]
        b = rules["ZWD-R0472"]["verbatim_old_Chinese_line"]
        self.assertIn("卯宫入庙酉宫得地", a)
        self.assertIn("寅宫入庙申宫陷地", b)
        self.assertFalse(rules["ZWD-R0472"]["numerical_behavioral_trait_modifier_justified"])

    def test_09_seven_multi_star_qualifier_lines_exact_original(self):
        self.assertEqual(len(self.clusters), 7)
        self.assertEqual(
            [x["accepted_source_id"] for x in self.clusters],
            [x[0] for x in subject.CLUSTER_WARNINGS],
        )
        for x in self.clusters:
            self.assertIn(x["exact_source_conditional_fragment"], x["verbatim_old_Chinese_line"])
            self.assertTrue(x["multiple_adverse_or_benefic_conditions_may_apply"])
            self.assertTrue(x["simple_one_partner_star_behavioral_reversal_is_NOT_defined"])
            self.assertEqual(x["actual_people_verified"], 0)

    def test_10_LianZhen_QingYang_possible_dispute_modifier_is_auxiliary_not_scorable(self):
        x = next(x for x in self.clusters if x["accepted_source_id"] == "ZWD-R0331")
        self.assertEqual(x["exact_source_conditional_fragment"], "与擎羊同是非日有")
        self.assertIn(
            "disputes with QingYang auxiliary", x["qualification_unverified_English_note"]
        )
        self.assertTrue(x["simple_one_partner_star_behavioral_reversal_is_NOT_defined"])

    def test_11_LianZhen_TianXiang_mitigation_is_not_claimed_argument_frequency(self):
        x = next(x for x in self.clusters if x["accepted_source_id"] == "ZWD-R0339")
        self.assertEqual(x["exact_source_conditional_fragment"], "天相同宫能化其恶")
        self.assertTrue(
            self.output["selected_behavioral_conjunctive_interaction_magnitude_not_established"]
        )

    def test_12_PoJun_LianZhen_negative_requires_extra_malefics_and_fallen_palace(self):
        x = next(x for x in self.clusters if x["accepted_source_id"] == "ZWD-R0508")
        self.assertIn("遇廉贞羊陀火铃于陷宫，争斗疾病", x["verbatim_old_Chinese_line"])
        self.assertTrue(x["simple_one_partner_star_behavioral_reversal_is_NOT_defined"])
        self.assertTrue(
            self.output[
                "source_ancient_gender_health_wealth_status_moral_categories_not_empirical_facts"
            ]
        )

    def test_13_original_312_synthetic_vendor_not_people_and_120_deduplicated(self):
        self.assertEqual(self.comparison["raw_vendor_synthetic_comparisons"], 312)
        self.assertEqual(self.comparison["structurally_unique_synthetic_source_charts"], 120)
        self.assertEqual(
            self.comparison["synthetic_charts_where_selected_four_star_has_any_major_colocation"],
            22,
        )
        self.assertEqual(self.comparison["distinct_colocated_selected_pair_types"], 13)

    def test_14_20_of_22_pairs_match_original_grade_pair_and_placement(self):
        self.assertEqual(
            self.comparison[
                "synthetic_colocated_charts_with_exact_pair_and_life_palace_natal_grade_phrase"
            ],
            20,
        )
        self.assertEqual(
            self.comparison[
                "synthetic_colocated_charts_with_no_matching_literal_grade_pair_in_THIS_NARROW_SOURCE_SUBSET"
            ],
            2,
        )
        self.assertEqual(
            len(self.comparison["all_22_explicitly_synthetic_star_pair_and_life_palace_rows"]), 22
        )

    def test_15_two_unmatched_LianZhen_TanLang_in_grade_subset_not_entire_text(self):
        self.assertEqual(
            self.comparison["unmatched_literal_grade_pair_in_THIS_SUBSET"],
            [["LianZhen", "TanLang"]],
        )
        unmatched = [
            x
            for x in self.comparison["all_22_explicitly_synthetic_star_pair_and_life_palace_rows"]
            if not x["pair_and_palace_mentioned_in_original_grade_text"]
        ]
        self.assertEqual(len(unmatched), 2)
        self.assertTrue(
            all(x["source_principal_stars_in_Life"] == ["LianZhen", "TanLang"] for x in unmatched)
        )

    def test_16_all_matching_pair_place_source_rows_physically_valid(self):
        grades = {}
        for x in self.grade:
            grades.setdefault(tuple(x["mechanical_unordered_principal_star_pair"]), []).append(x)
        for row in self.comparison["all_22_explicitly_synthetic_star_pair_and_life_palace_rows"]:
            pair = tuple(row["source_principal_stars_in_Life"])
            actual = {
                r["accepted_source_id"]
                for r in grades.get(pair, [])
                if row["source_synthetic_Life_palace"] in r["source_allowed_palaces_Earthly_roman"]
            }
            self.assertEqual(set(row["original_grade_source_clause_ids"]), actual)

    def test_17_no_behavioural_weights_or_psychological_reversal_emerges(self):
        self.assertTrue(
            self.output[
                "co_star_grade_context_does_NOT_automatically_negate_unconditional_intro_trait"
            ]
        )
        self.assertTrue(
            self.output[
                "sole_star_exclusion_is_a_methodological_choice_not_original_textual_requirement"
            ]
        )
        self.assertTrue(
            self.output[
                "historical_birth_stem_and_good_bad_aspect_condition_required_to_interpret_rank"
            ]
        )
        self.assertTrue(self.comparison["no_trait_scoring_or_probability_generated"])
        self.assertFalse(
            any(x["numerical_behavioral_trait_modifier_justified"] for x in self.grade)
        )

    def test_18_changed_ancient_raw_quote_bytes_fail_on_specific_source(self):
        source = subject.RAW.read_bytes()
        fragment = "子午宫旺地，与天府同度".encode()
        self.assertEqual(source.count(fragment), 1)
        changed = source.replace(fragment, "子午宫旺地，与天相同度".encode())
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "source.txt"
            p.write_bytes(changed)
            with (
                patch.object(subject, "RAW", p),
                self.assertRaisesRegex(ValueError, "quote bytes/sha/offset"),
            ):
                subject.source_notes()

    def test_19_duplicate_original_grade_reference_cannot_count_twice(self):
        with (
            patch.object(subject, "PAIR_RULES", subject.PAIR_RULES + (subject.PAIR_RULES[0],)),
            self.assertRaisesRegex(ValueError, "multiple times"),
        ):
            subject.original_grade_witnesses(subject.source_notes())

    def test_20_wrong_original_canonical_palace_or_pair_quotation_fails(self):
        wrong = ("ZWD-R0293", "WuQu", "TianFu", "与天府同度", "子亥")
        patchrules = (wrong,) + subject.PAIR_RULES[1:]
        with (
            patch.object(subject, "PAIR_RULES", patchrules),
            self.assertRaisesRegex(ValueError, "no longer exact"),
        ):
            subject.original_grade_witnesses(subject.source_notes())

    def test_21_missing_original_cluster_fragment_fails(self):
        wrong = ("ZWD-R0331", "LianZhen", "我捏造的文本", "not verified")
        changed = tuple(wrong if x[0] == "ZWD-R0331" else x for x in subject.CLUSTER_WARNINGS)
        with (
            patch.object(subject, "CLUSTER_WARNINGS", changed),
            self.assertRaisesRegex(ValueError, "not in original"),
        ):
            subject.narrative_clusters(subject.source_notes())

    def test_22_reproducible_original_15_grade_7_clauses_and_120_synthetic_charts(self):
        self.assertEqual(subject.run(), self.output)

    def test_23_no_false_ancient_or_psychological_truth_claims(self):
        self.assertEqual(self.output["human_predictive_validations"], 0)
        self.assertEqual(self.output["actual_consented_real_humans_tested"], 0)
        self.assertEqual(self.output["astrology_runtime_model_promotions"], 0)
        self.assertFalse(self.output["original_scholarly_critical_early_Ming_printing_verified"])
        self.assertTrue(
            self.output["source_absent_selected_star_is_NOT_negative_behavior_prediction"]
        )


if __name__ == "__main__":
    unittest.main()
