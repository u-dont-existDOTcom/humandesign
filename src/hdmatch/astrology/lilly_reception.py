"""First-edition 1647 Lilly p.112 mutual reception, source-limited research.

Reciprocal zodiacal essential dignities are NOT mutual occupation of
mundane houses. Table p.115 awards alternative +5 (by domicile) and +4
(by exaltation) to a planet, not extra cumulative +5/+4 on top of the
same component. No full natal-strength verdict or empirical claim.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .lilly_essential_dignity import (
    CLASSICAL,
    DOMICILE,
    EXALTATION,
    SIGNS,
    TRIPLICITY_DAY,
    TRIPLICITY_NIGHT,
)

MODES = ("domicile", "exaltation", "triplicity", "term", "face")


@dataclass(frozen=True, slots=True)
class DignityPlacement:
    planet: str
    zodiac_sign: str
    chart_sect: str
    term_ruler: str
    face_ruler: str

    def __post_init__(self) -> None:
        if self.planet not in CLASSICAL:
            raise ValueError("only seven classical planets can participate")
        if self.zodiac_sign not in SIGNS:
            raise ValueError("invalid tropical sign")
        if self.chart_sect not in ("day", "night"):
            raise ValueError("sect must be explicit day or night")
        if self.term_ruler not in CLASSICAL or self.face_ruler not in CLASSICAL:
            raise ValueError("source term and face rulers must be classical")


@dataclass(frozen=True, slots=True)
class ReceptionEvidence:
    planet_a: str
    planet_b: str
    a_in_b_modes: tuple[str, ...]
    b_in_a_modes: tuple[str, ...]
    same_mode_receptions: tuple[str, ...]
    mixed_only: bool
    source_house_reception_alternative_points: int
    source_exaltation_reception_alternative_points: int
    full_lilly_radix_strength: str = "UNRESOLVED"

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def host_rulers(placement: DignityPlacement) -> dict[str, str | None]:
    """Which body hosts this zodiacal position by each dignity class."""
    sign = SIGNS.index(placement.zodiac_sign)
    domicile_hosts = [body for body, signs in DOMICILE.items() if sign in signs]
    exaltation_hosts = [body for body, index in EXALTATION.items() if index == sign]
    if len(domicile_hosts) != 1 or len(exaltation_hosts) > 1:
        raise AssertionError("malformed original sign-dignity table")
    triplicity = TRIPLICITY_DAY if placement.chart_sect == "day" else TRIPLICITY_NIGHT
    return {
        "domicile": domicile_hosts[0],
        "exaltation": exaltation_hosts[0] if exaltation_hosts else None,
        "triplicity": triplicity[sign],
        "term": placement.term_ruler,
        "face": placement.face_ruler,
    }


def reception_between(a: DignityPlacement, b: DignityPlacement) -> ReceptionEvidence | None:
    """Same-mode evidence is p.112-attested; mixed types are explicitly NOT scored.

    Tests whether each planet occupies a sign/term/face whose ruler is
    the other planet. Source says reception is reciprocal, not a one-sided
    placement, and p.115 contains only sign and exaltation alternatives.
    """
    if a.planet == b.planet:
        raise ValueError("reception needs two distinct planets")
    if a.chart_sect != b.chart_sect:
        raise ValueError("both planets belong to the SAME birth chart and sect")
    hosted_a = host_rulers(a)
    hosted_b = host_rulers(b)
    a_in_b = tuple(kind for kind in MODES if hosted_a[kind] == b.planet)
    b_in_a = tuple(kind for kind in MODES if hosted_b[kind] == a.planet)
    if not (a_in_b and b_in_a):
        return None
    same = tuple(kind for kind in MODES if kind in a_in_b and kind in b_in_a)
    return ReceptionEvidence(
        planet_a=a.planet,
        planet_b=b.planet,
        a_in_b_modes=a_in_b,
        b_in_a_modes=b_in_a,
        same_mode_receptions=same,
        mixed_only=not bool(same),
        source_house_reception_alternative_points=5 if "domicile" in same else 0,
        source_exaltation_reception_alternative_points=4 if "exaltation" in same else 0,
    )


def all_chart_receptions(
    positions: tuple[DignityPlacement, ...],
) -> tuple[ReceptionEvidence, ...]:
    """One unordered pair per independent relation; no vote duplication."""
    from itertools import combinations

    if len(positions) != 7 or {p.planet for p in positions} != set(CLASSICAL):
        raise ValueError("exactly one of each seven classical planets is required")
    if len({p.chart_sect for p in positions}) != 1:
        raise ValueError("positions must use one internally consistent chart sect")
    sorted_planets = sorted(positions, key=lambda x: x.planet)
    return tuple(
        result
        for a, b in combinations(sorted_planets, 2)
        if (result := reception_between(a, b)) is not None
    )
