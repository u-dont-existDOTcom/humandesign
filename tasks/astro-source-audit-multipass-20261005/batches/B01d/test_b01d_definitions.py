import importlib.util
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
import sys

import pytest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('pt_b01d_definitions', HERE/'b01d_definitions.py')
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)

def relations(**kw):
    return dict.fromkeys(m.FORM_KEYS, False) | kw

def test_phase_and_aspect_are_one_not_two_forms():
    assert m.count_distinct_forms(dict.fromkeys(m.FORM_KEYS, True)) == (5, 5)
    assert m.count_distinct_forms(relations(phase=True, aspect=True)) == (1, 1)

def test_unknown_is_preserved_in_or_and_counts():
    assert m.tri_or(None, False) is None
    assert m.tri_or(None, True) is True
    assert m.count_distinct_forms(relations(trine=None, phase=None)) == (0, 2)

def test_missing_or_extra_form_is_rejected():
    r=relations(); del r['term']
    with pytest.raises(ValueError): m.count_distinct_forms(r)
    with pytest.raises(ValueError): m.count_distinct_forms(relations(face=True))

def test_numeric_truthiness_is_not_evidence():
    with pytest.raises(ValueError): m.count_distinct_forms(relations(house=1))
    with pytest.raises(ValueError): m.major_topic_eligibility(0)

def test_equal_count_candidates_remain_tied():
    r=m.possible_maximal_claimants({'Mars':relations(house=True), 'Venus':relations(term=True)})
    assert r['status']=='COUNT_TIE' and r['candidates']==['Mars','Venus']

def test_unknown_can_change_apparent_winner():
    r=m.possible_maximal_claimants({'Mars':relations(house=True, trine=True),
                                  'Venus':relations(term=True, trine=None, aspect=None)})
    assert r['status']=='UNRESOLVED_COUNTS' and r['candidates']==['Mars','Venus']

def test_no_claim_is_not_a_forced_winner():
    assert m.possible_maximal_claimants({'Mars':relations()})['status']=='NO_SUPPORTED_FORM'
    with pytest.raises(ValueError): m.possible_maximal_claimants({})

def test_same_degree_not_planets_full_longitude():
    assert m.corresponding_degree(223.25, 1)==43.25
    assert m.corresponding_degree(359.5, 0)==29.5
    assert m.corresponding_degree(0, 11)==330

@pytest.mark.parametrize('value', [float('nan'),float('inf'),360,-1,True])
def test_invalid_longitude_is_rejected(value):
    with pytest.raises(ValueError):m.corresponding_degree(value,1)

def test_invalid_sign_is_rejected():
    for index in (-1,12,1.2,True):
        with pytest.raises(ValueError):m.corresponding_degree(20,index)

BIRTH=datetime(2000,2,1,12,tzinfo=timezone.utc)

def test_latest_new_or_full_before_birth_not_later():
    events=[m.Syzygy('old',BIRTH-timedelta(days=18),'NEW_MOON'),
            m.Syzygy('next',BIRTH+timedelta(days=2),'NEW_MOON'),
            m.Syzygy('recent',BIRTH-timedelta(days=3),'FULL_MOON')]
    assert m.latest_preceding_syzygy(events,BIRTH)['selected']==['recent']

def test_coincident_syzygy_is_not_silently_preceding():
    events=[m.Syzygy('prior',BIRTH-timedelta(days=14),'FULL_MOON'),m.Syzygy('same',BIRTH,'NEW_MOON')]
    out=m.latest_preceding_syzygy(events,BIRTH)
    assert out['status']=='UNRESOLVED_AT_BIRTH' and not out['selected']

def test_absent_and_conflicting_events_are_not_certified():
    assert m.latest_preceding_syzygy([],BIRTH)['status']=='NO_PRECEDING_EVENT_SUPPLIED'
    t=BIRTH-timedelta(days=1)
    out=m.latest_preceding_syzygy([m.Syzygy('a',t,'NEW_MOON'),m.Syzygy('b',t,'FULL_MOON')],BIRTH)
    assert out['status']=='CONFLICTING_PRECEDING_EVENTS'

def test_invalid_event_time_kind_and_duplicates_rejected():
    with pytest.raises(ValueError):m.latest_preceding_syzygy([],BIRTH.replace(tzinfo=None))
    with pytest.raises(ValueError):m.latest_preceding_syzygy([m.Syzygy('x',BIRTH,'QUARTER')],BIRTH)
    e=m.Syzygy('same',BIRTH,'NEW_MOON')
    with pytest.raises(ValueError):m.latest_preceding_syzygy([e,e],BIRTH)

def test_timezone_equivalent_instants_are_compared_correctly():
    local=BIRTH.astimezone(timezone(timedelta(hours=3)))
    assert m.latest_preceding_syzygy([m.Syzygy('at',local,'FULL_MOON')],BIRTH)['status']=='UNRESOLVED_AT_BIRTH'

def test_parent_day_night_and_unknown_keep_both_natural_significators():
    assert m.parent_significators('father','DAY')['sect_focus']=='SUN'
    assert m.parent_significators('father','NIGHT')['sect_focus']=='SATURN'
    assert m.parent_significators('mother','DAY')['sect_focus']=='VENUS'
    assert m.parent_significators('mother','NIGHT')['sect_focus']=='MOON'
    assert m.parent_significators('father',None)['natural_pair']==['SUN','SATURN']
    assert m.parent_significators('father',None)['sect_focus'] is None

def test_topical_eligibility_is_neither_prediction_nor_zero_effect():
    assert m.major_topic_eligibility(False)=='NOT_ADMITTED_AS_MAJOR_TOPIC_CAUSE'
    assert m.major_topic_eligibility(None)=='UNRESOLVED_ORIGINAL_FAMILIARITY'
    assert m.major_topic_eligibility(True)=='ELIGIBLE_FOR_FURTHER_TOPIC_ANALYSIS'

def test_source_records_are_unique_edition_bound_and_sequential():
    a=json.loads((HERE/'RULES.json').read_text())
    b=json.loads((HERE.parent/'B01e/RULES.json').read_text())
    rr=a['records']+b['records']; ids=[r['id'] for r in rr]
    assert len(rr)==55 and len(set(ids))==55
    assert [int(i.split('.R')[-1]) for i in ids]==list(range(110,165))
    assert all(r['source_locator']['source_file_sha256']=='10b44f40e47409215aa3d6c4ec2863ebc3982b81d33b4d4e5e2a065761ab7fec' for r in rr)
    assert a['independent_predictions_count']==b['independent_predictions_count']==0
    assert all(r['source_locator']['passage_anchor'] for r in rr)

def test_adverse_sources_do_not_erase_qualifiers_or_admit_runtime():
    d=json.loads((HERE.parent/'B01e/RULES.json').read_text())
    paternal=next(r for r in d['records'] if 'Favorable paternal' in r['title'])
    assert 'does NOT thereby indicate short life' in paternal['consequent']
    assert paternal['antecedents']['any'][0]['relation']=='aspect whatever to Sun AND Saturn'
    discord=next(r for r in d['records'] if 'Sibling reference' in r['title'])
    assert discord['output_type']=='UNRESOLVED_REFERENCE_FRAME'
    assert all('NOT_ADMITTED' in r['admission'] for r in d['records'])
