import importlib.util
import sys
import json
from pathlib import Path
from collections import Counter
import pytest

B = Path(__file__).parent
spec = importlib.util.spec_from_file_location('b01j_reference', B / 'b01j_reference.py')
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)
R = m.RouteEvidence
TABLES = json.loads((B/'EXTERNAL_FORTUNE_TABLES.json').read_text())
RULES = json.loads((B/'RULES.json').read_text())['records']

def test_same_planet_is_one_not_two():
    r=m.select_action_references(R('QUALIFIED','Mercury'),R('QUALIFIED','Mercury'))
    assert r['selected']==['Mercury'] and r['mode']=='PRIMARY_SINGLE'

@pytest.mark.parametrize('a,b',[('Venus',None),(None,'Mars')])
def test_one_known_present_route(a,b):
    r=m.select_action_references(R('QUALIFIED',a) if a else R('ABSENT'),R('QUALIFIED',b) if b else R('ABSENT'))
    assert r['selected']==[a or b]

@pytest.mark.parametrize('counts,preferred',[(None,None),({'Venus':2,'Mercury':2},None),({'Venus':1,'Mercury':4},'Mercury'),({'Venus':3,'Mercury':1},'Venus'),({'Venus':3},None)])
def test_dual_routes_never_discard_second(counts,preferred):
    r=m.select_action_references(R('QUALIFIED','Venus'),R('QUALIFIED','Mercury'),claim_counts=counts)
    assert r['selected']==['Venus','Mercury'] and r['preferred']==preferred

@pytest.mark.parametrize('states',[('UNKNOWN','ABSENT'),('ABSENT','UNKNOWN'),('UNKNOWN','QUALIFIED'),('QUALIFIED','UNKNOWN')])
def test_unknown_never_triggers_fallback_or_single(states):
    a,b=[R(s,'Mercury' if s=='QUALIFIED' else None) for s in states]
    r=m.select_action_references(a,b,R('QUALIFIED','Venus'))
    assert r['status']=='UNRESOLVED_PRIMARY_ROUTE' and not r['selected']

def test_fallback_is_separately_labelled():
    r=m.select_action_references(R('ABSENT'),R('ABSENT'),R('QUALIFIED','Venus'))
    assert r['mode']=='FALLBACK_OCCASIONAL_ONLY'

@pytest.mark.parametrize('state,status',[('UNKNOWN','UNRESOLVED_FALLBACK'),('ABSENT','NO_FALLBACK_REFERENCE')])
def test_missing_fallback(state,status):
    assert m.select_action_references(R('ABSENT'),R('ABSENT'),R(state))['status']==status

@pytest.mark.parametrize('planet',['Saturn','Jupiter'])
def test_selector_does_not_invent_three_planet_conversion(planet):
    r=m.select_action_references(R('QUALIFIED',planet),R('ABSENT'))
    assert r['selected']==[planet] and not r['quality_profile_supported']

@pytest.mark.parametrize('state,planet',[('BAD',None),('ABSENT','Venus'),('UNKNOWN','Mars'),('QUALIFIED',None),('QUALIFIED','Sun')])
def test_invalid_route(state,planet):
    with pytest.raises(ValueError): R(state,planet)

@pytest.mark.parametrize('counts',[{'Mars':-1},{'Mars':True},{'Sun':2},{'Mars':1.2}])
def test_invalid_claim_counts(counts):
    with pytest.raises(ValueError):m.select_action_references(R('ABSENT'),R('ABSENT'),claim_counts=counts)

@pytest.mark.parametrize('row',TABLES['occupation_branches'],ids=lambda x:x['id'])
def test_all_19_source_rows_roundtrip_order_invariant(row):
    a=m.action_branch_reference(row['rulers'],row['branch'],topical_qualified=True)
    b=m.action_branch_reference(list(reversed(row['rulers'])),row['branch'],topical_qualified=True)
    assert a==b and a['records']==[row]
    assert not a['chart_qualification_performed'] and not a['empirical_validation']

