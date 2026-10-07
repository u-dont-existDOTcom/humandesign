"""Bounded reference helpers for Robbins's Ptolemy IV.10.

No ephemeris, person data, diagnosis or event prediction is evaluated here.
Astronomical qualifications must be supplied by the caller. Calendar epochs,
zero-based counting and half-open intervals are explicit implementation choices,
not claims that the ancient text settled those conventions.
"""
from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import json
from pathlib import Path
from typing import Any, Literal

BASE = Path(__file__).resolve().parent
TABLES = json.loads((BASE / "TIMING_REFERENCE_TABLES.json").read_text())
PLANETS = ("Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon")
ORIGINS = ("ASC", "Fortune", "Moon", "Sun", "MC")
SIGNS = ("Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
         "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces")
Truth = bool | None
Exact = int | str | Fraction
POLICY = "ZERO_BASED_ELAPSED_HALF_OPEN"


def _member(value: str, options: tuple[str, ...], label: str) -> str:
    if not isinstance(value, str) or value not in options:
        raise ValueError(f"Unknown {label}: {value!r}")
    return value


def _exact_nonnegative(value: Exact) -> Fraction:
    # Reject binary floats so values at 7/3 and 5/2 boundaries remain exact.
    if isinstance(value, bool) or not isinstance(value, (int, str, Fraction)):
        raise TypeError("Use an integer, Fraction, or exact rational string")
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("Invalid exact rational") from exc
    if result < 0:
        raise ValueError("Elapsed intervals cannot be negative")
    return result


def _truth(value: Truth) -> Truth:
    if value is not None and type(value) is not bool:
        raise TypeError("A qualification must be True, False, or None (unknown)")
    return value


def conjunction(*values: Truth) -> Truth:
    checked = [_truth(v) for v in values]
    if False in checked:
        return False
    return None if None in checked else True


def _row(table: str, key: str, value: str) -> dict[str, Any]:
    for row in TABLES[table]:
        if row[key] == value:
            return deepcopy(row)
    raise ValueError(f"No source row for {value!r}")


def natural_age_reference(planet: str) -> dict[str, Any]:
    """Return nominal age arithmetic, never infer a native's exact age ruler."""
    return _row("natural_ages", "planet", _member(planet, PLANETS, "planet"))


def topical_origin_reference(origin: str) -> dict[str, Any]:
    return _row("topical_origins", "origin", _member(origin, ORIGINS, "origin"))


def ingress_scale_reference(planet: str) -> dict[str, Any]:
    """An emphasized scale is not an exclusive permitted ingress."""
    return _row("emphasized_ingress_scales", "planet",
                _member(planet, PLANETS, "planet"))


def _count_contract(epoch_label: str, count_policy: str) -> None:
    if not isinstance(epoch_label, str) or not epoch_label.strip():
        raise ValueError("Supply the externally chosen epoch; no automatic birthday reset")
    if count_policy != POLICY:
        raise ValueError(f"Explicit counting policy required: {POLICY}")


def annual_sign_reference(start_sign: str, completed_year_steps: int, *,
                          epoch_label: str, count_policy: str) -> dict[str, Any]:
    """One sign per caller-supplied completed year, not one degree per year."""
    _member(start_sign, SIGNS, "sign")
    _count_contract(epoch_label, count_policy)
    if type(completed_year_steps) is not int or completed_year_steps < 0:
        raise ValueError("Completed year steps must be a nonnegative integer")
    index = (SIGNS.index(start_sign) + completed_year_steps) % 12
    return {"sign": SIGNS[index], "steps": completed_year_steps,
            "epoch_label": epoch_label, "count_policy": count_policy,
            "source_record": "PT.R64.IV.10.R670",
            "scope": "DECLARED_COUNT_ARITHMETIC_NOT_COMPLETE_CALENDAR_METHOD",
            "sign_ruler": "NOT_COMPUTED_HERE"}


