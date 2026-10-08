"""Bounded reference helpers for Lilly Book I VIII-XIV, not a chart interpreter.

Raw numbered degrees are deliberately not repaired from the later summary.
No source portrait is selected until its relevance and condition are supplied.
"""
from __future__ import annotations

from fractions import Fraction
import json
import math
from pathlib import Path
from typing import Any, Literal

HERE = Path(__file__).resolve().parent
SIGNS = ('Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra',
         'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces')
PLANETS = ('Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon')
Condition = Literal['WELL', 'ILL', 'MIXED', 'UNKNOWN']
LUNAR_MEAN = Fraction(13) + Fraction(10, 60) + Fraction(36, 3600)
LUNAR_SLOW_LIMIT = Fraction(13) + Fraction(10, 60)


def _data() -> dict[str, dict[str, Any]]:
    raw = json.loads((HERE / 'PLANETS.json').read_text(encoding='utf-8'))
    rows = raw['planets']
    if len(rows) != 7 or tuple(p['planet'] for p in rows) != PLANETS:
        raise ValueError('Seven distinct source planets in source order required')
    for p in rows:
        for field in ('raw_terms', 'raw_faces'):
            seen: set[str] = set()
            for row in p[field]:
                if row['sign'] not in SIGNS or row['sign'] in seen:
                    raise ValueError('Invalid or duplicate sign row')
                seen.add(row['sign'])
                ds = row['ordinal_degrees_inclusive']
                if not ds or len(set(ds)) != len(ds):
                    raise ValueError('Empty or duplicate degree list')
                if any(type(d) is not int or not 1 <= d <= 30 for d in ds):
                    raise ValueError('Source ordinals are integers 1..30')
    return {p['planet']: p for p in rows}


def planet_record(planet: str) -> dict[str, Any]:
    if planet not in PLANETS:
        raise ValueError('Not one of the seven source planets')
    return _data()[planet]


def numbered_degree_candidates(kind: Literal['term', 'face'], sign: str,
                               ordinal_degree: int) -> dict[str, Any]:
    """Return all raw owners, including gaps/conflicts, without angular conversion."""
    if kind not in ('term', 'face'):
        raise ValueError('Expected term or face')
    if sign not in SIGNS:
        raise ValueError('Unknown sign')
    if type(ordinal_degree) is not int or not 1 <= ordinal_degree <= 30:
        raise ValueError('Use an explicit printed ordinal, not zero-based longitude')
    field = 'raw_terms' if kind == 'term' else 'raw_faces'
    owners = [name for name, p in _data().items() for r in p[field]
              if r['sign'] == sign and ordinal_degree in r['ordinal_degrees_inclusive']]
    return {'status': 'SINGLE' if len(owners) == 1 else 'CONFLICT' if owners else 'GAP',
            'owners': owners, 'kind': kind, 'sign': sign,
            'ordinal_degree': ordinal_degree,
            'convention': 'printed_numbered_degrees_1_to_30', 'corrected': False}


def conditional_portrait(planet: str, *, relevant: bool | None,
                         condition: Condition) -> dict[str, Any]:
    p = planet_record(planet)
    if relevant is not None and type(relevant) is not bool:
        raise TypeError('Relevance must be true, false or unknown')
    if condition not in ('WELL', 'ILL', 'MIXED', 'UNKNOWN'):
        raise ValueError('Unrecognised condition')
    if relevant is False:
        return {'status': 'NOT_APPLICABLE', 'branches': {}}
    if relevant is None or condition == 'UNKNOWN':
        return {'status': 'UNRESOLVED', 'branches': {}}
    if condition == 'MIXED':
        return {'status': 'UNRESOLVED_MIXTURE', 'branches': dict(p['manners']),
                'selected_as_prediction': False}
    branch = 'well' if condition == 'WELL' else 'ill'
    return {'status': 'REFERENCE_BRANCH', 'branches': {branch: p['manners'][branch]},
            'astronomical_qualifications_computed': False, 'predictive_validity': 'UNTESTED'}


