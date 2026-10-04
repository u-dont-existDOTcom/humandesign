#!/usr/bin/env python3
"""Reproduce owner-development arithmetic without changing frozen author methods.

All outputs are retrospective diagnostics, not validated forecasts. The source
reference is imported unchanged. Any diagnostic flag is explicitly an adapter,
not the full reading of an author. Unknown years never enter the negative class.
"""
from __future__ import annotations
import calendar
from datetime import date, timedelta
import hashlib
import itertools
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import numerology_book_reference as r

OUT = ROOT / "experiments/numerology/owner_comparison_20261004"
BORN = date(1985, 1, 29)
PARTS = ["JOEL", "EDWARD", "SANE", "TODD", "DANIEL", "ROSENBLUM"]
CURRENT = ["JOEL", "ROSENBLUM"]
ROLES = [PARTS[0], "".join(PARTS[1:-1]), PARTS[-1]]
DECOZ = "DECOZ_CURRENT_V1"
MASK_C = ["".join("V" if c in "AEIOU" else "C" for c in p) for p in PARTS]
MASK_W = MASK_C.copy()
MASK_W[1] = "VCVVCC"  # EDWARD: W after D, explicitly labelled JB literal branch.
# Correct exact mask construction prevents a manually shifted letter index.
MASK_W[1] = "".join("V" if c in "AEIOU" or i == 2 else "C" for i, c in enumerate(PARTS[1]))

EVENTS = [
 {"id":"father_loss", "label":"Father's death", "lo":"2002-06-05", "hi":"2002-06-05", "quality":"strongly anchored memory", "impact":"major", "source":"notes/FATHER_LOSS_TIMING_V4_DEVELOPMENT_RESULT_20261002.md"},
 {"id":"first_major_love", "label":"First major love, Cuba", "lo":"2005-07-21", "hi":"2005-07-31", "quality":"approximate memory", "impact":"major", "source":"notes/CHALDEAN_LIFE_EVENT_RETRODIAGNOSTIC_20261003.md", "interval_note":"Late July is operationalized as21–31; no exact day claimed."},
 {"id":"relationship_rupture_2008", "label":"Relationship rupture", "lo":"2008-01-01", "hi":"2008-12-31", "quality":"approximate memory", "impact":"moderate", "source":"experiments/astrohd/chaldean_life_event_retrodiagnostic_20261003.json"},
 {"id":"ego_death", "label":"First reported ego-death experience", "lo":"2010-08-01", "hi":"2010-09-30", "quality":"strongly anchored memory", "impact":"major", "source":"notes/TIMING_MODEL_LESSONS_20261002.md", "interval_note":"Contemporaneous August-use anchor supports era, not exact experience date; September is the narrower recollection."},
 {"id":"nibbana", "label":"First reported nibbana breakthrough", "lo":"2013-01-07", "hi":"2013-01-20", "quality":"strongly anchored memory", "impact":"major", "source":"notes/EXPERIENTIAL_TRANSITION_2013_CHRONOLOGY_CORRECTION_20261003.md", "interval_note":"Jan6 contemporary email plus days-later memory; Jan7–14 narrower,Jan20 conservative end. No documentary exact event timestamp."},
 {"id":"relationship_onset_2013", "label":"Relationship onset", "lo":"2013-03-01", "hi":"2013-03-31", "quality":"approximate memory", "impact":"major", "source":"notes/HISTORICAL_TIMING_REVEAL_EVALUATION_2013_2014.md"},
 {"id":"son_birth", "label":"Son's birth", "lo":"2014-01-12", "hi":"2014-01-12", "quality":"strongly anchored memory", "impact":"major", "source":"notes/HISTORICAL_TIMING_REVEAL_EVALUATION_2013_2014.md"},
 {"id":"danger_escalation", "label":"Relationship danger escalation", "lo":"2014-09-01", "hi":"2014-11-30", "quality":"approximate memory", "impact":"major", "source":"notes/HISTORICAL_TIMING_REVEAL_EVALUATION_2013_2014.md"},
 {"id":"relationship_2018", "label":"Major relationship", "lo":"2018-05-01", "hi":"2018-08-31", "quality":"approximate memory", "impact":"major", "source":"notes/CHALDEAN_LIFE_EVENT_RETRODIAGNOSTIC_20261003.md", "interval_note":"Midyear memory operationalized conservatively May–August; not a dated onset record."},
 {"id":"separation_2020", "label":"Separation", "lo":"2020-01-01", "hi":"2020-12-31", "quality":"approximate memory", "impact":"major", "source":"notes/CHALDEAN_LIFE_EVENT_RETRODIAGNOSTIC_20261003.md"},
 {"id":"mother_loss", "label":"Mother's death", "lo":"2022-09-19", "hi":"2022-09-19", "quality":"strongly anchored memory", "impact":"low", "source":"notes/TIMING_MODEL_LESSONS_20261002.md", "interval_note":"Low impact on life trajectory, not a denial that the death occurred."},
 {"id":"romance_2026", "label":"January romance", "lo":"2026-01-01", "hi":"2026-01-31", "quality":"approximate memory", "impact":"major", "source":"notes/CHALDEAN_LIFE_EVENT_RETRODIAGNOSTIC_20261003.md", "interval_note":"Exact day unknown; must retain pre/postJan29 branches."}
]


