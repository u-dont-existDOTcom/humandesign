"""Reproducible conjunction-only primary-direction timelines, research lane.

Historical method geometry, symbolic time keys, and empirical claims are separate.
This module does NOT judge relationship, death, illness, career, or personality
outcomes, and does not implement aspects/terms/secondary motion.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import asdict, dataclass
from datetime import timedelta
from enum import StrEnum

from .geometry import GeometryMethod, GeometryUnavailable, direction_arc, direction_sense
from .sky import CLASSICAL_BODIES, DirectionBirthSnapshot

MODERN_MEAN_TROPICAL_YEAR_DAYS = 365.2422
METHODS = tuple(GeometryMethod)


class TimeKey(StrEnum):
    PTOLEMY_ONE_EQUINOCTIAL_DEGREE_PER_YEAR = "ptolemy_one_degree_per_year"
    MODERN_MEAN_SOLAR_DIAGNOSTIC = "modern_mean_solar_diagnostic"


def degrees_per_symbolic_year(key: TimeKey) -> float:
    key = TimeKey(key)
    if key is TimeKey.PTOLEMY_ONE_EQUINOCTIAL_DEGREE_PER_YEAR:
        return 1.0
    if key is TimeKey.MODERN_MEAN_SOLAR_DIAGNOSTIC:
        # Contemporary rational mean-solar scaling, *not* the original
        # Lilly Naibod printed table nor Cardan/Brahe historical time key.
        return 360.0 / MODERN_MEAN_TROPICAL_YEAR_DAYS
    raise AssertionError("unknown key")


@dataclass(frozen=True, slots=True)
class DirectionRecord:
    method: str
    time_key: str
    promissor: str
    significator: str
    contact: str
    direction: str
    arc_degrees: float
    symbolic_age_years: float
    model_date_utc: str

    def to_dict(self) -> dict[str, str | float]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class Timeline:
    schema: str
    natal: DirectionBirthSnapshot
    time_key: TimeKey
    methods: tuple[GeometryMethod, ...]
    max_age_years: float
    directions: tuple[DirectionRecord, ...]
    evaluated_pairs: int
    unavailable_by_reason: tuple[tuple[str, int], ...]
    outside_age_window: int

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema,
            "status": "RESEARCH_ONLY_ENGINEERING_VALIDATION_NOT_PREDICTIVE_VALIDATION",
            "scope": "seven classical body promissors; bodily conjunctions to "
            "other classical bodies and exact Asc/MC; no rays/terms/antiscia",
            "birth": {
                "utc": self.natal.birth_utc.isoformat(),
                "geographic_latitude_deg": self.natal.latitude_deg,
                "geographic_longitude_east_deg": self.natal.longitude_east_deg,
                "RAMC_deg": self.natal.ramc_deg,
                "ascendant_ecliptic_longitude_deg": self.natal.ascendant_ecliptic_lon_deg,
                "midheaven_ecliptic_longitude_deg": self.natal.midheaven_ecliptic_lon_deg,
            },
            "astronomy_provenance": self.natal.provenance(),
            "technique_provenance": {
                "methods": [m.value for m in self.methods],
                "time_key": self.time_key.value,
                "time_key_degrees_per_symbolic_year": degrees_per_symbolic_year(self.time_key),
                "model_date_year_length_days": MODERN_MEAN_TROPICAL_YEAR_DAYS,
                "warning": "Modern Gregorian mean-year model dates are not "
                "historically authenticated calendar keys. The modern mean-solar "
                "diagnostic is not the literal 1647 Lilly Naibod table.",
                "direction_sense": "shortest signed arc convention (Morinus-like), "
                "rather than a universal traditional converse definition",
                "no_event_interpretation": True,
            },
            "coverage": {
                "evaluated_method_pair_combinations": self.evaluated_pairs,
                "accepted_records": len(self.directions),
                "unavailable": dict(self.unavailable_by_reason),
                "outside_age_window": self.outside_age_window,
                "max_symbolic_age_years": self.max_age_years,
            },
            "directions": [r.to_dict() for r in self.directions],
        }


def generate_timeline(
    natal: DirectionBirthSnapshot,
    *,
    methods: Iterable[GeometryMethod] = METHODS,
    time_key: TimeKey = TimeKey.PTOLEMY_ONE_EQUINOCTIAL_DEGREE_PER_YEAR,
    max_age_years: float = 100.0,
) -> Timeline:
    """Return method-separated arcs/ages, not event predictions.

    Every accepted contact is one bodily conjunction. No retrospective
    outcome data is consumed; there is no birth-time rectification or
    selection of whichever method matches an event.
    """
    method_set = tuple(dict.fromkeys(GeometryMethod(m) for m in methods))
    if not method_set:
        raise ValueError("at least one historical geometry must be chosen")
    if not 0 < max_age_years <= 125:
        raise ValueError("max_age_years must be within (0,125]")
    time_key = TimeKey(time_key)
    points = natal.lookup()
    body_names = tuple(x.value for x in CLASSICAL_BODIES)
    missing = set(body_names + ("asc", "mc")) - set(points)
    if missing:
        raise ValueError(f"natal snapshot lacks required bodies/angles: {sorted(missing)}")
    results: list[DirectionRecord] = []
    failures: dict[str, int] = {}
    evaluated = out_of_window = 0
    for name in body_names:
        promissor = points[name]
        for target in body_names + ("asc", "mc"):
            if target == name:
                continue
            fixed = points[target]
            for method in method_set:
                evaluated += 1
                try:
                    raw = direction_arc(
                        method, natal.latitude_deg, natal.ramc_deg, fixed, promissor
                    )
                except GeometryUnavailable as exc:
                    key = f"{method.value}:{str(exc)}"
                    failures[key] = failures.get(key, 0) + 1
                    continue
                sense, arc = direction_sense(raw)
                age = arc / degrees_per_symbolic_year(time_key)
                if age > max_age_years:
                    out_of_window += 1
                    continue
                # One well-declared modern model-date convention, not an event
                # forecast or a claim about the sources' calendar procedures.
                model_date = natal.birth_utc + timedelta(days=age * MODERN_MEAN_TROPICAL_YEAR_DAYS)
                results.append(
                    DirectionRecord(
                        method=method.value,
                        time_key=time_key.value,
                        promissor=name,
                        significator=target,
                        contact="body_conjunction" if target in body_names else "body_to_angle",
                        direction=sense,
                        arc_degrees=arc,
                        symbolic_age_years=age,
                        model_date_utc=model_date.isoformat(),
                    )
                )
    results.sort(
        key=lambda x: (
            x.symbolic_age_years,
            x.method,
            x.promissor,
            x.significator,
        )
    )
    return Timeline(
        schema="astro-primary-directions-conjunction-timeline-v1",
        natal=natal,
        time_key=time_key,
        methods=method_set,
        max_age_years=max_age_years,
        directions=tuple(results),
        evaluated_pairs=evaluated,
        unavailable_by_reason=tuple(sorted(failures.items())),
        outside_age_window=out_of_window,
    )
