#!/usr/bin/env python3
"""Reproducible SXTWL-vs-lunar_python SOURCE CONVENTION comparison, not chart validation.

Both libraries model traditional Chinese calendar conventions; agreement is
implementation parity, not independent ancient-source authentication, exact
birthplace time, or a demonstrated human prediction. Gregorian inputs are
proleptic and interpreted as China-standard civil dates/hours for this audit.
SXTWL.getYearGZ(False)/getMonthGZ are date-boundary-only; do not coerce their
outputs to claim exact Li Chun instant parity. SXTWL getYearGZ(True) is LUNAR
NEW-YEAR convention; False is the Li-Chun convention. Never cross-compare. All disagreements are retained.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import date, timedelta
from pathlib import Path

STEMS = '甲乙丙丁戊己庚辛壬癸'
BRANCHES = '子丑寅卯辰巳午未申酉戌亥'
YEARS = (1600, 1616, 1700, 1800, 1900, 1950, 1985, 2000, 2014, 2023, 2024, 2025, 2026, 2050, 2099, 2100)

@dataclass(frozen=True)
class Match:
    gregorian_china_calendar_date: str
    china_civil_hour: int
    sxtwl_lunar: tuple[int,int,int,bool]
    lunar_python_lunar: tuple[int,int,int,bool]
    same_lunar: bool
    same_day_pillar: bool
    same_lunar_new_year_pillar: bool
    same_year_pillar_date_vs_exact_time: bool
    same_month_pillar_date_vs_exact_time: bool
    same_hour_pillar: bool
    sxtwl_has_solar_term_on_date: bool
    sxtwl_date_based_pillars: tuple[str,str,str,str]
    lunar_python_clock_based_pillars: tuple[str,str,str,str]
    sxtwl_lunar_year_pillar: str
    lunar_python_lunar_year_pillar: str


def ganzhi(stem_branch: object) -> str:
    return STEMS[stem_branch.tg] + BRANCHES[stem_branch.dz]


def compare_day(y: int, m: int, d: int, *, hh: int = 12) -> Match:
    if not 0 <= hh <= 23:
        raise ValueError('China standard civil hour must be 0..23')
    import sxtwl  # dependency only for explicit research audit
    from lunar_python import Solar
    a = sxtwl.fromSolar(y,m,d)
    lun = Solar.fromYmdHms(y,m,d,hh,0,0).getLunar()
    left = (a.getLunarYear(),a.getLunarMonth(),a.getLunarDay(),bool(a.isLunarLeap()))
    right = (lun.getYear(),abs(lun.getMonth()),lun.getDay(),lun.getMonth() < 0)
    lunar_year_sx = ganzhi(a.getYearGZ(True))  # Chinese Lunar New Year
    lunar_year_lp = lun.getYearInGanZhi()
    sx = (ganzhi(a.getYearGZ(False)),ganzhi(a.getMonthGZ()),ganzhi(a.getDayGZ()),ganzhi(a.getHourGZ(hh)))  # Li Chun calendar date
    lp = (lun.getYearInGanZhiExact(),lun.getMonthInGanZhiExact(),lun.getDayInGanZhiExact(),lun.getTimeInGanZhi())
    return Match(f'{y:04}-{m:02}-{d:02}',hh,left,right,left==right,sx[2]==lp[2],lunar_year_sx==lunar_year_lp,sx[0]==lp[0],sx[1]==lp[1],sx[3]==lp[3],bool(a.hasJieQi()),sx,lp,lunar_year_sx,lunar_year_lp)


def deterministic_sample() -> list[date]:
    dates: set[date] = set()
    for y in YEARS:
        for month in range(1,13):
            for day in (1,4,12,15,22,28):
                dates.add(date(y,month,day))
    for y in (2023,2024,2025):
        p=date(y,1,1)
        while p.year==y:
            dates.add(p); p+=timedelta(days=1)
    # Cover the embedded 1616 merchant source without presuming Julian-vs-Gregorian is resolved.
    for d in ((1616,9,19),(1616,9,29),(1985,1,29),(2023,3,22),(2024,2,4),(2026,10,20)):
        dates.add(date(*d))
    return sorted(dates)


def build_result() -> dict:
    sample=deterministic_sample()
    records=[compare_day(d.year,d.month,d.day) for d in sample]
    fields=['same_lunar','same_day_pillar','same_lunar_new_year_pillar','same_year_pillar_date_vs_exact_time','same_month_pillar_date_vs_exact_time','same_hour_pillar']
    mismatches={field:[asdict(x) for x in records if not getattr(x,field)] for field in fields}
    # This manifest saves EVERY mismatch, not only chosen successes, with stable reproducible samples.
    return {'schema':'CHINESE_DATE_ONLY_TWO_LIBRARY_COMPARISON_V1',
        'calendar_policy':'Proleptic Gregorian input dates, China civil 12:00 clock; sources not independently authenticated. Not exact solar-term instant or historical LMT.',
        'roles':{'sxtwl':'Gregorian-to-lunar, lunar-year if getYearGZ(True), LiChun-year if getYearGZ(False), LiChun-month by DATE, hour pillar at integer civil hour',
                 'lunar_python':'lunar conversion and clock-time exact eight-character conventions'},
        'libraries':{'sxtwl':importlib.metadata.version('sxtwl'),'lunar_python':importlib.metadata.version('lunar_python')},
        'sample_count':len(records),'sample_first':records[0].gregorian_china_calendar_date,
        'sample_last':records[-1].gregorian_china_calendar_date,
        'sample_dates_sha256':hashlib.sha256('\n'.join(x.gregorian_china_calendar_date for x in records).encode()).hexdigest(),
        'counts':{field:{'matched':len(records)-len(mismatches[field]),'mismatched':len(mismatches[field])} for field in fields},
        'mismatches_all':mismatches,
        'fixed_research_examples':[asdict(compare_day(*p,hh=h)) for p,h in [((1616,9,19),12),((1616,9,29),12),((1985,1,29),12),((2023,3,22),12),((2024,2,4),12),((2024,2,4),20),((2024,2,4),23),((2026,10,20),12)]],
        'interpretation_limits':['Agreement of two related implementers is NOT independent physical Chinese manuscript source authenticity.',
          'SXTWL lunar New-Year True vs lunar_python getYearInGanZhi, and SXTWL LiChun False vs lunar_python getYearInGanZhiExact are matched like-for-like. SXTWL solar-term year/month getters are DATE-only; lunar_python exact forms switch at instant within a Jieqi day.',
          'No time-zone/birthplace LMT or Chinese true solar-time conversion; no exact traditional natal calendar validation.',
          'Neither library is used to infer personality, mortality, wealth, moral character or actual human outcomes.'],
        'whole_natal_calendar_chart_engine_verified':False,'independent_real_human_predictions_validated':0,'runtime_astrology_promotions':0}


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    obj=build_result();args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'sample_count':obj['sample_count'],'counts':obj['counts'],'libraries':obj['libraries'],'sample_dates_sha256':obj['sample_dates_sha256'],'report_path':str(args.output)},indent=2))
if __name__=='__main__':main()
