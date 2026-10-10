"""Finite source lookups and testimony bookkeeping, not a prediction engine.

All names and slots are local to the fourth-house chapters. Unknown relationships,
omitted inputs and unspecified tie rules are rejected or exposed, never filled.
Source wording is retained as verbal direction, without invented compass angles.
"""
from collections import Counter, defaultdict
from copy import deepcopy

SIGNS = ('Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces')
GOODS_HOUSES = {'own': 2, 'sibling': 4, 'father': 5, 'mother': 11}
DIRECTIONS = {
    'Aries': ('east', 'east'), 'Leo': ('east by north', 'east'),
    'Sagittarius': ('east by south', 'east'),
    'Libra': ('west', 'west'), 'Gemini': ('west by south', 'west'),
    'Aquarius': ('west by north', 'west'),
    'Cancer': ('north', 'north'), 'Scorpio': ('north by east', 'north'),
    'Pisces': ('north by west', 'north'),
    'Capricorn': ('south', 'south'), 'Taurus': ('south by east', 'south'),
    'Virgo': ('south by west', 'south'),
}
MISLAID_SLOTS = ('Ascendant', 'AscendantLord', 'FourthCusp', 'FourthLord',
                'Moon', 'SecondCusp', 'SecondLord', 'PartOfFortune')
RAIN_SIGNS = ('Cancer', 'Leo', 'Aquarius', 'Pisces')
PROPERTY_FRAMES = {
    'purchase': {
        'first': 'Buyer, first lord and planet from which Moon separates',
        'fourth': 'Property, occupants, Moon and fourth lord',
        'seventh': 'Seller, seventh lord and planet to which Moon applies',
        'tenth': 'Price, occupants and tenth lord',
        'pdf_pages': [238, 239]},
    'land_quality': {
        'first': 'Tenants or farmers', 'fourth': 'Soil, land and buildings',
        'seventh': 'Herbage, small plants, corn or grass',
        'tenth': 'Timber, trees or larger plants', 'pdf_pages': [240, 241]},
    'rental': {
        'first': 'Tenant or person seeking to hire',
        'fourth': 'End of the undertaking', 'seventh': 'Lessor or person letting',
        'tenth': 'Profit arising from the undertaking', 'pdf_pages': [242, 243]},
}


def goods_house(relationship):
    """Explicit XXXII examples only; not a universal recursive house rule."""
    if relationship not in GOODS_HOUSES:
        raise ValueError('Relationship not one of the four source examples')
    return {'relationship': relationship, 'radical_house': GOODS_HOUSES[relationship],
            'source': 'II.XXXII PDF236 / printed202',
            'later_second_lord_substitution_automated': False,
            'status': 'SOURCE_ROLE_LOOKUP_ONLY'}


def property_frame(context):
    if context not in PROPERTY_FRAMES:
        raise ValueError('Explicit purchase, land_quality or rental context required')
    return {'context': context, 'roles': deepcopy(PROPERTY_FRAMES[context]),
            'status': 'SOURCE_ROLE_LOOKUP_ONLY'}


def sign_direction(sign):
    if sign not in DIRECTIONS:
        raise ValueError('Unknown sign')
    label, quarter = DIRECTIONS[sign]
    return {'sign': sign, 'verbal_direction': label, 'quarter': quarter,
            'bearing_degrees': None, 'source': 'II.XXXII PDF237–238 / printed203–204'}


def mislaid_direction_tally(slots):
    """Count the eight printed slots; expose ties and shared physical bodies.

    Each slot must have a sign. An optional body identifier records when named
    planetary roles coincide. This does not convert correlated slots into
    independent evidence or supply a location, probability, weight or tie-break.
    """
    if not isinstance(slots, dict) or set(slots) != set(MISLAID_SLOTS):
        raise ValueError('Exactly the eight printed sign slots are required')
    counts = Counter({q: 0 for q in ('east', 'west', 'north', 'south')})
    identities, body_signs = defaultdict(list), {}
    rows = []
    for slot in MISLAID_SLOTS:
        row = slots[slot]
        if not isinstance(row, dict) or row.get('sign') not in SIGNS:
            raise ValueError(f'Explicit valid sign required for {slot}')
        info = sign_direction(row['sign'])
        counts[info['quarter']] += 1
        body = row.get('body')
        if body is not None:
            if not isinstance(body, str) or not body:
                raise ValueError('Body identity must be a nonempty string or absent')
            if body in body_signs and body_signs[body] != row['sign']:
                raise ValueError('The same physical body cannot have two signs')
            body_signs[body] = row['sign']
            identities[body].append(slot)
        rows.append({'slot': slot, **info, 'body': body})
    maximum = max(counts.values())
    leaders = [q for q, n in counts.items() if n == maximum]
    return {
        'source': 'II.XXXII PDF237–238 / printed203–204',
        'scope': 'Mislaid/missing within the house; source expressly excludes theft',
        'source_slots_counted': 8, 'rows': rows, 'quarter_counts': dict(counts),
        'largest_count_quarters': leaders,
        'unresolved_tie': len(leaders) != 1,
        'shared_body_slots': {b: v for b, v in identities.items() if len(v) > 1},
        'independent_evidence_count': None, 'weights': None, 'tie_break': None,
        'location_prediction': None, 'status': 'RAW_SOURCE_TESTIMONY_BOOKKEEPING',
    }


def depth_order(first_sign_progress, second_sign_progress):
    """Compare only progress within a sign, under the attributed Alkindus rule."""
    for value in (first_sign_progress, second_sign_progress):
        if type(value) is not int or not 0 <= value < 1800:
            raise ValueError('Sign progress must be integer arcminutes 0..1799')
    relation = ('same sign progress' if first_sign_progress == second_sign_progress
                else 'first deeper' if first_sign_progress > second_sign_progress
                else 'second deeper')
    return {'source': 'II.XXXVII PDF252 / printed218, attributed to Alkindus',
            'ordinal_relation': relation, 'physical_depth': None,
            'shallow_deep_threshold': None, 'units': None,
            'status': 'SOURCE_ORDINAL_COMPARISON_ONLY'}


def reference_inventory():
    return {'goods_houses': deepcopy(GOODS_HOUSES),
            'property_frames': deepcopy(PROPERTY_FRAMES),
            'directions': {s: sign_direction(s) for s in SIGNS},
            'mislaid_slots': list(MISLAID_SLOTS),
            'waterworks_rain_signs': list(RAIN_SIGNS),
            'waterworks_list_is_all_water_signs': False,
            'ancient_hour_lord_rule': {
                'source': 'II.XXXII PDF237 / printed203',
                'source_first_branch_houses': [10, 11],
                'house_twelve_coverage': None, 'angular_endpoint_policy': None,
                'author_assessment': 'Lilly says this judgment is not very exact',
                'complete_house_mapping': None},
            'runtime_promotions': 0, 'predictive_validations': 0}


if __name__ == '__main__':
    from pathlib import Path
    import json
    target = Path(__file__).with_name('QUERY_REFERENCES.json')
    target.write_text(json.dumps(reference_inventory(), indent=2, ensure_ascii=False)+'\n')