def subperiod_sign_reference(start_sign: str, elapsed_days: Exact, *,
                             level: Literal["monthly", "daily"],
                             convention: str, epoch_label: str,
                             count_policy: str) -> dict[str, Any]:
    """Advance explicit sign counts without normalizing 336 days to a solar year.

    For monthly counting the start sign is supplied from the annual place; for
    daily counting it is supplied from the monthly place. This helper does not
    choose/reset those epochs or distribute dates between incompatible clocks.
    """
    _member(start_sign, SIGNS, "sign")
    _count_contract(epoch_label, count_policy)
    if level not in ("monthly", "daily"):
        raise ValueError("Level must be monthly or daily")
    conventions = TABLES["period_conventions"]
    if convention not in conventions:
        raise ValueError("Select an explicitly recorded complete convention")
    elapsed = _exact_nonnegative(elapsed_days)
    spec = conventions[convention]
    rate = Fraction(spec[f"{level}_days_per_sign"])
    steps = elapsed // rate
    within = elapsed - steps * rate
    return {"sign": SIGNS[(SIGNS.index(start_sign) + steps) % 12],
            "steps": steps, "days_per_sign": str(rate),
            "within_sign_days": str(within), "twelve_sign_days": str(12 * rate),
            "level": level, "convention": convention, "authority": spec["authority"],
            "epoch_label": epoch_label, "count_policy": count_policy,
            "source_records": ["PT.R64.IV.10.R672", "PT.R64.IV.10.R673"]
                if convention == "ROBBINS_MAIN" else
                ["PT.R64.IV.10.R674", "PT.R64.IV.10.R675"],
            "scope": "DECLARED_RATE_ARITHMETIC_ONLY",
            "automatic_civil_year_normalization": False}


def _carriers(values: list[str] | tuple[str, ...] | None) -> list[str] | None:
    if values is None:
        return None
    if not isinstance(values, (list, tuple)):
        raise TypeError("Use a complete qualified carrier list, [] for known absent, or None")
    for value in values:
        _member(value, PLANETS, "planet")
    # Repeated supplied bodies are one carrier, but distinct/tied bodies survive.
    return list(dict.fromkeys(values))


def reconcile_general_lords(*, at_degree_or_aspect: list[str] | None,
                            nearest_preceding: list[str] | None,
                            term_lords: list[str] | None) -> dict[str, Any]:
    """Reconcile already qualified source candidates; no geometry is inferred."""
    direct = _carriers(at_degree_or_aspect)
    preceding = _carriers(nearest_preceding)
    terms = _carriers(term_lords)
    result: dict[str, Any] = {
        "encounter_lords": None, "term_co_rulers": terms,
        "qualification": "CALLER_SUPPLIED_NOT_ASTRONOMICALLY_VERIFIED",
        "source_records": [f"PT.R64.IV.10.R{x}" for x in (661, 662, 663, 664)],
        "term_share_weight": "UNSPECIFIED_BY_PASSAGE",
        "prediction": None,
    }
    if direct is None:
        result.update(status="UNKNOWN_INITIAL_CONTACT", route="UNRESOLVED")
    elif direct:
        result.update(status="REFERENCE_CARRIERS_SELECTED", route="AT_DEGREE_OR_ASPECT",
                      encounter_lords=direct)
    elif preceding is None:
        result.update(status="UNKNOWN_PRECEDING_CONTACT", route="PRECEDING_FALLBACK")
    elif preceding:
        result.update(status="REFERENCE_CARRIERS_SELECTED", route="PRECEDING_FALLBACK",
                      encounter_lords=preceding)
    else:
        result.update(status="NO_SUPPLIED_QUALIFIED_CARRIER", route="PRECEDING_FALLBACK",
                      encounter_lords=[])
    result["term_status"] = "UNKNOWN" if terms is None else "SUPPLIED"
    return result


