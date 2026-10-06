"""Definition/record tests only; these do not validate human predictions."""
import importlib.util
import itertools
import json
from pathlib import Path
import pytest

B = Path(__file__).parent
spec = importlib.util.spec_from_file_location('b01l_reference', B/'b01l_reference.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
RULES = json.loads((B/'RULES.json').read_text())
TABLE = json.loads((B/'ASSOCIATION_TRAVEL_TABLES.json').read_text())
TECH = 'CROSS_NATIVITY_PROROGATION_III10_ROBBINS_NOTE'


@pytest.mark.parametrize('row', TABLE['pair_encounters'])
def test_all_ten_pairs_and_direction_labels(row):
    p, q = row['pair']
    for first, second in [(p,q),(q,p)]:
        result = m.pair_encounter_reference(first,second,technique=TECH,encounter_qualified=True)
        assert result['reference'] == row
        assert result['departure_body'] == first
        assert result['arrival_body'] == second
        assert result['status'] == 'SOURCE_REFERENCE_ONLY'


@pytest.mark.parametrize('q,status', [(None,'UNRESOLVED_QUALIFICATION'),(False,'NOT_TRIGGERED')])
def test_unqualified_pair_produces_no_row(q,status):
    r=m.pair_encounter_reference('Mars','Venus',technique=TECH,encounter_qualified=q)
    assert r['reference'] is None and r['status']==status


@pytest.mark.parametrize('bad', ['NATAL_CONJUNCTION','TRANSIT','SECONDARY_PROGRESSION',''])
def test_wrong_method_rejected(bad):
    with pytest.raises(ValueError):m.pair_encounter_reference('Saturn','Jupiter',technique=bad,encounter_qualified=True)


@pytest.mark.parametrize('pair', [('Sun','Moon'),('Saturn','Saturn'),('Uranus','Venus'),('Moon','Mercury')])
def test_absent_pair_not_invented(pair):
    with pytest.raises(ValueError):m.pair_encounter_reference(*pair,technique=TECH,encounter_qualified=True)


@pytest.mark.parametrize('bad', [1,0,'True',[],{}])
def test_truthy_qualifications_rejected(bad):
    with pytest.raises(TypeError):m.pair_encounter_reference('Saturn','Jupiter',technique=TECH,encounter_qualified=bad)


@pytest.mark.parametrize('row', TABLE['friendship_bases'])
def test_all_source_bases(row):
    assert m.relationship_basis_reference(row['key'],qualified=True)['reference']==row


def test_no_emotional_affection_inferred_from_need():
    r=m.relationship_basis_reference('fortune',qualified=True)['reference']
    assert r['bases']==['need']
    assert m.relationship_basis_reference('fortune',qualified=None)['reference'] is None


def test_mars_requires_hard_aspect_as_well_as_place():
    assert m.travel_branch_states(mars_setting=True,mars_hard_to_luminaries=False)['mars_source_branch'] is False
    assert m.travel_branch_states(mars_declining_from_mc=True,mars_hard_to_luminaries=True)['mars_source_branch'] is True
    assert m.travel_branch_states(mars_setting=True,mars_hard_to_luminaries=None)['mars_source_branch'] is None


def test_travel_three_valued_logic_exhaustively():
    vals=(False,None,True)
    def o(a,b):return True if a is True or b is True else False if a is False and b is False else None
    def a(x,y):return False if x is False or y is False else True if x is True and y is True else None
    for ms,md,xs,xd,h,f in itertools.product(vals,repeat=6):
        r=m.travel_branch_states(moon_setting=ms,moon_declining=md,mars_setting=xs,mars_declining_from_mc=xd,mars_hard_to_luminaries=h,fortune_in_travel_signs=f)
        assert r['moon_source_branch'] is o(ms,md)
        assert r['mars_source_branch'] is a(o(xs,xd),h)
        assert r['contextual_fortune_extension'] is a(o(o(ms,md),a(o(xs,xd),h)),f)
        assert r['prediction'] is None


def test_fortune_does_not_bypass_unknown_context():
    r=m.travel_branch_states(fortune_in_travel_signs=True)
    assert r['contextual_fortune_extension'] is None
    r=m.travel_branch_states(moon_setting=False,moon_declining=False,mars_setting=False,mars_declining_from_mc=False,mars_hard_to_luminaries=False,fortune_in_travel_signs=True)
    assert r['contextual_fortune_extension'] is False and r['prediction'] is None


@pytest.mark.parametrize('house',range(1,13))
def test_note_house_membership_not_ninth_only(house):
    r=m.robbins_travel_house_reference(house,house_frame_declared=True)
    assert r['membership'] is (house in (3,6,7,9,12))
    assert r['attribution']=='ROBBINS_IV8_NOTE' and r['natal_travel_prediction'] is None


def test_undeclared_frame_and_house_abstain():
    assert m.robbins_travel_house_reference(9,house_frame_declared=False)['membership'] is None
    assert m.robbins_travel_house_reference(None,house_frame_declared=True)['membership'] is None
    for bad in (0,13,True,3.5,'9'):
        with pytest.raises(ValueError):m.robbins_travel_house_reference(bad,house_frame_declared=True)


@pytest.mark.parametrize('a,b,expected',[(355,12,17),(12,355,17),(0,17,17),(0,16.9,16.9),(0,17.1,17.1),(0,180,180)])
def test_distance_probe_never_chooses_seventeen_degree_tolerance(a,b,expected):
    r=m.horoscopic_distance_probe(a,b)
    assert r['minimal_separation_degrees']==pytest.approx(expected)
    assert r['source_condition_satisfied'] is None and r['tolerance'] is None and r['prediction'] is None


def test_distance_invalid_inputs():
    for bad in (True,float('inf'),float('nan'),'17',None):
        with pytest.raises(ValueError):m.horoscopic_distance_probe(bad,10)


@pytest.mark.parametrize('row',TABLE['travel_hazards'])
def test_hazards_retain_parent(row):
    assert m.travel_hazard_reference(row['source_class'],adverse_parent_qualified=True)['reference']==row
    assert m.travel_hazard_reference(row['source_class'],adverse_parent_qualified=None)['reference'] is None
    assert m.travel_hazard_reference(row['source_class'],adverse_parent_qualified=False)['reference'] is None


def test_unallocated_desert_alternative_not_changed_to_terrestrial():
    desert=m.travel_hazard_reference('unallocated_alternative',adverse_parent_qualified=True)['reference']
    earth=m.travel_hazard_reference('terrestrial',adverse_parent_qualified=True)['reference']
    assert desert['historical_hazards']==['hard going','desert places']
    assert earth['historical_hazards']==['attacks of beasts','earthquakes']


def test_lookup_does_not_mutate_source():
    r=m.pair_encounter_reference('Jupiter','Mercury',technique=TECH,encounter_qualified=True)
    r['reference']['bases'].append('invented')
    assert 'invented' not in m.pair_encounter_reference('Jupiter','Mercury',technique=TECH,encounter_qualified=True)['reference']['bases']


def test_record_ids_and_coverage():
    rows=RULES['records'];assert len(rows)==71
    assert [int(r['id'].rsplit('R',1)[1]) for r in rows]==list(range(501,572))
    assert sum(r['source_locator']['chapter_or_verse']=='IV.7' for r in rows)==43
    assert sum(r['source_locator']['chapter_or_verse']=='IV.8' for r in rows)==28
    cov=json.loads((B/'SECTION_COVERAGE.json').read_text())
    assert {i for s in cov['sections'] for i in s['record_ids']}=={r['id'] for r in rows}
    for r in rows:
        assert r['unknown_is_not_false'] and r['admission']=='SOURCE_AUDIT_ONLY_NOT_ADMITTED_TO_FROZEN_PREDICTION_MODELS'
        assert r['source_locator']['source_file_sha256']=='10b44f40e47409215aa3d6c4ec2863ebc3982b81d33b4d4e5e2a065761ab7fec'


def test_complete_pair_universe_not_double_counted():
    rows=TABLE['pair_encounters'];actual={frozenset(r['pair']) for r in rows}
    assert actual=={frozenset(x) for x in itertools.combinations(['Saturn','Jupiter','Mars','Venus','Mercury'],2)}
    assert len(rows)==len(actual)==10


def test_table_links_and_tentative_notes():
    ids={r['id'] for r in RULES['records']}
    for key in ('pair_encounters','friendship_bases','travel_hazards'):
        assert all(r['record_id'] in ids for r in TABLE[key])
    r=next(r for r in RULES['records'] if r['title']=='Ingress target is translator inference')
    assert r['source_locator']['attribution_layer']=='ROBBINS_TENTATIVE_NOTE'
    assert TABLE['cause_cross_references']=={'action':'IV.4','property':'IV.2','body':'III.11','dignity':'IV.3'}
