"""Bounded arithmetic and source-table access for Lilly 1647, Book I.1-I.7.

This is a research reference module, not an astrological prediction engine.
No ephemeris, house-cusp astronomy, calendar conversion, empirical weights,
medical inference or runtime model is implemented here.
"""
from __future__ import annotations
from fractions import Fraction
from pathlib import Path
import json
from typing import Mapping

SIGNS = ('Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio',
         'Sagittarius','Capricorn','Aquarius','Pisces')
CIRCLE = Fraction(360)
DAY_MINUTES = 1440
TABLES = json.loads(Path(__file__).with_name('TABLES.json').read_text())
STATUS = 'SOURCE_REFERENCE_ONLY_NOT_PREDICTIVELY_VALIDATED'

def exact(value: int | str | Fraction) -> Fraction:
    """Accept explicit rational values; reject silent floating-point rounding."""
    if isinstance(value, bool) or not isinstance(value, (int, str, Fraction)):
        raise TypeError('Use int, Fraction or an explicit rational string.')
    return Fraction(value)

def longitude(sign: str, degree: int | str | Fraction,
              minute: int | str | Fraction = 0,
              second: int | str | Fraction = 0) -> Fraction:
    if sign not in SIGNS:
        raise ValueError('Unknown sign.')
    d, m, s = map(exact, (degree, minute, second))
    if not (0 <= d < 30 and 0 <= m < 60 and 0 <= s < 60):
        raise ValueError('Use zero-based degrees <30 and minutes/seconds <60.')
    if d + m/60 + s/3600 >= 30:
        raise ValueError('Coordinates cross the end of the declared sign.')
    return 30*SIGNS.index(sign) + d + m/60 + s/3600

def opposite(value: int | str | Fraction) -> Fraction:
    return (exact(value) + 180) % CIRCLE

def shortest_separation(a: int | str | Fraction,
                        b: int | str | Fraction) -> Fraction:
    difference = (exact(b)-exact(a)) % CIRCLE
    return min(difference, CIRCLE-difference)

def aspect_point(value: int | str | Fraction, degrees: int,
                 direction: str = 'following') -> Fraction:
    if degrees not in {0,30,60,72,90,108,120,144,150,180}:
        raise ValueError('Angle is not in the extracted source list.')
    if direction not in {'following','leading'}:
        raise ValueError('Declare following or leading sign order.')
    return (exact(value)+(1 if direction=='following' else -1)*degrees) % CIRCLE

def solar_degree_for_table(sign: str, degree: int, minute: int) -> dict:
    """I.4 rounding branch. Exact30-minute case deliberately remains unresolved."""
    longitude(sign,degree,minute)
    if minute == 30:
        return {'status':'UNRESOLVED_EXACT_HALF_DEGREE','longitude':None}
    return {'status':'SOURCE_HORARY_ROUNDING',
            'longitude':(30*SIGNS.index(sign)+degree+(minute>30))%360}

