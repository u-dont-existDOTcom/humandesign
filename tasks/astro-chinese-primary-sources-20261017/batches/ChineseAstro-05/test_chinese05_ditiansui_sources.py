"""Pinned Di Tian Sui six-chapter source and bounded historical enumerations."""

import hashlib
import json
import sys
import unittest
from pathlib import Path

B = Path(__file__).resolve().parent
P = B.parents[1]
ROOT = B.parents[3]
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
sys.path.insert(0, str(P / "bazi"))
import ditiansui_historical_conventions as classic  # noqa: E402


def j(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


class SixOriginalBaZiChapters(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = j(B / "BAZI_DITIAN_SUI_SIX_SECTIONS_55_SOURCE_NOTES_V1.json")
        cls.witness = j(B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json")
        cls.metadata = j(B / "DITIAN_SUI_PINNED_SOURCE_MANIFEST_V1.json")
        cls.chinese = j(P / "CHINESE_SOURCE_AUDIT_INDEX_V4.json")
        cls.bazi_old = j(P / "bazi/BAZI_SOURCE_FIRST_RULES_V1.json")

    def test_current_V4_source_anchor_counts_not_changed(self):
        self.assertEqual(self.chinese["sum_source_annotations"], 207)
        self.assertEqual(self.chinese["systems"][0]["accepted_source_annotations"], 46)
        self.assertEqual(self.chinese["systems"][0]["next_id"], "BZI-R0047")
        self.assertEqual(self.chinese["systems"][1]["accepted_source_annotations"], 161)
        self.assertEqual(self.bazi_old["records"][-1]["id"], "BZI-R0046")

    def test_source_six_specific_oldids(self):
        self.assertEqual(sorted(self.metadata), ["01", "02", "03", "06", "09", "10"])
        self.assertEqual(self.metadata["02"]["revision_id"], 11117658)
        self.assertEqual(self.metadata["01"]["revision_id"], 844395)
        for key, value in self.metadata.items():
            self.assertTrue(value["source_bytes"] > 500)
            self.assertEqual(len(value["full_source_sha256"]), 64)
            self.assertFalse(value["source_is_critical_early_print"])
            self.assertIn("oldid=" + str(value["revision_id"]), value["raw_source_url"])
            self.assertTrue(value["title"].endswith(key))

    def test_manifest_SHA_preserved(self):
        self.assertEqual(
            self.records["source_manifest_sha256"],
            sha(B / "DITIAN_SUI_PINNED_SOURCE_MANIFEST_V1.json"),
        )
        self.assertEqual(
            self.witness["source_manifest_sha256"], self.records["source_manifest_sha256"]
        )

    def test_55_source_notes_exact_range(self):
        self.assertEqual(self.records["source_only_annotation_count"], 55)
        self.assertEqual(len(self.records["records"]), 55)
        self.assertEqual(
            [r["id"] for r in self.records["records"]], [f"BZI-R{n:04d}" for n in range(47, 102)]
        )
        self.assertEqual(self.records["first_id"], "BZI-R0047")
        self.assertEqual(self.records["last_id"], "BZI-R0101")
        self.assertEqual(self.records["next_id"], "BZI-R0102")

    def test_source_layer_44_verses_11_commentary_passages(self):
        self.assertEqual(self.records["verse_quote_count"], 44)
        self.assertEqual(self.records["commentary_exact_quote_count"], 11)
        self.assertEqual(self.witness["exact_chinese_source_anchor_matches"], 55)
        self.assertEqual(self.witness["verses"], 44)
        self.assertEqual(self.witness["commentary_snippets"], 11)
        self.assertEqual(
            sum(r["text_layer"] == "TRANSMITTED_VERSE" for r in self.records["records"]), 44
        )
        self.assertEqual(
            sum(
                r["text_layer"] == "TRANSMITTED_COMMENTARY_UNDATED" for r in self.records["records"]
            ),
            11,
        )

    def test_original_quote_SHA_and_offsets_reversible(self):
        records = self.records["records"]
        proofs = self.witness["anchor_proofs"]
        self.assertEqual(len(records), len(proofs))
        for r, p in zip(records, proofs, strict=True):
            self.assertEqual(r["id"], p["record_id"])
            self.assertEqual(r["original_chinese_anchor"], p["exact_chinese_quote"])
            self.assertEqual(r["chapter_code"], p["chapter_code"])
            self.assertEqual(r["raw_anchor_char_offset"], p["raw_char_offset"])
            self.assertEqual(r["raw_anchor_utf8_byte_offset"], p["raw_utf8_byte_offset"])
            self.assertEqual(r["raw_anchor_utf8_sha256"], p["exact_quote_sha256"])
            self.assertEqual(sha_from_text(r["original_chinese_anchor"]), p["exact_quote_sha256"])
            self.assertEqual(p["oldid"], self.metadata[r["chapter_code"]]["revision_id"])
            self.assertEqual(
                p["full_raw_page_sha256"], self.metadata[r["chapter_code"]]["full_source_sha256"]
            )

    def test_working_glosses_not_historically_authoritative(self):
        self.assertFalse(self.records["source_author_or_commentary_attribution_certified"])
        self.assertFalse(self.records["original_print_edition_verified"])
        self.assertTrue(self.witness["source_authenticity_early_print_not_established"])
        self.assertFalse(self.witness["independent_classical_Chinese_expert_translation_review"])
        self.assertTrue(all(r["working_English_historical_gloss"] for r in self.records["records"]))

    def test_raw_original_claims_never_promoted(self):
        for r in self.records["records"]:
            self.assertTrue(r["original_quote_directly_matched"])
            self.assertTrue(r["source_precondition"])
            self.assertTrue(r["uncertainty_or_exception"])
            self.assertFalse(r["verified_authentic_Ming_witness"])
            self.assertFalse(r["verified_author_identification"])
            self.assertFalse(r["full_BaZi_calendar_engine_verified"])
            self.assertFalse(r["independent_real_person_predictive_validation"])
            self.assertFalse(r["runtime_model_promoted"])
        self.assertEqual(self.records["human_predictive_validations"], 0)
        self.assertEqual(self.records["runtime_promotions"], 0)

    def test_five_yang_five_yin_stems_match_Chinese_original(self):
        self.assertEqual(classic.YANG_STEMS, ("Jia", "Bing", "Wu", "Geng", "Ren"))
        self.assertEqual(classic.YIN_STEMS, ("Yi", "Ding", "Ji", "Xin", "Gui"))
        self.assertEqual(len(set(classic.YANG_STEMS + classic.YIN_STEMS)), 10)
        for s in classic.YANG_STEMS:
            self.assertEqual(classic.explicit_stem_polarity(s), "Yang")
        for s in classic.YIN_STEMS:
            self.assertEqual(classic.explicit_stem_polarity(s), "Yin")

    def test_six_yang_six_yin_branch_groups(self):
        self.assertEqual(classic.YANG_BRANCHES, ("Zi", "Yin", "Chen", "Wu", "Shen", "Xu"))
        self.assertEqual(classic.YIN_BRANCHES, ("Chou", "Mao", "Si", "Wei", "You", "Hai"))
        for b in classic.YANG_BRANCHES:
            self.assertEqual(classic.explicit_branch_polarity(b), "Yang")
        for b in classic.YIN_BRANCHES:
            self.assertEqual(classic.explicit_branch_polarity(b), "Yin")

    def test_birth_storehouse_defeat_twelve_branch_partition(self):
        self.assertEqual(
            set(classic.FOUR_BIRTH_BRANCHES),
            {"Yin", "Shen", "Si", "Hai"},
        )
        self.assertEqual(
            set(classic.FOUR_STOREHOUSE_BRANCHES),
            {"Chen", "Xu", "Chou", "Wei"},
        )
        self.assertEqual(
            set(classic.FOUR_DEFEAT_BRANCHES),
            {"Zi", "Wu", "Mao", "You"},
        )
        self.assertEqual(
            len(
                set(
                    classic.FOUR_BIRTH_BRANCHES
                    + classic.FOUR_STOREHOUSE_BRANCHES
                    + classic.FOUR_DEFEAT_BRANCHES
                )
            ),
            12,
        )
        self.assertEqual(classic.original_branch_category("Chen"), "FourStorehouse")
        self.assertEqual(classic.original_branch_category("Yin"), "FourBirth")
        self.assertEqual(classic.original_branch_category("Zi"), "FourDefeat")

    def test_all_ten_stem_metaphors_not_personality_predictions(self):
        self.assertEqual(len(classic.SOURCE_STEM_PATTERNS), 10)
        self.assertEqual(classic.source_stem_season_metaphor("Jia"), "Tall-Wood seasonal")
        self.assertEqual(classic.source_stem_season_metaphor("Gui"), "Subtle-Water conditional")

    def test_source_harmony_examples_only_not_full_combinatorial_engine(self):
        self.assertEqual(
            classic.source09_only_named_harmony_examples("Yi", "Geng")["historical_phase_claim"],
            "Metal",
        )
        self.assertEqual(
            classic.source09_only_named_harmony_examples("Zi", "Chou")["historical_phase_claim"],
            "Earth",
        )
        self.assertEqual(
            classic.source09_only_named_harmony_examples("Xin", "Geng")["original_relation"], "Hao"
        )
        self.assertIsNone(
            classic.source09_only_named_harmony_examples("Jia", "Zi")["original_relation"]
        )
        for x, y in (("Yi", "Geng"), ("Zi", "Chou")):
            self.assertFalse(
                classic.source09_only_named_harmony_examples(x, y)[
                    "general_universal_harmony_algorithm_implemented"
                ]
            )

    def test_rigid_birth_death_stage_forecasts_explicitly_rejected_by_source(self):
        self.assertIn("其論勿執", classic.TEXTUAL_CHAPTER03_BRANCH_CLASH_WARNING)
        self.assertFalse(
            classic.source_research_limits()[
                "historical_textually_claimed_fatalities_are_predictions_of_actual_people"
            ]
        )

    def test_invalid_symbols_fail_closed(self):
        for bad in ("INVALID", None, "", 17):
            with self.assertRaises(ValueError):
                classic.explicit_stem_polarity(bad)
            with self.assertRaises(ValueError):
                classic.original_branch_category(bad)
            with self.assertRaises(ValueError):
                classic.source09_only_named_harmony_examples("Jia", bad)

    def test_source_bazi_B4_timeline_index_unmutated(self):
        self.assertEqual(j(WEST)["records_count"], 12472)
        self.assertEqual(self.chinese["systems"][1]["next_id"], "ZWD-R0162")
        self.assertEqual(self.chinese["runtime_promotions"], 0)

    def test_no_complete_calendar_or_live_predictor(self):
        limits = classic.source_research_limits()
        self.assertFalse(limits["complete_60_ganzhi_year_month_day_hour_algorithm_verified"])
        self.assertFalse(limits["lunar_solar_term_and_time_zone_engine_verified"])
        self.assertFalse(limits["prognostic_body_strength_and_wealth_patterns_verified"])
        self.assertEqual(limits["human_forward_blind_successes"], 0)
        self.assertEqual(limits["runtime_promotions"], 0)


def sha_from_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def individual_original_anchor_test(i):
    def test(self):
        r = self.records["records"][i]
        p = self.witness["anchor_proofs"][i]
        self.assertEqual(r["id"], f"BZI-R{i + 47:04d}")
        self.assertEqual(r["original_chinese_anchor"], p["exact_chinese_quote"])
        self.assertEqual(r["raw_anchor_utf8_sha256"], sha_from_text(p["exact_chinese_quote"]))
        self.assertFalse(r["runtime_model_promoted"])

    return test


for i in range(55):
    setattr(
        SixOriginalBaZiChapters,
        f"test_exact_original_BaZi_anchor_{i + 47:04d}",
        individual_original_anchor_test(i),
    )

if __name__ == "__main__":
    unittest.main()
