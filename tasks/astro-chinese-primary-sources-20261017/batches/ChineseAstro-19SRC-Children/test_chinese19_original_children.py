#!/usr/bin/env python3
"""Independent original Wikitext source tests for Zi Wei Children historical audit."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
T=ROOT/"tasks/astro-chinese-primary-sources-20261017"
FULL=T/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
OLD=T/"CHINESE_SOURCE_AUDIT_INDEX_V18.json"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
NOTES=B/"ZIWEI_CHILDREN_34_SOURCE_NOTES_V1.json"
WIT=B/"SOURCE_CHILDREN_34_EXACT_OFFSET_WITNESS_V1.json"
EXCERPT=B/"SOURCE_1963110_CHILDREN_EXACT_EXCERPT.txt"
ACCEPT=B/"ACCEPTANCE.json"
RAW_SHA="1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
OLD_SHA="d3bdefc69a441140b9b16ef82bd10aad786a3d31e9919e5baec821fbe009e9eb"
WEST_SHA="c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8"


def sha(raw:bytes)->str:
    return hashlib.sha256(raw).hexdigest()


def load(file:Path)->dict:
    return json.loads(file.read_text(encoding="utf-8"))


class OriginalChildrenSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=FULL.read_bytes()
        cls.text=cls.raw.decode("utf-8")
        cls.doc=load(NOTES)
        cls.records=cls.doc["records"]
        cls.wit=load(WIT)
        cls.accept=load(ACCEPT)

    def test_unchanged_original_full_Wikitext(self):
        self.assertEqual((len(self.raw),sha(self.raw)),(106736,RAW_SHA))
        self.assertEqual(len(self.text),48890)

    def test_previous_Chinese_V18_index_is_accepted_and_pinned(self):
        self.assertEqual(sha(OLD.read_bytes()),OLD_SHA)
        prior=load(OLD)
        self.assertEqual(prior["sum_source_annotations"],1004)
        self.assertEqual([(x["accepted_source_annotations"],x["next_id"]) for x in prior["systems"]],
                         [(210,"BZI-R0211"),(794,"ZWD-R0795")])
        self.assertEqual(prior["accepted_batches"][-1]["id"],"ChineseAstro-18SRC-Spouses")

    def test_separate_older_Western_snapshot_is_untouched(self):
        self.assertEqual(sha(WEST.read_bytes()),WEST_SHA)
        west=load(WEST)
        self.assertEqual((west["records_count"],west["batches"][-1]["id"]),(13044,"B07bc"))

    def test_exact_unmodified_excerpt_and_original_boundaries(self):
        self.assertEqual(EXCERPT.read_bytes(),self.text[39218:40563].encode("utf-8"))
        self.assertEqual(sha(EXCERPT.read_bytes()),"74dd9b6644241165851022fbd18e234517a44d245ca6f29c5ecb16a130ad27d4")
        self.assertTrue(self.text[39218:].startswith("===四子女==="))
        self.assertTrue(self.text[40563:].startswith("===五财帛==="))
        self.assertEqual(self.text.index("===五财帛===",39218),40563)

    def test_full_documentary_line_count_and_verse_tags(self):
        part=self.text[39218:40563]
        lines=[t.strip() for t in part.splitlines() if t.strip() and t.strip() not in ("<poem>","</poem>")]
        self.assertEqual(len(lines),33)
        self.assertEqual(len(self.records),34)
        self.assertEqual([x["literal_markup"] for x in self.doc["original_verse_markup"]],["<poem>","</poem>"])
        self.assertEqual([r["source_original_exact_Chinese_quote"] for r in self.records[:-1]],lines)

    def test_every_original_quote_matches_codepoint_and_UTF8(self):
        for row in self.records:
            text=row["source_original_exact_Chinese_quote"]
            cp=row["absolute_codepoint_offset"]
            bp=row["absolute_UTF8_byte_offset"]
            encoded=text.encode("utf-8")
            self.assertEqual(self.text[cp:cp+len(text)],text,row["id"])
            self.assertEqual(self.raw[bp:bp+len(encoded)],encoded,row["id"])
            self.assertEqual(bp,len(self.text[:cp].encode("utf-8")),row["id"])
            self.assertEqual(len(encoded),row["quote_UTF8_bytes"],row["id"])
            self.assertEqual(sha(encoded),row["quote_SHA256"],row["id"])

    def test_reversible_witness_has_all_exact_offsets(self):
        self.assertEqual(self.wit["source_full_SHA256"],RAW_SHA)
        self.assertEqual(self.wit["source_excerpt_SHA256"],sha(EXCERPT.read_bytes()))
        self.assertEqual(len(self.wit["original_quotes"]),34)
        for a,b in zip(self.records,self.wit["original_quotes"]):
            self.assertEqual((a["id"],a["absolute_codepoint_offset"],
                              a["absolute_UTF8_byte_offset"],a["quote_SHA256"],a["quote_UTF8_bytes"]),
                             (b["id"],b["codepoint"],b["UTF8_byte_offset"],
                              b["quote_SHA256"],b["quote_UTF8_bytes"]))

    def test_historic_method_preamble_not_star_predicates(self):
        self.assertEqual(sum(x["source_type"]=="SOURCE_METHOD_AND_CONDITION_PREMISE"
                             for x in self.records),4)
        self.assertEqual([x["original_line_index"] for x in self.records[1:5]],[1,2,3,4])

    def test_four_real_source_wraps_not_invented_star_predictions(self):
        self.assertEqual([x["original_line_index"] for x in self.records if
                          x["source_type"]=="SOURCE_CONTINUED_PREVIOUS_STAR_PROFILE_LINE"],[6,11,15,19])
        self.assertEqual([self.records[i]["original_source_group"] for i in [6,11,15,19]],
                         ["ZiWei","TianTong","TaiYin","TianXiang"])

    def test_all_source_ids_consecutive_without_reusing_old_navigation(self):
        self.assertEqual([x["id"] for x in self.records],[f"ZWD-R{x:04d}" for x in range(795,829)])
        self.assertEqual(self.records[0]["source_type"],"SOURCE_SECTION_HEADING")
        self.assertEqual(self.records[-1]["source_type"],"NEXT_WEALTH_SECTION_NAVIGATION_ONLY")
        self.assertEqual(self.records[-1]["absolute_codepoint_offset"],40563)
        self.assertEqual(self.doc["next_id"],"ZWD-R0829")

    def test_source_groups_not_a_natal_engine(self):
        self.assertFalse(self.doc["original_Ming_printing_independently_authenticated"])
        self.assertFalse(self.doc["all_twelve_house_source_sections_completed"])
        self.assertTrue(self.doc["source_family_counts_are_not_independent_forecasts"])

    def test_zero_actual_human_predictions_and_runtime_promotions(self):
        self.assertEqual((self.doc["human_blind_predictive_validations"],
                          self.doc["runtime_astrological_promotions"]),(0,0))
        for row in self.records:
            self.assertEqual((row["independent_human_blind_predictive_validations"],
                              row["runtime_astrological_promotions"]),(0,0))
            self.assertFalse(row["original_Ming_printing_independently_authenticated"])

    def test_acceptance_candidate_count_and_frozen_sha(self):
        meta=self.accept
        self.assertEqual((meta["Chinese_before"],meta["new_original_source_notes"],
                          meta["Chinese_after_if_accepted"]),(1004,34,1038))
        self.assertEqual((meta["ZiWei_before"],meta["ZiWei_after_if_accepted"],
                          meta["BaZi_retained"]),(794,828,210))
        self.assertEqual(meta["source_notes_SHA256"],sha(NOTES.read_bytes()))
        self.assertEqual(meta["source_excerpt_SHA256"],sha(EXCERPT.read_bytes()))
        self.assertEqual((meta["human_predictive_validations"],meta["runtime_promotions"]),(0,0))


if __name__=="__main__":
    unittest.main()
