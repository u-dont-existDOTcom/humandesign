"""Source-bound references for Lilly 1647 II.XXIV-XXVI.

These functions retrieve historical definitions or reproduce static arithmetic.
They do not locate living people, assess health/vessel safety, or forecast events.
Coordinates are integer arcminutes, not degrees or ephemeris contact times.
"""
from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from functools import lru_cache
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SIGNS = ('Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces')
PLANETS = ('Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon')
CIRCLE = 21600
NEWS_PROFILE = 'Lilly_XXIV_p152_Moon_to_AscendantLord'
FORTUNE_PROFILE = 'Lilly_XXIII_p143_144_same_by_day_and_night'


@lru_cache(maxsize=None)
def _load(name: str) -> dict:
    if name not in {'QUERY_FRAMES', 'SHIP_PARTS', 'HISTORICAL_CASES',
                    'TIMING_REFERENCES', 'BODY_MARK_REFERENCE'}:
        raise ValueError('No declared source dataset')
    return json.loads((ROOT / (name + '.json')).read_text())


def _position(x: int) -> int:
    if type(x) is not int or not 0 <= x < CIRCLE:
        raise ValueError('Expected integer arcminutes in [0, 21600)')
    return x


def longitude(sign: str, degree: int, minute: int) -> int:
    if sign not in SIGNS:
        raise ValueError('Unknown source sign')
    if type(degree) is not int or not 0 <= degree < 30:
        raise ValueError('Expected within-sign degrees 0..29')
    if type(minute) is not int or not 0 <= minute < 60:
        raise ValueError('An actual minute is required; missing is not zero')
    return SIGNS.index(sign) * 1800 + degree * 60 + minute


def as_sign(x: int) -> tuple[str, int, int]:
    x = _position(x)
    sign, rest = divmod(x, 1800)
    degree, minute = divmod(rest, 60)
    return SIGNS[sign], degree, minute


def separation(a: int, b: int) -> int:
    d = abs(_position(a) - _position(b))
    return min(d, CIRCLE - d)


def aspect_residual(a: int, b: int, aspect_degrees: int) -> int:
    if type(aspect_degrees) is not int or aspect_degrees not in (0, 60, 90, 120, 180):
        raise ValueError('Only declared traditional aspect angles admitted')
    return abs(separation(a, b) - aspect_degrees * 60)


def antiscion(x: int) -> int:
    """Continuous-coordinate reflection, a declared arithmetic implementation."""
    return (10800 - _position(x)) % CIRCLE


def fortune(ascendant: int, moon: int, sun: int, *, profile: str) -> int:
    if profile != FORTUNE_PROFILE:
        raise ValueError('Use the explicitly identified earlier Lilly convention')
    return (_position(ascendant) + _position(moon) - _position(sun)) % CIRCLE


def person_house_reference(query: str, relationship: str) -> dict:
    """Choose a source role, not the state/whereabouts of any actual person."""
    q = _load('QUERY_FRAMES')
    if query == 'at_home':
        if relationship not in q['at_home_roles']:
            raise ValueError('Relationship not among these explicit examples')
        h = q['at_home_roles'][relationship]
        loc = 'II.XXIV printed147; sibling/neighbour II.XXV printed154'
    elif query == 'general_absent':
        if relationship != 'unrelated':
            raise ValueError('The local absent-person exception requires no relation')
        h = q['general_absent_unrelated_origin']
        loc = 'II.XXIV printed151'
    else:
        raise ValueError('Query context must be explicit')
    return {'query': query, 'relationship': relationship, 'radical_house': h,
            'source_locator': loc, 'status': 'historical_role_lookup_only'}


def presence_category_reference(category: str) -> dict:
    rows = _load('QUERY_FRAMES')['presence_rows']
    if category not in rows:
        raise ValueError('Expected angular, succedent, or cadent')
    return {'source_locator': 'II.XXIV printed147', 'status': 'historical_claim_only',
            **deepcopy(rows[category])}


def turned_house(origin: int, relative: int) -> int:
    if not all(type(n) is int and 1 <= n <= 12 for n in (origin, relative)):
        raise ValueError('Houses must be integer 1..12')
    return (origin + relative - 2) % 12 + 1


def beyond_cusp_window(forward_gap: int) -> bool | None:
    """Only the negative example: more than 5 degrees is excluded.

    At/below five degrees this particular counterexample does not decide admission.
    """
    if type(forward_gap) is not int or not 0 <= forward_gap < CIRCLE:
        raise ValueError('Expected nonnegative forward gap in integer arcminutes')
    return True if forward_gap > 300 else None


