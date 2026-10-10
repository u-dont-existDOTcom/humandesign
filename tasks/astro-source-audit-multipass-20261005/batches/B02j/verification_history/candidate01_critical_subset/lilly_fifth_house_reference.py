"""Bounded source-reference arithmetic for Lilly II XXXIX–XLIII.

This module transcribes particular historical methods. It does not determine
pregnancy, fertility, health, child sex, or astrological predictive accuracy.
All angular computations are static comparisons, without an ephemeris.
"""
from collections import Counter, defaultdict
from datetime import date
from fractions import Fraction

SIGNS = ('Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces')
CIRCLE = 360 * 60
HOUSE_YEAR_XXXIX = {1: 1, 2: 2, 10: 3, 7: 4, 4: 5}
GESTATION_XL = {
    'trine': {'values': [5, 3], 'basis': 'ordinal_month_of_conception'},
    'sextile': {'values': [2, 6], 'basis': 'ordinal_month_of_conception'},
    'square': {'values': [4], 'basis': 'ordinal_month_of_conception'},
    'opposition': {'values': [7], 'basis': 'months_already_conceived'},
    'conjunction': {'values': [1], 'basis': 'months_already_conceived'},
}


class SourceInputError(ValueError):
    """A missing or invalid value cannot be silently completed."""


def integer(value, label):
    if type(value) is not int:
        raise SourceInputError(f'{label} must be an explicit integer')
    return value


def longitude(sign, degree, minute):
    if sign not in SIGNS:
        raise SourceInputError('An explicit recognized zodiac sign is required')
    integer(degree, 'degree')
    integer(minute, 'minute')
    if not 0 <= degree < 30 or not 0 <= minute < 60:
        raise SourceInputError('Degree/minute is outside a zodiac sign')
    return SIGNS.index(sign) * 1800 + degree * 60 + minute


def read_coordinate(row):
    return longitude(row['sign'], row['degree'], row['minute'])


def zodiac(value):
    integer(value, 'longitude in minutes')
    sign, rest = divmod(value % CIRCLE, 1800)
    degree, minute = divmod(rest, 60)
    return {'sign': SIGNS[sign], 'degree': degree, 'minute': minute}


def span(degree, minute):
    integer(degree, 'arc degree')
    integer(minute, 'arc minute')
    if degree < 0 or not 0 <= minute < 60:
        raise SourceInputError('Arc must be nonnegative with minutes below60')
    return 60 * degree + minute


def part_of_children(ascendant, mars, jupiter, sect):
    """II XL p232: Mars to Jupiter, projected from Asc; same day/night."""
    if sect not in ('day', 'night'):
        raise SourceInputError('Declare day or night; neither reverses this formula')
    for value in (ascendant, mars, jupiter):
        integer(value, 'coordinate')
    return (ascendant + jupiter - mars) % CIRCLE


def retained_fortune(ascendant, moon, sun):
    """Retained II XXIII R625 formula; not a fresh formula from this batch."""
    for value in (ascendant, moon, sun):
        integer(value, 'coordinate')
    return (ascendant + moon - sun) % CIRCLE


def forward_arc(start, target):
    integer(start, 'start')
    integer(target, 'target')
    return (target - start) % CIRCLE


def remaining_to_aspect(moving, target, aspect_degrees, side):
    """Static remaining arc to an explicitly chosen aspect ray.

    `side` chooses target + or - the aspect. This does not infer motion,
    application, relative velocity, perfection, or time to an actual transit.
    """
    for value, label in ((moving, 'moving'), (target, 'target'), (aspect_degrees, 'aspect'), (side, 'side')):
        integer(value, label)
    if aspect_degrees not in (0, 60, 90, 120, 180) or side not in (-1, 1):
        raise SourceInputError('Choose an admitted aspect and explicit side')
    return forward_arc(moving, target + side * aspect_degrees * 60)


def house_year(house):
    integer(house, 'house')
    if not 1 <= house <= 12:
        raise SourceInputError('House must be1–12')
    return HOUSE_YEAR_XXXIX.get(house)  # absent mapping stays None


def gestation_alternatives(aspect):
    if aspect not in GESTATION_XL:
        raise SourceInputError('No mapping supplied for this aspect')
    source = GESTATION_XL[aspect]
    return {'values': list(source['values']), 'basis': source['basis']}


def timing_conversion(arc_minutes, method, measure):
    """Exact dimensional replay only; no universal degree-to-time rule."""
    integer(arc_minutes, 'arc')
    if arc_minutes < 0:
        raise SourceInputError('Arc must be nonnegative')
    models = {
        'XLIII_delivery_example': ('static_longitude_gap', 'week'),
        'XL_Part_of_Children_direction': ('ascensional_direction_arc', 'day'),
    }
    if method not in models or measure != models[method][0]:
        raise SourceInputError('Method and angular measure must match the source')
    return {'quantity': Fraction(arc_minutes, 60), 'unit': models[method][1]}


def dependency_keys(row):
    keys = row.get('dependencies')
    if not isinstance(keys, (list, tuple)) or not keys or not all(isinstance(x, str) and x for x in keys):
        raise SourceInputError('Dependencies must be a nonempty list of explicit names')
    return set(keys)


def tally(testimonies):
    seen = set()
    result = Counter({'male': 0, 'female': 0})
    for row in testimonies:
        if row['id'] in seen:
            raise SourceInputError('Duplicate testimony identifier')
        seen.add(row['id'])
        if row['direction'] not in result:
            raise SourceInputError('Unknown direction')
        dependency_keys(row)
        result[row['direction']] += 1
    return dict(result)


