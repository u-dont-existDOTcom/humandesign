"""Bounded Book I definitions, not a deployed prediction or scoring engine.

Continuous degree lookup uses an explicitly modern half-open convention.
Historical wording/ordinal examples require their own conversion contract.
"""
from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIGNS = tuple("ARIES TAURUS GEMINI CANCER LEO VIRGO LIBRA SCORPIO SAGITTARIUS CAPRICORN AQUARIUS PISCES".split())
PLANETS = frozenset({"SUN", "MOON", "SATURN", "JUPITER", "MARS", "VENUS", "MERCURY"})
TERMS = json.loads((HERE / "TERMS_TABLES.json").read_text())
DIGNITIES = json.loads((HERE / "DIGNITY_DEFINITIONS.json").read_text())


def _sign(sign: str) -> int:
    if sign not in SIGNS:
        raise ValueError("Expected an explicit uppercase sign name")
    return SIGNS.index(sign)


def _sect(sect: str) -> None:
    if sect not in {"DAY", "NIGHT"}:
        raise ValueError("Expected DAY or NIGHT, not an assumed sect")


def _number(value: float, low: float, high: float, *, closed_high: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError("Expected a finite number, not a boolean")
    if value < low or (value > high if closed_high else value >= high):
        raise ValueError("Value outside the declared interval")
    return float(value)


def domicile_owner(sign: str | None) -> str | None:
    if sign is None:
        return None
    _sign(sign)
    return next(p for p, houses in DIGNITIES["domiciles"].items() if sign in houses)


def exaltation_state(planet: str | None, sign: str | None) -> str | None:
    if planet is None or sign is None:
        return None
    if planet not in PLANETS:
        raise ValueError("This source table covers the seven traditional planets")
    _sign(sign)
    row = DIGNITIES["exaltation_and_depression"][planet]
    return "EXALTATION" if row["exaltation"] == sign else "DEPRESSION" if row["depression"] == sign else "NEITHER"


def triangle_governors(sign: str | None, sect: str | None) -> dict | None:
    if sign is None or sect is None:
        return None
    _sign(sign)
    _sect(sect)
    row = next(r for r in DIGNITIES["triangles"] if sign in r["signs"])
    return {"principal": row["primary_" + sect.lower()], "co_ruler": row["co_ruler_" + sect.lower()]}


def chaldean_rows(sign: str, sect: str) -> list[dict]:
    triangle = _sign(sign) % 4
    _sect(sect)
    spec = TERMS["chaldean_construction"]
    groups = [list(g) for g in spec["triplicity_groups"]]
    groups[2] = list(spec["day_pair" if sect == "DAY" else "night_pair"])
    groups = groups[triangle:] + groups[:triangle]
    order = [p for group in groups for p in group]
    start = 0
    rows = []
    for planet, width in zip(order, spec["length_sequence"], strict=True):
        rows.append({"planet": planet, "length_degrees": width, "computed_start": start, "computed_end": start + width})
        start += width
    return rows


def term_rows(sign: str, scheme: str, sect: str | None = None) -> list[dict]:
    _sign(sign)
    if scheme == "CHALDEAN":
        if sect is None:
            raise ValueError("Chaldean rows require declared DAY/NIGHT")
        return chaldean_rows(sign, sect)
    if scheme not in TERMS["tables"]:
        raise ValueError("Select an explicit source scheme")
    return TERMS["tables"][scheme]["rows"][sign]


def term_owner(sign: str | None, degree: float | None, scheme: str, sect: str | None = None) -> str | None:
    if sign is None or degree is None:
        return None
    if scheme == "CHALDEAN" and sect is None:
        return None
    degree = _number(degree, 0, 30)
    return next(r["planet"] for r in term_rows(sign, scheme, sect) if r["computed_start"] <= degree < r["computed_end"])


def scheme_totals(scheme: str, sect: str | None = None) -> dict[str, int]:
    count: Counter = Counter()
    for sign in SIGNS:
        for row in term_rows(sign, scheme, sect):
            count[row["planet"]] += row["length_degrees"]
    return dict(count)


def chariot_qualifies(familiarities: dict[str, bool | None]) -> bool | None:
    """A cardinality fixture only; caller must supply distinct source familiarities."""
    if not isinstance(familiarities, dict) or not familiarities:
        raise ValueError("Supply distinct named familiarities and explicit unknowns")
    if any(type(x) not in {bool, type(None)} for x in familiarities.values()):
        raise ValueError("Use True, False, or None only")
    true_count = sum(v is True for v in familiarities.values())
    unknown_count = sum(v is None for v in familiarities.values())
    if true_count >= 2:
        return True
    if true_count + unknown_count < 2:
        return False
    return None


def same_ecliptic_side(lat1: float | None, lat2: float | None) -> bool | None:
    """Minimal same-side reading only, not a complete application detector.

    Robbins also says 'same latitude'; numeric equality/tolerance remains unresolved.
    """
    if lat1 is None or lat2 is None:
        return None
    a = _number(lat1, -90, 90, closed_high=True)
    b = _number(lat2, -90, 90, closed_high=True)
    if a == 0 or b == 0:
        return None
    return (a > 0) == (b > 0)


def term_table_disagreement() -> dict:
    """Exact arc-length comparison of two printed tables, not predictive accuracy."""
    per_sign = {}
    for sign in SIGNS:
        a = term_rows(sign, "EGYPTIAN_ROBBINS_ADOPTED")
        b = term_rows(sign, "PTOLEMY_ROBBINS_ADOPTED")
        cuts = sorted({r[k] for rows in (a, b) for r in rows for k in ("computed_start", "computed_end")})
        per_sign[sign] = sum(hi - lo for lo, hi in zip(cuts, cuts[1:]) if term_owner(sign, (hi + lo) / 2, "EGYPTIAN_ROBBINS_ADOPTED") != term_owner(sign, (hi + lo) / 2, "PTOLEMY_ROBBINS_ADOPTED"))
    return {"different_degrees": sum(per_sign.values()), "total_degrees": 360, "per_sign": per_sign, "interpretation": "Arc-length difference in adopted term-ruler assignments, not predictive performance or a population frequency"}
