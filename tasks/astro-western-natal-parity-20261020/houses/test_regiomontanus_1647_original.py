"""Lilly's 1647/1659 merchant 4 visible house cusps v modern house systems.

The original book's chart is retrospective and subject known to the author.
Four unblinded original source readings and modern arithmetic agree; these
are source-mechanics checks, NEVER statistically predictive evidence.
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import swisseph as swe

H = Path(__file__).resolve().parent
sys.path.insert(0, str(H))
import source_swieph_regiomontanus_1616 as wh  # noqa: E402
from compute_1616_merchant_swe_parity import EPHE_FILES  # noqa: E402

FROZEN = H / "MERCHANT_1616_FOUR_HOUSE_CUSPS_EIGHT_SYSTEMS_V1.json"
EPHE_DIR = Path("/tmp/hd-western-swe-1616-20261020")
EXTERNAL_READY = (
    swe.version == "2.10.03"
    and all((EPHE_DIR / f).is_file() for f in EPHE_FILES)
)


class OriginalHousesSourceOffline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(FROZEN.read_text())
        cls.reg = next(
            r for r in cls.report["methods"] if r["method"] == "Regiomontanus"
        )

    def test_01_original_two_image_original_edition_SHA_frozen(self):
        source = wh.source_photo_fingerprints()
        self.assertEqual(set(source), set(wh.SOURCE_PHOTOS))
        for identifier, w in source.items():
            self.assertEqual(
                w["sha256"],wh.SOURCE_PHOTOS[identifier]["sha256"]
            )
            self.assertGreater(w["byte_length"], 250_000)
            self.assertTrue(w["human_transcribed_manually"])
            self.assertFalse(w["independently_expert_critical_editional_reading"])
        self.assertEqual(
            self.report["original_source_editions"], source
        )

    def test_02_original_RA_MC_is_222_not_232_source_photo_correction(self):
        self.assertEqual(self.report["source_original_ra_mc_deg_min"], [222, 10])
        self.assertEqual(self.report["source_original_oblique_asc_deg_min"], [312, 10])
        self.assertAlmostEqual(
            wh.SOURCE_OBLIQUE_ASC_DEG-wh.SOURCE_RA_MC_DEG, 90.0
        )
        self.assertEqual(
            self.report["original_oblique_asc_minus_ra_mc"],90
        )
        self.assertEqual(self.report["source_original_latitude_deg"],53.0)

    def test_03_manual_source_four_printed_cusps_1647_and_1659(self):
        self.assertEqual(wh.SOURCE_HOUSE_CUSPS,{
            "ASC":{"house":1,"zodiac":"Capricorn","deg":6,"arcmin":37},
            "HOUSE2":{"house":2,"zodiac":"Aquarius","deg":23,"arcmin":30},
            "HOUSE3":{"house":3,"zodiac":"Aries","deg":18,"arcmin":34},
            "MC":{"house":10,"zodiac":"Scorpio","deg":14,"arcmin":39},
        })
        self.assertEqual(self.report["source_printed_four_numeric_cusp_longitudes"],{
            "ASC": 276.61666667,"HOUSE2":323.5,
            "HOUSE3":18.56666667,"MC":224.65,
        })
        self.assertEqual(len(self.report["source_printed_cusps_glyph_reading"]),4)

    def test_04_original_source_4_regiomontanus_residuals_within_eight_arcmin(self):
        self.assertEqual(self.reg["swe_house_system_code"],"R")
        e=self.reg["source_4_house_cusps"]
        self.assertEqual(set(e),{"ASC","HOUSE2","HOUSE3","MC"})
        for label,expected in {
            "ASC":3.181125,"HOUSE2":4.246141,
            "HOUSE3":-7.512994,"MC":-0.562965,
        }.items():
            self.assertAlmostEqual(
                e[label]["signed_computed_minus_printed_arcmin"],expected,delta=0.001
            )
        self.assertTrue(self.reg["all_four_cusps_within_ten_arcmin"])
        self.assertLess(self.reg["max_abs_residual_arcmin"],8)
        self.assertAlmostEqual(self.reg["median_abs_residual_arcmin"],3.713633,delta=0.001)

    def test_05_six_major_methods_do_not_match_the_original_numeric_cusps(self):
        methods={x["method"]:x for x in self.report["methods"]}
        self.assertEqual(set(methods),set(wh.HOUSE_SYSTEMS))
        self.assertEqual(len(methods),8)
        self.assertEqual(
            {k for k,v in methods.items() if v["all_four_cusps_within_ten_arcmin"]},
            {"Regiomontanus"}
        )
        self.assertGreater(methods["Placidus"]["max_abs_residual_arcmin"],350)
        self.assertGreater(methods["Campanus"]["max_abs_residual_arcmin"],1700)
        self.assertGreater(methods["Alcabitius"]["max_abs_residual_arcmin"],1000)
        self.assertGreater(methods["Porphyry"]["max_abs_residual_arcmin"],900)

    def test_06_source_read_232_misreading_does_not_match_original_Midheaven(self):
        # A visually similar early candidate '232°10′' from the faint source
        # photo is WRONG: both 1647 and 1659 clearly show '222°10′'.
        true_eps=self.report["calculated_true_obliquity_at_original_julian_date_deg"]
        wrong=wh._candidate_houses(232+10/60,true_eps)
        regio=next(v for v in wrong if v["method"]=="Regiomontanus")
        self.assertGreater(regio["max_abs_residual_arcmin"],100)
        self.assertFalse(regio["all_four_cusps_within_ten_arcmin"])

    def test_07_implied_longitude_is_conditional_not_real_birthplace(self):
        rows=self.report["hypothetical_RA_MC_derived_longitudes_for_5_UT_clocks"]
        self.assertEqual(len(rows),5)
        self.assertEqual([r["assumed_printed_clock_mapped_to_UT_offset_hours"]
                          for r in rows],[-2,-1,0,1,2])
        self.assertAlmostEqual(
            rows[2]["conditional_longitude_east_deg_to_match_original_RA_MC"],
            -2.65912169,delta=1e-5
        )
        self.assertGreater(
            rows[0]["conditional_longitude_east_deg_to_match_original_RA_MC"],27
        )
        self.assertLess(
            rows[-1]["conditional_longitude_east_deg_to_match_original_RA_MC"],-32
        )
        self.assertTrue(all(
            not r["longitude_is_independently_real_birthplace_observed"] for r in rows
        ))
        self.assertFalse(self.report["original_merchant_geographical_birth_longitude_known"])

    def test_08_source_witness_retflag_and_de441_original_files_not_redistributed(self):
        self.assertTrue(self.report["actual_obliquity_swieph_flag"])
        self.assertTrue(self.report["returned_obliquity_flags"] & swe.FLG_SWIEPH)
        self.assertFalse(self.report["returned_obliquity_flags"] & swe.FLG_MOSEPH)
        self.assertTrue(self.report["requested_obliquity_swieph"])
        filedata=self.report["original_2026_DE441_file_binary_witnesses"]
        self.assertEqual({k:x["sha256"] for k,x in filedata.items()}, EPHE_FILES)
        self.assertTrue(all(
            not x["released_outside_repo_binary_copied_into_humandesign"]
            for x in filedata.values()
        ))

    def test_09_angle_geometry_longitude_exact_wrap_and_invalid_input(self):
        self.assertEqual(wh.zodiac_absolute_longitude("Scorpio",14,39),224.65)
        self.assertAlmostEqual(wh.zodiac_absolute_longitude("Capricorn",6,37),
                               276+37/60)
        for bad in (("Scorpio",30,0),("Wrong",0,0),("Capricorn",0,60),
                    ("Scorpio",True,0)):
            with self.assertRaises(ValueError):
                wh.zodiac_absolute_longitude(*bad)

    def test_10_false_ephemeris_return_flag_rejected(self):
        with patch.object(wh.swe,"calc_ut",return_value=(
            [23.491,23.489,0,0,0,0],swe.FLG_MOSEPH
        )), self.assertRaisesRegex(ValueError,"actual Swiss Ephemeris"):
            wh._calc_true_obliquity_swieph(2311564.1)

    def test_11_immutable_original_photograph_hash_mismatch_fails(self):
        bad={name:dict(row) for name,row in wh.SOURCE_PHOTOS.items()}
        bad["1647_first_printed_742"]["sha256"]="0"*64
        with (
            patch.object(wh, "SOURCE_PHOTOS", bad),
            self.assertRaisesRegex(ValueError, "image hash"),
        ):
            wh.source_photo_fingerprints()

    def test_12_no_real_human_astrology_validation_from_geometry(self):
        self.assertFalse(self.report["original_printed_clock_was_UT_verified"])
        self.assertFalse(self.report["independently_verified_early_time_or_actual_birthplace"])
        self.assertFalse(self.report["longitude_is_actual_birthplace"])
        self.assertFalse(self.report["source_specific_house_system_predeclared_independently_blind"])
        self.assertEqual(self.report["independent_prediction_on_unseen_humans"],0)
        self.assertEqual(self.report["runtime_forecast_promotions"],0)
        self.assertEqual(self.report["new_accepted_historical_annotation_records"],0)


@unittest.skipUnless(
    EXTERNAL_READY,
    "Pinned source Swiss ephemeris binaries unavailable; offline tests still run",
)
class LiveHouseGeometryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frozen=json.loads(FROZEN.read_text())

    def test_13_recalculate_original_regiomontanus_method_and_7_other_methods(self):
        actual=wh.compute(EPHE_DIR)
        for key in (
            "original_source_editions",
            "source_original_ra_mc_deg_min",
            "source_original_oblique_asc_deg_min",
            "original_2026_DE441_file_binary_witnesses",
            "calculated_true_obliquity_at_original_julian_date_deg",
            "methods",
            "hypothetical_RA_MC_derived_longitudes_for_5_UT_clocks",
        ):
            self.assertEqual(actual[key],self.frozen[key],key)

    def test_14_same_house_MC_via_swiss_houses_ex_given_conditional_clock_longitude(self):
        r=self.frozen
        eps=r["calculated_true_obliquity_at_original_julian_date_deg"]
        JD=swe.julday(1616,9,19,wh.REFERENCE_CLOCK_UT_HOURS_ASSUMED,swe.JUL_CAL)
        sid=swe.sidtime(JD)*15
        longitude=(wh.SOURCE_RA_MC_DEG-sid+180)%360-180
        c_utc,a_utc=swe.houses_ex(JD,wh.LATITUDE_DEG,longitude,b"R")
        c_ra,a_ra=swe.houses_armc(wh.SOURCE_RA_MC_DEG,wh.LATITUDE_DEG,eps,b"R")
        self.assertAlmostEqual(a_utc[2],wh.SOURCE_RA_MC_DEG,delta=1e-8)
        self.assertAlmostEqual(a_ra[0],a_utc[0],delta=2e-4)
        for i in (0,1,2,9):
            self.assertAlmostEqual(c_ra[i],c_utc[i],delta=2e-4)


if __name__=="__main__":
    unittest.main()
