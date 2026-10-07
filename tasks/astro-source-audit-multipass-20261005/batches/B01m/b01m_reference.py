"""Ptolemy IV.9 source-reference helpers, not a death or medical forecast engine.

Inputs are already interpreted source predicates. No function calculates a natal
chart, establishes the III.10 event, or supplies missing orbs/strength thresholds.
False means a clause is not established, not that its opposite is predicted.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any, Literal

Truth = bool | None
Mechanism = Literal['ray_occourse', 'descent_to_occident']
SOURCE_SCOPE = 'PTOLEMY_IV9_SOURCE_REFERENCE_ONLY'
PLANETS = frozenset({'Saturn', 'Jupiter', 'Mars', 'Venus', 'Mercury'})
_TABLES = json.loads((Path(__file__).with_name('QUALITY_OF_DEATH_TABLES.json')).read_text())


def _scope(scope: str) -> None:
    if scope != SOURCE_SCOPE:
        raise ValueError('This helper is only for the declared Ptolemy IV.9 source-reference scope.')


def _truth(value: Truth) -> Truth:
    if value is not None and type(value) is not bool:
        raise TypeError('Use True, False, or None; None means unknown, not false.')
    return value


def all_known(*values: Truth) -> Truth:
    """Three-valued conjunction; rejects empty or non-Boolean truth assertions."""
    if not values:
        raise ValueError('A clause must have at least one predicate.')
    values = tuple(_truth(x) for x in values)
    if False in values:
        return False
    return None if None in values else True


def any_known(*values: Truth) -> Truth:
    """Three-valued disjunction without converting unknown into absence."""
    if not values:
        raise ValueError('A clause must have at least one predicate.')
    values = tuple(_truth(x) for x in values)
    if True in values:
        return True
    return None if None in values else False


def _not(value: Truth) -> Truth:
    value = _truth(value)
    return None if value is None else not value


def _clause(value: Truth, ref: str) -> dict[str, Any]:
    value = _truth(value)
    return {'source_condition': value,
            'status': {True: 'CALLER_SUPPLIED_CONDITION_MET', False: 'CLAUSE_NOT_ESTABLISHED',
                       None: 'UNRESOLVED_INPUT'}[value],
            'source_ref': ref, 'personal_prediction': False,
            'opposite_outcome_inferred': False}


def selected_place(mechanism: Mechanism | None, *, scope: str) -> dict[str, Any]:
    """Route only an already established III.10 mechanism to its IV.9 locus."""
    _scope(scope)
    if mechanism is None:
        return {'status': 'UNRESOLVED_INPUT', 'place': None, 'personal_prediction': False}
    if mechanism not in _TABLES['topic_selection']:
        raise ValueError('Declare ray_occourse or descent_to_occident; no eighth-house shortcut.')
    return {'status': 'CALLER_SUPPLIED_MECHANISM', 'place': _TABLES['topic_selection'][mechanism],
            'personal_prediction': False}


def _planet_group(value: tuple[str, ...] | None) -> tuple[str, ...] | None:
    if value is None:
        return None
    if not isinstance(value, tuple):
        raise TypeError('Use tuple of source planets; None is unknown, () is known empty.')
    if any(not isinstance(p, str) or p not in PLANETS for p in value):
        raise ValueError('Only the five planets with IV.9 cause profiles are accepted.')
    if len(value) != len(set(value)):
        raise ValueError('Duplicate carrier records are not separate testimonies.')
    return value


def select_carriers(occupants: tuple[str, ...] | None,
                    first_approaching: tuple[str, ...] | None,
                    *, scope: str) -> dict[str, Any]:
    """Priority without computing occupancy, approach order, or an absent chart."""
    _scope(scope)
    occupants = _planet_group(occupants)
    first_approaching = _planet_group(first_approaching)
    if occupants is None:
        return {'status': 'UNRESOLVED_OCCUPANCY', 'selected': [], 'role': None,
                'personal_prediction': False}
    if occupants:
        return {'status': 'CALLER_SUPPLIED_CARRIERS', 'selected': list(occupants),
                'role': 'occupying', 'personal_prediction': False}
    if first_approaching is None:
        return {'status': 'UNRESOLVED_APPROACH', 'selected': [], 'role': None,
                'personal_prediction': False}
    if not first_approaching:
        return {'status': 'NO_CARRIER_SUPPLIED', 'selected': [], 'role': None,
                'personal_prediction': False, 'opposite_outcome_inferred': False}
    return {'status': 'CALLER_SUPPLIED_CARRIERS', 'selected': list(first_approaching),
            'role': 'first_approaching', 'personal_prediction': False}


def cause_profile(planet: str, *, qualification: Truth, role: str,
                  scope: str) -> dict[str, Any]:
    """Retrieve historical vocabulary only after a caller declares topical selection."""
    _scope(scope)
    _truth(qualification)
    if planet not in PLANETS:
        raise ValueError('No IV.9 cause spectrum in this table for that planet.')
    if role not in {'occupying', 'first_approaching'}:
        raise ValueError('A natal aspect, generic dominant planet, or eighth-house ruler is not this role.')
    if qualification is not True:
        return {'status': 'UNRESOLVED_INPUT' if qualification is None else 'CLAUSE_NOT_ESTABLISHED',
                'profile': None, 'personal_prediction': False, 'opposite_outcome_inferred': False}
    return {'status': 'CALLER_QUALIFIED_SOURCE_REFERENCE',
            'profile': deepcopy(_TABLES['five_planet_profiles'][planet]),
            'personal_prediction': False, 'medical_equivalence_established': False}


def example_reference(key: str, *, scope: str) -> dict[str, Any]:
    """Read an example with its full conditions; no trigger evaluation is asserted."""
    _scope(scope)
    row = next((r for r in _TABLES['conditional_violent_examples'] if r['id'] == key), None)
    if row is None:
        raise KeyError(key)
    return {'status': 'REFERENCE_ONLY_NOT_EVALUATED', 'example': deepcopy(row),
            'personal_prediction': False}


def natural_clause(prior_procedure: Truth, own_or_kindred: Truth,
                   injuring_overcome: Truth, *, scope: str) -> dict[str, Any]:
    _scope(scope)
    return _clause(all_known(prior_procedure, own_or_kindred, _not(injuring_overcome)),
                   'PT.R64.IV.09.R592')


def postmortem_clause(inherited_context: Truth, animal_or_bird_form: Truth,
                      benefic_to_ic: Truth, benefic_to_destructive: Truth,
                      *, scope: str) -> dict[str, Any]:
    _scope(scope)
    return _clause(all_known(inherited_context, animal_or_bird_form,
                            _not(benefic_to_ic), _not(benefic_to_destructive)),
                   'PT.R64.IV.09.R626')


def foreign_place_clause(selected_destructive_occupants: Truth, cadent: Truth,
                         moon_present: Truth, moon_square: Truth, moon_opposite: Truth,
                         *, scope: str) -> dict[str, Any]:
    _scope(scope)
    base = all_known(selected_destructive_occupants, cadent)
    emphasis = all_known(base, any_known(moon_present, moon_square, moon_opposite))
    out = _clause(base, 'PT.R64.IV.09.R628')
    out['lunar_emphasis'] = emphasis
    return out
