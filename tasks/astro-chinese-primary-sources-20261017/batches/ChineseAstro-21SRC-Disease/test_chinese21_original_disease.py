#!/usr/bin/env python3
"""Source-only tests: historical Zi Wei Disease lines, not medical accuracy."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import unittest

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT / "tasks/astro-chinese-primary-sources-20261017"
SOURCE = T / "batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
OLD = T / "CHINESE_SOURCE_AUDIT_INDEX_V20.json"
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
NOTES = B / "ZIWEI_DISEASE_25_SOURCE_NOTES_V1.json"
WIT = B / "SOURCE_DISEASE_25_EXACT_OFFSET_WITNESS_V1.json"
EXCERPT = B / "SOURCE_1963110_DISEASE_EXACT_EXCERPT.txt"
RAW_SHA = "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
V20_SHA = "a6b051ed03f19f663d5a363af9a5c4efbf2ca2aea4997e94920023fdcf32f9b5"
WEST_SHA = "c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8"
EXCERPT_SHA = "73422add45e43982abdaf3aeadb3bcf7a6b479498a9fa7187336dba0be3b2f06"


def sha(raw: bytes) -> str:
    return sha256(raw).hexdigest()


def read(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


class OriginalDisease(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = SOURCE.read_bytes()
        cls.s = cls.raw.decode("utf-8")
        cls.doc = read(NOTES)
        cls.records = cls.doc["records"]
        cls.wit = read(WIT)
        cls.accept = read(B/"ACCEPTANCE.json")

    def test_immutable_full_transmitted_original_bytes(self):
        self.assertEqual((len(self.raw), sha(self.raw)), (106736, RAW_SHA))
        self.assertEqual(len(self.s), 48890)

    def test_previous_V20_and_BaZi_source_frontier(self):
        self.assertEqual(sha(OLD.read_bytes()), V20_SHA)
        old = read(OLD)
        self.assertEqual(old["sum_source_annotations"], 1069)
        self.assertEqual([(x["accepted_source_annotations"], x["next_id"]) for x in old["systems"]],
                         [(210, "BZI-R0211"), (859, "ZWD-R0860")])
        self.assertEqual(old["accepted_batches"][-1]["id"], "ChineseAstro-20SRC-Wealth")

    def test_old_inherited_Western_source_unchanged(self):
        self.assertEqual(sha(WEST.read_bytes()), WEST_SHA)
        old = read(WEST)
        self.assertEqual((old["records_count"],old["batches"][-1]["id"]), (13044,"B07bc"))

    def test_original_section_and_future_boundaries(self):
        self.assertEqual(EXCERPT.read_bytes(), self.s[41672:42541].encode("utf-8"))
        self.assertEqual(sha(EXCERPT.read_bytes()), EXCERPT_SHA)
        self.assertEqual(self.s.index("===六疾厄===",41672), 41672)
        self.assertEqual(self.s.index("===七迁移===",41672), 42541)

    def test_all_exact_literal_lines_and_verse_markup(self):
        part = self.s[41672:42541]
        lines = [x.strip() for x in part.splitlines()
                 if x.strip() and x.strip() not in ("<poem>","</poem>")]
        self.assertEqual(len(lines), 24)
        self.assertEqual([x["source_original_exact_Chinese_Wikitext_quote"]
                          for x in self.records[:-1]], lines)
        self.assertEqual([x[1] for x in self.doc["source_original_poem_markup"]],
                         ["<poem>","</poem>"])

    def test_all_original_codepoint_utf8_byte_quote_sha(self):
        for r in self.records:
            q = r["source_original_exact_Chinese_Wikitext_quote"]
            cp = r["absolute_codepoint_offset"]
            b = r["absolute_UTF8_byte_offset"]
            enc = q.encode("utf-8")
            self.assertEqual(self.s[cp:cp+len(q)],q,r["id"])
            self.assertEqual(self.raw[b:b+len(enc)],enc,r["id"])
            self.assertEqual(len(self.s[:cp].encode("utf-8")), b, r["id"])
            self.assertEqual(sha(enc),r["source_quote_SHA256"],r["id"])
            self.assertEqual(len(enc),r["source_quote_UTF8_bytes"],r["id"])

    def test_reversible_exact_witness_matches_quotes(self):
        self.assertEqual(self.wit["original_full_Wikitext_SHA256"],RAW_SHA)
        self.assertEqual(self.wit["source_excerpt_SHA256"], EXCERPT_SHA)
        self.assertEqual(len(self.wit["source_quotes"]),25)
        for row,w in zip(self.records,self.wit["source_quotes"]):
            self.assertEqual((row["id"],row["absolute_codepoint_offset"],
               row["absolute_UTF8_byte_offset"],row["source_quote_SHA256"]),
               (w["id"],w["original_cp"],w["original_utf8_offset"],w["quote_sha256"]))

    def test_preamble_and_actual_one_taiyin_continuation(self):
        self.assertEqual(self.records[0]["source_kind"], "SOURCE_SECTION_HEADING")
        self.assertEqual(self.records[1]["source_kind"], "SOURCE_GENERAL_METHOD_PREAMBLE")
        self.assertEqual(self.records[10]["source_kind"],
                         "SOURCE_CONTINUATION_PRIOR_TAIYIN_PROFILE")
        self.assertEqual(self.records[10]["source_historical_star_group"],"TaiYin")
        self.assertEqual(sum(r["source_kind"]=="SOURCE_HISTORICAL_STAR_CONDITION"
                             for r in self.records),21)

    def test_two_unrepaired_yangling_occurrences_in_different_contexts(self):
        variants=[(r["id"],r["source_historical_star_group"]) for r in self.records
                  if "羊铃" in r["source_original_exact_Chinese_Wikitext_quote"]]
        self.assertEqual(variants,[("ZWD-R0862","ZiWei"),("ZWD-R0882","YangLing")])
        self.assertEqual(self.doc["yangling_literal_occurrences"],2)
        self.assertTrue(self.doc["same_glyph_apparent_context_dependent_adverse_vs_favorable_tension_unresolved"])

    def test_next_heading_is_navigation_and_ids_exactly_sequential(self):
        self.assertEqual([r["id"] for r in self.records],
                         [f"ZWD-R{x:04d}" for x in range(860,885)])
        self.assertEqual(self.records[-1]["source_kind"],"NEXT_TRAVEL_PALACE_NAVIGATION_ONLY")
        self.assertEqual(self.records[-1]["absolute_codepoint_offset"],42541)
        self.assertEqual(self.doc["next_id"],"ZWD-R0885")

    def test_no_human_predictions_or_health_recommendations(self):
        self.assertTrue(self.doc["historic_health_claims_not_medical_advice_or_diagnosis"])
        self.assertFalse(self.doc["authentic_original_Ming_woodblock_collated"])
        self.assertEqual((self.doc["human_blind_predictions_validated"],self.doc["runtime_astrology_promotions"]),(0,0))
        for row in self.records:
            self.assertFalse(row["modern_health_medical_prediction_allowed"])
            self.assertFalse(row["independently_authenticated_Ming_print"])
            self.assertEqual((row["real_human_predictions_validated"],row["runtime_astrology_promotions"]),(0,0))

    def test_acceptance_candidate_counts_sha(self):
        a=self.accept
        self.assertEqual((a["old_Chinese_total"],a["new_original_source_only_notes"],
                          a["new_Chinese_total_if_accepted"]),(1069,25,1094))
        self.assertEqual(a["new_ZiWei_total_if_accepted"],884)
        self.assertEqual(a["new_source_notes_sha256"],sha(NOTES.read_bytes()))
        self.assertEqual(a["source_witness_sha256"],sha(WIT.read_bytes()))
        self.assertEqual(a["source_excerpt_sha256"],sha(EXCERPT.read_bytes()))


if __name__=="__main__":
    unittest.main()
