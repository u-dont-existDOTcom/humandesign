"""Isolated Ptolemy I.4-I.8 definitions. Not a natal/event predictor.

This is a test reference for audited wording, not imported by production models.
A supplied phase category is not proof that morning/evening visibility was computed.
The longitude projection and unresolved exact boundaries are project conventions.
"""
from __future__ import annotations
import json
import math
from pathlib import Path

RULES = Path(__file__).with_name("RULES.json")

def record(suffix: str) -> dict:
    data = json.loads(RULES.read_text())
    return next(row for row in data["records"] if row["id"].endswith(suffix))

def planet_classes(planet: str, *, mercury_phase: str | None = None) -> dict:
    """Return historical classifications only, with unresolved Mercury preserved."""
    planet = planet.upper()
    permitted = {"SUN", "MOON", "MERCURY", "VENUS", "MARS", "JUPITER", "SATURN"}
    if planet not in permitted:
        raise ValueError("Only seven source-named bodies are admitted")
    benefic = record("R14")["consequent"]
    polarity = record("R15")["consequent"]
    membership = record("R18")["consequent"]
    out = {
        "benefic_class": next(k for k in ["beneficent", "maleficent", "common"] if planet in benefic[k]),
        "historical_category": next(k for k in ["feminine", "masculine", "common"] if planet in polarity[k]),
        "sect": "UNRESOLVED",
        "person_outcome_claim": None,
    }
    if planet == "MERCURY":
        if mercury_phase not in {None, "MORNING", "EVENING", "UNKNOWN", "BOUNDARY"}:
            raise ValueError("Phase must be explicit MORNING/EVENING/UNKNOWN/BOUNDARY")
        out["sect"] = {"MORNING": "DIURNAL", "EVENING": "NOCTURNAL"}.get(mercury_phase, "UNRESOLVED")
    else:
        out["sect"] = next(k.upper() for k in ["diurnal", "nocturnal"] if planet in membership[k])
    return out

def lunar_phase_quality(sun_longitude: float, moon_longitude: float) -> dict:
    """Project a pair of longitudes into I.8 quarter qualities, not event timing."""
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v)
           for v in (sun_longitude, moon_longitude)):
        raise ValueError("Longitudes must be finite numbers")
    phase = (moon_longitude - sun_longitude) % 360.0
    if phase in {0.0, 90.0, 180.0, 270.0}:
        return {"phase_degrees": phase, "quality": "BOUNDARY_UNRESOLVED", "convention": "PROJECT_OPEN_INTERVAL"}
    keys = ["NEW_TO_FIRST_QUARTER", "FIRST_QUARTER_TO_FULL", "FULL_TO_LAST_QUARTER", "LAST_QUARTER_TO_NEW"]
    index = int(phase // 90.0)
    return {"phase_degrees": phase, "quality": record("R21")["consequent"][keys[index]], "convention": "PROJECT_OPEN_INTERVAL"}
