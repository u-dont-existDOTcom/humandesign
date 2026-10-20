#!/usr/bin/env python3
"""Freeze independent Zi Wei chart-engine parity cases before iztro comparison.

The grid is deterministic and contains only synthetic/anonymous calendar dates.
IZTRO charts are engineering controls, NOT independent classical scholarship
or evidence that anybody's life experiences are predicted by astrology.
"""
from __future__ import annotations
import json,hashlib
from datetime import datetime,timezone,timedelta
from pathlib import Path

HERE=Path(__file__).resolve().parent
YEARS=(1970,1972,1985,1990,2000,2010,2014,2020,2023,2024,2025,2026,2050,2099)
MONTHS=(1,2,3,4,6,10)
DAYS=(1,5,15,28)
HOURS=(0,12,18,23)
RESEARCH_SAMPLES=(
 ('winter_1985_China_noon','1985-01-29',12,0),
 ('leap_second_month_2023','2023-03-22',12,0),
 ('2024_pre_LiChun_noon','2024-02-04',12,0),
 ('2024_exact_LiChun_1626','2024-02-04',16,26),
 ('2024_exact_LiChun_1630','2024-02-04',16,30),
 ('2024_after_LiChun_nextday','2024-02-05',12,0),
 ('2024_lateZi_2330','2024-02-04',23,30),
 ('2024_after_lunar_NewYear','2024-02-10',12,0),
 ('2000_Gregorian_leapday','2000-02-29',12,0),
 ('2026_October','2026-10-20',12,0),
)
def hour_index(h:int)->int:
    if not isinstance(h,int) or isinstance(h,bool) or not 0<=h<24:raise ValueError('Invalid civil hour')
    return 12 if h==23 else (h+1)//2

def build():
    cases=[]
    for label,date,h,minute in RESEARCH_SAMPLES:
        at=datetime.fromisoformat(date).replace(hour=h,minute=minute,tzinfo=timezone(timedelta(hours=8)))
        cases.append({'split':'KNOWN_DEVELOPMENT_FIXTURES','synthetic_label':label,'local_CST_fixed_timestamp':at.isoformat(),
          'solar_date_for_Iztro':f'{at.year}-{at.month}-{at.day}','timeIndex_0_to_12':hour_index(h),
          'calendar_clock_minutes_discarded_by_iztro_hour_branch_API': minute!=0,
          'sex_for_Iztro_required_field_but_not_main_star_placement':'male'})
    for y in YEARS:
        for m in MONTHS:
            for d in DAYS:
                for h in HOURS:
                    at=datetime(y,m,d,h,0,0,tzinfo=timezone(timedelta(hours=8)))
                    label=f'deterministic_grid_{y:04}_{m:02}_{d:02}_at_{h:02}'
                    cases.append({'split':'PREDECLARED_SYNTHETIC_GRID_PARITY','synthetic_label':label,'local_CST_fixed_timestamp':at.isoformat(),
                      'solar_date_for_Iztro':f'{y}-{m}-{d}','timeIndex_0_to_12':hour_index(h),
                      'calendar_clock_minutes_discarded_by_iztro_hour_branch_API':False,
                      'sex_for_Iztro_required_field_but_not_main_star_placement':'male'})
    assert len(cases)==10+len(YEARS)*len(MONTHS)*len(DAYS)*len(HOURS)
    return {'schema':'IZTRO_2_6_3_SOURCE_PARITY_FROZEN_INPUT_MANIFEST_V1',
       'upstream_reference_library':'iztro (SylarLong), npm pinned 2.6.3',
       'inputs_are_anonymous_synthetic_calendar_cases':True,
       'solar_dates_interpreted_as_modern_China_civil_date_only':True,
       'reference_iztro_library_fixed_leap_month_policy':True,
       'reference_iztro_gender_input_required_but_scope_main_stars_only':'male',
       'year_policy':'Default reference-library configuration, compared primarily to original source Lunar New Year route. BaZi LiChun is kept separate.',
       'development_fixture_count':10,
       'predeclared_grid_years':list(YEARS),'predeclared_grid_months':list(MONTHS),
       'predeclared_grid_days':list(DAYS),'predeclared_grid_hours':list(HOURS),
       'predeclared_grid_case_count':len(YEARS)*len(MONTHS)*len(DAYS)*len(HOURS),
       'total_predeclared_cases':len(cases),
       'synthetic_personal_predictive_results':0,
       'source_rule_revisions_frozen_before_independent_grid_reference_export':True,
       'cases':cases}
def main():
    p=HERE/'IZTRO_2_6_3_FROZEN_COMPARISON_INPUT_20261020.json'
    data=build();p.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'grid':data['predeclared_grid_case_count'],'development':10,'total':data['total_predeclared_cases'],
          'exact_manifest_SHA256':hashlib.sha256(p.read_bytes()).hexdigest()},indent=2))
if __name__=='__main__':main()