def directional_measure_reference(origin: str) -> dict[str, Any]:
    """Return the required temporal geometry class; no arc is computed."""
    _member(origin, ORIGINS, "origin")
    if origin == "ASC":
        measure, record = "LOCAL_ASCENSION_TIMES", 665
    elif origin == "MC":
        measure, record = "CULMINATION_TIMES", 666
    else:
        measure, record = "ANGULAR_POSITION_PROPORTION", 667
    return {"origin": origin, "measure": measure,
            "source_record": f"PT.R64.IV.10.R{record}",
            "ordinary_ecliptic_difference_is_substitute": False}


def equivalent_years_reference(origin: str, supplied_times: Exact, *,
                                supplied_measure: str,
                                geometry_qualified: Truth) -> dict[str, Any]:
    """Unit conversion only after caller has established the applicable times."""
    required = directional_measure_reference(origin)
    _truth(geometry_qualified)
    if supplied_measure != required["measure"]:
        raise ValueError("Wrong temporal measure; longitude degrees are not a substitute")
    amount = _exact_nonnegative(supplied_times)
    return {**required, "qualification": "CALLER_SUPPLIED",
            "status": "REFERENCE_UNIT_CONVERSION" if geometry_qualified is True else
                      ("UNQUALIFIED" if geometry_qualified is False else "UNKNOWN_GEOMETRY"),
            "years": str(amount) if geometry_qualified is True else None,
            "event_date": None, "event_outcome": None}


def aspect_context_reference(*, natal_harmonious: Truth,
                             ingress_favorable: Truth,
                             natal_inharmonious: Truth,
                             opposite_sect: Truth,
                             hard_transit_relation: Truth) -> dict[str, Any]:
    """Test two supplied antecedents; neither nontrigger is a favorable forecast."""
    favorable = conjunction(natal_harmonious, ingress_favorable)
    adverse = conjunction(natal_inharmonious, opposite_sect, hard_transit_relation)
    if favorable is True and adverse is True:
        status = "COMPETING_SUPPLIED_TESTIMONY_NO_PRECEDENCE"
    elif favorable is True:
        status = "FAVORABLE_SOURCE_CLAUSE_TRIGGERED"
    elif adverse is True:
        status = "ADVERSE_SOURCE_CLAUSE_TRIGGERED"
    elif favorable is None or adverse is None:
        status = "UNKNOWN_QUALIFICATION"
    else:
        status = "NEITHER_CLAUSE_TRIGGERED_NOT_OPPOSITE_PREDICTION"
    return {"favorable_clause": favorable, "adverse_clause": adverse, "status": status,
            "source_records": ["PT.R64.IV.10.R693", "PT.R64.IV.10.R695",
                               "PT.R64.IV.10.R696"],
            "astronomical_reference_target": "MUST_BE_RESOLVED_EXTERNALLY; see U19",
            "actual_event_inferred": False}


def role_coincidence_reference(*, same_time_and_ingress_lord: Truth,
                               original_natal_ruler: Truth) -> dict[str, Any]:
    """Preserve repeated roles as an interaction, not independent confirmation."""
    same = _truth(same_time_and_ingress_lord)
    original = _truth(original_natal_ruler)
    if same is None:
        state = "UNKNOWN_ROLE_COINCIDENCE"
    elif same is False:
        state = "NOT_TRIGGERED_NOT_WEAK_EVENT_PREDICTION"
    elif original is True:
        state = "SOURCE_INTENSIFICATION_PLUS_ORIGINAL_RULERSHIP"
    elif original is False:
        state = "SOURCE_INTENSIFICATION"
    else:
        state = "SOURCE_INTENSIFICATION_NATAL_ROLE_UNRESOLVED"
    return {"status": state, "valence": "NOT_DETERMINED_BY_COINCIDENCE",
            "independent_confirmations_added": 0,
            "numeric_weight": None,
            "source_records": ["PT.R64.IV.10.R697", "PT.R64.IV.10.R698"]}
