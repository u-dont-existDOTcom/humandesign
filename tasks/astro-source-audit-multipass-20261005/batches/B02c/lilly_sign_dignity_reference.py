"""Bounded helpers for Lilly B02c; deliberately not a chart/prediction engine.

Required table profile and numbered-degree inputs prevent an implicit choice
between the earlier enumerations and the later printed summary table. Geometry
uses explicitly declared continuous longitude, separately from ordinal degrees.
"""
from __future__ import annotations
from fractions import Fraction
import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
PROFILE = 'LILLY_1647_P104_TABLE'
DATA = json.loads((ROOT / 'DIGNITY_TABLE_P104.json').read_text(encoding='utf-8'))
CATALOGUE = json.loads((ROOT / 'PORTRAITS_AND_SIGNS.json').read_text(encoding='utf-8'))
SIGNS = tuple(DATA['terms'])
PLANETS = ('Saturn','Jupiter','Mars','Sun','Venus','Mercury','Moon')
GROUPS = {r['key']:frozenset(r['signs']) for r in CATALOGUE['sign_groups']}

def _profile(profile: str) -> None:
    if profile != PROFILE:
        raise ValueError('Choose the explicit LILLY_1647_P104_TABLE witness; no implicit source reconciliation.')

def _sign(sign: str) -> None:
    if sign not in SIGNS:
        raise ValueError(f'Unknown sign: {sign!r}')

def _ordinal(degree: int) -> None:
    if type(degree) is not int or not 1 <= degree <= 30:
        raise ValueError('A numbered degree must be an integer 1..30, not continuous longitude.')

def _integer(value: int, low: int, high: int) -> None:
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f'Expected integer {low}..{high}, got {value!r}')

def _longitude(value: int | float | Fraction) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int,float,Fraction)):
        raise ValueError('Expected a finite numeric continuous longitude.')
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError('Longitude must be finite.')
    q = Fraction(str(value)) if isinstance(value,float) else Fraction(value)
    if not 0 <= q < 360:
        raise ValueError('Declared continuous longitude must be in [0,360).')
    return q

def antiscion(longitude: int | float | Fraction) -> Fraction:
    """Continuous-coordinate translation of the reflection, not an orb/event rule."""
    return (180 - _longitude(longitude)) % 360

def contrantiscion(longitude: int | float | Fraction) -> Fraction:
    return (antiscion(longitude) + 180) % 360

def complement_degree_minute(degree: int, minute: int) -> tuple[int,int]:
    """Subtract a within-sign coordinate from30:00; zero maps to literal30:00.

This function does not decide to which ordinal degree a boundary belongs.
"""
    _integer(degree,0,29)
    _integer(minute,0,59)
    return divmod(1800 - (degree*60+minute),60)

def ordinal_term(sign: str, degree: int, *, profile: str) -> str:
    _profile(profile); _sign(sign); _ordinal(degree)
    return next(planet for planet,end in DATA['terms'][sign] if degree <= end)

