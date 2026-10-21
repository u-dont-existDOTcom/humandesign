"""Research-only geocentric whole-sign support, NOT human astrology validation.

Source coordinates: Sārāvalī 35.155 and 35.186, B35 source matrix.
Results are sign-based impossibility tests, not natal charts or a clinical tool.
"""
from itertools import combinations

ELONGATION = {'Mercury': 28, 'Venus': 48}
EXALTATION = {'Sun': 0, 'Moon': 1, 'Mars': 9, 'Mercury': 5,
             'Jupiter': 3, 'Venus': 11, 'Saturn': 6}


def minimum_whole_sign_gap_deg(a: int, b: int) -> int:
    """Lower bound between any two 30-degree sign bins (0=Aries)."""
    if type(a) is not int or type(b) is not int or not 0 <= a < 12 or not 0 <= b < 12:
        raise ValueError('Sign indices must be integers from 0 to 11')
    steps = min(abs(a - b), 12 - abs(a - b))
    return 30 * max(0, steps - 1)


def sun_pair_empty(planet: str, planet_sign: int, sun_sign: int) -> bool:
    if planet not in ELONGATION:
        raise ValueError('Only Mercury/Venus have the documented bounds')
    return minimum_whole_sign_gap_deg(planet_sign, sun_sign) > ELONGATION[planet]


def six_exaltation_exclusions() -> dict[str, list[str]]:
    """Only simple elongation constraints; no guarantee survivors actually occur."""
    result = {}
    for missing in EXALTATION:
        p = {k: v for k, v in EXALTATION.items() if k != missing}
        failures = []
        for pair in (('Sun', 'Mercury', 28), ('Sun', 'Venus', 48),
                     ('Mercury', 'Venus', 76)):
            a, b, bound = pair
            if a in p and b in p and minimum_whole_sign_gap_deg(p[a], p[b]) > bound:
                failures.append(f'{a}/{b}')
        result[missing] = failures
    return result
