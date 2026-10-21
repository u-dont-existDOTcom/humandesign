#!/usr/bin/env python3
"""Verify Wikitext source fidelity of Zi Wei Wealth historical source."""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
import unittest

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
RAW=T/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V19.json"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
NOTES=B/"ZIWEI_WEALTH_31_SOURCE_NOTES_V1.json"
WIT=B/"SOURCE_WEALTH_31_EXACT_OFFSET_WITNESS_V1.json"
EXCERPT=B/"SOURCE_1963110_WEALTH_EXACT_EXCERPT.txt"
SOURCE_SHA="1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
OLD_SHA="52c5d51a281d5e641d2e029af81929e7a327d04eb5e1b510534d45b78c27fcb2"
WEST_SHA="c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8"


def hash_bytes(raw:bytes)->str:
    return sha256(raw).hexdigest()


def rd(p:Path)->dict:
    return json.loads(p.read_text(encoding="utf-8"))


class ExactWealthText(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=RAW.read_bytes()
        cls.text=cls.raw.decode("utf-8")
        cls.notes=rd(NOTES)
        cls.rules=cls.notes["records"]
        cls.witness=rd(WIT)
        cls.meta=rd(B/"ACCEPTANCE.json")

    def test_original_transmitted_source_pinned(self):
        self.assertEqual((len(self.raw),hash_bytes(self.raw)),(106736,SOURCE_SHA))
        self.assertEqual(len(self.text),48890)

    def test_previous_accepted_source_version_unchanged(self):
        self.assertEqual(hash_bytes(OLD.read_bytes()),OLD_SHA)
        parent=rd(OLD)
        self.assertEqual(parent["sum_source_annotations"],1038)
        self.assertEqual([(r["accepted_source_annotations"],r["next_id"]) for r in parent["systems"]],
                         [(210,"BZI-R0211"),(828,"ZWD-R0829")])

    def test_older_Western_index_byte_identical(self):
        self.assertEqual(hash_bytes(WEST.read_bytes()),WEST_SHA)
        self.assertEqual((rd(WEST)["records_count"],rd(WEST)["batches"][-1]["id"]),(13044,"B07bc"))

    def test_actual_source_excerpt_and_next_chapter_head(self):
        self.assertEqual(EXCERPT.read_bytes(),self.text[40563:41672].encode("utf-8"))
        self.assertEqual(hash_bytes(EXCERPT.read_bytes()),
                         "a7088436d0d098759c0417ebde5d09db32e3ef5473c67243713e0916c4780fab")
        self.assertTrue(self.text[40563:].startswith("===五财帛==="))
        self.assertTrue(self.text[41672:].startswith("===六疾厄==="))
        self.assertEqual(self.text.index("===六疾厄===",40563),41672)

    def test_all_original_text_lines_and_verse_markup(self):
        s=self.text[40563:41672]
        lines=[x.strip() for x in s.splitlines() if x.strip() and x.strip() not in ("<poem>","</poem>")]
        self.assertEqual(len(lines),30)
        self.assertEqual([r["exact_original_Chinese_Wikitext_quote"] for r in self.rules[:-1]],lines)
        self.assertEqual(len(self.notes["original_poem_markup"]),2)
        self.assertEqual([t[1] for t in self.notes["original_poem_markup"]],["<poem>","</poem>"])

    def test_all_line_UTF8_offset_and_SHA_reversible(self):
        for row in self.rules:
            txt=row["exact_original_Chinese_Wikitext_quote"]
            cp=row["absolute_codepoint_offset"]
            offset=row["absolute_UTF8_byte_offset"]
            encoded=txt.encode("utf-8")
            self.assertEqual(self.text[cp:cp+len(txt)],txt,row["id"])
            self.assertEqual(self.raw[offset:offset+len(encoded)],encoded,row["id"])
            self.assertEqual(len(self.text[:cp].encode("utf-8")),offset,row["id"])
            self.assertEqual(hash_bytes(encoded),row["quote_sha256"],row["id"])
            self.assertEqual(len(encoded),row["quote_UTF8_bytes"],row["id"])

    def test_six_real_physical_continuations_not_independent_profiles(self):
        r=[x["original_line_index"] for x in self.rules[:-1]
           if x["source_type"]=="ORIGINAL_CONTINUATION_OF_PREVIOUS_STAR_LINE"]
        self.assertEqual(r,[2,6,9,14,17,19])
        self.assertEqual([self.rules[i]["historical_clause_group"] for i in r],
                         ["ZiWei","WuQu","LianZhen","JuMen","TianLiang","PoJun"])

    def test_31_strict_consecutive_records_and_next_navigation(self):
        self.assertEqual([r["id"] for r in self.rules],[f"ZWD-R{i:04d}" for i in range(829,860)])
        self.assertEqual(self.rules[0]["source_type"],"ORIGINAL_SECTION_HEADING")
        self.assertEqual(self.rules[-1]["source_type"],"NEXT_DISEASE_SECTION_NAVIGATION_ONLY")
        self.assertEqual(self.rules[-1]["absolute_codepoint_offset"],41672)

    def test_exact_witness_crosscheck(self):
        self.assertEqual(self.witness["original_full_source_sha256"],SOURCE_SHA)
        self.assertEqual(self.witness["source_excerpt_sha256"],hash_bytes(EXCERPT.read_bytes()))
        self.assertEqual(len(self.witness["quotes"]),31)
        for x,y in zip(self.rules,self.witness["quotes"]):
            self.assertEqual((x["id"],x["absolute_codepoint_offset"],x["absolute_UTF8_byte_offset"],
                              x["quote_sha256"],x["quote_UTF8_bytes"]),
                             (y["id"],y["cp"],y["UTF8_offset"],y["sha256"],y["utf8_bytes"]))

    def test_historical_financial_claims_not_accepted_model(self):
        self.assertTrue(self.notes["source_finance_claims_are_not_investment_advice_or_real_human_outcomes"])
        self.assertEqual((self.notes["human_blind_predictions_validated"],
                          self.notes["runtime_astrology_promotions"]),(0,0))
        for row in self.rules:
            self.assertFalse(row["actual_real_person_financial_forecast_verified"])
            self.assertFalse(row["original_ancient_printing_verified"])

    def test_candidates_only_until_guarded_canonical_append(self):
        self.assertEqual((self.meta["Chinese_before"],self.meta["new_original_source_notes"],
                          self.meta["Chinese_after_if_accepted"]),(1038,31,1069))
        self.assertEqual((self.meta["ZiWei_before"],self.meta["ZiWei_after_if_accepted"],
                          self.meta["BaZi_preserved"]),(828,859,210))
        self.assertEqual(self.meta["source_notes_sha256"],hash_bytes(NOTES.read_bytes()))
        self.assertEqual(self.meta["source_excerpt_sha256"],hash_bytes(EXCERPT.read_bytes()))


if __name__=="__main__":
    unittest.main()
