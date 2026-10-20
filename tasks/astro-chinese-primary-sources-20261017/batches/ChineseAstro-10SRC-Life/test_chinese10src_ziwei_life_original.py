"""Original Zi Wei first four Life-palace star source records, no human proof.

Replays full SHA-pinned Simplified Wikitext oldid1963110 by exact UTF-8
source substrings and codepoint offsets for four star-by-star introductions,
all natal-palace conditional rows and sex/time-limited historical verses.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import unittest

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = ROOT / "tasks/astro-chinese-primary-sources-20261017"
ORIGINAL = TASK / "batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
INDEX_V9 = TASK / "CHINESE_SOURCE_AUDIT_INDEX_V9.json"
PREV_V8 = TASK / "batches/ChineseAstro-08/ZIWEI_VOL2_POSTBUREAU_FOUR_DIAGRAMS_19_SOURCE_NOTES_V1.json"
WESTERN = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
SOURCE = B / "ZIWEI_LIFE_PALACE_FIRST_FOUR_89_SOURCE_NOTES_V1.json"
WITNESS = B / "SOURCE_LIFE_FIRST_FOUR_89_OFFSET_WITNESS_V1.json"
EXCERPT = B / "SOURCE_1963110_LIFE_PALACE_FIRST_FOUR_EXACT_EXCERPT.txt"
ACCEPT = B / "ACCEPTANCE.json"
SOURCE_HASH = "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"


def read(p):
    return json.loads(p.read_text(encoding="utf-8"))


def digest(b):
    return sha256(b).hexdigest()


class OriginalChineseLifePalaceFirstFour(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = ORIGINAL.read_bytes()
        cls.txt = cls.raw.decode("utf-8")
        cls.src = read(SOURCE)
        cls.wit = read(WITNESS)
        cls.accept = read(ACCEPT)
        cls.rows = cls.src["records"]

    def test_01_original_source_raw_exact_SHA_and_bytes(self):
        self.assertEqual(len(self.raw), 106736)
        self.assertEqual(digest(self.raw), SOURCE_HASH)
        self.assertEqual(self.src["original_full_Wikitext_SHA256"], SOURCE_HASH)
        self.assertEqual(self.src["original_full_UTF8_bytes"], 106736)
        self.assertEqual(self.src["original_wikitext_revision_oldid"], 1963110)

    def test_02_old_Chinese_V9_exact_frontier_before_or_after_V10_append(self):
        old=read(INDEX_V9)
        self.assertEqual(digest(INDEX_V9.read_bytes()),
                         self.accept["accepted_previous_V9_index_sha256"])
        self.assertEqual(old["sum_source_annotations"],430)
        self.assertEqual(old["systems"][0]["next_id"],"BZI-R0211")
        self.assertEqual(old["systems"][1]["next_id"],"ZWD-R0221")
        self.assertEqual(old["accepted_batches"][-1]["id"],"ChineseAstro-09")

    def test_03_exact_main_section_and_four_star_source_positions(self):
        s=self.src
        self.assertEqual(s["source_original_life_palace_heading_codepoint"],19953)
        self.assertEqual(s["original_first_ZiWei_profile_codepoint"],19965)
        self.assertEqual(s["original_source_span_end_exclusive"],22909)
        self.assertEqual(s["original_Chinese_siblings_next_section_starts_codepoint"],37269)
        self.assertEqual(self.txt[19953:19965],"===一 命宫===\n\n")
        self.assertTrue(self.txt[22909:].startswith("天同水，南斗化福"))
        self.assertTrue(self.txt[37269:].startswith("===二兄弟==="))

    def test_04_source_excerpt_exact_self_contained_and_sha(self):
        s=self.src
        b=EXCERPT.read_bytes()
        self.assertEqual(digest(b),s["original_source_excerpt_sha256_UTF8"])
        self.assertEqual(len(b),s["original_source_excerpt_bytes"])
        self.assertEqual(b,self.txt[19953:22909].encode("utf-8"))
        self.assertEqual(self.wit["original_exact_source_codepoint_range"],[19953,22909])
        self.assertEqual(self.wit["original_excerpt_SHA256"],digest(b))

    def test_05_previous_original_source_heading_was_already_ZWD_R0220(self):
        prior=read(PREV_V8)
        self.assertEqual(prior["last_id"],"ZWD-R0220")
        self.assertEqual(prior["record_rows"][-1]["source_original_exact_quote"],
                         "===一 命宫===")
        self.assertTrue(self.src["source_life_palace_heading_already_accepted_as_ZWD_R0220"])
        self.assertFalse(any(r["exact_original_Chinese_Wikitext_quote"]=="===一 命宫===" for r in self.rows))

    def test_06_89_ids_contiguous_with_88_line_records_and_next_boundary(self):
        self.assertEqual(len(self.rows),89)
        self.assertEqual([r["id"] for r in self.rows],
                         [f"ZWD-R{n:04d}" for n in range(221,310)])
        self.assertEqual(self.rows[-1]["source_line_type"],
                         "NEXT_STAR_BOUNDARY_NO_SUBSTANTIVE_TIANTONG_CLAIMS")
        self.assertEqual(self.rows[-1]["exact_original_Chinese_Wikitext_quote"],
                         "天同水，南斗化福")
        self.assertEqual(self.src["next_id"],"ZWD-R0310")
        self.assertEqual(self.src["first_id"],"ZWD-R0221")
        self.assertEqual(self.src["last_id"],"ZWD-R0309")

    def test_07_four_source_star_groups_exact_counts(self):
        c=Counter(r["star_group_romanization"] for r in self.rows[:-1])
        self.assertEqual(c,{"ZiWei":22,"TianJi":20,"TaiYang":24,"WuQu":22})
        self.assertEqual(self.src["star_source_note_counts"],dict(c))
        self.assertEqual([x["star_roman"] for x in self.src["star_original_sections"]],
                         ["ZiWei","TianJi","TaiYang","WuQu"])

    def test_08_89_actual_quote_SHA_byte_and_codepoint_addresses(self):
        ledger={w["id"]:w for w in self.wit["exact_source_quote_provenance"]}
        self.assertEqual(len(ledger),89)
        previous=-1
        for item in self.rows:
            text=item["exact_original_Chinese_Wikitext_quote"]
            utf8=text.encode("utf-8")
            pos=item["original_absolute_codepoint_offset"]
            byte_pos=item["original_absolute_UTF8_byte_offset"]
            self.assertEqual(self.txt[pos:pos+len(text)],text)
            self.assertEqual(self.raw[byte_pos:byte_pos+len(utf8)],utf8)
            self.assertEqual(digest(utf8),item["source_quote_sha256_UTF8"])
            self.assertEqual(len(utf8),item["source_quote_UTF8_bytes"])
            self.assertEqual(pos-item["original_excerpt_relative_codepoint_offset"],19953)
            self.assertGreater(pos,previous)
            previous=pos
            self.assertEqual(ledger[item["id"]]["original_quote_sha256"],digest(utf8))
            self.assertEqual(ledger[item["id"]]["original_absolute_UTF8_byte_offset"],byte_pos)

    def test_09_source_line_types_exact_and_timed_poems_preserved(self):
        counts=Counter(r["source_line_type"] for r in self.rows)
        self.assertEqual(counts,{
            "star_profile_intro":4,
            "natal_narrative_condition":18,
            "natal_branch_condition":25,
            "historical_poem_heading":12,
            "historical_sex_coded_or_time_poem_verse":29,
            "NEXT_STAR_BOUNDARY_NO_SUBSTANTIVE_TIANTONG_CLAIMS":1,
        })
        for name in ("ZiWei","TianJi","TaiYang","WuQu"):
            group=[x for x in self.rows if x["star_group_romanization"]==name]
            heading=[x["source_section_context"] for x in group
                     if x["source_line_type"]=="historical_poem_heading"]
            self.assertEqual(heading,[
                "male_life_poem_heading","female_life_poem_heading",
                "time_limit_poem_heading"
            ])

    def test_10_all_25_palace_specific_grade_clauses_preserved(self):
        branch=Counter(x["star_group_romanization"] for x in self.rows
                       if x["source_line_type"]=="natal_branch_condition")
        self.assertEqual(branch,{"ZiWei":7,"TianJi":6,"TaiYang":6,"WuQu":6})
        self.assertEqual(sum(branch.values()),25)

    def test_11_source_life_palace_medical_and_sex_claims_are_not_health_advice(self):
        flagged=[x for x in self.rows if
                 x.get("contains_historic_high_risk_health_sex_or_morality_words",False)]
        self.assertEqual(len(flagged),24)
        self.assertTrue(self.src["earlier_source_body_appearance_health_gender_claims_are_historic_not_medical_truth"])
        for item in flagged:
            self.assertFalse(item["independent_human_personality_relationship_or_fate_validation"])
            self.assertFalse(item["runtime_astrological_rule_promoted"])

    def test_12_original_co_location_words_differ_from_general_verse_encounters(self):
        """'遇' encounter is not automatically identical to '同度' same palace."""
        lines=[x["exact_original_Chinese_Wikitext_quote"] for x in self.rows]
        self.assertTrue(any("紫微辰戌遇破军" in x for x in lines))
        self.assertTrue(any("辰戌宫得地与天相同度" in x for x in lines))
        self.assertTrue(any("丑未宫入庙与破军同度" in x for x in lines))
        self.assertFalse(self.src["original_14_star_condition_table_critical_verified"])

    def test_13_main_four_profiles_are_partial_not_whole_life_palace(self):
        self.assertTrue(self.src["only_four_of_many_life_palace_stars_covered"])
        self.assertFalse(self.src["all_life_palace_section_covered"])
        self.assertEqual(self.src["next_unstudied_star_native"],"天同")
        self.assertEqual(self.src["next_star_substantive_codepoint"],22909)

    def test_14_printed_original_Ming_imprint_not_authentic_from_Wikitext(self):
        self.assertFalse(self.src["original_old_Ming_woodblock_source_edition_authenticated"])
        self.assertTrue(all(not r["source_original_Ming_woodblock_imprint_authenticated"]
                            for r in self.rows))
        self.assertEqual(self.src["validated_actual_human_chart_predictive_tests"],0)

    def test_15_parallel_BaZi_and_older_Western_source_registry_preserved(self):
        idx=read(INDEX_V9)
        self.assertEqual(idx["systems"][0]["accepted_source_annotations"],210)
        self.assertEqual(self.accept["next_BZI"],"BZI-R0211")
        west=read(WESTERN)
        self.assertEqual(west["records_count"],13044)
        self.assertEqual(west["batches"][-1]["id"],"B07bc")

    def test_16_no_source_line_promoted_as_real_person_prediction(self):
        self.assertEqual(self.src["validated_actual_human_chart_predictive_tests"],0)
        self.assertEqual(self.src["production_astrological_rule_promotions"],0)
        for r in self.rows:
            self.assertEqual(r["predictions_issued_to_blind_real_people"],0)
            self.assertFalse(r["runtime_astrological_rule_promoted"])
            self.assertFalse(r["independent_human_personality_relationship_or_fate_validation"])

    def test_17_acceptance_new_counts_and_SHA(self):
        self.assertEqual(self.accept["previous_accepted_Chineses_source_total"],430)
        self.assertEqual(self.accept["new_historical_ziwei_source_annotations"],89)
        self.assertEqual(self.accept["ZiWei_after_if_accepted"],309)
        self.assertEqual(self.accept["BaZi_after_if_accepted"],210)
        self.assertEqual(self.accept["Chinese_after_if_accepted"],519)
        self.assertEqual(digest(SOURCE.read_bytes()),self.accept["source_notes_sha256"])
        self.assertEqual(digest(WITNESS.read_bytes()),self.accept["source_offset_witness_sha256"])
        self.assertEqual(digest(EXCERPT.read_bytes()),self.accept["source_excerpt_sha256"])


if __name__=="__main__":
    unittest.main()