def dependency_groups(testimonies, *, planetary_bodies):
    """Role reuse needs a declared body vocabulary, not guessed string labels."""
    if not isinstance(planetary_bodies, (set, frozenset, list, tuple)) or not planetary_bodies or not all(isinstance(x, str) and x for x in planetary_bodies):
        raise SourceInputError('Explicit set/list of body names is required')
    bodies = set(planetary_bodies)
    groups = defaultdict(list)
    for row in testimonies:
        for key in dependency_keys(row) & bodies:
            groups[key].append(row['id'])
    return {key: value for key, value in sorted(groups.items()) if len(value) > 1}


def sensitivity_tally(testimonies, replacements, *, interpretation):
    """Labelled analyst counterfactual; never edits the source table."""
    if not interpretation:
        raise SourceInputError('A non-source counterfactual needs a label')
    ids = {r['id'] for r in testimonies}
    if not set(replacements) <= ids:
        raise SourceInputError('Unknown replacement row')
    changed = [{**r, 'direction': replacements.get(r['id'], r['direction'])}
               for r in testimonies]
    return {'tally': tally(changed), 'interpretation': interpretation,
            'source_repaired': False, 'changed_row_ids': sorted(replacements)}


def same_calendar_days(start, end):
    """Same-year interval wholly after February; no calendar or UTC conversion.

    Gregorian and Julian month lengths agree within this restricted interval.
    Requiring both dates after February prevents ambiguous leap-day arithmetic.
    """
    if start[0] != end[0]:
        raise SourceInputError('This helper is limited to one named calendar year')
    if start[1] < 3 or end[1] < 3:
        raise SourceInputError('Both date labels must be after February in the same calendar')
    return (date(*end) - date(*start)).days


def arc_distance(a, b):
    difference = (a - b) % CIRCLE
    return min(difference, CIRCLE - difference)


def comparison_receipt(tables):
    figures = tables['figures']
    points = [{r['label']: r for r in f['cusps'] + f['points']} for f in figures]
    x, y = points
    coord = lambda rows, label: read_coordinate(rows[label])
    first_fortune = retained_fortune(coord(x, 'cusp1'), coord(x, 'Moon'), coord(x, 'Sun'))
    children = part_of_children(coord(x, 'cusp1'), coord(x, 'Mars'), coord(x, 'Jupiter'), 'day')
    second_fortune = retained_fortune(coord(y, 'cusp1'), coord(y, 'Moon'), coord(y, 'Sun'))
    t = tables['delivery_table']
    saturn, moon, mercury = (longitude(*t[key]) for key in ('saturn', 'moon', 'mercury'))
    moon_arc = remaining_to_aspect(moon, saturn, 90, -1)
    mercury_arc = remaining_to_aspect(mercury, saturn, 0, 1)
    days = same_calendar_days((1645, 4, 7), (1645, 7, 11))
    return {
        'scope': 'Static arithmetic, printed-table counting and explicitly labelled sensitivity; not ephemeris or predictive validation.',
        'first_fortune': {'result': zodiac(first_fortune), 'matches': first_fortune == coord(x, 'Fortune'), 'conditional_on_declared_inferred_signs': True},
        'first_part_of_children': {'result': zodiac(children), 'matches': children == coord(x, 'PartOfChildren'), 'conditional_on_declared_inferred_signs': True},
        'second_fortune': {'result': zodiac(second_fortune), 'matches': second_fortune == coord(y, 'Fortune'), 'conditional_on_declared_chart_reading': True},
        'first_opposite_cusp_mismatch_minutes': arc_distance((coord(x, 'cusp3') + 180*60) % CIRCLE, coord(x, 'cusp9')),
        'source_testimony_tally': tally(tables['testimonies']),
        'repeated_body_dependencies': dependency_groups(tables['testimonies'], planetary_bodies={'Moon','Sun','Mercury','Venus','Mars','Jupiter','Saturn'}),
        'coherent_hour_chain_sensitivity': sensitivity_tally(tables['testimonies'], {'M6':'female','M7':'female'}, interpretation='Assume the figure Moon is intended as hour ruler; replace both the hour-body row and its dependent sign row. Analyst sensitivity only; the source does not give this tally.'),
        'moon_to_saturn_square_arc_minutes': moon_arc,
        'mercury_to_saturn_conjunction_arc_minutes': mercury_arc,
        'difference_minutes': abs(moon_arc - mercury_arc),
        'moon_route_weeks': str(timing_conversion(moon_arc, 'XLIII_delivery_example', 'static_longitude_gap')['quantity']),
        'mercury_route_weeks': str(timing_conversion(mercury_arc, 'XLIII_delivery_example', 'static_longitude_gap')['quantity']),
        'same_calendar_question_to_birth_days': days,
        'days_in_fourteen_weeks': 14*7,
        'reported_delivery_days_before_fourteen_week_point': 14*7-days,
        'question_sun_vs_reported_perfect_square_mismatch_minutes': arc_distance((coord(y, 'Sun')+90*60)%CIRCLE, longitude('Cancer',27,48)),
        'moon_forward_to_fifth_cusp_minutes': forward_arc(coord(y,'Moon'), coord(y,'cusp5')),
        'saturn_forward_to_ninth_cusp_minutes': forward_arc(coord(y,'Saturn'), coord(y,'cusp9')),
        'omitted_mercury_minutes_remain_null_in_figure': y['Mercury']['minute'] is None,
        'explicit_later_mercury_table_minutes': t['mercury'][2],
        'historical_ephemeris_computed': False,
        'accuracy_evaluated': False,
    }
