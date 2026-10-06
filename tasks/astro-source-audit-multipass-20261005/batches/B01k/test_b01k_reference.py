import importlib.util
import json
from pathlib import Path
import pytest

ROOT = Path(__file__).parent
spec = importlib.util.spec_from_file_location('b01k_reference', ROOT/'b01k_reference.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
RULES = json.loads((ROOT/'RULES.json').read_text())

@pytest.mark.parametrize('angle, expected', [(45,'EASTERN'), (135,'WESTERN'),
    (225,'EASTERN'), (315,'WESTERN'), (-45,'WESTERN'), (405,'EASTERN')])
def test_phase_reference_not_house(angle,expected):
    result=m.lunar_phase_quadrant(angle)
    assert result['quadrant']==expected
    assert result['frame']=='LUNAR_PHASE_NOT_NATAL_HOUSE'

@pytest.mark.parametrize('angle', [0,90,180,270,360])
def test_exact_boundaries_abstain(angle):
    assert m.lunar_phase_quadrant(angle)['quadrant']=='UNRESOLVED_EXACT_PHASE_BOUNDARY'

@pytest.mark.parametrize('angle', [float('nan'),float('inf'),float('-inf'),True,'45'])
def test_invalid_phase(angle):
    with pytest.raises((ValueError,TypeError)):m.lunar_phase_quadrant(angle)

def test_moon_frame_cannot_be_reused_for_sun():
    with pytest.raises(ValueError):m.lunar_phase_quadrant(45,body='Sun')

@pytest.mark.parametrize('branch,planet',[(b,p) for b in ['male_native','female_native']
    for p in ['Saturn','Jupiter','Mars','Venus','Mercury']])
def test_every_source_spouse_row_and_subject(branch,planet):
    result=m.spouse_reference(branch,planet,qualified=True)
    row=result['rows'][0]
    assert row['subject']==('wife' if branch=='male_native' else 'husband')
    assert row['referent']==('Moon' if branch=='male_native' else 'Sun')
    assert row['rule_ref'] in {r['id'] for r in RULES['records']}

def test_spouse_unknown_is_not_absence_and_no_unlisted_profile():
    assert m.spouse_reference('male_native','Saturn',qualified=None)['status']=='UNRESOLVED_QUALIFICATION'
    assert m.spouse_reference('male_native','Saturn',qualified=False)['status']=='NOT_APPLICABLE'
    assert m.spouse_reference('male_native','Sun',qualified=True)['status']=='NO_LISTED_SOURCE_PROFILE'

@pytest.mark.parametrize('geometry,benefic,malefic', [('HARMONIOUS',True,False),
    ('HARMONIOUS',False,True),('INHARMONIOUS',True,False),('INHARMONIOUS',False,True)])
def test_all_four_relationship_cells(geometry,benefic,malefic):
    r=m.relationship_reference(geometry,benefic=benefic,malefic=malefic,cross_chart_qualified=True)
    assert r['status']=='CALLER_QUALIFIED_SOURCE_REFERENCE'
    assert len(r['rows'])==1 and r['probability'] is None

def test_endurance_not_equated_with_quality():
    r=m.relationship_reference('HARMONIOUS',benefic=False,malefic=True,cross_chart_qualified=True)['rows'][0]
    assert 'divorce' in r['continuity'] and 'not' in r['continuity']
    assert 'quarrelsome' in r['quality']
    r=m.relationship_reference('INHARMONIOUS',benefic=True,malefic=False,cross_chart_qualified=True)['rows'][0]
    assert 'renewals' in r['continuity'] and 'affection' in r['quality']

def test_mixed_and_unknown_relationship_testimony_not_forced():
    mixed=m.relationship_reference('HARMONIOUS',benefic=True,malefic=True,cross_chart_qualified=True)
    assert mixed['status']=='UNRESOLVED_MIXED_TESTIMONY' and len(mixed['rows'])==2
    partial=m.relationship_reference('HARMONIOUS',benefic=True,malefic=None,cross_chart_qualified=True)
    assert partial['status']=='PARTIAL_KNOWN_SUPPORT_OTHER_TESTIMONY_UNKNOWN'
    assert m.relationship_reference('HARMONIOUS',benefic=False,malefic=False,cross_chart_qualified=True)['status']=='BASELINE_ONLY_NO_TESTIMONY_MODIFIER'

def test_cross_chart_qualification_required():
    assert m.relationship_reference('HARMONIOUS',benefic=True,malefic=False,cross_chart_qualified=False)['rows']==[]
    assert m.relationship_reference('HARMONIOUS',benefic=True,malefic=False,cross_chart_qualified=None)['status']=='UNRESOLVED_QUALIFICATION'

@pytest.mark.parametrize('primary,opposite,status',[(None,['Venus'],'UNRESOLVED_PRIMARY'),
    ([],None,'UNRESOLVED_FALLBACK'),([],['Venus'],'OPPOSITE_FALLBACK'),
    (['Moon'],['Venus'],'PRIMARY'),([],[],'NO_QUALIFYING_SOURCE_PLANET')])
def test_children_reference_routes(primary,opposite,status):
    assert m.children_reference_route(primary,opposite)['status']==status

def test_primary_preference_deduplicates_not_extra_votes():
    assert m.children_reference_route(['Moon','Moon','Jupiter'],['Venus'])['planets']==['Jupiter','Moon']

@pytest.mark.parametrize('planet,group', [('Moon','giving'),('Venus','giving'),('Jupiter','giving'),
    ('Sun','limiting'),('Saturn','limiting'),('Mars','limiting'),('Mercury','common')])
def test_children_groups_are_not_sects(planet,group):
    r=m.children_group(planet)
    assert r['group']==group and 'NOT_DIURNAL_NOCTURNAL' in r['scope']

def test_plurality_keeps_conjunction_and_fecund_alternative():
    kwargs=dict(donor_qualified=True,alone=False,bicorporeal=True,feminine=False,fecund=False)
    assert m.multiplicity_reference_flags(**kwargs)['multiple_clause_supported'] is False
    kwargs['feminine']=True
    assert m.multiplicity_reference_flags(**kwargs)['multiple_clause_supported'] is True
    kwargs.update(bicorporeal=False,feminine=False,fecund=True)
    assert m.multiplicity_reference_flags(**kwargs)['multiple_clause_supported'] is True

def test_multiplicity_unknown_and_conflicts_have_no_exact_count():
    r=m.multiplicity_reference_flags(donor_qualified=True,alone=True,bicorporeal=True,feminine=True,fecund=False)
    assert r['status']=='UNRESOLVED_CO_TRIGGERED_SOURCE_CLAUSES' and r['exact_child_count'] is None
    r=m.multiplicity_reference_flags(donor_qualified=True,alone=None,bicorporeal=True,feminine=None,fecund=False)
    assert r['multiple_clause_supported'] is None
    r=m.multiplicity_reference_flags(donor_qualified=False,alone=None,bicorporeal=None,feminine=None,fecund=None)
    assert r['multiple_clause_supported'] is False

@pytest.mark.parametrize('case', ['planet','branch','truth','collection','geometry'])
def test_bad_inputs_not_silently_repaired(case):
    with pytest.raises((ValueError,TypeError)):
        if case=='planet':m.children_group('Pluto')
        elif case=='branch':m.spouse_reference('modern_generic','Saturn',qualified=True)
        elif case=='truth':m.multiplicity_reference_flags(donor_qualified=1,alone=True,bicorporeal=False,feminine=False,fecund=False)
        elif case=='collection':m.children_reference_route('Moon',[])
        else:m.relationship_reference('GOOD',benefic=True,malefic=False,cross_chart_qualified=True)

def test_all_records_have_complete_source_provenance():
    rows=RULES['records'];assert len(rows)==RULES['records_count']==93
    assert [int(r['id'].split('.R')[-1]) for r in rows]==list(range(408,501))
    assert sum(r['source_locator']['chapter_or_verse']=='IV.5' for r in rows)==73
    assert sum(r['source_locator']['chapter_or_verse']=='IV.6' for r in rows)==20
    for r in rows:
        loc=r['source_locator']
        assert loc['source_file_sha256']=='10b44f40e47409215aa3d6c4ec2863ebc3982b81d33b4d4e5e2a065761ab7fec'
        assert loc['pdf_support_pages'] and all(417<=p<=437 for p in loc['pdf_support_pages'])
        assert loc['printed_support_pages']==[p-24 for p in loc['pdf_support_pages']]
        assert r['unknown_is_not_false'] and r['admission'].startswith('SOURCE_AUDIT_ONLY')

def test_tables_and_material_ambiguities_are_retained():
    assert len(m.DATA['relationship_continuity_quality'])==4
    assert m.DATA['children']['sterile_list_exhaustive'] is False
    titles={r['title']:r for r in RULES['records']}
    assert titles['Saturn versus Jupiter textual variant']['source_locator']['attribution_layer']=='ROBBINS_TEXTUAL_NOTE'
    assert titles['Passion with restraint in the Venus-Jupiter testimony clause']['ambiguities']
    assert titles['Venus-Saturn unions can be pleasant and firm']['consequent']==['pleasant unions','firm unions']
    assert RULES['independent_predictions_count']==0

def test_coverage_and_reading_hash_cover_exact_two_chapters():
    import hashlib
    coverage=json.loads((ROOT/'SECTION_COVERAGE.json').read_text())
    receipt=json.loads((ROOT/'READING_RECEIPT.json').read_text())
    assert {s['chapter'] for s in coverage['sections']}=={'IV.5','IV.6'}
    assert {i for s in coverage['sections'] for i in s['record_ids']}=={r['id'] for r in RULES['records']}
    assert receipt['rules_sha256']==hashlib.sha256((ROOT/'RULES.json').read_bytes()).hexdigest()
    assert receipt['english_pdf_pages']==list(range(417,438,2))
    assert receipt['new_ocr_calls']==0

def test_comparisons_do_not_misstate_target_or_validation():
    d=json.loads((ROOT/'CROSS_SOURCE_COMPARISONS.json').read_text())
    assert d['new_comparisons']==len(d['comparisons'])==3
    assert d['cumulative_comparisons']==11
    assert not d['empirical_corroboration_claimed']
    assert 'CONTINUING_ATTEMPT' in d['comparisons'][0]['classification']
    assert 'NOT_A_DIRECT' in d['comparisons'][1]['classification']
    assert 'NOT_PROOF' in d['comparisons'][2]['classification']
