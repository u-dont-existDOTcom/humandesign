"""Historically witnessed *by-sign* monomoiria, separate from by-trigon C04.

Ancient documentary parity experiment on P.Berl. 9825 (a horoscope dated
319 CE), analyzed by Dorian Gieseler Greenbaum and Alexander Jones, 2017,
ISAW Papers 12 pp.13-14, 31. The paper cites Paulus Introductory Matters
chapter 5: start at the sign's domicile lord for its ordinal first degree;
advance in Chaldean sequence for each subsequent degree.

This does NOT validate astrological prediction. It checks how many
transmitted ancient *written calculations* the simple rule reconstructs.
The one source-reported Mercury error must remain a negative result.
No human biography or living person's birth data are evaluated.
"""
from __future__ import annotations
from dataclasses import dataclass

CHALDEAN_SEQUENCE = (
    "Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"
)
SIGN_DOMICILE = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
    "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
    "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
    "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}


@dataclass(frozen=True)
class PapyrusRow:
    body: str
    sign: str
    complete_degrees: int
    minutes: int
    papyrus_ruler: str
    textual_status: str


# Source: original 319 CE horoscope as published in Greenbaum & Jones 2017,
# PDF pages 13-14 (translation); comments on p31, esp. Mercury error.
# The Jupiter phrase 'in its own monomoiria' is referentially ambiguous
# and is excluded until adjudicated; no label inferred from it.
PAPYRUS_ROWS = (
    PapyrusRow("Moon", "Cancer", 26, 0, "Venus",
               "MOON_MINUTES_NOT_IN_TRANSLATION_RECONSTRUCTION"),
    PapyrusRow("Saturn", "Aries", 3, 43, "Mercury", "MATCH"),
    PapyrusRow("Mars", "Scorpio", 22, 32, "Sun", "MATCH"),
    PapyrusRow("Venus", "Libra", 29, 18, "Mercury", "MATCH"),
    PapyrusRow("Mercury", "Sagittarius", 13, 53, "Mars",
               "SOURCE_REPORTED_ERROR"),
    PapyrusRow("Ascending node", "Scorpio", 9, 40, "Venus", "MATCH"),
    PapyrusRow("Descending node", "Taurus", 9, 40, "Moon", "MATCH"),
)


def sign_monomoiria(sign: str, complete_degrees: int, minutes: int) -> str:
    """Ruler for a physical longitude within a 30-degree sign.

    Ordinal first degree is the interval [0°,1°), not the completed
    degree integer 1. Any 0..59 arcminutes belong to that interval.
    """
    if sign not in SIGN_DOMICILE:
        raise ValueError("unknown sign")
    if type(complete_degrees) is not int or not (0 <= complete_degrees < 30):
        raise ValueError("degrees outside sign or not exact integer")
    if type(minutes) is not int or not (0 <= minutes < 60):
        raise ValueError("arcminutes outside 0..59 or not exact integer")
    start=CHALDEAN_SEQUENCE.index(SIGN_DOMICILE[sign])
    return CHALDEAN_SEQUENCE[(start+complete_degrees)%7]


def documented_papyrus_check() -> dict:
    rows=[]
    for r in PAPYRUS_ROWS:
        calculated=sign_monomoiria(r.sign,r.complete_degrees,r.minutes)
        rows.append({"body":r.body,"ruler_in_text":r.papyrus_ruler,
                    "calculated_ruler":calculated,"agrees":calculated==r.papyrus_ruler,
                    "textual_status":r.textual_status})
    return {"source":"Greenbaum-Jones-2017-PBerl9825",
            "kind":"historical_calculation_transmission_not_human_validation",
            "checked_rows":len(rows),
            "disagreements":sum(not r["agrees"] for r in rows),
            "records":rows}


if __name__=="__main__":
    import json
    print(json.dumps(documented_papyrus_check(),indent=2))