def ordinal_face(sign: str, degree: int, *, profile: str) -> str:
    _profile(profile); _sign(sign); _ordinal(degree)
    return DATA['faces'][sign][(degree-1)//10]

def essential_components(planet: str, sign: str, degree: int, day_or_night: str, *, profile: str) -> dict[str,Any]:
    """Only the five positive essential components; no moral/outcome/net score.

The chapter's own examples distinguish the components from the conditional
analogies, which can be defeated by combustion, retrogradation or affliction.
"""
    _profile(profile); _sign(sign); _ordinal(degree)
    if planet not in PLANETS:
        raise ValueError('This helper scores only the seven stated planets, not node exaltations.')
    if day_or_night not in ('day','night'):
        raise ValueError('Known day/night status required; unknown is not night.')
    element = next(k for k in ('fire','earth','air','water') if sign in GROUPS[k])
    exalted = DATA['exaltations'].get(sign)
    present = {
      'domicile':DATA['domiciles'][sign] == planet,
      'exaltation':bool(exalted and exalted[0] == planet),
      'triplicity':DATA['triplicity'][element][day_or_night] == planet,
      'term':ordinal_term(sign,degree,profile=profile) == planet,
      'face':ordinal_face(sign,degree,profile=profile) == planet,
    }
    components = {k:DATA['essential_weights'][k] if v else 0 for k,v in present.items()}
    return {'profile':profile,'coordinate_kind':'numbered_degree_1_to_30','components':components,
      'positive_essential_sum':sum(components.values()),
      'is_outcome_probability':False,'includes_accidental_conditions':False,
      'includes_debility_penalties':False,'includes_personality_judgment':False}

def _tri(values: tuple[bool|None,...]) -> bool|None:
    if any(v is not None and type(v) is not bool for v in values):
        raise ValueError('Use literal True, False or None for unknown.')
    if False in values:
        return False
    return None if None in values else True

def domicile_analogy_eligible(*, in_own_domicile: bool|None, retrograde: bool|None, combust: bool|None, afflicted: bool|None) -> bool|None:
    vals=(in_own_domicile,retrograde,combust,afflicted)
    if any(v is not None and type(v) is not bool for v in vals):
        raise ValueError('Use literal True, False or None.')
    return _tri((in_own_domicile,*tuple(None if v is None else not v for v in vals[1:])))

def exaltation_portrait_eligible(*, exalted: bool|None, unimpeded: bool|None, angular: bool|None) -> bool|None:
    return _tri((exalted,unimpeded,angular))

def modality_pair(ascendant_sign: str|None, ruler_sign: str|None) -> dict[str,Any]:
    for s in (ascendant_sign,ruler_sign):
        if s is not None:
            _sign(s)
    if ascendant_sign is None or ruler_sign is None:
        return {'source_branch':None,'reason':'missing_input','evaluated_as_match':False}
    a=next(m for m in ('movable','fixed','common') if ascendant_sign in GROUPS[m])
    b=next(m for m in ('movable','fixed','common') if ruler_sign in GROUPS[m])
    if a!=b:
        return {'source_branch':None,'reason':'mixed_modalities_not_specified','evaluated_as_match':False}
    return {'source_branch':a,'reason':'both_antecedents_satisfied','evaluated_as_match':True}

def feral_sign_status(sign: str) -> bool|None:
    _sign(sign)
    if sign=='Leo':
        return True
    if sign=='Sagittarius':
        return None  # Source says last part; no numerical threshold is chosen.
    return False

def source_time_segment(start: tuple[int,int], end: tuple[int,int], *, next_day: bool=False) -> dict[str,Any]:
    if type(next_day) is not bool:
        raise ValueError('next_day must be an explicit boolean.')
    if len(start)!=2 or len(end)!=2:
        raise ValueError('Expected (hour, minute) endpoints.')
    for h,m in (start,end):
        _integer(h,0,23); _integer(m,0,59)
    span=end[0]*60+end[1] - start[0]*60-start[1] + 1440*next_day
    if span<0 or span>1440:
        raise ValueError('Declare the civil-day rollover explicitly; at most one day here.')
    return {'elapsed_minutes':span,'kind':'tabulated_endpoint_segment','is_exact_full_sign_rising_time':False}

def compare_earlier_enumerations(earlier: dict[str,Any]) -> dict[str,Any]:
    """Enumerated owner sets versus explicit later table; nothing is repaired."""
    result={}
    for oldfield,kind,lookup in [('raw_terms','terms',ordinal_term),('raw_faces','faces',ordinal_face)]:
        owners={(s,d):[] for s in SIGNS for d in range(1,31)}
        for row in earlier['planets']:
            for entry in row[oldfield]:
                _sign(entry['sign'])
                for d in entry['ordinal_degrees_inclusive']:
                    _ordinal(d); owners[(entry['sign'],d)].append(row['planet'])
        differences=[]
        for (s,d),old in owners.items():
            new=lookup(s,d,profile=PROFILE)
            if old!=[new]:
                differences.append({'sign':s,'numbered_degree':d,'earlier_owners':old,'later_owner':new,
                  'earlier_status':'unassigned' if not old else 'multiple' if len(old)>1 else 'single_different_owner'})
        result[kind]={'compared_cells':360,'differences_count':len(differences),
           'earlier_nonunique_cells':sum(len(x['earlier_owners'])!=1 for x in differences),
           'differences':differences}
    return {'profile':PROFILE,'mutates_source':False,'comparison_coordinate':'integer numbered degrees','comparison':result}
