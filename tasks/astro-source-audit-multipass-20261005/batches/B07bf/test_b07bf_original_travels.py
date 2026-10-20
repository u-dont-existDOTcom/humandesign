"""Two first printings Lilly Travels: physical evidence, not tested forecasts."""
from hashlib import sha256
import json
from pathlib import Path
import unittest

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
BASE=ROOT/"tasks/astro-source-audit-multipass-20261005"
SRC=B/"ORIGINAL_1647_1659_TRAVELS_SOURCE_V1.json"
IDX=BASE/"LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA=ROOT/"tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def sha(p):return sha256(p.read_bytes()).hexdigest()

class OriginalSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s=rd(SRC)
        cls.a=rd(B/"ACCEPTANCE.json")
        cls.r=rd(B/"RULES.json")
        cls.byrole={r["source_role"]:r for r in cls.s["records"]}

    def test_01_parent_index_preserved_before_or_after_append(self):
        idx=rd(IDX)
        self.assertIn(idx["records_count"],(13131,13192))
        self.assertIn(idx["batches"][-1]["id"],("B07be","B07bf"))
        self.assertEqual(idx["source_sha256"],
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b")
        self.assertEqual(idx["empirical_validations"],0)

    def test_02_eight_source_original_photo_hashes(self):
        from build_b07bf_travels_source import original_witnesses
        w=original_witnesses()
        self.assertEqual(self.s["four_source_page_first_second_photo_witnesses"],w)
        self.assertEqual(set(w),{"758","759","760","761"})
        for folio,pair in w.items():
            self.assertEqual(set(pair),{"1647","1659"})
            for edition,obj in pair.items():
                p=ROOT/obj["source_photo_path"]
                self.assertEqual(sha(p),obj["sha256"])
                self.assertEqual(p.stat().st_size,obj["bytes"])
                self.assertEqual(obj["source_frame"],int(folio)+(34 if edition=="1647" else 29))

    def test_03_original_travels_folios_and_next_chapter(self):
        self.assertEqual(self.s["source_travels_substantive_folios"],[758,759,760])
        self.assertEqual(self.s["next_original_1647_pdf_frame"],794)
        self.assertEqual(self.s["next_chapter_editorial"],
                         "CLXXXIV Honours, Preferment, Magistery")
        self.assertEqual(self.s["records"][-1]["source_role"],
                         "NEXT_HONOURS_CHAPTER_CLXXXIIII")

    def test_04_records_contiguous_not_duplicated(self):
        rows=self.s["records"]
        self.assertEqual(len(rows),61)
        self.assertEqual([x["id"] for x in rows],[f"R{n}" for n in range(13132,13193)])
        self.assertEqual(len({x["source_role"] for x in rows}),61)
        self.assertEqual([x["printed_original_folio"] for x in rows],
                         sorted(x["printed_original_folio"] for x in rows))

    def test_05_prior_voyages_disclosed_not_astrological_forecasts(self):
        v=self.s["source_retrospective_marginal_voyages"]
        self.assertEqual((v["known_reported_voyages_beyond_sea"],
                          v["known_reported_voyages_to_Barbary"],
                          v["known_reported_voyages_to_Holland"]),(3,2,1))
        self.assertTrue(v["cannot_count_as_out_of_sample_chart_prediction"])
        roles={x["source_role"] for x in self.s["records"]
               if x["already_known_prior_travel_information"]}
        self.assertEqual(roles,{
            "REPORTED_THREE_PREVIOUS_SEA_VOYAGES",
            "REPORTED_TWO_BARBARY_VOYAGES","REPORTED_ONE_HOLLAND_VOYAGE"})
        self.assertFalse(v["external_ship_passenger_log_birth_history_verified"])

    def test_06_specific_risks_conditional_and_unverified(self):
        for r in ("FUTURE_FIRE_THREAT","FUTURE_SHIPWRECK_THREAT",
                  "FUTURE_ROBBERY_RISK","FUTURE_THIEVES_SAILORS"):
            self.assertEqual(self.byrole[r]["historical_evidence_type"],
                             "HISTORICAL_UNVERIFIED_HARM_FORECAST")
            self.assertFalse(self.byrole[r]["independently_validated_conditional_harm_forecast"])
        self.assertTrue(self.s["source_future_disaster_hazards_are_conditional_to_unspecified_directions"])

    def test_07_specific_geographical_source_claims_preserved(self):
        for role in ("SOUTH_BY_WEST_DESTINATIONS","SOUTHEAST_UNLIKELY_JOURNEY",
                     "CAPRICORN_COUNTRIES_HEALTH_SECURITY",
                     "PISCES_COUNTRIES_FORTUNE_GAIN","LIBRA_COUNTRIES_TRADE_REPUTATION",
                     "SAGITTARIUS_COUNTRIES_STOCK"):
            self.assertIn(role,self.byrole)
        self.assertEqual(self.byrole["SOUTHEAST_UNLIKELY_JOURNEY"]["historical_evidence_type"],
                         "NEGATIVE_HISTORICAL_DIRECTION_FORECAST")

    def test_08_source_good_and_bad_rule_overrides_not_resolved(self):
        self.assertTrue(self.s["source_contradictory_mars_benevolent_override_documented"])
        self.assertIn("WAIT_FOR_BENEVOLENT_DIRECTION",self.byrole)
        self.assertIn("BENEVOLENT_CAN_CONTRADICT_MARS",self.byrole)
        self.assertIn("RELIGIOUS_DREAMS_EXPLICIT_DEFERENCE",self.byrole)

    def test_09_index_shas_and_counts_match(self):
        self.assertEqual(self.s["records"],self.r["rules"])
        self.assertEqual(self.r["record_count"],61)
        self.assertEqual(sha(SRC),self.a["source_sha256"])
        self.assertEqual(sha(B/"RULES.json"),self.a["rules_sha256"])
        self.assertEqual(self.a["Lilly_after_if_accepted"],13192)
        self.assertEqual(self.a["Western_after_if_accepted"],14258)

    def test_10_independent_chinese_source_not_rewritten(self):
        self.assertEqual(sha(CHINA),self.a["Chinese_V7_sha256_unchanged"])
        self.assertEqual(rd(CHINA)["sum_source_annotations"],355)

    def test_11_source_only_no_person_prediction(self):
        for r in self.s["records"]:
            self.assertTrue(r["author_already_knows_merchant"])
            self.assertFalse(r["independently_blind_real_human_prediction"])
            self.assertFalse(r["astrological_runtime_rule_promoted"])
        self.assertEqual(self.s["human_prospective_blinded_outcomes_verified"],0)
        self.assertEqual(self.s["human_retro_blinded_outcomes_verified"],0)
        self.assertEqual(self.s["production_astrology_runtime_promotions"],0)

if __name__=="__main__":unittest.main()
