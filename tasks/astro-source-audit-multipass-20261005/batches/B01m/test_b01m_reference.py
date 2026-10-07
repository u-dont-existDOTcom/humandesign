"""Synthetic predicate/reference checks; no human outcomes or real charts."""
import importlib.util
import itertools
import json
from pathlib import Path

import pytest

B = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('b01m_reference', B/'b01m_reference.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
S = m.SOURCE_SCOPE
D = json.loads((B/'RULES.json').read_text())
T = json.loads((B/'QUALITY_OF_DEATH_TABLES.json').read_text())


def test_two_places_have_no_eighth_house_substitution():
    assert m.selected_place('ray_occourse', scope=S)['place'] == 'OCCOURSE_PLACE'
    assert m.selected_place('descent_to_occident', scope=S)['place'] == 'OCCIDENT'
    assert m.selected_place(None, scope=S)['status'] == 'UNRESOLVED_INPUT'
    with pytest.raises(ValueError):
        m.selected_place('eighth_house', scope=S)


@pytest.mark.parametrize('scope', ['PERSONAL_FORECAST', 'RHETORIUS_77', '', None])
def test_wrong_method_scope_is_rejected(scope):
    with pytest.raises(ValueError):
        m.selected_place('ray_occourse', scope=scope)


@pytest.mark.parametrize('occupants,approaching,status,selected', [
    (None, ('Mars',), 'UNRESOLVED_OCCUPANCY', []),
    (('Venus',), ('Mars',), 'CALLER_SUPPLIED_CARRIERS', ['Venus']),
    (('Venus', 'Jupiter'), None, 'CALLER_SUPPLIED_CARRIERS', ['Venus', 'Jupiter']),
    ((), None, 'UNRESOLVED_APPROACH', []),
    ((), (), 'NO_CARRIER_SUPPLIED', []),
    ((), ('Mars',), 'CALLER_SUPPLIED_CARRIERS', ['Mars']),
    ((), ('Mercury', 'Saturn'), 'CALLER_SUPPLIED_CARRIERS', ['Mercury', 'Saturn']),
])
def test_selection_uses_absence_not_unknown(occupants, approaching, status, selected):
    got = m.select_carriers(occupants, approaching, scope=S)
    assert got['status'] == status and got['selected'] == selected
    assert not got['personal_prediction']


@pytest.mark.parametrize('bad', [['Mars'], ('Mars', 'Mars'), ('Sun',), ('Uranus',), (1,)])
def test_invalid_carrier_collections(bad):
    with pytest.raises((ValueError, TypeError)):
        m.select_carriers(bad, None, scope=S)


@pytest.mark.parametrize('planet', ['Saturn', 'Jupiter', 'Mars', 'Venus', 'Mercury'])
def test_every_profile_requires_topic_qualification_and_preserves_words(planet):
    for unknown in [None, False]:
        assert m.cause_profile(planet, qualification=unknown, role='occupying', scope=S)['profile'] is None
    row = m.cause_profile(planet, qualification=True, role='occupying', scope=S)['profile']
    assert row['historical_conditions'] == T['five_planet_profiles'][planet]['historical_conditions']
    row['historical_conditions'].clear()
    assert m.cause_profile(planet, qualification=True, role='occupying', scope=S)['profile']['historical_conditions']


@pytest.mark.parametrize('role', ['eighth_house_ruler', 'natal_conjunction', 'generic_dominant', 'transiting'])
def test_bare_planet_roles_do_not_qualify(role):
    with pytest.raises(ValueError):
        m.cause_profile('Saturn', qualification=True, role=role, scope=S)


@pytest.mark.parametrize('planet', ['Sun', 'Moon', 'Neptune', ''])
def test_unlisted_cause_profiles_abstain(planet):
    with pytest.raises(ValueError):
        m.cause_profile(planet, qualification=True, role='occupying', scope=S)


@pytest.mark.parametrize('row', T['conditional_violent_examples'], ids=lambda r:r['id'])
def test_each_example_preserves_antecedents_without_claiming_trigger(row):
    got = m.example_reference(row['id'], scope=S)
    assert got['status'] == 'REFERENCE_ONLY_NOT_EVALUATED'
    assert got['example'] == row
    assert got['personal_prediction'] is False
    got['example']['outcome_alternatives'].clear()
    assert m.example_reference(row['id'], scope=S)['example']['outcome_alternatives']


def test_special_textual_qualifiers_are_not_normalized_away():
    rows={r['id']:r for r in T['conditional_violent_examples']}
    assert rows['SATURN_WATER']['conditions']['all'][0]['any'] == ['Virgo','Pisces','watery signs']
    assert rows['MARS_VENUS']['outcome_alternatives'][-1] == 'die as murderers of women'
    assert 'Jupiter himself afflicted' in rows['SATURN_JUPITER']['conditions']['all']
    assert 'Jupiter afflicted at same time' in rows['MARS_JUPITER']['conditions']['all']
    assert rows['SATURN_SETTING']['ambiguities'] and rows['MARS_BURNING']['ambiguities']


def expected_all(values):
    return False if any(x is False for x in values) else (None if any(x is None for x in values) else True)


def neg(v):
    return None if v is None else not v


def test_natural_condition_all_27_truth_combinations():
    for a,b,c in itertools.product([False,True,None],repeat=3):
        got=m.natural_clause(a,b,c,scope=S)
        assert got['source_condition'] is expected_all([a,b,neg(c)])
        assert got['opposite_outcome_inferred'] is False


def test_no_benefic_condition_all_81_truth_combinations():
    for a,b,c,d in itertools.product([False,True,None],repeat=4):
        got=m.postmortem_clause(a,b,c,d,scope=S)
        assert got['source_condition'] is expected_all([a,b,neg(c),neg(d)])
        assert got['personal_prediction'] is False


def test_lunar_emphasis_does_not_create_or_remove_base_foreign_clause():
    for values in itertools.product([False,True,None],repeat=5):
        a,b,c,d,e=values
        got=m.foreign_place_clause(*values,scope=S)
        base=expected_all([a,b])
        assert got['source_condition'] is base
        lunar=True if any(x is True for x in [c,d,e]) else (None if None in [c,d,e] else False)
        assert got['lunar_emphasis'] is expected_all([base,lunar])


@pytest.mark.parametrize('bad', [0, 1, 'true', [], {}])
def test_invalid_truth_values_rejected(bad):
    with pytest.raises(TypeError):
        m.natural_clause(bad,True,False,scope=S)


def test_empty_boolean_groups_rejected():
    for fn in [m.all_known,m.any_known]:
        with pytest.raises(ValueError):fn()


def test_complete_record_ids_locators_and_source_admission():
    assert D['records_count'] == 59
    assert [r['id'] for r in D['records']] == [f'PT.R64.IV.09.R{i}' for i in range(572,631)]
    for r in D['records']:
        loc=r['source_locator']
        assert loc['source_file_sha256'] == '10b44f40e47409215aa3d6c4ec2863ebc3982b81d33b4d4e5e2a065761ab7fec'
        assert all(p in [451,453,455,457,459,461] for p in loc['pdf_support_pages'])
        assert loc['printed_support_pages'] == [p-24 for p in loc['pdf_support_pages']]
        assert r['antecedents'] and r['consequent'] and r['dependency_groups']
        assert r['unknown_is_not_false'] is True
        assert r['admission'] == 'SOURCE_AUDIT_ONLY_NOT_ADMITTED_TO_FROZEN_PREDICTION_MODELS'
    ids={r['id'] for r in D['records']}
    assert {r['rule_id'] for r in T['conditional_violent_examples']} <= ids
    for row in T['five_planet_profiles'].values():
        assert {row['rule_id'],row['rationale_rule_id']} <= ids


def test_coverage_and_uncertainty_references_are_resolvable():
    ids={r['id'] for r in D['records']}
    cov=json.loads((B/'SECTION_COVERAGE.json').read_text())
    assert len(cov['sections']) == 1
    assert set(cov['sections'][0]['record_ids']) == ids
    for row in json.loads((B/'UNRESOLVED_INTERPRETATIONS.json').read_text())['issues']:
        assert set(row['record_ids']) <= ids
    for row in json.loads((B/'INTRASOURCE_QUALIFICATIONS.json').read_text())['qualifications']:
        assert set(row['source_records']) <= ids


def test_notes_not_promoted_to_direct_source():
    r={x['id'].rsplit('R',1)[1]:x for x in D['records']}
    assert r['594']['source_locator']['attribution_layer'] == 'ROBBINS_REPORTING_ANONYMOUS_COMMENTATOR'
    assert r['615']['consequent']['examples'] == ['Taurus','blind Cancer','Scorpio','Sagittarius']
    assert r['615']['source_locator']['attribution_layer'] == 'ROBBINS_NOTE'
    assert r['623']['ambiguities']


def test_cross_source_comparisons_carry_distinct_prerequisites():
    c=json.loads((B/'CROSS_SOURCE_COMPARISONS.json').read_text())
    assert len(c['comparisons']) == 3 and c['empirical_independent_tests'] == 0
    assert c['rhetorius_full_chapters_read'] == 0
    assert all(x['operational_consequence'] for x in c['comparisons'])
