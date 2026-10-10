"""Bounded historical-source helpers for Lilly II.XLIV's opening block.

These helpers select source evidence and evaluate caller-qualified clauses.
They do not calculate a horoscope, diagnose an illness, select treatment,
estimate survival, or combine testimonies into a prediction.
"""

from dataclasses import dataclass
from fractions import Fraction
import copy
import json
from pathlib import Path

SATISFIED = "SATISFIED"
CONTRADICTED = "CONTRADICTED"
UNKNOWN = "UNKNOWN"
MEAN_MOON_ARCSECONDS = 13 * 3600 + 10 * 60 + 36
RETROGRADE_ANALOGY_ARCSECONDS = 13 * 3600 + 10 * 60


def _boolean_or_unknown(value):
    if value is not None and type(value) is not bool:
        raise TypeError("Source predicates require bool or None, not truthy values")
    return value


def all_facts(*values):
    """Three-valued conjunction; an absent fact is not a negative fact."""
    checked = [_boolean_or_unknown(value) for value in values]
    if False in checked:
        return CONTRADICTED
    if None in checked:
        return UNKNOWN
    return SATISFIED


def _not(value):
    _boolean_or_unknown(value)
    return None if value is None else not value


@dataclass(frozen=True)
class TimeEvidence:
    """Whether a specified source event's time can be obtained.

    An event token identifies the supplied time without converting calendars.
    False means specifically unavailable. None means availability unknown.
    """

    available: bool | None
    event_token: str | None = None

    def __post_init__(self):
        _boolean_or_unknown(self.available)
        if self.available is True:
            if not isinstance(self.event_token, str) or not self.event_token.strip():
                raise ValueError("Available time evidence needs a nonempty event token")
        elif self.event_token is not None:
            raise ValueError("Unavailable or unknown evidence cannot assert an event time")


TIME_KEYS = (
    "enforced_bed_or_rest",
    "first_urine_inquiry",
    "physician_first_speaking",
    "physician_first_access",
    "physician_first_urine_receipt",
)


def select_source_time(evidence):
    """Preserve the ordered fallback on PDF277, without ranking stage-3 options.

    Missing keys mean UNKNOWN. The first slight symptom is not an admitted
    key. The three physician alternatives have no source-defined precedence.
    """
    extra = set(evidence) - set(TIME_KEYS)
    if extra:
        raise ValueError(f"Unrecognized source-time events: {sorted(extra)}")
    values = {key: evidence.get(key, TimeEvidence(None)) for key in TIME_KEYS}
    if any(not isinstance(item, TimeEvidence) for item in values.values()):
        raise TypeError("Each event requires TimeEvidence")
    for stage, key in enumerate(TIME_KEYS[:2], start=1):
        item = values[key]
        if item.available is None:
            return {"status": UNKNOWN, "stage": stage, "candidates": [], "blocking_event": key}
        if item.available:
            return {"status": "SELECTED", "stage": stage,
                    "candidates": [{"event": key, "token": item.event_token}]}
    candidates = [{"event": key, "token": values[key].event_token}
                  for key in TIME_KEYS[2:] if values[key].available is True]
    unknown = [key for key in TIME_KEYS[2:] if values[key].available is None]
    if unknown:
        return {"status": UNKNOWN, "stage": 3, "candidates": candidates,
                "unresolved_alternatives": unknown}
    if not candidates:
        return {"status": "UNAVAILABLE", "stage": 3, "candidates": []}
    distinct_times = {candidate["token"] for candidate in candidates}
    return {"status": "SELECTED" if len(distinct_times) == 1 else "CHOICE_UNRESOLVED",
            "stage": 3, "candidates": candidates}


def _rational(value):
    if type(value) not in (int, Fraction):
        raise TypeError("Use an exact integer or Fraction")
    return Fraction(value)


def moon_speed_comparisons(daily_motion_arcseconds):
    """Two different historical comparisons, not a physical retrograde result.

    PDF286 names mean motion; retained PDF114 supplies 13d10m36s.
    The distinct analogy on PDF114 uses strictly less than 13d10m.
    Equality is outside each strictly-less-than predicate.
    """
    if daily_motion_arcseconds is None:
        return {"below_stated_mean": None, "under_retrograde_analogy_threshold": None}
    speed = _rational(daily_motion_arcseconds)
    if speed < 0:
        raise ValueError("This historical comparison accepts nonnegative daily travel")
    return {"below_stated_mean": speed < MEAN_MOON_ARCSECONDS,
            "under_retrograde_analogy_threshold": speed < RETROGRADE_ANALOGY_ARCSECONDS}


def remaining_degrees_in_sign(degrees, minutes=None, seconds=None):
    """Exact remaining arc only; missing coordinate components stay unknown.

    This does not decide whether the source's number means months, weeks or
    days (PDF283). Supply each component explicitly, including a known zero.
    """
    for value, upper in ((degrees, 30), (minutes, 60), (seconds, 60)):
        if value is not None:
            number = _rational(value)
            if not 0 <= number < upper:
                raise ValueError("Coordinate component outside its within-sign range")
    if any(value is None for value in (degrees, minutes, seconds)):
        return {"remaining_degrees": None, "time_unit": None}
    position = _rational(degrees) + _rational(minutes) / 60 + _rational(seconds) / 3600
    return {"remaining_degrees": Fraction(30) - position, "time_unit": None}


def benevolent_sixth_predicate(*, benevolent, well_fortified, in_sixth, author_of_disease):
    """Only the PDF284 clause's prerequisites, including its explicit exclusion."""
    return all_facts(benevolent, well_fortified, in_sixth, _not(author_of_disease))


def declining_moon_saturn_predicate(*, light_decreasing, motion_decreasing,
                                   applying_conjunction_square_or_opposition,
                                   disease_already_decreasing):
    """Only the PDF286 adverse clause, with its already-declining exception."""
    return all_facts(light_decreasing, motion_decreasing,
                     applying_conjunction_square_or_opposition,
                     _not(disease_already_decreasing))


def source_lookup(namespace, key, *, path=None):
    """Retrieve a stated historical correspondence, retaining its own namespace.

    No inferred house-to-sign mapping, modern diagnostic synonym, missing
    star minutes, or unlisted planet-in-sign cell is supplied.
    """
    location = Path(path) if path is not None else Path(__file__).with_name("REFERENCE_TABLES.json")
    tables = json.loads(location.read_text(encoding="utf-8"))["namespaces"]
    if namespace not in tables:
        raise KeyError(f"Unknown source namespace: {namespace}")
    exact_key = str(key)
    if exact_key not in tables[namespace]:
        raise KeyError(f"Unrecorded source key: {namespace}/{exact_key}")
    return copy.deepcopy(tables[namespace][exact_key])