def reduce(n, masters=(11,22,33)):
    return r.reduction(n,masters)[-1]


def dec_result(n):
    return {"raw":n,"chain":r.reduction(n,(11,22,33)),"value":reduce(n),"root":r.root(n)}


def dec_name(parts, selection="all"):
    totals=[sum(r.COMPACT[c] for c in p if selection=="all" or (c in "AEIOU")== (selection=="vowels")) for p in parts]
    components=[reduce(n) for n in totals]
    return {"component_raw":totals,"component_addends":components,"result":dec_result(sum(components))}


def core():
    c={"input":{"born":BORN.isoformat(),"birth_components":PARTS,"current_components":CURRENT,"decoz_transit_role_groups":ROLES,"W_masks":{"ordinary_consonant":MASK_C,"JB_D_following_W_vowel":MASK_W},"pronunciation_not_observed":True}}
    c[r.CHEIRO]={"birth":r.date_number(BORN,r.CHEIRO),"current_name":r.name_number(CURRENT,r.CHEIRO),"birth_year_periodicity":r.periodicity(1985,4)}
    c[DECOZ]={"life_path":dec_result(sum(reduce(n) for n in [1,29,1985])),"birthday":dec_result(29),"names":{k:dec_name(PARTS,k) for k in ["all","vowels","consonants"]},"current_names":{k:dec_name(CURRENT,k) for k in ["all","vowels","consonants"]},"planes":r.planes(PARTS,r.CAMPBELL),"histogram":r.histogram(PARTS),"challenges":r.challenges(1,29,1985,r.JORDAN),"period_values":[1,11,5],"period_age_boundaries":[28,55],"pinnacle_age_boundaries":[28,37,46],"boundary_sensitivity":"begin at computed age or after its inclusive closing year; no outcome-selected lead-in"}
    c[DECOZ]["maturity"]=dec_result(c[DECOZ]["life_path"]["value"]+c[DECOZ]["names"]["all"]["result"]["value"])
    c[DECOZ]["balance"]=r.root(sum(r.COMPACT[p[0]] for p in PARTS))
    c[DECOZ]["rational_thought"]=r.root(29+sum(r.COMPACT[x] for x in PARTS[0]))
    c[DECOZ]["minor_interpretation_resource_gap"]="81-Duality complete bank not present in frozen payload; do not fabricate it from Jordan."
    c[r.JORDAN]={"birth_force":r.date_number(BORN,r.JORDAN),"names":{k:r.name_number(PARTS,r.JORDAN,selection=k) for k in ["all","vowels","consonants"]},"planes":r.planes(PARTS,r.JORDAN),"intensification_counts":r.histogram(PARTS),"habit_security":r.root(sum(map(len,PARTS))),"letter_count":sum(map(len,PARTS)),"challenges":r.challenges(1,29,1985,r.JORDAN),"pinnacles":r.pinnacles(1,29,1985,r.JORDAN),"boundary_ages":[28,37,46],"table_indexing_branches":["birth_start","display_age_minus_one"]}
    j=c[r.JORDAN];j['reality']=r.result(j['birth_force']['result']['root']+j['names']['all']['result']['root'],r.JORDAN)
    j['balance_intervals']=r.jordan_balance_intervals({'heart':j['names']['vowels']['result']['root'],'destiny':j['names']['all']['result']['root'],'birth_force':j['birth_force']['result']['root'],'reality':j['reality']['root']})
    c[r.CAMPBELL]={"branches":{m:{"life_path":r.date_number(BORN,r.CAMPBELL,component_masters=m),"names":{k:r.name_number(PARTS,r.CAMPBELL,masks=MASK_C,selection=k,component_masters=m,campbell_letters="literal") for k in ["all","vowels","consonants"]},"pinnacles":r.pinnacles(1,29,1985,r.CAMPBELL,component_masters=m)} for m in ['retain','root']},"no_K_or_V_in_owner_birth_name":True,"planes":r.planes(PARTS,r.CAMPBELL),"ruling_passion":r.campbell_ruling_passion(PARTS),"challenges":r.challenges(1,29,1985,r.CAMPBELL),"cycle_candidates":[r.campbell_cycle_candidates(BORN,a) for a in [28,56]],"key":r.name_number([PARTS[0]],r.CAMPBELL,component_masters='retain'),"cornerstone":"J","first_vowel":"O","sound_class":"UNRESOLVED_NO_AUDIO","impression_formula":"UNSPECIFIED_BY_AUTHOR"}
    c[r.JB]={"life_lesson":r.date_number(BORN,r.JB),"branches":{label:{k:r.name_number(PARTS,r.JB,masks=mask,selection=k) for k in ['all','vowels','consonants']} for label,mask in [('literal_DW_vowel',MASK_W),('ordinary_W_consonant_sensitivity',MASK_C)]},"triangle":r.jb_triangle(PARTS[:-1],BORN),"first_vowel_group":"OE (book explicitly lists Joel as example)","letter_counts":dict(__import__('collections').Counter(''.join(PARTS)))}
    for label,b in c[r.JB]['branches'].items():
        b['power_admitted']=r.jb_power(b['all']['result']['admitted'],c[r.JB]['life_lesson']['admitted'])
        b['power_raw_sensitivity']=r.jb_power(b['all']['result']['raw'],c[r.JB]['life_lesson']['admitted'])
        b['missing']=r.jb_missing(PARTS,[c[r.JB]['life_lesson']['admitted']]+[b[k]['result']['admitted'] for k in ['all','vowels','consonants']]+[b['power_admitted']['admitted']])
    return c


