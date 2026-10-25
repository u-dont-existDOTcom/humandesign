"""Generate *synthetic* C31 Swiss-file and angle-parity evidence; no people.

Call with an explicit existing .se1 directory (no network, no downloads):
  python docs/astrology-research-map/generate_hellenistic_c31_synthetic_evidence.py \
      --ephemeris-dir data/ephemeris
"""
import argparse
from datetime import UTC,datetime
import json
from pathlib import Path

from hellenistic_c31_expedition_chart_bridge import (
    joined_lot_diagnostic,swiss_positions,synthetic_angle_comparison,
    uncertified_angle_diagnostic,
)

CASES=(
    (datetime(2000,1,1,12,tzinfo=UTC),0.,0.),
    (datetime(2015,3,20,12,tzinfo=UTC),40.,-75.),
    (datetime(2026,1,1,0,tzinfo=UTC),20.5,-70.),
    (datetime(1999,6,15,3,tzinfo=UTC),-33.,151.),
    (datetime(2012,12,21,0,tzinfo=UTC),55.,12.),
)


def build_evidence(root:Path)->dict:
    from hdmatch.chart.ephemeris import SwissEphemerisProvider
    provider=SwissEphemerisProvider(
        (root/"sepl_18.se1",root/"semo_18.se1")
    )
    samples=[]
    for at,lat,lon in CASES:
        pair=swiss_positions(provider,at)
        angle=uncertified_angle_diagnostic(at,lat=lat,lon=lon)
        indicator=joined_lot_diagnostic(pair,angle)
        geometry=synthetic_angle_comparison(at,lat=lat,lon=lon)
        samples.append({
            "utc":at.isoformat(),
            "synthetic_latitude":lat,
            "synthetic_longitude":lon,
            "verified_planet_pair":indicator["bodies"],
            "uncertified_angle":angle,
            "documentary_lot":indicator["lot"],
            "analytic_angle_check":geometry,
            "real_human_prediction_admissible":False,
        })
    return {
        "schema":"HUMANDESIGN_C31_SYNTHETIC_STRICT_ASTRONOMY_DIAGNOSTIC_V1",
        "source_ancestor":"C30_A582BAAA",
        "real_person_birth_inputs_used":False,
        "historical_prediction_accuracy_estimated":False,
        "Swiss_bodies_strict_flags_and_file_hashes_verified":True,
        "Ascendant_MC_independently_certified":False,
        "UT1_EOP_timezone_disputed_case_resolved":False,
        "sample_count":len(samples),
        "max_asc_difference_arcminutes":max(x["analytic_angle_check"]
                 ["asc_error_arcminutes"] for x in samples),
        "max_mc_difference_arcminutes":max(x["analytic_angle_check"]
                 ["mc_error_arcminutes"] for x in samples),
        "full_birth_time_interval_certified":False,
        "untouched_blind_human_validations":0,
        "production_scorer_modified":False,
        "samples":samples,
    }

if __name__=="__main__":
    cli=argparse.ArgumentParser()
    cli.add_argument("--ephemeris-dir",type=Path,required=True)
    cli.add_argument("--out",type=Path,default=Path(__file__).with_name(
        "HELLENISTIC_C31_SYNTHETIC_STRICT_ASTRONOMY_EVIDENCE_V1.json"))
    args=cli.parse_args()
    data=build_evidence(args.ephemeris_dir.expanduser())
    args.out.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n")
    print("C31_SOURCE_DIAGNOSTIC",data["sample_count"],
          round(data["max_asc_difference_arcminutes"],5),
          round(data["max_mc_difference_arcminutes"],5),
          str(args.out))
