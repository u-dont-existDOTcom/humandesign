"""C31 real pinned-Swiss synthetic receipt: never interpreted as human evidence."""
import json
from pathlib import Path
import unittest

from hellenistic_c30_dorotheus_expedition_lot import documentary_claim

DATA=Path(__file__).with_name(
    "HELLENISTIC_C31_SYNTHETIC_STRICT_ASTRONOMY_EVIDENCE_V1.json")
FILE_SHA={
    "semo_18.se1":"1ca07bd67c24374d77226180c20a4f9996cba013697894810518e7eb582ca4f7",
    "sepl_18.se1":"ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66",
}


class TestC31SyntheticEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(DATA.read_text(encoding="utf-8"))

    def test_exact_five_source_diagnostics_not_human_results(self):
        x=self.data
        self.assertEqual((x["sample_count"],len(x["samples"])),(5,5))
        self.assertFalse(x["real_person_birth_inputs_used"])
        self.assertFalse(x["historical_prediction_accuracy_estimated"])
        self.assertEqual(x["untouched_blind_human_validations"],0)
        self.assertFalse(x["production_scorer_modified"])

    def test_verified_swiss_manifest_and_unverified_angle_separated(self):
        for r in self.data["samples"]:
            hashes=dict(r["verified_planet_pair"]["local_source_hashes"])
            self.assertEqual(hashes,FILE_SHA)
            self.assertEqual(r["verified_planet_pair"]["status"],
                             "STRICT_SWISS_RETURNED_FILE_VERIFIED")
            self.assertEqual(r["uncertified_angle"]["angle_status"],
                             "SWISS_HOUSES_ANGLE_NOT_INDEPENDENTLY_CERTIFIED")
            self.assertFalse(r["uncertified_angle"]
                             ["independent_angle_parity_certified"])
            self.assertFalse(r["uncertified_angle"]
                             ["full_timezone_UT1_EOP_chain_certified"])

    def test_no_angle_certification_from_small_numerical_errors(self):
        x=self.data
        self.assertLess(x["max_asc_difference_arcminutes"],0.4)
        self.assertLess(x["max_mc_difference_arcminutes"],0.4)
        self.assertFalse(x["Ascendant_MC_independently_certified"])
        self.assertFalse(x["UT1_EOP_timezone_disputed_case_resolved"])
        self.assertFalse(x["full_birth_time_interval_certified"])
        for r in x["samples"]:
            self.assertFalse(r["real_human_prediction_admissible"])
            self.assertFalse(r["analytic_angle_check"]
                             ["human_prediction_angles_certified"])
            self.assertFalse(r["analytic_angle_check"]
                             ["known_disputed_case_compared"])

    def test_lot_replay_is_pure_and_does_not_impute_negatives(self):
        for r in self.data["samples"]:
            body=r["verified_planet_pair"]
            angle=r["uncertified_angle"]
            value=documentary_claim(
                ascendant=angle["asc"],
                moon=body["moon"],saturn=body["saturn"])
            self.assertEqual(value,r["documentary_lot"])
            self.assertTrue(value["not_source_claiming_no_campaign_when_false"])


if __name__=="__main__":
    unittest.main()
