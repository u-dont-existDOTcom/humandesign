#!/usr/bin/env python3
"""Independent source-only evidence checks for Chinese Zi Wei V15."""
from __future__ import annotations
import hashlib
import json
import subprocess
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT / "tasks/astro-chinese-primary-sources-20261017"
RAW = T / "batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
NOTES = B / "ZIWEI_LIFE_SECOND_FOUR_AUXILIARY_SOURCE_NOTES_V1.json"
WITNESS = B / "SOURCE_LIFE_SECOND_FOUR_AUXILIARY_EXACT_OFFSET_WITNESS_V1.json"
EXCERPT = B / "SOURCE_1963110_LIFE_SECOND_FOUR_AUX_EXACT_EXCERPT.txt"
V14 = T / "CHINESE_SOURCE_AUDIT_INDEX_V14.json"
W_SHA = "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
V14_SHA = "c3a85dd972e010398b671730d86b2eea671db3da313494807bcb42e2c209c770"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


class OriginalChineseV15(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = RAW.read_bytes()
        cls.text = cls.raw.decode("utf-8")
        cls.data = load(NOTES)
        cls.records = cls.data["records"]
        cls.w = load(WITNESS)
        cls.metadata = load(B / "ACCEPTANCE.json")

    def test_pinned_full_transmitted_source(self):
        self.assertEqual((len(self.raw), sha(self.raw)), (106736, W_SHA))
        self.assertEqual(self.text.index("===二兄弟===", 31937), 37269)

    def test_old_accepted_index_bytewise_unchanged(self):
        self.assertEqual(sha(V14.read_bytes()), V14_SHA)
        index = load(V14)
        self.assertEqual(index["sum_source_annotations"], 796)
        self.assertEqual([i["accepted_source_annotations"] for i in index["systems"]], [210, 586])
        self.assertEqual(index["systems"][1]["next_id"], "ZWD-R0587")
        self.assertEqual(index["accepted_batches"][-1]["id"], "ChineseAstro-14SRC-Life")

    def test_exact_source_excerpt_from_pinned_text(self):
        a, b = self.data["source_excerpt_start_codepoint"], self.data["source_excerpt_end_codepoint_exclusive"]
        self.assertEqual((a, b), (31937, 33783))
        self.assertEqual(EXCERPT.read_bytes(), self.text[a:b].encode("utf-8"))
        self.assertEqual(sha(EXCERPT.read_bytes()), self.data["source_excerpt_SHA256"])
        self.assertEqual(self.data["source_excerpt_SHA256"], "f251de5988f4ef218de0a72e32f5c1c1d1c06a57db53158f61bc10bc252fb67d")

    def test_four_adjacent_original_star_segments(self):
        sections = self.data["star_sections"]
        self.assertEqual(
            [(x["star_native"],x["original_codepoint_start"],x["original_codepoint_end_exclusive"]) for x in sections],
            [("禄存",31937,32457),("魁钺",32457,32650),("擎羊",32650,33270),("陀罗",33270,33783)]
        )
        self.assertEqual([x["literal_source_line_count"] for x in sections],[14,6,17,16])
        for s in sections:
            part = self.text[s["original_codepoint_start"]:s["original_codepoint_end_exclusive"]]
            self.assertEqual(sha(part.encode("utf-8")),s["original_source_segment_SHA256"])

    def test_every_substantive_record_exact_unicode_and_utf8(self):
        substantive = self.records[:-1]
        self.assertEqual(len(substantive), 53)
        for row in substantive:
            quote = row["source_original_exact_Chinese_Wikitext_quote"]
            cp = row["absolute_codepoint_offset"]
            byte = row["absolute_UTF8_byte_offset"]
            encoded = quote.encode("utf-8")
            self.assertEqual(self.text[cp:cp+len(quote)], quote, row["id"])
            self.assertEqual(self.raw[byte:byte+len(encoded)], encoded, row["id"])
            self.assertEqual(len(encoded), row["source_quote_UTF8_bytes"], row["id"])
            self.assertEqual(sha(encoded), row["source_quote_sha256"], row["id"])
            self.assertEqual(byte,len(self.text[:cp].encode("utf-8")),row["id"])
            self.assertEqual(cp-31937,row["excerpt_relative_codepoint_offset"],row["id"])

    def test_ids_and_no_prior_navigation_double_count(self):
        self.assertEqual([r["id"] for r in self.records],[f"ZWD-R{i:04d}" for i in range(587,641)])
        self.assertEqual(self.data["next_id"],"ZWD-R0641")
        self.assertEqual(self.records[0]["source_original_exact_Chinese_Wikitext_quote"][:2], "禄存")
        self.assertEqual(self.records[-1]["source_type"],"NEXT_HUOXING_SOURCE_NAVIGATION_ONLY")
        self.assertEqual(self.records[-1]["star_native"], "火星")
        self.assertEqual(self.records[-1]["absolute_codepoint_offset"],33783)
        self.assertEqual(self.records[-1]["source_original_exact_Chinese_Wikitext_quote"],"火星，南斗浮星")

    def test_exact_witness_crosschecks(self):
        self.assertEqual(self.w["full_original_source_SHA256"],W_SHA)
        self.assertEqual(self.w["excerpt_SHA256"],sha(EXCERPT.read_bytes()))
        self.assertEqual(len(self.w["original_quotes"]),len(self.records))
        for row, witness in zip(self.records,self.w["original_quotes"]):
            self.assertEqual((witness["id"],witness["codepoint"],witness["UTF8_byte_offset"],witness["quote_SHA256"]),
                (row["id"],row["absolute_codepoint_offset"],row["absolute_UTF8_byte_offset"],row["source_quote_sha256"]))

    def test_original_qingyang_double_male_heading_not_normalized(self):
        src = self.text[32650:33270]
        self.assertEqual(src.count("擎羊入男命吉凶诀："),2)
        self.assertNotIn("擎羊入限吉凶诀",src)
        self.assertEqual([x[1] for x in self.data["star_sections"][2]["original_verbatim_headings"]].count("擎羊入男命吉凶诀："),2)
        self.assertTrue(self.data["QingYang_duplicate_original_male_verse_heading_preserved"])

    def test_original_tuoluo_female_markup_gap_not_filled(self):
        src = self.text[33270:33783]
        a=src.index("陀罗入女命吉凶诀")
        b=src.index("陀罗入限吉凶诀")
        self.assertNotIn("<poem>",src[a:b])
        self.assertTrue(self.data["TuoLuo_female_verse_markup_gap_preserved"])

    def test_original_kuiyue_single_heading_not_synthetic(self):
        src = self.text[32457:32650]
        self.assertEqual(src.count("魁钺入命限吉凶诀："),1)
        self.assertEqual(len(self.data["star_sections"][1]["original_verbatim_headings"]),1)
        self.assertTrue(self.data["KuiYue_absent_dedicated_male_female_time_headings_preserved"])

    def test_no_human_forecast_or_runtime_promotion(self):
        self.assertEqual((self.data["genuine_blinded_real_human_tests"],self.data["runtime_astrological_promotions"]),(0,0))
        for r in self.records:
            self.assertFalse(r["original_Ming_woodblock_imprint_authenticated"])
            self.assertEqual((r["genuine_human_predictions_validated"],r["runtime_astrology_promotions"]),(0,0))
        self.assertFalse(self.data["original_full_Life_palace_text_completed"])
        self.assertFalse(self.data["original_Ming_woodblock_imprint_verified"])

    def test_acceptance_counts_and_hashes(self):
        d=self.metadata
        self.assertEqual((d["Chinese_before"],d["new_original_source_notes"],d["Chinese_after_if_accepted"]),(796,54,850))
        self.assertEqual((d["ZiWei_before"],d["ZiWei_after_if_accepted"],d["BaZi_before_after"]),(586,640,210))
        self.assertEqual(sha(NOTES.read_bytes()),d["source_notes_SHA256"])
        self.assertEqual(sha(EXCERPT.read_bytes()),d["source_excerpt_SHA256"])
        self.assertEqual((d["actual_real_human_predictive_validations"],d["runtime_promotions"]),(0,0))

    def test_original_western_source_index_unmodified(self):
        p=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
        v=load(p)
        self.assertEqual((v["records_count"],v["batches"][-1]["id"]),(13044,"B07bc"))
        self.assertEqual(sha(p.read_bytes()),"c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8")
        rel=p.relative_to(ROOT).as_posix()
        check=subprocess.run(["git","rev-parse","--is-inside-work-tree"],cwd=ROOT,capture_output=True,text=True)
        if check.returncode == 0 and check.stdout.strip() == "true":
            orig=subprocess.run(["git","show","HEAD:"+rel],cwd=ROOT,capture_output=True,check=True).stdout
            self.assertEqual(p.read_bytes(),orig)


if __name__=="__main__":
    unittest.main()
