#!/usr/bin/env python3
"""Independent original Chinese online text tests for Zi Wei V16."""
import hashlib,json,subprocess,unittest
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
RAW=T/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
PREVIOUS=T/"CHINESE_SOURCE_AUDIT_INDEX_V15.json"
NOTES=B/"ZIWEI_LIFE_REMAINING_105_SOURCE_NOTES_V1.json"
WIT=B/"SOURCE_LIFE_REMAINING_105_EXACT_OFFSET_WITNESS_V1.json"
EXCERPT=B/"SOURCE_1963110_LIFE_REMAINING_EXACT_EXCERPT.txt"
RAW_SHA="1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
OLD_SHA="a5bf0e0cc4bd801b209caa98e1bd58558f2155fd73ba9a055d516472076311ad"
WEST_SHA="c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8"
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text(encoding="utf-8"))


class OriginalZiWeiV16(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=RAW.read_bytes();cls.text=cls.raw.decode("utf-8")
        cls.data=load(NOTES);cls.records=cls.data["records"]
        cls.w=load(WIT);cls.a=load(B/"ACCEPTANCE.json")

    def test_immutable_online_volume(self):
        self.assertEqual((len(self.raw),sha(self.raw)),(106736,RAW_SHA))
        self.assertEqual(self.text.index("===二兄弟===",33783),37269)

    def test_previous_accepted_v15_unmodified(self):
        self.assertEqual(sha(PREVIOUS.read_bytes()),OLD_SHA)
        prior=load(PREVIOUS)
        self.assertEqual(prior["sum_source_annotations"],850)
        self.assertEqual([x["accepted_source_annotations"] for x in prior["systems"]],[210,640])
        self.assertEqual(prior["accepted_batches"][-1]["id"],"ChineseAstro-15SRC-Life")

    def test_exact_literal_unedited_source_excerpt(self):
        self.assertEqual(EXCERPT.read_bytes(),self.text[33783:37269].encode("utf-8"))
        self.assertEqual(sha(EXCERPT.read_bytes()),self.data["source_excerpt_SHA256"])
        self.assertEqual(self.data["source_excerpt_SHA256"],"87a3b9316723f3acb4c02a52cacb39644d3261cb66a02da179d7344f06a728e9")

    def test_fifteen_contiguous_actual_source_spans(self):
        groups=self.data["source_segments"]
        self.assertEqual(len(groups),15)
        self.assertEqual([x["literal_source_line_count"] for x in groups],[7,7,9,6,8,3,2,4,5,8,11,11,16,5,2])
        self.assertEqual(groups[0]["original_codepoint_start"],33783)
        self.assertEqual(groups[-1]["original_codepoint_end_exclusive"],37269)
        for a,b in zip(groups,groups[1:]):
            self.assertEqual(a["original_codepoint_end_exclusive"],b["original_codepoint_start"])
        for x in groups:
            part=self.text[x["original_codepoint_start"]:x["original_codepoint_end_exclusive"]]
            self.assertEqual(sha(part.encode("utf-8")),x["original_source_segment_SHA256"])

    def test_all_104_lines_original_codepoints_and_utf8(self):
        self.assertEqual(len(self.records[:-1]),104)
        for r in self.records[:-1]:
            txt=r["source_original_exact_Chinese_Wikitext_quote"]
            cp=r["absolute_codepoint_offset"]
            byt=r["absolute_UTF8_byte_offset"]
            enc=txt.encode("utf-8")
            self.assertEqual(self.text[cp:cp+len(txt)],txt,r["id"])
            self.assertEqual(self.raw[byt:byt+len(enc)],enc,r["id"])
            self.assertEqual(byt,len(self.text[:cp].encode("utf-8")),r["id"])
            self.assertEqual((len(enc),sha(enc)),(r["source_quote_UTF8_bytes"],r["source_quote_sha256"]))

    def test_sequential_ids_and_new_siblings_navigation(self):
        self.assertEqual([r["id"] for r in self.records],[f"ZWD-R{i:04d}" for i in range(641,746)])
        self.assertEqual((self.records[0]["original_source_native_name"],self.records[0]["absolute_codepoint_offset"]),("火星",33783))
        last=self.records[-1]
        self.assertEqual((last["original_source_native_name"],last["absolute_codepoint_offset"]),("兄弟",37269))
        self.assertEqual(last["source_type"],"NEXT_ORIGINAL_BROTHERS_SECTION_NAVIGATION_ONLY")
        self.assertEqual(last["source_original_exact_Chinese_Wikitext_quote"],"===二兄弟===")
        self.assertEqual(self.data["next_id"],"ZWD-R0746")

    def test_original_two_star_combination_not_synthetically_split(self):
        self.assertTrue(self.text[34306:34620].startswith("火铃二星入男命吉凶诀"))
        self.assertTrue(self.text[35051:35156].startswith("地劫天空同入限吉凶诀"))
        self.assertEqual(self.data["source_segments"][2]["source_group"],"HuoLingCombined")
        self.assertEqual(self.data["source_segments"][5]["source_group"],"JieKongCombined")
        self.assertTrue(self.data["combined_HuoLing_and_JieKong_groups_unseparated"])

    def test_original_mixed_chinese_character_variants(self):
        fragment=self.text[35522:35758]
        self.assertIn("化禄入命断诀：",fragment)
        self.assertIn("化祿入限斷訣：",fragment)
        self.assertTrue(self.data["mixed_traditional_simplified_HuaLu_verses_retained"])

    def test_frozen_quote_witness_exact_crosscheck(self):
        self.assertEqual(self.w["source_full_SHA256"],RAW_SHA)
        self.assertEqual(len(self.w["original_quotes"]),105)
        for r,w in zip(self.records,self.w["original_quotes"]):
            self.assertEqual((w["id"],w["codepoint"],w["UTF8_byte_offset"],w["quote_SHA256"]),
                (r["id"],r["absolute_codepoint_offset"],r["absolute_UTF8_byte_offset"],r["source_quote_sha256"]))

    def test_source_not_medical_legal_or_empirical(self):
        self.assertEqual((self.data["genuine_blinded_real_human_tests"],self.data["runtime_astrological_promotions"]),(0,0))
        self.assertFalse(self.data["critically_collated_ancient_Life_palace_imprint"])
        self.assertFalse(self.data["other_11_online_house_sections_studied_completely"])
        for r in self.records:
            self.assertEqual((r["human_blinded_predictions_validated"],r["runtime_astrology_promotions"]),(0,0))
            self.assertFalse(r["original_Ming_woodblock_imprint_authenticated"])

    def test_expected_provisional_acceptance_counts(self):
        self.assertEqual((self.a["Chinese_before"],self.a["new_original_source_notes"],self.a["Chinese_after_if_accepted"]),(850,105,955))
        self.assertEqual((self.a["ZiWei_before"],self.a["ZiWei_after_if_accepted"],self.a["BaZi_before_after"]),(640,745,210))
        self.assertEqual((self.a["first_id"],self.a["last_id"],self.a["next_id"]),("ZWD-R0641","ZWD-R0745","ZWD-R0746"))
        self.assertEqual(sha(NOTES.read_bytes()),self.a["source_notes_SHA256"])
        self.assertEqual(sha(EXCERPT.read_bytes()),self.a["source_excerpt_SHA256"])

    def test_old_western_immutable_source(self):
        p=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
        self.assertEqual(sha(p.read_bytes()),WEST_SHA)
        w=load(p)
        self.assertEqual((w["records_count"],w["batches"][-1]["id"]),(13044,"B07bc"))
        check=subprocess.run(["git","rev-parse","--is-inside-work-tree"],cwd=ROOT,capture_output=True,text=True)
        if check.returncode==0 and check.stdout.strip()=="true":
            prior=subprocess.run(["git","show","HEAD:"+p.relative_to(ROOT).as_posix()],cwd=ROOT,capture_output=True,check=True).stdout
            self.assertEqual(p.read_bytes(),prior)


if __name__=="__main__":
    unittest.main()
