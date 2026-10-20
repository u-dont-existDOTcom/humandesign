#!/usr/bin/env python3
"""Independent SWISS astronomical replay of historic Lilly merchant case, source-only.

1647 printed nativity: 19 September 1616, 2:24:39 PM, latitude 53.
The author does NOT supply independently verified place/time-standard nor a
confirmed Julian calendar reading. Thus each alternative is HYPOTHETICAL.
Apparent geocentric tropical positions use Swiss file mode, explicitly
checking returned flags. House results assume longitude 0E solely for
numerical diagnostic; they are NOT original natal chart reconstruction.
"""
from __future__ import annotations

import argparse,hashlib,json
from dataclasses import dataclass
from pathlib import Path

BASE=Path(__file__).resolve().parents[2]
UPSTREAM_COMMIT='3fd0f956d73898b91cc4f67cf18b21af656d1342'
EPHE_EXPECTED={
 'sepl_12.se1':(483743,'8dccace2557601a223d5f8a7cf64de4e6bbb8a82b9b130b95a54d49adfbe546d'),
 'semo_12.se1':(1305932,'1c65fdbb854f350d3de36afc3e4ac126a53f360ae4f6dcb57beed7c690e7eb61'),
 'sepl_18.se1':(484061,'ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66'),
 'semo_18.se1':(1304771,'1ca07bd67c24374d77226180c20a4f9996cba013697894810518e7eb582ca4f7'),
}
NATAL=BASE/'tasks/astro-source-audit-multipass-20261005/batches/B07ax/ORIGINAL_1647_1659_MERCHANT_NATIVITY_30_SOURCE_NOTES_V1.json'
REVIEW=BASE/'tasks/astro-source-audit-multipass-20261005/batches/B07ax/ORIGINAL_MERCURY_ANTISCION_SOURCE_REVIEW_20261019.md'
SIGNS='Aries Taurus Gemini Cancer Leo Virgo Libra Scorpio Sagittarius Capricorn Aquarius Pisces'.split()
# Literal planet longitudes from the accepted 1647+1659 source review (antiscion section).
# These are HISTORICAL printed numbers, not validated observer positions.
SOURCE_PRINTED={
 'Saturn':('Taurus',9,2),'Jupiter':('Sagittarius',21,55),
 'Mars':('Leo',0,54),'Sun':('Libra',6,37),'Venus':('Libra',6,54),
 'Mercury':('Libra',3,34),'Moon':('Gemini',1,44),
}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def angular_signed_delta_deg(computed,printed):
    return ((computed-printed+180)%360)-180

def verify_inputs(ephemeris_dir):
    p=Path(ephemeris_dir).resolve()
    files=[]
    for name,(expected_bytes,expected_sha) in sorted(EPHE_EXPECTED.items()):
        f=p/name
        if not f.is_file() or f.stat().st_size!=expected_bytes or sha(f)!=expected_sha:
            raise ValueError(f'Swiss file missing/changed, cannot treat Moshier fallback as parity: {name}')
        files.append({'basename':name,'bytes':expected_bytes,'sha256':expected_sha,
            'upstream_repository':'aloistr/swisseph','upstream_immutable_commit':UPSTREAM_COMMIT})
    source=json.loads(NATAL.read_text())
    assert source['historic_chart_input_source_only']=={
      'source_printed_year':1616,'source_printed_month_word':'Septemb','source_printed_day':19,
      'source_printed_clock_text':'2 h. 24. 39 P.M.','source_printed_Latitude':53,
      'original_calendar_style_resolved':False,'source_nativity_birth_place_precise_city_verified':False,
      'original_chart_computed_against_modern_ephemeris':False,
      'birth_time_independent_source_certificate':False}
    review=REVIEW.read_text(encoding='utf-8')
    for name,(sign,deg,mn) in SOURCE_PRINTED.items():
        assert f'{name} {deg}°{mn:02d}′ {sign}' in review, f'Source literal changed: {name}'
    return files


def ecliptic_planets(julday, swe):
    objects={'Saturn':swe.SATURN,'Jupiter':swe.JUPITER,'Mars':swe.MARS,'Sun':swe.SUN,'Venus':swe.VENUS,'Mercury':swe.MERCURY,'Moon':swe.MOON}
    rows=[]
    for name,p in objects.items():
        x,flags=swe.calc_ut(julday,p,swe.FLG_SWIEPH|swe.FLG_SPEED)
        source_sign,deg,mn=SOURCE_PRINTED[name]
        printed=SIGNS.index(source_sign)*30+deg+mn/60
        # Swiss returned flags ephemeris mode bits: 2=SWIEPH, 4=MOSEPH, 1=JPLEPH.
        mode=flags & (swe.FLG_SWIEPH|swe.FLG_MOSEPH|swe.FLG_JPLEPH)
        if mode != swe.FLG_SWIEPH:
            raise RuntimeError(f'{name} returned non-SWIEPH mode {mode}, flags {flags}')
        rows.append({'body':name,'computed_tropical_geocentric_longitude_deg':round(x[0]%360,9),
            'computed_speed_degrees_per_day':round(x[3],9),
            'printed_first_original_zodiac_sign':source_sign,'printed_first_original_zodiac_degree':deg,
            'printed_first_original_zodiac_minute':mn,'printed_original_longitude_deg':round(printed,9),
            'computed_minus_printed_signed_arcmin':round(angular_signed_delta_deg(x[0],printed)*60,5),
            'absolute_error_arcmin':round(abs(angular_signed_delta_deg(x[0],printed)*60),5),
            'actual_returned_swiss_flags':int(flags),'returned_ephemeris_mode':'SWIEPH','matches_printed_within_one_arcminute':abs(angular_signed_delta_deg(x[0],printed)*60)<=1})
    return rows


