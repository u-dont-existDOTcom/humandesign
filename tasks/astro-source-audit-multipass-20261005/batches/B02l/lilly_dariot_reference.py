"""Bounded reference operations for Lilly, printed pp. 266–267.

These preserve source inputs and angular arithmetic. They do not diagnose,
forecast a patient's course, select treatment, or calculate calendar dates.
No ephemeris, chart, medical inference, or runtime promotion is supplied.
"""

DEGREE = 3600
CIRCLE = 360 * DEGREE
CRISIS_OFFSETS = (45 * DEGREE, 90 * DEGREE, 135 * DEGREE)
ANCIENT_SIGN_UNITS = {
    "moveable": ("days",),
    "common": ("weeks", "months"),
    "fixed": ("months", "years"),
}
HOUSE_CORRESPONDENCE = {
    "angular": "moveable", "succedent": "common", "cadent": "fixed"
}


def _time_observation(status, value):
    if status not in {"known", "unavailable", "unknown"}:
        raise ValueError("time status must be known, unavailable, or unknown")
    if status == "known":
        if not isinstance(value, str) or not value.strip():
            raise ValueError("a known time requires its supplied nonempty label")
    elif value is not None:
        raise ValueError("an unresolved/unavailable time cannot also carry a value")


def select_crisis_origin(bed_status, bed_time, physician_status, physician_time):
    """Preserve the p.266 priority; unknown is not proof of unavailability.

    A time label is carried verbatim, without calendar/time-zone conversion.
    Moon motion still has to be corrected to the selected hour externally.
    """
    _time_observation(bed_status, bed_time)
    _time_observation(physician_status, physician_time)
    if bed_status == "known":
        return {"status": "selected", "origin": "first_bed_hour", "time": bed_time}
    if bed_status == "unknown":
        return {"status": "unresolved", "origin": None, "time": None,
                "reason": "first_bed_hour_availability_unknown"}
    if physician_status == "known":
        return {"status": "selected", "origin": "first_physician_judgment_request",
                "time": physician_time}
    return {"status": "unresolved", "origin": None, "time": None,
            "reason": "no_available_hour" if physician_status == "unavailable"
            else "physician_request_hour_unknown"}


def crisis_geometry(initial_longitude_arcsec, illness_course, origin_status):
    """Return only the three angular targets stated at p.266.

    The supplied longitude must already be corrected to the chosen hour.
    Actual lunar travel time, contact tolerance, aspect judgment, and clinical
    outcomes are outside this function. No 180-degree or later series is added.
    """
    if illness_course not in {"acute", "chronic", "unknown"}:
        raise ValueError("illness_course must be acute, chronic, or unknown")
    if origin_status not in {"selected", "unresolved"}:
        raise ValueError("origin_status must be selected or unresolved")
    if initial_longitude_arcsec is not None and (
        type(initial_longitude_arcsec) is not int
        or not 0 <= initial_longitude_arcsec < CIRCLE
    ):
        raise ValueError("longitude must be an integer arcsecond in [0, 360 degrees)")
    if illness_course == "chronic":
        return {"status": "not_applicable", "targets_arcsec": (),
                "reason": "this_crisis_passage_excludes_chronic_illness", "dates": None}
    if illness_course == "unknown" or origin_status == "unresolved" or initial_longitude_arcsec is None:
        return {"status": "unresolved", "targets_arcsec": (),
                "reason": "course_origin_or_corrected_longitude_missing", "dates": None}
    return {"status": "angular_targets_only", "offsets_arcsec": CRISIS_OFFSETS,
            "targets_arcsec": tuple((initial_longitude_arcsec + n) % CIRCLE for n in CRISIS_OFFSETS),
            "dates": None, "predictive_outcome": None}


def timing_options(sign_mode, house_class):
    """Keep the Ancients' two input dimensions separate, without choosing a unit.

    Lilly qualifies the table by discretion, the nature of the illness,
    feasibility, motion, and lunar conditions. In particular his common-sign
    procedure does not mechanically choose months, weeks, or days.
    """
    if sign_mode not in {*ANCIENT_SIGN_UNITS, "unknown"}:
        raise ValueError("unknown sign mode")
    if house_class not in {*HOUSE_CORRESPONDENCE, "unknown"}:
        raise ValueError("unknown house class")
    corresponding = HOUSE_CORRESPONDENCE.get(house_class)
    return {"sign_mode": sign_mode, "sign_options": ANCIENT_SIGN_UNITS.get(sign_mode),
            "house_class": house_class, "house_corresponding_mode": corresponding,
            "house_options": ANCIENT_SIGN_UNITS.get(corresponding),
            "selected_unit": None, "date": None,
            "prior_recovery_judgment_required": True,
            "synthesis": "discretion_and_illness_context_not_numerically_specified"}
