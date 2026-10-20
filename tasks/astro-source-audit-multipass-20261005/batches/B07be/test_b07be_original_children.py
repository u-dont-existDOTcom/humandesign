"""One folio of original Lilly Children chapter, 1647/1659: NOT medicine.

Source evidence checks are NOT successful independent historical predictions
of the merchant's actual children's count, sex, life, health or occupations.
"""
from hashlib import sha256
import json
from pathlib import Path
import unittest
from unittest.mock import patch

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
INDEX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA=ROOT/"tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
SOURCE=B/"ORIGINAL_1647_1659_CLXXXII_CHILDREN_SOURCE_V1.json"
RULES=B/"RULES.json"
ACCEPT=B/"ACCEPTANCE.json"

def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def sh(p):return sha256(p.read_bytes()).hexdigest()

class OriginalLillyChildren(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s=rd(SOURCE); cls.a=rd(ACCEPT); cls.r=rd(RULES)
        cls.byrole={r["role"]:r for r in cls.s["records"]}

    def test_01_exact_parent_source_frontier(self):
        idx=rd(INDEX)
        self.assertIn(idx["records_count"],(13101,13131))
        self.assertIn(idx["batches"][-1]["id"],("B07bd","B07be"))
        self.assertEqual(idx["empirical_validations"],0)
        self.assertEqual(idx["runtime_promotions"],0)
        self.assertEqual(idx["source_sha256"],
                         "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")

    def test_02_two_original_1647_1659_photos_each_folio_exact_sha_byte(self):
        from build_b07be_children_source import photo_proof
        self.assertEqual(self.s["source_photo_witnesses"],photo_proof())
        for folio,pair in photo_proof().items():
            self.assertIn(folio,("757","758"))
            self.assertEqual(set(pair),{"1647","1659"})
            for ed,p in pair.items():
                fp=ROOT/p["source_photo_path"]
                self.assertTrue(fp.is_file())
                self.assertEqual(fp.stat().st_size,p["photo_bytes"])
                self.assertEqual(sh(fp),p["photo_SHA256"])
                self.assertEqual(p["source_edition"],int(ed))
                self.assertFalse(p["old_whole_edition_DjVu_verified"])

    def test_03_one_full_source_folio_start_and_next_folio_ending(self):
        self.assertEqual(self.s["original_printed_folios_read"],[757,758])
        self.assertTrue(self.s["source_first_and_second_print_folio_757_children"])
        self.assertTrue(self.s["next_first_and_second_print_folio_758_CLXXXIII_travels"])
        self.assertEqual(self.s["original_1647_PDF_frames"],[791,792])
        self.assertEqual(self.s["separately_original_1659_DjVu_frames"],[786,787])
        self.assertEqual(self.s["next_chapter"],"CLXXXIII Of Travels")
        self.assertEqual(self.s["next_source_pdf"],792)

    def test_04_sequential_30_reversible_historical_source_notes(self):
        rs=self.s["records"]
        self.assertEqual(len(rs),30)
        self.assertEqual([r["id"] for r in rs],[f"R{i}" for i in range(13102,13132)])
        self.assertEqual([r["record_number"] for r in rs],list(range(13102,13132)))
        self.assertEqual(len({r["role"] for r in rs}),30)
        self.assertEqual(rs[0]["role"],"CHILDREN_FIFTH_HOUSE_HEADING")
        self.assertEqual(rs[-1]["role"],"TRAVELS_CLXXXIII_NEXT_BOUNDARY")
        self.assertEqual(rs[0]["original_printed_folio"],757)
        self.assertEqual(rs[-1]["original_printed_folio"],758)
        self.assertTrue(all(r["original_printed_folio"]==757 for r in rs[:-1]))

    def test_05_negatives_preserved_before_positive_children_claim(self):
        i={r["role"]:k for k,r in enumerate(self.s["records"])}
        for negative in ("MERCURY_COMBUST_NO_ISSUE","GEMINI_BARREN_REPEATED",
                         "JUPITER_TWELFTH_IMPEDED"):
            self.assertLess(i[negative],i["YES_CHILDREN_FORECAST"])
        self.assertTrue(self.s["source_no_children_countertestimonies_explicit"])
        self.assertTrue(self.s["source_positive_children_prediction_explicit"])
        self.assertTrue(self.s["source_first_suggests_no_issue_then_overrides_with_yes_children"])
        self.assertEqual(self.byrole["YES_CHILDREN_FORECAST"]["original_1647_short_anchor_NOT_full_diplomatic_transcription"],
                         "he shall have Issue")

    def test_06_tentative_four_is_not_final_certified_4_children(self):
        r=self.byrole["PROBABILITY_OF_FOUR_CHILDREN"]
        self.assertIn("probability of four",r["original_1647_short_anchor_NOT_full_diplomatic_transcription"])
        self.assertEqual(r["candidate_future_blind_target_type_NOT_frozen"],"tentative_integer")
        self.assertTrue(self.s["source_conditional_tentative_four_children_not_actual_proven_count"])
        self.assertFalse(self.s["independently_verified_merchant_actual_children_count"])

    def test_07_contradictory_moon_mars_sextile_used_positive_then_negative(self):
        positive=self.byrole["MOON_MARS_SEXTILE_POSITIVE"]
        negative=self.byrole["MOON_MARS_SEXTILE_KILLS_ANOTHER"]
        self.assertEqual(positive["candidate_future_blind_target_type_NOT_frozen"],
                         "mechanical_predicate")
        self.assertEqual(negative["candidate_future_blind_target_type_NOT_frozen"],
                         "negative_life_event")
        self.assertIn("later",positive["historical_interpretation_NOT_original_verbatim"])
        self.assertIn("earlier benefic",negative["historical_interpretation_NOT_original_verbatim"])

    def test_08_historical_stereotyped_child_sex_not_medical_fact(self):
        for role in ("MARS_MALE_SIGN_MALE","SUN_MALE_SIGN_MALE",
                     "MOON_GEMINI_MARS_MALE","MERCURY_POWER_TO_SUN_MALE",
                     "VENUS_MOON_FEMININE_TWO_OR_THREE"):
            self.assertIn(role,self.byrole)
            self.assertFalse(self.byrole[role]["original_sex_gender_and_mortality_theories_medically_true"])
        self.assertTrue(self.s["source_male_female_and_death_claims_historical_only"])
        self.assertFalse(self.s["historical_reproductive_anatomy_medical_truth_verified"])

    def test_09_children_survival_claim_not_observed(self):
        r=self.byrole["FEMALES_MAY_LIVE_MALES_NOT_ALL"]
        self.assertEqual(r["candidate_future_blind_target_type_NOT_frozen"],"negative_life_event")
        self.assertFalse(r["actual_child_counts_or_sexes_independently_confirmed"])
        self.assertFalse(r["independently_validated_real_person_future_outcome"])

    def test_10_separate_next_Travels_chapter_not_tallied_as_child(self):
        r=self.s["records"][-1]
        self.assertEqual(r["original_printed_folio"],758)
        self.assertEqual(r["role"],"TRAVELS_CLXXXIII_NEXT_BOUNDARY")
        self.assertEqual(r["candidate_future_blind_target_type_NOT_frozen"],"navigation")
        self.assertEqual(self.s["next_R"],"R13132")

    def test_11_exact_annotation_bundle_sha(self):
        self.assertEqual(self.r["rules"],self.s["records"])
        self.assertEqual(sh(SOURCE),self.a["source_sha256"])
        self.assertEqual(sh(RULES),self.a["rules_sha256"])
        self.assertEqual(self.a["Lilly_after_if_accepted"],13131)
        self.assertEqual(self.a["Western_after_if_accepted"],14197)

    def test_12_offline_source_hash_fails_closed_when_claimed_image_changed(self):
        import build_b07be_children_source as m
        with patch.object(m,"PARENT",Path("/tmp/does-not-exist")):
            with self.assertRaises(FileNotFoundError):
                m.photo_proof()

    def test_13_every_record_nonpredictive_and_no_prod_promotion(self):
        for r in self.s["records"]:
            self.assertTrue(r["historical_statement_about_known_merchant_only"])
            self.assertFalse(r["actual_child_counts_or_sexes_independently_confirmed"])
            self.assertFalse(r["independently_validated_real_person_future_outcome"])
            self.assertFalse(r["allowed_for_medicine_parenting_reproductive_advice"])
            self.assertFalse(r["runtime_astrological_rule_promoted"])
        self.assertEqual(self.s["genuine_actual_person_predictive_accuracy_validated"],0)
        self.assertEqual(self.s["runtime_astrological_promotions"],0)

    def test_14_independent_old_chinese_V7_unchanged(self):
        self.assertEqual(sh(CHINA),self.a["Chinese_V7_sha256_unchanged"])
        self.assertEqual(rd(CHINA)["sum_source_annotations"],355)

if __name__=="__main__":
    unittest.main()
