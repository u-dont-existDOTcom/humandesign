"""Static source-table arithmetic for Lilly's Chapter XXXVIII purchase figure.

The unchanged B02f helper supplies longitude, circular separation, aspect
residual, Fortune and turned-house arithmetic. Printed coordinates remain
separate from computed values. No ephemeris, contact dates, global orb rule,
interpretive cusp influence, or predictive accuracy is computed.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
HELPER = ROOT.parent / "B02f" / "lilly_presence_ship_reference.py"
SPEC = importlib.util.spec_from_file_location("retained_lilly_fourth_geometry", HELPER)
if SPEC is None or SPEC.loader is None:
    raise ImportError(f"Retained sibling helper is required: {HELPER}")
GEO = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GEO)

SOURCE_TABLE = ROOT / "WORKED_NUMERIC_TABLES.json"
LILLY_FORTUNE_PROFILE = "Lilly_XXIII_p143_144_same_by_day_and_night"
MONTH_NAMES = {"March": 3, "April": 4, "May": 5}
SPRING_MONTH_LENGTHS = {3: 31, 4: 30, 5: 31}
SPRING_MONTH_OFFSETS = {3: 0, 4: 31, 5: 61}


def exact_longitude(row: dict) -> int:
    """Reject an incomplete coordinate; an omitted minute never becomes zero."""
    coordinate = row.get("coordinate")
    if not isinstance(coordinate, dict):
        raise ValueError("A source coordinate object is required")
    if any(coordinate.get(k) is None for k in ("sign", "degree", "minute")):
        raise ValueError("Complete source sign, degree and minute are required")
    return GEO.longitude(coordinate["sign"], coordinate["degree"], coordinate["minute"])


def _position(value: int) -> int:
    """Use the retained position validator through its public representation."""
    GEO.as_sign(value)
    return value


def forward_gap(origin: int, target: int) -> int:
    """Directed forward distance on the zodiac, in integer arcminutes."""
    return (_position(target) - _position(origin)) % GEO.CIRCLE


def in_forward_half_open_sector(position: int, start: int, end: int) -> bool:
    """Membership in the supplied [start, end) arc, not an influence rule.

    This requires only two complete bounding cusps. It does not reconstruct
    other missing cusps or assign a complete twelve-house chart.
    """
    width = forward_gap(start, end)
    if width == 0:
        raise ValueError("Coincident bounds do not define an admitted sector")
    return forward_gap(start, position) < width


def _angle(arcminutes: int) -> dict:
    if type(arcminutes) is not int or arcminutes < 0:
        raise ValueError("Expected nonnegative integer arcminutes")
    degree, minute = divmod(arcminutes, 60)
    return {"arcminutes": arcminutes, "degrees": degree, "minutes": minute}


def _coordinate(longitude: int) -> dict:
    sign, degree, minute = GEO.as_sign(longitude)
    return {"sign": sign, "degree": degree, "minute": minute}


def compare_fortune(ascendant: int, moon: int, sun: int, printed: int, *, profile: str) -> dict:
    """Compare the given printed point to a separately computed explicit profile."""
    computed = GEO.fortune(ascendant, moon, sun, profile=profile)
    return {
        "profile": profile,
        "profile_source": "Retained Lilly XXIII printed143-144; not restated in XXXVIII",
        "same_formula_by_day_and_night": True,
        "formula": "(Ascendant + Moon - Sun) modulo21600 arcminutes",
        "printed": {"coordinate": _coordinate(printed), "longitude_arcminutes": _position(printed)},
        "computed": {"coordinate": _coordinate(computed), "longitude_arcminutes": computed},
        "printed_matches_computed": printed == computed,
        "shortest_discrepancy": _angle(GEO.separation(printed, computed)),
        "forward_computed_to_printed": _angle(forward_gap(computed, printed)),
        "printed_coordinate_replaced": False,
        "cause_of_discrepancy_inferred": False,
    }


def _spring_ordinal(month: int, day: int) -> int:
    """A bounded March-May ordinal, independent of Julian/Gregorian leap rules."""
    if type(month) is not int or month not in SPRING_MONTH_LENGTHS:
        raise ValueError("Only the admitted March-May calendar interval is supported")
    if type(day) is not int or not 1 <= day <= SPRING_MONTH_LENGTHS[month]:
        raise ValueError("Day is outside the admitted month's fixed length")
    return SPRING_MONTH_OFFSETS[month] + day - 1


def calendar_intervals(question: dict, bargain: dict, completion: dict) -> dict:
    """Keep three named reported events; do not substitute agreement for completion."""
    events = {"question": question, "bargain": bargain, "payment_and_sealing": completion}
    years = [event.get("year") for event in events.values()]
    if any(type(year) is not int for year in years) or len(set(years)) != 1:
        raise ValueError("Three dates in one explicitly identified year are required")
    ordinal = {name: _spring_ordinal(event["month"], event["day"]) for name, event in events.items()}
    if not ordinal["question"] <= ordinal["bargain"] <= ordinal["payment_and_sealing"]:
        raise ValueError("Reported question, bargain and completion must retain chronological order")
    intervals = {}
    for key, start, end in (
        ("question_to_bargain", "question", "bargain"),
        ("bargain_to_payment_and_sealing", "bargain", "payment_and_sealing"),
        ("question_to_payment_and_sealing", "question", "payment_and_sealing"),
    ):
        days = ordinal[end] - ordinal[start]
        weeks, remainder = divmod(days, 7)
        intervals[key] = {"start_event": start, "end_event": end,
                          "days": days, "weeks": weeks, "remaining_days": remainder}
    return {
        "reported_events": deepcopy(events),
        "intervals": intervals,
        "assumption": "One unchanged calendar and year; March31 days, April30 days, May31 days",
        "calendar_system_selected": None,
        "time_of_day_used": False,
        "weekday_or_astronomical_contact_checked": False,
        "completion_endpoint": "payment_and_sealing",
    }


def _unique(rows: list[dict], field: str) -> dict:
    result = {}
    for row in rows:
        key = row[field]
        if key in result:
            raise ValueError(f"Duplicate source entry: {key}")
        result[key] = row
    return result


def _static_positions(chart: dict) -> tuple[dict, dict, list[str]]:
    cusps = _unique(chart["house_cusps"], "house")
    if set(cusps) != set(range(1, 13)):
        raise ValueError("All twelve source cusp records are required, including omissions")
    bodies = _unique(chart["bodies_and_points"], "body")
    expected = {"Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn",
                "NorthNode", "SouthNode", "Fortune"}
    if set(bodies) != expected:
        raise ValueError("Seven planets, two nodes and Fortune must retain their source records")
    rows = {f"H{number:02d}": row for number, row in cusps.items()} | bodies
    source_positions, longitudes, omitted = {}, {}, []
    for name, row in rows.items():
        coordinate = row.get("coordinate")
        if not isinstance(coordinate, dict):
            raise ValueError(f"Missing coordinate object for {name}")
        missing = [key for key in ("sign", "degree", "minute") if coordinate.get(key) is None]
        if missing:
            value = None
            omitted.append(name)
        else:
            value = exact_longitude(row)
        longitudes[name] = value
        source_positions[name] = {
            "entry_id": row["entry_id"],
            "printed_coordinate": deepcopy(coordinate),
            "raw_transcription": row["raw_transcription"],
            "sign_basis": row["sign_basis"],
            "longitude_arcminutes": value,
            "status": "WITHHELD_INCOMPLETE_SOURCE_COORDINATE" if missing else "EXACT_STATIC_LONGITUDE",
            "missing_fields": missing,
        }
    return source_positions, longitudes, omitted


def _required(longitudes: dict, name: str) -> int:
    value = longitudes[name]
    if value is None:
        raise ValueError(f"Required exact input {name} is incomplete; calculation not admitted")
    return value


def _source_calendar(raw: dict, chart: dict) -> dict:
    labels = _unique(chart["central_labels"], "id")
    question_reading = labels["central_date"]["reading"]
    narrative = _unique(raw["narrative_numeric_statements"], "kind")
    bargain = narrative["bargain_date"]
    completion = narrative["payment_date"]
    question = {"year": question_reading["year"], "month": question_reading["month_number"],
                "day": question_reading["day"], "source_anchor": "A253-F",
                "raw": labels["central_date"]["raw"], "year_basis": "printed_in_chart"}
    def event(row: dict) -> dict:
        if row["month"] not in MONTH_NAMES:
            raise ValueError("Narrated date outside the admitted month names")
        return {"year": row["year_inferred_from_case"], "month": MONTH_NAMES[row["month"]],
                "day": row["day"], "source_anchor": row["anchor"], "raw": row["raw"],
                "year_basis": "inferred_from_same_narrated_case"}
    result = calendar_intervals(question, event(bargain), event(completion))
    result["source_elapsed_phrase"] = deepcopy(narrative["author_stated_elapsed_time"])
    result["reported_date_associations_verified"] = False
    return result


def reconcile(source_path: Path | str = SOURCE_TABLE) -> dict:
    """Generate checks directly from the frozen table, without editing its values."""
    source_path = Path(source_path)
    source_bytes = source_path.read_bytes()
    raw = json.loads(source_bytes)
    charts = raw["charts"]
    if len(charts) != 1 or charts[0]["chart_id"] != "CH01":
        raise ValueError("This bounded implementation admits only the actual CH01 purchase figure")
    chart = charts[0]
    positions, longitudes, omitted = _static_positions(chart)
    h1, h7, h8, sun, moon, venus, mars, mercury, saturn, printed_fortune = (
        _required(longitudes, name) for name in
        ("H01", "H07", "H08", "Sun", "Moon", "Venus", "Mars", "Mercury", "Saturn", "Fortune")
    )
    if GEO.FORTUNE_PROFILE != LILLY_FORTUNE_PROFILE:
        raise ValueError("Retained helper Fortune profile differs from the explicitly admitted profile")
    fortune = compare_fortune(h1, moon, sun, printed_fortune, profile=LILLY_FORTUNE_PROFILE)
    fortune["printed_source_entry"] = "CH01-Fortune"
    fortune["printed_source_anchor"] = "A253-F"
    numeric_statements = _unique(raw["narrative_numeric_statements"], "kind")
    checks = {
        "Fortune": fortune,
        "Sun_Venus_gap": {
            "shortest_separation": _angle(GEO.separation(sun, venus)),
            "forward_Venus_to_Sun": _angle(forward_gap(venus, sun)),
            "source_stated_gap": deepcopy(numeric_statements["author_stated_angular_gap"]),
            "source_rounded_statement_replaced": False,
            "universal_degree_to_week_rule_inferred": False,
        },
        "Sun_Saturn_trine": {
            "shortest_separation": _angle(GEO.separation(sun, saturn)),
            "residual_from_120_degrees": _angle(GEO.aspect_residual(sun, saturn, 120)),
            "source_wording": "the Sun was in perfect trine with Saturn",
            "source_anchor": "A254-04",
            "meaning_of_perfect_resolved": False,
        },
        "Moon_Mars_gap": {
            "shortest_separation": _angle(GEO.separation(moon, mars)),
            "forward_Moon_to_Mars": _angle(forward_gap(moon, mars)),
            "translation_or_contact_timing_computed": False,
        },
        "Mercury_to_H08": {
            "forward_distance": _angle(forward_gap(mercury, h8)),
            "shortest_distance": _angle(GEO.separation(mercury, h8)),
            "cusp_influence_threshold_applied": None,
        },
        "Mercury_geometric_H07": {
            "membership": in_forward_half_open_sector(mercury, h7, h8),
            "start_cusp": "H07", "end_cusp": "H08",
            "start_inclusive": True, "end_exclusive": True,
            "start_longitude_arcminutes": h7, "end_longitude_arcminutes": h8,
            "position_longitude_arcminutes": mercury,
            "scope": "Only the forward half-open arc bounded by the two complete printed H7/H8 cusps",
            "full_twelve_house_classification_computed": False,
            "source_drawn_sector": next(row["diagram_house_sector"] for row in chart["bodies_and_points"] if row["body"] == "Mercury"),
            "source_occupancy_wording_reconciled": False,
            "interpretive_cusp_influence_applied": False,
        },
        "Venus_H07_gap": {
            "forward_cusp_to_Venus": _angle(forward_gap(h7, venus)),
            "shortest_distance": _angle(GEO.separation(h7, venus)),
            "numeric_direction": "Venus is after H7 in forward zodiac order",
            "qualitative_nearness_threshold_inferred": None,
        },
        "fifth_from_seventh": {
            "origin_house": 7, "relative_house": 5,
            "radical_house": GEO.turned_house(7, 5),
            "convention": "inclusive house count: origin is relative first",
            "source_anchor": "A255-01",
        },
        "reported_calendar_intervals": _source_calendar(raw, chart),
    }
    return {
        "status": "STATIC_PRINTED_ARITHMETIC_ONLY",
        "role": "calculation_implementation_helper_not_independent_evaluator",
        "source_id": raw["source_id"], "source_sha256": raw["source_sha256"],
        "source_table_filename": source_path.name,
        "source_table_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "source_notes_sha256": raw["frozen_notes_sha256"],
        "retained_helper": "../B02f/lilly_presence_ship_reference.py",
        "retained_helper_sha256": hashlib.sha256(HELPER.read_bytes()).hexdigest(),
        "chart_id": chart["chart_id"],
        "source_positions": positions,
        "skipped_incomplete_exact_positions": omitted,
        "static_longitudes_computed": sum(value is not None for value in longitudes.values()),
        "check_group_count": len(checks),
        "checks": checks,
        "ephemeris_computed": False,
        "physical_contact_times_computed": False,
        "station_or_ingress_dates_computed": False,
        "modern_calendar_resolved": False,
        "global_orb_classification_computed": False,
        "historical_events_independently_verified": False,
        "predictive_accuracy_tested": False,
        "source_predictions_replaced_by_arithmetic": False,
        "source_coordinates_modified": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE_TABLE)
    parser.add_argument("--output", type=Path, default=ROOT / "ARITHMETIC_CHECKS.json")
    args = parser.parse_args()
    if args.source.resolve() == args.output.resolve():
        raise ValueError("Arithmetic output must not overwrite the source table")
    result = reconcile(args.source)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"status": result["status"], "chart_id": result["chart_id"],
                      "static_longitudes": result["static_longitudes_computed"],
                      "check_groups": result["check_group_count"],
                      "printed_Fortune_matches": result["checks"]["Fortune"]["printed_matches_computed"]}))


if __name__ == "__main__":
    main()