def regio_illustration(jd,swe):
    # 53N is printed; zero geographical longitude is merely a diagnostic assumption.
    cusps,ascmc=swe.houses_ex(jd,53.0,0.0,b'R',0)
    if len(cusps)!=12:
        raise AssertionError('expected 12 house cusps')
    def diff(a,b):return abs(((a-b+180)%360)-180)
    assert diff(cusps[0],ascmc[0])<1e-7
    assert diff(cusps[9],ascmc[1])<1e-7
    assert all(diff((cusps[i]+180)%360,cusps[i+6])<1e-7 for i in range(6))
    c2,a2=swe.houses(jd,53.0,0.0,b'R')
    assert max(diff(x,y) for x,y in zip(cusps,c2))<1e-7
    assert diff(ascmc[0],a2[0])<1e-7
    return {'house_system':'Regiomontanus (R)','printed_latitude_degrees_north':53,
            'illustrative_geographic_longitude_degrees_east':0,
            'original_precise_birthplace_longitude_source_verified':False,
            'source_local_civil_clock_to_UT_conversion_verified':False,
            'cusp_longitudes_deg':[round(x,9) for x in cusps],
            'asc_longitude_deg':round(ascmc[0],9),'mc_longitude_deg':round(ascmc[1],9),
            'antipodal_house_pairs_verified_numerically':True,
            'Swiss_houses_ex_vs_houses_agree_same_library_only':True,
            'independently_verified_against_1616_printed_house_table':False}


def build_result(ephemeris_dir):
    import swisseph as swe
    files=verify_inputs(ephemeris_dir)
    swe.set_ephe_path(str(Path(ephemeris_dir).resolve()))
    # Authorial clock is unconverted. For comparison ONLY, treating clock as UT.
    hour=14+24/60+39/3600
    jul=swe.julday(1616,9,19,hour,swe.JUL_CAL)
    equivalent_greg=swe.julday(1616,9,29,hour,swe.GREG_CAL)
    literal_greg=swe.julday(1616,9,19,hour,swe.GREG_CAL)
    assert abs(jul-equivalent_greg)<1e-10
    assert abs(jul-literal_greg-10.0)<1e-10
    julrows=ecliptic_planets(jul,swe)
    gregrows=ecliptic_planets(literal_greg,swe)
    def summary(rows):return {'mean_abs_printed_difference_arcmin':round(sum(x['absolute_error_arcmin'] for x in rows)/len(rows),4),'greatest_abs_printed_difference_arcmin':max(x['absolute_error_arcmin'] for x in rows), 'all_seven_printed_positions_agree_within_one_arcminute':all(x['matches_printed_within_one_arcminute'] for x in rows)}
    return {'schema':'LILLY_ORIGINAL_1616_JULIAN_VS_GREGORIAN_SWIEPH_DIAGNOSTIC_V1',
        'original_source_1647_source_note_file':'tasks/astro-source-audit-multipass-20261005/batches/B07ax/ORIGINAL_1647_1659_MERCHANT_NATIVITY_30_SOURCE_NOTES_V1.json',
        'original_source_1647_mercury_anti_source_review':'tasks/astro-source-audit-multipass-20261005/batches/B07ax/ORIGINAL_MERCURY_ANTISCION_SOURCE_REVIEW_20261019.md',
        'original_source_note_SHA256':sha(NATAL),'original_edition_antiscion_review_SHA256':sha(REVIEW),
        'software_library':'pyswisseph','swisseph_lib_version':swe.version,
        'programmatic_ephemeris_source':'Swiss Ephemeris immutable commit', 'downloaded_non_committed_binary_files':files,
        'printed_source_civil_date_and_time':'1616-09-19 2 h. 24. 39 P.M.; latitude 53',
        'original_calendar_style_resolved':False,'original_place_longitude_verified':False,'LMT_to_UT_offset_known':False,
        'illustrative_convention':'Treat original 14h24m39 PM as UT and use Earth-centre apparent tropical geocentric ecliptic coordinates; not a confirmed native time.',
        'julian_1616_09_19_JD_UT':round(jul,12),'gregorian_1616_09_29_same_JD_UT':round(equivalent_greg,12),
        'literal_gregorian_1616_09_19_JD_UT':round(literal_greg,12),
        'julian_to_gregorian_1616_calendar_days_difference':10,
        'julian_source_date_interpretation':{'jd_ut':round(jul,12),'printed_comparison_summary':summary(julrows),'planet_rows':julrows,'regiomontanus_assumed_0E_lat53':regio_illustration(jul,swe)},
        'literal_Gregorian_source_date_interpretation':{'jd_ut':round(literal_greg,12),'printed_comparison_summary':summary(gregrows),'planet_rows':gregrows},
        'sun_printed_Libra_6deg37_but_larger_chart_PARITY_unverified':True,
        'independent_second_astronomical_algorithm_compared':False,
        'old_historical_source_year_natal_chart_parity_verified':False,
        'original_historical_house_chart_matched':False,
        'empirical_human_outcomes_or_predictions_validated':0,'runtime_astro_rules_promoted':0}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--ephemeris-dir',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    data=build_result(args.ephemeris_dir)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'ephemeris_version':data['swisseph_lib_version'],'Julian_candidate_summary':data['julian_source_date_interpretation']['printed_comparison_summary'],'Gregorian_candidate_summary':data['literal_Gregorian_source_date_interpretation']['printed_comparison_summary'],'solar_Julian_vs_printed':next(x['computed_minus_printed_signed_arcmin'] for x in data['julian_source_date_interpretation']['planet_rows'] if x['body']=='Sun'),'files_SHA_ok':len(data['downloaded_non_committed_binary_files']),'full_natal_parity_verified':False},indent=2))
if __name__=='__main__':main()
