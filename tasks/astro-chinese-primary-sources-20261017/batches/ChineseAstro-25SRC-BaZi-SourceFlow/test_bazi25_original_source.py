#!/usr/bin/env python3
"""Independent pinned Di Tian Sui 19 text verification, not human prediction."""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
import unittest
import re

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT/"tasks/astro-chinese-primary-sources-20261017"
RAW = B/"evidence/DiTianSui_19_oldid844368.wikitext"
PREV = T/"CHINESE_SOURCE_AUDIT_INDEX_V24.json"
NOTES = B/"BAZI_DITIAN_SUI_19_6_SOURCE_NOTES_V1.json"
WIT = B/"SOURCE_DTS19_6_EXACT_OFFSET_WITNESS_V1.json"
MAN = B/"PINNED_DITIAN_SUI_19_SOURCE_MANIFEST_V1.json"
ACCEPT = B/"ACCEPTANCE.json"
RAW_SHA = "032a772c550dedb35aa130b835bb12d09dd3f3e89652aea382d7b00587ccf28d"
OLD_SHA = "ff40d64df1f4d2a5525591c5e4b5fa7e823c9c81e420093413b01cc292a919d1"

def sha(blob:bytes)->str:
    return sha256(blob).hexdigest()
def read(p:Path)->dict:
    return json.loads(p.read_text("utf-8"))

