"""Research-only source bridge: verified planets, unverified Ascendant."""
import importlib.util
from datetime import UTC,datetime
from decimal import Decimal
import unittest

from hellenistic_c31_expedition_chart_bridge import (
    ANGLE_STATUS,BODY_STATUS,VerifiedBodyPair,
    circular_distance,closed_lot_indicator_envelope,
    joined_lot_diagnostic,mean_geometric_angles,
    swiss_positions,synthetic_angle_comparison,
)


class TestC31ChartBridge(unittest.TestCase):
    def test_mock_provider_rejected_even_if_looks_like_swiss(self):
        with self.assertRaises(ValueError):
            swiss_positions(object(),datetime(2000,1,1,12,tzinfo=UTC))

    def test_naive_time_rejected_prior_to_any_live_ephemeris(self):
        with self.assertRaises(ValueError):
            swiss_positions(object(),datetime(2000,1,1,12))

    def test_unverified_angle_never_qualifies_as_prediction(self):
        body=VerifiedBodyPair("2000-01-01T12:00:00+00:00","20","100",
                              "test",(("semo_18.se1","123"),("sepl_18.se1","abc")))
        ang={"asc":"45","mc":"15","angle_status":ANGLE_STATUS,
             "independent_angle_parity_certified":False,
             "full_timezone_UT1_EOP_chain_certified":False}
        x=joined_lot_diagnostic(body,ang)
        self.assertFalse(x["eligible_for_human_prediction"])
        self.assertFalse(x["evaluated_real_human_outcomes"])
        self.assertEqual(x["lot"]["lot_sign"],"Aquarius")
        self.assertEqual(x["lot"]["source_claim_status"],
                         "SOURCE_PREDICTS_MILITARY_CAMPAIGN")
        ang["independent_angle_parity_certified"]=True
        with self.assertRaises(ValueError):
            joined_lot_diagnostic(body,ang)

    def test_invalid_body_and_unlabelled_angle_fail_closed(self):
        bad=VerifiedBodyPair("x","20","100","test",(),status="UNTRUSTED")
        with self.assertRaises(ValueError):
            joined_lot_diagnostic(bad,{"asc":"0","angle_status":ANGLE_STATUS})
        good=VerifiedBodyPair("x","20","100","test",(),status=BODY_STATUS)
        with self.assertRaises(ValueError):
            joined_lot_diagnostic(good,{"asc":"0"})

    def test_closed_interval_one_sign_stable_but_not_a_prediction(self):
        r=closed_lot_indicator_envelope(
            asc=("9","9.2"),moon=("10","10.1"),saturn=("0","0"))
        self.assertEqual(r["possible_signs"],["Aries"])
        self.assertEqual(r["possible_indicator_values"],[True])
        self.assertTrue(r["constant_indicator_if_envelopes_proven"])
        self.assertFalse(r["real_person_claim_allowed"])

    def test_crossing_capricorn_aquarius_still_positive(self):
        r=closed_lot_indicator_envelope(
            asc=("299.9","300.1"),moon=("0","0"),saturn=("0","0"),
            bounds_continuously_certified=True)
        self.assertEqual(r["possible_signs"],["Aquarius","Capricorn"])
        self.assertEqual(r["possible_indicator_values"],[True])
        self.assertTrue(r["constant_indicator_if_envelopes_proven"])
        self.assertTrue(r["input_enclosures_certified"])
        self.assertFalse(r["Ascendant_angle_audit_complete"])
        self.assertFalse(r["real_person_claim_allowed"])

    def test_one_way_positive_negative_boundary_270(self):
        r=closed_lot_indicator_envelope(
            asc=("269.9","270.1"),moon=("0","0"),saturn=("0","0"))
        self.assertEqual(r["possible_signs"],["Capricorn","Sagittarius"])
        self.assertEqual(r["possible_indicator_values"],[False,True])
        self.assertFalse(r["constant_indicator_if_envelopes_proven"])

    def test_circular_boundary_360_cannot_be_endpoint_only(self):
        r=closed_lot_indicator_envelope(
            asc=("359.9","360.1"),moon=("0","0"),saturn=("0","0"))
        self.assertEqual(r["possible_signs"],["Aries","Pisces"])
        self.assertEqual(r["possible_indicator_values"],[False,True])
        n=closed_lot_indicator_envelope(
            asc=("-0.1","0.1"),moon=("0","0"),saturn=("0","0"))
        self.assertEqual(n["possible_signs"],["Aries","Pisces"])

    def test_wide_interval_covers_every_sign(self):
        r=closed_lot_indicator_envelope(
            asc=("-1","360"),moon=("0","0"),saturn=("0","0"))
        self.assertEqual(len(r["possible_signs"]),12)
        self.assertEqual(r["possible_indicator_values"],[False,True])

    def test_correlated_extrema_widen_conservatively(self):
        r=closed_lot_indicator_envelope(
            asc=("0","0"),moon=("290","292"),saturn=("1","3"))
        self.assertEqual((r["unwrapped_lot_min_deg"],r["unwrapped_lot_max_deg"]),
                         ("287","291"))
        self.assertEqual(r["possible_indicator_values"],[True])

    def test_bad_envelopes_fail(self):
        inputs=[
            {"asc":("10","9"),"moon":("0","0"),"saturn":("0","0")},
            {"asc":("NaN","20"),"moon":("0","0"),"saturn":("0","0")},
            {"asc":("0","0"),"moon":("Infinity","0"),"saturn":("0","0")},
        ]
        for x in inputs:
            with self.subTest(x=x),self.assertRaises(ValueError):
                closed_lot_indicator_envelope(**x)
        with self.assertRaises(ValueError):
            closed_lot_indicator_envelope(
                asc=("0","0"),moon=("0","0"),saturn=("0","0"),
                bounds_continuously_certified="yes")

    def test_mean_angle_rejects_ambiguous_and_out_of_horizon(self):
        with self.assertRaises(ValueError):
            mean_geometric_angles(datetime(2000,1,1),lat=0,lon=0)
        with self.assertRaises(ValueError):
            mean_geometric_angles(datetime(2000,1,1,tzinfo=UTC),
                                  lat=90,lon=0)

    @unittest.skipUnless(importlib.util.find_spec("swisseph"),
                         "optional Swiss angle comparison needs pyswisseph")
    def test_synthetic_mean_geometry_is_near_swiss_but_not_certified(self):
        cases=[
            (datetime(2000,1,1,12,tzinfo=UTC),0.0,0.0),
            (datetime(2015,3,20,12,tzinfo=UTC),40.0,-75.0),
            (datetime(2026,1,1,0,tzinfo=UTC),20.5,-70.0),
            (datetime(1999,6,15,3,tzinfo=UTC),-33.0,151.0),
            (datetime(2012,12,21,0,tzinfo=UTC),55.0,12.0),
        ]
        for time,lat,lon in cases:
            with self.subTest(iso=time.isoformat()):
                r=synthetic_angle_comparison(time,lat=lat,lon=lon)
                self.assertLess(r["asc_error_arcminutes"],0.4)
                self.assertLess(r["mc_error_arcminutes"],0.4)
                self.assertFalse(r["human_prediction_angles_certified"])
                self.assertFalse(r["known_disputed_case_compared"])
                self.assertTrue(r["UT1_nutation_and_EOP_unverified"])

if __name__=="__main__":
    unittest.main()
