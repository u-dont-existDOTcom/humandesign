#!/usr/bin/env python3
"""Bounded policy-explicit BaZi/partial Zi Wei candidate, NOT validated natal chart.

Input is modern fixed China-standard UTC+08 CIVIL date/hour; does not accept
arbitrary birthplace or 1616 old time standards. Lunar conversion is checked
between SXTWL and lunar_python. Published historical source calculators are
reused for Zi Wei life/body/palace stem; full 14 stars and timings unavailable.
Unlike a full natal chart this is a partial, policy-sensitive candidate and
cannot predict a particular person's behavior, illness, wealth or fate.
"""
from __future__ import annotations
import argparse,json,sys
from dataclasses import dataclass,asdict
from datetime import datetime,timedelta,timezone
from pathlib import Path
from calendar_parity import ganzhi,STEMS,BRANCHES

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tasks/astro-chinese-primary-sources-20261017'))
from ziwei.ziwei_source_mechanics import life_and_body_palaces, palace_stem_from_yin  # noqa: E402

CHINESE_TO_ROMAN_STEM=('Jia','Yi','Bing','Ding','Wu','Ji','Geng','Xin','Ren','Gui')
CHINESE_TO_ROMAN_BRANCH=('Zi','Chou','Yin','Mao','Chen','Si','Wu','Wei','Shen','You','Xu','Hai')
CHINA_CIVIL_FIXED_UTC_PLUS8=timezone(timedelta(hours=8))

@dataclass(frozen=True)
class Candidate:
    input_china_UTC_plus_8: str
    lunar_ymd: tuple[int,int,int]
    source_lunar_leap_month: bool
    bazi_year_LiChun_exact: str
    bazi_month_exact_jieqi: str
    bazi_calendar_day_pillar: str
    bazi_day_23h_next_day_convention: str
    bazi_day_unresolved_for_23h: bool
    bazi_hour_pillar: str
    bazi_four_pillars_if_policy_lunar_python_exact: tuple[str,str,str,str]
    source_sxtwl_four_pillars_date_convention: tuple[str,str,str,str]
    original_sxtwl_has_JieQi_on_date: bool
    sxtwl_exact_year_month_conventions_agree: bool
    sxtwl_lunar_new_year_equals_lunar_python: bool
    ziwei_calendar_year_stem_lunar_new_year: str
    ziwei_month_for_palace_rule: int
    ziwei_chosen_lunar_leap_policy: str
    ziwei_life_palace_partial: str
    ziwei_body_palace_partial: str
    ziwei_life_palace_stem_partial: str
    no_full_ziwei_14_star_calculation: bool
    no_independent_original_calendar_policy_confirmation: bool
    actual_person_predictions_validated: bool
    runtime_model_promoted: bool


def source_candidate(local_utc_plus_8: datetime) -> Candidate:
    if local_utc_plus_8.tzinfo is None or local_utc_plus_8.utcoffset()!=timedelta(hours=8):
        raise ValueError('Require explicit fixed China Standard Time UTC+08:00 input, not arbitrary birthplace')
    if not 1970 <= local_utc_plus_8.year <= 2099:
        raise ValueError('This candidate is scoped to post-1970 China Standard civil dates, not original early modern dates')
    import sxtwl
    from lunar_python import Solar
    y,m,d,h,minute,sec=local_utc_plus_8.year,local_utc_plus_8.month,local_utc_plus_8.day,local_utc_plus_8.hour,local_utc_plus_8.minute,local_utc_plus_8.second
    day=sxtwl.fromSolar(y,m,d)
    lunar=Solar.fromYmdHms(y,m,d,h,minute,sec).getLunar()
    left=(day.getLunarYear(),day.getLunarMonth(),day.getLunarDay(),bool(day.isLunarLeap()))
    right=(lunar.getYear(),abs(lunar.getMonth()),lunar.getDay(),lunar.getMonth()<0)
    if left!=right:raise ValueError('Independent lunar date implementations disagree; do not choose silently')
    sx_lunyear=ganzhi(day.getYearGZ(True));lp_lunyear=lunar.getYearInGanZhi()
    if sx_lunyear!=lp_lunyear:raise ValueError('Independent lunar year GZ implementations disagree')
    year=lunar.getYearInGanZhiExact();month=lunar.getMonthInGanZhiExact()
    day_civil=lunar.getDayInGanZhi();day_exact=lunar.getDayInGanZhiExact();hour=lunar.getTimeInGanZhi()
    sx=(ganzhi(day.getYearGZ(False)),ganzhi(day.getMonthGZ()),ganzhi(day.getDayGZ()),ganzhi(day.getHourGZ(h)))
    if sx[3]!=hour:
        raise ValueError('SXTWL and lunar_python hour-pillar implementations disagree')
    # For late Zi, retain both explicit day-roll conventions. Do not optimize one to a person's outcomes.
    late_zi_unresolved=(h==23 and day_civil!=day_exact)
    hour_roman=CHINESE_TO_ROMAN_BRANCH[BRANCHES.index(hour[1])]
    lunyear_stem_roman=CHINESE_TO_ROMAN_STEM[STEMS.index(lp_lunyear[0])]
    life,body=life_and_body_palaces(abs(lunar.getMonth()),hour_roman,is_leap_month=bool(left[3]),leap_rule='quan_shu_as_next')
    life_stem=palace_stem_from_yin(lunyear_stem_roman,life)
    month_for_life=(abs(lunar.getMonth())%12)+1 if left[3] else abs(lunar.getMonth())
    return Candidate(local_utc_plus_8.isoformat(),tuple(left[:3]),left[3],year,month,day_civil,day_exact,late_zi_unresolved,hour,
      (year,month,day_exact,hour),sx,bool(day.hasJieQi()),sx[0]==year and sx[1]==month,
      sx_lunyear==lp_lunyear,lunyear_stem_roman,month_for_life,'quan_shu_as_next (source-specific, not universal)',
      life,body,life_stem,True,True,False,False)


