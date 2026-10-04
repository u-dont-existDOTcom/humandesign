#!/usr/bin/env python3
"""Ancillary chart mechanics and author coverage, not added predictive weights."""
from pathlib import Path
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import numerology_owner_comparison as m
r=m.r


def additional():
 c=m.core();h=r.histogram(m.PARTS);missing=[n for n,count in h.items() if not count]
 # These value computations remain separate from source-specific meanings.
 dec_p=[m.dec_result(1+11),m.dec_result(11+5)]
 dec_p += [m.dec_result(dec_p[0]['value']+dec_p[1]['value']),m.dec_result(1+5)]
 common={'birthday_raw':29,'birthday_root':2,'birth_month':1,'birth_year_sum':23,'birth_year_root':5,'included_number_counts':h,'missing_digits':missing,'subconscious_distinct_digit_count':9-len(missing)}
 result={'scope':'ANCILLARY_ARITHMETIC_NOT_COMPLETE_READING_ENGINE','common_input_counts':common,
 m.DECOZ:{'pinnacles':dec_p,'periods':[m.dec_result(n) for n in [1,29,1985]],'rooted_bridge_differences':{'life_path_expression':7,'life_path_birthday':6,'heart_personality':2},'sun_attitude_root':3,'first_vowel':'O','cornerstone':'J','capstone':'L','hidden_passion':[n for n,count in h.items() if count==max(h.values())],'planes_same_letter_table_as_campbell_not_same_interpretation':True,'current_minor_names':c[m.DECOZ]['current_names']},
 r.CAMPBELL:{'key_first_name':15,'key_value':6,'birthday_value_branches':[11,2],'eccentric_angle_branches':[r.result(6+11,r.CAMPBELL),r.result(6+2,r.CAMPBELL)],'squared_key_birthday':False,'first_vowel':'O','first_vowel_planet':'Jupiter','actual_vowel_sound_class':'UNKNOWN','core_pair_root_relations':{'Soul_Expression':[4,1],'Soul_Path':[4,8],'Expression_Path':[1,8]},'missing_lessons':missing,'subconscious':9-len(missing),'name_change_absorption_dates':'UNKNOWN'},
 r.JORDAN:{'security_letter_count':33,'security_root':6,'core_position_roots':{'Destiny':1,'BirthForce':8,'Heart':4,'Personality':6,'Reality':9},'balance_source_relations':'Heart4 greater than Destiny1, BirthForce8 greater than Destiny1, Reality9; mixed rather than a scalar score','pair_intervals':c[r.JORDAN]['balance_intervals'],'first_letter':'J','first_ordinary_vowel':'O','signature_adoption_dates':'UNKNOWN'},
 r.JB:{'birth_core_activation_roots':{'LifeLesson':8,'Destiny':1,'Power':9,'Soul_literal_DW':9,'Outer_literal_DW':1,'Soul_W_consonant_sensitivity':4,'Outer_W_consonant_sensitivity':6},'blueprint_youth_to_power_boundary':'2012-01-29','blueprint_power_to_wisdom_boundary':'2039-01-29','first_vowel_group':'OE','all_given_letters_sequential_not_parallel':True,'raw_gt78_downstream_branch_retained':True}}
 positions=[]
 for e in m.EVENTS:
  vals={}
  for d in m.date_range(e['lo'],e['hi']):
   age=d.year-1985-((d.month,d.day)<(1,29))
   p={str(o):{'number':dec_p[min(sum(age>=t+o for t in [28,37,46]),3)]['root'],'stage':min(sum(age>=t+o for t in [28,37,46]),3)+1} for o in [0,1]}
   periods={str(o):min(sum(age>=t+o for t in [28,55]),2)+1 for o in [0,1]}
   key=json.dumps([p,periods],sort_keys=True);vals[key]={'pinnacle_value_by_boundary_offset':p,'decoz_period_stage_by_boundary_offset':periods}
  positions.append({'event_id':e['id'],'possible_long_cycle_positions':list(vals.values()),'boundary_offsets_are_explicit_sensitivity_not_an_exact_author_resolution':True})
 result['long_cycle_event_positions']=positions
 return result


if __name__=='__main__':
 (m.OUT/'ancillary_chart_context.json').write_text(json.dumps(additional(),indent=2)+'\n')
 print('Ancillary chart values and all event long-cycle boundary branches saved; no predictive weights introduced.')
