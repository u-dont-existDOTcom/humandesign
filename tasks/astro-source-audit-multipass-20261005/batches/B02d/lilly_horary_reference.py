"""Bounded, source-labelled lookup helpers for Lilly 1647 Book I XIX–XXI.

Not a forecasting engine: no outcome scoring, unverified source rules,
person-specific predictions, calendar inference or rule-selection by fit.
All angle arguments are integer arcminutes, 0 <= x < 21600.
"""
from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CIRCLE = 360 * 60
ASPECT_DEGREES = (0, 60, 90, 120, 180)


@lru_cache(maxsize=None)
def _data(basename: str) -> dict:
    allowed = {
        'ORB_PROFILES', 'ASPECT_TABLES', 'STRENGTH_ROWS',
        'DEGREE_TABLE', 'BODY_TABLE', 'HOUSE_EXAMPLES',
    }
    if basename not in allowed:
        raise ValueError('No declared B02d source table')
    return json.loads((ROOT / (basename + '.json')).read_text())


def source_orb(planet: str, profile: str) -> int:
    """Full orb in arcminutes, not its moiety. Explicit profile required."""
    profiles = _data('ORB_PROFILES')['profiles']
    if profile not in profiles:
        raise ValueError('Explicit named printed orb column required')
    try:
        return int(profiles[profile][planet])
    except KeyError:
        raise ValueError('Unknown planet in Lilly orb table') from None


def angular_distance(a: int, b: int) -> int:
    if not all(type(v) is int and 0 <= v < CIRCLE for v in (a, b)):
        raise ValueError('Positions must be integer arcminutes in [0, 21600)')
    d = abs(a - b)
    return min(d, CIRCLE - d)


def aspect_residual(a: int, b: int, aspect: int) -> int:
    """Distance from exact angular separation, without a presumed orb."""
    if type(aspect) is not int or aspect not in ASPECT_DEGREES:
        raise ValueError('No source-qualified aspect with that angle')
    return abs(angular_distance(a, b) - aspect * 60)


def is_exact_partile(a: int, b: int, aspect: int) -> bool:
    """One narrowly specified exact-degree-and-minute point, not the general rule's orb."""
    return aspect_residual(a, b, aspect) == 0


def platick_contact(a: int, b: int, aspect: int, planet_a: str, planet_b: str, profile: str) -> bool | None:
    """Within moiety sum. Equality returns unresolved (the text says 'within')."""
    residual = Fraction(aspect_residual(a, b, aspect), 1)
    allowance = Fraction(source_orb(planet_a, profile) + source_orb(planet_b, profile), 2)
    if residual == allowance:
        return None
    return residual < allowance


def _sign_number(sign: str) -> int:
    try:
        return _data('ASPECT_TABLES')['sign_names'].index(sign) + 1
    except ValueError:
        raise ValueError('Sign not in the source table') from None


def rays_from(source_sign: str) -> dict:
    i = _sign_number(source_sign)
    for row in _data('ASPECT_TABLES')['aspect_rows']:
        if row[0] == i:
            names = _data('ASPECT_TABLES')['sign_names']
            return {
                'source_sign': source_sign,
                'dexter': dict(zip((60, 90, 120), (names[n-1] for n in row[1]))),
                'sinister': dict(zip((60, 90, 120), (names[n-1] for n in row[2]))),
                'opposition': names[row[3]-1],
                'source_ref': 'Lilly printed108-109 PDF142-143',
            }
    raise AssertionError('Source sign table incomplete')


def in_nonbeholding_source_table(source_sign: str, target_sign: str) -> bool | None:
    """True when explicitly listed; None otherwise, since printed table is incomplete."""
    _sign_number(source_sign)
    target_n = _sign_number(target_sign)
    return True if target_n in _data('ASPECT_TABLES')['not_beholding_raw'][source_sign] else None


def turned_radical_house(subject_radical_house: int, subject_relative_house: int) -> int:
    if not all(type(v) is int and 1 <= v <= 12 for v in (subject_radical_house, subject_relative_house)):
        raise ValueError('Houses numbered 1-12 only')
    return (subject_radical_house + subject_relative_house - 2) % 12 + 1


def declared_horary_house_example(subject: str) -> dict:
    """Source's fixed role examples. Returns reference frame separately from topic."""
    t = _data('HOUSE_EXAMPLES')
    origins = {'partner': t['partner_origin'], 'wife_brother_or_minister': t['minister_or_wifes_brother_origin'],
               'king_as_subject': t['king_asked_about_origin'], 'asker_even_if_king': t['asker_origin_regardless_rank'],
               'natal_even_if_king': t['natal_native_origin_regardless_rank']}
    if subject not in origins:
        raise ValueError('Undeclared source example: no speculative generic role')
    return {'subject': subject, 'radical_origin': origins[subject],
            'relative_houses': [turned_radical_house(origins[subject], i) for i in range(1, 13)],
            'source_ref': 'Lilly Book I XXI printed127-128 PDF161-162'}


def solar_separation_claims(planet_sign: str, sun_sign: str, separation_arcminutes: int) -> dict:
    """Source reports thresholds AND a contradictory combustion worked example.

    The boolean fields describe strict textual thresholds, not a predictive,
    fully adjudicated zone classifier; boundary cases return None.
    """
    _sign_number(planet_sign)
    _sign_number(sun_sign)
    if type(separation_arcminutes) is not int or not 0 <= separation_arcminutes <= 180*60:
        raise ValueError('Separation must be 0..10800 integer arcminutes')
    same = planet_sign == sun_sign
    def below_or_unresolved(threshold: int) -> bool | None:
        return None if separation_arcminutes == threshold else separation_arcminutes < threshold
    cazimi = below_or_unresolved(17)
    within_combust = below_or_unresolved(8*60+30) if same else False
    within_beams = below_or_unresolved(17*60)
    conflict = same and separation_arcminutes == 10*60
    return {
        'literal_cazimi_17arcmin': cazimi,
        'literal_same_sign_combust_8d30': within_combust,
        'literal_sun_beams_17d': within_beams,
        'directly_conflicting_10degree_combust_example': conflict,
        'claim_scope': 'literal source thresholds only; exact boundaries and precedence unresolved',
        'source_ref': 'Lilly Book I XIX printed113-114 PDF147-148',
    }


def printed_strength_row(row_id: str) -> dict:
    """One signed-table line; never combine all matching lines into a net score."""
    matches = [r for r in _data('STRENGTH_ROWS')['rows'] if r['id'] == row_id]
    if len(matches) != 1:
        raise ValueError('A single source row ID is required')
    return dict(matches[0])


def historical_body_entry(sign: str, planet: str) -> dict:
    """Historical body-part text, not medical diagnosis, risk or advice."""
    _sign_number(sign)
    if planet not in {'Sun', 'Moon', 'Saturn', 'Jupiter', 'Mars', 'Venus', 'Mercury'}:
        raise ValueError('Unknown planet')
    d = _data('BODY_TABLE')
    return {'sign': sign, 'planet': planet, 'raw_reading': d['rows'][sign][planet],
            'source_ref': 'Lilly Book I XIX printed119 PDF153',
            'not_validated_medical_guidance': True}
