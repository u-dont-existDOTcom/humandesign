"""Zi Wei source auxiliary stars and five elemental-bureau original diagrams."""

import hashlib
import json
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
P = B.parents[1]
ROOT = B.parents[3]
FULL_SOURCE_SHA = "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(data):
    return hashlib.sha256(data).hexdigest()


class SourceAuxiliaryBureaus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = j(B / "ZIWEI_VOLUME2_AUX_STARS_FIVE_BUREAU_40_SOURCE_NOTES_V1.json")
        cls.witness = j(B / "SOURCE_1963110_AUXILIARY_BUREAU_WITNESS_V1.json")
        cls.excerpt = (B / "SOURCE_1963110_AUXILIARY_AND_BUREAU_EXCERPT.txt").read_text(
            encoding="utf-8"
        )
        cls.notes = cls.source["record_rows"]
        cls.proof = cls.witness["quote_receipts"]

    def test_original_1963110_full_source_sha_witness(self):
        self.assertEqual(self.source["pinned_original_volume2_raw_oldid"], 1963110)
        self.assertEqual(self.source["pinned_original_volume2_full_raw_SHA256"], FULL_SOURCE_SHA)
        self.assertEqual(self.witness["whole_raw_original_SHA256"], FULL_SOURCE_SHA)
        self.assertEqual(self.source["pinned_original_volume2_full_raw_bytes"], 106736)

    def test_original_source_excerpt_exact_SHA(self):
        self.assertEqual(
            sha(self.excerpt.encode("utf-8")), self.source["full_original_excerpt_SHA256"]
        )
        self.assertEqual(
            self.source["full_original_excerpt_SHA256"], self.witness["excerpt_SHA256"]
        )
        self.assertEqual(
            len(self.excerpt.encode("utf-8")), self.source["original_source_excerpt_bytes"]
        )

    def test_no_duplicate_ZiWei_earlier_source_records(self):
        prior = j(P / "CHINESE_SOURCE_AUDIT_INDEX_V6.json")
        self.assertEqual(prior["sum_source_annotations"], 315)
        self.assertEqual(prior["systems"][0]["accepted_source_annotations"], 154)
        self.assertEqual(prior["systems"][1]["accepted_source_annotations"], 161)
        self.assertEqual(prior["systems"][1]["next_id"], "ZWD-R0162")
        old = j(P / "batches/ChineseAstro-04/ZIWEI_VOLUME2_LIFE_BODY_TAXONOMY_SOURCE_NOTES_V1.json")
        self.assertEqual(old["records"][-1]["id"], "ZWD-R0161")

    def test_40_individually_anchored_source_rows(self):
        self.assertEqual(len(self.notes), 40)
        self.assertEqual(len(self.proof), 40)
        self.assertEqual([x["id"] for x in self.notes], [f"ZWD-R{i:04d}" for i in range(162, 202)])
        self.assertEqual(self.source["first_id"], "ZWD-R0162")
        self.assertEqual(self.source["next_id"], "ZWD-R0202")

    def test_original_source_quote_offset_exact(self):
        offset = self.source["original_text_segment_absolute_start_codepoint"]
        for r, p in zip(self.notes, self.proof, strict=True):
            at = r["original_excerpt_relative_character_offset"]
            quote = r["source_original_verbatim_chinese_anchor"]
            self.assertEqual(self.excerpt[at : at + len(quote)], quote)
            self.assertEqual(r["original_full_source_character_offset"], offset + at)
            self.assertEqual(r["original_quote_utf8_SHA256"], sha(quote.encode("utf-8")))
            self.assertEqual(p["verbatim_chinese"], quote)
            self.assertEqual(r["id"], p["id"])
            self.assertFalse(r["runtime_promoted"])

    def test_29_auxiliary_star_lines_and_exclusion_not_regular_18(self):
        types = [x["source_type"] for x in self.notes]
        self.assertEqual(types.count("auxiliary_status"), 1)
        self.assertEqual(types.count("aux_star"), 29)
        self.assertEqual(types.count("bureau_poem"), 5)
        self.assertEqual(types.count("bureau_original_grid"), 5)
        self.assertEqual(
            self.notes[0]["source_original_verbatim_chinese_anchor"], "魁钺天马亦是吉星俱不入正曜"
        )

    def test_historical_auspicious_and_illness_claims_not_live(self):
        for r in self.notes:
            self.assertFalse(r["source_original_good_illness_crime_wealth_omens_personal_accuracy"])
            self.assertFalse(r["independently_validated_real_human_prediction"])
        self.assertIn("病符主病", self.excerpt)
        self.assertIn("大小耗属火小耗钱财大耗退祖", self.excerpt)

    def test_confusable_but_distinct_official_star_names(self):
        names = [x["source_original_verbatim_chinese_anchor"] for x in self.notes]
        self.assertIn("官府主官符", names)
        self.assertIn("官符火", names)
        self.assertNotEqual("官府主官符", "官符火")

    def test_5_bureau_poem_grid_pairs_and_hash(self):
        grids = self.witness["diagram_reversible_witnesses"]
        self.assertEqual(len(grids), 5)
        self.assertEqual(
            [x["bureau"] for x in grids], ["水二局", "木三局", "金四局", "土五局", "火六局"]
        )
        a = self.source["original_text_segment_absolute_start_codepoint"]
        for g in grids:
            txt = g["diagram_content"]
            st = g["original_codepoint_start"] - a
            en = g["original_codepoint_end"] - a
            self.assertEqual(self.excerpt[st:en], txt)
            self.assertEqual(sha(txt.encode("utf-8")), g["original_utf8_sha256"])
            self.assertIn(g["bureau"], txt)
            self.assertFalse(g["source_day_to_palace_original_diagram_interpretation_verified"])

    def test_bureau_verbal_starts_are_transcribed_without_placement_engine(self):
        poems = [
            x["source_original_verbatim_chinese_anchor"]
            for x in self.notes
            if x["source_type"] == "bureau_poem"
        ]
        self.assertEqual(len(poems), 5)
        self.assertTrue(poems[0].startswith("坎水宫中二岁行"))
        self.assertTrue(poems[1].startswith("生逢木宫三岁起"))
        self.assertTrue(poems[2].startswith("紫微金宫四岁花"))
        self.assertTrue(poems[3].startswith("戌土五龙居其中"))
        self.assertTrue(poems[4].startswith("离火宫中六岁奇"))

    def test_source_is_not_expert_diplomatic_print(self):
        self.assertFalse(self.source["earliest_original_woodblock_attribution_verified"])
        self.assertFalse(self.source["separate_independent_classical_Chinese_expert_review"])
        self.assertTrue(self.witness["original_visual_tables_not_calendar_chart_engine"])

    def test_no_real_year_month_day_birth_engine_claim(self):
        self.assertFalse(self.source["original_diagrams_decode_consistency_verified"])
        self.assertFalse(self.source["original_lunisolar_year_to_birth_date_hour_verified"])
        self.assertEqual(self.source["independent_real_person_predictions_validated"], 0)
        self.assertEqual(self.source["runtime_promotions"], 0)

    def test_aux_lines_not_replaced_with_previous_b04_main_stars(self):
        old = j(P / "batches/ChineseAstro-04/ZIWEI_VOLUME2_LIFE_BODY_TAXONOMY_SOURCE_NOTES_V1.json")
        self.assertEqual(old["records"][-1]["id"], "ZWD-R0161")
        self.assertTrue(any("火玲星" in r["original_chinese_anchor"] for r in old["records"]))
        self.assertTrue(self.source["original_18_regular_stars_source_boundary_preserved"])

    def test_no_lilly_index_mutation(self):
        west = j(
            ROOT
            / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
        )
        self.assertEqual(west["records_count"], 12611)

    def test_source_zero_high_stakes_runtime(self):
        for r in self.notes:
            self.assertFalse(r["source_original_early_print_authenticity_verified"])
            self.assertFalse(r["source_traditional_day_to_palace_bureau_engine_verified"])
            self.assertFalse(r["source_full_lunisolar_leapmonth_birth_engine_verified"])
            self.assertFalse(r["runtime_promoted"])


def one_source_annotation(i):
    def test(self):
        note = self.notes[i]
        receipt = self.proof[i]
        self.assertEqual(note["id"], f"ZWD-R{162 + i:04d}")
        self.assertEqual(receipt["utf8_quote_sha256"], note["original_quote_utf8_SHA256"])
        self.assertFalse(note["runtime_promoted"])

    return test


for i in range(40):
    setattr(
        SourceAuxiliaryBureaus, f"test_exact_original_quote_{162 + i:04d}", one_source_annotation(i)
    )


if __name__ == "__main__":
    unittest.main()