def at(d, c):
    age=d.year-BORN.year-((d.month,d.day)<(1,29)); by=BORN.year+age
    pyroot=r.root(1+29+r.digit_sum(d.year))
    out={'date':d.isoformat(),'completed_age':age,'last_birthday_year':by,'calendar_py_root':pyroot,'calendar_pm_root':r.root(pyroot+d.month),'calendar_pd_root':r.root(pyroot+d.month+d.day)}
    out['cheiro']={'year_root':r.root(d.year),'completed_age_root':r.root(age),'ordinal_life_year_root':r.root(age+1),'month_period':r.cheiro_period(d.month,d.day),'day_root':r.root(d.day),'birth_seed_periodicity':d.year in c[r.CHEIRO]['birth_year_periodicity'][1:]}
    dt=r.tape(ROLES,age,r.JORDAN);out['decoz']={'transit_letters':dt['active'],'essence':dec_result(dt['essence']['raw']),'duality_pair':[pyroot,dt['essence']['root']],'duality_interpretation':'RESOURCE_UNBOUND','age_digit':r.root(r.root(age)+r.root(age+1))}
    out['jordan']={'birth_start':r.tape(PARTS,age,r.JORDAN),'display_age_minus_one':r.tape(PARTS,age,r.JORDAN,'display_age_minus_one'),'race_consciousness':r.jordan_race_consciousness(age)}
    out['campbell']={'tape':r.tape(PARTS,age,r.CAMPBELL),'calendar_py_branches':{b:r.calendar_number(1,29,d.year,r.CAMPBELL,b) for b in ['retain','root']}}
    out['campbell']['essence_py_root_equality']=out['campbell']['tape']['essence']['root']==pyroot
    triangle=c[r.JB]['triangle'];line=triangle['lines'][min(age//9,8)]
    active_major=[x for x in line['major'] if x['age']==age];active_minor=[x for x in line['minor'] if x['age']==age]
    # Also retain entries at a boundary generated by the preceding line.
    boundary_entries=[dict(x,source_line=l['line']) for l in triangle['lines'] for x in l['major']+l['minor'] if x['age']==age]
    pnum=0 if d<date(by,5,29) else 1 if d<date(by,9,29) else 2
    year=r.jb_year(BORN,by)
    out['jb']={'year':year,'month':r.jb_month(year['admitted'],d.month),'four_month_phase':pnum+1,'period_branches':{label:r.jb_periods(BORN,by,triangle['life_lesson']['admitted'],b['vowels']['result']['admitted'])[pnum] for label,b in c[r.JB]['branches'].items()},'line':line['line'],'peak_letter':line['letter'],'square':triangle['squares'][min(age//27,2)],'active_major':active_major,'active_minor':active_minor,'all_entries_at_age':boundary_entries}
    out['pinnacle_boundary_sensitivity']={str(offset):min(sum(age>=b+offset for b in [28,37,46]),3)+1 for offset in [0,1]}
    return out


def date_range(lo,hi):
    d=date.fromisoformat(lo);end=date.fromisoformat(hi)
    while d<=end:
        yield d;d+=timedelta(days=1)


def summarize_interval(event,c):
    rows=[at(d,c) for d in date_range(event['lo'],event['hi'])]
    def unique(fn):
        seen={json.dumps(fn(v),sort_keys=True) for v in rows}
        return [json.loads(x) for x in sorted(seen)]
    return {**event,'states':{'age':unique(lambda x:x['completed_age']),'PY':unique(lambda x:x['calendar_py_root']),'PM':unique(lambda x:x['calendar_pm_root']),'Decoz_Essence':unique(lambda x:x['decoz']['essence']['raw']),'Jordan_Essence_birth_start':unique(lambda x:x['jordan']['birth_start']['essence']['raw']),'Jordan_Essence_display_minus_one':unique(lambda x:x['jordan']['display_age_minus_one'].get('essence',{}).get('raw')),'Campbell_Essence':unique(lambda x:x['campbell']['tape']['essence']['raw']),'JB_PY':unique(lambda x:x['jb']['year']['admitted']),'JB_period':unique(lambda x:{k:v['admitted'] for k,v in x['jb']['period_branches'].items()}),'JB_active_entries':unique(lambda x:[{'age':v['age'],'compound':v['number']['admitted'],'source_line':v['source_line']} for v in x['jb']['all_entries_at_age']]),'JB_square':unique(lambda x:x['jb']['square']['admitted']),'JB_month':unique(lambda x:x['jb']['month']['admitted'])},'range_evaluation':'all possible date states retained; no best-fitting date selected'}


def diagnostics(c):
    # Fixed small adapter family, recorded before the first result inspection.
    # These are not complete-author forecasts or event-specific death indicators.
    years=list(range(2000,2027)); positives={2002,2005,2010,2013,2014,2018,2020,2026}; lower={2008,2022}
    def flags(y):
        age=y-1985
        major={x['age'] for line in c[r.JB]['triangle']['lines'] for x in line['major']}
        minor={x['age'] for line in c[r.JB]['triangle']['lines'] for x in line['minor']}
        return {'CHEIRO_YEAR_HARMONY':r.root(y) in {1,2,4,7},
                'CHEIRO_BIRTH_SEED_RECURRENCE':y in c[r.CHEIRO]['birth_year_periodicity'][1:],
                'CAMPBELL_CHANGE_PY':r.root(1+29+r.digit_sum(y)) in {1,5,9},
                'LEGACY_WESTERN_CHANGE_SET':r.root(1+29+r.digit_sum(y)) in {1,5,7,9},
                'JB_MAJOR_AGE_MARK':age in major,
                'JB_ANY_AGE_MARK':age in major|minor}
    base={name:{y for y in years if flags(y)[name]} for name in flags(years[0])}
    models=dict(base)
    for a,b in itertools.combinations(base,2):
        for op in ['AND','OR']:
            models[f'{a}__{op}__{b}']=base[a]&base[b] if op=='AND' else base[a]|base[b]
    results=[]
    for name,marked in models.items():
        tp=sorted(positives&marked);fn=sorted(positives-marked);fp=sorted(lower&marked);tn=sorted(lower-marked)
        results.append({'adapter_id':name,'flagged_years':sorted(marked),'coverage_years':len(marked),'major_year_hits':tp,'major_year_misses':fn,'lower_impact_false_flags':fp,'lower_impact_correct_not_flags':tn,'observed_impact_errors':len(fn)+len(fp),'unknown_flagged_years':sorted(marked-positives-lower),'interpretation':'Retrospective selected impact contrast, not all-events discrimination. Unlabelled years never count as negatives.'})
    return {'scope':'COARSE_IMPACT_ADAPTERS_NOT_FULL_AUTHORS','calendar_years':years,'major_years':sorted(positives),'explicit_lower_impact_event_years':sorted(lower),'models_tested':len(results),'unlabelled_years_are_unknown':True,'results':results,'candidate_selection_is_retrospective':True,'thresholds_or_author_rules_fitted':False,'limitations':['2008/2022 are impact contrasts, not absence of any events','historical event selection incomplete','one person already revealed','calendar year collapses distinct events','birth-year age mapping is not exact occurrence timing','zero-cost unknown years prevent estimating predictive precision']}


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    c=core();rows=[summarize_interval(e,c) for e in EVENTS]
    result={'status':'DEVELOPMENT_CALCULATIONS_EXECUTED','core':c,'events':rows,'diagnostics':diagnostics(c),'future_outcomes_used':False}
    for name,value in [('calculated_comparison.json',result),('core_charts.json',c),('event_feature_comparison.json',rows),('coarse_adapter_combinations.json',result['diagnostics'])]:
        (OUT/name).write_text(json.dumps(value,indent=2)+'\n')
    yearrows=[at(date(y,7,1),c) for y in range(2000,2027)]
    (OUT/'full_background_feature_table.json').write_text(json.dumps(yearrows,indent=2)+'\n')
    print('CORE')
    for system in [r.CHEIRO,DECOZ,r.CAMPBELL,r.JORDAN,r.JB]:
        print(system,json.dumps(c[system],ensure_ascii=False))
    print('\nEVENT SUMMARY')
    for row in rows: print(row['id'],json.dumps(row['states'],ensure_ascii=False))
    print('\nDIAGNOSTIC ADAPTERS, sorted by selected-history errors then coverage (not a full-system ranking)')
    for row in sorted(result['diagnostics']['results'],key=lambda v:(v['observed_impact_errors'],v['coverage_years'],v['adapter_id']))[:15]:
        print(json.dumps(row))
    print('Saved',len(rows),'event intervals and',result['diagnostics']['models_tested'],'diagnostic adapters/combinations.')


if __name__=='__main__':
    main()