def clock_from_noon(elapsed_minutes: int | str | Fraction) -> dict:
    """Map a dated noon's elapsed minutes to clock time and civil-day offset.

    Does not choose Julian/Gregorian calendar or a UTC/time-zone interpretation.
    Extended elapsed time is allowed but its date shift is always retained.
    """
    t=exact(elapsed_minutes)+720
    shift=t//DAY_MINUTES
    within=t-shift*DAY_MINUTES
    return {'civil_day_offset':int(shift),'hour':int(within//60),
            'minute':within % 60}

def noon_origin_for_clock(hour: int, minute: int) -> dict:
    if any(isinstance(v,bool) or not isinstance(v,int) for v in (hour,minute)):
        raise TypeError('Whole clock hour and minute are required.')
    if not 0<=hour<24 or not 0<=minute<60:
        raise ValueError('Invalid clock time.')
    t=60*hour+minute
    return {'noon_date_offset':-1 if t<720 else 0,
            'elapsed_minutes':(t-720)%DAY_MINUTES}

def add_table_time(table_minutes: int, elapsed_minutes: int) -> dict:
    for value in (table_minutes,elapsed_minutes):
        if isinstance(value,bool) or not isinstance(value,int) or not 0<=value<1440:
            raise ValueError('Each input is an integer number of minutes in [0,1440).')
    total=table_minutes+elapsed_minutes
    return {'unwrapped_minutes':total,'wrapped_minutes':total%1440,
            'turns':total//1440}

def daily_arcminutes(earlier: int | str | Fraction,
                     later: int | str | Fraction, direction: str) -> Fraction:
    """Signed short daily displacement for a declared direction, not a station finder."""
    a,b=map(exact,(earlier,later))
    if direction=='direct':
        delta=(b-a)%CIRCLE
    elif direction=='retrograde':
        delta=-((a-b)%CIRCLE)
    else:
        raise ValueError('Declare direct or retrograde; unknown/station is not guessed.')
    if abs(delta)>=180:
        raise ValueError('Declared direction implies a non-short daily displacement.')
    return delta*60

def hourly_arcseconds(signed_daily_arcminutes: int | str | Fraction) -> Fraction:
    return exact(signed_daily_arcminutes)*60/24

def linear_advance(value: int | str | Fraction,
                   signed_daily_arcminutes: int | str | Fraction,
                   elapsed_minutes: int | str | Fraction) -> Fraction:
    """Exact evaluation of the source's linear model; not exact physical astronomy."""
    return (exact(value)+exact(signed_daily_arcminutes)*exact(elapsed_minutes)/1440/60)%360

def meridian_position_elapsed(london_minutes: int | str | Fraction,
                              east_offset_minutes: int | str | Fraction) -> Fraction:
    return exact(london_minutes)+exact(east_offset_minutes)

def meridian_event_time(source_minutes: int | str | Fraction,
                        east_offset_minutes: int | str | Fraction) -> Fraction:
    # Do not wrap away a date crossing: clock_from_noon handles it explicitly.
    return exact(source_minutes)-exact(east_offset_minutes)

def complete_opposite_cusps(six: Mapping[int,Fraction]) -> dict[int,Fraction]:
    if set(six)!={1,2,3,10,11,12}:
        raise ValueError('Require exactly houses1,2,3,10,11,12.')
    output={h:exact(v)%360 for h,v in six.items()}
    for h in list(output):
        output[(h+5)%12+1]=opposite(output[h])
    _validate_cusps(output)
    return output

def _validate_cusps(cusps: Mapping[int,Fraction]) -> None:
    if set(cusps)!=set(range(1,13)):
        raise ValueError('All twelve cusps are required.')
    lengths=[(exact(cusps[h%12+1])-exact(cusps[h]))%360 for h in range(1,13)]
    if any(v<=0 for v in lengths) or sum(lengths)!=360:
        raise ValueError('Cusps must make one ordered, nondegenerate zodiacal circuit.')

def physical_house(value: int | str | Fraction,
                   cusps: Mapping[int,Fraction]) -> int:
    _validate_cusps(cusps)
    value=exact(value)%360
    for h in range(1,13):
        start=exact(cusps[h])%360
        length=(exact(cusps[h%12+1])-start)%360
        if (value-start)%360 < length:
            return h
    raise RuntimeError('Validated cusps failed to partition the circle.')

def cusp_virtue_reference(value: int | str | Fraction,
                         cusps: Mapping[int,Fraction]) -> dict:
    """Preserve physical house while exposing ONLY I.4's nearest-cusp ingredient.

    This does not decide the full five-degree rule's later qualifications.
    """
    physical=physical_house(value,cusps)
    distances={h:shortest_separation(value,c) for h,c in cusps.items()}
    nearest=min(distances.values())
    winners=[h for h,d in distances.items() if d==nearest]
    if len(winners)>1:
        status='UNRESOLVED_NEAREST_CUSP_TIE';candidate=None
    elif nearest==5:
        status='UNRESOLVED_EXACT_FIVE_DEGREES';candidate=None
    elif nearest<5:
        status='CANDIDATE_PENDING_LATER_SOURCE_QUALIFICATIONS';candidate=winners[0]
    else:
        status='NO_WITHIN_FIVE_DEGREE_CANDIDATE';candidate=None
    return {'physical_house':physical,'status':status,
            'candidate_virtue_house':candidate,'nearest_distance_degrees':nearest}

def house_reference(house: int) -> dict:
    if isinstance(house,bool) or house not in range(1,13):
        raise ValueError('House must be1..12.')
    return json.loads(json.dumps(TABLES['houses'][house-1]))

def compare_house_strength(a: int,b: int, *, equally_dignified: bool | None) -> dict:
    house_reference(a);house_reference(b)
    if equally_dignified is not True:
        return {'status':'UNRESOLVED_OTHER_DIGNITIES','stronger_house':None}
    order=TABLES['house_strength_order']
    return {'status':'SOURCE_ORDINAL_ONLY','stronger_house':None if a==b else min((a,b),key=order.index)}

def annotation(letter: str, context: str) -> str:
    vocabulary={
        'latitude_direction':{'A':'ascending latitude','D':'descending latitude'},
        'latitude_hemisphere':{'M':'south of ecliptic','S':'north of ecliptic'},
        'longitudinal_motion':{'D':'direct','Di':'direct','R':'retrograde'},
    }
    if context not in vocabulary or letter not in vocabulary[context]:
        raise ValueError('The source context does not license this interpretation.')
    return vocabulary[context][letter]
