#!/usr/bin/env python3
"""Independent modern-era DE440s/Skyfield vs Swiss .se1 planetary longitudes.

Geocentric apparent ecliptic-of-date tropical coordinates. Treat Mars/Jupiter/
Saturn DE440s targets as barycenters; mark center mismatch rather than imply
exact planetary center identity. The de440s SPK covers 1849–2150 only and
CANNOT independently verify Lilly's historic 1616 merchant nativity.
Coordinates do not validate any chart-to-person predictions.
"""
from __future__ import annotations
import argparse,hashlib,importlib.metadata,json,statistics
from datetime import datetime,timezone
from pathlib import Path
from western_merchant_diagnostics import EPHE_EXPECTED,UPSTREAM_COMMIT,angular_signed_delta_deg,sha

JPL_KERNEL_URL='https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440s.bsp'
JPL_KERNEL_BYTES=32726016
JPL_KERNEL_SHA256='c1c7feeab882263fc493a9d5a5b2ddd71b54826cdf65d8d17a76126b260a49f2'
SAMPLES=((1900,1,1,12),(1985,1,1,12),(2000,1,1,12),(2024,6,1,12),(2026,7,1,12))


def verify_binaries(ephemeris_dir,kernel_file):
    root=Path(ephemeris_dir)
    for name in ('sepl_18.se1','semo_18.se1'):
        n,digest=EPHE_EXPECTED[name];p=root/name
        if not p.is_file() or p.stat().st_size!=n or sha(p)!=digest:
            raise ValueError('Swiss source file unavailable/changed; no Moshier substitution: '+name)
    p=Path(kernel_file)
    if not p.is_file() or p.stat().st_size!=JPL_KERNEL_BYTES or sha(p)!=JPL_KERNEL_SHA256:
        raise ValueError('JPL DE440s original byte SHA/size mismatch; independent comparison unavailable')
    with p.open('rb') as handle:
        magic = handle.read(7)
    if magic != b'DAF/SPK':raise ValueError('JPL file is not a SPICE SPK kernel')


