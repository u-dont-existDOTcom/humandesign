"""Bounded references for Robbins IV.7-IV.8; not an astrological predictor.

Astronomical/topical qualification is supplied by the caller. Unknown remains
unknown. False means this particular source branch is not triggered, never that
an event cannot happen. No chart, directions engine, risk score or country
selection is implemented here.
"""
from __future__ import annotations

import copy
import json
import math
from pathlib import Path
from typing import Any

Tri = bool | None
_TABLES = json.loads(Path(__file__).with_name('ASSOCIATION_TRAVEL_TABLES.json').read_text())
_PLANETS = frozenset({'Saturn', 'Jupiter', 'Mars', 'Venus', 'Mercury'})
_TECHNIQUE = 'CROSS_NATIVITY_PROROGATION_III10_ROBBINS_NOTE'


def _tri(value: Tri) -> Tri:
    if value is not None and type(value) is not bool:
        raise TypeError('Qualification must be True, False or None; not a truthy number/string.')
    return value


def _and(*values: Tri) -> Tri:
    values = tuple(_tri(v) for v in values)
    return False if False in values else (None if None in values else True)


def _or(*values: Tri) -> Tri:
    values = tuple(_tri(v) for v in values)
    return True if True in values else (None if None in values else False)


def _gate(qualification: Tri, payload: dict[str, Any]) -> dict[str, Any]:
    q = _tri(qualification)
    if q is None:
        return {'status': 'UNRESOLVED_QUALIFICATION', 'reference': None}
    if q is False:
        return {'status': 'NOT_TRIGGERED', 'reference': None,
                'boundary': 'No contrary real-world prediction follows.'}
    return {'status': 'SOURCE_REFERENCE_ONLY', 'reference': copy.deepcopy(payload)}


def pair_encounter_reference(first: str, second: str, *, technique: str,
                             encounter_qualified: Tri) -> dict[str, Any]:
    """Retrieve the source pair only for an explicitly supplied cross-chart method.

The unordered key selects shared wording; it does not erase departure/arrival
roles, authorize a same-chart conjunction, or determine which native benefits.
"""
    if not isinstance(first, str) or not isinstance(second, str):
        raise TypeError('Planet names must be strings.')
    if first not in _PLANETS or second not in _PLANETS or first == second:
        raise ValueError('Use two different planets from Saturn through Mercury; no luminary row exists.')
    if technique != _TECHNIQUE:
        raise ValueError('This table belongs to the explicit cross-nativity prorogation context.')
    row = next(r for r in _TABLES['pair_encounters'] if set(r['pair']) == {first, second})
    result = _gate(encounter_qualified, row)
    result['departure_body'] = first
    result['arrival_body'] = second
    result['technique'] = technique
    return result


def relationship_basis_reference(family: str, *, qualified: Tri) -> dict[str, Any]:
    """Family selection and full/partial familiarity must already be qualified."""
    rows = {r['key']: r for r in _TABLES['friendship_bases']}
    if not isinstance(family, str) or family not in rows:
        raise ValueError('Unsupported source family; no arbitrary majority/compatibility score.')
    return _gate(qualified, rows[family])


def travel_branch_states(*, moon_setting: Tri = None, moon_declining: Tri = None,
                         mars_setting: Tri = None, mars_declining_from_mc: Tri = None,
                         mars_hard_to_luminaries: Tri = None,
                         fortune_in_travel_signs: Tri = None) -> dict[str, Any]:
    """Reconcile caller-qualified clauses, retaining OR/AND and unknown states.

Only the two explicit Moon/Mars branches and their contextual Fortune extension
are modeled. The general Sun enquiry and dominance/mixture remain outside this
helper. A non-triggered branch is NOT a forecast of no travel.
"""
    moon = _or(moon_setting, moon_declining)
    mars = _and(_or(mars_setting, mars_declining_from_mc), mars_hard_to_luminaries)
    contextual = _or(moon, mars)
    fortune = _and(contextual, fortune_in_travel_signs)
    return {'moon_source_branch': moon, 'mars_source_branch': mars,
            'contextual_fortune_extension': fortune, 'prediction': None,
            'scope': 'CALLER_QUALIFIED_SOURCE_CLAUSES_NOT_ALL_TRAVEL_RULES',
            'mixed_judgment': 'UNRESOLVED_NOT_COMPUTED'}


def robbins_travel_house_reference(house: int | None, *, house_frame_declared: bool) -> dict[str, Any]:
    """Membership in Robbins's note, not a universal doctrine or house calculator."""
    if type(house_frame_declared) is not bool:
        raise TypeError('House-frame declaration must be a boolean.')
    if house is not None and (type(house) is not int or not 1 <= house <= 12):
        raise ValueError('House must be an integer 1..12 or None.')
    q = None if house is None or not house_frame_declared else house in _TABLES['rob_broad_travel_places']['houses']
    return {'attribution': 'ROBBINS_IV8_NOTE', 'membership': q,
            'source_houses': [3, 6, 7, 9, 12], 'natal_travel_prediction': None}


def horoscopic_distance_probe(a: float, b: float) -> dict[str, Any]:
    """Calculate ecliptic separation as a probe, without claiming to resolve17°.

Ecliptic longitudes are the caller's declared frame for this synthetic probe.
The passage's aggregation, 'about' tolerance and main/note distinction remain
open; even a computed distance of17 does not certify the whole source rule.
"""
    for x in (a, b):
        if type(x) not in (int, float) or not math.isfinite(x):
            raise ValueError('Use finite numeric longitudes, not booleans or strings.')
    delta = (float(b) - float(a)) % 360
    return {'minimal_separation_degrees': min(delta, 360 - delta),
            'frame': 'CALLER_DECLARED_ECLIPTIC_LONGITUDE_PROBE',
            'main_text': 'about17degrees apart', 'translator_note': 'within17degrees',
            'source_condition_satisfied': None, 'tolerance': None,
            'prediction': None}


def travel_hazard_reference(source_class: str, *, adverse_parent_qualified: Tri) -> dict[str, Any]:
    """Retain inherited Saturn/Mars context; no hazard estimate for real travel."""
    rows = {r['source_class']: r for r in _TABLES['travel_hazards']}
    if not isinstance(source_class, str) or source_class not in rows:
        raise ValueError('Use the source class, not an unverified modern sign-category substitute.')
    result = _gate(adverse_parent_qualified, rows[source_class])
    result['risk_estimate'] = None
    return result
