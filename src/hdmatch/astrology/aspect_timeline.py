"""Method-separated direction timelines of zodiacal rays and mundane phase aspects.

Neither ray construction is interchangeable with the bodily-conjunction engine,
nor are the resulting symbolic dates human predictions. Source:
GANSTEN_PRIMARY_DIRECTIONS_AUDIT.md §§1.3,2.1,3.3, Ch.5 pp.65–70,
Ch.8 pp.88–92 (as reported in the research audit).

Unsupported historical latitude constructions (Bianchini, Morin orbital
maximum, Placidus aspect subtleties) remain intentionally unavailable.
"""

from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from datetime import timedelta
from enum import StrEnum

from .aspect_points import (
    ASPECT_DEGREES,
    RayAspect,
    aspect_branches,
    ecliptic_to_equatorial,
    mundane_semi_arc_phase_arc,
    zodiacal_promissor_ray,
)
from .geometry import (
    GeometryMethod,
    GeometryUnavailable,
    direction_arc,
    direction_sense,
)
from .sky import CLASSICAL_BODIES, DirectionBirthSnapshot
from .timeline import (
    MODERN_MEAN_TROPICAL_YEAR_DAYS,
    TimeKey,
    degrees_per_symbolic_year,
)


class AspectProfile(StrEnum):
    ZODIACAL_PROMISSOR_RAYS = "zodiacal_promissor_rays"
    MUNDANE_PROPORTIONAL_SEMI_ARC = "mundane_proportional_semi_arc"


class SignificatorProjection(StrEnum):
    RETAIN_BODILY = "retain_bodily"
    PROJECT_TO_ECLIPTIC = "project_to_ecliptic"


@dataclass(frozen=True, slots=True)
class AspectDirectionRecord:
    method: str
    time_key: str
    profile: str
    promissor: str
    significator: str
    significator_projection: str
    ray_aspect: str
    ray_offset_branch: str
    aspect_angle_degrees: float
    aspect_coordinate_frame: str
    ray_ecliptic_longitude_degrees: float | None
    ray_ecliptic_latitude_degrees: float | None
    direction: str
    arc_degrees: float
    symbolic_age_years: float
    model_date_utc: str

    def to_dict(self) -> dict[str, str | float | None]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class AspectTimeline:
    schema: str
    natal: DirectionBirthSnapshot
    profile: AspectProfile
    significator_projection: SignificatorProjection
    time_key: TimeKey
    methods: tuple[GeometryMethod, ...]
    aspects: tuple[RayAspect, ...]
    max_age_years: float
    directions: tuple[AspectDirectionRecord, ...]
    evaluated: int
    rejected: tuple[tuple[str, int], ...]
    outside_age_window: int

    def to_dict(self) -> dict[str, object]:
        kind = (
            "λ_promissor ± ψ, projected to equator at β_ray=0°"
            if self.profile is AspectProfile.ZODIACAL_PROMISSOR_RAYS
            else "u_promissor reaches u_significator ± ψ in normalized semi-arc phase"
        )
        return {
            "schema_version": self.schema,
            "status": "RESEARCH_ONLY_ASPECT_GEOMETRY_NOT_PREDICTIVE_VALIDATION",
            "scope": {
                "profile": self.profile.value,
                "contact": kind,
                "promissors": "seven classical natal planets only",
                "significators": "other classical planets, exact natal ASC/MC",
                "aspect_names": [a.value for a in self.aspects],
                "method_names": [m.value for m in self.methods],
                "branch_convention": (
                    "positive/negative angle offsets in the named coordinate frame"
                ),
                "opposition_unique_branch": True,
                "zodiacal_ray_latitude": (
                    "β=0°; Bianchini/Morin alternatives not implemented"
                    if self.profile is AspectProfile.ZODIACAL_PROMISSOR_RAYS
                    else None
                ),
                "significator_projection": self.significator_projection.value,
                "latitude_angle_exception": (
                    "Angle significators remain actual angular circles even when "
                    "the planetary significator projection is set to ecliptic."
                ),
                "not_implemented": [
                    "historical Bianchini/Morin ray latitude",
                    "mundane Regiomontanian/under-pole ray methods",
                    "planetary secondary motion",
                    "aspects belonging to significators",
                    "historical traditional-converse role reversal",
                    "terms/bounds, lots, stars, antiscia, intermediate cusps",
                ],
            },
            "birth": {
                "utc": self.natal.birth_utc.isoformat(),
                "latitude_north_deg": self.natal.latitude_deg,
                "longitude_east_deg": self.natal.longitude_east_deg,
                "ramc_deg": self.natal.ramc_deg,
            },
            "astronomy_provenance": {
                **self.natal.provenance(),
                "true_obliquity_of_date_deg": self.natal.true_obliquity_deg,
            },
            "method_provenance": {
                "source_locator": "Gansten Primary Directions (2009), Ch.5 pp.65–70, "
                "Ch.8 pp.88–92; research audit §§1.3,2.1,3.3",
                "mundane_phase_status": "independent analytic reconstruction of "
                "equal normalized semi-arc phase, not a universal primary-source "
                "algorithm attributed to every astrologer",
                "time_key": self.time_key.value,
                "time_key_degrees_per_symbolic_year": degrees_per_symbolic_year(self.time_key),
                "calendar_model_year_days": MODERN_MEAN_TROPICAL_YEAR_DAYS,
                "date_warning": "model dates are symbolic modern mean-year conversions, "
                "not literal Lilly Naibod tables or verified historical calendars",
                "direction_sense": "shortest-signed-arc convention, not traditional "
                "role-reversed converse",
            },
            "coverage": {
                "evaluated": self.evaluated,
                "accepted": len(self.directions),
                "unavailable": dict(self.rejected),
                "outside_age_window": self.outside_age_window,
                "max_symbolic_age_years": self.max_age_years,
            },
            "directions": [d.to_dict() for d in self.directions],
        }


