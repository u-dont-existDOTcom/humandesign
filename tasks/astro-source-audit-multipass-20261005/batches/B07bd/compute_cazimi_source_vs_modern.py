#!/usr/bin/env python3
"""Lilly CLXXXI Venus Cazimi attribution versus source positions / modern Sun-Venus.

The 1647/1659 printed original marriage chapter explicitly says Venus 'in
Caximi'. Seven printed natal longitudes were preserved earlier in B07ax.
Compare the printed Sun-Venus numerical separation to actual 1616 Julian
modern Swiss Ephemeris with exact version/file/returned SWIEPH checks.
The printed clock's true UT is NOT known; a ±2h reference sensitivity is
declared, not optimized. No natal outcome or marriage history is validated.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys
import argparse

import swisseph as swe

B = Path(__file__).resolve().parent
ROOT=B.parents[3]
SOURCE_PATH = (ROOT / "tasks/astro-source-audit-multipass-20261005/batches/B07ax/"
               "MERCHANT_MERCURY_ANTISCION_ORIGINAL_EDITION_SOURCE_CONFLICT_V1.json")
REFERENCE_CLOCK_UT_HOURS_ASSUMED = 14 + 24 / 60 + 39 / 3600
PINNED_EPHE = {
    "sepl_12.se1": "8dccace2557601a223d5f8a7cf64de4e6bbb8a82b9b130b95a54d49adfbe546d",
    "semo_12.se1": "1c65fdbb854f350d3de36afc3e4ac126a53f360ae4f6dcb57beed7c690e7eb61",
}

def validate_ephe_dir(ephe_dir):
    if not ephe_dir.is_absolute() or not ephe_dir.is_dir():
        raise ValueError("Explicit original ephemeris directory required")
    witnesses={}
    for name,pinned_hash in PINNED_EPHE.items():
        raw=(ephe_dir/name).read_bytes()
        h=sha256(raw).hexdigest()
        if h!=pinned_hash:
            raise ValueError("Original Swiss ephemeris binary hash does not match pinned")
        witnesses[name]={"sha256":h,"bytes":len(raw),"binary_copied_into_repo":False}
    return witnesses
VENUS_THRESHOLD_ARCMIN_FOR_SCREEN_ONLY=17
REFERENCE_HOURS=[-2,-1,0,1,2]

def compute(ephe_dir: Path):
    native=json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    records={r["source_body"]:r for r in native["records"]}
    def zlon(name):
        sign,deg,minutes=records[name]["original_first_1647_and_second_1659_printed_natal_longitude"]
        if sign!="Libra" or type(deg) is not int or type(minutes) is not int:
            raise ValueError(f"Printed Sun/Venus zodiac changed: {name}")
        return 180+deg+minutes/60
    printed_sun=zlon("Sun")
    printed_venus=zlon("Venus")
    if [printed_sun, printed_venus] != [180+6+37/60,180+6+54/60]:
        raise ValueError("Expected original printed Sun and Venus positions changed")
    old_sep=abs(printed_venus-printed_sun)*60
    if abs(old_sep-17)>1e-7:
        raise ValueError("Expected original source 17 arcminute cazimi boundary changed")
    rules=json.loads((B/"ORIGINAL_CLXXXI_1647_1659_MARRIAGE_SOURCE_V1.json").read_text())
    cazimi=[r for r in rules["all_source_records"] if r["role"]=="VENUS_LIBRA_CAZIMI"]
    if len(cazimi)!=1 or "Caximi" not in cazimi[0]["1647_short_original_anchor_not_diplomatic_transcription"]:
        raise ValueError("Original 1647 source CLXXXI explicit Cazimi record absent")
    files=validate_ephe_dir(ephe_dir)
    swe.close()
    swe.set_ephe_path(str(ephe_dir))
    jd=swe.julday(1616,9,19,REFERENCE_CLOCK_UT_HOURS_ASSUMED,swe.JUL_CAL)
    results=[]
    for offset in REFERENCE_HOURS:
        ut_jd=jd+offset/24
        a,af=swe.calc_ut(ut_jd,swe.SUN,swe.FLG_SWIEPH|swe.FLG_SPEED)
        b,bf=swe.calc_ut(ut_jd,swe.VENUS,swe.FLG_SWIEPH|swe.FLG_SPEED)
        if any(not f&swe.FLG_SWIEPH or f&swe.FLG_MOSEPH for f in (af,bf)):
            raise ValueError("Actual SWIEPH returned flags missing in Sun/Venus calculation")
        sep=abs((b[0]-a[0]+180)%360-180)*60
        results.append({
            "original_source_calendar_date_assumed_Julian":[1616,9,19],
            "printed_2_24_39_PM_assumed_to_be_UT":False,
            "hypothetical_UT_offset_hours_from_14_24_39":offset,
            "modern_Sun_Libra_degrees_in_sign":round(a[0]-180,9),
            "modern_Venus_Libra_degrees_in_sign":round(b[0]-180,9),
            "modern_Sun_Venus_separation_arcmin":round(sep,6),
            "definitely_outside_17_arcmin":sep>17,
            "returned_true_SWIEPH_both":True,
            "returned_solar_flags":af,
            "returned_venus_flags":bf,
        })
    if any(not r["definitely_outside_17_arcmin"] for r in results):
        raise ValueError("Modern source position within 17 arcmin changes premise")
    return {
        "study":"Original CLXXXI Venus Cazimi printed statement versus historical old natal table and verified independently computed Swiss Sun Venus",
        "source_1647_1659_marriage_page":"printed755, first PDF789, second DjVu784",
        "source_1647_original_venue_short_anchor":"and in Caximi",
        "source_author_already_knew_merchant":True,
        "original_B07ax_seven_planet_table_original_file_sha256":sha256(SOURCE_PATH.read_bytes()).hexdigest(),
        "modern_2000s_software":"pyswisseph "+swe.version,
        "western_ephemeris_files_outside_repo_checksum_witnesses":files,
        "printed_Sun_Libra_deg_min":[6,37],
        "printed_Venus_Libra_deg_min":[6,54],
        "printed_natal_separation_arcmin":round(old_sep,6),
        "source_printed_nominal_cazimi_threshold_development_17arcmin_borderline":True,
        "original_orb_within_exact_threshold_independently_verified":False,
        "printed_exact_glyph_date_source_historical_UT_unknown":True,
        "modern_UT_reference_only_separations":results,
        "modern_at_nominal_UT_separation_arcmin":results[2]["modern_Sun_Venus_separation_arcmin"],
        "modern_min_separation_arcmin":min(r["modern_Sun_Venus_separation_arcmin"] for r in results),
        "modern_max_separation_arcmin":max(r["modern_Sun_Venus_separation_arcmin"] for r in results),
        "mechanical_historical_cazimi_premise_not_identical_to_modern_source_under_the_tested_UT_range":True,
        "which_historic_edition_or_original_birthday_is_correct":None,
        "actual_merchant_two_marriages_verified":False,
        "actual_human_fate_predictions_validated":0,
        "production_astrological_rule_promotions":0
    }

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--ephe-dir",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    data=compute(args.ephe_dir)
    args.output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
    print("ORIGINAL",data["printed_natal_separation_arcmin"],
          "MODERN_NOMINAL",data["modern_at_nominal_UT_separation_arcmin"],
          "MODERN_RANGE",data["modern_min_separation_arcmin"],data["modern_max_separation_arcmin"],
          "REAL_MARRIAGE_VERIFIED",data["actual_merchant_two_marriages_verified"])
