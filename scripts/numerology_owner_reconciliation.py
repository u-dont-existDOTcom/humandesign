#!/usr/bin/env python3
"""Reproduce diagnostic reviewer checks without changing the original 36 tests.

All added selectors here are POST_RESULT sensitivity descriptions, not newly
validated rules and not silently admitted author-method branches.
"""
from datetime import date
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import numerology_owner_comparison as m
r=m.r


def checks():
 c=m.core();d=m.diagnostics(c);years=list(range(2000,2027))
 recurrence=set(c[r.CHEIRO]['birth_year_periodicity'][1:])
 root_match=[];exact_match=[];shifted_match=[];potential=set();rows=[]
 annual_romance_values={34,37,38,39,41,42}
 annual_romance=[]
 for y in years:
  age=y-1985;v=m.at(date(y,7,1),c)['jb'];annual=v['year']['admitted']
  entries={e['number']['admitted'] for e in v['all_entries_at_age']}
  roots={r.root(n) for n in entries}
  if r.root(annual) in roots:root_match.append(y)
  if annual>=10 and annual in entries:exact_match.append(y)
  # This deliberately shifted age is a robustness probe, not a sourced JB rule.
  shifted={e['number']['admitted'] for l in c[r.JB]['triangle']['lines'] for e in l['major']+l['minor'] if e['age']==age+1}
  if annual>=10 and annual in shifted:shifted_match.append(y)
  if annual in annual_romance_values:annual_romance.append(y)
  potential.update(n for n in entries if 32<=n<=42)
  rows.append({'birthday_year':y,'annual_compound':annual,'experience_compounds':sorted(entries),'root_match':y in root_match,'exact_match':y in exact_match})
 simpler=[v for v in d['results'] if v['adapter_id'] in ['CHEIRO_BIRTH_SEED_RECURRENCE__AND__CAMPBELL_CHANGE_PY','CHEIRO_BIRTH_SEED_RECURRENCE__AND__LEGACY_WESTERN_CHANGE_SET']]
 period_windows={}
 for branch,soul in [('literal_DW_vowel',63),('ordinary_W_consonant_sensitivity',58)]:
  period_windows[branch]=[{'start':f'{y}-09-29','end_exclusive':f'{y+1}-01-29'} for y in years if r.jb_periods(m.BORN,y,53,soul)[2]['admitted']==16]
 return {'status':'POST_RESULT_REVIEW_RECONCILIATION','original_coarse_family_changed':False,
 'already_registered_simpler_separators':simpler,
 'root_match_years':root_match,'root_match_and_cheiro_recurrence_years':sorted(set(root_match)&recurrence),
 'exact_match_years':exact_match,'counterfactual_age_plus_one_match_years':shifted_match,
 'shift_status':'UNSOURCED_ROBUSTNESS_PROBE_NOT_AN_ADMITTED_JB_AGE_BRANCH',
 'matching_algebra_2018':'1+29+digit_sum(year) = L12+29 iff digit_sum(year)+1=12. Shared birthday-side29 cancels.',
 'possible_experience_compounds_within_observed_PY_range':sorted(potential),
 'romance_vocabulary_lower_bound':{'selected_source_compounds':sorted(annual_romance_values),'years':annual_romance,'count':len(annual_romance),'denominator':len(years),'definition':'Explicit temporary love/romance/marriage content in these six source rows, not an exhaustive calibrated classifier. Selected after results; other layers can add further coverage.'},
 'third_period16_windows_by_W_branch':period_windows,
 'corrected_2005_essence':{'raw':36,'root':9,'both_jordan_index_branches':True},
 'corrected_2020':{'Jan01_to_Jan28':{'JB_year':42,'completed_age':34,'experience':29},'Jan29_to_Dec31':{'JB_year':34,'completed_age':35,'experience':53}},
 'Jordan_2013_onset_2014_birth_branches':{'birth_start':24,'display_age_minus_one':22,'both_roots':[6,4]},
 '2014_escalation_interval_straddle':{'reported_window':['2014-09-01','2014-11-30'],'literal_period_until_Sep28':15,'literal_period_from_Sep29':16},
 '2010_ego_death_window_W_sensitivity':{'ordinary_W_period16_start':'2010-09-29','overlap_with_broad_Aug01_Sep30_interval_days':2,'exact_event_date_known':False},
 'January2026_context':{'prebirthday_minor':55,'prebirthday_annual39_major50_repeated_in_birthday_year':2016,'postbirthday_minor34_allows_romance_and_quarrels':True},
 'source_minor_major_clarification':'JB pp56–57 says minor-process experiences may be just as important as major-process experiences; labels primarily distinguish current versus longer-range effects, not subjective impact classes.',
 'rows':rows}


def transparency():
 c=m.core();d=m.diagnostics(c)
 return {'status':'POST_RESULT_TRANSPARENCY_CONTROLS','method_count':len(d['results']),'distinct_flag_sets':len({tuple(v['flagged_years']) for v in d['results']}),'selected_label_count':10,
 'controls':[{'id':'ALWAYS_FLAG','flagged_years':d['calendar_years'],'major_hits':8,'major_misses':0,'lower_impact_false_flags':2,'counted_impact_errors':2},{'id':'NEVER_FLAG','flagged_years':[],'major_hits':0,'major_misses':8,'lower_impact_false_flags':0,'counted_impact_errors':8}],
 'lowest_candidate_error':min(v['observed_impact_errors'] for v in d['results']),
 'interpretation':'Always-flag beats all36 on positively selected incomplete labels. This exposes selection bias, not a useful every-year forecast. No full-system predictive superiority established.',
 'original36_unchanged':True,'posterior_hypothesis_count':3,'duality_pair_storage_order':['personal_year','essence'],'official_sample_heading_order':['essence','personal_year'],'lookup_must_use_named_positions':True,
 'named_pair_examples':{'early_2013':{'personal_year':9,'essence':9},'2018':{'personal_year':5,'essence':5},'2022':{'personal_year':9,'essence':5}},'source_coverage_limits':'LAYER_COVERAGE_AND_SOURCE_NOTES.md'}


if __name__=='__main__':
 for name,data in [('review_reconciliation_checks.json',checks()),('transparency_controls.json',transparency())]:
  (m.OUT/name).write_text(json.dumps(data,indent=2)+'\n')
 x=checks();print(json.dumps({k:v for k,v in x.items() if k!='rows'},indent=2))