def uncertainty_envelope(center: datetime, radius_minutes: int) -> dict:
    if not isinstance(radius_minutes,int) or not 0<=radius_minutes<=120:
        raise ValueError('Bounded uncertainty needs an integer radius 0..120 minutes')
    values=[]
    for delta in range(-radius_minutes,radius_minutes+1):
        at=center+timedelta(minutes=delta)
        if at.tzinfo is None or at.utcoffset()!=timedelta(hours=8):raise ValueError('CST offset must be fixed')
        values.append(source_candidate(at))
    def variant(c):
        return {'bazi_exact_four_pillars':list(c.bazi_four_pillars_if_policy_lunar_python_exact),
                'bazi_civil_day_policy':c.bazi_calendar_day_pillar,
                'bazi_late_zi_unresolved':c.bazi_day_unresolved_for_23h,
                'ziwei_partial_life':c.ziwei_life_palace_partial,
                'ziwei_partial_body':c.ziwei_body_palace_partial,
                'ziwei_life_palace_stem':c.ziwei_life_palace_stem_partial}
    uniques={json.dumps(variant(c),sort_keys=True,ensure_ascii=False):variant(c) for c in values}
    return {'time_center_CST_fixed_UTC8':center.isoformat(),'uncertainty_radius_minutes':radius_minutes,
            'evaluated_clock_minute_points':len(values),'possible_distinct_variants':list(uniques.values()),
            'unique_partial_states':len(uniques),
            'all_minute_samples_disagreeing_with_sxtwl_date_level_year_or_month':sum(not x.sxtwl_exact_year_month_conventions_agree for x in values),
            'full_traditional_source_calendar_14_star_engine_verified':False,
            'independent_real_human_predictions_validated':0,'runtime_promotions':0}


def build_demo():
    samples=[('winter_1985_noon',1985,1,29,12,0,0,0),('leap_month_2023',2023,3,22,12,0,0,0),
         ('lichun_2024_China_clock_uncertain',2024,2,4,16,26,0,5),('late_zi_2024_two_day_policies',2024,2,4,23,30,0,0),
         ('leap_day_2000',2000,2,29,12,0,0,0),('october_2026',2026,10,20,12,0,0,0)]
    results={}
    for key,y,m,d,h,mi,s,r in samples:
        at=datetime(y,m,d,h,mi,s,tzinfo=CHINA_CIVIL_FIXED_UTC_PLUS8)
        results[key]={'at_center':asdict(source_candidate(at)),
                      'full_minute_level_time_uncertainty_envelope':uncertainty_envelope(at,r)}
    return {'schema':'PARTIAL_TRADITIONAL_BAZI_ZIWEI_CANDIDATE_CST_EXAMPLES_V1',
      'input_scope':'Modern fixed UTC+08 clock only, NOT general birthplace/timezone, old calendar nor universal charts',
      'bazi_year_and_month_policy':'lunar_python exact JieQi at civil instant (disagreement with SXTWL date-only disclosed)',
      'bazi_day_23h_day_roll_policy':'Both calendar-day and next-day-at-23 alternatives preserved; neither selected as universal for test participants',
      'ziwei_year_policy':'Lunar New Year stem from both SXTWL and lunar_python; not necessarily same as LiChun BaZi year',
      'ziwei_leap_policy':'Quan Shu transmitted source takes leap month as following month; author/lineage alternatives not calibrated',
      'ziwei_source_partial_engine':'Existing source-anchored life_and_body_palaces and palace_stem_from_yin only; NO bureau/14 stars/full timing',
      'demo_scenarios':results,
      'full_natal_engine_validated':False,'human_predictions_validated':0,'runtime_model_promoted':False}

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args();obj=build_demo();args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'scenarios':len(obj['demo_scenarios']),'LiChun_sample_distinct_states':obj['demo_scenarios']['lichun_2024_China_clock_uncertain']['full_minute_level_time_uncertainty_envelope']['unique_partial_states'],'late_Zi_explicit_ambiguity':obj['demo_scenarios']['late_zi_2024_two_day_policies']['at_center']['bazi_day_unresolved_for_23h'],'full_chart_validated':False},indent=2))
if __name__=='__main__':main()
