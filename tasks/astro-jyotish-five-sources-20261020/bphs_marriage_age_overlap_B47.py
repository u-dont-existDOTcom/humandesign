"""B47 source-only witness; NOT a natal prediction engine or production SWIEPH."""
from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet


@dataclass(frozen=True)
class Witness:
    ascendant: float
    sun: float
    venus: float
    saturn: float
    sun_flags: int
    venus_flags: int
    saturn_flags: int


def zodiac_sign(longitude: float) -> int:
    return int(longitude % 360 // 30)


def distance(a: float, b: float) -> float:
    sep = abs(a - b) % 360
    return min(sep, 360 - sep)


def source_age_sets(w: Witness) -> tuple[FrozenSet[int], FrozenSet[int]]:
    """Specialized to the Cancer-Lagna/Saturn-seventh-lord source witness.

    Ch18 v22: seventh lord both in ninth AND in a Jupiter-owned benefic sign,
    plus Venus exalted. This stronger conjunction satisfies both translations.
    Ch18 v23: Sun in seventh, seventh lord Saturn joined Venus in the same
    sign, with separation < 1 degree in this selected case. The Sanskrit
    does not define an orb; the numeric proximity is *additional* evidence.
    """
    rising = zodiac_sign(w.ascendant)
    seventh = (rising + 6) % 12
    ninth = (rising + 8) % 12
    if (rising, seventh, ninth) != (3, 9, 11):
        raise ValueError("B47 witness supports Cancer Lagna and Capricorn seventh only")
    lord_in_ninth = zodiac_sign(w.saturn) == ninth
    lord_in_benefic_sign = zodiac_sign(w.saturn) in (8, 11)
    venus_exalted = zodiac_sign(w.venus) == 11
    verse22 = lord_in_ninth and lord_in_benefic_sign and venus_exalted
    verse23 = (zodiac_sign(w.sun) == seventh and
               zodiac_sign(w.saturn) == zodiac_sign(w.venus) and
               distance(w.saturn, w.venus) < 1.0)
    return (frozenset((5, 9)) if verse22 else frozenset(),
            frozenset((7, 11)) if verse23 else frozenset())


def original_moshier_witness() -> Witness:
    """Equatorial synthetic location at 0N 0E, 1908-02-10 17:30 UTC.

    Moshier+Lahiri SIDEREAL intentionally NOT the SWIEPH production engine.
    Require the actual returned ephemeris flag (not merely the request).
    """
    import swisseph as swe
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    jd = swe.julday(1908, 2, 10, 17.5)
    requested = swe.FLG_MOSEPH | swe.FLG_SIDEREAL
    positions: dict[str, float] = {}
    returned: dict[str, int] = {}
    for name, planet in (("sun", swe.SUN), ("venus", swe.VENUS),
                         ("saturn", swe.SATURN)):
        (values, flags) = swe.calc_ut(jd, planet, requested)
        if (flags & 7) != swe.FLG_MOSEPH or not (flags & swe.FLG_SIDEREAL):
            raise RuntimeError(f"Ephemeris returned unexpected mode: {name}={flags}")
        positions[name] = values[0] % 360
        returned[name] = flags
    (_, ascmc) = swe.houses_ex(jd, 0.0, 0.0, b"P", swe.FLG_SIDEREAL)
    return Witness(ascmc[0] % 360, positions["sun"], positions["venus"],
                   positions["saturn"], returned["sun"], returned["venus"],
                   returned["saturn"])


if __name__ == "__main__":
    import json
    from dataclasses import asdict
    w = original_moshier_witness()
    a, b = source_age_sets(w)
    print(json.dumps({"schema_version": 1, "source_only": True,
                      "date_utc": "1908-02-10T17:30:00Z", "lat": 0, "lon": 0,
                      "ephemeris": "MOSEPH Lahiri sidereal NONPRODUCTION",
                      "witness": asdict(w), "18_22_ages": sorted(a),
                      "18_23_ages": sorted(b),
                      "first_marriage_age_intersection": sorted(a & b)}, indent=2))
