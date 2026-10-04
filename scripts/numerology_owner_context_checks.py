#!/usr/bin/env python3
"""Explicit post-result DEVELOPMENT hypotheses; never updates an author method.

This companion records why a new pattern is attractive and what it still misses.
It also checks original false-peak windows rather than deleting them.
"""
from datetime import date
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import numerology_owner_comparison as m
r=m.r
OUT=m.OUT


def check():
 c=m.core();years=list(range(2000,2027));rec=set(c[r.CHEIRO]['birth_year_periodicity'][1:])
 repeat=[];double5=[];details=[]
 for y in years:
  v=m.at(date(y,7,1),c);jb=v['jb']
  compounds={e['number']['admitted'] for e in jb['all_entries_at_age']}
  match=jb['year']['admitted']>=10 and jb['year']['admitted'] in compounds
  if match:repeat.append(y)
  if v['calendar_py_root']==5 and v['decoz']['essence']['root']==5:double5.append(y)
  details.append({'birthday_year':y,'JB_personal_year_compound':jb['year']['admitted'],'JB_active_experience_compounds':sorted(compounds),'JB_exact_repeat':match,'Decoz_PY_Essence_5_5':y in double5})
 hypotheses={
  'DEV_JB_YEAR_EXPERIENCE_EXACT_COMPOUND_V1':{'rule':'An admitted compound10–78 occurs both in the birthday Personal Year and an active major/minor Triangle experience at that age. No preferred compound selected.','years':repeat},
  'DEV_CHEIRO_RECURRENCE_AND_JB_EXACT_COMPOUND_V1':{'rule':'Birth-year-seeded Cheiro recurrence AND the JB exact-compound flag.','years':sorted(rec&set(repeat))},
  'DEV_CHEIRO_RECURRENCE_AND_DECOZ_DOUBLE5_V1':{'rule':'Birth-year-seeded Cheiro recurrence AND Personal Year5/Essence5 in the Decoz-role-group arithmetic. This is not the unavailable official5/5 Duality interpretation.','years':sorted(rec&set(double5))}}
 # Same broad interval is kept on both sides: these are source signatures, not
 # full binary predictions of marriage, violence, enlightenment, or death.
 controls=[]
 for key,lo,hi in [('old_child_peak','2011-01-01','2011-01-31'),('old_danger_peak','2012-06-01','2012-08-31'),('old_spiritual_year','2011-01-01','2011-12-31'),('early_pre_relationship_period16','2005-09-29','2006-01-28')]:
  e={'id':key,'label':key,'lo':lo,'hi':hi,'quality':'negative-control window from canonical historical evaluation, not a new event','impact':None,'source':'docs/23_longitudinal_event_discrimination_policy.md; notes/HISTORICAL_TIMING_REVEAL_EVALUATION_2013_2014.md; notes/TIMING_MODEL_LESSONS_20261002.md'}
  controls.append(m.summarize_interval(e,c))
 period16=[]
 for y in years:
  p=r.jb_periods(m.BORN,y,53,63)[2]
  if p['admitted']==16:period16.append({'start':f'{y}-09-29','end_exclusive':f'{y+1}-01-29','compound':16,'branch':'literal_DW_vowel'})
 future=m.at(date(2029,7,1),c)
 fcomp={e['number']['admitted'] for e in future['jb']['all_entries_at_age']}
 return {'status':'POST_RESULT_HYPOTHESIS_NOT_VALIDATION','hypotheses':hypotheses,'comparison_details':details,'double5_years':double5,'known_recurrence_impact_contrast':{'2008':'moderate','2018':'major','one_positive_one_negative_only':True},'no_winner_between_identically_fitting_filters':True,'control_windows':controls,'literal_JB_third_period_16_windows':period16,'future_2029_not_scored':{'cheiro_recurrence':True,'JB_year':future['jb']['year']['admitted'],'JB_experience_compounds':sorted(fcomp),'JB_exact_compound_filter':future['jb']['year']['admitted'] in fcomp,'Decoz_PY':future['calendar_py_root'],'Decoz_Essence':future['decoz']['essence']['raw'],'observed_outcome':None},'limitations':['Hypotheses proposed after seeing the first calculations and known history; retrospective selection is explicit.','Exact repeat is a new project concurrence feature, not an author probability rule.','Compound1-digit coincidences excluded by a declared development choice, not a source mandate.','Removing2008 while keeping2018 improves a two-point development contrast only; neither filter independently establishes predictive value.','Unknown2009 remains unknown even though the double5 flag occurs there.','Period16 in2005 shows why the2014 matching passage cannot establish a safe or specific relationship-danger detector.','Full systems have additional conditional/contextual material; these signatures are not complete author forecasts.']}


if __name__=='__main__':
 data=check();(OUT/'posthoc_context_checks.json').write_text(json.dumps(data,indent=2)+'\n')
 print(json.dumps({k:v for k,v in data.items() if k not in ['comparison_details','control_windows']},indent=2))
 for c in data['control_windows']:print(c['id'],json.dumps(c['states']))
