"""Original Zi Wei Life-palace stars 9–12, exact oldid1963110 quotes.

No ancient book authenticity, chart interpretation or human forecasting claim.
"""
from __future__ import annotations
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import unittest

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
RAW=T/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
INDEX=T/"CHINESE_SOURCE_AUDIT_INDEX_V11.json"
PREVIOUS=T/"batches/ChineseAstro-11SRC-Life/ZIWEI_LIFE_PALACE_NEXT_FOUR_90_SOURCE_NOTES_V1.json"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
SOURCE=B/"ZIWEI_LIFE_PALACE_THIRD_FOUR_83_SOURCE_NOTES_V1.json"
WITNESS=B/"SOURCE_LIFE_THIRD_FOUR_83_EXACT_OFFSET_WITNESS_V1.json"
EXCERPT=B/"SOURCE_1963110_LIFE_PALACE_THIRD_FOUR_EXACT_EXCERPT.txt"
ACCEPT=B/"ACCEPTANCE.json"
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def h(v):return sha256(v).hexdigest()

class OriginalSourceStarNineThroughTwelve(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=RAW.read_bytes()
        cls.full=cls.raw.decode("utf-8")
        cls.s=rd(SOURCE)
        cls.w=rd(WITNESS)
        cls.a=rd(ACCEPT)
        cls.rows=cls.s["records"]

    def test_01_original_chinese_full_raw_sha_bytes(self):
        self.assertEqual(len(self.raw),106736)
        self.assertEqual(h(self.raw),
                         "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72")
        self.assertEqual(self.s["original_oldid"],1963110)
        self.assertFalse(self.s["original_Ming_woodblock_imprint_authenticated"])

    def test_02_prior_V11_exact_accepted_chinese_source_frontier(self):
        old=rd(INDEX)
        self.assertEqual(h(INDEX.read_bytes()),self.a["prior_V11_Chinese_source_index_SHA256"])
        self.assertEqual(old["sum_source_annotations"],609)
        self.assertEqual([(p["accepted_source_annotations"],p["next_id"]) for p in old["systems"]],
                         [(210,"BZI-R0211"),(399,"ZWD-R0400")])
        self.assertEqual(old["accepted_batches"][-1]["id"],"ChineseAstro-11SRC-Life")

    def test_03_prior_TanLang_prefix_only_navigation_is_not_a_studied_star(self):
        previous=rd(PREVIOUS)
        self.assertEqual(previous["last_id"],"ZWD-R0399")
        self.assertEqual(previous["records"][-1]["source_line_type"],
                         "NEXT_STAR_BOUNDARY_NO_SUBSTANTIVE_TANLANG_CLAIMS")
        self.assertEqual(previous["records"][-1]["original_absolute_codepoint_offset"],25795)
        self.assertTrue(self.rows[0]["exact_original_Chinese_Wikitext_quote"].startswith(
            previous["records"][-1]["exact_original_Chinese_Wikitext_quote"]))
        self.assertTrue(self.s["previous_V11_TanLang_only_heading_prefix_already_in_R0399"])

    def test_04_original_source_exact_excerpt_span_and_sha(self):
        self.assertEqual(self.s["original_excerpt_start_codepoint"],25795)
        self.assertEqual(self.s["original_excerpt_end_codepoint_exclusive"],28621)
        self.assertEqual(self.s["siblings_next_section_heading_codepoint"],37269)
        self.assertEqual(EXCERPT.read_bytes(),self.full[25795:28621].encode("utf-8"))
        self.assertEqual(h(EXCERPT.read_bytes()),self.s["original_excerpt_sha256"])
        self.assertEqual(self.w["original_excerpt_source_codepoint_range"],[25795,28621])

    def test_05_four_star_sections_are_complete_and_exact_source_segments(self):
        specs=[
            ("TanLang","贪狼",25795,26547,21,6),
            ("JuMen","巨门",26547,27330,22,7),
            ("TianXiang","天相",27330,27995,21,6),
            ("TianLiang","天梁",27995,28621,18,5),
        ]
        for row,(roman,han,a,b,n,branch) in zip(self.s["star_original_sections"],specs):
            self.assertEqual((row["star_roman"],row["original_star"]),(roman,han))
            self.assertEqual((row["original_codepoint_start"],row["original_codepoint_end_exclusive"]),(a,b))
            self.assertEqual(row["source_line_annotation_count"],n)
            self.assertEqual(row["original_palace_line_count"],branch)
            self.assertEqual(row["source_original_UTF8_SHA256"],h(self.full[a:b].encode("utf-8")))
        self.assertEqual(self.s["star_line_counts"],{x[0]:x[4] for x in specs})

    def test_06_exact_83_record_ids_and_next_nonstudied_QiSha_boundary(self):
        self.assertEqual(len(self.rows),83)
        self.assertEqual([r["id"] for r in self.rows],
                         [f"ZWD-R{i:04d}" for i in range(400,483)])
        self.assertEqual(len(set(r["id"] for r in self.rows)),83)
        self.assertEqual(self.rows[-1]["source_line_type"],
                         "NEXT_STAR_BOUNDARY_NO_SUBSTANTIVE_QISHA_CLAIMS")
        self.assertEqual(self.rows[-1]["exact_original_Chinese_Wikitext_quote"],
                         "七杀火金，南斗将星")
        self.assertEqual(self.s["next_id"],"ZWD-R0483")

    def test_07_each_original_quote_codepoint_and_utf8_exact_offset(self):
        witnesses={w["id"]:w for w in self.w["exact_quote_offsets"]}
        self.assertEqual(len(witnesses),83)
        old=-1
        for item in self.rows:
            quote=item["exact_original_Chinese_Wikitext_quote"]
            encoded=quote.encode("utf-8")
            cp=item["original_absolute_codepoint_offset"]
            off=item["original_absolute_UTF8_byte_offset"]
            self.assertEqual(self.full[cp:cp+len(quote)],quote)
            self.assertEqual(self.raw[off:off+len(encoded)],encoded)
            self.assertEqual(h(encoded),item["source_quote_sha256_UTF8"])
            self.assertEqual(len(encoded),item["source_quote_UTF8_bytes"])
            self.assertEqual(cp-item["original_excerpt_relative_codepoint_offset"],25795)
            self.assertGreater(cp,old);old=cp
            w=witnesses[item["id"]]
            self.assertEqual(w["original_UTF8_byte_offset"],off)
            self.assertEqual(w["quote_SHA256"],h(encoded))

    def test_08_source_line_types_exact_distribution_and_missing_verse(self):
        self.assertEqual(Counter(r["source_line_type"] for r in self.rows),{
            "historical_sex_coded_or_time_poem_verse":32,
            "natal_branch_condition":24,
            "natal_narrative_condition":11,
            "historical_poem_heading":11,
            "star_profile_intro":4,
            "NEXT_STAR_BOUNDARY_NO_SUBSTANTIVE_QISHA_CLAIMS":1
        })
        for star in ("TanLang","JuMen","TianXiang"):
            heads=[r["source_section_context"] for r in self.rows
                   if r["star_group_romanization"]==star and
                   r["source_line_type"]=="historical_poem_heading"]
            self.assertEqual(heads,[
                "male_life_poem_heading","female_life_poem_heading",
                "time_limit_poem_heading"
            ])
        heads=[r["source_section_context"] for r in self.rows if
               r["star_group_romanization"]=="TianLiang" and
               r["source_line_type"]=="historical_poem_heading"]
        self.assertEqual(heads,["male_life_poem_heading","time_limit_poem_heading"])

    def test_09_TianLiang_female_heading_absent_do_not_invent_one(self):
        self.assertTrue(self.s["TianLiang_source_has_no_distinct_female_verse_heading"])
        self.assertFalse(self.s["star_original_sections"][-1][
            "distinct_original_female_poem_heading_present"])
        src=self.full[27995:28621]
        self.assertIn("天梁入男命吉凶诀：",src)
        self.assertIn("天梁入限吉凶诀：",src)
        self.assertNotIn("天梁入女命吉凶诀：",src)

    def test_10_old_health_mortality_and_sex_moral_stereotypes_not_evidence(self):
        self.assertEqual(sum(r.get("contains_historic_health_sex_morality_or_death_terms",False)
                             for r in self.rows),20)
        self.assertFalse(self.s["original_claims_of_sex_health_disability_and_longevity_medically_true"])
        self.assertTrue(all(not r["medical_or_moral_advice_authorized"] for r in self.rows))
        self.assertTrue(all(not r["genuine_human_behavior_or_fate_validated"] for r in self.rows))

    def test_11_TanLang_JuMen_TianXiang_source_conditional_not_Astro_chart(self):
        alltext=" ".join(x["exact_original_Chinese_Wikitext_quote"] for x in self.rows)
        for word in ("贪狼","巨门","天相","天梁","七杀","宫","化忌"):
            self.assertIn(word,alltext)
        self.assertFalse(self.s["source_original_inconsistent_star_conditions_resolved"])
        self.assertTrue(all(not r["original_natal_star_premise_astronomically_verified"]
                            for r in self.rows))

    def test_12_correct_next_source_QiSha_and_brothers_boundary_not_covered(self):
        self.assertEqual(self.s["next_unstudied_star_native"],"七杀")
        self.assertEqual(self.s["next_unstudied_star_original_codepoint"],28621)
        self.assertTrue(self.full[28621:].startswith("七杀火金，南斗将星"))
        self.assertTrue(self.full[37269:].startswith("===二兄弟==="))
        self.assertFalse(self.s["complete_Life_palace_source_study"])

    def test_13_separate_original_BaZi_Western_and_prior_Chinese_versions_untouched(self):
        old=rd(INDEX)
        self.assertEqual(old["systems"][0]["accepted_source_annotations"],210)
        self.assertEqual(self.a["next_BZI"],"BZI-R0211")
        west=rd(WEST)
        self.assertEqual(west["records_count"],13044)
        self.assertEqual(west["batches"][-1]["id"],"B07bc")

    def test_14_history_not_genuine_human_predictions(self):
        self.assertEqual(self.s["genuine_real_human_predictive_validations"],0)
        self.assertEqual(self.s["runtime_forecast_promotions"],0)
        self.assertTrue(all(x["actual_forward_reverse_blind_people_tested"]==0 for x in self.rows))
        self.assertTrue(all(not x["runtime_rule_promoted"] for x in self.rows))

    def test_15_source_acceptance_SHA_and_new_index_counts(self):
        self.assertEqual(self.a["Chinese_before"],609)
        self.assertEqual(self.a["Chinese_after_if_accepted"],692)
        self.assertEqual(self.a["ZiWei_after_if_accepted"],482)
        self.assertEqual(self.a["BaZi_retained"],210)
        self.assertEqual(self.a["new_original_source_only_annotations"],83)
        self.assertEqual(h(SOURCE.read_bytes()),self.a["note_SHA256"])
        self.assertEqual(h(WITNESS.read_bytes()),self.a["witness_SHA256"])
        self.assertEqual(h(EXCERPT.read_bytes()),self.a["excerpt_SHA256"])

if __name__=="__main__":unittest.main()
