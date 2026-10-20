"""First four Zi Wei auxiliary source profiles, exact original source only.

No original Ming print provenance or human personality/fate prediction.
"""
from __future__ import annotations
from hashlib import sha256
from collections import Counter
import json
from pathlib import Path
import unittest

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
RAW=T/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
V13=T/"CHINESE_SOURCE_AUDIT_INDEX_V13.json"
PREVIOUS=T/"batches/ChineseAstro-13SRC-Life/ZIWEI_LIFE_PALACE_FINAL_TWO_46_SOURCE_NOTES_V1.json"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
SOURCE=B/"ZIWEI_LIFE_FIRST_FOUR_AUXILIARY_58_SOURCE_NOTES_V1.json"
WITNESS=B/"SOURCE_LIFE_FIRST_FOUR_AUXILIARY_58_EXACT_OFFSET_WITNESS_V1.json"
EXCERPT=B/"SOURCE_1963110_LIFE_FIRST_FOUR_AUX_EXACT_EXCERPT.txt"
ACCEPT=B/"ACCEPTANCE.json"
def read(p):return json.loads(p.read_text(encoding="utf-8"))
def hash_data(b):return sha256(b).hexdigest()

class FirstFourOriginalAuxiliaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=RAW.read_bytes();cls.full=cls.raw.decode("utf-8")
        cls.src=read(SOURCE);cls.w=read(WITNESS);cls.acc=read(ACCEPT)
        cls.rows=cls.src["records"]

    def test_01_raw_original_source_exact_rev_hash_bytes(self):
        self.assertEqual(len(self.raw),106736)
        self.assertEqual(hash_data(self.raw),
            "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72")
        self.assertFalse(self.src["original_Ming_woodblock_imprint_verified"])

    def test_02_previous_V13_original_source_index_immutable(self):
        ix=read(V13)
        self.assertEqual(hash_data(V13.read_bytes()),self.acc["previous_source_V13_index_SHA256"])
        self.assertEqual(ix["sum_source_annotations"],738)
        self.assertEqual([(x["accepted_source_annotations"],x["next_id"]) for x in ix["systems"]],
                         [(210,"BZI-R0211"),(528,"ZWD-R0529")])
        self.assertEqual(ix["accepted_batches"][-1]["id"],"ChineseAstro-13SRC-Life")

    def test_03_previous_WenChang_was_only_source_navigation_marker(self):
        r=read(PREVIOUS)
        self.assertEqual(r["last_id"],"ZWD-R0528")
        self.assertEqual(r["records"][-1]["source_type"] if "source_type" in r["records"][-1]
                         else r["records"][-1]["source_line_type"],
                         "NEXT_AUXILIARY_STAR_BOUNDARY_NO_SUBSTANTIVE_WENCHANG_CLAIMS")
        self.assertEqual(r["records"][-1]["original_absolute_codepoint_offset"],30135)
        self.assertTrue(self.rows[0]["source_original_exact_Chinese_Wikitext_quote"].startswith(
            r["records"][-1]["exact_original_Chinese_Wikitext_quote"]))
        self.assertTrue(self.src["source_V13_WenChang_navigation_only_not_prior_substantive_claim"])

    def test_04_original_source_excerpt_exact_range_sha(self):
        self.assertEqual((self.src["source_excerpt_start_codepoint"],
                          self.src["source_excerpt_end_codepoint_exclusive"]),(30135,31937))
        self.assertEqual(EXCERPT.read_bytes(),self.full[30135:31937].encode("utf-8"))
        self.assertEqual(hash_data(EXCERPT.read_bytes()),self.src["source_excerpt_SHA256"])
        self.assertEqual(self.w["excerpt_codepoint_range"],[30135,31937])
        self.assertEqual(self.src["original_Brothers_next_section_codepoint"],37269)

    def test_05_four_original_source_auxiliary_group_counts_positions(self):
        data=[
            ("WenChang","文昌",30135,30665,16,4,True),
            ("WenQu","文曲",30665,31212,18,4,True),
            ("ZuoFu","左辅",31212,31613,13,0,True),
            ("YouBi","右弼",31613,31937,10,0,False)
        ]
        self.assertEqual(len(self.src["star_sections"]),4)
        for rec,(name,han,start,end,count,grades,female) in zip(self.src["star_sections"],data):
            self.assertEqual((rec["star_roman"],rec["star_native"]),(name,han))
            self.assertEqual((rec["original_codepoint_start"],rec["original_codepoint_end_exclusive"]),(start,end))
            self.assertEqual((rec["literal_source_line_count"],rec["original_palace_grade_rows"],
                              rec["has_independent_original_female_poem_heading"]),(count,grades,female))
            self.assertEqual(rec["original_source_segment_SHA256"],
                             hash_data(self.full[start:end].encode("utf-8")))

    def test_06_ids_exact_58_and_last_LuCun_navigation_only(self):
        self.assertEqual(len(self.rows),58)
        self.assertEqual([r["id"] for r in self.rows],[f"ZWD-R{i:04d}" for i in range(529,587)])
        self.assertEqual(self.rows[0]["id"],"ZWD-R0529")
        self.assertEqual(self.rows[-1]["id"],"ZWD-R0586")
        self.assertEqual(self.rows[-1]["source_type"],"NEXT_AUXILIARY_LUCUN_NAVIGATION_ONLY")
        self.assertEqual(self.rows[-1]["source_original_exact_Chinese_Wikitext_quote"],"禄存土，北斗")
        self.assertEqual(self.src["next_id"],"ZWD-R0587")

    def test_07_each_58_source_quote_exact_utf8_byte_and_codepoint(self):
        source_byid={x["id"]:x for x in self.w["original_quotes"]}
        self.assertEqual(len(source_byid),58)
        last=-1
        for r in self.rows:
            quote=r["source_original_exact_Chinese_Wikitext_quote"]
            utf=quote.encode("utf-8")
            cp=r["absolute_codepoint_offset"]
            bp=r["absolute_UTF8_byte_offset"]
            self.assertEqual(self.full[cp:cp+len(quote)],quote)
            self.assertEqual(self.raw[bp:bp+len(utf)],utf)
            self.assertEqual(hash_data(utf),r["source_quote_sha256"])
            self.assertEqual(len(utf),r["source_quote_UTF8_bytes"])
            self.assertEqual(cp-r["excerpt_relative_codepoint_offset"],30135)
            self.assertGreater(cp,last);last=cp
            self.assertEqual(source_byid[r["id"]]["UTF8_byte_offset"],bp)

    def test_08_verse_distribution_preserves_nonuniform_source(self):
        self.assertEqual(Counter(r["source_type"] for r in self.rows),{
            "auxiliary_star_profile_intro":4,
            "auxiliary_natal_narrative_condition":13,
            "auxiliary_palace_grade_condition":8,
            "historical_poem_heading":11,
            "historical_sex_coded_or_time_poem_verse":21,
            "NEXT_AUXILIARY_LUCUN_NAVIGATION_ONLY":1,
        })
        self.assertTrue(self.src["ZuoFu_YouBi_separate_palace_grade_rows_absent_from_original"])
        self.assertTrue(self.src["YouBi_distinct_female_poem_heading_absent_from_original"])
        self.assertFalse(self.src["star_sections"][-1]["has_independent_original_female_poem_heading"])

    def test_09_no_fake_palace_or_female_poems_for_ZuoFu_YouBi(self):
        for star in ("ZuoFu","YouBi"):
            self.assertFalse(any(r["source_type"]=="auxiliary_palace_grade_condition"
                                 for r in self.rows if r["star_roman"]==star))
        headings=[x["source_context"] for x in self.rows
                  if x["star_roman"]=="YouBi" and x["source_type"]=="historical_poem_heading"]
        self.assertEqual(headings,["male_life_poem_heading","time_limit_poem_heading"])

    def test_10_old_health_morality_not_validated_human_facts(self):
        risk=sum(r.get("mentions_historic_health_sex_morality_or_mortality",False) for r in self.rows)
        self.assertEqual(risk,15)
        self.assertFalse(self.src["historical_health_mortality_moral_gender_statements_empirical"])
        self.assertTrue(all(r["genuine_human_predictions_validated"]==0 for r in self.rows))
        self.assertTrue(all(r["runtime_astrology_promotions"]==0 for r in self.rows))

    def test_11_no_full_life_section_or_natal_model_claim(self):
        self.assertFalse(self.src["original_full_Life_palace_text_completed"])
        self.assertTrue(self.src["auxiliary_source_incomplete_after_LuCun"])
        self.assertEqual(self.src["next_unstudied_original_codepoint"],31937)
        self.assertTrue(self.full[31937:].startswith("禄存土，北斗"))
        self.assertTrue(self.full[37269:].startswith("===二兄弟==="))
        self.assertEqual(self.src["genuine_blinded_real_human_tests"],0)

    def test_12_old_Western_parent_unaltered_in_separate_source_branch(self):
        self.assertEqual(read(WEST)["records_count"],13044)
        self.assertEqual(read(WEST)["batches"][-1]["id"],"B07bc")
        self.assertTrue(self.src["BaZi_next_original_BZI_R0211_untouched"])

    def test_13_original_acceptance_file_sha_counts_and_no_prod(self):
        self.assertEqual(self.acc["Chinese_before"],738)
        self.assertEqual(self.acc["Chinese_after_if_accepted"],796)
        self.assertEqual(self.acc["ZiWei_after_if_accepted"],586)
        self.assertEqual(self.acc["BaZi_before_after"],210)
        self.assertEqual(self.acc["new_original_source_notes"],58)
        self.assertEqual(hash_data(SOURCE.read_bytes()),self.acc["source_notes_SHA256"])
        self.assertEqual(hash_data(WITNESS.read_bytes()),self.acc["source_witness_SHA256"])
        self.assertEqual(hash_data(EXCERPT.read_bytes()),self.acc["source_excerpt_SHA256"])

if __name__=="__main__":unittest.main()
