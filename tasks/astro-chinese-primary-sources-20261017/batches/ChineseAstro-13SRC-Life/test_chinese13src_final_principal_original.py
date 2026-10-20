"""Last two principal Zi Wei source profiles with literal original UTF8 offsets.

Complete 14 named principal star profile text ≠ full natal horoscope,
verified ancient printed edition, auxiliary star rules or human evidence.
"""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import unittest

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
RAW=T/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
INDEX=T/"CHINESE_SOURCE_AUDIT_INDEX_V12.json"
PREVIOUS=T/"batches/ChineseAstro-12SRC-Life/ZIWEI_LIFE_PALACE_THIRD_FOUR_83_SOURCE_NOTES_V1.json"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
SOURCE=B/"ZIWEI_LIFE_PALACE_FINAL_TWO_46_SOURCE_NOTES_V1.json"
WITNESS=B/"SOURCE_LIFE_FINAL_TWO_46_EXACT_OFFSET_WITNESS_V1.json"
EXCERPT=B/"SOURCE_1963110_LIFE_PALACE_FINAL_TWO_EXACT_EXCERPT.txt"
ACCEPT=B/"ACCEPTANCE.json"
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def h(b):return sha256(b).hexdigest()

class LastTwoPrincipalSourceText(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=RAW.read_bytes();cls.full=cls.raw.decode("utf-8")
        cls.s=rd(SOURCE);cls.w=rd(WITNESS);cls.a=rd(ACCEPT)
        cls.rows=cls.s["records"]

    def test_01_original_transmitted_chinese_text_hash_not_early_print(self):
        self.assertEqual(len(self.raw),106736)
        self.assertEqual(h(self.raw),
                         "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72")
        self.assertFalse(self.s["original_Ming_woodblock_imprint_authenticated"])
        self.assertEqual(self.s["original_oldid"],1963110)

    def test_02_prior_v12_exact_accepted_root(self):
        old=rd(INDEX)
        self.assertEqual(h(INDEX.read_bytes()),self.a["prior_V12_Chinese_source_index_SHA256"])
        self.assertEqual(old["sum_source_annotations"],692)
        self.assertEqual([(x["accepted_source_annotations"],x["next_id"]) for x in old["systems"]],
                         [(210,"BZI-R0211"),(482,"ZWD-R0483")])
        self.assertEqual(old["accepted_batches"][-1]["id"],"ChineseAstro-12SRC-Life")

    def test_03_old_QiSha_navigation_prefix_not_a_previous_description(self):
        old=rd(PREVIOUS)
        self.assertEqual(old["last_id"],"ZWD-R0482")
        self.assertEqual(old["records"][-1]["source_line_type"],
                         "NEXT_STAR_BOUNDARY_NO_SUBSTANTIVE_QISHA_CLAIMS")
        self.assertEqual(old["records"][-1]["original_absolute_codepoint_offset"],28621)
        self.assertTrue(self.rows[0]["exact_original_Chinese_Wikitext_quote"].startswith(
            old["records"][-1]["exact_original_Chinese_Wikitext_quote"]))
        self.assertTrue(self.s["previous_V12_QiSha_only_heading_prefix_already_in_R0482"])

    def test_04_source_excerpt_exact_and_next_Aux_boundary(self):
        self.assertEqual(self.s["original_excerpt_start_codepoint"],28621)
        self.assertEqual(self.s["original_excerpt_end_codepoint_exclusive"],30135)
        self.assertEqual(self.s["siblings_next_section_heading_codepoint"],37269)
        self.assertEqual(EXCERPT.read_bytes(),self.full[28621:30135].encode("utf-8"))
        self.assertEqual(h(EXCERPT.read_bytes()),self.s["original_excerpt_sha256"])
        self.assertEqual(self.w["original_excerpt_source_codepoint_range"],[28621,30135])

    def test_05_two_star_source_ranges_and_subsections(self):
        segments=[
            ("QiSha","七杀",28621,29332,22,7),
            ("PoJun","破军",29332,30135,23,6),
        ]
        self.assertEqual(len(self.s["star_original_sections"]),2)
        for row,(name,native,a,b,count,palaces) in zip(self.s["star_original_sections"],segments):
            self.assertEqual((row["star_roman"],row["original_star"]),(name,native))
            self.assertEqual((row["original_codepoint_start"],row["original_codepoint_end_exclusive"]),(a,b))
            self.assertEqual(row["source_line_annotation_count"],count)
            self.assertEqual(row["original_palace_line_count"],palaces)
            self.assertEqual(row["source_original_UTF8_SHA256"],h(self.full[a:b].encode("utf-8")))
        self.assertEqual(self.s["star_line_counts"],{"QiSha":22,"PoJun":23})

    def test_06_last_46_source_rows_identical_and_sequential(self):
        self.assertEqual(len(self.rows),46)
        self.assertEqual([x["id"] for x in self.rows],
                         [f"ZWD-R{x:04d}" for x in range(483,529)])
        self.assertEqual(self.s["first_id"],"ZWD-R0483")
        self.assertEqual(self.s["last_id"],"ZWD-R0528")
        self.assertEqual(self.s["next_id"],"ZWD-R0529")

    def test_07_all_46_original_utf8_quotes_exact_codepoint_byte_sha(self):
        byid={x["id"]:x for x in self.w["exact_quote_offsets"]}
        self.assertEqual(len(byid),46)
        prev=-1
        for rec in self.rows:
            quote=rec["exact_original_Chinese_Wikitext_quote"]
            coded=quote.encode("utf-8")
            cp=rec["original_absolute_codepoint_offset"]
            bp=rec["original_absolute_UTF8_byte_offset"]
            self.assertEqual(self.full[cp:cp+len(quote)],quote)
            self.assertEqual(self.raw[bp:bp+len(coded)],coded)
            self.assertEqual(h(coded),rec["source_quote_sha256_UTF8"])
            self.assertEqual(len(coded),rec["source_quote_UTF8_bytes"])
            self.assertEqual(cp-rec["original_excerpt_relative_codepoint_offset"],28621)
            self.assertGreater(cp,prev);prev=cp
            self.assertEqual(byid[rec["id"]]["original_UTF8_byte_offset"],bp)
            self.assertEqual(byid[rec["id"]]["quote_SHA256"],h(coded))

    def test_08_original_source_types_covers_verses_and_palaces(self):
        self.assertEqual(Counter(x["source_line_type"] for x in self.rows),{
            "star_profile_intro":2,
            "natal_narrative_condition":8,
            "natal_branch_condition":13,
            "historical_poem_heading":6,
            "historical_sex_coded_or_time_poem_verse":16,
            "NEXT_AUXILIARY_STAR_BOUNDARY_NO_SUBSTANTIVE_WENCHANG_CLAIMS":1,
        })
        for star in ("QiSha","PoJun"):
            heads=[r["source_section_context"] for r in self.rows
                   if r["star_group_romanization"]==star and
                   r["source_line_type"]=="historical_poem_heading"]
            self.assertEqual(heads,[
                "male_life_poem_heading","female_life_poem_heading",
                "time_limit_poem_heading"
            ])

    def test_09_last_principal_profile_is_complete_but_Life_palace_not(self):
        self.assertTrue(self.s["all_fourteen_principal_star_profiles_now_source_covered"])
        self.assertTrue(self.s["all_fourteen_principal_star_profiles_end_at_this_batch"])
        self.assertTrue(self.s["auxiliary_star_text_from_WenChang_through_Siblings_heading_unstudied"])
        self.assertFalse(self.s["complete_Life_palace_source_study"])
        self.assertEqual(self.s["next_unstudied_star_native"],"文昌")

    def test_10_next_WenChang_prefix_only_no_aux_rules_in_this_batch(self):
        self.assertEqual(self.s["next_unstudied_star_original_codepoint"],30135)
        self.assertTrue(self.full[30135:].startswith("文昌金，南北斗"))
        self.assertTrue(self.full[37269:].startswith("===二兄弟==="))
        self.assertEqual(self.rows[-1]["source_line_type"],
                         "NEXT_AUXILIARY_STAR_BOUNDARY_NO_SUBSTANTIVE_WENCHANG_CLAIMS")
        self.assertEqual(self.rows[-1]["exact_original_Chinese_Wikitext_quote"],
                         "文昌金，南北斗")

    def test_11_source_old_mortality_sex_moralism_not_modern_clinical_science(self):
        self.assertEqual(sum(x.get("contains_historic_health_sex_morality_or_death_terms",False)
                             for x in self.rows),23)
        self.assertFalse(self.s["original_claims_of_sex_health_disability_and_longevity_medically_true"])
        self.assertTrue(all(not x["medical_or_moral_advice_authorized"] for x in self.rows))
        self.assertTrue(all(not x["genuine_human_behavior_or_fate_validated"] for x in self.rows))

    def test_12_parallel_bazi_western_parent_unchanged(self):
        old=rd(INDEX)
        self.assertEqual(old["systems"][0]["accepted_source_annotations"],210)
        self.assertEqual(self.a["next_BZI"],"BZI-R0211")
        west=rd(WEST)
        self.assertEqual(west["records_count"],13044)
        self.assertEqual(west["batches"][-1]["id"],"B07bc")

    def test_13_full_chart_model_and_actual_person_validation_still_unverified(self):
        self.assertEqual(self.s["genuine_real_human_predictive_validations"],0)
        self.assertEqual(self.s["runtime_forecast_promotions"],0)
        self.assertFalse(self.s["original_Ming_woodblock_imprint_authenticated"])
        self.assertTrue(all(x["actual_forward_reverse_blind_people_tested"]==0 for x in self.rows))

    def test_14_source_acceptance_count_and_archive_SHA_fields(self):
        self.assertEqual(self.a["Chinese_before"],692)
        self.assertEqual(self.a["Chinese_after_if_accepted"],738)
        self.assertEqual(self.a["ZiWei_after_if_accepted"],528)
        self.assertEqual(self.a["BaZi_retained"],210)
        self.assertEqual(self.a["new_original_source_only_annotations"],46)
        self.assertEqual(h(SOURCE.read_bytes()),self.a["note_SHA256"])
        self.assertEqual(h(WITNESS.read_bytes()),self.a["witness_SHA256"])
        self.assertEqual(h(EXCERPT.read_bytes()),self.a["excerpt_SHA256"])

if __name__=="__main__":unittest.main()
