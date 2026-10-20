"""Zi Wei 4 next Life palace star profiles, exact source byte tests, not human data."""
from __future__ import annotations
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import unittest
from unittest.mock import patch

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
RAW=T/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
V10=T/"CHINESE_SOURCE_AUDIT_INDEX_V10.json"
PREVIOUS=T/"batches/ChineseAstro-10SRC-Life/ZIWEI_LIFE_PALACE_FIRST_FOUR_89_SOURCE_NOTES_V1.json"
SOURCE=B/"ZIWEI_LIFE_PALACE_NEXT_FOUR_90_SOURCE_NOTES_V1.json"
WITNESS=B/"SOURCE_LIFE_NEXT_FOUR_90_EXACT_OFFSET_WITNESS_V1.json"
EXCERPT=B/"SOURCE_1963110_LIFE_PALACE_NEXT_FOUR_EXACT_EXCERPT.txt"
ACCEPT=B/"ACCEPTANCE.json"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
def r(p):return json.loads(p.read_text(encoding="utf-8"))
def h(blob):return sha256(blob).hexdigest()

class FourAdditionalOriginalZiWeiStars(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=RAW.read_bytes()
        cls.full=cls.raw.decode("utf-8")
        cls.s=r(SOURCE)
        cls.w=r(WITNESS)
        cls.a=r(ACCEPT)
        cls.rows=cls.s["records"]

    def test_01_exact_transmitted_full_original_rev_sha(self):
        self.assertEqual(len(self.raw),106736)
        self.assertEqual(h(self.raw),
            "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72")
        self.assertEqual(self.s["original_oldid"],1963110)
        self.assertFalse(self.s["original_Ming_woodblock_imprint_authenticated"])

    def test_02_old_v10_source_fully_preserved_and_next_frontier(self):
        old=r(V10)
        self.assertEqual(h(V10.read_bytes()),self.a["prior_V10_Chinese_source_index_SHA256"])
        self.assertEqual(old["sum_source_annotations"],519)
        self.assertEqual(old["systems"][0]["next_id"],"BZI-R0211")
        self.assertEqual(old["systems"][1]["next_id"],"ZWD-R0310")
        self.assertEqual(old["accepted_batches"][-1]["id"],"ChineseAstro-10SRC-Life")

    def test_03_v10_only_TianTong_navigation_marker_not_full_verses(self):
        prev=r(PREVIOUS)
        self.assertEqual(prev["last_id"],"ZWD-R0309")
        self.assertEqual(prev["records"][-1]["source_line_type"],
                         "NEXT_STAR_BOUNDARY_NO_SUBSTANTIVE_TIANTONG_CLAIMS")
        self.assertEqual(prev["records"][-1]["original_absolute_codepoint_offset"],22909)
        self.assertTrue(self.rows[0]["exact_original_Chinese_Wikitext_quote"].startswith(
            prev["records"][-1]["exact_original_Chinese_Wikitext_quote"]
        ))
        self.assertTrue(self.s["previous_V10_TianTong_only_heading_prefix_already_in_R0309"])

    def test_04_full_source_segment_ranges_and_sha(self):
        self.assertEqual(self.s["original_excerpt_start_codepoint"],22909)
        self.assertEqual(self.s["original_excerpt_end_codepoint_exclusive"],25795)
        self.assertEqual(self.s["siblings_next_section_heading_codepoint"],37269)
        self.assertEqual(EXCERPT.read_bytes(),self.full[22909:25795].encode("utf-8"))
        self.assertEqual(h(EXCERPT.read_bytes()),self.s["original_excerpt_sha256"])
        self.assertEqual(self.w["original_excerpt_source_codepoint_range"],[22909,25795])

    def test_05_four_star_segments_positions_and_line_counts(self):
        expected=[
            ("TianTong","天同",22909,23557,20),
            ("LianZhen","廉贞",23557,24407,26),
            ("TianFu","天府",24407,25060,20),
            ("TaiYin","太阴",25060,25795,23),
        ]
        self.assertEqual(len(self.s["star_original_sections"]),4)
        for section,(roman,han,first,last,count) in zip(self.s["star_original_sections"],expected):
            self.assertEqual(section["star_roman"],roman)
            self.assertEqual(section["original_star"],han)
            self.assertEqual(section["original_codepoint_start"],first)
            self.assertEqual(section["original_codepoint_end_exclusive"],last)
            self.assertEqual(section["source_line_annotation_count"],count)
            self.assertEqual(section["source_original_UTF8_SHA256"],
                             h(self.full[first:last].encode("utf-8")))
        self.assertEqual(self.s["star_line_counts"],
                         {n:c for n,_,_,_,c in expected})

    def test_06_90_contiguous_unique_ids_and_navigation_last(self):
        self.assertEqual(len(self.rows),90)
        self.assertEqual([item["id"] for item in self.rows],
                         [f"ZWD-R{i:04d}" for i in range(310,400)])
        self.assertEqual(len({x["id"] for x in self.rows}),90)
        self.assertEqual(self.rows[-1]["source_line_type"],
                         "NEXT_STAR_BOUNDARY_NO_SUBSTANTIVE_TANLANG_CLAIMS")
        self.assertEqual(self.rows[-1]["exact_original_Chinese_Wikitext_quote"],
                         "贪狼属木，化桃花杀")
        self.assertEqual(self.s["next_id"],"ZWD-R0400")

    def test_07_every_record_original_codepoint_utf8_exact_and_sha(self):
        witnesses={x["id"]:x for x in self.w["exact_quote_offsets"]}
        self.assertEqual(len(witnesses),90)
        prior=-1
        for item in self.rows:
            quote=item["exact_original_Chinese_Wikitext_quote"]
            encoded=quote.encode("utf-8")
            cp=item["original_absolute_codepoint_offset"]
            byte_pos=item["original_absolute_UTF8_byte_offset"]
            self.assertEqual(self.full[cp:cp+len(quote)],quote)
            self.assertEqual(self.raw[byte_pos:byte_pos+len(encoded)],encoded)
            self.assertEqual(h(encoded),item["source_quote_sha256_UTF8"])
            self.assertEqual(len(encoded),item["source_quote_UTF8_bytes"])
            self.assertEqual(cp-item["original_excerpt_relative_codepoint_offset"],22909)
            self.assertGreater(cp,prior)
            prior=cp
            witness=witnesses[item["id"]]
            self.assertEqual(witness["original_UTF8_byte_offset"],byte_pos)
            self.assertEqual(witness["quote_SHA256"],h(encoded))

    def test_08_source_line_types_and_no_missing_three_verse_contexts(self):
        kinds=Counter(x["source_line_type"] for x in self.rows)
        self.assertEqual(kinds,{
            "star_profile_intro":4,"natal_narrative_condition":20,
            "natal_branch_condition":24,"historical_poem_heading":12,
            "historical_sex_coded_or_time_poem_verse":29,
            "NEXT_STAR_BOUNDARY_NO_SUBSTANTIVE_TANLANG_CLAIMS":1,
        })
        for star in ("TianTong","LianZhen","TianFu","TaiYin"):
            group=[x for x in self.rows if x["star_group_romanization"]==star]
            headings=[x["source_section_context"] for x in group
                      if x["source_line_type"]=="historical_poem_heading"]
            self.assertEqual(headings,[
                "male_life_poem_heading","female_life_poem_heading",
                "time_limit_poem_heading"
            ])

    def test_09_palace_specific_rows_not_fake_chart_locations(self):
        n=Counter(x["star_group_romanization"] for x in self.rows
                  if x["source_line_type"]=="natal_branch_condition")
        self.assertEqual(n,{"TianTong":6,"LianZhen":8,"TianFu":6,"TaiYin":4})
        self.assertFalse(self.s["source_original_inconsistent_star_conditions_resolved"])
        self.assertFalse(any(x["original_natal_star_premise_astronomically_verified"]
                             for x in self.rows))

    def test_10_original_health_social_and_old_sex_moral_claims_not_medicine(self):
        risky=[x for x in self.rows if
               x.get("contains_historic_health_sex_morality_or_death_terms",False)]
        self.assertEqual(len(risky),22)
        self.assertFalse(self.s["original_claims_of_sex_health_disability_and_longevity_medically_true"])
        self.assertTrue(all(not x["medical_or_moral_advice_authorized"] for x in self.rows))
        self.assertTrue(all(not x["genuine_human_behavior_or_fate_validated"] for x in self.rows))

    def test_11_ambiguity_example_sex_and_branches_without_forced_repair(self):
        corpus="\n".join(x["exact_original_Chinese_Wikitext_quote"] for x in self.rows)
        self.assertIn("女命",corpus)
        self.assertIn("化忌",corpus)
        self.assertIn("丑未宫",corpus)
        self.assertIn("入限吉凶诀",corpus)
        self.assertFalse(self.s["complete_Life_palace_source_study"])

    def test_12_source_span_next_TanLang_not_consumed(self):
        self.assertEqual(self.s["next_unstudied_star_native"],"贪狼")
        self.assertEqual(self.s["next_unstudied_star_original_codepoint"],25795)
        self.assertTrue(self.full[25795:].startswith("贪狼属木，化桃花杀"))
        self.assertTrue(self.full[37269:].startswith("===二兄弟==="))
        self.assertTrue(self.s["only_four_additional_of_all_original_Life_palace_stars"])

    def test_13_separate_bazi_and_snapshot_western_unmodified(self):
        self.assertTrue(self.s["separate_BaZi_original_source_next_BZI_R0211_retained"])
        old=r(V10)
        self.assertEqual(old["systems"][0]["accepted_source_annotations"],210)
        west=r(WEST)
        self.assertEqual(west["records_count"],13044)
        self.assertEqual(west["batches"][-1]["id"],"B07bc")

    def test_14_source_only_not_synthetic_engine_or_human_accuracy(self):
        self.assertEqual(self.s["genuine_real_human_predictive_validations"],0)
        self.assertEqual(self.s["runtime_forecast_promotions"],0)
        self.assertTrue(all(x["actual_forward_reverse_blind_people_tested"]==0 for x in self.rows))
        self.assertTrue(all(not x["runtime_rule_promoted"] for x in self.rows))

    def test_15_acceptance_source_and_witness_sha_guard(self):
        self.assertEqual(self.a["Chinese_before"],519)
        self.assertEqual(self.a["Chinese_after_if_accepted"],609)
        self.assertEqual(self.a["ZiWei_after_if_accepted"],399)
        self.assertEqual(self.a["BaZi_retained"],210)
        self.assertEqual(self.a["new_original_source_only_annotations"],90)
        self.assertEqual(h(SOURCE.read_bytes()),self.a["note_SHA256"])
        self.assertEqual(h(WITNESS.read_bytes()),self.a["witness_SHA256"])
        self.assertEqual(h(EXCERPT.read_bytes()),self.a["excerpt_SHA256"])

if __name__=="__main__":unittest.main()