def generate_aspect_timeline(
    natal: DirectionBirthSnapshot,
    *,
    profile: AspectProfile,
    methods: Iterable[GeometryMethod] | None = None,
    aspects: Iterable[RayAspect] = tuple(RayAspect),
    significator_projection: SignificatorProjection = SignificatorProjection.RETAIN_BODILY,
    time_key: TimeKey = TimeKey.PTOLEMY_ONE_EQUINOCTIAL_DEGREE_PER_YEAR,
    max_age_years: float = 100.0,
) -> AspectTimeline:
    """Calculate only the declared ray/phase geometry; never use event answers."""
    profile = AspectProfile(profile)
    significator_projection = SignificatorProjection(significator_projection)
    time_key = TimeKey(time_key)
    if methods is None:
        methods = (
            (GeometryMethod.PROPORTIONAL_SEMI_ARC,)
            if profile is AspectProfile.MUNDANE_PROPORTIONAL_SEMI_ARC
            else tuple(GeometryMethod)
        )
    method_set = tuple(dict.fromkeys(GeometryMethod(m) for m in methods))
    aspect_set = tuple(dict.fromkeys(RayAspect(a) for a in aspects))
    if not method_set or not aspect_set:
        raise ValueError("select at least one geometry and one aspect type")
    if not math.isfinite(max_age_years) or not 0 < max_age_years <= 125:
        raise ValueError("max_age_years must be finite and in (0,125]")
    if profile is AspectProfile.MUNDANE_PROPORTIONAL_SEMI_ARC:
        if method_set != (GeometryMethod.PROPORTIONAL_SEMI_ARC,):
            raise ValueError("mundane phase reconstruction has proportional semi-arcs only")
        if significator_projection is not SignificatorProjection.RETAIN_BODILY:
            raise ValueError(
                "mundane phase requires bodily coordinates; zodiacal projection not defined"
            )
    else:
        if natal.true_obliquity_deg is None or len(natal.ecliptic_lookup()) < len(CLASSICAL_BODIES):
            raise ValueError("zodiacal rays require Swiss ecliptic longitudes and true obliquity")

    body_names = tuple(x.value for x in CLASSICAL_BODIES)
    points = natal.lookup()
    missing = set(body_names + ("asc", "mc")) - set(points)
    if missing:
        raise ValueError(f"natal state lacks required bodies/angles: {sorted(missing)}")
    ecl = natal.ecliptic_lookup()
    out: list[AspectDirectionRecord] = []
    errors: dict[str, int] = {}
    evaluated = outside = 0

    for prom_name in body_names:
        bodily_promissor = points[prom_name]
        for target_name in body_names + ("asc", "mc"):
            # The traditional source registry excludes a planet directed to its
            # own natal significator from this first test profile.
            if prom_name == target_name:
                continue
            fixed = points[target_name]
            fixed_projection = SignificatorProjection.RETAIN_BODILY.value
            if target_name in ("asc", "mc"):
                fixed_projection = "exact_angle"
            elif significator_projection is SignificatorProjection.PROJECT_TO_ECLIPTIC:
                if target_name not in ecl:
                    raise ValueError(f"missing ecliptic state for significator {target_name}")
                lon, _lat = ecl[target_name]
                assert natal.true_obliquity_deg is not None
                fixed = ecliptic_to_equatorial(lon, 0, natal.true_obliquity_deg)
                fixed_projection = SignificatorProjection.PROJECT_TO_ECLIPTIC.value
            for aspect in aspect_set:
                for branch in aspect_branches(aspect):
                    if profile is AspectProfile.ZODIACAL_PROMISSOR_RAYS:
                        if prom_name not in ecl:
                            raise ValueError(f"missing ecliptic state for promissor {prom_name}")
                        lon, _lat = ecl[prom_name]
                        assert natal.true_obliquity_deg is not None
                        ray = zodiacal_promissor_ray(
                            lon,
                            aspect=aspect,
                            branch=branch,
                            obliquity_deg=natal.true_obliquity_deg,
                        )
                        moving = ray.equatorial
                        ray_lon: float | None = ray.ecliptic_longitude_deg
                        ray_lat: float | None = ray.ecliptic_latitude_deg
                        frame = "tropical_ecliptic_longitude_of_date"
                    else:
                        moving = bodily_promissor
                        ray_lon = ray_lat = None
                        frame = "normalized_proportional_semi_arc_phase"
                    for method in method_set:
                        evaluated += 1
                        try:
                            if profile is AspectProfile.ZODIACAL_PROMISSOR_RAYS:
                                raw = direction_arc(
                                    method, natal.latitude_deg, natal.ramc_deg, fixed, moving
                                )
                            else:
                                raw = mundane_semi_arc_phase_arc(
                                    natal.latitude_deg,
                                    natal.ramc_deg,
                                    fixed,
                                    moving,
                                    aspect=aspect,
                                    branch=branch,
                                )
                        except GeometryUnavailable as exc:
                            key = f"{method.value}:{str(exc)}"
                            errors[key] = errors.get(key, 0) + 1
                            continue
                        sense, arc = direction_sense(raw)
                        age = arc / degrees_per_symbolic_year(time_key)
                        if age > max_age_years:
                            outside += 1
                            continue
                        date = natal.birth_utc + timedelta(
                            days=age * MODERN_MEAN_TROPICAL_YEAR_DAYS
                        )
                        out.append(
                            AspectDirectionRecord(
                                method=method.value,
                                time_key=time_key.value,
                                profile=profile.value,
                                promissor=prom_name,
                                significator=target_name,
                                significator_projection=fixed_projection,
                                ray_aspect=aspect.value,
                                ray_offset_branch=branch.value,
                                aspect_angle_degrees=ASPECT_DEGREES[aspect],
                                aspect_coordinate_frame=frame,
                                ray_ecliptic_longitude_degrees=ray_lon,
                                ray_ecliptic_latitude_degrees=ray_lat,
                                direction=sense,
                                arc_degrees=arc,
                                symbolic_age_years=age,
                                model_date_utc=date.isoformat(),
                            )
                        )
    out.sort(
        key=lambda x: (
            x.symbolic_age_years,
            x.method,
            x.promissor,
            x.significator,
            x.ray_aspect,
            x.ray_offset_branch,
        )
    )
    return AspectTimeline(
        schema="astro-primary-directions-aspect-timeline-v1",
        natal=natal,
        profile=profile,
        significator_projection=significator_projection,
        time_key=time_key,
        methods=method_set,
        aspects=aspect_set,
        max_age_years=max_age_years,
        directions=tuple(out),
        evaluated=evaluated,
        rejected=tuple(sorted(errors.items())),
        outside_age_window=outside,
    )
