"""Exact Chinese revision source-first and bounded Zi Wei Life/Body chart mechanics."""

import hashlib
import json
import sys
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
P = B.parents[1]
ROOT = B.parents[3]
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
sys.path.insert(0, str(P / "ziwei"))
import quan_shu_vol2_life_body_taxonomy as lords  # noqa: E402


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class ChineseVolume2LifeLords(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notes = j(B / "ZIWEI_VOLUME2_LIFE_BODY_TAXONOMY_SOURCE_NOTES_V1.json")
        cls.witness = j(B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json")
        cls.v3 = j(P / "CHINESE_SOURCE_AUDIT_INDEX_V3.json")
        cls.prev = j(P / "batches/ChineseAstro-03/ZIWEI_VOLUME2_AUXILIARY_45_SOURCE_NOTES_V1.json")
        cls.records = cls.notes["records"]
        cls.proofs = cls.witness["anchor_receipts"]

    def test_predecessor_Chinese_V3_not_overwritten(self):
        self.assertEqual(self.v3["sum_source_annotations"], 142)
        self.assertEqual(self.v3["systems"][0]["accepted_source_annotations"], 46)
        self.assertEqual(self.v3["systems"][1]["accepted_source_annotations"], 96)
        self.assertEqual(self.v3["systems"][1]["next_id"], "ZWD-R0097")
        self.assertEqual(self.prev["records"][-1]["id"], "ZWD-R0096")

    def test_exact_65_new_annotations_sequential(self):
        self.assertEqual(len(self.records), 65)
        self.assertEqual(self.notes["count"], 65)
        self.assertEqual(
            [r["id"] for r in self.records],
            [f"ZWD-R{n:04d}" for n in range(97, 162)],
        )
        self.assertEqual(self.notes["first_id"], "ZWD-R0097")
        self.assertEqual(self.notes["last_id"], "ZWD-R0161")
        self.assertEqual(self.notes["next_id"], "ZWD-R0162")

    def test_old_ids_disjoint(self):
        self.assertFalse(
            set(r["id"] for r in self.prev["records"]) & set(r["id"] for r in self.records)
        )

    def test_pinned_original_wikitext_SHA_and_bytes(self):
        self.assertEqual(
            self.notes["raw_source_sha256"], self.witness["original_full_raw_source_sha256"]
        )
        self.assertEqual(
            self.notes["raw_source_sha256"],
            "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72",
        )
        self.assertEqual(self.witness["original_full_raw_source_bytes"], 106736)
        self.assertEqual(self.notes["wikisource_revision_id"], 1963110)
        self.assertEqual(self.witness["source_revision_id"], 1963110)

    def test_exact_sixty_five_chinese_quotes_in_ten_named_sections(self):
        self.assertEqual(self.notes["short_chinese_quote_direct_match_count"], 65)
        self.assertEqual(self.witness["original_quote_count"], 65)
        self.assertTrue(self.witness["all_65_short_anchor_exact_matches"])
        self.assertEqual(len(self.witness["separate_original_heading_ranges"]), 10)

    def test_source_quote_reversible_sha_and_offsets(self):
        for r, p in zip(self.records, self.proofs, strict=True):
            self.assertEqual(r["id"], p["id"])
            self.assertEqual(r["original_chinese_anchor"], p["anchor_text"])
            self.assertEqual(r["locator"].split(":", 1)[1], p["section_name"])
            self.assertEqual(r["raw_revision_anchor_char_offset"], p["anchor_start_char_offset"])
            self.assertGreaterEqual(p["anchor_start_char_offset"], p["section_start_char_offset"])
            self.assertLessEqual(
                p["anchor_start_char_offset"] + len(p["anchor_text"]), p["section_end_char_offset"]
            )
            self.assertEqual(
                r["raw_revision_anchor_utf8_sha256"],
                hashlib.sha256(p["anchor_text"].encode()).hexdigest(),
            )

    def test_all_source_only_no_individual_prediction(self):
        for r in self.records:
            self.assertTrue(r["original_revision_quote_match_confirmed"])
            self.assertEqual(r["rule_status"], "SOURCE_ONLY_DOCUMENTED")
            self.assertTrue(r["source_precondition"])
            self.assertTrue(r["uncertainty_or_exception"])
            self.assertFalse(r["independently_validated_real_person_accuracy"])
            self.assertFalse(r["full_birth_calendar_engine_verified"])
            self.assertFalse(r["runtime_promoted"])
        self.assertEqual(self.notes["runtime_promotions"], 0)
        self.assertEqual(self.notes["independent_human_prediction_validations"], 0)

    def test_not_an_authenticated_Ming_original(self):
        self.assertFalse(self.notes["author_attribution_verified"])
        self.assertFalse(self.notes["source_is_complete_original_diplomatic_edition"])
        self.assertFalse(self.witness["source_is_authentic_Ming_woodblock_verified"])
        self.assertFalse(self.witness["independent_classical_Chinese_translation_validated"])

    def test_first_new_record_follows_child_limit(self):
        self.assertEqual(self.records[0]["original_chinese_anchor"], "余年一派顺流行")
        self.assertEqual(self.records[1]["original_chinese_anchor"], "十五命宫看端的")

    def test_mortality_source_quarantine(self):
        high = [
            r
            for r in self.records
            if r["rule_or_section_type"]
            in (
                "jin_suo_mortality_rhetoric",
                "zhulu_life_mortality_rhetoric",
            )
        ]
        self.assertEqual(len(high), 2)
        self.assertTrue(all(not r["runtime_promoted"] for r in high))

    def test_12_Life_Lord_Source_mappings(self):
        expected = {
            "Zi": "贪狼",
            "Chou": "巨门",
            "Yin": "禄存",
            "Mao": "文曲",
            "Chen": "廉真",
            "Si": "武曲",
            "Wu": "破军",
            "Wei": "武曲",
            "Shen": "廉真",
            "You": "文曲",
            "Xu": "禄存",
            "Hai": "巨门",
        }
        self.assertEqual(lords.SOURCE_LIFE_LORD_BY_LIFE_PALACE, expected)
        for birth, star in expected.items():
            self.assertEqual(lords.source_life_lord_star_label(birth), star)

    def test_selected_Life_Lord_is_not_same_as_actual_palace(self):
        self.assertEqual(lords.source_life_lord_star_label("Wu"), "破军")
        with self.assertRaises(ValueError):
            lords.source_life_lord_actual_palace("Wu", {})
        self.assertEqual(lords.source_life_lord_actual_palace("Wu", {"破军": "Xu"}), "Xu")
        self.assertNotEqual("Wu", "Xu")

    def test_selected_Life_Lord_invalid_external_natal_position_fails(self):
        with self.assertRaises(ValueError):
            lords.source_life_lord_actual_palace("Zi", {"贪狼": "INVALID"})
        with self.assertRaises(ValueError):
            lords.source_life_lord_actual_palace("Zi", None)

    def test_12_body_lord_source_labels_and_two_ambiguous_birth_branches(self):
        self.assertEqual(len(lords.SOURCE_BODY_LORD_BY_NATAL_YEAR), 12)
        for branch in ("Zi", "Wu"):
            value = lords.source_body_lord_star_label(branch)
            self.assertEqual(value["original_chinese_label"], "火玲星")
            self.assertTrue(value["raw_text_star_identification_ambiguous"])
        for branch in ("Chou", "Wei", "Yin", "Shen", "Mao", "You", "Chen", "Xu", "Si", "Hai"):
            self.assertFalse(
                lords.source_body_lord_star_label(branch)["raw_text_star_identification_ambiguous"]
            )

    def test_child_period_explicit_ages_no_filling_gap(self):
        names = ["命", "财", "疾厄", "妻", "福", "官禄"]
        self.assertEqual([lords.source_child_limit_palace(i) for i in range(1, 7)], names)
        self.assertEqual(lords.source_child_limit_palace(15), "命")
        for i in range(7, 15):
            with self.assertRaises(ValueError):
                lords.source_child_limit_palace(i)

    def test_no_deduced_historic_birth_year_from_Gregorian(self):
        for val in (None, 14, True, "Zi", "invalid"):
            with self.assertRaises(ValueError):
                lords.source_child_limit_palace(val)

    def test_all_eight_source_idle_star_palace_groups(self):
        expected = {
            "紫微": ("Zi", "Chen", "Hai"),
            "贪狼": ("Yin", "Chen"),
            "天相": ("Chen", "Xu"),
            "七杀": ("Chen", "Hai"),
            "天梁": ("Si", "You"),
            "天机": ("Si",),
            "破军": ("Si", "Shen"),
            "武曲": ("Shen",),
        }
        self.assertEqual(lords.IDLE_SOURCE_PALACES, expected)
        for star, branches in expected.items():
            self.assertEqual(lords.source_idle_palace_branches(star), branches)

    def test_source_annual_JiChou_example_not_general_YearPillar_rules(self):
        self.assertEqual(
            lords.source_ji_chou_year_annual_example("Ji", "Chou"),
            {"FlowLu": "Wu", "FlowYang": "Wei", "FlowTuo": "Si"},
        )
        with self.assertRaises(ValueError):
            lords.source_ji_chou_year_annual_example("Jia", "Zi")

    def test_element_source_four_declared_suppression_pairs_only(self):
        for s, p in lords.TEXTUAL_ELEMENT_RESTRAINTS:
            self.assertIs(lords.source_classifies_element_as_restrained(s, p), True)
        self.assertIsNone(lords.source_classifies_element_as_restrained("Wood", "Metal"))
        with self.assertRaises(ValueError):
            lords.source_classifies_element_as_restrained("Air", "Wood")

    def test_transmitted_eighteen_source_star_classifications(self):
        self.assertEqual(len(lords.STAR_ELEMENT_LABELS_18_TRANSMITTED), 18)
        self.assertEqual(lords.source_star_element_labels("天同"), ("Water", "Metal"))
        self.assertEqual(lords.source_star_element_labels("贪狼"), ("Water", "Wood"))
        self.assertEqual(lords.source_star_element_labels("七杀"), ("Fire", "Metal"))
        self.assertIsNone(lords.source_star_element_labels("辅弼二星"))

    def test_no_invented_star_taxonomy_members(self):
        with self.assertRaises(ValueError):
            lords.source_star_element_labels("不是星")

    def test_invalid_branches_fail_closed(self):
        with self.assertRaises(ValueError):
            lords.source_life_lord_star_label("Foo")
        with self.assertRaises(ValueError):
            lords.source_body_lord_star_label("Foo")
        with self.assertRaises(ValueError):
            lords.source_idle_palace_branches("Foo")

    def test_source_no_14_main_star_full_chart_silent_claim(self):
        limits = lords.source_limits()
        self.assertFalse(limits["full_14_main_star_placement_engine_verified"])
        self.assertFalse(limits["chinese_solar_terms_and_leap_month_calendar_verified"])
        self.assertFalse(limits["source_eighteen_list_is_the_same_as_modern_fourteen_main_stars"])
        self.assertFalse(limits["historical_sex_and_death_omensation_validated"])
        self.assertEqual(limits["real_human_predictive_successes"], 0)
        self.assertEqual(limits["runtime_promotions"], 0)

    def test_original_Western_index_not_mutated(self):
        self.assertEqual(j(WEST)["records_count"], 12472)


def evidence_one(i):
    def test(self):
        r = self.records[i]
        proof = self.proofs[i]
        self.assertEqual(r["id"], f"ZWD-R{i + 97:04d}")
        self.assertEqual(r["original_chinese_anchor"], proof["anchor_text"])
        self.assertGreaterEqual(len(r["original_chinese_anchor"]), 4)
        self.assertFalse(r["runtime_promoted"])
        self.assertEqual(r["raw_revision_anchor_utf8_sha256"], proof["anchor_utf8_sha256"])

    return test


for i in range(65):
    setattr(ChineseVolume2LifeLords, f"test_original_anchor_{i + 97:04d}", evidence_one(i))


if __name__ == "__main__":
    unittest.main()
