#!/usr/bin/env python3
"""Two distinct solar-term algorithms: SXTWL JieQi vs Swiss Ephemeris solcross.

SXTWL event JD is encoded as China UTC+08 CIVIL JD, so convert to UT by
subtracting 8h. This is a modern standard-hour reference, not evidence that
historic 1616 birth times were recorded in China standard civil time.
Both implement astronomical 15-degree apparent tropical solar terms. Agreement
therefore checks SOLAR-TERM GEOMETRY only, not original BaZi/ZWDS birth charts.
"""
from __future__ import annotations
import argparse,hashlib,importlib.metadata,json,statistics
from collections import Counter
from pathlib import Path
from western_merchant_diagnostics import EPHE_EXPECTED,UPSTREAM_COMMIT,sha,angular_signed_delta_deg

SOURCE_YEARS=(1615,1616,1617,1618,1700,1800,1900,1985,2024,2026)
CHINA_STANDARD_TIME_OFFSET_HOURS=8

def verify_ephe(path):
    root=Path(path)
    for name,(n,hash_) in EPHE_EXPECTED.items():
        p=root/name
        if not p.is_file() or p.stat().st_size!=n or sha(p)!=hash_:
            raise ValueError('Swiss file not present/exact SHA; refusing ephemeris fallback: '+name)


