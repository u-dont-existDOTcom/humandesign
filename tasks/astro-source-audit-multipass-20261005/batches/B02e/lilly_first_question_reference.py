"""Exact source-reference arithmetic for Lilly 1647 II.XXII-XXIII.

No medical, financial, personality or life-event inference is performed.
Distances are static chart geometry, not actual moving-target encounter times.
"""
from __future__ import annotations
import copy
from fractions import Fraction
import json
from pathlib import Path
from typing import Literal

ROOT=Path(__file__).resolve().parent
SIGNS=('Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces')
CIRCLE=21600
PROFILES=('lilly_same_day_night','reported_nocturnal_reverse')

def _data(name: str):
    if name not in {'CASE_REFERENCE','TIMING_CASES','FORTUNE_TABLE','DIRECTIONAL_QUARTERS'}:
        raise ValueError('Undeclared source dataset')
    return json.loads((ROOT/(name+'.json')).read_text())

def _position(x: int)->int:
    if type(x) is not int or not 0<=x<CIRCLE:
        raise ValueError('Position must be integer arcminutes, 0 <= x < 21600')
    return x

def zodiac(sign: str,degrees: int,minutes: int)->int:
    if sign not in SIGNS or type(degrees) is not int or type(minutes) is not int or not 0<=degrees<30 or not 0<=minutes<60:
        raise ValueError('Named sign, degrees 0..29 and minutes 0..59 required')
    return SIGNS.index(sign)*1800+degrees*60+minutes

def decompose(x: int)->tuple[str,int,int]:
    _position(x)
    sign,remainder=divmod(x,1800)
    d,m=divmod(remainder,60)
    return SIGNS[sign],d,m

def fortune_position(asc: int,sun: int,moon: int,*,sect: Literal['day','night'],profile: str)->int:
    """An explicit source choice: main convention does not reverse at night."""
    for x in (asc,sun,moon):_position(x)
    if sect not in ('day','night') or profile not in PROFILES:
        raise ValueError('Known sect and explicitly named source profile required')
    direction=-1 if profile=='reported_nocturnal_reverse' and sect=='night' else 1
    return (asc+direction*(moon-sun))%CIRCLE

def angular_residual(a: int,b: int,aspect_degrees: int)->int:
    """Unsigned residual from a named exact aspect; no orb, speed or timing scale."""
    _position(a);_position(b)
    if type(aspect_degrees) is not int or aspect_degrees not in (0,60,90,120,180):
        raise ValueError('Only a declared principal aspect is admitted')
    d=abs(a-b);d=min(d,CIRCLE-d)
    return abs(d-aspect_degrees*60)

def house_age_bounds(house: int,*,years_per_house: Literal[5,6])->dict:
    """Algebraic schedule bounds, not a determination of life or happiness.

    5 is the ordinary source scale; 6 is its conditional extra-year alternative.
    Which scale applies, and inclusion of exact age endpoints, stay unresolved.
    """
    if type(house) is not int or not 1<=house<=12 or type(years_per_house) is not int or years_per_house not in (5,6):
        raise ValueError('House 1..12 and explicit source scale 5 or 6 required')
    lo=(12-house)*years_per_house
    return {'bounds_years':[lo,lo+years_per_house], 'years_per_house':years_per_house,
            'selection_not_determined':True,'boundary_inclusion':'UNRESOLVED',
            'source':'II.XXII printed134'}

def phase_mnemonic(elongation: int)->dict:
    """Return what the source says; do not claim computed unequal-house position."""
    _position(elongation)
    guide=_data('FORTUNE_TABLE')['phase_guide']
    q,r=divmod(elongation,5400)
    row=guide[q]
    return {'source_phase':row['phase'],'source_exact_house':row['author_house'] if r==0 else None,
            'source_interval_houses':None if r==0 else row['author_interval_houses'],
            'geometric_offset_from_asc_arcmin':elongation,
            'actual_house_from_cusps':None,
            'status':'SOURCE_MNEMONIC_NOT_HOUSE_ENGINE'}

def fortune_table_row(row_id: str)->dict:
    rows=[r for r in _data('FORTUNE_TABLE')['rows'] if r['id']==row_id]
    if len(rows)!=1:raise ValueError('Unknown row ID')
    return copy.deepcopy(rows[0])

def literal_quadrant_for_house(house: int)->dict:
    """Return the author's house group; no geographic bearing or cusp interpolation."""
    if type(house) is not int or not 1<=house<=12:raise ValueError('House 1..12 required')
    return copy.deepcopy(next(r for r in _data('DIRECTIONAL_QUARTERS') if house in r['houses']))

def can_cast_to_fortune(caster: str)->bool:
    if caster=='Fortune':return False
    if caster not in ('Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn'):
        raise ValueError('Only the source traditional planets or Fortune admitted')
    return True

def exact_case_calculations()->dict:
    d=_data('CASE_REFERENCE')['verified_positions']
    p={k:zodiac(*v) for k,v in d.items()}
    f=fortune_position(p['Ascendant'],p['Sun'],p['Moon'],sect='day',profile='lilly_same_day_night')
    m=angular_residual(p['Moon'],p['Mars'],180)
    return {
       'fortune_result':list(decompose(f)),
       'fortune_arcminutes':f,
       'sun_to_moon_forward_arcminutes':(p['Moon']-p['Sun'])%CIRCLE,
       'sun_beyond_ninth_cusp_arcminutes':p['Sun']-p['ninth_cusp'],
       'moon_mercury_opposition_residual_arcminutes':angular_residual(p['Moon'],p['Mercury'],180),
       'moon_jupiter_trine_residual_arcminutes':angular_residual(p['Moon'],p['Jupiter'],120),
       'sun_to_aries_end_arcminutes':1800-p['Sun'],
       'moon_mars_opposition_residual_arcminutes':m,
       'moon_mars_author_result_years':'about three years and three quarters',
       'moon_mars_mean_formula':None,
       'moon_mars_other_stated_option_years':str(Fraction(m,60)),
       'other_option_status':'arithmetic at explicitly mentioned one-year-per-degree; not selected as correct',
       'physical_contact_times_computed':False,
       'historical_calendar_resolved':False,
       'personal_forecast':False}

if __name__=='__main__':
    print(json.dumps(exact_case_calculations(),indent=2))
