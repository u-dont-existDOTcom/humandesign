#!/usr/bin/env python3
"""Independent Zi Wei Volume II online-source final four-palace quote tests."""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
import unittest

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT / "tasks/astro-chinese-primary-sources-20261017"
FULL = T/"batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
OLD = T/"CHINESE_SOURCE_AUDIT_INDEX_V23.json"
WEST = ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
NOTES = B/"ZIWEI_FINAL_FOUR_123_SOURCE_NOTES_V1.json"
WIT = B/"SOURCE_FINAL_FOUR_123_EXACT_OFFSET_WITNESS_V1.json"
EXCERPT = B/"SOURCE_1963110_FINAL_FOUR_EXACT_EXCERPT.txt"
RAW_SHA = "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
OLD_SHA = "0bc5836d92c332a458a7d4a74dbb25488705344aa38df256dc721c6c5a673a0e"
WEST_SHA = "c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8"
SECTIONS = (
    ("Career",44429,45743,38,"fa97eb2aa98e9a8d87ca2ed754268d558f6a399a836a47ab1d86b6480aa7e97a"),
    ("Estate",45743,46678,24,"ccc5e2f6cf55e772c37c7f2f78e78d6b0d7ffb66bf529aaf74e7d6ba0a631efb"),
    ("Fortune",46678,47640,28,"d67acacd1d8e4ca1150267f6c8e955447f4f096d78637ae34e76c4c5e64e356c"),
    ("Parents",47640,48890,33,"80d8ed7db08ea75b48f1a728cb4b2cd4c1641a4bec063efe1bd7f93235bf9c04"),
)
def sha(raw: bytes) -> str: return sha256(raw).hexdigest()
def load(p:Path) -> dict: return json.loads(p.read_text(encoding="utf-8"))

