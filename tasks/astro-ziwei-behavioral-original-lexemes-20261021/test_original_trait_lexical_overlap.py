"""Exact original source phrase overlap, context qualifiers and negative controls."""

from __future__ import annotations

import json
import tempfile
import unittest
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch

import audit_original_trait_lexical_overlap as source

B = Path(__file__).resolve().parent
ROOT = B.parents[1]
FILE = B / "ZIWEI_LIFE_BEHAVIORAL_LEXEME_OVERLAP_SOURCE_AUDIT_V1.json"


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def sha(b):
    return sha256(b).hexdigest()


class ZiWeiOriginalFourBehaviorLexemes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = load(FILE)
        cls.hits = cls.d["verbatim_behavior_related_lexical_source_witnesses"]
        cls.source_raw = source.RAW.read_bytes()
        cls.full = cls.source_raw.decode("utf-8")
        cls.hits_by_phrase = {}
        for x in cls.hits:
            cls.hits_by_phrase.setdefault(x["verbatim_narrow_Chinese_phrase"], []).append(x)

    def test_01_original_source_exact_SHA_oldid_and_palace_heading(self):
        self.assertEqual(len(self.source_raw), 106736)
        self.assertEqual(sha(self.source_raw), source.RAW_SHA)
        self.assertEqual(self.d["transmitted_source_revision_oldid"], 1963110)
        self.assertEqual(
            self.d["original_Life_palace_section_absolute_codepoint_range"], [19953, 37269]
        )
        self.assertTrue(self.full[19953:].startswith("===一 命宫==="))
        self.assertTrue(self.full[37269:].startswith("===二兄弟==="))
        self.assertFalse(self.d["source_ming_woodblock_early_printing_independently_authenticated"])

    def test_02_accepted_V14_registry_and_old_four_question_SHA(self):
        self.assertEqual(sha(source.INDEX.read_bytes()), source.INDEX_SHA)
        self.assertEqual(sha(source.CANDIDATE.read_bytes()), source.CANDIDATE_SHA)
        self.assertEqual(
            [r["accepted_source_annotations"] for r in load(source.INDEX)["systems"]], [210, 586]
        )
        self.assertEqual(load(source.CANDIDATE)["human_predictive_validation_count"], 0)

    def test_03_eight_predeclared_narrow_chinese_lexemes_total_11(self):
        expected = {
            "果决": 3,
            "好济施": 2,
            "好施济": 1,
            "好忿争": 1,
            "是非日有": 1,
            "好争强": 1,
            "争斗疾病": 1,
            "好勇斗狠": 1,
        }
        self.assertEqual(self.d["original_verbatim_narrow_lexeme_counts_whole_volume"], expected)
        self.assertEqual(len(self.hits), 11)
        for word, count in expected.items():
            self.assertEqual(self.full.count(word), count)
            self.assertEqual(self.full[19953:37269].count(word), count)

    def test_04_each_11_phrase_word_and_full_line_exact_utf8_source_offsets(self):
        for hit in self.hits:
            fragment = hit["verbatim_narrow_Chinese_phrase"]
            line = hit["original_Chinese_full_context_line"]
            cp = hit["source_word_exact_codepoint_offset"]
            b = hit["source_word_exact_UTF8_byte_offset"]
            line_cp = hit["original_full_context_line_codepoint_offset"]
            line_b = hit["original_full_context_line_UTF8_byte_offset"]
            self.assertEqual(self.full[cp : cp + len(fragment)], fragment)
            self.assertEqual(self.source_raw[b : b + len(fragment.encode())], fragment.encode())
            self.assertEqual(self.full[line_cp : line_cp + len(line)], line)
            self.assertEqual(self.source_raw[line_b : line_b + len(line.encode())], line.encode())
            self.assertEqual(sha(fragment.encode()), hit["source_word_exact_sha256_UTF8"])
            self.assertEqual(sha(line.encode()), hit["original_full_context_line_sha256_UTF8"])
            self.assertEqual(hit["transmitted_full_original_source_SHA256"], source.RAW_SHA)
            self.assertEqual(hit["transmitted_full_original_source_oldid"], 1963110)

    def test_05_nine_already_accepted_source_notes_two_QingYang_original_raw_only(self):
        expected = {
            "ZWD-R0287",
            "ZWD-R0548",
            "ZWD-R0263",
            "ZWD-R0464",
            "ZWD-R0576",
            "ZWD-R0330",
            "ZWD-R0331",
            "ZWD-R0505",
            "ZWD-R0508",
        }
        actual = {
            r["already_accepted_historical_source_annotation_id"]
            for r in self.hits
            if r["already_accepted_historical_source_annotation_id"]
        }
        self.assertEqual(actual, expected)
        raw_only = [r for r in self.hits if r["source_record_status"].startswith("RAW_WIKITEXT")]
        self.assertEqual(len(raw_only), 2)
        self.assertEqual({r["original_occurrence_source_star"] for r in raw_only}, {"QingYang"})
        self.assertTrue(
            all(
                r["already_accepted_historical_source_annotation_id"] is None
                and r["accepted_source_annotation_file"] is None
                for r in raw_only
            )
        )

    def test_06_accepted_source_line_annotation_file_hashes_verified(self):
        for r in self.hits:
            rel = r["accepted_source_annotation_file"]
            if rel is None:
                continue
            p = ROOT / rel
            self.assertEqual(sha(p.read_bytes()), r["accepted_source_annotation_file_SHA256"])
            q = load(p)
            row = next(
                x
                for x in q["records"]
                if x["id"] == r["already_accepted_historical_source_annotation_id"]
            )
            orig = row.get(
                "exact_original_Chinese_Wikitext_quote",
                row.get("source_original_exact_Chinese_Wikitext_quote"),
            )
            self.assertEqual(orig, r["original_Chinese_full_context_line"])

    def test_07_exact_helping_phrase_is_shared_by_two_major_stars(self):
        stars = [x["original_occurrence_source_star"] for x in self.hits_by_phrase["好济施"]]
        self.assertEqual(stars, ["TaiYang", "TianLiang"])
        self.assertEqual(
            self.d["identical_giving_phrase_in_two_different_principal_stars"],
            ["TaiYang", "TianLiang"],
        )
        self.assertEqual(
            [
                r["already_accepted_historical_source_annotation_id"]
                for r in self.hits_by_phrase["好济施"]
            ],
            ["ZWD-R0263", "ZWD-R0464"],
        )

    def test_08_similar_helping_word_order_YouBi_auxiliary_not_proven_synonym(self):
        x = self.hits_by_phrase["好施济"]
        self.assertEqual(len(x), 1)
        self.assertEqual(x[0]["original_occurrence_source_star"], "YouBi")
        self.assertEqual(x[0]["original_phrase_context_tag"], "star_intro_in_temple_context")
        self.assertIn("入庙", x[0]["original_Chinese_full_context_line"])
        self.assertFalse(
            self.d["source_related_phrases_semantically_synonymous_without_expert_review"]
        )
        self.assertFalse(x[0]["word_order_or_semantic_equivalence_validated"])

    def test_09_resoluteness_FuoJue_occurs_three_different_source_star_contexts(self):
        x = self.hits_by_phrase["果决"]
        self.assertEqual(
            [r["original_occurrence_source_star"] for r in x], ["WuQu", "WenQu", "QingYang"]
        )
        self.assertEqual(
            [r["original_phrase_context_tag"] for r in x],
            [
                "star_intro_general",
                "multiple_stars_and_palace_required",
                "star_intro_in_temple_context",
            ],
        )
        self.assertTrue(
            self.d["resoluteness_WenQu_requires_named_co_present_stars_and_favourable_house"]
        )

    def test_10_WenQu_decisiveness_is_conditional_not_baseline_WenQu_trait(self):
        row = self.hits_by_phrase["果决"][1]
        self.assertIn("若与同梁武曲会旺宫，聪明果决", row["original_Chinese_full_context_line"])
        self.assertEqual(row["already_accepted_historical_source_annotation_id"], "ZWD-R0548")
        self.assertFalse(row["expert_full_original_chinese_translation_verified"])

    def test_11_QingYang_auxiliary_decisiveness_not_in_fourteen_principal_star_engine(self):
        r = self.hits_by_phrase["果决"][2]
        self.assertEqual(r["original_occurrence_source_star"], "QingYang")
        self.assertIn("入庙权贵", r["original_Chinese_full_context_line"])
        self.assertIsNone(r["already_accepted_historical_source_annotation_id"])
        self.assertTrue(self.d["resoluteness_QingYang_auxiliary_chart_engine_not_in_14_main_stars"])

    def test_12_LianZhen_intro_and_QingYang_conditional_different_claims(self):
        intro = self.hits_by_phrase["好忿争"][0]
        conditional = self.hits_by_phrase["是非日有"][0]
        self.assertEqual(intro["original_occurrence_source_star"], "LianZhen")
        self.assertEqual(intro["original_phrase_context_tag"], "star_intro_general")
        self.assertEqual(
            conditional["original_phrase_context_tag"], "with_QingYang_auxiliary_condition"
        )
        self.assertIn("与擎羊同是非日有", conditional["original_Chinese_full_context_line"])

    def test_13_PoJun_intro_competition_vs_multimalefic_fallen_quarrel(self):
        intro = self.hits_by_phrase["好争强"][0]
        cluster = self.hits_by_phrase["争斗疾病"][0]
        self.assertEqual(intro["original_occurrence_source_star"], "PoJun")
        self.assertEqual(intro["original_phrase_context_tag"], "star_intro_general")
        self.assertEqual(
            cluster["original_phrase_context_tag"], "fallen_palace_with_multiple_adverse_stars"
        )
        self.assertIn(
            "遇廉贞羊陀火铃于陷宫，争斗疾病", cluster["original_Chinese_full_context_line"]
        )

    def test_14_QingYang_related_aggression_is_not_equivalent_to_PoJun_competition(self):
        r = self.hits_by_phrase["好勇斗狠"][0]
        self.assertEqual(r["original_occurrence_source_star"], "QingYang")
        self.assertEqual(r["original_phrase_context_tag"], "star_intro_in_temple_context")
        self.assertEqual(r["already_accepted_historical_source_annotation_id"], None)
        self.assertFalse(r["word_order_or_semantic_equivalence_validated"])

    def test_15_parent_four_behavior_source_uniqueness_unsupported_by_word_scan(self):
        self.assertTrue(
            self.d[
                "source_behavior_lexical_uniqueness_not_sufficient_for_discriminative_chart_prediction"
            ]
        )
        self.assertTrue(
            self.d["source_behavioral_leakage_risk_if_exclusive_star_fingerprint_assumed"]
        )
        self.assertTrue(
            self.d["quantified_behavior_effect_directions_and_conditional_priority_unresolved"]
        )
        self.assertTrue(
            self.d[
                "source_same_chinese_lexeme_occurrence_does_NOT_equal_independent_human_predicted_evidence"
            ]
        )

    def test_16_original_120_synthetic_main_star_chart_overlap_source_years(self):
        sample = self.d["source_star_placements_only_synthetic"]
        self.assertEqual(sample["synthetic_comparator_raw_cases"], 312)
        self.assertEqual(sample["synthetic_comparator_unique_source_chart_structures"], 120)
        self.assertEqual(
            sample["main_star_Life_presence_synthetic_only"],
            {
                "TaiYang": 10,
                "TianLiang": 8,
                "WuQu": 9,
                "TaiYang_or_TianLiang": 16,
                "TaiYang_and_TianLiang": 2,
            },
        )
        self.assertEqual(
            len(sample["same_exact_helping_phrase_both_main_stars_in_two_source_charts"]), 2
        )

    def test_17_no_auxiliary_star_positions_claimed_from_14_major_star_engine(self):
        d = self.d["source_star_placements_only_synthetic"]
        self.assertFalse(d["WenQu_YouBi_QingYang_auxiliary_star_positions_computed_here"])
        self.assertTrue(d["calendar_dates_are_purposefully_selected_not_population"])
        self.assertTrue(d["synthetic_main_star_overlap_cannot_establish_behavioral_trait_validity"])

    def test_18_original_Chinese_RAW_sha_tamper_detected_before_lexical_scan(self):
        altered = self.source_raw.replace("心无私曲好济施".encode(), "心无私曲好济泗".encode())
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "raw.txt"
            f.write_bytes(altered)
            with patch.object(source, "RAW", f), self.assertRaisesRegex(ValueError, "Wikitext"):
                source.accepted_source()

    def test_19_source_lexeme_word_change_unsupported_fails_closed(self):
        with (
            patch.dict(source.TARGETS, {"helping_added": "帮别人"}),
            self.assertRaises(ValueError),
        ):
            source.phrase_inventory()

    def test_20_forged_original_star_context_claim_not_accepted(self):
        with (
            patch.dict(
                source.QUALIFICATIONS,
                {
                    ("果决", "WenQu"): (
                        "unconditional_intro",
                        "this clause was never present in old source",
                    )
                },
            ),
            self.assertRaisesRegex(ValueError, "drift"),
        ):
            source.phrase_inventory()

    def test_21_past_annotated_source_claim_mismatched_file_sha_rejected(self):
        original = source.SOURCE_GROUPS["TaiYang"]
        with (
            patch.dict(
                source.SOURCE_GROUPS,
                {
                    "TaiYang": (
                        original[0],
                        original[1],
                        "ChineseAstro-14SRC-Life/ZIWEI_LIFE_FIRST_FOUR_AUXILIARY_58_SOURCE_NOTES_V1.json",
                    )
                },
            ),
            self.assertRaises(ValueError),
        ):
            source.phrase_inventory()

    def test_22_two_exact_selected_helping_source_stars_not_two_independent_people(self):
        r = self.d["source_star_placements_only_synthetic"][
            "main_star_Life_presence_synthetic_only"
        ]
        self.assertEqual(
            r["TaiYang"] + r["TianLiang"] - r["TaiYang_and_TianLiang"], r["TaiYang_or_TianLiang"]
        )
        self.assertEqual(r["TaiYang_and_TianLiang"], 2)
        self.assertEqual(self.d["participant_natal_birth_coordinates_or_answers_included"], 0)
        self.assertEqual(self.d["human_forward_reverse_validations"], 0)

    def test_23_full_lexeme_source_study_replay_identical(self):
        self.assertEqual(source.run(), self.d)
        self.assertEqual(self.d["production_astrological_personality_rules"], 0)


if __name__ == "__main__":
    unittest.main()