def _fraction(value: int | float | Fraction) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, float, Fraction)):
        raise TypeError('A finite numeric value is required')
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError('Nonfinite value')
        return Fraction(str(value))
    return Fraction(value)


def lunar_slow_analogy(daily_motion_degrees: int | float | Fraction | None) -> dict[str, Any]:
    if daily_motion_degrees is None:
        return {'status': 'UNRESOLVED', 'equivalent_to_retrograde': None}
    motion = _fraction(daily_motion_degrees)
    if motion < 0:
        raise ValueError('Negative input contradicts the source direct-only lunar model')
    return {'status': 'SOURCE_THRESHOLD_EVALUATED',
            'equivalent_to_retrograde': motion < LUNAR_SLOW_LIMIT,
            'input_motion_degrees_per_day': str(motion),
            'source_threshold': str(LUNAR_SLOW_LIMIT),
            'source_mean': str(LUNAR_MEAN),
            'physical_direction_overwritten': False}


def minor_dignity_excludes_peregrine(*, own_term: bool | None,
                                   own_face: bool | None) -> bool | None:
    """Three-valued OR. False means this clause does not settle peregrinity."""
    for v in (own_term, own_face):
        if v is not None and type(v) is not bool:
            raise TypeError('Truth values or unknown required')
    if own_term is True or own_face is True:
        return True
    if own_term is None or own_face is None:
        return None
    return False


def orb_reference(planet: str) -> dict[str, Any]:
    value = planet_record(planet)['orb']
    return {'planet': planet, 'before_degrees': value, 'after_degrees': value,
            'pair_aggregation': 'NOT_DETERMINED_HERE'}


def mercury_assimilation(other_planet: str, *, has_aspect: bool | None) -> dict[str, Any]:
    modifiers = {'Saturn': 'heavy', 'Jupiter': 'more temperate', 'Mars': 'more rash',
                 'Sun': 'more genteel', 'Venus': 'more jesting', 'Moon': 'more shifting'}
    if other_planet not in modifiers:
        raise ValueError('Expected one of the six other planets')
    if has_aspect is not None and type(has_aspect) is not bool:
        raise TypeError('Aspect must be true, false or unknown')
    if has_aspect is not True:
        return {'status': 'UNRESOLVED' if has_aspect is None else 'NOT_APPLICABLE',
                'modifier': None}
    return {'status': 'REFERENCE_MODIFIER', 'modifier': modifiers[other_planet],
            'gender_conjunction_clause_applied': False, 'mixture_rule': 'UNRESOLVED'}


def node_reference(node: Literal['Head', 'Tail'], companion: Literal['benefic', 'malefic'],
                   *, doctrine: Literal['reported_ancients', 'Lilly_preferred']) -> dict[str, Any]:
    if node not in ('Head', 'Tail') or companion not in ('benefic', 'malefic'):
        raise ValueError('Unknown source node/companion category')
    if doctrine not in ('reported_ancients', 'Lilly_preferred'):
        raise ValueError('An explicitly named doctrine is required')
    ancient = {('Head', 'benefic'): 'good', ('Head', 'malefic'): 'evil',
               ('Tail', 'benefic'): 'evil', ('Tail', 'malefic'): 'good'}
    preferred = {('Head', 'benefic'): 'increase_good', ('Head', 'malefic'): 'lessen_evil',
                 ('Tail', 'benefic'): 'obstacles_with_conditional_failure',
                 ('Tail', 'malefic'): 'intensify_evil'}
    return {'status': 'REFERENCE_ONLY', 'doctrine': doctrine,
            'result': (ancient if doctrine == 'reported_ancients' else preferred)[node, companion],
            'numeric_multiplier': None, 'personal_prediction': False,
            'tail_benefic_scope': 'Question with a qualifying significator; principal angles AND essential fortification qualify the failure branch' if node == 'Tail' and companion == 'benefic' and doctrine == 'Lilly_preferred' else None}


def source_year_numbers(planet: str) -> dict[str, str]:
    """Read four named categories; deliberately no function that predicts lifespan."""
    return dict(planet_record(planet)['year_numbers'])