@pytest.mark.parametrize('q,status',[(None,'UNRESOLVED_TOPICAL_QUALIFICATION'),(False,'NOT_APPLICABLE')])
def test_topical_qualification_not_assumed(q,status):
    r=m.action_branch_reference(['Venus'],'BASE',topical_qualified=q)
    assert r['status']==status and not r['records']

@pytest.mark.parametrize('rulers',[['Mars','Venus','Mercury'],['Saturn'],['Jupiter','Venus']])
def test_unspecified_profiles_abstain(rulers):
    assert m.action_branch_reference(rulers,'BASE',topical_qualified=True)['status']=='UNSPECIFIED_RULER_COMBINATION'

@pytest.mark.parametrize('rulers',[[],['Venus','Venus'],['Moon'],'Mercury'])
def test_malformed_lookup(rulers):
    with pytest.raises(ValueError):m.action_branch_reference(rulers,'BASE',topical_qualified=True)

def test_mars_has_no_unspecified_sun_branch():
    assert m.action_branch_reference(['Mars'],'BASE',topical_qualified=True)['status']=='UNSPECIFIED_BRANCH'

def test_complete_table_inventory():
    assert len(TABLES['occupation_branches'])==19
    assert len(TABLES['wealth_channels'])==5 and len(TABLES['bases_of_honour'])==4
    assert len(TABLES['action_sign_classes'])==4 and len(TABLES['moon_mercury_groups'])==4
    signs=[s for g in TABLES['moon_mercury_groups'] for s in g['signs']]
    assert len(set(signs))==10 and 'Gemini' not in signs and 'Aquarius' not in signs

def test_rule_continuity_attribution_and_references():
    ids=[r['id'] for r in RULES]
    assert len(ids)==len(set(ids))==74
    assert [int(s.rsplit('R',1)[1]) for s in ids]==list(range(334,408))
    assert Counter(r['source_locator']['chapter_or_verse'] for r in RULES)=={'IV.1':1,'IV.2':14,'IV.3':18,'IV.4':41}
    for r in RULES:
        loc=r['source_locator'];assert all(p-24==q for p,q in zip(loc['pdf_support_pages'],loc['printed_support_pages']))
        assert r['unknown_is_not_false'] and 'SOURCE_AUDIT_ONLY' in r['admission']
    for group in ('wealth_channels','bases_of_honour','occupation_branches','action_sign_classes','moon_mercury_groups'):
        assert all(row['rule_id'] in ids for row in TABLES[group])

def test_not_all_mars_rows_are_solar_conjunctions():
    solar=next(r for r in TABLES['occupation_branches'] if r['branch']=='SUN_ASPECT')
    no_solar=next(r for r in TABLES['occupation_branches'] if r['branch']=='WITHOUT_SUN')
    assert solar['extra_conditions']['Sun_aspect'] is True
    assert no_solar['extra_conditions']['Sun_aspect'] is False
    assert solar['historical_activity_examples']!=no_solar['historical_activity_examples']

def test_historical_mixed_examples_not_sanitized():
    rows=TABLES['occupation_branches']
    assert any('dealers in slaves' in r['historical_activity_examples'] for r in rows)
    assert any('surgeons' in r['historical_activity_examples'] and 'forgers' in r['historical_activity_examples'] for r in rows)

def test_reading_receipt_is_bound_to_rules():
    import hashlib
    receipt=json.loads((B/'READING_RECEIPT.json').read_text())
    assert receipt['rules_sha256']==hashlib.sha256((B/'RULES.json').read_bytes()).hexdigest()
    assert len(receipt['chapter_spans'])==4
    assert set(r for c in receipt['chapter_spans'] for r in c['record_ids'])==set(x['id'] for x in RULES)

def test_cross_source_dependency_not_validation():
    d=json.loads((B/'CROSS_SOURCE_COMPARISONS.json').read_text())
    assert d['count']==4 and not d['full_rhetorius_audit']
    assert all(not x['independent_empirical_corroboration'] for x in d['comparisons'])
    assert any(x['relation']=='EXPLICIT_REUSE_WITH_VARIANTS' for x in d['comparisons'])