def build_result(ephemeris_dir):
    import sxtwl,swisseph as swe
    verify_ephe(ephemeris_dir)
    swe.set_ephe_path(str(Path(ephemeris_dir).resolve()))
    records=[]
    for year in SOURCE_YEARS:
        entries=sxtwl.getJieQiByYear(year)
        assert len(entries)==25,(year,len(entries))
        for j,q in enumerate(entries):
            degree=(int(q.jqIndex)*15+270)%360
            ut_jd=float(q.jd)-CHINA_STANDARD_TIME_OFFSET_HOURS/24
            # Allow a *ten-day* look-back. An actual 1616/1617 SXTWL
            # outlier is two days late, and a 12-hour window would select
            # the following YEAR crossing (~363 days later), hiding cause.
            # Solar longitude completes same target only once per year.
            swiss_jd=swe.solcross_ut(float(degree),ut_jd-10,swe.FLG_SWIEPH)
            xx,returned=swe.calc_ut(ut_jd,swe.SUN,swe.FLG_SWIEPH|swe.FLG_SPEED)
            root_x,root_flags=swe.calc_ut(swiss_jd,swe.SUN,swe.FLG_SWIEPH|swe.FLG_SPEED)
            for flags in (returned,root_flags):
                if flags & (swe.FLG_SWIEPH|swe.FLG_MOSEPH|swe.FLG_JPLEPH) != swe.FLG_SWIEPH:
                    raise RuntimeError('Swiss returned Moshier/JPL fallback instead of actual .se1: '+str(flags))
            cal=sxtwl.JD2DD(float(q.jd))
            secs=round((ut_jd-swiss_jd)*86400,5)
            signed_arcsec=round(angular_signed_delta_deg(xx[0],float(degree))*3600,5)
            records.append({'source_year_input':year,'term_index_in_25':j,'jieqi_index':int(q.jqIndex),
                'expected_tropical_sun_longitude_deg':degree,
                'sxtwl_jd_encoded_in_china_civil_UTC_plus_8':round(float(q.jd),12),
                'sxtwl_local_CST_UTC_plus_8':[int(cal.Y),int(cal.M),int(cal.D),int(cal.h),int(cal.m),round(float(cal.s),5)],
                'sxtwl_instant_utc_jd':round(ut_jd,12),'swiss_solcross_utc_jd':round(swiss_jd,12),
                'sxtwl_minus_swiss_solar_term_seconds':secs,'swiss_geocentric_apparent_longitude_at_sxtwl_utc':round(xx[0],9),
                'sxtwl_event_longitude_residual_arcsec':signed_arcsec,
                'swiss_solar_longitude_at_swiss_cross_deg':round(root_x[0]%360,9),
                'swisseph_flags_at_sxtwl':int(returned),'swisseph_flags_at_swiss_cross':int(root_flags),
                'original_astrological_birth_chart_computed':False})
    diffs=[abs(r['sxtwl_minus_swiss_solar_term_seconds']) for r in records]
    stats={str(y):{'events':len([r for r in records if r['source_year_input']==y]),
      'max_abs_disagreement_seconds':round(max(abs(r['sxtwl_minus_swiss_solar_term_seconds']) for r in records if r['source_year_input']==y),5),
      'median_abs_disagreement_seconds':round(statistics.median(abs(r['sxtwl_minus_swiss_solar_term_seconds']) for r in records if r['source_year_input']==y),5)} for y in SOURCE_YEARS}
    anomalies=[r for r in records if abs(r['sxtwl_minus_swiss_solar_term_seconds'])>60]
    # Adjacent-year duplicated LiChun reports can disagree internally in some older years.
    duplicate_checks=[]
    for y in SOURCE_YEARS:
        if y+1 not in SOURCE_YEARS:continue
        late=next(x for x in records if x['source_year_input']==y and x['term_index_in_25']==24)
        early=next(x for x in records if x['source_year_input']==y+1 and x['term_index_in_25']==0)
        duplicate_checks.append({'first_year':y,'next_year':y+1,'same_expected_jieqi_index':3,
          'sxtwl_next_LiChun_inconsistent_duplicate_seconds':round((late['sxtwl_jd_encoded_in_china_civil_UTC_plus_8']-early['sxtwl_jd_encoded_in_china_civil_UTC_plus_8'])*86400,3),
          'duplicate_source_entries_identical':abs(late['sxtwl_jd_encoded_in_china_civil_UTC_plus_8']-early['sxtwl_jd_encoded_in_china_civil_UTC_plus_8'])<1e-8})
    return {'schema':'SXTWL_VS_SWIEPH_25_SOLAR_TERMS_PER_YEAR_V1',
      'purpose':'Partial Chinese astronomical term-boundary numerical cross-implementation check, not classical calendar/horoscope nor prediction validation',
      'term_definition':'24 yearly Jie Qi at apparent solar ecliptic geocentric tropical longitude multiples of 15 degrees, with inclusive extra following Li Chun event',
      'sxtwl_jieqi_index_to_ecliptic_longitude':'(jieqi_index * 15 + 270) modulo 360; index3 LiChun = 315 degrees; index6 vernal equinox = 0 degrees',
      'SXTWL_convention':'JD expressed in China standard UTC+08 civil hour, not true solar time. Explicitly subtract eight hours before Swiss UT comparison.',
      'historical_1616_Beijing_CST_UTC_plus_8_not_an_original_source_time_standard':True,
      'years':list(SOURCE_YEARS),'year_count':len(SOURCE_YEARS),'events_per_year':25,'comparison_events':len(records),
      'libraries':{'sxtwl_version':importlib.metadata.version('sxtwl'),'pyswisseph_distribution_version':importlib.metadata.version('pyswisseph'),'swisseph_C_library_version':swe.version},
      'ephemeris_source_immutable_commit':UPSTREAM_COMMIT,
      'ephemeris_file_witnesses':{n:{'sha256':sha(Path(ephemeris_dir)/n),'bytes':(Path(ephemeris_dir)/n).stat().st_size} for n in sorted(EPHE_EXPECTED)},
      'max_absolute_term_disagreement_seconds':round(max(diffs),5),
      'median_absolute_term_disagreement_seconds':round(statistics.median(diffs),5),
      'comparison_year_summaries':stats,
      'all_25_per_year_kept_unfiltered':True,
      'anomalies_exceed_60_seconds_all_kept':anomalies,
      'anomalies_exceed_60_seconds_count':len(anomalies),
      'cross_year_duplicate_LiChun_consistency_checks':duplicate_checks,
      'swiss_root_search_begins_10_days_before_SXTWL_date_to_preserve_two_day_outliers':True,
      'independent_computed_Chinese_birth_four_pillars_or_14_star_palaces_verified':False,
      'original_traditional_time_zone_and_LiChun_hidden_stem_rules_verified':False,
      'independent_real_human_predictions_validated':0,'runtime_rules_promoted':0,
      'individual_source_versus_swiss_term_results':records}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--ephemeris-dir',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    obj=build_result(args.ephemeris_dir);args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'events':obj['comparison_events'],'max_abs_disagreement_seconds':obj['max_absolute_term_disagreement_seconds'],'median_abs_disagreement_seconds':obj['median_absolute_term_disagreement_seconds'],'per_year':obj['comparison_year_summaries'],'anomalies_exceed_60_seconds_count':obj['anomalies_exceed_60_seconds_count'],'human_validations':0},indent=2))
if __name__=='__main__':main()
