"""Original first/second printing Lilly honours source and Roman title variants.

Known merchant, unverified actual vocation/honours. Text-source parity only.
"""
from hashlib import sha256
import json
from pathlib import Path
import unittest

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
TASK=ROOT/"tasks/astro-source-audit-multipass-20261005"
INDEX=TASK/"LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA=ROOT/"tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
SRC=B/"ORIGINAL_1647_1659_HONOURS_SOURCE_V1.json"
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def sha(p):return sha256(p.read_bytes()).hexdigest()

class HonourSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s=rd(SRC)
        cls.a=rd(B/"ACCEPTANCE.json")
        cls.r=rd(B/"RULES.json")
        cls.byrole={x["role"]:x for x in cls.s["records"]}

    def test_01_prior_canonical_frontier_or_valid_new_accepted_frontier(self):
        i=rd(INDEX)
        self.assertIn(i["records_count"],(13192,13236))
        self.assertIn(i["batches"][-1]["id"],("B07bf","B07bg"))
        if i["records_count"]==13192:
            self.assertEqual(i["next"]["chapter"],"CLXXXIIII")
            self.assertEqual(i["next"]["pdf_page"],794)
            self.assertEqual(i["next"]["printed_page"],760)
        self.assertEqual(i["empirical_validations"],0)

    def test_02_all_eight_two_independent_printings_source_photo_sha(self):
        from build_b07bg_honours_source import original_photos
        witness=original_photos()
        self.assertEqual(witness,self.s["source_photo_witnesses"])
        self.assertEqual(set(witness),{"760","761","762","763"})
        for folio,pair in witness.items():
            self.assertEqual(set(pair),{"1647","1659"})
            for ed,item in pair.items():
                img=ROOT/item["source_photo_path"]
                self.assertEqual(img.stat().st_size,item["original_photo_bytes"])
                self.assertEqual(sha(img),item["original_photo_SHA256"])
                self.assertEqual(item["scan_page"],int(folio)+(34 if ed=="1647" else 29))

    def test_03_honours_p760_762_and_next_friends_distinct(self):
        self.assertEqual(self.s["source_honours_original_folios"],[760,761,762])
        self.assertEqual(self.s["distinct_next_friends_original_start_folio"],762)
        self.assertEqual(self.s["next_original_printed_folio"],762)
        self.assertEqual(self.s["next_original_1647_pdf_frame"],796)
        self.assertEqual(self.s["records"][-1]["role"],"NEXT_FRIENDS_CLXXXIII_PRINTED_HEADING")

    def test_04_printed_Roman_decreases_and_editorial_ordinal_advances(self):
        self.assertEqual(self.s["source_original_printed_Roman_literal_honours"],"CLXXXIIII")
        self.assertEqual(self.s["honours_editorial_numerical_ordinal"],184)
        self.assertEqual(self.s["next_original_chapter_source_label"],
                         "CLXXXIII of Friends (original repeats Travels Roman numeral)")
        self.assertEqual(self.s["next_editorial_source_sequence_ordinal"],185)
        self.assertTrue(self.s["next_chapter_printed_literally_CLXXXIII_reused_from_Travels"])
        self.assertEqual(self.a["next_printed_chapter"],"CLXXXIII")

    def test_05_44_source_units_and_new_record_ordinal(self):
        records=self.s["records"]
        self.assertEqual(len(records),44)
        self.assertEqual([r["id"] for r in records],[f"R{x}" for x in range(13193,13237)])
        self.assertEqual(len({r["role"] for r in records}),44)
        self.assertEqual([r["original_printed_folio"] for r in records],
                         sorted(r["original_printed_folio"] for r in records))
        self.assertEqual(self.s["next_R"],"R13237")

    def test_06_p760_original_honours_header_and_profession_rule(self):
        self.assertEqual(self.s["records"][0]["role"],"HONOURS_CLXXXIIII_SOURCE_BOUNDARY")
        self.assertIn("PROFESSION_NATURAL_SIGNIFICATORS",self.byrole)
        self.assertEqual(self.byrole["PROFESSION_RULE_MARS_SELECTED"][
                         "historical_evidence_type"],"SOURCE_ASTRO_RULE")
        self.assertIn("SOCIAL_RANK_CONDITION_FOR_PROFESSION",self.byrole)

    def test_07_trade_goods_differentiation_not_observed_merchant_job(self):
        for role in ("MARS_LEO_METALS_MINERALS","VENUS_JEWELS_BRACELETS",
                     "MERCURY_ACCOUNTS_MERCHANDISE","MERCURY_SOLAR_BUSINESS"):
            self.assertIn(role,self.byrole)
            self.assertEqual(self.byrole[role]["historical_evidence_type"],
                             "HISTORICAL_UNVERIFIED_VOCATION")
            self.assertFalse(self.byrole[role]["historical_original_actual_career_verified"])

    def test_08_cazimi_repeat_not_second_independent_natal_evidence(self):
        self.assertTrue(self.s["venus_cazimi_repeated_as_professional_honours_premise"])
        self.assertTrue(self.s["previous_original_marriage_cazimi_premise_same_natal_data_not_independent_repeat_evidence"])
        self.assertTrue(self.s["original_1647_Sun_Venus_17arcminute_source_and_modern_75arcminute_disagreement_not_resolved"])
        self.assertEqual(self.byrole["VENUS_CAZIMI_WITH_SUN_REPEATED"][
            "historical_evidence_type"],"REPEATED_UNVERIFIED_CHART_PREMISE")
        self.assertFalse(self.s["no_occupational_honor_income_fame_outcome_verified"] is False)

    def test_09_religion_or_honours_not_known_biographical_truth(self):
        for role in ("PREFERMENT_HONOR_FROM_TRADE","SUDDEN_UNEXPECTED_PREFERMENT",
                     "PREFERMENT_FROM_PRINCE","JUPITER_PUBLIC_OFFICE_HYPOTHESIS"):
            self.assertIn(role,self.byrole)
            self.assertFalse(self.byrole[role]["independent_human_blind_forecast_tested"])
        self.assertTrue(self.s["author_known_merchant"])

    def test_10_qualified_directions_and_industry_preserved(self):
        self.assertIn("CAUTION_GOOD_DIRECTIONS_TO_MC_SUN",self.byrole)
        self.assertIn("UNFAVORABLE_DIRECTIONS_INACTIVE",self.byrole)
        self.assertIn("INDUSTRY_AFFECTS_OUTCOME",self.byrole)
        self.assertEqual(self.byrole["COMPLEX_MULTIPLE_OCCUPATIONS"][
             "candidate_future_observable_type_NOT_frozen"],"career_changes")

    def test_11_rules_and_acceptance_sha_consistent(self):
        self.assertEqual(self.s["records"],self.r["rules"])
        self.assertEqual(self.r["record_count"],44)
        self.assertEqual(sha(SRC),self.a["source_SHA256"])
        self.assertEqual(sha(B/"RULES.json"),self.a["rules_SHA256"])
        self.assertEqual(self.a["Lilly_after_if_accepted"],13236)
        self.assertEqual(self.a["Western_after_if_accepted"],14302)

    def test_12_old_Chinese_V7_original_sha_preserved(self):
        self.assertEqual(sha(CHINA),self.a["Chinese_V7_SHA256_unchanged"])
        self.assertEqual(rd(CHINA)["sum_source_annotations"],355)

    def test_13_no_actual_known_merchant_success_or_promotions(self):
        for row in self.s["records"]:
            self.assertTrue(row["merchant_already_known_to_author"])
            self.assertFalse(row["historical_original_actual_career_verified"])
            self.assertFalse(row["independent_human_blind_forecast_tested"])
            self.assertFalse(row["runtime_astrological_rule_promoted"])
        self.assertEqual(self.s["independent_real_human_predictive_validations"],0)
        self.assertEqual(self.s["runtime_astrological_promotions"],0)

if __name__=="__main__":unittest.main()