class SourceFlowOriginal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=RAW.read_bytes()
        cls.s=cls.raw.decode("utf-8")
        cls.data=read(NOTES)
        cls.rows=cls.data["records"]
        cls.witness=read(WIT)
        cls.accept=read(ACCEPT)

    def test_raw_original_full_revision_sha_and_size(self):
        self.assertEqual((len(self.raw),sha(self.raw)),(909,RAW_SHA))
        self.assertEqual(len(self.s),455)
        self.assertTrue(self.s.startswith("{{Novel|滴天髓|源流論|18|20|論}}"))

    def test_manifest_exact_original_revision_sha(self):
        manifest=read(MAN)["19"]
        self.assertEqual((manifest["pinned_oldid"],manifest["exact_utf8_bytes"],manifest["exact_sha256"]),
                         (844368,909,RAW_SHA))
        self.assertIn("oldid=844368",manifest["pinned_raw_url"])

    def test_previous_V24_BaZi_and_ZiWei_immutable_index(self):
        self.assertEqual(sha(PREV.read_bytes()),OLD_SHA)
        p=read(PREV)
        self.assertEqual(p["sum_source_annotations"],1269)
        self.assertEqual([(x["accepted_source_annotations"],x["next_id"]) for x in p["systems"]],
                         [(210,"BZI-R0211"),(1059,"ZWD-R1060")])

    def test_verse_commentary_historical_case_structure(self):
        d=self.data
        self.assertEqual(d["source_components"],{"transmitted_original_verse":1,
                         "transmitted_commentary":3,"historical_four_pillar_example":2})
        self.assertEqual([x["source_layer"] for x in self.rows],
                         ["transmitted_original_verse","transmitted_commentary",
                          "historical_four_pillar_example","transmitted_commentary",
                          "historical_four_pillar_example","transmitted_commentary"])
        self.assertEqual(len(self.rows),6)

    def test_all_six_verbatim_UTF8_original_quote_witnesses(self):
        self.assertEqual(len(self.witness["record_original_quote_witness"]),6)
        for r,w in zip(self.rows,self.witness["record_original_quote_witness"]):
            q=r["original_exact_Chinese_quote"]
            cp=r["source_absolute_codepoint_offset"]
            bp=r["source_absolute_UTF8_byte_offset"]
            encoded=q.encode("utf-8")
            self.assertEqual(self.s[cp:cp+len(q)],q,r["id"])
            self.assertEqual(self.raw[bp:bp+len(encoded)],encoded,r["id"])
            self.assertEqual(bp,len(self.s[:cp].encode("utf-8")),r["id"])
            self.assertEqual((sha(encoded),len(encoded)),
                             (r["quote_SHA256"],r["quote_UTF8_bytes"]),r["id"])
            self.assertEqual((w["id"],w["codepoint"],w["utf8_byte_offset"],w["source_quote_SHA256"]),
                             (r["id"],cp,bp,sha(encoded)),r["id"])
    def test_original_example_columns_both_tables(self):
        self.assertEqual(self.s.count("! 時 !! 日 !! 月 !! 年"),2)
        charts=[r for r in self.rows if r["source_layer"]=="historical_four_pillar_example"]
        self.assertEqual([r["original_column_order"] for r in charts],
                         [["hour","day","month","year"]]*2)
        self.assertEqual(charts[0]["historical_chart_pillars"],
                         {"hour":"丁巳","day":"戊申","month":"癸巳","year":"辛酉"})
        self.assertEqual(charts[1]["historical_chart_pillars"],
                         {"hour":"壬子","day":"癸丑","month":"壬戌","year":"癸丑"})
        self.assertEqual([r["original_exact_Chinese_quote"] for r in charts],
                         ["| 丁巳 || 戊申 || 癸巳 || 辛酉","| 壬子 || 癸丑 || 壬戌 || 癸丑"])

    def test_original_table_headings_exact_cp_byte_witness(self):
        heads=self.witness["original_source_column_order_time_day_month_year"]
        self.assertEqual(len(heads),2)
        for h in heads:
            q=h["original_exact_Chinese_header"]
            cp=h["original_codepoint_offset"]
            bp=h["original_UTF8_byte_offset"]
            self.assertEqual(q,"! 時 !! 日 !! 月 !! 年")
            self.assertEqual(self.s[cp:cp+len(q)],q)
            self.assertEqual(self.raw[bp:bp+len(q.encode("utf-8"))],q.encode("utf-8"))
            self.assertEqual(h["original_quote_SHA256"],sha(q.encode("utf-8")))

    def test_edition_differences_not_silently_repaired(self):
        self.assertEqual(self.rows[0]["original_exact_Chinese_quote"],
                         "何處起根源，流向可方住，機括此中求，知來亦知去。")
        self.assertIn("無從引助",self.rows[-1]["original_exact_Chinese_quote"])
        self.assertIn("所以為僧也",self.rows[-1]["original_exact_Chinese_quote"])
        self.assertNotIn("得從引助",self.rows[-1]["original_exact_Chinese_quote"])
        self.assertNotIn("所以為憎也",self.rows[-1]["original_exact_Chinese_quote"])
        self.assertTrue(self.data["source_variant_compare_longer_DiTianSuiChanWei_requires_independent_pin"])

    def test_original_two_outcomes_not_observed_human_accuracy(self):
        self.assertIn("所以富貴",self.rows[3]["original_exact_Chinese_quote"])
        self.assertIn("所以為僧",self.rows[5]["original_exact_Chinese_quote"])
        self.assertFalse(self.data["source_outcome_first_example_richness_independently_authenticated"])
        self.assertFalse(self.data["source_outcome_second_example_monk_independently_authenticated"])
        for r in self.rows:
            self.assertFalse(r["independent_historical_case_outcome_verified"])
            self.assertFalse(r["original_ancient_Ming_print_authorship_verified"])
            self.assertEqual((r["real_human_blind_predictive_validations"],
                              r["runtime_astrological_rule_promotions"]),(0,0))

    def test_next_record_ids_consecutive_no_duplicate(self):
        self.assertEqual([r["id"] for r in self.rows],
                         [f"BZI-R{i:04d}" for i in range(211,217)])
        self.assertEqual(self.data["next_id"],"BZI-R0217")
        self.assertEqual(self.data["next_ziwei_source_id_unchanged"],"ZWD-R1060")

    def test_candidate_acceptance_sha_counts_and_no_runtime(self):
        a=self.accept
        self.assertEqual((a["Chinese_before"],a["new_BaZi_source_only_records"],
                          a["Chinese_after_if_accepted"]),(1269,6,1275))
        self.assertEqual((a["BaZi_before"],a["BaZi_after_if_accepted"],
                          a["ZiWei_unchanged"]),(210,216,1059))
        self.assertEqual(a["source_notes_sha256"],sha(NOTES.read_bytes()))
        self.assertEqual(a["source_witness_sha256"],sha(WIT.read_bytes()))
        self.assertEqual((a["real_human_blind_predictions_validated"],
                          a["runtime_promotions"]),(0,0))

if __name__=="__main__":
    unittest.main()