def news_symbolic_interval(gap: int, modality: str, *, profile: str) -> dict:
    """Exact symbolic quantity only; prerequisites and calendar remain uncomputed."""
    if profile != NEWS_PROFILE:
        raise ValueError('Explicit printed152 lunar-news profile required')
    if type(gap) is not int or not 0 <= gap < CIRCLE:
        raise ValueError('Expected nonnegative arcminute gap')
    units = _load('TIMING_REFERENCES')['news_symbolic_units']
    if modality not in units:
        raise ValueError('No rule for an unknown or mixed modality')
    quantity = Fraction(gap, 60)
    return {'quantity': str(quantity), 'unit': units[modality], 'profile': profile,
            'requirements': 'Moon applies sextile/trine to Ascendant lord after survival inquiry',
            'astronomical_encounter_computed': False, 'civil_date_computed': False,
            'is_forecast': False}


def hypothetical_news_options() -> dict:
    return deepcopy(_load('TIMING_REFERENCES')['hypothetical_ten_degree_options'])


def square_equivalence_reference() -> dict:
    return {'source_locator': 'II.XXV printed157', 'geometric_angle_degrees': 90,
            'interpretive_comparison': 'trine', 'requires': 'both planets in long-ascension signs',
            'equivalence_is_geometric': False, 'strength_multiplier': None}


def ship_part_reference(sign: str) -> dict:
    if sign not in SIGNS:
        raise ValueError('Unknown sign')
    return {'sign': sign, 'source_description': _load('SHIP_PARTS')['parts'][sign],
            'source_locator': 'II.XXVI printed158', 'modern_safety_guidance': False}


def ship_role_dependencies(ascendant_lord: str) -> dict:
    """Represent role overlap; this is not an evidence count or a vessel verdict."""
    if ascendant_lord not in PLANETS:
        raise ValueError('Expected a classical planet')
    return {'ship_and_goods': ['Ascendant_sign', 'Moon'],
            'sailors': [ascendant_lord],
            'planetary_roles_share_body': ascendant_lord == 'Moon',
            'distinct_named_planets': sorted({'Moon', ascendant_lord}),
            'independent_evidence_count': None}


def question_clock_reference(mode: str) -> dict:
    origins = {
        'sudden_event': ('II.XXIV printed148', 'event time, else first heard'),
        'spoken_request': ('II.XXVI printed166', 'moment the desire is propounded'),
        'letter': ('II.XXVI printed166', 'opened and querent intention perceived, not mere delivery'),
        'self_question': ('II.XXVI printed166-167', 'genuinely troubling personal concern; impartiality required'),
    }
    if mode not in origins:
        raise ValueError('No source convention for that interface or event')
    page, anchor = origins[mode]
    return {'source_locator': page, 'selected_anchor_description': anchor,
            'actual_timestamp_chosen': False, 'modern_interface_mapping': None}


def worked_arithmetic() -> dict:
    cases = _load('HISTORICAL_CASES')['cases']
    c = cases['mother_son_1638']['selected_positions']
    mother_fortune = fortune(longitude(*c['Ascendant']), longitude(*c['Moon']),
                             longitude(*c['Sun']), profile=FORTUNE_PROFILE)
    s = cases['surviving_ship_1644']['selected_positions']
    mars_reflection = antiscion(longitude(*s['Mars']))
    return {'mother_case_fortune': as_sign(mother_fortune),
            'printed_fortune_matches': mother_fortune == longitude(*c['Fortune']),
            'ship_mars_antiscion': as_sign(mars_reflection),
            'ship_mars_antiscion_to_ascendant_arcminutes': separation(mars_reflection, longitude(*s['Ascendant'])),
            'ship_moon_mercury_trine_residual_arcminutes': aspect_residual(longitude(*s['Moon']), longitude(*s['Mercury']), 120),
            'ship_moon_sun_trine_residual_arcminutes': aspect_residual(longitude(*s['Moon']), longitude(*s['Sun']), 120),
            'jupiter_exact_antiscion': None,
            'jupiter_limit': 'Jupiter minute field absent; ninth-degree source assertion retained without zero-filling',
            'physical_contact_times_computed': False, 'historical_calendar_resolved': False,
            'predictive_validation': False}
