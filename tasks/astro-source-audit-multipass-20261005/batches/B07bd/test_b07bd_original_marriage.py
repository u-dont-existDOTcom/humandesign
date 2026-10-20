"""Original 1647 & separately printed 1659 Marriage: source integrity, not reality.

57 strictly historical annotations include marriage 2, lovers 2, age >29;
these are specific unverified original statements about a merchant Lilly KNEW.
If Swiss .se1 files are supplied externally and pinned, compare the source's
Venus-Cazimi premise only as astronomical engineering, not predictive truth.
"""
from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA_V7 = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
PREFETCH=B/"CHILDREN_NEXT_CHAPTER_PREFETCH_NOT_ADMITTED.json"
SOURCE=B/"ORIGINAL_CLXXXI_1647_1659_MARRIAGE_SOURCE_V1.json"
RULES=B/"RULES.json"
ACCEPT=B/"ACCEPTANCE.json"
MANIFEST=B/"ORIGINAL_1647_1659_MARRIAGE_PHOTOS_PROVISIONAL_V1.json"
CAZIMI=B/"VENUS_CAZIMI_SOURCE_VS_SWIEPH_1616_V1.json"
SWE_EPHE_DIR=Path("/tmp/hd-western-swe-1616-20261020")

def rd(p):
    return json.loads(p.read_text(encoding="utf-8"))

def h(p):
    return sha256(p.read_bytes()).hexdigest()

