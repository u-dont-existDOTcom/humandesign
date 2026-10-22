"""B57 reproducible, non-production symbolic ārūḍha source comparison.

No ephemeris, natal input, historic/real individual, questionnaire, rating,
predictive score or source-variant selection. Sign indices: Aries=0, Pisces=11.
The Venkateśa branch is deliberately LOCAL to clauses explicitly checked;
there is no invented global rider or source priority.
"""
from __future__ import annotations
from typing import Literal

CanonicalPolicy = Literal['RATH_BPHS_CH29', 'VENKATESHA_COMMENTARY_LOCAL']
GrahaBase = Literal['OWNED_SIGN', 'PLANET_SELF_GLOSS']
DegreeMode = Literal['RATH_COMPLEMENT', 'RETAIN_SIGN_DEGREE', 'SIGN_ONLY']


def _sign(n: int) -> int:
    if not isinstance(n, int) or isinstance(n, bool) or not 0 <= n <= 11:
        raise ValueError('Synthetic sidereal sign indices must be integers 0..11')
    return n


def count_inclusive(source_sign: int, target_sign: int) -> int:
    """Forward inclusive zodiacal sign count; no orientation variants assumed."""
    return (_sign(target_sign) - _sign(source_sign)) % 12 + 1


def nth_from(sign: int, n: int) -> int:
    _sign(sign)
    if not isinstance(n, int) or isinstance(n, bool) or not 1 <= n <= 12:
        raise ValueError('Inclusive sign count must be 1..12')
    return (sign + n - 1) % 12


def bhava_arudha(*, bhava_sign: int, lord_sign: int, version: CanonicalPolicy,
                 synthetic: bool = False) -> dict[str, object]:
    """Version-isolated *readings*, not truth claims or scoreable chart rules."""
    if synthetic is not True:
        raise ValueError('Require synthetic=True for research-only calculation')
    _sign(bhava_sign); _sign(lord_sign)
    n = count_inclusive(bhava_sign, lord_sign)
    raw = nth_from(lord_sign, n)
    source_relative_raw = count_inclusive(bhava_sign, raw)
    if version == 'RATH_BPHS_CH29':
        if source_relative_raw in (1, 7):
            result = nth_from(raw, 10)
            status = 'EXPLICIT_RIDER_FROM_BPHS_29_4_5_AND_RATH_LESSON18'
        else:
            result = raw
            status = 'UNMODIFIED_COUNT'
    elif version == 'VENKATESHA_COMMENTARY_LOCAL':
        if n in (1, 7):
            result = bhava_sign
            status = 'COMMENTARY_OR_CITED_VRIDDHA_FIRST_SEVENTH_RULE'
        elif n == 4:
            result = nth_from(bhava_sign, 7)
            status = 'COMMENTARY_SVASTHE_DARAH_SEVENTH'
        elif n == 10:
            result = None
            status = 'UNRESOLVED_TENTH_LORD_PLACEMENT_NOT_LOCAL_SOURCE_RULE'
        else:
            result = raw
            status = 'BASE_COUNT_NO_ADDITIONAL_COMMENTARIAL_RIDER'
    else:
        raise ValueError('Unknown source interpretation; source selection forbidden')
    return {
        'source_version': version, 'bhava_sign': bhava_sign, 'lord_sign': lord_sign,
        'lord_relative_house': n, 'raw_pada_sign': raw, 'pada_sign': result,
        'status': status, 'synthetic_only': True, 'canonical_choice': None,
        'score_allowed': False
    }


def unresolved_two_lords(*, bhava_sign: int, lord_signs: dict[str, int],
                         version: CanonicalPolicy, synthetic: bool = False) -> dict[str, object]:
    """Preserve multiple candidate padas; source's stronger-lord rule not implemented."""
    if synthetic is not True or len(lord_signs) != 2 or len(set(lord_signs)) != 2:
        raise ValueError('Require two distinct labeled synthetic co-lords')
    if any(not isinstance(k, str) or not k.strip() for k in lord_signs):
        raise ValueError('Every synthetic lord must be named')
    vals = {name:bhava_arudha(bhava_sign=bhava_sign,lord_sign=pos,version=version,
                                synthetic=True) for name,pos in lord_signs.items()}
    return {'variants': vals, 'candidate_signs':sorted(set(v['pada_sign'] for v in vals.values() if v['pada_sign'] is not None)),
            'strengths_verified': False, 'dominant_lord': None,
            'canonical_choice': None, 'score_allowed': False}


def graha_arudha(*, planet_sign: int, owned_sign: int, base: GrahaBase,
                  synthetic: bool = False) -> dict[str,object]:
    if synthetic is not True: raise ValueError('Synthetic-only source review')
    n = count_inclusive(planet_sign, owned_sign)
    if base == 'OWNED_SIGN':
        pada = nth_from(owned_sign, n)
    elif base == 'PLANET_SELF_GLOSS':
        pada = nth_from(planet_sign, n)
    else:
        raise ValueError('Unknown textual source base')
    return {'count': n, 'planet_sign': planet_sign, 'owned_sign': owned_sign,
            'pada_sign': pada, 'source_base':base,
            'exception_rider_applied':False, 'canonical_choice':None,
            'score_allowed':False}


def arudha_degree(*, natal_sign_degree: float, mode: DegreeMode,
                  synthetic: bool = False) -> dict[str,object]:
    if synthetic is not True: raise ValueError('Synthetic-only source review')
    if (not isinstance(natal_sign_degree,(float,int)) or isinstance(natal_sign_degree,bool)
            or not 0 <= natal_sign_degree < 30):
        raise ValueError('Sign degree must be numeric in [0,30)')
    status = 'DEFINED_WITHIN_SIGN'
    if mode == 'RETAIN_SIGN_DEGREE':
        degree = float(natal_sign_degree)
    elif mode == 'RATH_COMPLEMENT':
        if natal_sign_degree == 0:
            degree = None
            status = 'ZERO_DEGREE_COMPLEMENT_30_DEG_BOUNDARY_UNRESOLVED'
        else:
            degree = 30-float(natal_sign_degree)
    elif mode == 'SIGN_ONLY':
        degree = None
        status = 'NO_SOURCE_AUTHORIZED_ARUDHA_DEGREE'
    else:
        raise ValueError('Unverified longitude mode')
    return {'arudha_degree':degree, 'degree_mode':mode, 'status':status,
            'classical_sanskrit_explicitly_defines_degree':False,
            'canonical_choice':None,'score_allowed':False}