def build_result(ephemeris_dir,kernel_file):
    import swisseph as swe
    import skyfield
    from skyfield.api import load,load_file
    from skyfield.framelib import ecliptic_frame
    verify_binaries(ephemeris_dir,kernel_file)
    swe.set_ephe_path(str(Path(ephemeris_dir).resolve()))
    kernel=load_file(str(Path(kernel_file).resolve()))
    ts=load.timescale(builtin=True)
    objs=(('Sun',swe.SUN,'sun','center'),('Moon',swe.MOON,'moon','center'),('Mercury',swe.MERCURY,'mercury','center'),('Venus',swe.VENUS,'venus','center'),('Mars',swe.MARS,'mars barycenter','barycenter'),('Jupiter',swe.JUPITER,'jupiter barycenter','barycenter'),('Saturn',swe.SATURN,'saturn barycenter','barycenter'))
    rows=[]
    for y,m,d,h in SAMPLES:
        dt=datetime(y,m,d,h,0,0,tzinfo=timezone.utc)
        t_nominal_utc=ts.from_datetime(dt)
        jd=swe.julday(y,m,d,h,swe.GREG_CAL)
        # HISTORICALLY CRUCIAL: Swiss UT1-based old dates are not the same as
        # Skyfield's modern pre-1972 UTC->TT convention. In 1900 these differ
        # by ~44 seconds. Compare *at identical TT*, also retain the bad
        # nominal-UTC comparison to prevent silent repair/accuracy laundering.
        t_common_tt=ts.tt_jd(jd+swe.deltat(jd))
        if not (2396752.5<t_common_tt.tdb<2506352.5):raise ValueError('Date outside official short DE440s coverage')
        naiveTTminusSwissTTseconds=round((t_nominal_utc.tt-t_common_tt.tt)*86400,6)
        for name,planet,target,entity_type in objs:
            x,flags=swe.calc_ut(jd,planet,swe.FLG_SWIEPH)
            if flags & (swe.FLG_SWIEPH|swe.FLG_MOSEPH|swe.FLG_JPLEPH)!=swe.FLG_SWIEPH:
                raise RuntimeError('Swiss fell back from SWIEPH: '+name)
            lat1,lon1,dist1=kernel['earth'].at(t_nominal_utc).observe(kernel[target]).apparent().frame_latlon(ecliptic_frame)
            lat2,lon2,dist2=kernel['earth'].at(t_common_tt).observe(kernel[target]).apparent().frame_latlon(ecliptic_frame)
            nominal_utc_lon=lon1.degrees%360; aligned_tt_lon=lon2.degrees%360
            nominal_delta=angular_signed_delta_deg(nominal_utc_lon,x[0])*3600
            aligned_delta=angular_signed_delta_deg(aligned_tt_lon,x[0])*3600
            rows.append({'utc_timestamp':dt.isoformat(),'planet':name,
              'Swiss_SE1_apparent_geocentric_ecliptic_of_date_tropical_longitude_deg':round(x[0],10),
              'JPL_DE440s_Skyfield_nominal_UTC_mapped_longitude_deg':round(nominal_utc_lon,10),
              'JPL_DE440s_Skyfield_same_TT_longitude_deg':round(aligned_tt_lon,10),
              'JPL_nominal_UTC_minus_Swiss_UT1_signed_arcseconds':round(nominal_delta,6),
              'abs_naive_UTC_comparison_arcseconds':round(abs(nominal_delta),6),
              'JPL_same_TT_minus_Swiss_signed_arcseconds':round(aligned_delta,6),
              'abs_matched_TT_longitude_difference_arcseconds':round(abs(aligned_delta),6),
              'skyfield_nominal_UTC_TT_minus_Swiss_UT1_TT_seconds':naiveTTminusSwissTTseconds,
              'Swiss_deltaT_model_seconds':round(swe.deltat(jd)*86400,6),
              'Swiss_returned_ephemeris_flags':int(flags),'Swiss_returned_mode':'SWIEPH',
              'JPL_kernel_target':target,'JPL_target_type':entity_type,
              'independent_full_original_natal_chart_1616_verified':False})
    absvals=[r['abs_matched_TT_longitude_difference_arcseconds'] for r in rows]
    naive_absvals=[r['abs_naive_UTC_comparison_arcseconds'] for r in rows]
    result = {'schema':'MODERN_JPL_DE440S_VS_SWISS_SE1_PLANETARY_LONGITUDE_DIAGNOSTIC_V1',
      'astronomical_comparison_scope':'Five named civil UT1 nominal timestamps x 7 traditional planets; primary longitude comparison fixes common dynamical terrestrial time (TT). Also retains pre-1972 modern UTC mapping mismatch. No houses/directions, social claims or real humans.',
      'JPL_kernels_nasa_source_URI':JPL_KERNEL_URL,'JPL_original_DE440s_SHA256':sha(kernel_file),
      'JPL_DE440s_bytes':Path(kernel_file).stat().st_size,'JPL_DE440s_coverage':'1849-12-25 to 2150-01-21; EXCLUDES 1616',
      'Swiss_ephemeris_immutable_git_commit':UPSTREAM_COMMIT,
      'Swiss_ephemeris_1900_plus_files_SHA_and_bytes':{n:{'bytes':EPHE_EXPECTED[n][0],'sha256':EPHE_EXPECTED[n][1]} for n in ('sepl_18.se1','semo_18.se1')},
      'libraries':{'pyswisseph_distribution_version':importlib.metadata.version('pyswisseph'),'swisseph_C_library_version':swe.version,'skyfield_version':skyfield.__version__,'jplephem_version':importlib.metadata.version('jplephem'),'numpy_version':importlib.metadata.version('numpy')},
      'independent_implementations':'JPL DE440s SPK via Skyfield/JPLEphem vs Swiss Ephemeris .se1 via PySwissEph; may share upstream planetary observations/model families',
      'JPL_de440s_barycenter_caveat':'Mars, Jupiter, Saturn SPK targets are planetary-system BARYCENTERS, not exact individual planetary centers; geocentric angular differences at sampled dates are separately reported.',
      'sample_nominal_UT1_dates_labeled_UTC_for_modern_software':[datetime(*p,tzinfo=timezone.utc).isoformat() for p in SAMPLES],
      'sample_count':len(SAMPLES),'planet_count':len(objs),'total_independent_planet_comparisons':len(rows),
      'max_absolute_matched_TT_longitude_difference_arcseconds':round(max(absvals),6),
      'median_absolute_matched_TT_longitude_difference_arcseconds':round(statistics.median(absvals),6),
      'matched_TT_disagreements_over_one_arcsecond':[r for r in rows if r['abs_matched_TT_longitude_difference_arcseconds']>1],
      'max_naive_UTC_vs_Swiss_UT1_mismatch_arcseconds':round(max(naive_absvals),6),
      'naive_UTC_vs_UT1_disagreements_over_one_arcsecond':[r for r in rows if r['abs_naive_UTC_comparison_arcseconds']>1],
      'pre_1972_nominal_UTC_vs_UT1_TT_offset_flagged':True,
      'all_errors_and_individual_results_retained':True,
      'historical_1616_original_natal_ephemeris_independently_parity_verified':False,
      'geocentric_tropical_point_calculation_agreement_modern_subset_only':True,
      'Regiomontanus_houses_lunar_calendar_14_stars_and_timing_full_parity_verified':False,
      'prospective_blinded_human_predictive_results':0,'runtime_model_promotions':0,
      'planetary_comparison_records':rows}
    kernel.close()  # avoid leaving the NASA SPK file descriptor open between tests
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--ephemeris-dir',type=Path,required=True);p.add_argument('--jpl-kernel',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    data=build_result(args.ephemeris_dir,args.jpl_kernel)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'n_independent_longitude_comparisons':data['total_independent_planet_comparisons'],'same_TT_max_abs_error_arcsec':data['max_absolute_matched_TT_longitude_difference_arcseconds'],'same_TT_median_abs_error_arcsec':data['median_absolute_matched_TT_longitude_difference_arcseconds'],'same_TT_over_one_arcsecond':len(data['matched_TT_disagreements_over_one_arcsecond']),'naive_UTC_over_one_arcsecond':len(data['naive_UTC_vs_UT1_disagreements_over_one_arcsecond']),'early_1616_covered':False},indent=2))
if __name__=='__main__':main()