class OriginalSourceMarriageSourceOnly(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notes=rd(SOURCE)
        cls.rules=rd(RULES)
        cls.accept=rd(ACCEPT)
        cls.photo=rd(MANIFEST)
        cls.cazimi=rd(CAZIMI)

    def test_01_parent_append_frontier_is_precisely_R13045(self):
        old=rd(WEST)
        self.assertIn(old["records_count"],(13044,13101))
        if old["records_count"]==13044:
            self.assertEqual(old["batches"][-1]["id"],"B07bc")
            self.assertEqual(old["next"]["chapter"],"CLXXXI")
            self.assertEqual(old["next"]["pdf_page"],788)
            self.assertEqual(old["next"]["printed_page"],754)
        else:
            self.assertEqual(old["batches"][-1]["id"],"B07bd")
            self.assertEqual(old["next"]["chapter"],"CLXXXII")
            self.assertEqual(old["next"]["pdf_page"],791)
            self.assertEqual(old["next"]["printed_page"],757)
        self.assertEqual(old["empirical_validations"],0)
        self.assertEqual(old["runtime_promotions"],0)

    def test_02_chinese_accepted_V7_sha_unchanged(self):
        self.assertEqual(h(CHINA_V7),
                         "bb73f28bf74a1ccb3a0a0e76b91c45f647128733047b8145094f28c9a4ae9d84")
        self.assertEqual(rd(CHINA_V7)["sum_source_annotations"],355)

    def test_03_source_claims_57_unique_ordered_records_4_original_folios(self):
        rs=self.notes["all_source_records"]
        self.assertEqual(len(rs),57)
        self.assertEqual([x["id"] for x in rs],
                         [f"R{i}" for i in range(13045,13102)])
        self.assertEqual([x["record_number"] for x in rs],
                         list(range(13045,13102)))
        self.assertEqual(len({x["role"] for x in rs}),57)
        self.assertEqual(self.notes["first_R"],"R13045")
        self.assertEqual(self.notes["last_R"],"R13101")
        self.assertEqual(self.notes["next_R"],"R13102")
        self.assertEqual(sorted({x["printed_folio"] for x in rs}),[754,755,756,757])
        self.assertEqual(list(x["printed_folio"] for x in rs),
                         sorted(x["printed_folio"] for x in rs))

    def test_04_source_original_8_page_photo_sha_exact_bytes(self):
        from build_b07bd_marriage_source import photo_witnesses
        photos=photo_witnesses()
        self.assertEqual(photos,self.notes["four_original_folio_photographs"])
        self.assertEqual(set(photos),{"754","755","756","757"})
        for folio,witness in photos.items():
            self.assertEqual(set(witness),{"1647","1659"})
            for edition,item in witness.items():
                p=ROOT/item["repository_source_path"]
                self.assertTrue(p.is_file())
                self.assertEqual(item["original_printed_folio"],int(folio))
                self.assertEqual(item["source_edition"],int(edition))
                self.assertEqual(item["photo_sha256"],h(p))
                self.assertEqual(item["photo_byte_length"],p.stat().st_size)
                self.assertGreater(p.stat().st_size,100000)
                self.assertFalse(item["full_original_1659_DjVu_binary_sha_checked"])

    def test_05_independent_1659_scans_not_claimed_as_whole_DjVu_hash(self):
        self.assertFalse(self.notes["whole_1659_DjVu_binary_verified"])
        self.assertEqual(self.notes["original_1659_DjVu_frames"],[783,784,785,786])
        self.assertEqual(self.notes["original_1647_printed_folios"],[754,755,756,757])
        self.assertEqual(self.notes["original_Wellcome_1647_whole_PDF_sha256"],
                         "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")

    def test_06_paragraphs_bounded_by_2_separate_original_heading_dividers(self):
        self.assertEqual(self.notes["all_source_records"][0]["role"],
                         "CHAP_CLXXXI_MARRIAGE_BOUNDARY")
        self.assertEqual(self.notes["all_source_records"][-1]["role"],
                         "PHYSICAL_CHILDREN_NEXT_CHAPTER")
        self.assertEqual(self.notes["next_chapter"],"CLXXXII Of Children")
        self.assertEqual(self.notes["next_original_folio"],757)
        self.assertEqual(self.notes["next_original_pdf_frame"],791)
        self.assertTrue(self.notes["first_marriage_Chapter_CLXXXI_begins_after_CLXXX_sixth_house_divider"])
        self.assertTrue(self.notes["last_marriage_Chapter_CLXXXI_ends_before_CLXXXII_children_divider"])

    def test_07_marry_after29_twice_two_sweethearts_explicit_literal_source(self):
        roles={r["role"]:r for r in self.notes["all_source_records"]}
        self.assertIn("twenty ninth",roles["MARRIAGE_AFTER_SATURN_RETURN_29"]["1647_short_original_anchor_not_diplomatic_transcription"])
        self.assertEqual(roles["EXACT_TWO_MARRIAGES_FORECAST"]["1647_short_original_anchor_not_diplomatic_transcription"],
                         "marry two times onely")
        self.assertIn("two Sweet-hearts",roles["EXACT_TWO_EXTRA_SWEETHEARTS"]["1647_short_original_anchor_not_diplomatic_transcription"])
        self.assertEqual(self.notes["source_predicted_marriage_count"],2)
        self.assertEqual(self.notes["source_predicted_extra_sweethearts"],2)
        self.assertEqual(self.notes["source_maturity_threshold_after_age_years"],29)
        self.assertFalse(self.notes["source_actual_merchant_marriage_count_independently_verified"])

    def test_08_source_one_vs_two_marriage_qualifications_preserved(self):
        r={x["role"]:x for x in self.notes["all_source_records"]}
        self.assertEqual(r["MOON_GEMINI_MARS_LEO_MERCURY_COMBUST_ONE"]["candidate_scored_target_type_NOT_pre_registered"],
                         "mechanical_countertestimony")
        self.assertEqual(r["EXACT_TWO_MARRIAGES_FORECAST"]["candidate_scored_target_type_NOT_pre_registered"],
                         "integer")
        self.assertIn("not provide a specific marriage year",
                      r["EXACT_MARRIAGE_YEAR_REQUIRES_DIRECTIONS"]["working_source_gloss_not_original_quote"])
        self.assertFalse(self.notes["original_1647_1659_exact_all_glyphs_expert_collated"])

    def test_09_spouse_attributes_specific_count_direction_and_age_but_unverified(self):
        r={x["role"]:x for x in self.notes["all_source_records"]}
        for role in (
            "FIRST_WIFE_HAIR_COMPLEXION","FIRST_WIFE_FACE_SCARS",
            "SECOND_WIFE_LEFT_FOREHEAD_MOLE",
            "FIRST_WIFE_EAST_SOUTH_FROM_BIRTH","FIRST_WIFE_NOT_SAME_SHIRE",
            "SECOND_WIFE_WEST_FAR","SECOND_WIFE_ENGLISH",
            "WIFE_INHERITS_ESTATE","FORTUNE_AND_TROUBLE_COMBINED"
        ):
            self.assertIn(role,r)
            self.assertFalse(r[role]["actual_merchant_life_and_spouse_outcomes_independently_verified"])
        self.assertFalse(self.notes["source_actual_spouse_appearance_or_money_geography_independently_verified"])

    def test_10_source_months_or_terms_ambiguity_is_not_false_precise_date(self):
        r={x["role"]:x for x in self.notes["all_source_records"]}
        line=r["ESTATE_APPROX_THREE_MONTHS_OR_TERMS"]
        self.assertEqual(line["historical_evidence_category"],
                         "EXPLICIT_HISTORICAL_TIME_AMBIGUITY")
        self.assertIn("or perhaps so many Termes",
                      line["1647_short_original_anchor_not_diplomatic_transcription"])

    def test_11_b07bd_source_rules_acceptance_hash_and_labels(self):
        self.assertEqual(len(self.rules["rules"]),57)
        self.assertEqual(self.rules["rules"],self.notes["all_source_records"])
        self.assertEqual(h(SOURCE),self.accept["source_notes_sha256"])
        self.assertEqual(h(RULES),self.accept["rules_sha256"])
        self.assertEqual(h(MANIFEST),self.accept["original_photo_manifest_sha256"])
        self.assertEqual(self.accept["Lilly_after_if_accepted"],13101)
        self.assertEqual(self.accept["Western_after_if_accepted"],14167)
        self.assertEqual(self.accept["Ptolemy_retained"],1066)
        self.assertEqual(self.accept["next_R"],"R13102")
        self.assertTrue(self.accept["retrospective_known_merchant_cannot_count_as_blind"])

    def test_12_all_records_fail_closed_on_measured_person_outcomes(self):
        for r in self.notes["all_source_records"]:
            self.assertFalse(r["actual_merchant_life_and_spouse_outcomes_independently_verified"])
            self.assertFalse(r["original_astrological_glyphs_full_expert_collation_done"])
            self.assertFalse(r["apply_historical_moral_gender_appearance_claims_to_person"])
            self.assertFalse(r["runtime_astrological_model_promoted"])
            self.assertEqual(r["real_human_behavioral_prediction_validation_count"],0)
        self.assertEqual(self.notes["independent_prospective_human_predictive_tests"],0)
        self.assertEqual(self.notes["astrology_production_promotions"],0)

    def test_13_refuse_mutated_source_image_or_replaced_previous_photo(self):
        import build_b07bd_marriage_source as b
        m=rd(MANIFEST)
        tampered=json.loads(json.dumps(m))
        tampered["folios"]["755"]["1647"]["sha256"]="0"*64
        temp=B/"_test_mutation_temporary.json"
        temp.write_text(json.dumps(tampered))
        try:
            with patch.object(b,"B",B):
                # The function deliberately loads a named immutable manifest;
                # mutate its return by swapping original image witness only
                with patch.object(b,"read",side_effect=lambda p:
                    tampered if p.name==MANIFEST.name else rd(p)):
                    with self.assertRaisesRegex(ValueError,"SHA drift"):
                        b.photo_witnesses()
        finally:
            temp.unlink(missing_ok=True)

    def test_14_cazimi_printed_17_vs_modern_about75_source_math_preserved(self):
        m=self.cazimi
        self.assertEqual(m["printed_Sun_Libra_deg_min"],[6,37])
        self.assertEqual(m["printed_Venus_Libra_deg_min"],[6,54])
        self.assertAlmostEqual(m["printed_natal_separation_arcmin"],17.0,delta=0.0001)
        self.assertAlmostEqual(m["modern_at_nominal_UT_separation_arcmin"],
                               74.604895,delta=0.001)
        self.assertGreater(m["modern_min_separation_arcmin"],73.0)
        self.assertLess(m["modern_max_separation_arcmin"],77)
        self.assertEqual(len(m["modern_UT_reference_only_separations"]),5)
        self.assertTrue(all(row["definitely_outside_17_arcmin"]
                            for row in m["modern_UT_reference_only_separations"]))
        self.assertTrue(m["mechanical_historical_cazimi_premise_not_identical_to_modern_source_under_the_tested_UT_range"])
        self.assertFalse(m["original_orb_within_exact_threshold_independently_verified"])
        self.assertFalse(m["actual_merchant_two_marriages_verified"])

    def test_15_glyph_cazimi_source_rule_separate_from_merchant_biography(self):
        roles={r["role"]:r for r in self.notes["all_source_records"]}
        self.assertEqual(roles["VENUS_LIBRA_CAZIMI"]["candidate_scored_target_type_NOT_pre_registered"],
                         "mechanical_predicate")
        self.assertFalse(self.notes["source_actual_merchant_marriage_count_independently_verified"])
        self.assertTrue(self.cazimi["printed_exact_glyph_date_source_historical_UT_unknown"])

    def test_16_children_images_only_prefetch_next_chapter_not_admitted(self):
        pre=rd(PREFETCH)
        self.assertTrue(pre["not_part_of_B07bd_marriage_physical_source_records"])
        self.assertEqual(pre["accepted_historical_annotations"],0)
        for folio in (758,759):
            q=pre[f"original_1647_folio{folio}"]
            p=ROOT/q["path"]
            self.assertEqual(h(p),q["sha256"])
            self.assertEqual(p.stat().st_size,q["bytes"])

    def test_17_source_layers_are_historical_not_real_validation(self):
        rs=self.notes["all_source_records"]
        types=Counter(r["candidate_scored_target_type_NOT_pre_registered"] for r in rs)
        self.assertGreater(types["integer"],1)
        self.assertGreater(types["mechanical_predicate"],7)
        self.assertGreater(types["physical"],4)
        self.assertGreater(types["navigation"],2)
        self.assertIn(rd(WEST)["records_count"],(13044,13101))


import os
_HAS_SWE=importlib.util.find_spec("swisseph") is not None
_HAS_FILES=all((SWE_EPHE_DIR/x).is_file() for x in ("sepl_12.se1","semo_12.se1"))
@unittest.skipUnless(_HAS_SWE and _HAS_FILES,
                     "Source-only tests pass offline; verified external Swiss .se1 files optional")
class OriginalSunVenusLiveEphemeris(unittest.TestCase):
    def test_18_optional_separate_modern_swiss_true_flag_recompute(self):
        import compute_cazimi_source_vs_modern as m
        current=m.compute(SWE_EPHE_DIR)
        self.assertEqual(current,rd(CAZIMI))
        self.assertTrue(all(row["returned_true_SWIEPH_both"]
                            for row in current["modern_UT_reference_only_separations"]))

    def test_19_corrupt_external_ephe_fails_closed(self):
        import compute_cazimi_source_vs_modern as m
        import tempfile
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)
            (p/"sepl_12.se1").write_bytes(b"bad")
            (p/"semo_12.se1").write_bytes(b"bad")
            with self.assertRaisesRegex(ValueError,"pinned"):
                m.validate_ephe_dir(p)


if __name__=="__main__":
    unittest.main()
