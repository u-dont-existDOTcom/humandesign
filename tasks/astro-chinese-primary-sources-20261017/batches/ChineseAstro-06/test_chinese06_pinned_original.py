"""Di Tian Sui six pinned original Chinese pages source-first, 53 exact quotes."""

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
import ditiansui_source_formations as source_formations  # noqa: E402


def j(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


class OriginalSixChineseChapters(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notes = j(B / "BAZI_DITIAN_SUI_FORMATIONS_TRANSFORMATIONS_53_NOTES_V1.json")
        cls.witness = j(B / "PINNED_DI_TIAN_SUI_SIX_PAGE_53_ANCHOR_WITNESS_V1.json")
        cls.manifest = j(B / "DITIAN_SUI_ADDITIONAL_PINNED_PAGES_MANIFEST_V1.json")
        cls.v5 = j(P / "CHINESE_SOURCE_AUDIT_INDEX_V5.json")
        cls.records = cls.notes["records"]
        cls.proofs = cls.witness["quote_receipts"]
        cls.pages = {
            key: (B / "evidence" / item["raw_file_local"]).read_bytes().decode("utf-8")
            for key, item in cls.manifest.items()
        }

    def test_source_original_held_in_project(self):
        self.assertEqual(set(self.manifest), {"04", "05", "07", "08", "11", "12"})
        for chapter, item in self.manifest.items():
            path = B / "evidence" / item["raw_file_local"]
            self.assertEqual(path.stat().st_size, item["source_bytes"])
            self.assertEqual(sha(path.read_bytes()), item["source_sha256"])
            self.assertIn("滴天髓", self.pages[chapter])
            self.assertIn("oldid=" + str(item["wikisource_oldid"]), item["pinned_raw_url"])

    def test_old_versions_exact_and_no_ID_collision(self):
        self.assertEqual(self.v5["sum_source_annotations"], 262)
        self.assertEqual(self.v5["systems"][0]["accepted_source_annotations"], 101)
        self.assertEqual(self.v5["systems"][0]["next_id"], "BZI-R0102")
        self.assertEqual(self.v5["systems"][1]["next_id"], "ZWD-R0162")
        self.assertEqual(self.notes["first_id"], "BZI-R0102")
        self.assertEqual(self.notes["last_id"], "BZI-R0154")
        self.assertEqual(self.notes["next_id"], "BZI-R0155")

    def test_53_records_exact_consecutive_original_chinese(self):
        self.assertEqual(len(self.records), 53)
        self.assertEqual(self.notes["source_annotations_added"], 53)
        self.assertEqual(
            [r["id"] for r in self.records], [f"BZI-R{n:04d}" for n in range(102, 155)]
        )

    def test_strict_raw_bytes_sha_offsets_all_53(self):
        self.assertEqual(len(self.proofs), 53)
        for r, p in zip(self.records, self.proofs, strict=True):
            chapter = r["source_section"]
            text = self.pages[chapter]
            literal = r["original_chinese_anchor_verbatim"]
            start = r["source_character_offset"]
            self.assertEqual(r["id"], p["id"])
            self.assertEqual(literal, p["anchor_literal"])
            self.assertEqual(text[start : start + len(literal)], literal)
            self.assertEqual(r["source_UTF8_byte_offset"], len(text[:start].encode("utf-8")))
            self.assertEqual(r["original_anchor_UTF8_SHA256"], sha(literal.encode("utf-8")))
            self.assertEqual(
                r["source_wikisource_oldid"], self.manifest[chapter]["wikisource_oldid"]
            )
            self.assertEqual(
                r["source_full_raw_chapter_sha256"], self.manifest[chapter]["source_sha256"]
            )

    def test_true_verse_vs_later_commentary_counts(self):
        self.assertEqual(self.notes["historical_original_verse_anchors"], 15)
        self.assertEqual(self.notes["later_transmitted_commentary_anchor_quotes"], 38)
        self.assertEqual(sum(x["text_layer"] == "TRANSMITTED_VERSE" for x in self.records), 15)
        self.assertEqual(
            sum(x["text_layer"] == "TRANSMITTED_COMMENTARY_UNDATED" for x in self.records), 38
        )

    def test_all_exact_source_records_from_sections(self):
        self.assertEqual(self.witness["matched_independently_pinned_source_quotes"], 53)
        self.assertEqual(
            self.witness["original_source_manifest_SHA256"],
            sha((B / "DITIAN_SUI_ADDITIONAL_PINNED_PAGES_MANIFEST_V1.json").read_bytes()),
        )
        self.assertEqual(
            self.notes["pinned_source_manifest_SHA256"],
            self.witness["original_source_manifest_SHA256"],
        )

    def test_source_does_not_prove_early_woodblock_or_authorship(self):
        self.assertFalse(self.notes["source_physical_authorship_or_early_print_verified"])
        self.assertFalse(self.witness["source_is_original_diplomatic_early_witness"])
        self.assertFalse(self.witness["independent_expert_Chinese_glosses_validated"])
        for r in self.records:
            self.assertFalse(r["source_original_early_print_verified"])
            self.assertFalse(r["source_author_verified"])

    def test_no_source_to_live_human_deduction(self):
        self.assertEqual(self.notes["independent_real_human_prediction_validations"], 0)
        self.assertEqual(self.notes["runtime_promotions"], 0)
        self.assertTrue(all(not r["runtime_promoted"] for r in self.records))
        self.assertTrue(
            all(not r["independently_validated_real_human_accuracy"] for r in self.records)
        )
        self.assertTrue(
            all(
                not r["source_claims_about_actual_personality_or_morality_validated"]
                for r in self.records
            )
        )

    def test_moralized_apparent_following_source_quarantined(self):
        moral = [
            r
            for r in self.records
            if r["source_section"] == "08"
            and any(
                word in r["original_chinese_anchor_verbatim"] for word in ("心術不端", "異姓孤兒")
            )
        ]
        self.assertEqual(len(moral), 2)
        self.assertTrue(
            all(not r["source_health_lifespan_or_wealth_prediction_validated"] for r in moral)
        )

    def test_no_synthetic_old_history_update(self):
        old = j(WEST)
        self.assertEqual(old["records_count"], 12611)
        self.assertEqual(old["batches"][-1]["id"], "B07al")
        self.assertEqual(self.v5["sum_source_annotations"], 262)

    def test_wood_two_original_triplets_strict(self):
        self.assertEqual(source_formations.HISTORIC_WOOD_EAST_DIRECTION, ("Yin", "Mao", "Chen"))
        self.assertEqual(source_formations.HISTORIC_WOOD_THREE_HARMONY, ("Hai", "Mao", "Wei"))
        self.assertEqual(
            source_formations.original_text_wood_branch_group(("Mao", "Yin", "Chen"))[
                "matched_source_group"
            ],
            "wood_eastern_direction",
        )
        self.assertEqual(
            source_formations.original_text_wood_branch_group(("Wei", "Mao", "Hai"))[
                "matched_source_group"
            ],
            "wood_three_harmony",
        )

    def test_unlisted_combination_unknown_not_fortune(self):
        r = source_formations.original_text_wood_branch_group(("Zi", "Mao", "Xu"))
        self.assertIsNone(r["matched_source_group"])
        self.assertIsNone(r["predicted_fortune_or_character"])
        self.assertFalse(r["full_natal_or_luck_structure_computed"])

    def test_source_genuine_following_preconditions_not_engine(self):
        r = source_formations.original_text_true_false_following_preconditions()
        self.assertIn("絕無一毫生扶", r["literal_original_true_following_condition"])
        self.assertIn("中有所助者，便假", r["literal_original_apparent_following_condition"])
        self.assertFalse(r["full_general_true_false_transformation_engine_verified"])
        self.assertTrue(r["requires_month_luck_calendar_context"])

    def test_explicit_source_strength_exceptions_retained(self):
        r = source_formations.original_text_formation_source_warnings()
        self.assertEqual(len(r["strength_exception_Chinese_quotes"]), 5)
        for text in r["strength_exception_Chinese_quotes"]:
            self.assertIn(text, self.pages["12"])
        self.assertTrue(r["no_universal_want_stronger_or_weaker_rule"])

    def test_unknown_or_duplicate_branches_fail_closed(self):
        for invalid in (("Zi", "Zi", "Mao"), ("notABranch",), ["Yin", "Mao", "Chen"]):
            with self.assertRaises(ValueError):
                source_formations.original_text_wood_branch_group(invalid)

    def test_no_bazi_four_pillars_ephemeris(self):
        r = source_formations.source_research_limits()
        self.assertFalse(r["Four_Pillars_accurate_natal_engine_verified"])
        self.assertFalse(r["birth_Gregorian_to_lunisolar_and_solar_terms_verified"])
        self.assertEqual(r["real_human_prospective_blind_predictions_validated"], 0)
        self.assertEqual(r["model_runtime_promotions"], 0)


def one_anchor(i):
    def test(self):
        r = self.records[i]
        p = self.proofs[i]
        self.assertEqual(r["id"], f"BZI-R{i + 102:04d}")
        self.assertEqual(r["original_anchor_UTF8_SHA256"], p["anchor_UTF8_SHA256"])
        self.assertFalse(r["runtime_promoted"])

    return test


for i in range(53):
    setattr(
        OriginalSixChineseChapters, f"test_original_source_anchor_BZI_{i + 102:04d}", one_anchor(i)
    )


if __name__ == "__main__":
    unittest.main()