class OriginalVolumeIIFinalFour(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = FULL.read_bytes()
        cls.text = cls.raw.decode("utf-8")
        cls.data = load(NOTES)
        cls.rows = cls.data["records"]
        cls.witness = load(WIT)
        cls.accept = load(B/"ACCEPTANCE.json")

    def test_full_online_wikitext_original_identity(self):
        self.assertEqual((len(self.raw), sha(self.raw)), (106736,RAW_SHA))
        self.assertEqual(len(self.text),48890)

    def test_previous_accepted_parent_bazi_and_ziwei(self):
        self.assertEqual(sha(OLD.read_bytes()),OLD_SHA)
        p=load(OLD)
        self.assertEqual(p["sum_source_annotations"],1146)
        self.assertEqual([(x["accepted_source_annotations"],x["next_id"]) for x in p["systems"]],[(210,"BZI-R0211"),(936,"ZWD-R0937")])
        self.assertEqual(p["accepted_batches"][-1]["id"],"ChineseAstro-23SRC-Servants")

    def test_inherited_older_western_registry_unchanged(self):
        self.assertEqual(sha(WEST.read_bytes()),WEST_SHA)
        self.assertEqual((load(WEST)["records_count"],load(WEST)["batches"][-1]["id"]),(13044,"B07bc"))

    def test_exact_four_adjacent_pinned_source_segments(self):
        for name,a,b,n,expected in SECTIONS:
            piece=self.text[a:b]
            self.assertEqual(sha(piece.encode("utf-8")),expected)
            self.assertEqual(piece[:3],"===")
            self.assertEqual(len([x for x in piece.splitlines() if x.strip() and x.strip() not in ("<poem>","</poem>","</onlyinclude>") and not x.startswith("{{footer|")]),n)
        self.assertEqual([s["source_palace"] for s in self.data["source_sections"]],[x[0] for x in SECTIONS])

    def test_whole_excerpt_through_online_volume_end(self):
        self.assertEqual(EXCERPT.read_bytes(),self.text[44429:48890].encode("utf-8"))
        self.assertEqual(sha(EXCERPT.read_bytes()),self.data["excerpt_SHA256"])
        self.assertEqual(self.data["excerpt_SHA256"],"0aef457fb4a4b9f46fffff4ad83bf10f8e2a90c87a47b0960ff8d01b942c59be")

    def test_all_123_historical_line_quotations_match_absolute_unicode_and_UTF8(self):
        self.assertEqual(len(self.rows),123)
        for row in self.rows:
            txt=row["original_exact_Chinese_Wikitext_quote"]
            cp=row["original_absolute_codepoint_offset"]
            byte=row["original_UTF8_byte_offset"]
            enc=txt.encode("utf-8")
            self.assertEqual(self.text[cp:cp+len(txt)],txt,row["id"])
            self.assertEqual(self.raw[byte:byte+len(enc)],enc,row["id"])
            self.assertEqual(len(self.text[:cp].encode("utf-8")),byte,row["id"])
            self.assertEqual(sha(enc),row["original_quote_SHA256"],row["id"])
            self.assertEqual(len(enc),row["original_quote_UTF8_bytes"],row["id"])
    def test_independent_witness_for_each_source_record(self):
        witness=self.witness
        self.assertEqual(witness["original_full_Wikitext_SHA256"],RAW_SHA)
        self.assertEqual(witness["source_excerpt_SHA256"],sha(EXCERPT.read_bytes()))
        self.assertEqual(len(witness["quoted_original_records"]),123)
        for a,b in zip(self.rows,witness["quoted_original_records"]):
            self.assertEqual((a["id"],a["original_absolute_codepoint_offset"],
                              a["original_UTF8_byte_offset"],a["original_quote_SHA256"]),
                             (b["id"],b["absolute_codepoint"],
                              b["absolute_UTF8_byte_offset"],b["quote_SHA256"]))

    def test_four_original_poem_markup_pairs(self):
        marks=self.data["source_poem_markup_records"]
        self.assertEqual(len(marks),8)
        self.assertEqual([x["quote"] for x in marks],["<poem>","</poem>"]*4)
        for mark in marks:
            q=mark["quote"];cp=mark["codepoint"]
            self.assertEqual(self.text[cp:cp+len(q)],q)
        self.assertEqual([x["historical_original_line_count"]
                          for x in self.data["source_sections"]],[38,24,28,33])

    def test_website_footer_excluded_but_original_bytes_preserved(self):
        meta=self.data["nonhistorical_Wikitext_footer_records_preserved_not_counted"]
        self.assertEqual(len(meta),2)
        self.assertEqual(meta[0]["quote"],"</onlyinclude>")
        self.assertTrue(meta[1]["quote"].startswith("{{footer|"))
        for item in meta:
            q=item["quote"];cp=item["codepoint"]
            self.assertEqual(self.text[cp:cp+len(q)],q)
            self.assertEqual(sha(q.encode("utf-8")),item["sha256"])
        self.assertEqual(sum("</onlyinclude>" in r["original_exact_Chinese_Wikitext_quote"] for r in self.rows),0)

    def test_career_poetry_is_not_five_independent_natal_laws(self):
        labels=[x["original_exact_Chinese_Wikitext_quote"] for x in self.rows
                if x["source_kind"]=="ORIGINAL_POEM_TITLE_NOT_NATAL_RULE"]
        self.assertEqual(labels,["定公卿","定两官府","定文官","定武官","定曹吏"])
        verses=[x for x in self.rows if x["source_kind"]=="ORIGINAL_HISTORIC_CAREER_VERSE"]
        self.assertEqual(len(verses),5)

    def test_continuation_lines_and_parental_method_kept_distinct(self):
        continued=[x for x in self.rows if x["source_kind"]=="ORIGINAL_CONTINUED_PRIOR_PROFILE_LINE"]
        self.assertEqual(len(continued),10)
        self.assertEqual([(x["source_palace"],x["original_source_line_index"])
                          for x in continued],[
                              ("Career",5),("Career",12),("Career",14),
                              ("Estate",5),
                              ("Fortune",4),("Fortune",6),("Fortune",15),
                              ("Parents",7),("Parents",9),("Parents",19)])
        self.assertEqual(sum(x["source_kind"]=="ORIGINAL_PARENTAL_SOURCE_METHOD_PREAMBLE"
                             for x in self.rows),4)

    def test_ids_and_future_source_are_ordered_without_fake_navigation(self):
        self.assertEqual([x["id"] for x in self.rows],
                         [f"ZWD-R{i:04d}" for i in range(937,1060)])
        self.assertEqual(self.data["first_record_id"],"ZWD-R0937")
        self.assertEqual(self.data["last_record_id"],"ZWD-R1059")
        self.assertEqual(self.data["next_documentary_id"],"ZWD-R1060")
        self.assertTrue(self.data["source_online_volume_II_end_reached"])

    def test_no_human_validation_no_ancient_authority(self):
        self.assertFalse(self.data["independently_authenticated_early_original_printing"])
        self.assertFalse(self.data["complete_original_critical_work_collated"])
        self.assertFalse(self.data["full_Chinese_natal_calendar_engine_verified"])
        self.assertEqual((self.data["real_human_predictive_validations"],
                          self.data["runtime_astrological_promotions"]),(0,0))
        for rec in self.rows:
            self.assertFalse(rec["ancient_Ming_printing_authenticated"])
            self.assertEqual((rec["independent_human_blind_forecasts_validated"],
                              rec["runtime_astrology_promotions"]),(0,0))

    def test_candidate_source_annotation_count_and_hashes(self):
        a=self.accept
        self.assertEqual((a["Chinese_before"],a["new_original_historical_text_notes"],
                          a["Chinese_after_if_accepted"]),(1146,123,1269))
        self.assertEqual((a["BaZi_unchanged"],a["ZiWei_after_if_accepted"]),(210,1059))
        self.assertEqual(a["source_note_sha256"],sha(NOTES.read_bytes()))
        self.assertEqual(a["source_witness_sha256"],sha(WIT.read_bytes()))
        self.assertEqual(a["source_excerpt_sha256"],sha(EXCERPT.read_bytes()))

if __name__ == "__main__":
    unittest.main()
